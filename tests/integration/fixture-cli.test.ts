import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";

describe("fixture-only CLI", () => {
  it("prints only the byte-identical committed golden JSON", () => {
    const output = execFileSync(
      process.execPath,
      ["--import", "tsx", resolve("scripts/run-stage1-fixture.ts")],
      {
        cwd: process.cwd(),
        encoding: "utf8",
        env: { ...process.env, NEXT_TELEMETRY_DISABLED: "1" },
      },
    );
    const golden = readFileSync(
      resolve("tests/golden/stage1-greenhouse-ready-for-review.json"),
      "utf8",
    );

    expect(output).toBe(golden);
  });
});
