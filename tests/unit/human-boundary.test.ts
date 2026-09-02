import { describe, expect, it } from "vitest";

import {
  AUTONOMOUS_TERMINAL_STATE,
  PROHIBITED_EMPLOYER_ACTIONS,
  isProhibitedEmployerAction,
} from "../../packages/core/src/index.js";

describe("human submission boundary", () => {
  it("stops autonomous authority at READY_FOR_REVIEW", () => {
    expect(AUTONOMOUS_TERMINAL_STATE).toBe("READY_FOR_REVIEW");
  });

  it("contains every prohibited employer action", () => {
    expect(PROHIBITED_EMPLOYER_ACTIONS).toEqual([
      "EMPLOYER_AUTHENTICATION",
      "EMPLOYER_FORM_ENTRY",
      "EMPLOYER_FILE_UPLOAD",
      "EMPLOYER_ATTESTATION",
      "EMPLOYER_COMMUNICATION",
      "EMPLOYER_SUBMISSION",
    ]);
  });

  it("recognizes a prohibited employer submission request", () => {
    expect(isProhibitedEmployerAction("EMPLOYER_SUBMISSION")).toBe(true);
    expect(isProhibitedEmployerAction("PREPARE_PACKET")).toBe(false);
  });
});
