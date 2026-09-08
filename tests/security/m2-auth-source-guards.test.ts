// ============================================================
// CHECK CONFIGURATION CONTRACTS WITHOUT READING CREDENTIAL FILES.
// ============================================================
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

// ============================================================
// SOURCE ASSERTIONS ARE NOT A REAL DOCKER BUILD OR OAUTH FLOW.
// ============================================================
describe("M2 authentication source protections", () => {
  it("retains recursive environment and key exclusions", () => {
    const lines = readFileSync(".dockerignore", "utf8").split(/\r?\n/);
    for (const pattern of [
      "**/.env",
      "**/.env.*",
      "**/*.key",
      "**/*secret*.json",
      "**/*token*.json",
    ]) {
      expect(lines).toContain(pattern);
    }
    expect(lines.some((line) => line.startsWith("!"))).toBe(false);
  });
  it("disables framework development logging without removing security headers", () => {
    const source = readFileSync("apps/web/next.config.ts", "utf8");
    expect(source).toMatch(/^\s*logging: false,$/m);
    for (const header of [
      "X-Content-Type-Options",
      "X-Frame-Options",
      "Referrer-Policy",
      "Permissions-Policy",
    ]) {
      expect(source).toContain(header);
    }
  });
  it("leaves the normal development command unchanged", () => {
    const manifest = JSON.parse(readFileSync("apps/web/package.json", "utf8"));
    expect(manifest.scripts.dev).toBe("node ../../scripts/run-next.mjs dev");
    expect(manifest.scripts["dev:auth-spike"]).toBe("node ../../scripts/run-auth-spike.mjs");
  });
  it("defines a fixed loopback auth launcher without shell interpolation", () => {
    const source = readFileSync("scripts/run-auth-spike.mjs", "utf8");
    expect(source).toContain('"--hostname", "localhost", "--port", "3000"');
    expect(source).toContain("shell: false");
    expect(source).toContain("extraArguments.length !== 0");
  });
});
