// ============================================================
// GENERATE CORRELATION IDS ON THE SERVER, NOT FROM HTTP HEADERS.
// ============================================================
import { randomUUID } from "node:crypto";

// ============================================================
// ALLOW ONLY FIXED EVENT CODES; NEVER ACCEPT A MESSAGE OR PAYLOAD.
// ============================================================
const eventCodes = new Set([
  "AUTH_REQUEST_STARTED",
  "AUTH_CONFIGURATION_DENIED",
  "AUTH_IDENTITY_DENIED",
  "AUTH_CANDIDATE_CAPTURED",
  "AUTH_CAPTURE_FAILED",
  "AUTH_SESSION_ADMITTED",
  "AUTH_SIGN_OUT_COMPLETED",
  "AUTH_PROVIDER_FAILED",
]);

// ============================================================
// CREATE ONE WRITER PER REQUEST TO CORRELATE SAFE EVENTS.
// NO SUBJECT, TOKEN, EMAIL, URL, HEADER, OR EXCEPTION IS ACCEPTED.
// CUSTOM WRITERS SUPPORT DETERMINISTIC CAPTURE IN TESTS.
// ============================================================
export function createAuthEventWriter(
  writeLine: (line: string) => void = (line) => console.info(line),
): (eventCode: unknown) => void {
  const correlationId = randomUUID();
  return (eventCode: unknown): void => {
    // ====================================================
    // MAP UNRECOGNIZED INPUT TO A FIXED CODE WITHOUT COERCION.
    // ====================================================
    const code =
      typeof eventCode === "string" && eventCodes.has(eventCode)
        ? eventCode
        : "AUTH_EVENT_INPUT_REJECTED";
    // ====================================================
    // REBUILD THE RECORD FROM ALLOWED FIELDS; NEVER SPREAD INPUT.
    // ====================================================
    writeLine(
      JSON.stringify({
        schema: "ajas.auth.event.v1",
        correlationId,
        timestamp: new Date().toISOString(),
        code,
      }),
    );
  };
}
