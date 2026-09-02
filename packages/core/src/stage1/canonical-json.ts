import { createHash } from "node:crypto";

import { Stage1ValidationError } from "./contracts.js";

type JsonPrimitive = boolean | null | number | string;
type CanonicalJsonValue = JsonPrimitive | readonly CanonicalJsonValue[] | CanonicalJsonObject;
interface CanonicalJsonObject {
  readonly [key: string]: CanonicalJsonValue;
}

function canonicalize(value: unknown, seen: Set<object>): CanonicalJsonValue {
  if (value === null || typeof value === "boolean") {
    return value;
  }

  if (typeof value === "string") {
    return value.normalize("NFC");
  }

  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      throw new Stage1ValidationError("NON_CANONICAL_JSON", "JSON numbers must be finite");
    }

    return value;
  }

  if (typeof value !== "object") {
    throw new Stage1ValidationError(
      "NON_CANONICAL_JSON",
      `Unsupported JSON value type: ${typeof value}`,
    );
  }

  if (seen.has(value)) {
    throw new Stage1ValidationError("NON_CANONICAL_JSON", "Circular JSON value detected");
  }

  seen.add(value);

  try {
    if (Array.isArray(value)) {
      return value.map((item) => canonicalize(item, seen));
    }

    const record = value as Record<string, unknown>;
    const normalizedKeys = new Set<string>();
    const canonicalEntries = Object.keys(record)
      .map((key) => [key.normalize("NFC"), key] as const)
      .sort(([left], [right]) => (left < right ? -1 : left > right ? 1 : 0))
      .map(([normalizedKey, originalKey]) => {
        if (normalizedKeys.has(normalizedKey)) {
          throw new Stage1ValidationError(
            "NON_CANONICAL_JSON",
            "Object contains duplicate Unicode-normalized keys",
          );
        }

        normalizedKeys.add(normalizedKey);
        return [normalizedKey, canonicalize(record[originalKey], seen)] as const;
      });

    return Object.fromEntries(canonicalEntries);
  } finally {
    seen.delete(value);
  }
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(canonicalize(value, new Set<object>()));
}

export function sha256Hex(value: string | Uint8Array): string {
  return createHash("sha256").update(value).digest("hex");
}

export function stablePrettyJson(value: unknown): string {
  return `${JSON.stringify(canonicalize(value, new Set<object>()), null, 2)}\n`;
}
