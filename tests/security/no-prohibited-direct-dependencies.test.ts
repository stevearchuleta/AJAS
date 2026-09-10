import { readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";

const excludedDirectories = new Set([".git", ".next", "coverage", "dist", "node_modules", "tmp"]);

function findPackageFiles(directory = "."): string[] {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = resolve(directory, entry.name);

    if (entry.isDirectory()) {
      return excludedDirectories.has(entry.name) ? [] : findPackageFiles(entryPath);
    }

    return entry.isFile() && entry.name === "package.json" ? [entryPath] : [];
  });
}

const prohibitedDirectDependencies = [
  "@googleapis/gmail",
  "googleapis",
  "linkedin",
  "indeed",
  "playwright",
  "puppeteer",
  "selenium-webdriver",
  "stripe",
] as const;

const allowedDirectDependencies = new Set([
  "@eslint/js",
  "@types/node",
  "@types/react",
  "@types/react-dom",
  "eslint",
  "globals",
  "next",
  "prettier",
  "react",
  "react-dom",
  "tsx",
  "typescript",
  "typescript-eslint",
  "vitest",
  // ADR-001: Better Auth 1.7.3 is the reviewed M2 authentication dependency.
  "better-auth",
]);

describe("Stage-0B dependency boundary", () => {
  it("contains no direct employer, browser-agent, Google, email, or payment dependency", () => {
    const directDependencyNames = findPackageFiles().flatMap((packageFile) => {
      const packageJson = JSON.parse(readFileSync(packageFile, "utf8")) as {
        dependencies?: Record<string, string>;
        devDependencies?: Record<string, string>;
      };

      return [
        ...Object.keys(packageJson.dependencies ?? {}),
        ...Object.keys(packageJson.devDependencies ?? {}),
      ];
    });

    for (const prohibitedDependency of prohibitedDirectDependencies) {
      expect(directDependencyNames).not.toContain(prohibitedDependency);
    }

    expect([...new Set(directDependencyNames)].sort()).toEqual(
      [...allowedDirectDependencies].sort(),
    );
  });

  it("does not model the employer-action prohibition as a configurable switch", () => {
    const environmentExample = readFileSync(resolve(".env.example"), "utf8");

    expect(environmentExample).not.toMatch(/EMPLOYER/i);
  });
});
