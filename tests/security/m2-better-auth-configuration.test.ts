// ============================================================
// TEST CONFIGURATION WITH SYNTHETIC VALUES; NEVER LOAD ENV FILES.
// ============================================================
import { describe, expect, it } from "vitest";
import {
  AUTH_SPIKE_ORIGIN,
  environmentAuthSecrets,
  readLocalAuthConfiguration,
} from "../../apps/web/src/lib/auth/local-auth-configuration.js";

// ============================================================
// KEEP SYNTHETIC IDENTITIES IN TESTS, NEVER IN SHIPPED UI DEFAULTS.
// ============================================================
const syntheticEnvironment = () => ({
  NODE_ENV: "development",
  CI: "",
  AJAS_AUTH_SPIKE_LOOPBACK_LAUNCH: "1",
  AJAS_AUTH_SPIKE_DISCOVERY: "0",
  AJAS_ALLOWED_GOOGLE_SUB: "SYNTHETIC-SUBJECT",
  BETTER_AUTH_URL: AUTH_SPIKE_ORIGIN,
  BETTER_AUTH_TELEMETRY: "0",
  BETTER_AUTH_TELEMETRY_DEBUG: "0",
  GOOGLE_CLIENT_ID: "synthetic-client.apps.googleusercontent.com",
  GOOGLE_CLIENT_SECRET: "SYNTHETIC-CLIENT-SECRET",
  BETTER_AUTH_SECRET: "SYNTHETIC-TEST-ONLY-SIGNING-SECRET-32-CHARACTERS",
});

describe("M2 Better Auth configuration boundary", () => {
  it("preserves the exact opaque subject through the merged policy", async () => {
    const environment = syntheticEnvironment();
    const value = await readLocalAuthConfiguration(
      environment,
      environmentAuthSecrets(environment),
    );
    expect(value.policy.allowedGoogleSubject).toBe("SYNTHETIC-SUBJECT");
    expect(Object.isFrozen(value)).toBe(true);
  });

  for (const [key, value] of [
    ["NODE_ENV", "production"],
    ["NODE_ENV", "test"],
    ["CI", "true"],
    ["AJAS_AUTH_SPIKE_LOOPBACK_LAUNCH", "0"],
    ["BETTER_AUTH_URL", "https://example.invalid"],
    ["BETTER_AUTH_URL", "http://localhost:3000.evil.invalid"],
    ["BETTER_AUTH_URL", "http://localhost:3000/"],
    ["BETTER_AUTH_TELEMETRY", "1"],
    ["BETTER_AUTH_TELEMETRY", ""],
    ["BETTER_AUTH_TELEMETRY_DEBUG", "1"],
    ["BETTER_AUTH_SECRETS", "UNREVIEWED-KEY-ROTATION"],
    ["AJAS_ALLOWED_GOOGLE_SUB", ""],
    ["AJAS_AUTH_SPIKE_DISCOVERY", "1"],
  ] as const) {
    it(`rejects ${key} override ${value || "empty"} before reading secrets`, async () => {
      let reads = 0;
      const environment = { ...syntheticEnvironment(), [key]: value };
      await expect(
        readLocalAuthConfiguration(environment, {
          read: async () => {
            reads += 1;
            return undefined;
          },
        }),
      ).rejects.toThrow("AUTH_SPIKE_CONFIGURATION_DENIED");
      expect(reads).toBe(0);
    });
  }

  for (const [key, value] of [
    ["BETTER_AUTH_SECRET", "short"],
    ["BETTER_AUTH_SECRET", ""],
    ["GOOGLE_CLIENT_SECRET", "PRIVATE\nVALUE"],
    ["GOOGLE_CLIENT_ID", " PRIVATE"],
    ["GOOGLE_CLIENT_ID", "P".repeat(4097)],
  ] as const) {
    it(`rejects invalid ${key} without including private content`, async () => {
      const environment = { ...syntheticEnvironment(), [key]: value };
      try {
        await readLocalAuthConfiguration(environment, environmentAuthSecrets(environment));
        throw new Error("UNEXPECTED_ACCEPTANCE");
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
        expect((error as Error).message).toBe("AUTH_SPIKE_CONFIGURATION_DENIED");
      }
    });
  }

  it("maps a secret-provider exception to a fixed error", async () => {
    await expect(
      readLocalAuthConfiguration(syntheticEnvironment(), {
        read: async () => {
          throw new Error("SYNTHETIC-PRIVATE-EXCEPTION");
        },
      }),
    ).rejects.toThrow(/^AUTH_SPIKE_CONFIGURATION_DENIED$/);
  });
});
