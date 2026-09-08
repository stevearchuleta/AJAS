export {
  AUTONOMOUS_TERMINAL_STATE,
  PROHIBITED_EMPLOYER_ACTIONS,
  isProhibitedEmployerAction,
  type ProhibitedEmployerAction,
} from "./human-boundary.js";

export { validateApprovedFacts } from "./stage1/approved-facts.js";
export { canonicalJson, sha256Hex, stablePrettyJson } from "./stage1/canonical-json.js";
export {
  SAVED_FIXTURE_OPERATION,
  STAGE1_EXECUTION_MODE,
  STAGE1_READINESS_SCOPE,
  Stage1ValidationError,
  parseApprovedFactsSnapshot,
  parseSavedPostingFixture,
  parseSourcePolicy,
  parseStage1FixtureCommand,
  type ApprovedFact,
  type ApprovedFactsSnapshot,
  type AuditCommitReceipt,
  type AuditEvent,
  type EvidencePointerBasis,
  type FactUse,
  type FactValue,
  type FitRequirementResult,
  type LivenessDecision,
  type PacketArtifactMetadata,
  type PacketMetadata,
  type PostingRequirement,
  type RequirementOperator,
  type SavedCaptureObservation,
  type SavedPostingFixture,
  type ScreeningResult,
  type SliceState,
  type SourcePolicy,
  type SourcePolicyDecision,
  type SourcePolicyState,
  type SourceFragmentEvidence,
  type Stage1FixtureCommand,
  type Stage1VerticalSliceInput,
  type Stage1VerticalSliceResult,
} from "./stage1/contracts.js";
export { evaluateEligibilityAndFit } from "./stage1/screening.js";
export {
  assertNetworkOperationDenied,
  validateSavedLiveness,
  validateSourcePolicy,
} from "./stage1/source-policy.js";
export { assertSliceTransition, buildSliceStateHistory } from "./stage1/state-machine.js";
export {
  InMemoryAuditSink,
  InMemoryFixtureArtifactStore,
  InMemoryVerticalSliceRepository,
  Stage1SliceError,
  runStage1VerticalSlice,
  type AuditSink,
  type AuditBatchReceipt,
  type FixtureArtifactStore,
  type InMemoryAuditSinkOptions,
  type IdempotentVerticalSliceResult,
  type VerticalSliceDependencies,
} from "./stage1/vertical-slice.js";

// ============================================================
// EXPOSE THE SHARED AUTH POLICY WITHOUT READING PRIVATE CONFIG.
// AUTH EVENTS REMAIN A NODE-ONLY INTERNAL MODULE FOR NOW.
// ============================================================
export {
  evaluatePersonalAlphaAdmission,
  readPersonalAlphaConfiguration,
  type PersonalAlphaConfiguration,
  type PersonalAlphaDecision,
  type PersonalAlphaDecisionCode,
} from "./auth/personal-alpha-policy.js";
