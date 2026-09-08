// ============================================================
// REGISTER THE SHARED SYNTHETIC CASES IN THE EXISTING VITEST SUITE.
// ============================================================
import { describe, it } from "vitest";
import { authFoundationCases } from "../fixtures/m2-auth-foundation-cases.js";

// ============================================================
// RUN EVERY POLICY AND REDACTION ASSERTION WITHOUT LIVE SECRETS.
// ============================================================
describe("M2 local authentication foundation", () => {
  for (const scenario of authFoundationCases) {
    it(scenario.name, scenario.run);
  }
});
