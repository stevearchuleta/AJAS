import { describe, expect, it } from "vitest";

import {
  InMemoryAuditSink,
  InMemoryFixtureArtifactStore,
  InMemoryVerticalSliceRepository,
  Stage1SliceError,
  Stage1ValidationError,
  assertSliceTransition,
  canonicalJson,
  runStage1VerticalSlice,
  sha256Hex,
  stablePrettyJson,
  type FixtureArtifactStore,
  type Stage1VerticalSliceInput,
} from "../../packages/core/src/index.js";
import { cloneStage1Input, loadStage1VerticalSliceInput } from "../helpers/stage1-fixtures.js";

const SAFE_REVIEW_INSTRUCTION =
  "Review this synthetic fixture output inside AJAS only. Do not open an employer application form, contact the employer, upload files, make an attestation, or submit anything from this test result.";

function rebindTrustedFactsAndCommand(input: Stage1VerticalSliceInput): void {
  const factsSha256 = sha256Hex(canonicalJson(input.facts));
  (input.command as unknown as { factsSnapshotSha256: string }).factsSnapshotSha256 = factsSha256;
  const commandSha256 = sha256Hex(canonicalJson(input.command));
  const policy = input.policy as unknown as {
    approvedFactsSnapshotSha256: string;
    approvedCommandSha256: string;
  };
  policy.approvedFactsSnapshotSha256 = factsSha256;
  policy.approvedCommandSha256 = commandSha256;
}

describe("packet metadata, state, audit, and idempotency", () => {
  it("performs real in-memory byte readback before fixture-scoped READY", () => {
    const input = loadStage1VerticalSliceInput();
    const store = new InMemoryFixtureArtifactStore();
    const auditSink = new InMemoryAuditSink();
    const result = runStage1VerticalSlice(input, { artifactStore: store, auditSink });

    expect(result.state).toBe("READY_FOR_REVIEW");
    expect(result.productionReady).toBe(false);
    expect(result.packetMetadata.artifactStore).toBe("IN_MEMORY_FIXTURE_STORE");
    expect(result.packetMetadata.authoritativeByteStoreUsed).toBe(false);
    expect(result.packetMetadata.artifacts).toHaveLength(3);
    expect(
      result.packetMetadata.artifacts.every(
        (artifact) => artifact.sha256 === artifact.readbackSha256,
      ),
    ).toBe(true);
    expect(store.size).toBe(3);
    expect(result.auditCommit).toEqual({
      store: "IN_MEMORY_FIXTURE_AUDIT",
      status: "COMMITTED",
      eventCount: 5,
      batchSha256: sha256Hex(canonicalJson(result.auditEvents)),
    });
  });

  it("records the exact five-state path and complete transition audit", () => {
    const input = loadStage1VerticalSliceInput();
    const result = runStage1VerticalSlice(input);

    expect(result.stateHistory).toEqual([
      "DISCOVERED",
      "SCREENED",
      "SELECTED",
      "PREPARING",
      "READY_FOR_REVIEW",
    ]);
    expect(result.auditEvents).toHaveLength(5);

    for (const event of result.auditEvents) {
      expect(event).toMatchObject({
        userId: input.command.userId,
        actorId: input.command.actorId,
        actorVersion: input.command.actorVersion,
        targetId: input.command.applicationId,
        idempotencyKey: input.command.idempotencyKey,
        correlationId: input.command.correlationId,
        outcome: "SUCCESS",
      });
      expect(event.evidenceRefs.length).toBeGreaterThan(0);
    }
  });

  it("rejects invalid and post-boundary transitions", () => {
    expect(() => assertSliceTransition("DISCOVERED", "PREPARING")).toThrow();
    expect(() =>
      assertSliceTransition(
        "READY_FOR_REVIEW",
        "SUBMITTED_BY_USER" as unknown as "READY_FOR_REVIEW",
      ),
    ).toThrow();
  });

  it("replays a defensive immutable copy without duplicate audit", () => {
    const input = loadStage1VerticalSliceInput();
    const repository = new InMemoryVerticalSliceRepository();
    const auditSink = new InMemoryAuditSink();
    const first = repository.execute(input, { auditSink });
    const replay = repository.execute(input, { auditSink });

    expect(first.replayed).toBe(false);
    expect(replay.replayed).toBe(true);
    expect(replay.result).not.toBe(first.result);
    expect(stablePrettyJson(replay.result)).toBe(stablePrettyJson(first.result));
    expect(Object.isFrozen(first.result)).toBe(true);
    expect(Object.isFrozen(first.result.auditEvents[0])).toBe(true);
    expect(() => {
      (first.result as unknown as { state: string }).state = "CORRUPTED";
    }).toThrow(TypeError);
    expect(repository.size).toBe(1);
    expect(auditSink.readAll()).toHaveLength(5);

    const firstRead = auditSink.readAll();
    const secondRead = auditSink.readAll();
    expect(firstRead).not.toBe(secondRead);
    expect(Object.isFrozen(firstRead)).toBe(true);
    expect(Object.isFrozen(firstRead[0])).toBe(true);
    expect(() => {
      (firstRead[0] as unknown as { outcome: string }).outcome = "DENIED";
    }).toThrow(TypeError);
    expect(secondRead[0]?.outcome).toBe("SUCCESS");
  });

  it("rejects a conflicting payload under the same idempotency key", () => {
    const input = loadStage1VerticalSliceInput();
    const repository = new InMemoryVerticalSliceRepository();
    repository.execute(input);
    const conflicting = cloneStage1Input(input);
    (conflicting.command as unknown as { runId: string }).runId = "different-run";

    expect(() => repository.execute(conflicting)).toThrowError(
      expect.objectContaining({ code: "IDEMPOTENCY_CONFLICT" }),
    );
  });

  it("binds packet, artifact, and event identities to valid input content", () => {
    const firstInput = loadStage1VerticalSliceInput();
    const changedInput = cloneStage1Input(firstInput);
    const mutableFacts = changedInput.facts as unknown as {
      facts: Array<{ factKey: string; value: unknown }>;
    };
    const yearsFact = mutableFacts.facts.find(
      (fact) => fact.factKey === "years_relevant_fpa_or_corporate_finance_experience",
    );
    expect(yearsFact).toBeDefined();

    if (yearsFact !== undefined) {
      yearsFact.value = 10;
    }

    rebindTrustedFactsAndCommand(changedInput);

    const first = runStage1VerticalSlice(firstInput);
    const changed = runStage1VerticalSlice(changedInput);

    expect(changed.inputSha256).not.toBe(first.inputSha256);
    expect(changed.packetMetadata.packetId).not.toBe(first.packetMetadata.packetId);
    expect(changed.packetMetadata.artifacts.map((artifact) => artifact.artifactId)).not.toEqual(
      first.packetMetadata.artifacts.map((artifact) => artifact.artifactId),
    );
    expect(changed.auditEvents.map((event) => event.eventId)).not.toEqual(
      first.auditEvents.map((event) => event.eventId),
    );
  });

  it("records completed transitions plus denial for an ordinary failure", () => {
    const input = cloneStage1Input();
    const mutableFacts = input.facts as unknown as {
      facts: Array<{ factKey: string; value: unknown }>;
    };
    const workAuthorization = mutableFacts.facts.find(
      (fact) => fact.factKey === "authorized_to_work_us_full_time",
    );
    expect(workAuthorization).toBeDefined();

    if (workAuthorization !== undefined) {
      workAuthorization.value = false;
    }

    rebindTrustedFactsAndCommand(input);

    const store = new InMemoryFixtureArtifactStore();
    const auditSink = new InMemoryAuditSink();

    expect(() => runStage1VerticalSlice(input, { artifactStore: store, auditSink })).toThrowError(
      expect.objectContaining({ code: "SCREENING_BLOCKED" }),
    );
    expect(store.size).toBe(0);
    expect(auditSink.readAll().map((event) => [event.newState, event.outcome])).toEqual([
      ["DISCOVERED", "SUCCESS"],
      ["SCREENED", "SUCCESS"],
      ["SCREENED", "DENIED"],
    ]);
  });

  it("rolls back the complete artifact batch when audit fails before commit", () => {
    const store = new InMemoryFixtureArtifactStore();
    const auditSink = new InMemoryAuditSink({ failBeforeCommit: true });

    expect(() =>
      runStage1VerticalSlice(loadStage1VerticalSliceInput(), { artifactStore: store, auditSink }),
    ).toThrowError(expect.objectContaining({ code: "AUDIT_WRITE_FAILED" }));
    expect(store.size).toBe(0);
    expect(auditSink.size).toBe(0);
  });

  it("rejects structurally compatible external adapters at runtime", () => {
    const externalStore: FixtureArtifactStore = {
      create() {},
      read() {
        return new Uint8Array();
      },
    };

    expect(() =>
      runStage1VerticalSlice(loadStage1VerticalSliceInput(), {
        artifactStore: externalStore,
        auditSink: new InMemoryAuditSink(),
      }),
    ).toThrowError(expect.objectContaining({ code: "UNSUPPORTED_FIXTURE_ADAPTER" }));
  });

  it("deep-validates input before hashing or touching transactional stores", () => {
    const input = cloneStage1Input();
    (input.command as unknown as { factsSnapshotVersion: unknown }).factsSnapshotVersion = "one";
    const artifactStore = new InMemoryFixtureArtifactStore();
    const auditSink = new InMemoryAuditSink();

    expect(() => runStage1VerticalSlice(input, { artifactStore, auditSink })).toThrowError(
      Stage1ValidationError,
    );
    expect(artifactStore.size).toBe(0);
    expect(auditSink.size).toBe(0);
  });

  it.each([
    ["approvedFactsSnapshotSha256", "POLICY_FACTS_BINDING_MISMATCH"],
    ["approvedCommandSha256", "POLICY_COMMAND_BINDING_MISMATCH"],
  ] as const)("enforces the source-policy %s pin", (field, expectedCode) => {
    const input = cloneStage1Input();
    (input.policy as unknown as Record<typeof field, string>)[field] = "0".repeat(64);
    const auditSink = new InMemoryAuditSink();

    expect(() => runStage1VerticalSlice(input, { auditSink })).toThrowError(
      expect.objectContaining({ code: expectedCode }),
    );
    expect(auditSink.readAll()).toHaveLength(1);
    expect(auditSink.readAll()[0]).toMatchObject({
      outcome: "DENIED",
      failureCode: expectedCode,
    });
  });

  it("uses provenance-only synthetic review wording", () => {
    const result = runStage1VerticalSlice(loadStage1VerticalSliceInput());

    expect(result.humanBoundary.officialPostingUrlPurpose).toBe(
      "SAVED_FIXTURE_SOURCE_PROVENANCE_ONLY",
    );
    expect(result.humanBoundary.requiredHumanAction).toBe(SAFE_REVIEW_INSTRUCTION);
    expect(result).not.toBeInstanceOf(Stage1SliceError);
  });
});
