import { describe, expect, it } from "vitest";

import {
  evaluateEligibilityAndFit,
  validateApprovedFacts,
  type ApprovedFactsSnapshot,
} from "../../packages/core/src/index.js";
import { cloneStage1Input, loadStage1VerticalSliceInput } from "../helpers/stage1-fixtures.js";

describe("approved applicant facts", () => {
  it("accepts a versioned synthetic snapshot with claim-level provenance", () => {
    const input = loadStage1VerticalSliceInput();
    const facts = validateApprovedFacts(input.facts, input.command.evaluatedAtUtc);

    expect(facts.size).toBe(9);
    expect(
      facts.get("years_relevant_fpa_or_corporate_finance_experience")?.provenance.evidenceRef,
    ).toBe("synthetic-evidence-relevant-finance-years-001");
  });

  it.each(["UNAPPROVED", "MISSING_PROVENANCE", "DISALLOWED_USE"])(
    "fails closed for %s facts",
    (failureMode) => {
      const input = cloneStage1Input();
      const mutable = input as unknown as {
        facts: {
          facts: Array<{
            status: string;
            allowedUses: string[];
            provenance: { evidenceRef: string };
          }>;
        };
      };
      const target = mutable.facts.facts[2];

      expect(target).toBeDefined();

      if (target === undefined) {
        return;
      }

      if (failureMode === "UNAPPROVED") {
        target.status = "DRAFT";
      } else if (failureMode === "MISSING_PROVENANCE") {
        target.provenance.evidenceRef = "";
      } else {
        target.allowedUses = ["PACKET"];
      }

      if (failureMode === "DISALLOWED_USE") {
        const result = evaluateEligibilityAndFit(
          input.facts,
          input.fixture,
          input.command.evaluatedAtUtc,
        );
        expect(result.fitDisposition).toBe("BLOCKED");
        expect(result.unresolvedRequirements).toContain("req_7_years_relevant_finance");
      } else {
        expect(() => validateApprovedFacts(input.facts, input.command.evaluatedAtUtc)).toThrow();
      }
    },
  );

  it("keeps an absent preferred fact as an explicit named gap", () => {
    const input = loadStage1VerticalSliceInput();
    const result = evaluateEligibilityAndFit(
      input.facts as ApprovedFactsSnapshot,
      input.fixture,
      input.command.evaluatedAtUtc,
    );
    const planningTools = result.requirements.find(
      (row) => row.requirementId === "req_planning_platforms",
    );

    expect(planningTools?.result).toBe("GAP");
    expect(planningTools?.reasonCode).toBe("NO_APPROVED_FACT");
    expect(planningTools?.namedGap).toContain("No approved fact");
  });
});
