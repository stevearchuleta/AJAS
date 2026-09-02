export const STAGE1_EXECUTION_MODE = "FIXTURE_ONLY" as const;
export const STAGE1_READINESS_SCOPE = "STAGE1_VERTICAL_SLICE_TEST" as const;
export const SAVED_FIXTURE_OPERATION = "PROCESS_SAVED_FIXTURE" as const;

export type FactUse = "ELIGIBILITY" | "FIT" | "PACKET";
export type FactValue = string | number | boolean | readonly string[];

export interface FactProvenance {
  readonly evidenceRef: string;
  readonly approvedByRef: string;
  readonly approvedAtUtc: string;
}

export interface ApprovedFact {
  readonly factId: string;
  readonly factKey: string;
  readonly version: number;
  readonly value: FactValue;
  readonly status: "APPROVED";
  readonly allowedUses: readonly FactUse[];
  readonly sensitivity: "STANDARD" | "SENSITIVE";
  readonly effectiveFromUtc: string;
  readonly effectiveToUtc: string | null;
  readonly correctionHistory: readonly string[];
  readonly provenance: FactProvenance;
}

export interface ApprovedFactsSnapshot {
  readonly schemaVersion: "ajas.approved-facts.v1";
  readonly snapshotId: string;
  readonly subjectId: string;
  readonly version: number;
  readonly classification: "SYNTHETIC";
  readonly approvedAtUtc: string;
  readonly approvalRef: string;
  readonly facts: readonly ApprovedFact[];
}

export type SourcePolicyState = "ENABLED" | "MANUAL_ONLY" | "UNDER_REVIEW" | "DISABLED" | "EXPIRED";

export interface ReviewReference {
  readonly url: string;
  readonly reviewedAtUtc: string;
  readonly timestampBasis: "DETERMINISTIC_FIXTURE_CLOCK_NOT_OBSERVED_WALL_CLOCK";
  readonly finding: string;
}

export interface SourcePolicy {
  readonly schemaVersion: "ajas.source-policy.v1";
  readonly policyId: string;
  readonly policyVersion: number;
  readonly sourceKey: string;
  readonly provider: "GREENHOUSE";
  readonly boardToken: string;
  readonly sourceType: "PUBLIC_ATS_JOB_BOARD";
  readonly environment: "TEST";
  readonly state: SourcePolicyState;
  readonly effectiveFromUtc: string;
  readonly effectiveTimestampBasis: "DETERMINISTIC_FIXTURE_CLOCK_NOT_RUNTIME_AUTHORIZATION";
  readonly expiresAtUtc: string;
  readonly fixtureControlBasis: "PROMPT5_TEST_CONTROLS_NOT_RATIFIED_RUNTIME_TARGETS";
  readonly ownerRole: string;
  readonly documentation: ReviewReference;
  readonly terms: ReviewReference;
  readonly allowedOperations: readonly (typeof SAVED_FIXTURE_OPERATION)[];
  readonly prohibitedOperations: readonly string[];
  readonly allowedApiHosts: readonly string[];
  readonly allowedPublicHosts: readonly string[];
  readonly detailPathTemplate: string;
  readonly allowedNetworkMethods: readonly string[];
  readonly authenticationRequirement: "NONE_FOR_DOCUMENTED_GET_RUNTIME_STILL_DISABLED";
  readonly credentialsAllowed: false;
  readonly cookiesAllowed: false;
  readonly redirectsAllowed: false;
  readonly providerRateLimit: string;
  readonly runtimeRequestBudget: 0;
  readonly runtimeCacheTtlSeconds: 0;
  readonly fixtureRetention: string;
  readonly attributionRequirements: readonly string[];
  readonly dataFieldsCollected: readonly string[];
  readonly identityFields: readonly string[];
  readonly canonicalPostingIdentityMethod: "PROVIDER_BOARD_EXTERNAL_ID_AND_CANONICAL_URL";
  readonly savedLivenessMaxAgeSeconds: number;
  readonly livenessMethod: "SAVED_PUBLIC_DETAIL_GET";
  readonly changeMonitoringOwner: string;
  readonly networkKillSwitch: true;
  readonly runtimeEnablementApproved: false;
  readonly approvedFixtureId: string;
  readonly approvedRawBodySha256: string;
  readonly approvedSavedPostingSha256: string;
  readonly approvedResponseHeadersSha256: readonly [string, string];
  readonly approvedFactsSnapshotId: string;
  readonly approvedFactsSnapshotSha256: string;
  readonly approvedCommandSha256: string;
}

export interface SavedCaptureObservation {
  readonly evidenceId: string;
  readonly phase: "INTAKE" | "PRE_READY";
  readonly observedAtUtc: string;
  readonly observedStatus: "LIVE_AT_CAPTURE";
  readonly currentStatus: "NOT_CHECKED";
  readonly method: "SAVED_PUBLIC_DETAIL_GET";
  readonly httpStatus: 200;
  readonly contentType: "application/json";
  readonly contentLength: number;
  readonly etag: string;
  readonly requestId: string;
  readonly responseHeadersSha256: string;
  readonly rawBodySha256: string;
  readonly requestUrl: string;
  readonly finalUrl: string;
  readonly authentication: "NONE";
  readonly credentialsSent: false;
  readonly cookiesSent: false;
  readonly redirectCount: 0;
}

export type RequirementOperator = "EQUALS" | "AT_LEAST" | "INCLUDES_ALL" | "INCLUDES_ANY";

export interface PostingRequirement {
  readonly requirementId: string;
  readonly label: string;
  readonly gate: "ELIGIBILITY" | "FIT";
  readonly materiality: "REQUIRED" | "PREFERRED";
  readonly factKey: string;
  readonly operator: RequirementOperator;
  readonly expected: FactValue;
  readonly extractionConfidence: "HIGH" | "MEDIUM" | "LOW";
  readonly sourceEvidenceRefs: readonly string[];
  readonly derivation: "HUMAN_REVIEWED_PARAPHRASE";
}

export interface EvidencePointerBasis {
  readonly jsonPointer: "/content" | "/location/name";
  readonly representation: "RFC8259_DECODED_SCALAR_UTF8";
  readonly valueBytes: number;
  readonly valueSha256: string;
}

export interface SourceFragmentEvidence {
  readonly evidenceId: string;
  readonly jsonPointer: "/content" | "/location/name";
  readonly startByte: number;
  readonly endByteExclusive: number;
  readonly fragmentByteLength: number;
  readonly fragmentSha256: string;
}

export interface MinimizedSavedPosting {
  readonly id: number;
  readonly internalJobId: number;
  readonly title: string;
  readonly companyName: string;
  readonly locationName: string;
  readonly firstPublished: string;
  readonly updatedAt: string;
  readonly applicationDeadline: string | null;
  readonly anticipatedClosingDate: {
    readonly humanReviewedDate: string;
    readonly structuredApiValue: null;
    readonly status: "UNSTRUCTURED_DATE_PRESERVED_SEPARATELY";
    readonly sourceEvidenceRefs: readonly string[];
  };
  readonly language: string;
  readonly canonicalPostingUrl: string;
  readonly evidenceBasis: {
    readonly captureSha256: string;
    readonly pointers: readonly EvidencePointerBasis[];
    readonly reviewedByRef: string;
    readonly reviewedAtUtc: string;
    readonly reviewedScope: readonly (
      "ROLE_LOCATION" | "WORK_AUTHORIZATION" | "QUALIFICATIONS" | "ANTICIPATED_CLOSING_DATE"
    )[];
    readonly rawContentRetainedInRepository: false;
  };
  readonly sourceEvidence: readonly SourceFragmentEvidence[];
  readonly requirements: readonly PostingRequirement[];
  readonly untrustedContentMarker: string;
}

export interface SavedPostingFixture {
  readonly schemaVersion: "ajas.saved-greenhouse-fixture.v1";
  readonly fixtureId: string;
  readonly classification: "PUBLIC_JOB_POSTING_SNAPSHOT";
  readonly fixtureTransform: "MINIMIZED_HUMAN_REVIEWED_DERIVATIVE";
  readonly source: {
    readonly provider: "GREENHOUSE";
    readonly boardToken: string;
    readonly sourceKey: string;
    readonly externalPostingId: string;
    readonly requestMethod: "GET";
    readonly requestUrl: string;
    readonly canonicalPostingUrl: string;
    readonly documentationUrl: string;
  };
  readonly capture: {
    readonly actor: "AJAS_FIXTURE_AUTHOR";
    readonly tool: "curl";
    readonly toolVersion: "8.5.0";
    readonly commandEvidenceRef: string;
    readonly rawBodyAvailableInRepository: false;
    readonly responseHeadersAvailableInRepository: false;
    readonly rawBodySha256: string;
    readonly rawBodyBytes: number;
    readonly minimizationReason: string;
  };
  readonly observations: readonly SavedCaptureObservation[];
  readonly savedPosting: MinimizedSavedPosting;
  readonly savedPostingSha256: string;
  readonly parserVersion: string;
}

export interface Stage1FixtureCommand {
  readonly schemaVersion: "ajas.stage1-fixture-command.v1";
  readonly executionMode: typeof STAGE1_EXECUTION_MODE;
  readonly environment: "TEST_FIXTURE";
  readonly evaluatedAtUtc: string;
  readonly userId: string;
  readonly subjectId: string;
  readonly actorId: string;
  readonly actorVersion: string;
  readonly applicationId: string;
  readonly runId: string;
  readonly correlationId: string;
  readonly idempotencyKey: string;
  readonly factsSnapshotId: string;
  readonly factsSnapshotVersion: number;
  readonly factsSnapshotSha256: string;
  readonly postingFixtureId: string;
  readonly sourcePolicyId: string;
  readonly sourcePolicyVersion: number;
  readonly authorizationRef: string;
  readonly selectionAuthorizationRef: string;
}

export interface SourcePolicyDecision {
  readonly decision: "ALLOW_FIXTURE_PROCESSING";
  readonly operation: typeof SAVED_FIXTURE_OPERATION;
  readonly policyId: string;
  readonly policyVersion: number;
  readonly sourceKey: string;
  readonly networkAuthorized: false;
  readonly reason: "EXACT_BOARD_POLICY_ALLOWS_OFFLINE_FIXTURE_ONLY";
}

export interface LivenessDecision {
  readonly decision: "VALID_SAVED_EVIDENCE";
  readonly currentStatus: "NOT_CHECKED";
  readonly evidence: readonly {
    readonly evidenceId: string;
    readonly phase: "INTAKE" | "PRE_READY";
    readonly observedStatus: "LIVE_AT_CAPTURE";
    readonly observedAtUtc: string;
    readonly ageSecondsAtEvaluation: number;
    readonly rawBodySha256: string;
  }[];
}

export interface FitRequirementResult {
  readonly requirementId: string;
  readonly label: string;
  readonly gate: "ELIGIBILITY" | "FIT";
  readonly materiality: "REQUIRED" | "PREFERRED";
  readonly result: "MATCHED" | "GAP" | "UNRESOLVED" | "DISQUALIFIER";
  readonly reasonCode:
    | "APPROVED_FACT_MATCH"
    | "NO_APPROVED_FACT"
    | "APPROVED_FACT_DOES_NOT_MATCH"
    | "FACT_NOT_ALLOWED_FOR_USE"
    | "LOW_EXTRACTION_CONFIDENCE";
  readonly extractionConfidence: "HIGH" | "MEDIUM" | "LOW";
  readonly sourceEvidenceRefs: readonly string[];
  readonly matchedEvidence: readonly {
    readonly factId: string;
    readonly factVersion: number;
    readonly evidenceRef: string;
    readonly approvedByRef: string;
  }[];
  readonly namedGap: string | null;
}

export interface ScreeningResult {
  readonly eligibility: "ELIGIBLE" | "INELIGIBLE" | "INDETERMINATE";
  readonly fitDisposition: "PROCEED" | "PROCEED_WITH_NAMED_GAPS" | "BLOCKED";
  readonly requirements: readonly FitRequirementResult[];
  readonly disqualifiers: readonly string[];
  readonly unresolvedRequirements: readonly string[];
  readonly namedGaps: readonly string[];
  readonly userOverride: null;
  readonly numericScoreUsed: false;
}

export interface PacketArtifactMetadata {
  readonly artifactId: string;
  readonly kind: "POSTING_SNAPSHOT" | "FIT_EXPLANATION" | "REVIEW_HANDOFF";
  readonly filename: string;
  readonly mimeType: "application/json";
  readonly bytes: number;
  readonly sha256: string;
  readonly readbackSha256: string;
  readonly readbackStatus: "PASS";
}

export interface PacketMetadata {
  readonly schemaVersion: "ajas.packet-metadata.v1";
  readonly packetId: string;
  readonly applicationId: string;
  readonly subjectId: string;
  readonly runId: string;
  readonly inputSha256: string;
  readonly commandSha256: string;
  readonly executionMode: typeof STAGE1_EXECUTION_MODE;
  readonly readinessScope: typeof STAGE1_READINESS_SCOPE;
  readonly productionReady: false;
  readonly factsSnapshotId: string;
  readonly factsSnapshotVersion: number;
  readonly factsSnapshotSha256: string;
  readonly postingFixtureId: string;
  readonly postingExternalId: string;
  readonly postingRawBodySha256: string;
  readonly postingSavedSha256: string;
  readonly sourcePolicyId: string;
  readonly sourcePolicyVersion: number;
  readonly sourcePolicySha256: string;
  readonly parserVersion: string;
  readonly rulesVersion: string;
  readonly validatorVersion: string;
  readonly templateVersion: string;
  readonly officialPostingUrl: string;
  readonly officialPostingUrlPurpose: "SAVED_FIXTURE_SOURCE_PROVENANCE_ONLY";
  readonly artifactStore: "IN_MEMORY_FIXTURE_STORE";
  readonly authoritativeByteStoreUsed: false;
  readonly artifacts: readonly PacketArtifactMetadata[];
  readonly validation: {
    readonly extractionScope: "REVIEWED_MINIMIZED_SCOPE_ONLY";
    readonly completeness: "PASS_FOR_DECLARED_SCOPE";
    readonly byteHashReadback: "PASS";
    readonly finalSavedLiveness: "VALID_SAVED_EVIDENCE";
    readonly currentLiveness: "NOT_CHECKED";
    readonly status: "PASS";
    readonly validatedAtUtc: string;
  };
  readonly employerActionsPerformed: readonly [];
  readonly nextAutonomousAction: null;
}

export type SliceState = "DISCOVERED" | "SCREENED" | "SELECTED" | "PREPARING" | "READY_FOR_REVIEW";

export interface AuditEvent {
  readonly schemaVersion: "ajas.audit-event.v1";
  readonly eventId: string;
  readonly timestampUtc: string;
  readonly userId: string;
  readonly subjectId: string;
  readonly actorId: string;
  readonly actorVersion: string;
  readonly action: "APPLICATION_STATE_TRANSITION" | "VERTICAL_SLICE_DENIED";
  readonly targetId: string;
  readonly priorState: SliceState | null;
  readonly newState: SliceState | null;
  readonly authorizationRef: string;
  readonly evidenceRefs: readonly string[];
  readonly idempotencyKey: string;
  readonly outcome: "SUCCESS" | "DENIED";
  readonly failureCode: string | null;
  readonly correlationId: string;
  readonly environment: "TEST_FIXTURE";
  readonly classification: "SYNTHETIC";
}

export interface AuditCommitReceipt {
  readonly store: "IN_MEMORY_FIXTURE_AUDIT";
  readonly status: "COMMITTED";
  readonly eventCount: number;
  readonly batchSha256: string;
}

export interface Stage1VerticalSliceResult {
  readonly schemaVersion: "ajas.stage1-vertical-slice-result.v1";
  readonly executionMode: typeof STAGE1_EXECUTION_MODE;
  readonly readinessScope: typeof STAGE1_READINESS_SCOPE;
  readonly productionReady: false;
  readonly applicationId: string;
  readonly subjectId: string;
  readonly correlationId: string;
  readonly idempotencyKey: string;
  readonly inputSha256: string;
  readonly sourcePolicyDecision: SourcePolicyDecision;
  readonly livenessDecision: LivenessDecision;
  readonly screening: ScreeningResult;
  readonly packetMetadata: PacketMetadata;
  readonly state: "READY_FOR_REVIEW";
  readonly stateHistory: readonly SliceState[];
  readonly auditEvents: readonly AuditEvent[];
  readonly auditCommit: AuditCommitReceipt;
  readonly humanBoundary: {
    readonly terminalState: "READY_FOR_REVIEW";
    readonly employerActionPermitted: false;
    readonly employerActionsPerformed: readonly [];
    readonly officialPostingUrl: string;
    readonly officialPostingUrlPurpose: "SAVED_FIXTURE_SOURCE_PROVENANCE_ONLY";
    readonly requiredHumanAction: string;
  };
}

export interface Stage1VerticalSliceInput {
  readonly command: Stage1FixtureCommand;
  readonly facts: ApprovedFactsSnapshot;
  readonly policy: SourcePolicy;
  readonly fixture: SavedPostingFixture;
}

export class Stage1ValidationError extends Error {
  public readonly code: string;

  public constructor(code: string, message: string) {
    super(message);
    this.name = "Stage1ValidationError";
    this.code = code;
  }
}

type JsonRecord = Record<string, unknown>;

function record(value: unknown, label: string): JsonRecord {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label} must be an object`);
  }
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label} must be a plain JSON object`);
  }
  return value as JsonRecord;
}

function exact(value: JsonRecord, keys: readonly string[], label: string): void {
  const expected = new Set(keys);
  const actual = Object.keys(value);
  if (actual.length !== expected.size || actual.some((key) => !expected.has(key))) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label} must contain exactly the v1 contract fields`,
    );
  }
}

function text(value: JsonRecord, key: string, label: string): string {
  const candidate = value[key];
  if (typeof candidate !== "string" || candidate.length === 0) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label}.${key} must be nonempty text`);
  }
  return candidate;
}

function integer(value: JsonRecord, key: string, label: string, minimum = 0): number {
  const candidate = value[key];
  if (typeof candidate !== "number" || !Number.isSafeInteger(candidate) || candidate < minimum) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label}.${key} must be an integer >= ${minimum}`,
    );
  }
  return candidate;
}

function literal<T extends string | number | boolean | null>(
  value: JsonRecord,
  key: string,
  expected: T,
  label: string,
): T {
  if (value[key] !== expected) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label}.${key} must equal ${String(expected)}`,
    );
  }
  return expected;
}

function oneOf<T extends string>(
  value: JsonRecord,
  key: string,
  values: readonly T[],
  label: string,
): T {
  const candidate = value[key];
  if (typeof candidate !== "string" || !values.includes(candidate as T)) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label}.${key} is outside the closed v1 vocabulary`,
    );
  }
  return candidate as T;
}

function array(value: JsonRecord, key: string, label: string): unknown[] {
  const candidate = value[key];
  if (!Array.isArray(candidate)) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label}.${key} must be an array`);
  }
  return candidate;
}

function strings(value: JsonRecord, key: string, label: string, allowEmpty = false): string[] {
  const candidates = array(value, key, label);
  if (
    (!allowEmpty && candidates.length === 0) ||
    candidates.some((candidate) => typeof candidate !== "string" || candidate.length === 0)
  ) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label}.${key} must contain${allowEmpty ? " only" : " one or more"} nonempty strings`,
    );
  }
  return candidates as string[];
}

function unique(values: readonly string[], label: string): void {
  if (new Set(values).size !== values.length) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label} must be unique`);
  }
}

function sha256(value: string, label: string): void {
  if (!/^[a-f0-9]{64}$/.test(value)) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label} must be lowercase SHA-256`);
  }
}

function utc(value: string, label: string): void {
  const parsed = Date.parse(value);
  const normalized = Number.isFinite(parsed) ? new Date(parsed).toISOString() : "";
  const normalizedWithoutMilliseconds = normalized.replace(".000Z", "Z");
  if (value !== normalized && value !== normalizedWithoutMilliseconds) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label} must be a canonical UTC ISO-8601 timestamp`,
    );
  }
}

function iso(value: string, label: string): void {
  if (!Number.isFinite(Date.parse(value))) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label} must be an ISO-8601 timestamp`);
  }
}

function factValue(value: JsonRecord, key: string, label: string): FactValue {
  const candidate = value[key];
  if (typeof candidate === "string" || typeof candidate === "boolean") return candidate;
  if (typeof candidate === "number" && Number.isFinite(candidate)) return candidate;
  if (
    Array.isArray(candidate) &&
    candidate.length > 0 &&
    candidate.every((item) => typeof item === "string" && item.length > 0)
  ) {
    unique(candidate as string[], `${label}.${key}`);
    return candidate as string[];
  }
  throw new Stage1ValidationError("VALIDATION_ERROR", `${label}.${key} is not a FactValue`);
}

function freezeValidated<T>(value: unknown): T {
  const cloned = structuredClone(value) as T;
  const freeze = (candidate: unknown): void => {
    if (typeof candidate !== "object" || candidate === null || Object.isFrozen(candidate)) return;
    for (const child of Object.values(candidate)) freeze(child);
    Object.freeze(candidate);
  };
  freeze(cloned);
  return cloned;
}

function parseProvenance(value: unknown, label: string): void {
  const item = record(value, label);
  exact(item, ["evidenceRef", "approvedByRef", "approvedAtUtc"], label);
  text(item, "evidenceRef", label);
  text(item, "approvedByRef", label);
  utc(text(item, "approvedAtUtc", label), `${label}.approvedAtUtc`);
}

function parseFact(value: unknown, label: string): void {
  const item = record(value, label);
  exact(
    item,
    [
      "factId",
      "factKey",
      "version",
      "value",
      "status",
      "allowedUses",
      "sensitivity",
      "effectiveFromUtc",
      "effectiveToUtc",
      "correctionHistory",
      "provenance",
    ],
    label,
  );
  text(item, "factId", label);
  text(item, "factKey", label);
  integer(item, "version", label, 1);
  factValue(item, "value", label);
  literal(item, "status", "APPROVED", label);
  const uses = strings(item, "allowedUses", label);
  unique(uses, `${label}.allowedUses`);
  if (!uses.every((use) => ["ELIGIBILITY", "FIT", "PACKET"].includes(use))) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label}.allowedUses is invalid`);
  }
  oneOf(item, "sensitivity", ["STANDARD", "SENSITIVE"] as const, label);
  utc(text(item, "effectiveFromUtc", label), `${label}.effectiveFromUtc`);
  if (item.effectiveToUtc !== null)
    utc(text(item, "effectiveToUtc", label), `${label}.effectiveToUtc`);
  strings(item, "correctionHistory", label, true);
  parseProvenance(item.provenance, `${label}.provenance`);
}

export function parseApprovedFactsSnapshot(value: unknown): ApprovedFactsSnapshot {
  const item = record(value, "facts");
  exact(
    item,
    [
      "schemaVersion",
      "snapshotId",
      "subjectId",
      "version",
      "classification",
      "approvedAtUtc",
      "approvalRef",
      "facts",
    ],
    "facts",
  );
  literal(item, "schemaVersion", "ajas.approved-facts.v1", "facts");
  text(item, "snapshotId", "facts");
  text(item, "subjectId", "facts");
  integer(item, "version", "facts", 1);
  literal(item, "classification", "SYNTHETIC", "facts");
  utc(text(item, "approvedAtUtc", "facts"), "facts.approvedAtUtc");
  text(item, "approvalRef", "facts");
  const facts = array(item, "facts", "facts");
  if (facts.length === 0)
    throw new Stage1ValidationError("VALIDATION_ERROR", "facts.facts is empty");
  facts.forEach((fact, index) => parseFact(fact, `facts.facts[${index}]`));
  const records = facts as JsonRecord[];
  unique(
    records.map((fact) => String(fact.factId)),
    "facts.factId",
  );
  unique(
    records.map((fact) => String(fact.factKey)),
    "facts.factKey",
  );
  return freezeValidated<ApprovedFactsSnapshot>(item);
}

function parseReview(value: unknown, label: string): void {
  const item = record(value, label);
  exact(item, ["url", "reviewedAtUtc", "timestampBasis", "finding"], label);
  text(item, "url", label);
  utc(text(item, "reviewedAtUtc", label), `${label}.reviewedAtUtc`);
  literal(item, "timestampBasis", "DETERMINISTIC_FIXTURE_CLOCK_NOT_OBSERVED_WALL_CLOCK", label);
  text(item, "finding", label);
}

export function parseSourcePolicy(value: unknown): SourcePolicy {
  const item = record(value, "policy");
  exact(
    item,
    [
      "schemaVersion",
      "policyId",
      "policyVersion",
      "sourceKey",
      "provider",
      "boardToken",
      "sourceType",
      "environment",
      "state",
      "effectiveFromUtc",
      "effectiveTimestampBasis",
      "expiresAtUtc",
      "fixtureControlBasis",
      "ownerRole",
      "documentation",
      "terms",
      "allowedOperations",
      "prohibitedOperations",
      "allowedApiHosts",
      "allowedPublicHosts",
      "detailPathTemplate",
      "allowedNetworkMethods",
      "authenticationRequirement",
      "credentialsAllowed",
      "cookiesAllowed",
      "redirectsAllowed",
      "providerRateLimit",
      "runtimeRequestBudget",
      "runtimeCacheTtlSeconds",
      "fixtureRetention",
      "attributionRequirements",
      "dataFieldsCollected",
      "identityFields",
      "canonicalPostingIdentityMethod",
      "savedLivenessMaxAgeSeconds",
      "livenessMethod",
      "changeMonitoringOwner",
      "networkKillSwitch",
      "runtimeEnablementApproved",
      "approvedFixtureId",
      "approvedRawBodySha256",
      "approvedSavedPostingSha256",
      "approvedResponseHeadersSha256",
      "approvedFactsSnapshotId",
      "approvedFactsSnapshotSha256",
      "approvedCommandSha256",
    ],
    "policy",
  );
  literal(item, "schemaVersion", "ajas.source-policy.v1", "policy");
  text(item, "policyId", "policy");
  integer(item, "policyVersion", "policy", 1);
  text(item, "sourceKey", "policy");
  literal(item, "provider", "GREENHOUSE", "policy");
  text(item, "boardToken", "policy");
  literal(item, "sourceType", "PUBLIC_ATS_JOB_BOARD", "policy");
  literal(item, "environment", "TEST", "policy");
  oneOf(
    item,
    "state",
    ["ENABLED", "MANUAL_ONLY", "UNDER_REVIEW", "DISABLED", "EXPIRED"] as const,
    "policy",
  );
  utc(text(item, "effectiveFromUtc", "policy"), "policy.effectiveFromUtc");
  literal(
    item,
    "effectiveTimestampBasis",
    "DETERMINISTIC_FIXTURE_CLOCK_NOT_RUNTIME_AUTHORIZATION",
    "policy",
  );
  utc(text(item, "expiresAtUtc", "policy"), "policy.expiresAtUtc");
  literal(
    item,
    "fixtureControlBasis",
    "PROMPT5_TEST_CONTROLS_NOT_RATIFIED_RUNTIME_TARGETS",
    "policy",
  );
  text(item, "ownerRole", "policy");
  parseReview(item.documentation, "policy.documentation");
  parseReview(item.terms, "policy.terms");
  for (const key of [
    "allowedOperations",
    "prohibitedOperations",
    "allowedApiHosts",
    "allowedPublicHosts",
    "attributionRequirements",
    "dataFieldsCollected",
    "identityFields",
  ])
    strings(item, key, "policy");
  strings(item, "allowedNetworkMethods", "policy", true);
  text(item, "detailPathTemplate", "policy");
  literal(
    item,
    "authenticationRequirement",
    "NONE_FOR_DOCUMENTED_GET_RUNTIME_STILL_DISABLED",
    "policy",
  );
  literal(item, "credentialsAllowed", false, "policy");
  literal(item, "cookiesAllowed", false, "policy");
  literal(item, "redirectsAllowed", false, "policy");
  text(item, "providerRateLimit", "policy");
  literal(item, "runtimeRequestBudget", 0, "policy");
  literal(item, "runtimeCacheTtlSeconds", 0, "policy");
  text(item, "fixtureRetention", "policy");
  literal(
    item,
    "canonicalPostingIdentityMethod",
    "PROVIDER_BOARD_EXTERNAL_ID_AND_CANONICAL_URL",
    "policy",
  );
  integer(item, "savedLivenessMaxAgeSeconds", "policy", 1);
  literal(item, "livenessMethod", "SAVED_PUBLIC_DETAIL_GET", "policy");
  text(item, "changeMonitoringOwner", "policy");
  literal(item, "networkKillSwitch", true, "policy");
  literal(item, "runtimeEnablementApproved", false, "policy");
  text(item, "approvedFixtureId", "policy");
  text(item, "approvedFactsSnapshotId", "policy");
  for (const key of [
    "approvedRawBodySha256",
    "approvedSavedPostingSha256",
    "approvedFactsSnapshotSha256",
    "approvedCommandSha256",
  ])
    sha256(text(item, key, "policy"), `policy.${key}`);
  const headerHashes = strings(item, "approvedResponseHeadersSha256", "policy");
  if (headerHashes.length !== 2)
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      "policy requires two approved header hashes",
    );
  headerHashes.forEach((hash, index) =>
    sha256(hash, `policy.approvedResponseHeadersSha256[${index}]`),
  );
  return freezeValidated<SourcePolicy>(item);
}

function parseObservation(value: unknown, label: string): void {
  const item = record(value, label);
  exact(
    item,
    [
      "evidenceId",
      "phase",
      "observedAtUtc",
      "observedStatus",
      "currentStatus",
      "method",
      "httpStatus",
      "contentType",
      "contentLength",
      "etag",
      "requestId",
      "responseHeadersSha256",
      "rawBodySha256",
      "requestUrl",
      "finalUrl",
      "authentication",
      "credentialsSent",
      "cookiesSent",
      "redirectCount",
    ],
    label,
  );
  text(item, "evidenceId", label);
  oneOf(item, "phase", ["INTAKE", "PRE_READY"] as const, label);
  utc(text(item, "observedAtUtc", label), `${label}.observedAtUtc`);
  literal(item, "observedStatus", "LIVE_AT_CAPTURE", label);
  literal(item, "currentStatus", "NOT_CHECKED", label);
  literal(item, "method", "SAVED_PUBLIC_DETAIL_GET", label);
  literal(item, "httpStatus", 200, label);
  literal(item, "contentType", "application/json", label);
  integer(item, "contentLength", label, 1);
  text(item, "etag", label);
  text(item, "requestId", label);
  sha256(text(item, "responseHeadersSha256", label), `${label}.responseHeadersSha256`);
  sha256(text(item, "rawBodySha256", label), `${label}.rawBodySha256`);
  text(item, "requestUrl", label);
  text(item, "finalUrl", label);
  literal(item, "authentication", "NONE", label);
  literal(item, "credentialsSent", false, label);
  literal(item, "cookiesSent", false, label);
  literal(item, "redirectCount", 0, label);
}

function parsePointerBasis(value: unknown, label: string): void {
  const item = record(value, label);
  exact(item, ["jsonPointer", "representation", "valueBytes", "valueSha256"], label);
  oneOf(item, "jsonPointer", ["/content", "/location/name"] as const, label);
  literal(item, "representation", "RFC8259_DECODED_SCALAR_UTF8", label);
  integer(item, "valueBytes", label, 1);
  sha256(text(item, "valueSha256", label), `${label}.valueSha256`);
}

function parseSourceEvidence(value: unknown, label: string): void {
  const item = record(value, label);
  exact(
    item,
    [
      "evidenceId",
      "jsonPointer",
      "startByte",
      "endByteExclusive",
      "fragmentByteLength",
      "fragmentSha256",
    ],
    label,
  );
  text(item, "evidenceId", label);
  oneOf(item, "jsonPointer", ["/content", "/location/name"] as const, label);
  const start = integer(item, "startByte", label);
  const end = integer(item, "endByteExclusive", label, 1);
  const length = integer(item, "fragmentByteLength", label, 1);
  if (end <= start || end - start !== length) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label} has an invalid byte span`);
  }
  sha256(text(item, "fragmentSha256", label), `${label}.fragmentSha256`);
}

function parseRequirement(value: unknown, label: string): void {
  const item = record(value, label);
  exact(
    item,
    [
      "requirementId",
      "label",
      "gate",
      "materiality",
      "factKey",
      "operator",
      "expected",
      "extractionConfidence",
      "sourceEvidenceRefs",
      "derivation",
    ],
    label,
  );
  text(item, "requirementId", label);
  text(item, "label", label);
  oneOf(item, "gate", ["ELIGIBILITY", "FIT"] as const, label);
  oneOf(item, "materiality", ["REQUIRED", "PREFERRED"] as const, label);
  text(item, "factKey", label);
  const operator = oneOf(
    item,
    "operator",
    ["EQUALS", "AT_LEAST", "INCLUDES_ALL", "INCLUDES_ANY"] as const,
    label,
  );
  const expected = factValue(item, "expected", label);
  if (
    (operator === "EQUALS" && Array.isArray(expected)) ||
    (operator === "AT_LEAST" && typeof expected !== "number") ||
    ((operator === "INCLUDES_ALL" || operator === "INCLUDES_ANY") && !Array.isArray(expected))
  ) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label}.operator is incompatible with expected`,
    );
  }
  oneOf(item, "extractionConfidence", ["HIGH", "MEDIUM", "LOW"] as const, label);
  const refs = strings(item, "sourceEvidenceRefs", label);
  unique(refs, `${label}.sourceEvidenceRefs`);
  literal(item, "derivation", "HUMAN_REVIEWED_PARAPHRASE", label);
}

function parseSavedPosting(value: unknown, label: string): void {
  const item = record(value, label);
  exact(
    item,
    [
      "id",
      "internalJobId",
      "title",
      "companyName",
      "locationName",
      "firstPublished",
      "updatedAt",
      "applicationDeadline",
      "anticipatedClosingDate",
      "language",
      "canonicalPostingUrl",
      "evidenceBasis",
      "sourceEvidence",
      "requirements",
      "untrustedContentMarker",
    ],
    label,
  );
  integer(item, "id", label, 1);
  integer(item, "internalJobId", label, 1);
  for (const key of [
    "title",
    "companyName",
    "locationName",
    "language",
    "canonicalPostingUrl",
    "untrustedContentMarker",
  ])
    text(item, key, label);
  iso(text(item, "firstPublished", label), `${label}.firstPublished`);
  iso(text(item, "updatedAt", label), `${label}.updatedAt`);
  if (item.applicationDeadline !== null)
    iso(text(item, "applicationDeadline", label), `${label}.applicationDeadline`);

  const closing = record(item.anticipatedClosingDate, `${label}.anticipatedClosingDate`);
  exact(
    closing,
    ["humanReviewedDate", "structuredApiValue", "status", "sourceEvidenceRefs"],
    `${label}.anticipatedClosingDate`,
  );
  if (
    !/^\d{4}-\d{2}-\d{2}$/.test(
      text(closing, "humanReviewedDate", `${label}.anticipatedClosingDate`),
    )
  ) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      "anticipated closing date must be YYYY-MM-DD",
    );
  }
  literal(closing, "structuredApiValue", null, `${label}.anticipatedClosingDate`);
  literal(
    closing,
    "status",
    "UNSTRUCTURED_DATE_PRESERVED_SEPARATELY",
    `${label}.anticipatedClosingDate`,
  );
  const closingRefs = strings(closing, "sourceEvidenceRefs", `${label}.anticipatedClosingDate`);

  const basis = record(item.evidenceBasis, `${label}.evidenceBasis`);
  exact(
    basis,
    [
      "captureSha256",
      "pointers",
      "reviewedByRef",
      "reviewedAtUtc",
      "reviewedScope",
      "rawContentRetainedInRepository",
    ],
    `${label}.evidenceBasis`,
  );
  sha256(
    text(basis, "captureSha256", `${label}.evidenceBasis`),
    `${label}.evidenceBasis.captureSha256`,
  );
  const pointers = array(basis, "pointers", `${label}.evidenceBasis`);
  pointers.forEach((pointer, index) =>
    parsePointerBasis(pointer, `${label}.evidenceBasis.pointers[${index}]`),
  );
  const pointerRecords = pointers as JsonRecord[];
  if (pointerRecords.length !== 2)
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label}.evidenceBasis requires two pointers`,
    );
  unique(
    pointerRecords.map((pointer) => String(pointer.jsonPointer)),
    `${label}.evidenceBasis.jsonPointer`,
  );
  text(basis, "reviewedByRef", `${label}.evidenceBasis`);
  utc(
    text(basis, "reviewedAtUtc", `${label}.evidenceBasis`),
    `${label}.evidenceBasis.reviewedAtUtc`,
  );
  const scopes = strings(basis, "reviewedScope", `${label}.evidenceBasis`);
  unique(scopes, `${label}.evidenceBasis.reviewedScope`);
  if (
    !scopes.every((scope) =>
      [
        "ROLE_LOCATION",
        "WORK_AUTHORIZATION",
        "QUALIFICATIONS",
        "ANTICIPATED_CLOSING_DATE",
      ].includes(scope),
    )
  ) {
    throw new Stage1ValidationError("VALIDATION_ERROR", `${label}.reviewedScope is invalid`);
  }
  literal(basis, "rawContentRetainedInRepository", false, `${label}.evidenceBasis`);

  const evidence = array(item, "sourceEvidence", label);
  evidence.forEach((entry, index) =>
    parseSourceEvidence(entry, `${label}.sourceEvidence[${index}]`),
  );
  const evidenceRecords = evidence as JsonRecord[];
  const evidenceIds = evidenceRecords.map((entry) => String(entry.evidenceId));
  unique(evidenceIds, `${label}.sourceEvidence.evidenceId`);
  const pointerMap = new Map(
    pointerRecords.map((pointer) => [String(pointer.jsonPointer), pointer]),
  );
  evidenceRecords.forEach((entry, index) => {
    const pointer = pointerMap.get(String(entry.jsonPointer));
    if (pointer === undefined || Number(entry.endByteExclusive) > Number(pointer.valueBytes)) {
      throw new Stage1ValidationError(
        "VALIDATION_ERROR",
        `${label}.sourceEvidence[${index}] is outside its pointer value`,
      );
    }
  });

  const requirements = array(item, "requirements", label);
  requirements.forEach((requirement, index) =>
    parseRequirement(requirement, `${label}.requirements[${index}]`),
  );
  const requirementRecords = requirements as JsonRecord[];
  unique(
    requirementRecords.map((requirement) => String(requirement.requirementId)),
    `${label}.requirements.requirementId`,
  );
  const availableEvidence = new Set(evidenceIds);
  const usedEvidence = [
    ...closingRefs,
    ...requirementRecords.flatMap((requirement) => requirement.sourceEvidenceRefs as string[]),
  ];
  if (!usedEvidence.every((reference) => availableEvidence.has(reference))) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      `${label} has an unresolved source-evidence reference`,
    );
  }
}

export function parseSavedPostingFixture(value: unknown): SavedPostingFixture {
  const item = record(value, "fixture");
  exact(
    item,
    [
      "schemaVersion",
      "fixtureId",
      "classification",
      "fixtureTransform",
      "source",
      "capture",
      "observations",
      "savedPosting",
      "savedPostingSha256",
      "parserVersion",
    ],
    "fixture",
  );
  literal(item, "schemaVersion", "ajas.saved-greenhouse-fixture.v1", "fixture");
  text(item, "fixtureId", "fixture");
  literal(item, "classification", "PUBLIC_JOB_POSTING_SNAPSHOT", "fixture");
  literal(item, "fixtureTransform", "MINIMIZED_HUMAN_REVIEWED_DERIVATIVE", "fixture");

  const source = record(item.source, "fixture.source");
  exact(
    source,
    [
      "provider",
      "boardToken",
      "sourceKey",
      "externalPostingId",
      "requestMethod",
      "requestUrl",
      "canonicalPostingUrl",
      "documentationUrl",
    ],
    "fixture.source",
  );
  literal(source, "provider", "GREENHOUSE", "fixture.source");
  for (const key of [
    "boardToken",
    "sourceKey",
    "externalPostingId",
    "requestUrl",
    "canonicalPostingUrl",
    "documentationUrl",
  ])
    text(source, key, "fixture.source");
  literal(source, "requestMethod", "GET", "fixture.source");

  const capture = record(item.capture, "fixture.capture");
  exact(
    capture,
    [
      "actor",
      "tool",
      "toolVersion",
      "commandEvidenceRef",
      "rawBodyAvailableInRepository",
      "responseHeadersAvailableInRepository",
      "rawBodySha256",
      "rawBodyBytes",
      "minimizationReason",
    ],
    "fixture.capture",
  );
  literal(capture, "actor", "AJAS_FIXTURE_AUTHOR", "fixture.capture");
  literal(capture, "tool", "curl", "fixture.capture");
  literal(capture, "toolVersion", "8.5.0", "fixture.capture");
  text(capture, "commandEvidenceRef", "fixture.capture");
  literal(capture, "rawBodyAvailableInRepository", false, "fixture.capture");
  literal(capture, "responseHeadersAvailableInRepository", false, "fixture.capture");
  sha256(text(capture, "rawBodySha256", "fixture.capture"), "fixture.capture.rawBodySha256");
  integer(capture, "rawBodyBytes", "fixture.capture", 1);
  text(capture, "minimizationReason", "fixture.capture");

  const observations = array(item, "observations", "fixture");
  if (observations.length !== 2)
    throw new Stage1ValidationError("VALIDATION_ERROR", "fixture requires two observations");
  observations.forEach((observation, index) =>
    parseObservation(observation, `fixture.observations[${index}]`),
  );
  parseSavedPosting(item.savedPosting, "fixture.savedPosting");
  sha256(text(item, "savedPostingSha256", "fixture"), "fixture.savedPostingSha256");
  text(item, "parserVersion", "fixture");
  return freezeValidated<SavedPostingFixture>(item);
}

export function parseStage1FixtureCommand(value: unknown): Stage1FixtureCommand {
  const item = record(value, "command");
  exact(
    item,
    [
      "schemaVersion",
      "executionMode",
      "environment",
      "evaluatedAtUtc",
      "userId",
      "subjectId",
      "actorId",
      "actorVersion",
      "applicationId",
      "runId",
      "correlationId",
      "idempotencyKey",
      "factsSnapshotId",
      "factsSnapshotVersion",
      "factsSnapshotSha256",
      "postingFixtureId",
      "sourcePolicyId",
      "sourcePolicyVersion",
      "authorizationRef",
      "selectionAuthorizationRef",
    ],
    "command",
  );
  literal(item, "schemaVersion", "ajas.stage1-fixture-command.v1", "command");
  literal(item, "executionMode", STAGE1_EXECUTION_MODE, "command");
  literal(item, "environment", "TEST_FIXTURE", "command");
  utc(text(item, "evaluatedAtUtc", "command"), "command.evaluatedAtUtc");
  for (const key of [
    "userId",
    "subjectId",
    "actorId",
    "actorVersion",
    "applicationId",
    "runId",
    "correlationId",
    "idempotencyKey",
    "factsSnapshotId",
    "postingFixtureId",
    "sourcePolicyId",
    "authorizationRef",
    "selectionAuthorizationRef",
  ])
    text(item, key, "command");
  integer(item, "factsSnapshotVersion", "command", 1);
  sha256(text(item, "factsSnapshotSha256", "command"), "command.factsSnapshotSha256");
  integer(item, "sourcePolicyVersion", "command", 1);
  return freezeValidated<Stage1FixtureCommand>(item);
}
