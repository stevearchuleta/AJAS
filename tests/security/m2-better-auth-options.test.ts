// ============================================================
// TEST THE REAL OPTIONS BUILDER WITHOUT NETWORK OR PRIVATE FILES.
// THESE HOOK TESTS DO NOT SUBSTITUTE FOR GOOGLE TOKEN VALIDATION.
// ============================================================
import { describe, expect, it } from "vitest";
import { makeLocalBetterAuthOptions } from "../../apps/web/src/lib/auth/better-auth-options.js";
import type { LocalAuthConfiguration } from "../../apps/web/src/lib/auth/local-auth-configuration.js";

const subject = "SYNTHETIC-SUBJECT";
const configuration = (discovery = false): LocalAuthConfiguration => ({
  policy: {
    mode: discovery ? "discovery" : "allowlist",
    localDevelopment: true,
    allowedGoogleSubject: discovery ? null : subject,
  },
  signingSecret: "SYNTHETIC-TEST-ONLY-SIGNING-SECRET-32-CHARACTERS",
  clientId: "synthetic-client",
  clientSecret: "SYNTHETIC-CLIENT-SECRET",
});
const providerInput = () => ({
  user: {},
  source: {
    action: "create-user" as const,
    method: "oauth" as const,
    oauth: {
      providerId: "google",
      profile: { sub: subject, email: "fixture@example.invalid", email_verified: true },
    },
  },
});

describe("M2 Better Auth fixed options and admission", () => {
  it("explicitly disables telemetry and raw vendor logging", () => {
    const options = makeLocalBetterAuthOptions(configuration());
    expect(options.telemetry).toEqual({ enabled: false, debug: false });
    expect(options.logger.disabled).toBe(true);
    expect(options.socialProviders.google.scope).toEqual(["openid", "email", "profile"]);
    expect(options.socialProviders.google.accessType).toBe("online");
    expect(options.socialProviders.google.includeGrantedScopes).toBe(false);
    expect(options.socialProviders.google.disableDefaultScope).toBe(true);
  });

  it("retains state and origin protections without a persistent database", () => {
    const options = makeLocalBetterAuthOptions(configuration());
    expect(options).not.toHaveProperty("database");
    expect(options).not.toHaveProperty("secondaryStorage");
    expect(options.account.storeStateStrategy).toBe("cookie");
    expect(options.account.skipStateCookieCheck).toBe(false);
    expect(options.account.storeAccountCookie).toBe(false);
    expect(options.account.accountLinking.enabled).toBe(false);
    expect(options.advanced.disableCSRFCheck).toBe(false);
    expect(options.advanced.disableOriginCheck).toBe(false);
    expect(options.advanced.trustedProxyHeaders).toBe(false);
    expect(options.session.expiresIn).toBe(900);
    expect(options.session.disableSessionRefresh).toBe(true);
    expect(options.session.cookieCache).toEqual({
      enabled: true,
      strategy: "jwe",
      maxAge: 900,
      refreshCache: false,
    });
  });

  it("admits the exact verified subject but does not claim session creation", async () => {
    const lines: string[] = [];
    const options = makeLocalBetterAuthOptions(configuration(), {
      writeEventLine: (line) => lines.push(line),
    });
    expect(await options.user.validateUserInfo(providerInput())).toBeUndefined();
    expect(lines.join("")).not.toContain("AUTH_SESSION_ADMITTED");
  });

  for (const action of ["create-user", "sign-in"] as const) {
    it(`denies a wrong subject on ${action}`, async () => {
      const input = providerInput();
      const source = {
        ...input.source,
        action,
        oauth: { ...input.source.oauth, profile: { ...input.source.oauth.profile, sub: "OTHER" } },
      };
      const options = makeLocalBetterAuthOptions(configuration(), {
        writeEventLine: () => undefined,
      });
      expect(await options.user.validateUserInfo({ ...input, source })).toEqual({
        error: "AJAS_IDENTITY_DENIED",
      });
    });
  }

  it("rejects account linking even with a matching subject", async () => {
    const input = providerInput();
    const options = makeLocalBetterAuthOptions(configuration(), {
      writeEventLine: () => undefined,
    });
    expect(
      await options.user.validateUserInfo({
        ...input,
        source: { ...input.source, action: "link-account" },
      }),
    ).toEqual({ error: "AJAS_IDENTITY_DENIED" });
  });

  it("rejects an unverified email without using email as an owner key", async () => {
    const input = providerInput();
    input.source.oauth.profile.email_verified = false;
    const options = makeLocalBetterAuthOptions(configuration(), {
      writeEventLine: () => undefined,
    });
    expect(await options.user.validateUserInfo(input)).toEqual({ error: "AJAS_IDENTITY_DENIED" });
  });

  it("rejects discovery when private capture has not been supplied", async () => {
    const options = makeLocalBetterAuthOptions(configuration(true), {
      writeEventLine: () => undefined,
    });
    expect(await options.user.validateUserInfo(providerInput())).toEqual({
      error: "AJAS_PRIVATE_CAPTURE_UNAVAILABLE",
    });
  });

  it("denies every discovery session after successful private capture", async () => {
    const lines: string[] = [];
    const captured: unknown[] = [];
    const options = makeLocalBetterAuthOptions(configuration(true), {
      writeEventLine: (line) => lines.push(line),
      captureCandidate: async (candidate) => {
        captured.push(candidate);
        return true;
      },
    });
    const result = await options.user.validateUserInfo(providerInput());
    expect(result?.error).toBe("AJAS_DISCOVERY_SESSION_DENIED");
    expect(captured).toEqual([{ provider: "google", subject, email: "fixture@example.invalid" }]);
    expect(JSON.stringify(result) + lines.join("\n")).not.toContain(subject);
    expect(JSON.stringify(result) + lines.join("\n")).not.toContain("fixture@example.invalid");
  });

  for (const fail of [false, true]) {
    it(`never admits a failed capture, throwing=${fail}`, async () => {
      const lines: string[] = [];
      const options = makeLocalBetterAuthOptions(configuration(true), {
        writeEventLine: (line) => lines.push(line),
        captureCandidate: async () => {
          if (fail) throw new Error("SYNTHETIC-PRIVATE");
          return false;
        },
      });
      expect(await options.user.validateUserInfo(providerInput())).toHaveProperty("error");
      expect(lines.join("\n")).not.toContain("SYNTHETIC");
    });
  }

  it("maps malformed provider data to a fixed denial", async () => {
    const options = makeLocalBetterAuthOptions(configuration(), {
      writeEventLine: () => undefined,
    });
    type Input = Parameters<typeof options.user.validateUserInfo>[0];
    expect(await options.user.validateUserInfo({ source: null } as unknown as Input)).toEqual({
      error: "AJAS_IDENTITY_DENIED",
    });
  });
});
