// ============================================================
// USE SYNTHETIC IDENTIFIERS ONLY; NEVER LOAD A REAL ENVIRONMENT FILE.
// ============================================================
import assert from "node:assert/strict";
import { createAuthEventWriter } from "../../packages/core/src/auth/auth-events.js";
import {
  evaluatePersonalAlphaAdmission,
  readPersonalAlphaConfiguration,
} from "../../packages/core/src/auth/personal-alpha-policy.js";

// ============================================================
// EXPORT THE SAME ASSERTIONS TO VITEST AND THE OFFLINE NODE HARNESS.
// ============================================================
export interface AuthFoundationCase {
  name: string;
  run: () => void;
}

// ============================================================
// CONSTRUCT EXPLICITLY SYNTHETIC CONFIGURATION AND VERIFIED-INPUT
// FIXTURES. NO CRYPTOGRAPHIC VERIFICATION IS CLAIMED BY THESE TESTS.
// ============================================================
const allowedSubject = "SYNTHETIC-GOOGLE-SUBJECT-A";
const allowlist = {
  mode: "allowlist",
  localDevelopment: true,
  allowedGoogleSubject: allowedSubject,
};
const discovery = { mode: "discovery", localDevelopment: true, allowedGoogleSubject: null };
const identity = { provider: "google", subject: allowedSubject, context: "provider-admission" };
const development = { NODE_ENV: "development", AJAS_AUTH_SPIKE_LOOPBACK_LAUNCH: "1" };

// ============================================================
// EXERCISE POSITIVE ADMISSION AND NEGATIVE/ADVERSARIAL DECISIONS.
// ============================================================
export const authFoundationCases: AuthFoundationCase[] = [
  {
    name: "exact subject is admitted after explicit allowlisting",
    run: () => {
      assert.deepEqual(evaluatePersonalAlphaAdmission(allowlist, identity), {
        allowed: true,
        captureCandidate: false,
        code: "AUTH_ADMITTED",
      });
    },
  },
  {
    name: "protected operations reuse the same admission policy",
    run: () => {
      assert.equal(
        evaluatePersonalAlphaAdmission(allowlist, { ...identity, context: "protected-operation" })
          .allowed,
        true,
      );
    },
  },
  {
    name: "discovery requests capture but never grants a session",
    run: () => {
      assert.deepEqual(evaluatePersonalAlphaAdmission(discovery, identity), {
        allowed: false,
        captureCandidate: true,
        code: "AUTH_DISCOVERY_SESSION_DENIED",
      });
    },
  },
  {
    name: "discovery never requests capture from a protected operation",
    run: () => {
      assert.equal(
        evaluatePersonalAlphaAdmission(discovery, { ...identity, context: "protected-operation" })
          .captureCandidate,
        false,
      );
    },
  },
  {
    name: "a matching email cannot authorize a different subject",
    run: () => {
      assert.equal(
        evaluatePersonalAlphaAdmission(allowlist, {
          ...identity,
          subject: "SYNTHETIC-OTHER-SUBJECT",
          email: "fixture@example.invalid",
        }).allowed,
        false,
      );
    },
  },
  {
    name: "subject comparison is case sensitive",
    run: () => {
      assert.equal(
        evaluatePersonalAlphaAdmission(allowlist, {
          ...identity,
          subject: allowedSubject.toLowerCase(),
        }).allowed,
        false,
      );
    },
  },
  {
    name: "non-numeric opaque subjects remain valid",
    run: () => {
      assert.equal(evaluatePersonalAlphaAdmission(allowlist, identity).allowed, true);
    },
  },
  {
    name: "discovery refuses a simultaneous configured allowlist",
    run: () => {
      assert.equal(
        evaluatePersonalAlphaAdmission(
          { ...discovery, allowedGoogleSubject: allowedSubject },
          identity,
        ).captureCandidate,
        false,
      );
    },
  },
  {
    name: "public or production contexts cannot enable the local spike",
    run: () => {
      assert.equal(
        evaluatePersonalAlphaAdmission({ ...allowlist, localDevelopment: false }, identity).allowed,
        false,
      );
      assert.equal(
        evaluatePersonalAlphaAdmission({ ...discovery, localDevelopment: false }, identity)
          .captureCandidate,
        false,
      );
    },
  },
  {
    name: "decision results never expose the candidate or allowed subject",
    run: () => {
      assert.equal(
        JSON.stringify(evaluatePersonalAlphaAdmission(allowlist, identity)).includes(
          allowedSubject,
        ),
        false,
      );
      assert.equal(
        JSON.stringify(evaluatePersonalAlphaAdmission(discovery, identity)).includes(
          allowedSubject,
        ),
        false,
      );
    },
  },
  {
    name: "decisions are immutable",
    run: () => {
      assert.equal(Object.isFrozen(evaluatePersonalAlphaAdmission(allowlist, identity)), true);
    },
  },
  {
    name: "configuration defaults to disabled",
    run: () => {
      assert.equal(readPersonalAlphaConfiguration({}).mode, "disabled");
    },
  },
  {
    name: "missing loopback launcher marker disables discovery",
    run: () => {
      assert.equal(
        readPersonalAlphaConfiguration({ NODE_ENV: "development", AJAS_AUTH_SPIKE_DISCOVERY: "1" })
          .mode,
        "disabled",
      );
    },
  },
  {
    name: "production disables discovery even with a launcher marker",
    run: () => {
      assert.equal(
        readPersonalAlphaConfiguration({
          ...development,
          NODE_ENV: "production",
          AJAS_AUTH_SPIKE_DISCOVERY: "1",
        }).mode,
        "disabled",
      );
    },
  },
  {
    name: "explicit local discovery creates no allowed subject",
    run: () => {
      assert.deepEqual(
        readPersonalAlphaConfiguration({ ...development, AJAS_AUTH_SPIKE_DISCOVERY: "1" }),
        discovery,
      );
    },
  },
  {
    name: "exact local allowlist configuration preserves the subject",
    run: () => {
      assert.deepEqual(
        readPersonalAlphaConfiguration({
          ...development,
          AJAS_AUTH_SPIKE_DISCOVERY: "0",
          AJAS_ALLOWED_GOOGLE_SUB: allowedSubject,
        }),
        allowlist,
      );
    },
  },
  {
    name: "conflicting discovery and allowlist configuration disables auth",
    run: () => {
      assert.equal(
        readPersonalAlphaConfiguration({
          ...development,
          AJAS_AUTH_SPIKE_DISCOVERY: "1",
          AJAS_ALLOWED_GOOGLE_SUB: allowedSubject,
        }).mode,
        "disabled",
      );
    },
  },
  {
    name: "configuration is immutable",
    run: () => {
      assert.equal(Object.isFrozen(readPersonalAlphaConfiguration({})), true);
    },
  },
  {
    name: "safe auth events correlate a request without private payloads",
    run: () => {
      const lines: string[] = [];
      const write = createAuthEventWriter((line) => lines.push(line));
      write("AUTH_REQUEST_STARTED");
      write("AUTH_IDENTITY_DENIED");
      const records = lines.map((line) => JSON.parse(line) as Record<string, unknown>);
      assert.equal(records[0]?.correlationId, records[1]?.correlationId);
      assert.match(String(records[0]?.correlationId), /^[0-9a-f-]{36}$/);
      assert.deepEqual(Object.keys(records[0] ?? {}).sort(), [
        "code",
        "correlationId",
        "schema",
        "timestamp",
      ]);
    },
  },
  {
    name: "separate auth requests receive separate correlation IDs",
    run: () => {
      const lines: string[] = [];
      createAuthEventWriter((line) => lines.push(line))("AUTH_REQUEST_STARTED");
      createAuthEventWriter((line) => lines.push(line))("AUTH_REQUEST_STARTED");
      assert.notEqual(
        JSON.parse(lines[0] ?? "{}").correlationId,
        JSON.parse(lines[1] ?? "{}").correlationId,
      );
    },
  },
  {
    name: "logger drops subject token URL cookie and exception sentinels",
    run: () => {
      const lines: string[] = [];
      const write = createAuthEventWriter((line) => lines.push(line));
      for (const value of [
        allowedSubject,
        "SYNTHETIC-ACCESS-TOKEN",
        "https://example.invalid/?code=SYNTHETIC-CODE",
        new Error("SYNTHETIC-SECRET"),
        { cookie: "SYNTHETIC-COOKIE" },
      ]) {
        write(value);
      }
      assert.equal(lines.join("\n").includes("SYNTHETIC"), false);
      assert.equal(
        lines.every((line) => JSON.parse(line).code === "AUTH_EVENT_INPUT_REJECTED"),
        true,
      );
    },
  },
  {
    name: "logger never invokes a private object's string conversion",
    run: () => {
      const lines: string[] = [];
      createAuthEventWriter((line) => lines.push(line))({
        toString: () => {
          throw new Error("SYNTHETIC-PRIVATE");
        },
      });
      assert.equal(lines.length, 1);
      assert.equal(lines[0]?.includes("SYNTHETIC"), false);
    },
  },
];

// ============================================================
// RUN THE SAME DENIAL CONTRACT ACROSS MALFORMED SUBJECT VALUES.
// ============================================================
for (const [name, subject] of [
  ["missing", undefined],
  ["null", null],
  ["numeric", 123],
  ["empty", ""],
  ["leading whitespace", " SYNTHETIC"],
  ["trailing whitespace", "SYNTHETIC "],
  ["control character", "SYNTHETIC\nVALUE"],
  ["oversized", "S".repeat(256)],
] as const) {
  authFoundationCases.push({
    name: `malformed ${name} subject cannot admit or capture`,
    run: () => {
      for (const policy of [allowlist, discovery]) {
        const result = evaluatePersonalAlphaAdmission(policy, { ...identity, subject });
        assert.equal(result.allowed, false);
        assert.equal(result.captureCandidate, false);
      }
    },
  });
}

// ============================================================
// REJECT MISSING AND UNEXPECTED CONFIGURATION WITHOUT EXCEPTIONS.
// ============================================================
for (const configuration of [
  null,
  undefined,
  [],
  {},
  { mode: "TRUE" },
  { ...allowlist, allowedGoogleSubject: null },
]) {
  authFoundationCases.push({
    name: `invalid configuration ${authFoundationCases.length} denies admission`,
    run: () => {
      assert.equal(evaluatePersonalAlphaAdmission(configuration, identity).allowed, false);
    },
  });
}

// ============================================================
// OTHER PROVIDERS AND CONTEXTS CANNOT ENTER THE GOOGLE-ONLY SPIKE.
// ============================================================
for (const value of [
  null,
  undefined,
  {},
  { ...identity, provider: "github" },
  { ...identity, provider: "Google" },
  { ...identity, context: "link-account" },
]) {
  authFoundationCases.push({
    name: `untrusted identity shape ${authFoundationCases.length} denies admission`,
    run: () => {
      const result = evaluatePersonalAlphaAdmission(allowlist, value);
      assert.equal(result.allowed, false);
      assert.equal(result.captureCandidate, false);
    },
  });
}
