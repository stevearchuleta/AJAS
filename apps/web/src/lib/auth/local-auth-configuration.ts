// ============================================================
// REUSE THE MERGED POLICY; KEEP SUBJECT CONFIGURATION CENTRALIZED.
// ============================================================
import {
  readPersonalAlphaConfiguration,
  type PersonalAlphaConfiguration,
} from "../../../../../packages/core/src/auth/personal-alpha-policy.js";

// ============================================================
// FIX THE LOCAL ORIGIN; NEVER DERIVE CALLBACKS FROM REQUEST HEADERS.
// ============================================================
export const AUTH_SPIKE_ORIGIN = "http://localhost:3000";
export const AUTH_SPIKE_ERROR_URL = `${AUTH_SPIKE_ORIGIN}/auth-spike/result`;

// ============================================================
// DEFINE AN ASYNC SECRET PORT FOR LATER PROVIDER REPLACEMENT.
// ============================================================
export type AuthSecretName = "BETTER_AUTH_SECRET" | "GOOGLE_CLIENT_SECRET";
export interface AuthSecretProvider {
  read(name: AuthSecretName): Promise<string | undefined>;
}
export interface LocalAuthConfiguration {
  readonly policy: PersonalAlphaConfiguration;
  readonly signingSecret: string;
  readonly clientId: string;
  readonly clientSecret: string;
}

// ============================================================
// NEVER RETURN VARIABLE CONTENT IN CONFIGURATION ERRORS.
// ============================================================
export class AuthConfigurationError extends Error {
  constructor() {
    super("AUTH_SPIKE_CONFIGURATION_DENIED");
    this.name = "AuthConfigurationError";
  }
}

// ============================================================
// READ ONLY EXPLICITLY REQUESTED SECRETS; NEVER ENUMERATE VALUES.
// ============================================================
export function environmentAuthSecrets(
  environment: Readonly<Record<string, string | undefined>>,
): AuthSecretProvider {
  return {
    read: async (name) => environment[name],
  };
}

// ============================================================
// REJECT EMPTY, OVERSIZED, WHITESPACE, AND CONTROL-BEARING VALUES.
// DO NOT TRIM OR REWRITE CREDENTIALS.
// ============================================================
function validPrivateValue(value: unknown, minimum: number): value is string {
  return (
    typeof value === "string" &&
    value.length >= minimum &&
    value.length <= 4096 &&
    !/\s/u.test(value) &&
    !Array.from(value).some((character) => {
      const code = character.charCodeAt(0);
      return code < 32 || (code >= 127 && code <= 159);
    })
  );
}

// ============================================================
// VALIDATE PUBLIC CONTEXT BEFORE READING ANY SECRET.
// NO DEFAULT SIGNING KEY AND NO PRODUCTION BYPASS ARE PERMITTED.
// ============================================================
export async function readLocalAuthConfiguration(
  environment: Readonly<Record<string, string | undefined>>,
  secrets: AuthSecretProvider,
): Promise<LocalAuthConfiguration> {
  try {
    const policy = readPersonalAlphaConfiguration(environment);
    if (
      policy.mode === "disabled" ||
      !policy.localDevelopment ||
      (environment.CI !== undefined && environment.CI !== "" && environment.CI !== "false") ||
      environment.BETTER_AUTH_URL !== AUTH_SPIKE_ORIGIN ||
      environment.BETTER_AUTH_TELEMETRY !== "0" ||
      (environment.BETTER_AUTH_TELEMETRY_DEBUG !== undefined &&
        environment.BETTER_AUTH_TELEMETRY_DEBUG !== "0") ||
      Boolean(environment.BETTER_AUTH_SECRETS)
    ) {
      throw new AuthConfigurationError();
    }
    const clientId = environment.GOOGLE_CLIENT_ID;
    const signingSecret = await secrets.read("BETTER_AUTH_SECRET");
    const clientSecret = await secrets.read("GOOGLE_CLIENT_SECRET");
    if (
      !validPrivateValue(clientId, 1) ||
      !validPrivateValue(clientSecret, 1) ||
      !validPrivateValue(signingSecret, 32)
    ) {
      throw new AuthConfigurationError();
    }
    return Object.freeze({ policy, signingSecret, clientId, clientSecret });
  } catch {
    throw new AuthConfigurationError();
  }
}
