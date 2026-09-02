import { describe, expect, it } from "vitest";

import { canonicalJson } from "../../packages/core/src/index.js";

describe("canonical JSON Unicode key normalization", () => {
  it("rejects duplicate normalized keys on the top-level object", () => {
    const value = { "e\u0301": 1, é: 2 };

    expect(() => canonicalJson(value)).toThrowError(
      expect.objectContaining({ code: "NON_CANONICAL_JSON" }),
    );
  });

  it("rejects duplicate normalized keys inside a nested object", () => {
    const value = { outer: [{ "A\u030a": true, Å: false }] };

    expect(() => canonicalJson(value)).toThrowError(
      expect.objectContaining({ code: "NON_CANONICAL_JSON" }),
    );
  });

  it("allows the same normalized key in separate sibling objects", () => {
    const value = [{ "e\u0301": 1 }, { é: 2 }];

    expect(canonicalJson(value)).toBe('[{"é":1},{"é":2}]');
  });

  it("sorts keys after Unicode normalization", () => {
    expect(canonicalJson({ "e\u0301": 1, z: 2 })).toBe(canonicalJson({ é: 1, z: 2 }));
  });
});
