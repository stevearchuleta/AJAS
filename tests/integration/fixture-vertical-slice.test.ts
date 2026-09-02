import { describe, expect, it } from "vitest";

import {
  InMemoryAuditSink,
  InMemoryFixtureArtifactStore,
  InMemoryVerticalSliceRepository,
  Stage1SliceError,
  Stage1ValidationError,
  canonicalJson,
  runStage1VerticalSlice,
  sha256Hex,
  stablePrettyJson,
} from "../../packages/core/src/index.js";
import { cloneStage1Input, loadStage1VerticalSliceInput } from "../helpers/stage1-fixtures.js";

describe("fixture-only vertical slice integration", () => {
  it("runs approved synthetic facts through the saved Greenhouse fixture to READY", () => {
    const input = loadStage1VerticalSliceInput();
    const result = runStage1VerticalSlice(input);

    expect(result).toMatchObject({
      executionMode: "FIXTURE_ONLY",
      readinessScope: "STAGE1_VERTICAL_SLICE_TEST",
      productionReady: false,
      state: "READY_FOR_REVIEW",
      sourcePolicyDecision: { networkAuthorized: false },
      livenessDecision: { currentStatus: "NOT_CHECKED" },
      screening: {
        eligibility: "ELIGIBLE",
        fitDisposition: "PROCEED_WITH_NAMED_GAPS",
        numericScoreUsed: false,
      },
    });
    expect(new Set(result.auditEvents.map((event) => event.correlationId))).toEqual(
      new Set([input.command.correlationId]),
    );
  });

  it.each(["FACTS", "POLICY", "LIVENESS", "ELIGIBILITY"])(
    "stops before READY when the %s gate fails",
    (failureMode) => {
      const input = cloneStage1Input();

      if (failureMode === "FACTS") {
        (
          input.facts as unknown as {
            facts: Array<{ provenance: { evidenceRef: string } }>;
          }
        ).facts[0]!.provenance.evidenceRef = "";
      } else if (failureMode === "POLICY") {
        (input.policy as unknown as { boardToken: string }).boardToken = "unregistered";
      } else if (failureMode === "LIVENESS") {
        (
          input.fixture as unknown as {
            observations: Array<{ httpStatus: number }>;
          }
        ).observations[1]!.httpStatus = 404;
      } else {
        const fact = (
          input.facts as unknown as {
            facts: Array<{ factKey: string; value: unknown }>;
          }
        ).facts.find((candidate) => candidate.factKey === "authorized_to_work_us_full_time");
        expect(fact).toBeDefined();

        if (fact !== undefined) {
          fact.value = false;
        }

        const factsSha256 = sha256Hex(canonicalJson(input.facts));
        (input.command as unknown as { factsSnapshotSha256: string }).factsSnapshotSha256 =
          factsSha256;
        const policy = input.policy as unknown as {
          approvedFactsSnapshotSha256: string;
          approvedCommandSha256: string;
        };
        policy.approvedFactsSnapshotSha256 = factsSha256;
        policy.approvedCommandSha256 = sha256Hex(canonicalJson(input.command));
      }

      const expectedError =
        failureMode === "FACTS" || failureMode === "LIVENESS"
          ? Stage1ValidationError
          : Stage1SliceError;
      expect(() => runStage1VerticalSlice(input)).toThrowError(expectedError);

      try {
        runStage1VerticalSlice(input);
      } catch (error) {
        expect(error).toBeInstanceOf(expectedError);

        if (error instanceof Stage1SliceError) {
          expect(error.auditEvent.outcome).toBe("DENIED");
          expect(error.lastState).not.toBe("READY_FOR_REVIEW");
        }
      }
    },
  );

  it("performs no network request even when global fetch would fail", () => {
    const originalFetch = globalThis.fetch;
    let calls = 0;
    globalThis.fetch = (() => {
      calls += 1;
      throw new Error("network access is prohibited in the fixture slice");
    }) as typeof fetch;

    try {
      const result = runStage1VerticalSlice(loadStage1VerticalSliceInput());
      expect(result.state).toBe("READY_FOR_REVIEW");
      expect(calls).toBe(0);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("returns byte-identical output on idempotent replay", () => {
    const repository = new InMemoryVerticalSliceRepository();
    const input = loadStage1VerticalSliceInput();
    const first = repository.execute(input);
    const replay = repository.execute(input);

    expect(stablePrettyJson(replay.result)).toBe(stablePrettyJson(first.result));
    expect(replay.replayed).toBe(true);
    expect(repository.size).toBe(1);
  });

  it("cannot return READY when the audit sink is unavailable", () => {
    const artifactStore = new InMemoryFixtureArtifactStore();
    const failingAuditSink = new InMemoryAuditSink({ failBeforeCommit: true });

    expect(() =>
      runStage1VerticalSlice(loadStage1VerticalSliceInput(), {
        artifactStore,
        auditSink: failingAuditSink,
      }),
    ).toThrowError(expect.objectContaining({ code: "AUDIT_WRITE_FAILED" }));
    expect(artifactStore.size).toBe(0);
    expect(failingAuditSink.size).toBe(0);
  });

  it("writes one transition batch on success", () => {
    const sink = new InMemoryAuditSink();
    runStage1VerticalSlice(loadStage1VerticalSliceInput(), { auditSink: sink });
    expect(sink.readAll()).toHaveLength(5);
  });
});
