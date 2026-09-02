import { describe, expect, it } from "vitest";

import { evaluateEligibilityAndFit } from "../../packages/core/src/index.js";
import { cloneStage1Input, loadStage1VerticalSliceInput } from "../helpers/stage1-fixtures.js";

describe("deterministic eligibility and explainable fit", () => {
  it("lists every material requirement once in source order", () => {
    const input = loadStage1VerticalSliceInput();
    const result = evaluateEligibilityAndFit(
      input.facts,
      input.fixture,
      input.command.evaluatedAtUtc,
    );

    expect(result.eligibility).toBe("ELIGIBLE");
    expect(result.fitDisposition).toBe("PROCEED_WITH_NAMED_GAPS");
    expect(result.requirements.map((row) => row.requirementId)).toEqual(
      input.fixture.savedPosting.requirements.map((requirement) => requirement.requirementId),
    );
    expect(new Set(result.requirements.map((row) => row.requirementId)).size).toBe(
      result.requirements.length,
    );
    expect(result.requirements.map((row) => row.sourceEvidenceRefs)).toEqual(
      input.fixture.savedPosting.requirements.map((requirement) =>
        Array.from(requirement.sourceEvidenceRefs),
      ),
    );
  });

  it("uses approved evidence references and no numeric score", () => {
    const input = loadStage1VerticalSliceInput();
    const result = evaluateEligibilityAndFit(
      input.facts,
      input.fixture,
      input.command.evaluatedAtUtc,
    );
    const serialized = JSON.stringify(result);

    expect(result.numericScoreUsed).toBe(false);
    expect(serialized).not.toMatch(/"score"|"rank"|"weight"/i);
    expect(
      result.requirements
        .filter((row) => row.result === "MATCHED")
        .every((row) => row.matchedEvidence[0]?.evidenceRef.startsWith("synthetic-evidence-")),
    ).toBe(true);
  });

  it.each(["HARD_MISMATCH", "HARD_UNKNOWN"])("blocks preparation for %s", (failureMode) => {
    const input = cloneStage1Input();
    const mutableFacts = input.facts as unknown as {
      facts: Array<{ factKey: string; value: unknown }>;
    };
    const workAuthorizationIndex = mutableFacts.facts.findIndex(
      (fact) => fact.factKey === "authorized_to_work_us_full_time",
    );

    expect(workAuthorizationIndex).toBeGreaterThanOrEqual(0);

    if (failureMode === "HARD_MISMATCH") {
      mutableFacts.facts[workAuthorizationIndex]!.value = false;
    } else {
      mutableFacts.facts.splice(workAuthorizationIndex, 1);
    }

    const result = evaluateEligibilityAndFit(
      input.facts,
      input.fixture,
      input.command.evaluatedAtUtc,
    );

    expect(result.fitDisposition).toBe("BLOCKED");
    expect(result.eligibility).toBe(
      failureMode === "HARD_MISMATCH" ? "INELIGIBLE" : "INDETERMINATE",
    );
  });
});
