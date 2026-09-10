// ============================================================
// LOAD PRIVATE CONFIGURATION ONLY WHEN THE SERVER CALLS THE FACTORY.
// MODULE IMPORTS AND SECRET-FREE NEXT.JS BUILDS DO NOT INITIALIZE AUTH.
// ============================================================
import {
  AuthConfigurationError,
  environmentAuthSecrets,
  readLocalAuthConfiguration,
  type AuthSecretProvider,
} from "./local-auth-configuration.js";
import { makeLocalBetterAuthOptions, type LocalAuthPorts } from "./better-auth-options.js";

// ============================================================
// FAIL CLOSED BEFORE IMPORTING THE LIBRARY OR READING SECRETS.
// THIS IS A SERVER FACTORY, NOT AN HTTP ENDPOINT OR CLIENT EXPORT.
// ============================================================
export async function createLocalBetterAuth(
  ports: LocalAuthPorts = {},
  secrets: AuthSecretProvider = environmentAuthSecrets(process.env),
) {
  if ("window" in globalThis) {
    throw new AuthConfigurationError();
  }
  const configuration = await readLocalAuthConfiguration(process.env, secrets);
  if (configuration.policy.mode === "discovery" && ports.captureCandidate === undefined) {
    throw new AuthConfigurationError();
  }
  try {
    const { betterAuth } = await import("better-auth/minimal");
    const instance = betterAuth(makeLocalBetterAuthOptions(configuration, ports));
    // ======================================================
    // AWAIT INITIALIZATION; DO NOT LEAVE A REJECTED PROMISE.
    // ======================================================
    await instance.$context;
    return instance;
  } catch {
    // ======================================================
    // DISCARD VENDOR EXCEPTION CONTENT BEFORE CROSSING THE PORT.
    // ======================================================
    throw new AuthConfigurationError();
  }
}
