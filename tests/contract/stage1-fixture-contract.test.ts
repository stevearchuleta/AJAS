import { describe, expect, it } from "vitest";

import {
  AUTONOMOUS_TERMINAL_STATE,
  PROHIBITED_EMPLOYER_ACTIONS,
  canonicalJson,
  parseApprovedFactsSnapshot,
  parseSavedPostingFixture,
  parseSourcePolicy,
  parseStage1FixtureCommand,
  runStage1VerticalSlice,
  sha256Hex,
  type Stage1VerticalSliceInput,
} from "../../packages/core/src/index.js";
import { cloneStage1Input, loadStage1VerticalSliceInput } from "../helpers/stage1-fixtures.js";

type ContractDocument = "command" | "facts" | "fixture" | "policy";
type PathSegment = number | string;

function mutableRecord(value: unknown): Record<string, unknown> {
  return value as Record<string, unknown>;
}

function valueAtPath(value: unknown, path: readonly PathSegment[]): unknown {
  let current = value;

  for (const segment of path) {
    current =
      typeof segment === "number"
        ? (current as unknown[])[segment]
        : mutableRecord(current)[segment];
  }

  return current;
}

function setAtPath(value: unknown, path: readonly PathSegment[], replacement: unknown): void {
  if (path.length === 0) {
    throw new Error("test mutation path must not be empty");
  }

  const key = path[path.length - 1];
  const parent = valueAtPath(value, path.slice(0, -1));

  if (typeof key === "number") {
    (parent as unknown[])[key] = replacement;
  } else if (key !== undefined) {
    mutableRecord(parent)[key] = replacement;
  }
}

function documentFrom(input: Stage1VerticalSliceInput, document: ContractDocument): unknown {
  switch (document) {
    case "command":
      return input.command;
    case "facts":
      return input.facts;
    case "fixture":
      return input.fixture;
    case "policy":
      return input.policy;
  }
}

function parseDocument(document: ContractDocument, value: unknown): unknown {
  switch (document) {
    case "command":
      return parseStage1FixtureCommand(value);
    case "facts":
      return parseApprovedFactsSnapshot(value);
    case "fixture":
      return parseSavedPostingFixture(value);
    case "policy":
      return parseSourcePolicy(value);
  }
}

describe("Stage-1 fixture contracts", () => {
  it("accepts every committed v1 fixture and rejects an unknown major schema", () => {
    const input = loadStage1VerticalSliceInput();

    expect(parseApprovedFactsSnapshot(input.facts)).toEqual(input.facts);
    expect(parseSourcePolicy(input.policy)).toEqual(input.policy);
    expect(parseSavedPostingFixture(input.fixture)).toEqual(input.fixture);
    expect(parseStage1FixtureCommand(input.command)).toEqual(input.command);

    const invalid = cloneStage1Input(input);
    (invalid.fixture as unknown as { schemaVersion: string }).schemaVersion =
      "ajas.saved-greenhouse-fixture.v2";
    expect(() => parseSavedPostingFixture(invalid.fixture)).toThrow(/schemaVersion/);
  });

  it.each([
    ["facts root", "facts", []],
    ["approved fact", "facts", ["facts", 0]],
    ["fact provenance", "facts", ["facts", 0, "provenance"]],
    ["policy root", "policy", []],
    ["documentation review", "policy", ["documentation"]],
    ["terms review", "policy", ["terms"]],
    ["fixture root", "fixture", []],
    ["fixture source", "fixture", ["source"]],
    ["capture metadata", "fixture", ["capture"]],
    ["capture observation", "fixture", ["observations", 0]],
    ["saved posting", "fixture", ["savedPosting"]],
    ["anticipated closing date", "fixture", ["savedPosting", "anticipatedClosingDate"]],
    ["evidence basis", "fixture", ["savedPosting", "evidenceBasis"]],
    ["evidence pointer", "fixture", ["savedPosting", "evidenceBasis", "pointers", 0]],
    ["source evidence", "fixture", ["savedPosting", "sourceEvidence", 0]],
    ["posting requirement", "fixture", ["savedPosting", "requirements", 0]],
    ["command root", "command", []],
  ] as const)("rejects an unknown field in the %s contract", (_name, document, path) => {
    const input = cloneStage1Input();
    const value = documentFrom(input, document);
    mutableRecord(valueAtPath(value, path)).unexpectedV1Field = true;

    expect(() => parseDocument(document, value)).toThrow(/exactly the v1 contract fields/);
  });

  it.each([
    ["fractional facts version", "facts", ["version"], 1.5],
    ["object fact value", "facts", ["facts", 0, "value"], { asserted: true }],
    ["non-string allowed use", "facts", ["facts", 0, "allowedUses"], ["FIT", 7]],
    ["unknown sensitivity enum", "facts", ["facts", 0, "sensitivity"], "SECRET"],
    [
      "non-canonical provenance UTC",
      "facts",
      ["facts", 0, "provenance", "approvedAtUtc"],
      "2026-08-30T05:00:00+00:00",
    ],
    ["fractional policy version", "policy", ["policyVersion"], 1.5],
    ["fractional liveness age", "policy", ["savedLivenessMaxAgeSeconds"], 0.5],
    ["unknown policy state enum", "policy", ["state"], "ACTIVE"],
    [
      "non-canonical policy-review UTC",
      "policy",
      ["documentation", "reviewedAtUtc"],
      "2026-08-30T05:00:00+00:00",
    ],
    [
      "wrong response-header hash tuple length",
      "policy",
      ["approvedResponseHeadersSha256"],
      ["d".repeat(64)],
    ],
    ["fractional posting ID", "fixture", ["savedPosting", "id"], 8073203.5],
    ["fractional raw body bytes", "fixture", ["capture", "rawBodyBytes"], 12618.5],
    [
      "fractional observation content length",
      "fixture",
      ["observations", 0, "contentLength"],
      12618.5,
    ],
    ["unknown observation phase enum", "fixture", ["observations", 0, "phase"], "FINAL"],
    [
      "fractional source-evidence byte offset",
      "fixture",
      ["savedPosting", "sourceEvidence", 0, "startByte"],
      0.5,
    ],
    [
      "unknown requirement gate enum",
      "fixture",
      ["savedPosting", "requirements", 0, "gate"],
      "SCORING",
    ],
    [
      "operator and expected-type mismatch",
      "fixture",
      ["savedPosting", "requirements", 2, "expected"],
      "seven",
    ],
    ["fractional command policy version", "command", ["sourcePolicyVersion"], 1.5],
    ["non-canonical command UTC", "command", ["evaluatedAtUtc"], "2026-08-30T05:23:00+00:00"],
    ["uppercase command hash", "command", ["factsSnapshotSha256"], "A".repeat(64)],
  ] as const)("rejects invalid nested type or vocabulary: %s", (_name, document, path, value) => {
    const input = cloneStage1Input();
    const contract = documentFrom(input, document);
    setAtPath(contract, path, value);

    expect(() => parseDocument(document, contract)).toThrow();
  });

  it("pins a genuine exact-board capture identity and recomputable minimized hash", () => {
    const { fixture, policy } = loadStage1VerticalSliceInput();

    expect(fixture.source).toMatchObject({
      provider: "GREENHOUSE",
      boardToken: "greenhouse",
      sourceKey: "GREENHOUSE:greenhouse",
      externalPostingId: "8073203",
      requestUrl: "https://boards-api.greenhouse.io/v1/boards/greenhouse/jobs/8073203",
    });
    expect(fixture.capture.rawBodySha256).toBe(
      "8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b",
    );
    expect(sha256Hex(canonicalJson(fixture.savedPosting))).toBe(fixture.savedPostingSha256);
    expect(policy.sourceKey).toBe(fixture.source.sourceKey);
    expect(policy.documentation.url).toBe(fixture.source.documentationUrl);
  });

  it("pins the approved facts and command bytes to the exact policy", () => {
    const { command, facts, policy } = loadStage1VerticalSliceInput();
    const factsSha256 = sha256Hex(canonicalJson(facts));
    const commandSha256 = sha256Hex(canonicalJson(command));

    expect(command.subjectId).toBe(facts.subjectId);
    expect(command.factsSnapshotId).toBe(facts.snapshotId);
    expect(command.factsSnapshotVersion).toBe(facts.version);
    expect(command.factsSnapshotSha256).toBe(factsSha256);
    expect(policy.approvedFactsSnapshotId).toBe(facts.snapshotId);
    expect(policy.approvedFactsSnapshotSha256).toBe(factsSha256);
    expect(policy.approvedCommandSha256).toBe(commandSha256);
  });

  it.each(["SUBJECT", "FACTS_CONTENT", "COMMAND_CONTENT"])(
    "rejects a %s binding mismatch before READY",
    (failureMode) => {
      const input = cloneStage1Input();

      if (failureMode === "SUBJECT") {
        (input.command as unknown as { subjectId: string }).subjectId =
          "different-synthetic-applicant";
      } else if (failureMode === "FACTS_CONTENT") {
        const fact = (
          input.facts as unknown as { facts: Array<{ factKey: string; value: unknown }> }
        ).facts.find((candidate) => candidate.factKey === "communication_strength");
        expect(fact).toBeDefined();
        if (fact !== undefined) fact.value = false;
      } else {
        (input.command as unknown as { authorizationRef: string }).authorizationRef =
          "different-unapproved-authorization";
      }

      expect(() => runStage1VerticalSlice(input)).toThrow();
    },
  );

  it.each(["FACTS_ID", "FACTS_HASH", "COMMAND_HASH"])(
    "rejects a policy %s trust-anchor mismatch before READY",
    (failureMode) => {
      const input = cloneStage1Input();
      const policy = input.policy as unknown as {
        approvedCommandSha256: string;
        approvedFactsSnapshotId: string;
        approvedFactsSnapshotSha256: string;
      };

      if (failureMode === "FACTS_ID") {
        policy.approvedFactsSnapshotId = "different-approved-facts";
      } else if (failureMode === "FACTS_HASH") {
        policy.approvedFactsSnapshotSha256 = "a".repeat(64);
      } else {
        policy.approvedCommandSha256 = "b".repeat(64);
      }

      expect(() => runStage1VerticalSlice(input)).toThrow();
    },
  );

  it("returns the required typed packet, fit, state, and audit envelopes", () => {
    const result = runStage1VerticalSlice(loadStage1VerticalSliceInput());

    expect(result.schemaVersion).toBe("ajas.stage1-vertical-slice-result.v1");
    expect(result.packetMetadata.schemaVersion).toBe("ajas.packet-metadata.v1");
    expect(result.screening.requirements).toHaveLength(12);
    expect(result.auditEvents.every((event) => event.schemaVersion === "ajas.audit-event.v1")).toBe(
      true,
    );
    expect(result.humanBoundary.terminalState).toBe(AUTONOMOUS_TERMINAL_STATE);
  });

  it("keeps output actions disjoint from prohibited employer actions", () => {
    const input = loadStage1VerticalSliceInput();
    const result = runStage1VerticalSlice(input);
    const outputActions = result.auditEvents.map((event) => event.action);

    for (const prohibitedAction of PROHIBITED_EMPLOYER_ACTIONS) {
      expect(outputActions).not.toContain(prohibitedAction);
    }

    expect(input.policy.prohibitedOperations).toEqual(
      expect.arrayContaining([
        "POST_APPLICATION",
        "LOGIN",
        "AUTHENTICATED_SESSION",
        "FORM_INTERACTION",
        "UPLOAD",
        "CONTACT_EMPLOYER",
        "SUBMIT",
      ]),
    );
    expect(input.policy.allowedNetworkMethods).toEqual([]);
    expect(result.humanBoundary.employerActionPermitted).toBe(false);
  });
});
