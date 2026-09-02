import { readFileSync } from "node:fs";

import { describe, expect, it } from "vitest";

import {
  InMemoryFixtureArtifactStore,
  canonicalJson,
  runStage1VerticalSlice,
  sha256Hex,
  stablePrettyJson,
} from "../../packages/core/src/index.js";
import { loadStage1VerticalSliceInput } from "../helpers/stage1-fixtures.js";

describe("Stage-1 vertical-slice golden output", () => {
  it("matches the exact committed canonical result", () => {
    const golden = readFileSync(
      new URL("./stage1-greenhouse-ready-for-review.json", import.meta.url),
      "utf8",
    );
    const result = runStage1VerticalSlice(loadStage1VerticalSliceInput());

    expect(stablePrettyJson(result)).toBe(golden);
    expect(golden.endsWith("\n")).toBe(true);
  });

  it("canonicalizes object insertion order deterministically", () => {
    const left = { zeta: 3, alpha: { second: 2, first: 1 } };
    const right = { alpha: { first: 1, second: 2 }, zeta: 3 };

    expect(canonicalJson(left)).toBe(canonicalJson(right));
    expect(sha256Hex(canonicalJson(left))).toBe(sha256Hex(canonicalJson(right)));
  });

  it("recomputes the fixture and every artifact/readback hash", () => {
    const input = loadStage1VerticalSliceInput();
    const store = new InMemoryFixtureArtifactStore();
    const result = runStage1VerticalSlice(input, { artifactStore: store });

    expect(sha256Hex(canonicalJson(input.fixture.savedPosting))).toBe(
      input.fixture.savedPostingSha256,
    );

    for (const artifact of result.packetMetadata.artifacts) {
      const bytes = store.read(artifact.artifactId);
      expect(sha256Hex(bytes)).toBe(artifact.sha256);
      expect(artifact.readbackSha256).toBe(artifact.sha256);
      expect(bytes.byteLength).toBe(artifact.bytes);
    }
  });
});
