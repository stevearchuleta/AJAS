import { canonicalJson, sha256Hex } from "./canonical-json.js";
import {
  SAVED_FIXTURE_OPERATION,
  type LivenessDecision,
  type SavedCaptureObservation,
  type SavedPostingFixture,
  type SourcePolicy,
  type SourcePolicyDecision,
  Stage1ValidationError,
  parseSavedPostingFixture,
  parseSourcePolicy,
} from "./contracts.js";

function parseUtc(value: string, label: string): number {
  const parsed = Date.parse(value);

  if (!value.endsWith("Z") || !Number.isFinite(parsed)) {
    throw new Stage1ValidationError("INVALID_UTC_TIMESTAMP", `${label} must be UTC`);
  }

  return parsed;
}

function requireSafeHttpsUrl(value: string, exactHost: string, label: string): URL {
  let parsed: URL;

  try {
    parsed = new URL(value);
  } catch {
    throw new Stage1ValidationError("SOURCE_POLICY_DENIED", `${label} is not a valid URL`);
  }

  if (
    parsed.protocol !== "https:" ||
    parsed.hostname !== exactHost ||
    parsed.username !== "" ||
    parsed.password !== "" ||
    parsed.hash !== ""
  ) {
    throw new Stage1ValidationError("SOURCE_POLICY_DENIED", `${label} is outside policy`);
  }

  return parsed;
}

function validateObservation(
  observation: SavedCaptureObservation,
  fixture: SavedPostingFixture,
  policy: SourcePolicy,
  evaluationTime: number,
  policyEvidenceFloor: number,
): LivenessDecision["evidence"][number] {
  const observedTime = parseUtc(observation.observedAtUtc, `${observation.phase}.observedAtUtc`);
  const ageSeconds = (evaluationTime - observedTime) / 1000;

  if (ageSeconds < 0) {
    throw new Stage1ValidationError("LIVENESS_EVIDENCE_IN_FUTURE", "liveness is future-dated");
  }

  if (observedTime < policyEvidenceFloor) {
    throw new Stage1ValidationError(
      "LIVENESS_EVIDENCE_BEFORE_POLICY",
      "saved liveness evidence predates the fixture policy review window",
    );
  }

  if (ageSeconds > policy.savedLivenessMaxAgeSeconds) {
    throw new Stage1ValidationError("LIVENESS_EVIDENCE_STALE", "saved liveness evidence is stale");
  }

  if (
    observation.observedStatus !== "LIVE_AT_CAPTURE" ||
    observation.currentStatus !== "NOT_CHECKED" ||
    observation.method !== policy.livenessMethod ||
    observation.httpStatus !== 200 ||
    observation.contentType !== "application/json" ||
    observation.contentLength !== fixture.capture.rawBodyBytes ||
    !observation.etag ||
    !observation.requestId ||
    !/^[a-f0-9]{64}$/.test(observation.responseHeadersSha256) ||
    observation.rawBodySha256 !== fixture.capture.rawBodySha256 ||
    observation.authentication !== "NONE" ||
    observation.credentialsSent ||
    observation.cookiesSent ||
    observation.redirectCount !== 0 ||
    observation.requestUrl !== fixture.source.requestUrl ||
    observation.finalUrl !== fixture.source.requestUrl
  ) {
    throw new Stage1ValidationError(
      "LIVENESS_EVIDENCE_INVALID",
      `saved liveness evidence ${observation.evidenceId} is invalid`,
    );
  }

  return {
    evidenceId: observation.evidenceId,
    phase: observation.phase,
    observedStatus: observation.observedStatus,
    observedAtUtc: observation.observedAtUtc,
    ageSecondsAtEvaluation: ageSeconds,
    rawBodySha256: observation.rawBodySha256,
  };
}

export function validateSourcePolicy(
  policy: SourcePolicy,
  fixture: SavedPostingFixture,
  evaluatedAtUtc: string,
): SourcePolicyDecision {
  policy = parseSourcePolicy(policy);
  fixture = parseSavedPostingFixture(fixture);
  const evaluationTime = parseUtc(evaluatedAtUtc, "evaluatedAtUtc");
  const effectiveFrom = parseUtc(policy.effectiveFromUtc, "policy.effectiveFromUtc");
  const expiresAt = parseUtc(policy.expiresAtUtc, "policy.expiresAtUtc");
  const documentationReviewedAt = parseUtc(
    policy.documentation.reviewedAtUtc,
    "policy.documentation.reviewedAtUtc",
  );
  const termsReviewedAt = parseUtc(policy.terms.reviewedAtUtc, "policy.terms.reviewedAtUtc");

  if (
    evaluationTime < effectiveFrom ||
    evaluationTime >= expiresAt ||
    documentationReviewedAt > evaluationTime ||
    termsReviewedAt > evaluationTime
  ) {
    throw new Stage1ValidationError("SOURCE_POLICY_EXPIRED", "source policy is not effective");
  }

  if (
    policy.schemaVersion !== "ajas.source-policy.v1" ||
    policy.environment !== "TEST" ||
    policy.sourceType !== "PUBLIC_ATS_JOB_BOARD" ||
    !policy.policyId ||
    policy.policyVersion < 1 ||
    policy.state !== "MANUAL_ONLY" ||
    policy.effectiveTimestampBasis !== "DETERMINISTIC_FIXTURE_CLOCK_NOT_RUNTIME_AUTHORIZATION" ||
    policy.fixtureControlBasis !== "PROMPT5_TEST_CONTROLS_NOT_RATIFIED_RUNTIME_TARGETS" ||
    policy.allowedOperations.length !== 1 ||
    policy.allowedOperations[0] !== SAVED_FIXTURE_OPERATION ||
    !policy.allowedOperations.includes(SAVED_FIXTURE_OPERATION) ||
    policy.allowedNetworkMethods.length !== 0 ||
    policy.authenticationRequirement !== "NONE_FOR_DOCUMENTED_GET_RUNTIME_STILL_DISABLED" ||
    policy.runtimeRequestBudget !== 0 ||
    !policy.networkKillSwitch ||
    policy.runtimeEnablementApproved ||
    policy.credentialsAllowed ||
    policy.cookiesAllowed ||
    policy.redirectsAllowed
  ) {
    throw new Stage1ValidationError(
      "SOURCE_POLICY_DENIED",
      "policy does not enforce offline fixture-only processing",
    );
  }

  const requiredProhibitions = [
    "NETWORK_GET",
    "NETWORK_HEAD",
    "POST_APPLICATION",
    "LOGIN",
    "AUTHENTICATED_SESSION",
    "FORM_INTERACTION",
    "UPLOAD",
    "CONTACT_EMPLOYER",
    "SUBMIT",
  ];
  const requiredAttribution = [
    "provider",
    "employer",
    "title",
    "canonical_url",
    "capture_time",
    "raw_body_sha256",
  ];
  const requiredDataFields = [
    "external_posting_id",
    "internal_job_id",
    "title",
    "employer",
    "location",
    "published_at",
    "updated_at",
    "canonical_url",
    "material_requirements",
    "response_integrity_metadata",
  ];
  const requiredIdentityFields = [
    "provider",
    "board_token",
    "external_posting_id",
    "canonical_url",
  ];

  if (
    policy.allowedApiHosts.length !== 1 ||
    policy.allowedApiHosts[0] !== "boards-api.greenhouse.io" ||
    policy.allowedPublicHosts.length !== 1 ||
    policy.allowedPublicHosts[0] !== "job-boards.greenhouse.io" ||
    policy.detailPathTemplate !== "/v1/boards/greenhouse/jobs/{numeric_id}" ||
    !requiredProhibitions.every((operation) => policy.prohibitedOperations.includes(operation)) ||
    policy.attributionRequirements.length !== requiredAttribution.length ||
    !requiredAttribution.every((field) => policy.attributionRequirements.includes(field)) ||
    policy.dataFieldsCollected.length !== requiredDataFields.length ||
    !requiredDataFields.every((field) => policy.dataFieldsCollected.includes(field)) ||
    policy.identityFields.length !== requiredIdentityFields.length ||
    !requiredIdentityFields.every((field) => policy.identityFields.includes(field)) ||
    policy.canonicalPostingIdentityMethod !== "PROVIDER_BOARD_EXTERNAL_ID_AND_CANONICAL_URL" ||
    !policy.providerRateLimit ||
    !policy.fixtureRetention ||
    !policy.changeMonitoringOwner
  ) {
    throw new Stage1ValidationError(
      "SOURCE_POLICY_INCOMPLETE",
      "source policy restrictions or governance metadata are incomplete",
    );
  }

  if (
    policy.provider !== fixture.source.provider ||
    policy.boardToken !== fixture.source.boardToken ||
    policy.sourceKey !== fixture.source.sourceKey ||
    policy.sourceKey !== `${policy.provider}:${policy.boardToken}`
  ) {
    throw new Stage1ValidationError(
      "SOURCE_POLICY_DENIED",
      "fixture does not match the exact board policy",
    );
  }

  if (
    policy.approvedFixtureId !== fixture.fixtureId ||
    policy.approvedRawBodySha256 !== fixture.capture.rawBodySha256 ||
    policy.approvedSavedPostingSha256 !== fixture.savedPostingSha256 ||
    fixture.savedPosting.evidenceBasis.captureSha256 !== fixture.capture.rawBodySha256 ||
    policy.approvedResponseHeadersSha256[0] !== fixture.observations[0]?.responseHeadersSha256 ||
    policy.approvedResponseHeadersSha256[1] !== fixture.observations[1]?.responseHeadersSha256
  ) {
    throw new Stage1ValidationError(
      "FIXTURE_TRUST_ANCHOR_MISMATCH",
      "fixture content is not pinned by the approved source policy",
    );
  }

  const requestUrl = requireSafeHttpsUrl(
    fixture.source.requestUrl,
    "boards-api.greenhouse.io",
    "fixture request URL",
  );
  const canonicalUrl = requireSafeHttpsUrl(
    fixture.source.canonicalPostingUrl,
    "job-boards.greenhouse.io",
    "canonical posting URL",
  );
  const expectedApiPath = `/v1/boards/${policy.boardToken}/jobs/${fixture.source.externalPostingId}`;
  const expectedPublicPath = `/${policy.boardToken}/jobs/${fixture.source.externalPostingId}`;

  if (
    fixture.schemaVersion !== "ajas.saved-greenhouse-fixture.v1" ||
    fixture.classification !== "PUBLIC_JOB_POSTING_SNAPSHOT" ||
    fixture.fixtureTransform !== "MINIMIZED_HUMAN_REVIEWED_DERIVATIVE" ||
    !fixture.fixtureId ||
    !fixture.parserVersion ||
    fixture.source.requestMethod !== "GET" ||
    fixture.capture.rawBodyAvailableInRepository ||
    !/^[a-f0-9]{64}$/.test(fixture.capture.rawBodySha256) ||
    fixture.capture.rawBodyBytes <= 0 ||
    requestUrl.pathname !== expectedApiPath ||
    requestUrl.search !== "" ||
    canonicalUrl.pathname !== expectedPublicPath ||
    canonicalUrl.searchParams.get("gh_jid") !== fixture.source.externalPostingId ||
    [...canonicalUrl.searchParams.keys()].length !== 1 ||
    fixture.savedPosting.id.toString() !== fixture.source.externalPostingId ||
    fixture.savedPosting.canonicalPostingUrl !== fixture.source.canonicalPostingUrl
  ) {
    throw new Stage1ValidationError("SOURCE_IDENTITY_MISMATCH", "posting identity is inconsistent");
  }

  if (
    !fixture.savedPosting.title ||
    !fixture.savedPosting.companyName ||
    !fixture.savedPosting.locationName ||
    fixture.savedPosting.requirements.length === 0 ||
    !fixture.savedPosting.requirements.every(
      (requirement) =>
        requirement.requirementId.length > 0 &&
        requirement.label.length > 0 &&
        requirement.sourceEvidenceRefs.length > 0 &&
        requirement.derivation === "HUMAN_REVIEWED_PARAPHRASE",
    )
  ) {
    throw new Stage1ValidationError(
      "FIXTURE_CONTENT_INVALID",
      "minimized posting identity or requirements are incomplete",
    );
  }

  if (
    policy.documentation.url !== "https://docs.greenhouse.io/job-board.html" ||
    policy.documentation.url !== fixture.source.documentationUrl ||
    policy.documentation.finding !==
      "Public GET job-board data requires no authentication; this record does not approve runtime access." ||
    policy.terms.url !== "https://www.greenhouse.com/legal" ||
    policy.terms.finding !== "NOT_CONCLUSIVE_FOR_RUNTIME_ENABLEMENT" ||
    !policy.documentation.reviewedAtUtc ||
    !policy.terms.url ||
    !policy.terms.reviewedAtUtc ||
    !policy.ownerRole ||
    policy.savedLivenessMaxAgeSeconds <= 0
  ) {
    throw new Stage1ValidationError(
      "SOURCE_POLICY_INCOMPLETE",
      "source policy review metadata is incomplete",
    );
  }

  if (
    sha256Hex(canonicalJson(fixture.savedPosting)) !== fixture.savedPostingSha256 ||
    fixture.savedPostingSha256 !== policy.approvedSavedPostingSha256
  ) {
    throw new Stage1ValidationError("FIXTURE_HASH_MISMATCH", "minimized fixture hash mismatch");
  }

  return {
    decision: "ALLOW_FIXTURE_PROCESSING",
    operation: SAVED_FIXTURE_OPERATION,
    policyId: policy.policyId,
    policyVersion: policy.policyVersion,
    sourceKey: policy.sourceKey,
    networkAuthorized: false,
    reason: "EXACT_BOARD_POLICY_ALLOWS_OFFLINE_FIXTURE_ONLY",
  };
}

export function validateSavedLiveness(
  policy: SourcePolicy,
  fixture: SavedPostingFixture,
  evaluatedAtUtc: string,
): LivenessDecision {
  policy = parseSourcePolicy(policy);
  fixture = parseSavedPostingFixture(fixture);
  const evaluationTime = parseUtc(evaluatedAtUtc, "evaluatedAtUtc");
  const phases = new Set(fixture.observations.map((observation) => observation.phase));

  if (fixture.observations.length !== 2 || !phases.has("INTAKE") || !phases.has("PRE_READY")) {
    throw new Stage1ValidationError(
      "LIVENESS_EVIDENCE_INCOMPLETE",
      "both intake and pre-ready liveness evidence are required",
    );
  }

  const policyEvidenceFloor = Math.max(
    parseUtc(policy.effectiveFromUtc, "policy.effectiveFromUtc"),
    parseUtc(policy.documentation.reviewedAtUtc, "policy.documentation.reviewedAtUtc"),
    parseUtc(policy.terms.reviewedAtUtc, "policy.terms.reviewedAtUtc"),
  );
  const evidence = fixture.observations.map((observation) =>
    validateObservation(observation, fixture, policy, evaluationTime, policyEvidenceFloor),
  );

  if (evidence[0]?.phase !== "INTAKE" || evidence[1]?.phase !== "PRE_READY") {
    throw new Stage1ValidationError(
      "LIVENESS_EVIDENCE_ORDER_INVALID",
      "liveness evidence must be ordered intake then pre-ready",
    );
  }

  if (
    Date.parse(evidence[1].observedAtUtc) <= Date.parse(evidence[0].observedAtUtc) ||
    fixture.observations[0]?.evidenceId === fixture.observations[1]?.evidenceId ||
    fixture.observations[0]?.requestId === fixture.observations[1]?.requestId ||
    fixture.observations[0]?.responseHeadersSha256 ===
      fixture.observations[1]?.responseHeadersSha256
  ) {
    throw new Stage1ValidationError(
      "LIVENESS_EVIDENCE_ORDER_INVALID",
      "pre-ready evidence cannot precede intake evidence",
    );
  }

  return {
    decision: "VALID_SAVED_EVIDENCE",
    currentStatus: "NOT_CHECKED",
    evidence,
  };
}

export function assertNetworkOperationDenied(policy: SourcePolicy, operation: string): never {
  throw new Stage1ValidationError(
    "SOURCE_POLICY_DENIED",
    `network operation ${operation} is denied by ${policy.state} fixture policy`,
  );
}
