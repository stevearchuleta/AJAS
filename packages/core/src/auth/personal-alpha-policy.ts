// ============================================================
// DEFINE FIXED POLICY RESULTS WITHOUT RETURNING PRIVATE VALUES.
// PROVIDER SIGNATURE/TOKEN VERIFICATION BELONGS TO BETTER AUTH.
// NEVER CALL THIS POLICY WITH IDENTITY TAKEN FROM REQUEST JSON.
// ============================================================
export type PersonalAlphaDecisionCode =
  | "AUTH_DISABLED"
  | "AUTH_CONFIGURATION_INVALID"
  | "AUTH_SPIKE_LOCAL_ONLY"
  | "AUTH_IDENTITY_INVALID"
  | "AUTH_PROVIDER_DENIED"
  | "AUTH_DISCOVERY_SESSION_DENIED"
  | "AUTH_SUBJECT_DENIED"
  | "AUTH_ADMITTED";

// ============================================================
// SEPARATE PERMISSION TO CAPTURE A CANDIDATE FROM ADMISSION.
// CAPTURE CANDIDATES NEVER IMPLY AUTHORIZATION OR SESSION ISSUANCE.
// ============================================================
export interface PersonalAlphaDecision {
  readonly allowed: boolean;
  readonly captureCandidate: boolean;
  readonly code: PersonalAlphaDecisionCode;
}

// ============================================================
// KEEP CONFIGURATION INDEPENDENT OF ANY AUTHENTICATION LIBRARY.
// ONLY THE PRIVATE CONFIGURATION BOUNDARY READS ENVIRONMENT DATA.
// ============================================================
export interface PersonalAlphaConfiguration {
  readonly mode: "disabled" | "discovery" | "allowlist";
  readonly localDevelopment: boolean;
  readonly allowedGoogleSubject: string | null;
}

// ============================================================
// ACCEPT PLAIN RECORDS; DO NOT COERCE NUMBERS OR MISSING VALUES.
// ============================================================
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// ============================================================
// TREAT SUBJECTS AS OPAQUE, CASE-SENSITIVE STRINGS UP TO 255 CHARS.
// NEVER PARSE AS A NUMBER, TRIM, LOWERCASE, OR NORMALIZE A SUBJECT.
// ============================================================
function isSubject(value: unknown): value is string {
  if (typeof value !== "string" || value.length === 0 || value.length > 255) {
    return false;
  }
  // ========================================================
  // REJECT WHITESPACE AND CONTROL CHARACTERS WITHOUT REWRITING.
  // ========================================================
  return !Array.from(value).some((character) => {
    const code = character.charCodeAt(0);
    return character.trim() === "" || code < 32 || (code >= 127 && code <= 159);
  });
}

// ============================================================
// CENTRALIZE THE ONLY READ OF THE PRIVATE SUBJECT CONFIGURATION.
// A LAUNCH MARKER ALONE IS NOT PROOF OF A LOOPBACK SOCKET; THE
// FIXED LOCAL LAUNCHER AND LATER RUNTIME TEST PROVIDE THAT EVIDENCE.
// ============================================================
export function readPersonalAlphaConfiguration(
  environment: Readonly<Record<string, string | undefined>>,
): PersonalAlphaConfiguration {
  const localDevelopment =
    environment.NODE_ENV === "development" && environment.AJAS_AUTH_SPIKE_LOOPBACK_LAUNCH === "1";
  const discoverySetting = environment.AJAS_AUTH_SPIKE_DISCOVERY;
  const allowedGoogleSubject = environment.AJAS_ALLOWED_GOOGLE_SUB;
  // ========================================================
  // DISABLED IS THE DEFAULT; AMBIGUOUS MODES CANNOT ENABLE AUTH.
  // ========================================================
  if (!localDevelopment || (discoverySetting !== "0" && discoverySetting !== "1")) {
    return Object.freeze({ mode: "disabled", localDevelopment, allowedGoogleSubject: null });
  }
  // ========================================================
  // DISCOVERY AND AN EXISTING ALLOWLIST CANNOT BE ENABLED TOGETHER.
  // ========================================================
  if (discoverySetting === "1") {
    if (allowedGoogleSubject !== undefined && allowedGoogleSubject !== "") {
      return Object.freeze({ mode: "disabled", localDevelopment, allowedGoogleSubject: null });
    }
    return Object.freeze({ mode: "discovery", localDevelopment, allowedGoogleSubject: null });
  }
  // ========================================================
  // NORMAL ADMISSION REQUIRES AN EXPLICIT VALID PRIVATE SUBJECT.
  // ========================================================
  if (!isSubject(allowedGoogleSubject)) {
    return Object.freeze({ mode: "disabled", localDevelopment, allowedGoogleSubject: null });
  }
  return Object.freeze({ mode: "allowlist", localDevelopment, allowedGoogleSubject });
}

// ============================================================
// RETURN ONLY FIXED, IMMUTABLE DECISION FIELDS.
// ============================================================
function decision(
  code: PersonalAlphaDecisionCode,
  allowed = false,
  captureCandidate = false,
): PersonalAlphaDecision {
  return Object.freeze({ allowed, captureCandidate, code });
}

// ============================================================
// IMPLEMENT THE SINGLE PERSONAL-ALPHA POLICY AT MULTIPLE FUTURE
// ENFORCEMENT POINTS. INPUT IDENTITY MUST ALREADY BE VERIFIED BY
// THE AUTH LIBRARY OR AN AUTHORITATIVE SERVER-SIDE SESSION CHECK.
// THIS PURE FUNCTION DOES NOT AUTHENTICATE AN OIDC TOKEN.
// ============================================================
export function evaluatePersonalAlphaAdmission(
  configuration: unknown,
  verifiedIdentity: unknown,
): PersonalAlphaDecision {
  // ========================================================
  // FAIL CLOSED EVEN IF AN UNEXPECTED OBJECT THROWS ON ACCESS.
  // ========================================================
  try {
    if (!isRecord(configuration)) {
      return decision("AUTH_CONFIGURATION_INVALID");
    }
    if (configuration.mode === "disabled") {
      return decision("AUTH_DISABLED");
    }
    if (configuration.mode !== "discovery" && configuration.mode !== "allowlist") {
      return decision("AUTH_CONFIGURATION_INVALID");
    }
    if (configuration.localDevelopment !== true) {
      return decision("AUTH_SPIKE_LOCAL_ONLY");
    }
    if (!isRecord(verifiedIdentity)) {
      return decision("AUTH_IDENTITY_INVALID");
    }
    if (verifiedIdentity.provider !== "google") {
      return decision("AUTH_PROVIDER_DENIED");
    }
    if (
      !isSubject(verifiedIdentity.subject) ||
      (verifiedIdentity.context !== "provider-admission" &&
        verifiedIdentity.context !== "protected-operation")
    ) {
      return decision("AUTH_IDENTITY_INVALID");
    }
    // ====================================================
    // DISCOVERY ALWAYS DENIES; ONLY A VERIFIED FRESH PROVIDER
    // CALLBACK MAY REQUEST CAPTURE FOR PRIVATE CONFIRMATION.
    // ====================================================
    if (configuration.mode === "discovery") {
      if (configuration.allowedGoogleSubject !== null) {
        return decision("AUTH_CONFIGURATION_INVALID");
      }
      return decision(
        "AUTH_DISCOVERY_SESSION_DENIED",
        false,
        verifiedIdentity.context === "provider-admission",
      );
    }
    // ====================================================
    // COMPARE EXACT SUBJECTS; EMAIL HAS NO AUTHORIZATION ROLE.
    // ====================================================
    if (!isSubject(configuration.allowedGoogleSubject)) {
      return decision("AUTH_CONFIGURATION_INVALID");
    }
    if (verifiedIdentity.subject !== configuration.allowedGoogleSubject) {
      return decision("AUTH_SUBJECT_DENIED");
    }
    return decision("AUTH_ADMITTED", true);
  } catch {
    return decision("AUTH_IDENTITY_INVALID");
  }
}
