import { Buffer } from "node:buffer";

import { canonicalJson, sha256Hex } from "./canonical-json.js";
import {
  STAGE1_EXECUTION_MODE,
  STAGE1_READINESS_SCOPE,
  type AuditCommitReceipt,
  type AuditEvent,
  type LivenessDecision,
  type PacketArtifactMetadata,
  type PacketMetadata,
  type ScreeningResult,
  type SliceState,
  type Stage1VerticalSliceInput,
  type Stage1VerticalSliceResult,
  Stage1ValidationError,
  parseApprovedFactsSnapshot,
  parseSavedPostingFixture,
  parseSourcePolicy,
  parseStage1FixtureCommand,
} from "./contracts.js";
import { evaluateEligibilityAndFit } from "./screening.js";
import { validateSavedLiveness, validateSourcePolicy } from "./source-policy.js";
import { assertSliceTransition, buildSliceStateHistory } from "./state-machine.js";

const RULES_VERSION = "ajas-rules.v1.1.0";
const VALIDATOR_VERSION = "ajas-validator.v1.1.0";
const TEMPLATE_VERSION = "ajas-fixture-packet.v1.1.0";

interface ArtifactWrite {
  readonly artifactId: string;
  readonly bytes: Uint8Array;
  readonly expectedSha256: string;
}

interface PreparedArtifact {
  readonly metadata: PacketArtifactMetadata;
  readonly write: ArtifactWrite;
}

interface PreparedPacket {
  readonly metadata: PacketMetadata;
  readonly writes: readonly ArtifactWrite[];
}

interface ContentHashes {
  readonly inputSha256: string;
  readonly commandSha256: string;
  readonly factsSha256: string;
  readonly policySha256: string;
  readonly fixtureSha256: string;
  readonly bindingSha256: string;
}

type AuditEventBody = Omit<AuditEvent, "eventId">;

function deepFreeze<T>(value: T, seen = new Set<object>()): T {
  if (typeof value !== "object" || value === null || Object.isFrozen(value)) {
    return value;
  }

  const objectValue = value as object;

  if (seen.has(objectValue)) {
    return value;
  }

  seen.add(objectValue);

  for (const nestedValue of Object.values(value as Record<string, unknown>)) {
    deepFreeze(nestedValue, seen);
  }

  return Object.freeze(value);
}

function immutableCopy<T>(value: T): T {
  return deepFreeze(structuredClone(value));
}

function parseVerticalSliceInput(value: unknown): Stage1VerticalSliceInput {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Stage1ValidationError("VALIDATION_ERROR", "vertical-slice input must be an object");
  }

  const candidate = value as Record<string, unknown>;
  const expectedKeys = new Set(["command", "facts", "policy", "fixture"]);
  const actualKeys = Object.keys(candidate);

  if (actualKeys.length !== expectedKeys.size || actualKeys.some((key) => !expectedKeys.has(key))) {
    throw new Stage1ValidationError(
      "VALIDATION_ERROR",
      "vertical-slice input must contain exactly command, facts, policy, and fixture",
    );
  }

  return immutableCopy({
    command: parseStage1FixtureCommand(candidate.command),
    facts: parseApprovedFactsSnapshot(candidate.facts),
    policy: parseSourcePolicy(candidate.policy),
    fixture: parseSavedPostingFixture(candidate.fixture),
  });
}

export interface FixtureArtifactStore {
  create(artifactId: string, bytes: Uint8Array): void;
  read(artifactId: string): Uint8Array;
}

export type AuditBatchReceipt = AuditCommitReceipt;

export interface AuditSink {
  appendBatch(events: readonly AuditEvent[]): AuditBatchReceipt;
}

export interface VerticalSliceDependencies {
  readonly artifactStore?: FixtureArtifactStore;
  readonly auditSink?: AuditSink;
}

export class InMemoryFixtureArtifactStore implements FixtureArtifactStore {
  #artifacts = new Map<string, Uint8Array>();

  public create(artifactId: string, bytes: Uint8Array): void {
    this.createAndVerifyBatch([
      {
        artifactId,
        bytes,
        expectedSha256: sha256Hex(bytes),
      },
    ]);
  }

  public createAndVerifyBatch(writes: readonly ArtifactWrite[]): void {
    if (writes.length === 0) {
      throw new Stage1ValidationError("ARTIFACT_BATCH_EMPTY", "artifact batch must not be empty");
    }

    const nextArtifacts = new Map(this.#artifacts);
    const batchIds = new Set<string>();

    for (const write of writes) {
      if (!write.artifactId || batchIds.has(write.artifactId)) {
        throw new Stage1ValidationError(
          "ARTIFACT_BATCH_DUPLICATE",
          "artifact batch contains a missing or duplicate identity",
        );
      }

      if (nextArtifacts.has(write.artifactId)) {
        throw new Stage1ValidationError(
          "ARTIFACT_ALREADY_EXISTS",
          `artifact ${write.artifactId} already exists`,
        );
      }

      const storedBytes = Uint8Array.from(write.bytes);

      if (sha256Hex(storedBytes) !== write.expectedSha256) {
        throw new Stage1ValidationError(
          "ARTIFACT_WRITE_HASH_MISMATCH",
          `artifact ${write.artifactId} does not match its expected hash`,
        );
      }

      batchIds.add(write.artifactId);
      nextArtifacts.set(write.artifactId, storedBytes);
    }

    for (const write of writes) {
      const readbackBytes = nextArtifacts.get(write.artifactId);

      if (
        readbackBytes === undefined ||
        readbackBytes.byteLength !== write.bytes.byteLength ||
        sha256Hex(readbackBytes) !== write.expectedSha256
      ) {
        throw new Stage1ValidationError(
          "ARTIFACT_READBACK_MISMATCH",
          `artifact ${write.artifactId} failed byte readback`,
        );
      }
    }

    this.#artifacts = nextArtifacts;
  }

  public deleteBatchIfHashesMatch(writes: readonly ArtifactWrite[]): void {
    if (writes.length === 0) {
      return;
    }

    const batchIds = new Set<string>();

    for (const write of writes) {
      const storedBytes = this.#artifacts.get(write.artifactId);

      if (
        batchIds.has(write.artifactId) ||
        storedBytes === undefined ||
        sha256Hex(storedBytes) !== write.expectedSha256
      ) {
        throw new Stage1ValidationError(
          "ARTIFACT_ROLLBACK_HASH_MISMATCH",
          `artifact ${write.artifactId} cannot be removed safely`,
        );
      }

      batchIds.add(write.artifactId);
    }

    const nextArtifacts = new Map(this.#artifacts);

    for (const write of writes) {
      nextArtifacts.delete(write.artifactId);
    }

    this.#artifacts = nextArtifacts;
  }

  public read(artifactId: string): Uint8Array {
    const bytes = this.#artifacts.get(artifactId);

    if (bytes === undefined) {
      throw new Stage1ValidationError("ARTIFACT_NOT_FOUND", `artifact ${artifactId} is missing`);
    }

    return Uint8Array.from(bytes);
  }

  public get size(): number {
    return this.#artifacts.size;
  }
}

export interface InMemoryAuditSinkOptions {
  readonly failBeforeCommit?: boolean;
}

export class InMemoryAuditSink implements AuditSink {
  #events: readonly AuditEvent[] = Object.freeze([]);
  readonly #failBeforeCommit: boolean;

  public constructor(options: InMemoryAuditSinkOptions = {}) {
    this.#failBeforeCommit = options.failBeforeCommit ?? false;
  }

  public appendBatch(events: readonly AuditEvent[]): AuditBatchReceipt {
    if (events.length === 0) {
      throw new Stage1ValidationError("AUDIT_BATCH_EMPTY", "audit batch must not be empty");
    }

    const storedEvents = immutableCopy([...events]);
    const existingEventIds = new Set(this.#events.map((event) => event.eventId));
    const batchEventIds = new Set<string>();

    for (const event of storedEvents) {
      if (
        !event.eventId ||
        existingEventIds.has(event.eventId) ||
        batchEventIds.has(event.eventId)
      ) {
        throw new Stage1ValidationError(
          "AUDIT_EVENT_DUPLICATE",
          "audit batch contains a missing or duplicate event identity",
        );
      }

      batchEventIds.add(event.eventId);
    }

    const batchSha256 = sha256Hex(canonicalJson(storedEvents));

    if (this.#failBeforeCommit) {
      throw new Stage1ValidationError(
        "AUDIT_WRITE_FAILED",
        "audit sink test mode rejected the batch before commit",
      );
    }

    this.#events = immutableCopy([...this.#events, ...storedEvents]);

    return immutableCopy({
      store: "IN_MEMORY_FIXTURE_AUDIT" as const,
      status: "COMMITTED" as const,
      eventCount: storedEvents.length,
      batchSha256,
    });
  }

  public readAll(): readonly AuditEvent[] {
    return immutableCopy(this.#events);
  }

  public get size(): number {
    return this.#events.length;
  }
}

export class Stage1SliceError extends Error {
  public readonly code: string;
  public readonly lastState: SliceState | null;
  public readonly auditEvent: AuditEvent;

  public constructor(
    code: string,
    message: string,
    lastState: SliceState | null,
    auditEvent: AuditEvent,
  ) {
    super(message);
    this.name = "Stage1SliceError";
    this.code = code;
    this.lastState = lastState;
    this.auditEvent = immutableCopy(auditEvent);
  }
}

function hasExactPrototype(value: object, expectedPrototype: object): boolean {
  try {
    return Object.getPrototypeOf(value) === expectedPrototype;
  } catch {
    return false;
  }
}

function resolveDependencies(dependencies: VerticalSliceDependencies): {
  readonly artifactStore: InMemoryFixtureArtifactStore;
  readonly auditSink: InMemoryAuditSink;
} {
  const artifactStore = dependencies.artifactStore ?? new InMemoryFixtureArtifactStore();
  const auditSink = dependencies.auditSink ?? new InMemoryAuditSink();

  if (
    !hasExactPrototype(artifactStore, InMemoryFixtureArtifactStore.prototype) ||
    !hasExactPrototype(auditSink, InMemoryAuditSink.prototype)
  ) {
    throw new Stage1ValidationError(
      "UNSUPPORTED_FIXTURE_ADAPTER",
      "Prompt-5 accepts only the built-in in-memory artifact and audit adapters",
    );
  }

  return {
    artifactStore: artifactStore as InMemoryFixtureArtifactStore,
    auditSink: auditSink as InMemoryAuditSink,
  };
}

function stableId(prefix: string, value: string): string {
  return `${prefix}_${sha256Hex(value).slice(0, 20)}`;
}

function contentHashesFor(input: Stage1VerticalSliceInput): ContentHashes {
  const inputSha256 = sha256Hex(canonicalJson(input));
  const commandSha256 = sha256Hex(canonicalJson(input.command));
  const factsSha256 = sha256Hex(canonicalJson(input.facts));
  const policySha256 = sha256Hex(canonicalJson(input.policy));
  const fixtureSha256 = sha256Hex(canonicalJson(input.fixture));
  const bindingSha256 = sha256Hex(
    canonicalJson({
      factsSha256,
      fixtureSha256,
      inputSha256,
      commandSha256,
      policySha256,
      rulesVersion: RULES_VERSION,
      templateVersion: TEMPLATE_VERSION,
      validatorVersion: VALIDATOR_VERSION,
    }),
  );

  return {
    inputSha256,
    commandSha256,
    factsSha256,
    policySha256,
    fixtureSha256,
    bindingSha256,
  };
}

function prepareArtifact(
  hashes: ContentHashes,
  correlationId: string,
  ordinal: number,
  kind: PacketArtifactMetadata["kind"],
  filename: string,
  payload: unknown,
): PreparedArtifact {
  const serialized = `${canonicalJson(payload)}\n`;
  const bytes = Buffer.from(serialized, "utf8");
  const expectedSha256 = sha256Hex(bytes);
  const artifactId = stableId(
    "artifact",
    canonicalJson({
      bindingSha256: hashes.bindingSha256,
      correlationId,
      expectedSha256,
      filename,
      kind,
      ordinal,
      templateVersion: TEMPLATE_VERSION,
    }),
  );

  return {
    write: {
      artifactId,
      bytes,
      expectedSha256,
    },
    metadata: {
      artifactId,
      kind,
      filename,
      mimeType: "application/json",
      bytes: bytes.byteLength,
      sha256: expectedSha256,
      readbackSha256: expectedSha256,
      readbackStatus: "PASS",
    },
  };
}

function preparePacketMetadata(
  input: Stage1VerticalSliceInput,
  screening: ScreeningResult,
  liveness: LivenessDecision,
  hashes: ContentHashes,
): PreparedPacket {
  const { command, facts, fixture, policy } = input;
  const packetId = stableId(
    "packet",
    canonicalJson({
      applicationId: command.applicationId,
      bindingSha256: hashes.bindingSha256,
      commandSha256: hashes.commandSha256,
      factsVersion: facts.version,
      policyVersion: policy.policyVersion,
      rulesVersion: RULES_VERSION,
      runId: command.runId,
      templateVersion: TEMPLATE_VERSION,
      validatorVersion: VALIDATOR_VERSION,
    }),
  );
  const preparedArtifacts = [
    prepareArtifact(hashes, command.correlationId, 0, "POSTING_SNAPSHOT", "posting-snapshot.json", {
      capture: fixture.capture,
      fixtureId: fixture.fixtureId,
      fixtureSha256: hashes.fixtureSha256,
      observations: fixture.observations,
      savedPosting: fixture.savedPosting,
      savedPostingSha256: fixture.savedPostingSha256,
      source: fixture.source,
    }),
    prepareArtifact(hashes, command.correlationId, 1, "FIT_EXPLANATION", "fit-explanation.json", {
      factsSha256: hashes.factsSha256,
      factsSnapshotId: facts.snapshotId,
      factsSnapshotVersion: facts.version,
      postingFixtureId: fixture.fixtureId,
      screening,
    }),
    prepareArtifact(hashes, command.correlationId, 2, "REVIEW_HANDOFF", "review-handoff.json", {
      applicationId: command.applicationId,
      employerActionsPerformed: [],
      executionMode: command.executionMode,
      inputSha256: hashes.inputSha256,
      officialPostingUrl: fixture.source.canonicalPostingUrl,
      policySha256: hashes.policySha256,
      requiredHumanAction:
        "Review this synthetic fixture output inside AJAS only. Do not open an employer application form, contact the employer, upload files, make an attestation, or submit anything from this test result.",
      state: "READY_FOR_REVIEW",
    }),
  ] as const;

  return {
    writes: preparedArtifacts.map((artifact) => artifact.write),
    metadata: {
      schemaVersion: "ajas.packet-metadata.v1",
      packetId,
      applicationId: command.applicationId,
      subjectId: command.subjectId,
      runId: command.runId,
      inputSha256: hashes.inputSha256,
      commandSha256: hashes.commandSha256,
      executionMode: STAGE1_EXECUTION_MODE,
      readinessScope: STAGE1_READINESS_SCOPE,
      productionReady: false,
      factsSnapshotId: facts.snapshotId,
      factsSnapshotVersion: facts.version,
      factsSnapshotSha256: hashes.factsSha256,
      postingFixtureId: fixture.fixtureId,
      postingExternalId: fixture.source.externalPostingId,
      postingRawBodySha256: fixture.capture.rawBodySha256,
      postingSavedSha256: fixture.savedPostingSha256,
      sourcePolicyId: policy.policyId,
      sourcePolicyVersion: policy.policyVersion,
      sourcePolicySha256: hashes.policySha256,
      parserVersion: fixture.parserVersion,
      rulesVersion: RULES_VERSION,
      validatorVersion: VALIDATOR_VERSION,
      templateVersion: TEMPLATE_VERSION,
      officialPostingUrl: fixture.source.canonicalPostingUrl,
      officialPostingUrlPurpose: "SAVED_FIXTURE_SOURCE_PROVENANCE_ONLY",
      artifactStore: "IN_MEMORY_FIXTURE_STORE",
      authoritativeByteStoreUsed: false,
      artifacts: preparedArtifacts.map((artifact) => artifact.metadata),
      validation: {
        extractionScope: "REVIEWED_MINIMIZED_SCOPE_ONLY",
        completeness: "PASS_FOR_DECLARED_SCOPE",
        byteHashReadback: "PASS",
        finalSavedLiveness: liveness.decision,
        currentLiveness: liveness.currentStatus,
        status: "PASS",
        validatedAtUtc: command.evaluatedAtUtc,
      },
      employerActionsPerformed: [],
      nextAutonomousAction: null,
    },
  };
}

function createAuditEvent(hashes: ContentHashes | undefined, body: AuditEventBody): AuditEvent {
  const eventId = stableId(
    "event",
    canonicalJson({
      bindingSha256: hashes?.bindingSha256 ?? "UNAVAILABLE_BEFORE_VALIDATION",
      body,
      rulesVersion: RULES_VERSION,
      validatorVersion: VALIDATOR_VERSION,
    }),
  );

  return immutableCopy({ eventId, ...body });
}

function transitionAuditEvent(
  input: Stage1VerticalSliceInput,
  hashes: ContentHashes,
  priorState: SliceState | null,
  newState: SliceState,
  evidenceRefs: readonly string[],
): AuditEvent {
  return createAuditEvent(hashes, {
    schemaVersion: "ajas.audit-event.v1",
    timestampUtc: input.command.evaluatedAtUtc,
    userId: input.command.userId,
    subjectId: input.command.subjectId,
    actorId: input.command.actorId,
    actorVersion: input.command.actorVersion,
    action: "APPLICATION_STATE_TRANSITION",
    targetId: input.command.applicationId,
    priorState,
    newState,
    authorizationRef:
      newState === "SELECTED"
        ? input.command.selectionAuthorizationRef
        : input.command.authorizationRef,
    evidenceRefs,
    idempotencyKey: input.command.idempotencyKey,
    outcome: "SUCCESS",
    failureCode: null,
    correlationId: input.command.correlationId,
    environment: "TEST_FIXTURE",
    classification: "SYNTHETIC",
  });
}

function denialAuditEvent(
  input: Stage1VerticalSliceInput,
  hashes: ContentHashes | undefined,
  lastState: SliceState | null,
  code: string,
): AuditEvent {
  const evidenceRefs = [
    input.fixture.fixtureId,
    input.policy.policyId,
    input.facts.snapshotId,
    ...(hashes === undefined
      ? []
      : [
          hashes.inputSha256,
          hashes.commandSha256,
          hashes.factsSha256,
          hashes.policySha256,
          hashes.fixtureSha256,
        ]),
  ];

  return createAuditEvent(hashes, {
    schemaVersion: "ajas.audit-event.v1",
    timestampUtc: input.command.evaluatedAtUtc,
    userId: input.command.userId,
    subjectId: input.command.subjectId,
    actorId: input.command.actorId,
    actorVersion: input.command.actorVersion,
    action: "VERTICAL_SLICE_DENIED",
    targetId: input.command.applicationId,
    priorState: lastState,
    newState: lastState,
    authorizationRef: input.command.authorizationRef,
    evidenceRefs,
    idempotencyKey: input.command.idempotencyKey,
    outcome: "DENIED",
    failureCode: code,
    correlationId: input.command.correlationId,
    environment: "TEST_FIXTURE",
    classification: "SYNTHETIC",
  });
}

function commitAuditBatch(
  auditSink: InMemoryAuditSink,
  events: readonly AuditEvent[],
): AuditBatchReceipt {
  const expectedBatchSha256 = sha256Hex(canonicalJson(events));
  let receipt: AuditBatchReceipt;

  try {
    receipt = auditSink.appendBatch(events);
  } catch {
    throw new Stage1ValidationError("AUDIT_WRITE_FAILED", "audit batch failed before commit");
  }

  if (
    receipt.store !== "IN_MEMORY_FIXTURE_AUDIT" ||
    receipt.status !== "COMMITTED" ||
    receipt.eventCount !== events.length ||
    receipt.batchSha256 !== expectedBatchSha256
  ) {
    throw new Stage1ValidationError(
      "AUDIT_RECEIPT_INVALID",
      "audit sink returned an invalid commit receipt",
    );
  }

  return receipt;
}

function validateCommand(input: Stage1VerticalSliceInput): void {
  const { command } = input;

  if (
    command.executionMode !== STAGE1_EXECUTION_MODE ||
    command.environment !== "TEST_FIXTURE" ||
    !command.userId ||
    !command.subjectId ||
    !command.actorId ||
    !command.actorVersion ||
    !command.applicationId ||
    !command.runId ||
    !command.correlationId ||
    !command.idempotencyKey ||
    !command.factsSnapshotId ||
    command.factsSnapshotVersion < 1 ||
    !command.factsSnapshotSha256 ||
    !command.postingFixtureId ||
    !command.sourcePolicyId ||
    command.sourcePolicyVersion < 1 ||
    !command.authorizationRef ||
    !command.selectionAuthorizationRef
  ) {
    throw new Stage1ValidationError(
      "INVALID_FIXTURE_COMMAND",
      "fixture command identity or authority is incomplete",
    );
  }

  if (
    !command.evaluatedAtUtc.endsWith("Z") ||
    !Number.isFinite(Date.parse(command.evaluatedAtUtc))
  ) {
    throw new Stage1ValidationError("INVALID_UTC_TIMESTAMP", "command evaluation time must be UTC");
  }
}

function validateCommandBindings(input: Stage1VerticalSliceInput, hashes: ContentHashes): void {
  const { command, facts, fixture, policy } = input;

  if (command.subjectId !== facts.subjectId) {
    throw new Stage1ValidationError(
      "COMMAND_SUBJECT_MISMATCH",
      "fixture command subject does not match the approved facts subject",
    );
  }

  if (
    command.factsSnapshotId !== facts.snapshotId ||
    command.factsSnapshotVersion !== facts.version ||
    command.factsSnapshotSha256 !== hashes.factsSha256
  ) {
    throw new Stage1ValidationError(
      "COMMAND_FACTS_BINDING_MISMATCH",
      "fixture command does not match the approved facts snapshot",
    );
  }

  if (command.postingFixtureId !== fixture.fixtureId) {
    throw new Stage1ValidationError(
      "COMMAND_POSTING_BINDING_MISMATCH",
      "fixture command does not match the saved posting fixture",
    );
  }

  if (
    command.sourcePolicyId !== policy.policyId ||
    command.sourcePolicyVersion !== policy.policyVersion
  ) {
    throw new Stage1ValidationError(
      "COMMAND_POLICY_BINDING_MISMATCH",
      "fixture command does not match the exact source policy version",
    );
  }

  if (
    policy.approvedFactsSnapshotId !== facts.snapshotId ||
    policy.approvedFactsSnapshotSha256 !== hashes.factsSha256
  ) {
    throw new Stage1ValidationError(
      "POLICY_FACTS_BINDING_MISMATCH",
      "source policy does not approve the exact applicant facts snapshot",
    );
  }

  if (policy.approvedCommandSha256 !== hashes.commandSha256) {
    throw new Stage1ValidationError(
      "POLICY_COMMAND_BINDING_MISMATCH",
      "source policy does not approve the exact fixture command",
    );
  }
}

export function runStage1VerticalSlice(
  rawInput: Stage1VerticalSliceInput,
  dependencies: VerticalSliceDependencies = {},
): Stage1VerticalSliceResult {
  const input = parseVerticalSliceInput(rawInput);
  const { artifactStore, auditSink } = resolveDependencies(dependencies);
  const completedAuditEvents: AuditEvent[] = [];
  let lastState: SliceState | null = null;
  let hashes: ContentHashes | undefined;
  let committedArtifactWrites: readonly ArtifactWrite[] | null = null;

  const completeState = (newState: SliceState, evidenceRefs: readonly string[]): void => {
    if (hashes === undefined) {
      throw new Stage1ValidationError(
        "CONTENT_BINDING_UNAVAILABLE",
        "content hashes must exist before a state transition",
      );
    }

    assertSliceTransition(lastState, newState);
    completedAuditEvents.push(
      transitionAuditEvent(input, hashes, lastState, newState, evidenceRefs),
    );
    lastState = newState;
  };

  try {
    validateCommand(input);
    hashes = contentHashesFor(input);
    validateCommandBindings(input, hashes);
    const sourcePolicyDecision = validateSourcePolicy(
      input.policy,
      input.fixture,
      input.command.evaluatedAtUtc,
    );
    const livenessDecision = validateSavedLiveness(
      input.policy,
      input.fixture,
      input.command.evaluatedAtUtc,
    );

    completeState("DISCOVERED", [
      input.fixture.fixtureId,
      input.fixture.capture.rawBodySha256,
      hashes.fixtureSha256,
    ]);

    const screening = evaluateEligibilityAndFit(
      input.facts,
      input.fixture,
      input.command.evaluatedAtUtc,
    );

    completeState("SCREENED", [
      input.facts.snapshotId,
      hashes.factsSha256,
      ...screening.requirements.map((row) => row.requirementId),
    ]);

    if (screening.eligibility !== "ELIGIBLE" || screening.fitDisposition === "BLOCKED") {
      throw new Stage1ValidationError(
        "SCREENING_BLOCKED",
        "eligibility or a required fit requirement blocks preparation",
      );
    }

    completeState("SELECTED", [input.command.selectionAuthorizationRef, hashes.inputSha256]);

    const preparedPacket = preparePacketMetadata(input, screening, livenessDecision, hashes);
    artifactStore.createAndVerifyBatch(preparedPacket.writes);
    committedArtifactWrites = preparedPacket.writes;
    const packetMetadata = preparedPacket.metadata;

    completeState("PREPARING", [
      packetMetadata.packetId,
      ...packetMetadata.artifacts.map((artifact) => artifact.artifactId),
    ]);

    const readyAuditEvent = transitionAuditEvent(input, hashes, lastState, "READY_FOR_REVIEW", [
      input.policy.policyId,
      hashes.policySha256,
      livenessDecision.evidence[1]?.evidenceId ?? "MISSING_PRE_READY_EVIDENCE",
      ...packetMetadata.artifacts.map((artifact) => artifact.sha256),
    ]);
    const auditEvents = [...completedAuditEvents, readyAuditEvent] as const;

    const auditCommit = commitAuditBatch(auditSink, auditEvents);
    lastState = "READY_FOR_REVIEW";

    const result: Stage1VerticalSliceResult = {
      schemaVersion: "ajas.stage1-vertical-slice-result.v1",
      executionMode: STAGE1_EXECUTION_MODE,
      readinessScope: STAGE1_READINESS_SCOPE,
      productionReady: false,
      applicationId: input.command.applicationId,
      subjectId: input.command.subjectId,
      correlationId: input.command.correlationId,
      idempotencyKey: input.command.idempotencyKey,
      inputSha256: hashes.inputSha256,
      sourcePolicyDecision,
      livenessDecision,
      screening,
      packetMetadata,
      state: "READY_FOR_REVIEW",
      stateHistory: buildSliceStateHistory(),
      auditEvents,
      auditCommit,
      humanBoundary: {
        terminalState: "READY_FOR_REVIEW",
        employerActionPermitted: false,
        employerActionsPerformed: [],
        officialPostingUrl: input.fixture.source.canonicalPostingUrl,
        officialPostingUrlPurpose: "SAVED_FIXTURE_SOURCE_PROVENANCE_ONLY",
        requiredHumanAction:
          "Review this synthetic fixture output inside AJAS only. Do not open an employer application form, contact the employer, upload files, make an attestation, or submit anything from this test result.",
      },
    };

    return immutableCopy(result);
  } catch (error) {
    let code = error instanceof Stage1ValidationError ? error.code : "INTERNAL_FIXTURE_FAILURE";
    let message =
      error instanceof Stage1ValidationError ? error.message : "fixture vertical slice failed";

    if (committedArtifactWrites !== null) {
      try {
        artifactStore.deleteBatchIfHashesMatch(committedArtifactWrites);
        committedArtifactWrites = null;
      } catch {
        code = "ARTIFACT_ROLLBACK_FAILED";
        message = "fixture artifact cleanup failed its hash-bound rollback";
      }
    }

    let auditEvent = denialAuditEvent(input, hashes, lastState, code);

    if (code !== "AUDIT_WRITE_FAILED" && code !== "AUDIT_RECEIPT_INVALID") {
      try {
        commitAuditBatch(auditSink, [...completedAuditEvents, auditEvent]);
      } catch {
        code = "AUDIT_WRITE_FAILED";
        message = "audit failure batch failed before commit";
        auditEvent = denialAuditEvent(input, hashes, lastState, code);
      }
    }

    throw new Stage1SliceError(code, message, lastState, auditEvent);
  }
}

export interface IdempotentVerticalSliceResult {
  readonly replayed: boolean;
  readonly result: Stage1VerticalSliceResult;
}

interface StoredVerticalSliceResult {
  readonly inputHash: string;
  readonly result: Stage1VerticalSliceResult;
}

export class InMemoryVerticalSliceRepository {
  readonly #results = new Map<string, StoredVerticalSliceResult>();

  public execute(
    rawInput: Stage1VerticalSliceInput,
    dependencies: VerticalSliceDependencies = {},
  ): IdempotentVerticalSliceResult {
    const input = parseVerticalSliceInput(rawInput);
    const resolvedDependencies = resolveDependencies(dependencies);
    const inputHash = sha256Hex(canonicalJson(input));
    const existing = this.#results.get(input.command.idempotencyKey);

    if (existing !== undefined) {
      if (existing.inputHash !== inputHash) {
        const hashes = contentHashesFor(input);
        let auditEvent = denialAuditEvent(input, hashes, null, "IDEMPOTENCY_CONFLICT");

        try {
          commitAuditBatch(resolvedDependencies.auditSink, [auditEvent]);
        } catch {
          auditEvent = denialAuditEvent(input, hashes, null, "AUDIT_WRITE_FAILED");
          throw new Stage1SliceError(
            "AUDIT_WRITE_FAILED",
            "idempotency-conflict audit failed before commit",
            null,
            auditEvent,
          );
        }

        throw new Stage1SliceError(
          "IDEMPOTENCY_CONFLICT",
          "idempotency key was reused with a different payload",
          null,
          auditEvent,
        );
      }

      return immutableCopy({ replayed: true, result: existing.result });
    }

    const result = runStage1VerticalSlice(input, resolvedDependencies);
    const storedResult = immutableCopy(result);
    this.#results.set(
      input.command.idempotencyKey,
      immutableCopy({ inputHash, result: storedResult }),
    );

    return immutableCopy({ replayed: false, result: storedResult });
  }

  public get size(): number {
    return this.#results.size;
  }
}
