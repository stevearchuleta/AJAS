import { factAllowsUse, validateApprovedFacts } from "./approved-facts.js";
import type {
  ApprovedFact,
  ApprovedFactsSnapshot,
  FactUse,
  FactValue,
  FitRequirementResult,
  PostingRequirement,
  SavedPostingFixture,
  ScreeningResult,
} from "./contracts.js";
import { Stage1ValidationError, parseSavedPostingFixture } from "./contracts.js";

function isStringArray(value: FactValue): value is readonly string[] {
  return Array.isArray(value);
}

function factValueMatches(actual: FactValue, requirement: PostingRequirement): boolean {
  switch (requirement.operator) {
    case "EQUALS": {
      const expected = requirement.expected;
      return isStringArray(actual) && isStringArray(expected)
        ? actual.length === expected.length &&
            actual.every((item, index) => item === expected[index])
        : actual === expected;
    }
    case "AT_LEAST":
      return (
        typeof actual === "number" &&
        typeof requirement.expected === "number" &&
        actual >= requirement.expected
      );
    case "INCLUDES_ALL":
      return (
        isStringArray(actual) &&
        isStringArray(requirement.expected) &&
        requirement.expected.every((expectedItem) => actual.includes(expectedItem))
      );
    case "INCLUDES_ANY":
      return (
        isStringArray(actual) &&
        isStringArray(requirement.expected) &&
        requirement.expected.some((expectedItem) => actual.includes(expectedItem))
      );
  }
}

function requiredFactUse(requirement: PostingRequirement): FactUse {
  return requirement.gate === "ELIGIBILITY" ? "ELIGIBILITY" : "FIT";
}

function resultForMissingFact(requirement: PostingRequirement): FitRequirementResult {
  const isPreferred = requirement.materiality === "PREFERRED";

  return {
    requirementId: requirement.requirementId,
    label: requirement.label,
    gate: requirement.gate,
    materiality: requirement.materiality,
    result: isPreferred ? "GAP" : "UNRESOLVED",
    reasonCode: "NO_APPROVED_FACT",
    extractionConfidence: requirement.extractionConfidence,
    sourceEvidenceRefs: requirement.sourceEvidenceRefs,
    matchedEvidence: [],
    namedGap: `No approved fact resolves ${requirement.requirementId}`,
  };
}

function resultForFact(requirement: PostingRequirement, fact: ApprovedFact): FitRequirementResult {
  if (requirement.extractionConfidence === "LOW") {
    return {
      requirementId: requirement.requirementId,
      label: requirement.label,
      gate: requirement.gate,
      materiality: requirement.materiality,
      result: requirement.materiality === "REQUIRED" ? "UNRESOLVED" : "GAP",
      reasonCode: "LOW_EXTRACTION_CONFIDENCE",
      extractionConfidence: requirement.extractionConfidence,
      sourceEvidenceRefs: requirement.sourceEvidenceRefs,
      matchedEvidence: [],
      namedGap: `Low-confidence extraction requires review for ${requirement.requirementId}`,
    };
  }

  if (!factAllowsUse(fact, requiredFactUse(requirement))) {
    return {
      requirementId: requirement.requirementId,
      label: requirement.label,
      gate: requirement.gate,
      materiality: requirement.materiality,
      result: requirement.materiality === "REQUIRED" ? "UNRESOLVED" : "GAP",
      reasonCode: "FACT_NOT_ALLOWED_FOR_USE",
      extractionConfidence: requirement.extractionConfidence,
      sourceEvidenceRefs: requirement.sourceEvidenceRefs,
      matchedEvidence: [],
      namedGap: `Approved fact ${fact.factId} is not allowed for ${requiredFactUse(requirement)}`,
    };
  }

  if (!factValueMatches(fact.value, requirement)) {
    return {
      requirementId: requirement.requirementId,
      label: requirement.label,
      gate: requirement.gate,
      materiality: requirement.materiality,
      result: requirement.materiality === "REQUIRED" ? "DISQUALIFIER" : "GAP",
      reasonCode: "APPROVED_FACT_DOES_NOT_MATCH",
      extractionConfidence: requirement.extractionConfidence,
      sourceEvidenceRefs: requirement.sourceEvidenceRefs,
      matchedEvidence: [
        {
          factId: fact.factId,
          factVersion: fact.version,
          evidenceRef: fact.provenance.evidenceRef,
          approvedByRef: fact.provenance.approvedByRef,
        },
      ],
      namedGap: `Approved fact ${fact.factId} does not satisfy ${requirement.requirementId}`,
    };
  }

  return {
    requirementId: requirement.requirementId,
    label: requirement.label,
    gate: requirement.gate,
    materiality: requirement.materiality,
    result: "MATCHED",
    reasonCode: "APPROVED_FACT_MATCH",
    extractionConfidence: requirement.extractionConfidence,
    sourceEvidenceRefs: requirement.sourceEvidenceRefs,
    matchedEvidence: [
      {
        factId: fact.factId,
        factVersion: fact.version,
        evidenceRef: fact.provenance.evidenceRef,
        approvedByRef: fact.provenance.approvedByRef,
      },
    ],
    namedGap: null,
  };
}

export function evaluateEligibilityAndFit(
  snapshot: ApprovedFactsSnapshot,
  fixture: SavedPostingFixture,
  evaluatedAtUtc: string,
): ScreeningResult {
  fixture = parseSavedPostingFixture(fixture);
  const factsByKey = validateApprovedFacts(snapshot, evaluatedAtUtc);
  const requirementIds = new Set<string>();

  if (fixture.savedPosting.requirements.length === 0) {
    throw new Stage1ValidationError("REQUIREMENTS_MISSING", "posting has no material requirements");
  }

  const requirements = fixture.savedPosting.requirements.map((requirement) => {
    if (requirementIds.has(requirement.requirementId)) {
      throw new Stage1ValidationError(
        "DUPLICATE_REQUIREMENT",
        `duplicate requirement ${requirement.requirementId}`,
      );
    }

    requirementIds.add(requirement.requirementId);
    const fact = factsByKey.get(requirement.factKey);
    return fact === undefined
      ? resultForMissingFact(requirement)
      : resultForFact(requirement, fact);
  });

  const eligibilityRows = requirements.filter((row) => row.gate === "ELIGIBILITY");

  if (eligibilityRows.length === 0) {
    throw new Stage1ValidationError(
      "ELIGIBILITY_REQUIREMENTS_MISSING",
      "posting has no explicit eligibility requirements",
    );
  }

  const eligibility = eligibilityRows.some((row) => row.result === "DISQUALIFIER")
    ? "INELIGIBLE"
    : eligibilityRows.some((row) => row.result !== "MATCHED")
      ? "INDETERMINATE"
      : "ELIGIBLE";
  const disqualifiers = requirements
    .filter((row) => row.result === "DISQUALIFIER")
    .map((row) => row.requirementId);
  const unresolvedRequirements = requirements
    .filter((row) => row.result === "UNRESOLVED")
    .map((row) => row.requirementId);
  const namedGaps = requirements
    .filter((row) => row.namedGap !== null)
    .map((row) => row.namedGap as string);
  const hasRequiredBlocker = requirements.some(
    (row) =>
      row.materiality === "REQUIRED" &&
      (row.result === "UNRESOLVED" || row.result === "DISQUALIFIER"),
  );
  const fitDisposition = hasRequiredBlocker
    ? "BLOCKED"
    : namedGaps.length > 0
      ? "PROCEED_WITH_NAMED_GAPS"
      : "PROCEED";

  return {
    eligibility,
    fitDisposition,
    requirements,
    disqualifiers,
    unresolvedRequirements,
    namedGaps,
    userOverride: null,
    numericScoreUsed: false,
  };
}
