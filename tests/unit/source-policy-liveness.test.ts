import { describe, expect, it } from "vitest";

import {
  Stage1ValidationError,
  assertNetworkOperationDenied,
  canonicalJson,
  sha256Hex,
  validateSavedLiveness,
  validateSourcePolicy,
} from "../../packages/core/src/index.js";
import { cloneStage1Input, loadStage1VerticalSliceInput } from "../helpers/stage1-fixtures.js";

describe("source policy and saved liveness", () => {
  it("allows only exact-board offline fixture processing", () => {
    const input = loadStage1VerticalSliceInput();
    const decision = validateSourcePolicy(
      input.policy,
      input.fixture,
      input.command.evaluatedAtUtc,
    );

    expect(decision).toMatchObject({
      decision: "ALLOW_FIXTURE_PROCESSING",
      sourceKey: "GREENHOUSE:greenhouse",
      networkAuthorized: false,
    });
  });

  it.each(["UNDER_REVIEW", "DISABLED", "EXPIRED", "ENABLED"])(
    "denies fixture processing when policy state is %s",
    (state) => {
      const input = cloneStage1Input();
      (input.policy as unknown as { state: string }).state = state;

      expect(() =>
        validateSourcePolicy(input.policy, input.fixture, input.command.evaluatedAtUtc),
      ).toThrowError(Stage1ValidationError);
    },
  );

  it.each(["WRONG_BOARD", "EXPIRED", "NETWORK_METHOD", "HASH_MISMATCH"])(
    "fails closed for policy/fixture drift: %s",
    (failureMode) => {
      const input = cloneStage1Input();

      if (failureMode === "WRONG_BOARD") {
        (input.policy as unknown as { boardToken: string }).boardToken = "other-board";
      } else if (failureMode === "EXPIRED") {
        (input.policy as unknown as { expiresAtUtc: string }).expiresAtUtc =
          input.command.evaluatedAtUtc;
      } else if (failureMode === "NETWORK_METHOD") {
        (input.policy as unknown as { allowedNetworkMethods: string[] }).allowedNetworkMethods = [
          "GET",
        ];
      } else {
        (input.fixture as unknown as { savedPostingSha256: string }).savedPostingSha256 =
          "0".repeat(64);
      }

      expect(() =>
        validateSourcePolicy(input.policy, input.fixture, input.command.evaluatedAtUtc),
      ).toThrow();
    },
  );

  it.each(["TITLE", "REQUIREMENT", "UNTRUSTED_CONTENT"])(
    "rejects policy-pinned fixture tamper after recomputing its self-hash: %s",
    (failureMode) => {
      const input = cloneStage1Input();
      const mutable = input.fixture as unknown as {
        savedPosting: {
          title: string;
          requirements: Array<{ label: string }>;
          untrustedContentMarker: string;
        };
        savedPostingSha256: string;
      };

      if (failureMode === "TITLE") {
        mutable.savedPosting.title = "Tampered role";
      } else if (failureMode === "REQUIREMENT") {
        mutable.savedPosting.requirements[0]!.label = "Tampered material requirement";
      } else {
        mutable.savedPosting.untrustedContentMarker = "Tampered fixture content";
      }

      mutable.savedPostingSha256 = sha256Hex(canonicalJson(mutable.savedPosting));

      expect(() =>
        validateSourcePolicy(input.policy, input.fixture, input.command.evaluatedAtUtc),
      ).toThrowError(expect.objectContaining({ code: "FIXTURE_TRUST_ANCHOR_MISMATCH" }));
    },
  );

  it.each(["DOCUMENTATION", "TERMS"])(
    "rejects official governance URL drift: %s",
    (failureMode) => {
      const input = cloneStage1Input();

      if (failureMode === "DOCUMENTATION") {
        (input.policy.documentation as unknown as { url: string }).url =
          "https://docs.greenhouse.io/unreviewed";
        (input.fixture.source as unknown as { documentationUrl: string }).documentationUrl =
          "https://docs.greenhouse.io/unreviewed";
      } else {
        (input.policy.terms as unknown as { url: string }).url =
          "https://www.greenhouse.com/privacy-policy";
      }

      expect(() =>
        validateSourcePolicy(input.policy, input.fixture, input.command.evaluatedAtUtc),
      ).toThrowError(expect.objectContaining({ code: "SOURCE_POLICY_INCOMPLETE" }));
    },
  );

  it("validates intake and pre-ready evidence without claiming current liveness", () => {
    const input = loadStage1VerticalSliceInput();
    const decision = validateSavedLiveness(
      input.policy,
      input.fixture,
      input.command.evaluatedAtUtc,
    );

    expect(decision.decision).toBe("VALID_SAVED_EVIDENCE");
    expect(decision.currentStatus).toBe("NOT_CHECKED");
    expect(decision.evidence.map((evidence) => evidence.phase)).toEqual(["INTAKE", "PRE_READY"]);
    expect(
      new Set(input.fixture.observations.map((observation) => observation.evidenceId)).size,
    ).toBe(2);
    expect(
      new Set(input.fixture.observations.map((observation) => observation.requestId)).size,
    ).toBe(2);
    expect(
      new Set(input.fixture.observations.map((observation) => observation.responseHeadersSha256))
        .size,
    ).toBe(2);
  });

  it.each([
    "STALE",
    "FUTURE",
    "BEFORE_POLICY_FLOOR",
    "MISSING_PHASE",
    "BODY_HASH",
    "REDIRECT",
    "SAME_TIME",
    "REVERSED_TIME",
    "DUPLICATE_EVIDENCE_ID",
    "DUPLICATE_REQUEST_ID",
    "DUPLICATE_HEADER_HASH",
  ])("rejects invalid saved liveness evidence: %s", (failureMode) => {
    const input = cloneStage1Input();
    const mutable = input.fixture as unknown as {
      observations: Array<{
        evidenceId: string;
        observedAtUtc: string;
        rawBodySha256: string;
        redirectCount: number;
        requestId: string;
        responseHeadersSha256: string;
      }>;
    };

    if (failureMode === "STALE") {
      mutable.observations[0]!.observedAtUtc = "2026-08-30T03:00:00.000Z";
    } else if (failureMode === "FUTURE") {
      mutable.observations[1]!.observedAtUtc = "2026-08-30T06:00:00.000Z";
    } else if (failureMode === "BEFORE_POLICY_FLOOR") {
      mutable.observations[0]!.observedAtUtc = "2026-08-30T04:59:59.000Z";
    } else if (failureMode === "MISSING_PHASE") {
      mutable.observations.pop();
    } else if (failureMode === "BODY_HASH") {
      mutable.observations[1]!.rawBodySha256 = "f".repeat(64);
    } else if (failureMode === "REDIRECT") {
      mutable.observations[1]!.redirectCount = 1;
    } else if (failureMode === "SAME_TIME") {
      mutable.observations[1]!.observedAtUtc = mutable.observations[0]!.observedAtUtc;
    } else if (failureMode === "REVERSED_TIME") {
      mutable.observations[1]!.observedAtUtc = "2026-08-30T05:18:00.000Z";
    } else if (failureMode === "DUPLICATE_EVIDENCE_ID") {
      mutable.observations[1]!.evidenceId = mutable.observations[0]!.evidenceId;
    } else if (failureMode === "DUPLICATE_REQUEST_ID") {
      mutable.observations[1]!.requestId = mutable.observations[0]!.requestId;
    } else {
      mutable.observations[1]!.responseHeadersSha256 =
        mutable.observations[0]!.responseHeadersSha256;
    }

    expect(() =>
      validateSavedLiveness(input.policy, input.fixture, input.command.evaluatedAtUtc),
    ).toThrow();
  });

  it("denies every requested network operation", () => {
    const input = loadStage1VerticalSliceInput();

    expect(() => assertNetworkOperationDenied(input.policy, "GET_JOB_DETAIL")).toThrow(/denied/);
  });
});
