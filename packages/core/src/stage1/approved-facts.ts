import type { ApprovedFact, ApprovedFactsSnapshot, FactUse } from "./contracts.js";
import { Stage1ValidationError, parseApprovedFactsSnapshot } from "./contracts.js";

function parseUtc(value: string, label: string): number {
  const parsed = Date.parse(value);

  if (!value.endsWith("Z") || !Number.isFinite(parsed)) {
    throw new Stage1ValidationError("INVALID_UTC_TIMESTAMP", `${label} must be UTC`);
  }

  return parsed;
}

function isSupportedFactValue(value: unknown): boolean {
  if (typeof value === "string" || typeof value === "boolean") {
    return true;
  }

  if (typeof value === "number") {
    return Number.isFinite(value);
  }

  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

export function validateApprovedFacts(
  snapshot: ApprovedFactsSnapshot,
  evaluatedAtUtc: string,
): ReadonlyMap<string, ApprovedFact> {
  snapshot = parseApprovedFactsSnapshot(snapshot);
  if (snapshot.classification !== "SYNTHETIC") {
    throw new Stage1ValidationError(
      "REAL_PERSONAL_DATA_NOT_ALLOWED",
      "Prompt-5 facts must be synthetic",
    );
  }

  if (
    !snapshot.snapshotId ||
    !snapshot.subjectId ||
    snapshot.version < 1 ||
    !snapshot.approvalRef
  ) {
    throw new Stage1ValidationError(
      "INVALID_FACTS_SNAPSHOT",
      "facts snapshot identity is incomplete",
    );
  }

  const evaluationTime = parseUtc(evaluatedAtUtc, "evaluatedAtUtc");
  const approvedTime = parseUtc(snapshot.approvedAtUtc, "facts.approvedAtUtc");

  if (approvedTime > evaluationTime) {
    throw new Stage1ValidationError(
      "FACTS_APPROVED_IN_FUTURE",
      "facts approval cannot be after evaluation",
    );
  }

  const factsByKey = new Map<string, ApprovedFact>();
  const factIds = new Set<string>();

  for (const fact of snapshot.facts) {
    if (!fact.factId || !fact.factKey || fact.version < 1) {
      throw new Stage1ValidationError("INVALID_APPROVED_FACT", "fact identity is incomplete");
    }

    if (fact.status !== "APPROVED") {
      throw new Stage1ValidationError("UNAPPROVED_FACT", `fact ${fact.factId} is not approved`);
    }

    if (!isSupportedFactValue(fact.value)) {
      throw new Stage1ValidationError(
        "INVALID_FACT_VALUE",
        `fact ${fact.factId} has invalid value`,
      );
    }

    if (fact.allowedUses.length === 0 || !fact.provenance.evidenceRef) {
      throw new Stage1ValidationError(
        "FACT_PROVENANCE_REQUIRED",
        `fact ${fact.factId} lacks allowed use or provenance`,
      );
    }

    if (
      !fact.allowedUses.every((use) => (["ELIGIBILITY", "FIT", "PACKET"] as const).includes(use)) ||
      !["STANDARD", "SENSITIVE"].includes(fact.sensitivity) ||
      !Array.isArray(fact.correctionHistory)
    ) {
      throw new Stage1ValidationError(
        "INVALID_APPROVED_FACT",
        `fact ${fact.factId} has invalid policy metadata`,
      );
    }

    if (!fact.provenance.approvedByRef || !fact.provenance.approvedAtUtc) {
      throw new Stage1ValidationError(
        "FACT_PROVENANCE_REQUIRED",
        `fact ${fact.factId} lacks approval provenance`,
      );
    }

    const factApprovedAt = parseUtc(
      fact.provenance.approvedAtUtc,
      `${fact.factId}.provenance.approvedAtUtc`,
    );

    if (factApprovedAt > evaluationTime) {
      throw new Stage1ValidationError(
        "FACTS_APPROVED_IN_FUTURE",
        `fact ${fact.factId} approval cannot be after evaluation`,
      );
    }

    const effectiveFrom = parseUtc(fact.effectiveFromUtc, `${fact.factId}.effectiveFromUtc`);
    const effectiveTo =
      fact.effectiveToUtc === null
        ? null
        : parseUtc(fact.effectiveToUtc, `${fact.factId}.effectiveToUtc`);

    if (effectiveFrom > evaluationTime || (effectiveTo !== null && effectiveTo < evaluationTime)) {
      throw new Stage1ValidationError(
        "FACT_NOT_EFFECTIVE",
        `fact ${fact.factId} is not effective at evaluation`,
      );
    }

    if (factIds.has(fact.factId) || factsByKey.has(fact.factKey)) {
      throw new Stage1ValidationError("DUPLICATE_FACT", `duplicate fact ${fact.factId}`);
    }

    factIds.add(fact.factId);
    factsByKey.set(fact.factKey, fact);
  }

  return factsByKey;
}

export function factAllowsUse(fact: ApprovedFact, use: FactUse): boolean {
  return fact.allowedUses.includes(use);
}
