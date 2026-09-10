// ============================================================
// IMPORT LIBRARY TYPES ONLY; OPTIONS CONSTRUCTION HAS NO NETWORK.
// ============================================================
import type { BetterAuthOptions } from "better-auth";
import { createAuthEventWriter } from "../../../../../packages/core/src/auth/auth-events.js";
import { evaluatePersonalAlphaAdmission } from "../../../../../packages/core/src/auth/personal-alpha-policy.js";
import {
  AUTH_SPIKE_ERROR_URL,
  AUTH_SPIKE_ORIGIN,
  type LocalAuthConfiguration,
} from "./local-auth-configuration.js";

// ============================================================
// DEFINE THE PRIVATE CAPTURE PORT WITHOUT IMPLEMENTING FILE ACCESS.
// THE NEXT REVIEWED BOOTSTRAP BATCH MUST SUPPLY ACL-CHECKED STORAGE.
// TRUE MEANS VERIFIED PRIVATE WRITE/READBACK, NOT MERELY AN ATTEMPT.
// ============================================================
export interface PrivateIdentityCandidate {
  readonly provider: "google";
  readonly subject: string;
  readonly email: string;
}
export interface LocalAuthPorts {
  readonly captureCandidate?: (candidate: PrivateIdentityCandidate) => Promise<boolean>;
  readonly writeEventLine?: (line: string) => void;
}

// ============================================================
// BUILD FIXED GOOGLE-ONLY OPTIONS; NEVER EXPOSE THIS OBJECT IN LOGS.
// HTTP ROUTES ARE NOT MOUNTED BY M2A-10. DIRECTLY EXPORTING THE
// LIBRARY HANDLER WOULD BYPASS THE FUTURE REQUEST-SCOPE GUARD.
// ============================================================
export function makeLocalBetterAuthOptions(
  configuration: LocalAuthConfiguration,
  ports: LocalAuthPorts = {},
) {
  return {
    appName: "AJAS Personal",
    baseURL: AUTH_SPIKE_ORIGIN,
    basePath: "/api/auth",
    secret: configuration.signingSecret,
    telemetry: { enabled: false, debug: false },
    logger: { disabled: true },
    trustedOrigins: [AUTH_SPIKE_ORIGIN],
    emailAndPassword: { enabled: false },
    plugins: [],
    socialProviders: {
      google: {
        clientId: configuration.clientId,
        clientSecret: configuration.clientSecret,
        disableDefaultScope: true,
        scope: ["openid", "email", "profile"],
        accessType: "online",
        includeGrantedScopes: false,
        prompt: "select_account",
      },
    },
    account: {
      accountLinking: { enabled: false, disableImplicitLinking: true },
      storeAccountCookie: false,
      storeStateStrategy: "cookie",
      skipStateCookieCheck: false,
      encryptOAuthTokens: true,
    },
    session: {
      expiresIn: 900,
      disableSessionRefresh: true,
      cookieCache: { enabled: true, strategy: "jwe", maxAge: 900, refreshCache: false },
    },
    advanced: {
      disableCSRFCheck: false,
      disableOriginCheck: false,
      trustedProxyHeaders: false,
      cookiePrefix: "ajas-local-spike",
      defaultCookieAttributes: { httpOnly: true, sameSite: "lax" },
    },
    rateLimit: { enabled: true, storage: "memory", window: 60, max: 30 },
    onAPIError: {
      errorURL: AUTH_SPIKE_ERROR_URL,
      // ====================================================
      // DISCARD RAW ERRORS AND CONTEXT; LOG ONLY A FIXED CODE.
      // ====================================================
      onError: () => {
        createAuthEventWriter(ports.writeEventLine)("AUTH_PROVIDER_FAILED");
      },
    },
    user: {
      // ====================================================
      // THE LIBRARY MUST VERIFY OAUTH BEFORE THIS ADMISSION HOOK.
      // CALLING THIS FUNCTION DIRECTLY DOES NOT VERIFY A TOKEN.
      // ====================================================
      validateUserInfo: async ({ source }) => {
        const writeEvent = createAuthEventWriter(ports.writeEventLine);
        try {
          const profile = source.oauth?.profile;
          if (
            source.method !== "oauth" ||
            source.action === "link-account" ||
            (source.action !== "create-user" && source.action !== "sign-in") ||
            profile?.email_verified !== true
          ) {
            writeEvent("AUTH_IDENTITY_DENIED");
            return { error: "AJAS_IDENTITY_DENIED" };
          }
          const subject = profile.sub;
          const decision = evaluatePersonalAlphaAdmission(configuration.policy, {
            provider: source.oauth?.providerId,
            subject,
            context: "provider-admission",
          });
          if (decision.allowed) {
            // ================================================
            // ADMISSION IS NOT PROOF THAT A SESSION WAS CREATED.
            // DO NOT LOG AUTH_SESSION_ADMITTED AT THIS POINT.
            // ================================================
            return;
          }
          if (decision.captureCandidate && typeof subject === "string") {
            const email = profile.email;
            if (
              ports.captureCandidate === undefined ||
              typeof email !== "string" ||
              email.length === 0 ||
              email.length > 254 ||
              /\s/u.test(email) ||
              Array.from(email).some((character) => {
                const code = character.charCodeAt(0);
                return code < 32 || (code >= 127 && code <= 159);
              })
            ) {
              writeEvent("AUTH_CAPTURE_FAILED");
              return { error: "AJAS_PRIVATE_CAPTURE_UNAVAILABLE" };
            }
            const captured = await ports.captureCandidate({ provider: "google", subject, email });
            if (captured === true) {
              writeEvent("AUTH_CANDIDATE_CAPTURED");
              return {
                error: "AJAS_DISCOVERY_SESSION_DENIED",
                errorDescription: "Sign-in intentionally stopped for private identity review.",
              };
            }
            writeEvent("AUTH_CAPTURE_FAILED");
            return { error: "AJAS_PRIVATE_CAPTURE_UNAVAILABLE" };
          }
          writeEvent("AUTH_IDENTITY_DENIED");
          return { error: "AJAS_IDENTITY_DENIED" };
        } catch {
          writeEvent("AUTH_IDENTITY_DENIED");
          return { error: "AJAS_IDENTITY_DENIED" };
        }
      },
    },
  } satisfies BetterAuthOptions;
}
