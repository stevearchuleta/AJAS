import { existsSync, readFileSync } from "node:fs";

const requiredFiles = [
  "README.md",
  "AGENTS.md",
  "package.json",
  "tsconfig.base.json",
  "apps/web/package.json",
  "apps/worker/package.json",
  "packages/core/package.json",
  "scripts/run-next.mjs",
  "tests/unit/human-boundary.test.ts",
  "tests/security/no-prohibited-direct-dependencies.test.ts",
];

const forbiddenEnvironmentAssignments = [
  /GOOGLE[^=]*=\S+/i,
  /GMAIL[^=]*=\S+/i,
  /DATABASE_URL=\S+/i,
  /API_KEY=\S+/i,
  /TOKEN=\S+/i,
];

for (const requiredFile of requiredFiles) {
  if (!existsSync(requiredFile)) {
    throw new Error(`Missing required scaffold file: ${requiredFile}`);
  }
}

const environmentExample = readFileSync(".env.example", "utf8");

for (const forbiddenAssignment of forbiddenEnvironmentAssignments) {
  if (forbiddenAssignment.test(environmentExample)) {
    throw new Error(`Credential-like value found in .env.example: ${forbiddenAssignment}`);
  }
}

console.log("AJAS Stage-0B scaffold verification passed.");
