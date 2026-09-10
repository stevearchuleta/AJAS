// ============================================================
// EXERCISE THE INSTALLED BETTER AUTH RUNTIME, NOT A LIBRARY MOCK.
// ALL NETWORK ACCESS IS REPLACED WITH AN EXPLICIT TEST FAILURE.
// ============================================================
import { afterEach, describe, expect, it, vi } from "vitest";
import { createLocalBetterAuth } from "../../apps/web/src/lib/auth/better-auth-runtime.js";
import { makeLocalBetterAuthOptions } from "../../apps/web/src/lib/auth/better-auth-options.js";
import {
  environmentAuthSecrets,
  readLocalAuthConfiguration,
} from "../../apps/web/src/lib/auth/local-auth-configuration.js";

// ============================================================
// RESTORE TEST ENVIRONMENT AND NETWORK STUBS AFTER EVERY TEST.
// ============================================================
afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

describe("M2 Better Auth actual runtime", () => {
  it("imports without secrets and rejects production before secret access", async () => {
    vi.stubEnv("NODE_ENV", "production");
    let reads = 0;
    await expect(
      createLocalBetterAuth(
        {},
        {
          read: async () => {
            reads += 1;
            return undefined;
          },
        },
      ),
    ).rejects.toThrow("AUTH_SPIKE_CONFIGURATION_DENIED");
    expect(reads).toBe(0);
  });

  it("initializes stateless options with telemetry off and rejects a forged session", async () => {
    const network = vi.fn(() => {
      throw new Error("UNEXPECTED_NETWORK_IN_SYNTHETIC_TEST");
    });
    vi.stubGlobal("fetch", network);
    for (const [name, value] of Object.entries({
      NODE_ENV: "development",
      CI: "",
      AJAS_AUTH_SPIKE_LOOPBACK_LAUNCH: "1",
      AJAS_AUTH_SPIKE_DISCOVERY: "0",
      AJAS_ALLOWED_GOOGLE_SUB: "SYNTHETIC-SUBJECT",
      BETTER_AUTH_URL: "http://localhost:3000",
      BETTER_AUTH_TELEMETRY: "0",
      BETTER_AUTH_TELEMETRY_DEBUG: "0",
      BETTER_AUTH_SECRETS: "",
      GOOGLE_CLIENT_ID: "synthetic-client",
      GOOGLE_CLIENT_SECRET: "SYNTHETIC-CLIENT-SECRET",
      BETTER_AUTH_SECRET: "SYNTHETIC-TEST-ONLY-SIGNING-SECRET-32-CHARACTERS",
    })) {
      vi.stubEnv(name, value);
    }
    const auth = await createLocalBetterAuth({ writeEventLine: () => undefined });
    const context = await auth.$context;
    expect(context.options.telemetry?.enabled).toBe(false);
    expect(context.options.account?.storeAccountCookie).toBe(false);
    expect(context.options.session?.cookieCache?.strategy).toBe("jwe");
    expect(context.options.session?.cookieCache?.refreshCache).toBe(false);
    expect(await auth.api.getSession({ headers: new Headers() })).toBeNull();
    expect(
      await auth.api.getSession({
        headers: new Headers({
          cookie: "ajas-local-spike.session_token=FORGED; ajas-local-spike.session_data=FORGED",
        }),
      }),
    ).toBeNull();
    expect(network).not.toHaveBeenCalled();
  }, 60_000);

  it("retains no-secret option construction outside a live factory", async () => {
    const environment = {
      NODE_ENV: "development",
      CI: "",
      AJAS_AUTH_SPIKE_LOOPBACK_LAUNCH: "1",
      AJAS_AUTH_SPIKE_DISCOVERY: "1",
      BETTER_AUTH_URL: "http://localhost:3000",
      BETTER_AUTH_TELEMETRY: "0",
      GOOGLE_CLIENT_ID: "synthetic-client",
      BETTER_AUTH_SECRET: "SYNTHETIC-TEST-ONLY-SIGNING-SECRET-32-CHARACTERS",
      GOOGLE_CLIENT_SECRET: "SYNTHETIC-CLIENT-SECRET",
    };
    const config = await readLocalAuthConfiguration(
      environment,
      environmentAuthSecrets(environment),
    );
    expect(makeLocalBetterAuthOptions(config).onAPIError.errorURL).toBe(
      "http://localhost:3000/auth-spike/result",
    );
  });
});
