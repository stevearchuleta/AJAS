// ============================================================
// SOURCE CHECKS COMPLEMENT RUNTIME TESTS; NO PRIVATE FILES ARE READ.
// ============================================================
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

describe("M2 Better Auth source and package guards", () => {
  it("pins only the reviewed Better Auth direct version", () => {
    const web = JSON.parse(readFileSync("apps/web/package.json", "utf8"));
    expect(web.dependencies["better-auth"]).toBe("1.7.3");
    expect(web.dependencies.next).toBe("16.3.3");
    expect(web.dependencies.react).toBe("19.2.0");
  });
  it("pins telemetry off in both supported Next.js launchers", () => {
    for (const path of ["scripts/run-next.mjs", "scripts/run-auth-spike.mjs"]) {
      const source = readFileSync(path, "utf8");
      expect(source).toContain('BETTER_AUTH_TELEMETRY: "0"');
      expect(source).toContain('BETTER_AUTH_TELEMETRY_DEBUG: "0"');
    }
    const options = readFileSync("apps/web/src/lib/auth/better-auth-options.ts", "utf8");
    expect(options).toContain("telemetry: { enabled: false, debug: false }");
    expect(options).toContain("logger: { disabled: true }");
  });
  it("publishes blank environment names only", () => {
    const lines = readFileSync("apps/web/.env.example", "utf8").split(/\r?\n/);
    for (const line of lines.filter((line) => line !== "" && !line.startsWith("#"))) {
      expect(line).toMatch(/^[A-Z][A-Z0-9_]*=$/);
      expect(line).not.toMatch(/^NEXT_PUBLIC_/);
    }
    expect(lines).toContain("GOOGLE_CLIENT_ID=");
    expect(lines).toContain("GOOGLE_CLIENT_SECRET=");
    expect(lines).toContain("BETTER_AUTH_SECRET=");
  });
  it("uses the minimal entry point without altering the vendor graph", () => {
    const source = readFileSync("apps/web/src/lib/auth/better-auth-runtime.ts", "utf8");
    expect(source).toContain('await import("better-auth/minimal")');
    expect(source).not.toContain("console.");
    expect(source).not.toContain("readFile");
  });
});
