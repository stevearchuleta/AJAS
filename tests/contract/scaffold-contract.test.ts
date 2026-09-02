import { existsSync } from "node:fs";

import { describe, expect, it } from "vitest";

const requiredPaths = [
  "apps/web",
  "apps/worker",
  "packages/core",
  "packages/database",
  "packages/agents",
  "packages/tools",
  "packages/documents",
  "packages/observability",
  "packages/config",
  "packages/ui",
  "tests/unit",
  "tests/integration",
  "tests/contract",
  "tests/e2e",
  "tests/security",
  "tests/fixtures",
  "tests/golden",
  "scripts",
  "infra/local",
  "infra/preview",
  "infra/staging",
  "infra/production",
  ".github/workflows/ci.yml",
  "README.md",
  "AGENTS.md",
  ".env.example",
  ".gitignore",
] as const;

describe("Stage-0B scaffold contract", () => {
  it("contains every required scaffold path", () => {
    for (const requiredPath of requiredPaths) {
      expect(existsSync(requiredPath), requiredPath).toBe(true);
    }
  });
});
