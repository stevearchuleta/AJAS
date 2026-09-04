#!/usr/bin/env python3
"""
AJAS MILESTONE 1 PRESERVATION PREFLIGHT, VERSION 0.1.0.

PURPOSE:
- VERIFY THE CURRENT MILESTONE-0 GIT BASELINE IMMEDIATELY BEFORE PRESERVATION.
- VERIFY THE THREE VERSIONED RECONCILIATION UTILITIES BY SHA-256.
- VERIFY THE LIVE COLD-CACHE RECONCILIATION EVIDENCE BY SHA-256 AND CONTENT.
- RE-RUN THE V0.1.2 IN-PROCESS PARSER REGRESSION TESTS.
- CHECK PROPOSED BRANCH, TAG, WORKTREE, TARGET PATH, AND IGNORE-RULE COLLISIONS.
- SCAN CANDIDATE ARTIFACTS FOR HIGH-CONFIDENCE SECRET MATERIAL.
- PRODUCE AN OPTIONAL IMMUTABLE JSON PREFLIGHT RECORD OUTSIDE THE REPOSITORY.

SAFETY GUARANTEES:
- NO GIT MUTATION COMMANDS.
- NO AZURE COMMANDS.
- NO GITHUB NETWORK COMMANDS.
- NO REPOSITORY FILE WRITES.
- NO BRANCH, TAG, COMMIT, WORKTREE, PUSH, OR PULL-REQUEST CREATION.
- NO BILLABLE RESOURCE CREATION.
- STDOUT AND STDERR REMAIN SEPARATE FOR EVERY CHILD PROCESS.
- MISSING OUTPUT VALUES ARE NORMALIZED BEFORE STRING OPERATIONS.
- OPTIONAL JSON OUTPUT USES EXCLUSIVE CREATION AND MUST REMAIN OUTSIDE THE REPOSITORY.
"""

# ============================================================
# IMPORT STANDARD-LIBRARY FUTURE ANNOTATION SUPPORT.
# ============================================================
from __future__ import annotations

# ============================================================
# IMPORT COMMAND-LINE ARGUMENT SUPPORT.
# ============================================================
import argparse

# ============================================================
# IMPORT SHA-256 HASH SUPPORT.
# ============================================================
import hashlib

# ============================================================
# IMPORT JSON SUPPORT.
# ============================================================
import json

# ============================================================
# IMPORT OPERATING-SYSTEM SUPPORT.
# ============================================================
import os

# ============================================================
# IMPORT REGULAR-EXPRESSION SUPPORT.
# ============================================================
import re

# ============================================================
# IMPORT EXECUTABLE-DISCOVERY SUPPORT.
# ============================================================
import shutil

# ============================================================
# IMPORT CHILD-PROCESS SUPPORT.
# ============================================================
import subprocess

# ============================================================
# IMPORT PROCESS-EXIT SUPPORT.
# ============================================================
import sys

# ============================================================
# IMPORT DATA-CLASS SUPPORT.
# ============================================================
from dataclasses import asdict, dataclass

# ============================================================
# IMPORT UTC TIMESTAMP SUPPORT.
# ============================================================
from datetime import datetime, timezone

# ============================================================
# IMPORT PORTABLE FILESYSTEM-PATH SUPPORT.
# ============================================================
from pathlib import Path

# ============================================================
# IMPORT TYPE-ANNOTATION SUPPORT.
# ============================================================
from typing import Any, Final, Sequence


# ============================================================
# DECLARE THE UTILITY VERSION.
# ============================================================
UTILITY_VERSION: Final[str] = "0.1.0"

# ============================================================
# DECLARE THE EVIDENCE-SCHEMA VERSION.
# ============================================================
EVIDENCE_SCHEMA_VERSION: Final[str] = "1.0"

# ============================================================
# DECLARE THE AUTHORITATIVE AJAS REPOSITORY PATH.
# ============================================================
DEFAULT_REPOSITORY: Final[Path] = Path(r"C:\Users\steve\Code\AJAS")

# ============================================================
# DECLARE THE DEFAULT DOWNLOAD DIRECTORY.
# ============================================================
DEFAULT_DOWNLOADS: Final[Path] = Path.home() / "Downloads"

# ============================================================
# DECLARE THE EXPECTED BASELINE BRANCH.
# ============================================================
EXPECTED_BRANCH: Final[str] = "main"

# ============================================================
# DECLARE THE EXPECTED BASELINE COMMIT.
# ============================================================
EXPECTED_HEAD: Final[str] = "df08693da3157504d7f4a10dcb840969950bd184"

# ============================================================
# DECLARE THE EXPECTED BASELINE TAG.
# ============================================================
EXPECTED_BASELINE_TAG: Final[str] = "milestone0-complete"

# ============================================================
# DECLARE THE EXPECTED TRACKED-FILE COUNT.
# ============================================================
EXPECTED_TRACKED_FILE_COUNT: Final[int] = 93

# ============================================================
# DECLARE THE EXPECTED PRIVATE GITHUB REMOTE WITHOUT A SUFFIX.
# ============================================================
EXPECTED_REMOTE_URL: Final[str] = "https://github.com/stevearchuleta/AJAS"

# ============================================================
# DECLARE THE PLANNED PRESERVATION BRANCH.
# ============================================================
PROPOSED_BRANCH: Final[str] = "milestone1-preserve-ops-evidence"

# ============================================================
# DECLARE THE PLANNED POST-MERGE CHECKPOINT TAG.
# ============================================================
PROPOSED_TAG: Final[str] = "milestone1b-reconciliation-complete"

# ============================================================
# DECLARE THE PLANNED DISPOSABLE WORKTREE DIRECTORY NAME.
# ============================================================
PROPOSED_WORKTREE_DIRECTORY_NAME: Final[str] = "milestone1-preserve-ops-evidence"

# ============================================================
# DECLARE THE VERIFIED AZURE SUBSCRIPTION IDENTIFIER.
# ============================================================
EXPECTED_SUBSCRIPTION_ID: Final[str] = "efe2c2b2-d541-4b47-952d-e1af59db9910"

# ============================================================
# DECLARE THE VERIFIED COLD-CACHE WARNING NEEDLE.
# ============================================================
EXPECTED_WARNING_NEEDLE: Final[str] = "cannot import name 'load_capability_host'"

# ============================================================
# DECLARE THE VERIFIED RECONCILIATION EVIDENCE FILE NAME.
# ============================================================
RECONCILIATION_EVIDENCE_NAME: Final[str] = (
    "AJAS_M1_Reconciliation_20260904T174914819Z_v0_1_1.json"
)

# ============================================================
# DECLARE THE VERIFIED RECONCILIATION EVIDENCE SHA-256 DIGEST.
# ============================================================
RECONCILIATION_EVIDENCE_SHA256: Final[str] = (
    "7BA149D2F3A2392FA95340AC4EFE03F073B17A8A8099FCE194C89F576DAAB4A9"
)

# ============================================================
# DECLARE THE REQUIRED V0.1.2 SELF-TEST MARKERS.
# ============================================================
REQUIRED_V012_SELF_TEST_MARKERS: Final[tuple[str, ...]] = (
    "SELF_TEST_CONTAMINATED_AZURE_STDOUT=PASS",
    "SELF_TEST_CONTAMINATED_TSV_BOOLEAN=PASS",
    "SELF_TEST_CONTAMINATED_NONNEGATIVE_INTEGER=PASS",
    "SELF_TEST_SCALAR_AMBIGUITY_FAIL_CLOSED=PASS",
    "SELF_TEST_SCALAR_TRAILING_CONTAMINATION_FAIL_CLOSED=PASS",
    "SELF_TEST_JSON_TYPE_VALIDATION=PASS",
    "SELF_TEST_TRAILING_CONTAMINATION_FAIL_CLOSED=PASS",
    "AJAS_READ_ONLY_RECONCILIATION_SELF_TEST_v0.1.2=PASS",
)


# ============================================================
# STORE ONE REQUIRED SOURCE ARTIFACT SPECIFICATION.
# ============================================================
@dataclass(frozen=True)
class ArtifactSpec:
    """STORE ONE DOWNLOAD ARTIFACT AND THE EXPECTED FILE IDENTITY."""

    # ========================================================
    # STORE THE EXPECTED SOURCE FILE NAME.
    # ========================================================
    filename: str

    # ========================================================
    # STORE THE EXPECTED SHA-256 DIGEST.
    # ========================================================
    expected_sha256: str

    # ========================================================
    # STORE THE PLANNED REPOSITORY TARGET PATH.
    # ========================================================
    target_relative_path: str

    # ========================================================
    # STORE THE ARTIFACT CLASSIFICATION.
    # ========================================================
    artifact_type: str


# ============================================================
# DECLARE THE REQUIRED DOWNLOAD ARTIFACTS.
# ============================================================
REQUIRED_ARTIFACTS: Final[tuple[ArtifactSpec, ...]] = (
    ArtifactSpec(
        filename="ajas_m1_readonly_reconcile_v0_1_0.py",
        expected_sha256=(
            "FC904C72AE779776A45079319B43D87AA38F33770208EB7CCC245FDE7BEAF736"
        ),
        target_relative_path="scripts/ops/ajas_m1_readonly_reconcile_v0_1_0.py",
        artifact_type="PYTHON_UTILITY",
    ),
    ArtifactSpec(
        filename="ajas_m1_readonly_reconcile_v0_1_1.py",
        expected_sha256=(
            "C2BA5134107BE5F10B0E474289486FD94D3ADF1A5C8133E4D667A587DD50E4C4"
        ),
        target_relative_path="scripts/ops/ajas_m1_readonly_reconcile_v0_1_1.py",
        artifact_type="PYTHON_UTILITY",
    ),
    ArtifactSpec(
        filename="ajas_m1_readonly_reconcile_v0_1_2.py",
        expected_sha256=(
            "2ABFC081F41EE5D31494E9AE8A3D7CF7C037EC34BD6AACB0328D364D3D504815"
        ),
        target_relative_path="scripts/ops/ajas_m1_readonly_reconcile_v0_1_2.py",
        artifact_type="PYTHON_UTILITY",
    ),
    ArtifactSpec(
        filename=RECONCILIATION_EVIDENCE_NAME,
        expected_sha256=RECONCILIATION_EVIDENCE_SHA256,
        target_relative_path=(
            "ops/evidence/private/"
            "AJAS_M1_Reconciliation_20260904T174914819Z_v0_1_1.json"
        ),
        artifact_type="PRIVATE_MACHINE_EVIDENCE",
    ),
)

# ============================================================
# DECLARE THE STATIC GENERATED TARGET PATHS FOR THE LATER APPLY STEP.
# ============================================================
STATIC_GENERATED_TARGETS: Final[tuple[str, ...]] = (
    "scripts/ops/ajas_m1_preservation_preflight_v0_1_0.py",
    "ops/evidence/README.md",
    "ops/incidents/AJAS_INCIDENT_2026-09-03_POWERSHELL_NULL_WRAPPER.md",
    "ops/incidents/AJAS_INCIDENT_2026-09-04_AZURE_CLI_STDOUT_CONTAMINATION.md",
)

# ============================================================
# DECLARE HIGH-CONFIDENCE SECRET PATTERNS.
# ============================================================
HIGH_CONFIDENCE_SECRET_PATTERNS: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    (
        "PEM_PRIVATE_KEY",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "GITHUB_CLASSIC_TOKEN",
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    ),
    (
        "GITHUB_FINE_GRAINED_TOKEN",
        re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    ),
    (
        "AWS_ACCESS_KEY",
        re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    ),
    (
        "AZURE_STORAGE_ACCOUNT_KEY",
        re.compile(r"(?i)\bAccountKey\s*=\s*[A-Za-z0-9+/=]{20,}"),
    ),
    (
        "AZURE_SAS_SIGNATURE",
        re.compile(r"(?i)(?:[?&]|\b)sig=[A-Za-z0-9%+/=_-]{20,}"),
    ),
    (
        "JWT_BEARER_TOKEN",
        re.compile(
            r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"
        ),
    ),
    (
        "EXPLICIT_CLIENT_SECRET_VALUE",
        re.compile(
            r"(?i)\bclient[_-]?secret\b\s*[:=]\s*[\"']?[A-Za-z0-9._~+/-]{16,}"
        ),
    ),
)

# ============================================================
# DECLARE FORBIDDEN GIT MUTATION TOKENS FOR THIS READ-ONLY UTILITY.
# ============================================================
FORBIDDEN_GIT_MUTATION_TOKENS: Final[frozenset[str]] = frozenset(
    {
        "add",
        "am",
        "apply",
        "branch-create",
        "checkout",
        "cherry-pick",
        "clean",
        "commit",
        "fetch",
        "merge",
        "mv",
        "pull",
        "push",
        "rebase",
        "reset",
        "restore",
        "rm",
        "stash",
        "switch",
        "tag-create",
        "worktree-add",
        "worktree-remove",
    }
)


# ============================================================
# STORE ONE CHILD-PROCESS RECORD WITH SEPARATE OUTPUT STREAMS.
# ============================================================
@dataclass(frozen=True)
class CommandRecord:
    """STORE ONE READ-ONLY COMMAND INVOCATION."""

    # ========================================================
    # STORE A STABLE COMMAND LABEL.
    # ========================================================
    label: str

    # ========================================================
    # STORE THE HUMAN-READABLE COMMAND.
    # ========================================================
    logical_command: str

    # ========================================================
    # STORE THE PROCESS EXIT CODE.
    # ========================================================
    exit_code: int

    # ========================================================
    # STORE NORMALIZED STANDARD OUTPUT.
    # ========================================================
    stdout: str

    # ========================================================
    # STORE NORMALIZED STANDARD ERROR.
    # ========================================================
    stderr: str


# ============================================================
# STORE ONE SOURCE-ARTIFACT INSPECTION RESULT.
# ============================================================
@dataclass(frozen=True)
class ArtifactAudit:
    """STORE ONE DOWNLOAD ARTIFACT INTEGRITY AND SAFETY RESULT."""

    # ========================================================
    # STORE THE SOURCE FILE NAME.
    # ========================================================
    filename: str

    # ========================================================
    # STORE THE SOURCE FILE PATH.
    # ========================================================
    source_path: str

    # ========================================================
    # STORE THE PLANNED TARGET PATH.
    # ========================================================
    target_relative_path: str

    # ========================================================
    # STORE THE ARTIFACT CLASSIFICATION.
    # ========================================================
    artifact_type: str

    # ========================================================
    # STORE WHETHER THE SOURCE FILE EXISTS.
    # ========================================================
    exists: bool

    # ========================================================
    # STORE WHETHER THE SOURCE IS A REGULAR FILE.
    # ========================================================
    is_file: bool

    # ========================================================
    # STORE THE FILE BYTE COUNT WHEN KNOWN.
    # ========================================================
    bytes: int | None

    # ========================================================
    # STORE THE EXPECTED SHA-256 DIGEST.
    # ========================================================
    expected_sha256: str

    # ========================================================
    # STORE THE ACTUAL SHA-256 DIGEST WHEN KNOWN.
    # ========================================================
    actual_sha256: str | None

    # ========================================================
    # STORE WHETHER THE FILE IDENTITY MATCHES.
    # ========================================================
    hash_matches: bool

    # ========================================================
    # STORE THE HIGH-CONFIDENCE SECRET RULE NAMES.
    # ========================================================
    high_confidence_secret_rule_names: tuple[str, ...]

    # ========================================================
    # STORE WHETHER PRIVATE ACCOUNT OR LOCAL-PATH METADATA EXISTS.
    # ========================================================
    private_metadata_present: bool


# ============================================================
# STORE ONE TARGET-PATH INSPECTION RESULT.
# ============================================================
@dataclass(frozen=True)
class TargetAudit:
    """STORE ONE PLANNED REPOSITORY TARGET COLLISION AND IGNORE RESULT."""

    # ========================================================
    # STORE THE REPOSITORY-RELATIVE TARGET PATH.
    # ========================================================
    relative_path: str

    # ========================================================
    # STORE WHETHER THE TARGET ALREADY EXISTS.
    # ========================================================
    exists: bool

    # ========================================================
    # STORE THE GIT CHECK-IGNORE EXIT CODE.
    # ========================================================
    check_ignore_exit_code: int

    # ========================================================
    # STORE WHETHER AN IGNORE RULE MATCHED.
    # ========================================================
    ignored: bool | None

    # ========================================================
    # STORE THE MATCHING IGNORE RULE WITHOUT FILE CONTENT.
    # ========================================================
    ignore_rule: str | None


# ============================================================
# NORMALIZE A POSSIBLY MISSING PROCESS-OUTPUT VALUE.
# ============================================================
def normalize_text(value: str | bytes | None) -> str:
    """RETURN SAFE TEXT FOR PRESENT, BYTE, OR MISSING OUTPUT."""

    # ========================================================
    # RETURN AN EMPTY STRING FOR A MISSING VALUE.
    # ========================================================
    if value is None:
        return ""

    # ========================================================
    # DECODE BYTE OUTPUT WITH REPLACEMENT FOR INVALID BYTES.
    # ========================================================
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")

    # ========================================================
    # RETURN PRESENT TEXT WITHOUT MODIFICATION.
    # ========================================================
    return value


# ============================================================
# COMPUTE A FILE SHA-256 DIGEST.
# ============================================================
def sha256_file(path: Path) -> str:
    """RETURN AN UPPERCASE SHA-256 DIGEST FOR ONE REGULAR FILE."""

    # ========================================================
    # CREATE THE SHA-256 HASHER.
    # ========================================================
    digest = hashlib.sha256()

    # ========================================================
    # OPEN THE FILE IN BINARY READ MODE.
    # ========================================================
    with path.open("rb") as handle:
        # ====================================================
        # READ THE FILE IN BOUNDED CHUNKS.
        # ====================================================
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            # ================================================
            # ADD THE CURRENT CHUNK TO THE HASHER.
            # ================================================
            digest.update(chunk)

    # ========================================================
    # RETURN THE UPPERCASE FILE DIGEST.
    # ========================================================
    return digest.hexdigest().upper()


# ============================================================
# COMPUTE THE RUNNING SCRIPT SHA-256 DIGEST.
# ============================================================
def script_sha256() -> str:
    """RETURN THE RUNNING UTILITY SHA-256 DIGEST."""

    # ========================================================
    # HASH THE RESOLVED RUNNING SCRIPT PATH.
    # ========================================================
    return sha256_file(Path(__file__).resolve())


# ============================================================
# CONVERT A BOOLEAN OR MISSING VALUE TO A STABLE MARKER.
# ============================================================
def marker_bool(value: bool | None) -> str:
    """RETURN TRUE, FALSE, OR UNKNOWN AS A STABLE TEXT MARKER."""

    # ========================================================
    # RETURN UNKNOWN FOR A MISSING VALUE.
    # ========================================================
    if value is None:
        return "UNKNOWN"

    # ========================================================
    # RETURN TRUE FOR A TRUE VALUE.
    # ========================================================
    if value:
        return "True"

    # ========================================================
    # RETURN FALSE FOR A FALSE VALUE.
    # ========================================================
    return "False"


# ============================================================
# NORMALIZE A GITHUB HTTPS REMOTE FOR STABLE COMPARISON.
# ============================================================
def normalize_remote_url(value: str) -> str:
    """REMOVE A TRAILING SLASH OR DOT-GIT SUFFIX FOR COMPARISON."""

    # ========================================================
    # TRIM SURROUNDING WHITESPACE.
    # ========================================================
    normalized = value.strip().rstrip("/")

    # ========================================================
    # REMOVE A TRAILING DOT-GIT SUFFIX.
    # ========================================================
    if normalized.lower().endswith(".git"):
        normalized = normalized[:-4]

    # ========================================================
    # RETURN THE NORMALIZED REMOTE VALUE.
    # ========================================================
    return normalized


# ============================================================
# DETERMINE WHETHER ONE PATH LIVES INSIDE ANOTHER PATH.
# ============================================================
def path_is_within(child: Path, parent: Path) -> bool:
    """RETURN TRUE WHEN THE RESOLVED CHILD IS INSIDE THE RESOLVED PARENT."""

    # ========================================================
    # RESOLVE THE CANDIDATE CHILD PATH WITHOUT REQUIRING EXISTENCE.
    # ========================================================
    resolved_child = child.resolve(strict=False)

    # ========================================================
    # RESOLVE THE CANDIDATE PARENT PATH WITHOUT REQUIRING EXISTENCE.
    # ========================================================
    resolved_parent = parent.resolve(strict=False)

    # ========================================================
    # RETURN THE PORTABLE RELATIONSHIP RESULT.
    # ========================================================
    try:
        resolved_child.relative_to(resolved_parent)
        return True
    except ValueError:
        return False


# ============================================================
# RESOLVE A REQUIRED EXECUTABLE WITHOUT MUTATION.
# ============================================================
def resolve_executable(name: str) -> Path | None:
    """RETURN A RESOLVED EXECUTABLE PATH OR NONE."""

    # ========================================================
    # ASK THE CURRENT PATH TO LOCATE THE EXECUTABLE.
    # ========================================================
    resolved = shutil.which(name)

    # ========================================================
    # RETURN NONE WHEN DISCOVERY FAILS.
    # ========================================================
    if resolved is None:
        return None

    # ========================================================
    # RETURN THE RESOLVED EXECUTABLE PATH.
    # ========================================================
    return Path(resolved)


# ============================================================
# RUN ONE CHILD PROCESS WITH SEPARATE OUTPUT STREAMS.
# ============================================================
def run_command(
    label: str,
    executable: Path,
    arguments: Sequence[str],
    *,
    working_directory: Path | None = None,
    timeout_seconds: int = 120,
) -> CommandRecord:
    """RUN ONE FIXED READ-ONLY COMMAND AND RETURN A STRUCTURED RECORD."""

    # ========================================================
    # BUILD THE DIRECT OPERATING-SYSTEM ARGUMENT VECTOR.
    # ========================================================
    command = [str(executable), *arguments]

    # ========================================================
    # BUILD THE HUMAN-READABLE LOGICAL COMMAND.
    # ========================================================
    logical_command = subprocess.list2cmdline(command)

    # ========================================================
    # COPY THE CURRENT PROCESS ENVIRONMENT.
    # ========================================================
    child_environment = os.environ.copy()

    # ========================================================
    # DISABLE GIT TERMINAL PROMPTS FOR READ-ONLY COMMANDS.
    # ========================================================
    child_environment["GIT_TERMINAL_PROMPT"] = "0"

    # ========================================================
    # DISABLE GIT PAGERS FOR MACHINE-READABLE OUTPUT.
    # ========================================================
    child_environment["GIT_PAGER"] = "cat"

    # ========================================================
    # EXECUTE WITHOUT SHELL EXPANSION OR STREAM MERGING.
    # ========================================================
    try:
        completed = subprocess.run(
            command,
            cwd=(
                str(working_directory)
                if working_directory is not None
                else None
            ),
            env=child_environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            shell=False,
            timeout=timeout_seconds,
        )

    # ========================================================
    # CONVERT A PROCESS-LAUNCH FAILURE TO A STRUCTURED RECORD.
    # ========================================================
    except OSError as error:
        return CommandRecord(
            label=label,
            logical_command=logical_command,
            exit_code=126,
            stdout="",
            stderr=f"PROCESS_LAUNCH_ERROR={type(error).__name__}:{error}",
        )

    # ========================================================
    # CONVERT A TIMEOUT TO A STRUCTURED RECORD.
    # ========================================================
    except subprocess.TimeoutExpired as error:
        timeout_stdout = normalize_text(error.stdout).rstrip("\r\n")
        timeout_stderr = normalize_text(error.stderr).rstrip("\r\n")
        timeout_marker = f"PROCESS_TIMEOUT_SECONDS={timeout_seconds}"
        combined_stderr = (
            f"{timeout_stderr}\n{timeout_marker}"
            if timeout_stderr != ""
            else timeout_marker
        )
        return CommandRecord(
            label=label,
            logical_command=logical_command,
            exit_code=124,
            stdout=timeout_stdout,
            stderr=combined_stderr,
        )

    # ========================================================
    # NORMALIZE STANDARD OUTPUT WITHOUT CALLING METHODS ON NONE.
    # ========================================================
    normalized_stdout = normalize_text(completed.stdout).rstrip("\r\n")

    # ========================================================
    # NORMALIZE STANDARD ERROR WITHOUT CALLING METHODS ON NONE.
    # ========================================================
    normalized_stderr = normalize_text(completed.stderr).rstrip("\r\n")

    # ========================================================
    # RETURN THE IMMUTABLE COMMAND RECORD.
    # ========================================================
    return CommandRecord(
        label=label,
        logical_command=logical_command,
        exit_code=completed.returncode,
        stdout=normalized_stdout,
        stderr=normalized_stderr,
    )


# ============================================================
# READ ONE SUCCESSFUL SINGLE-LINE COMMAND VALUE.
# ============================================================
def successful_single_line(record: CommandRecord) -> str | None:
    """RETURN ONE NONEMPTY LINE OR NONE FOR FAILED OR AMBIGUOUS OUTPUT."""

    # ========================================================
    # REJECT A FAILED COMMAND.
    # ========================================================
    if record.exit_code != 0:
        return None

    # ========================================================
    # COLLECT NONEMPTY OUTPUT LINES.
    # ========================================================
    lines = [line.strip() for line in record.stdout.splitlines() if line.strip()]

    # ========================================================
    # REJECT EMPTY OR MULTILINE OUTPUT.
    # ========================================================
    if len(lines) != 1:
        return None

    # ========================================================
    # RETURN THE ONLY PRESENT LINE.
    # ========================================================
    return lines[0]


# ============================================================
# SCAN TEXT FOR HIGH-CONFIDENCE SECRET MATERIAL.
# ============================================================
def scan_high_confidence_secrets(text: str) -> tuple[str, ...]:
    """RETURN MATCHED RULE NAMES WITHOUT RETURNING SECRET VALUES."""

    # ========================================================
    # CREATE THE MATCHED-RULE COLLECTION.
    # ========================================================
    matched_rules: list[str] = []

    # ========================================================
    # TEST EVERY HIGH-CONFIDENCE SECRET RULE.
    # ========================================================
    for rule_name, pattern in HIGH_CONFIDENCE_SECRET_PATTERNS:
        # ====================================================
        # RECORD THE RULE NAME ON THE FIRST MATCH.
        # ====================================================
        if pattern.search(text) is not None:
            matched_rules.append(rule_name)

    # ========================================================
    # RETURN A STABLE DEDUPLICATED RULE-NAME TUPLE.
    # ========================================================
    return tuple(sorted(set(matched_rules)))


# ============================================================
# INSPECT ONE REQUIRED SOURCE ARTIFACT.
# ============================================================
def inspect_artifact(downloads: Path, spec: ArtifactSpec) -> ArtifactAudit:
    """VERIFY ONE DOWNLOAD ARTIFACT WITHOUT MODIFYING THE FILE."""

    # ========================================================
    # BUILD THE SOURCE FILE PATH.
    # ========================================================
    source_path = downloads / spec.filename

    # ========================================================
    # READ FILE EXISTENCE.
    # ========================================================
    exists = source_path.exists()

    # ========================================================
    # READ REGULAR-FILE STATUS.
    # ========================================================
    is_file = source_path.is_file()

    # ========================================================
    # INITIALIZE OPTIONAL FILE RESULTS.
    # ========================================================
    byte_count: int | None = None
    actual_sha256: str | None = None
    secret_rule_names: tuple[str, ...] = ()
    private_metadata_present = False

    # ========================================================
    # INSPECT FILE CONTENT ONLY FOR A REGULAR FILE.
    # ========================================================
    if is_file:
        # ====================================================
        # READ THE FILE BYTE COUNT.
        # ====================================================
        byte_count = source_path.stat().st_size

        # ====================================================
        # COMPUTE THE FILE SHA-256 DIGEST.
        # ====================================================
        actual_sha256 = sha256_file(source_path)

        # ====================================================
        # READ TEXT WITH REPLACEMENT FOR NON-UTF-8 BYTES.
        # ====================================================
        text = source_path.read_text(encoding="utf-8", errors="replace")

        # ====================================================
        # SCAN FOR HIGH-CONFIDENCE SECRET MATERIAL.
        # ====================================================
        secret_rule_names = scan_high_confidence_secrets(text)

        # ====================================================
        # CLASSIFY KNOWN ACCOUNT OR LOCAL-PATH METADATA.
        # ====================================================
        private_metadata_present = (
            EXPECTED_SUBSCRIPTION_ID.lower() in text.lower()
            or r"C:\Users\steve".lower() in text.lower()
        )

    # ========================================================
    # RETURN THE COMPLETE ARTIFACT AUDIT.
    # ========================================================
    return ArtifactAudit(
        filename=spec.filename,
        source_path=str(source_path),
        target_relative_path=spec.target_relative_path,
        artifact_type=spec.artifact_type,
        exists=exists,
        is_file=is_file,
        bytes=byte_count,
        expected_sha256=spec.expected_sha256,
        actual_sha256=actual_sha256,
        hash_matches=(
            actual_sha256 == spec.expected_sha256
            if actual_sha256 is not None
            else False
        ),
        high_confidence_secret_rule_names=secret_rule_names,
        private_metadata_present=private_metadata_present,
    )


# ============================================================
# VALIDATE THE VERIFIED V0.1.1 RECONCILIATION EVIDENCE CONTENT.
# ============================================================
def validate_reconciliation_evidence(path: Path) -> tuple[bool, dict[str, Any]]:
    """RETURN A FAIL-CLOSED CONTENT VALIDATION SUMMARY."""

    # ========================================================
    # CREATE THE DEFAULT VALIDATION SUMMARY.
    # ========================================================
    summary: dict[str, Any] = {
        "json_parse_status": "NOT_ATTEMPTED",
        "utility_version": None,
        "utility_script_sha256": None,
        "reconciliation_status": None,
        "local_git_clean": None,
        "azure_subscription_matches_handoff": None,
        "containerapp_extension_state": None,
        "containerapp_extension_version": None,
        "resource_group_exists": None,
        "container_registry_name_available": None,
        "account_json_parse_status": None,
        "account_warning_prefix_reproduced": None,
        "validation_errors": [],
    }

    # ========================================================
    # REJECT AN ABSENT OR NONFILE PATH.
    # ========================================================
    if not path.is_file():
        summary["json_parse_status"] = "SOURCE_FILE_ABSENT"
        summary["validation_errors"].append("SOURCE_FILE_ABSENT")
        return False, summary

    # ========================================================
    # PARSE THE JSON DOCUMENT.
    # ========================================================
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        summary["json_parse_status"] = "JSON_PARSE_FAILED"
        summary["validation_errors"].append(
            f"JSON_PARSE_FAILED:{type(error).__name__}"
        )
        return False, summary

    # ========================================================
    # REQUIRE A DICTIONARY TOP-LEVEL VALUE.
    # ========================================================
    if not isinstance(payload, dict):
        summary["json_parse_status"] = "TOP_LEVEL_TYPE_INVALID"
        summary["validation_errors"].append("TOP_LEVEL_TYPE_INVALID")
        return False, summary

    # ========================================================
    # RECORD SUCCESSFUL TOP-LEVEL JSON PARSING.
    # ========================================================
    summary["json_parse_status"] = "PARSED"

    # ========================================================
    # READ THE UTILITY OBJECT FAIL CLOSED.
    # ========================================================
    utility = payload.get("utility")
    if not isinstance(utility, dict):
        summary["validation_errors"].append("UTILITY_OBJECT_ABSENT")
        utility = {}

    # ========================================================
    # READ THE RECONCILED-STATE OBJECT FAIL CLOSED.
    # ========================================================
    state = payload.get("reconciled_state")
    if not isinstance(state, dict):
        summary["validation_errors"].append("RECONCILED_STATE_OBJECT_ABSENT")
        state = {}

    # ========================================================
    # READ THE COMMAND COLLECTION FAIL CLOSED.
    # ========================================================
    commands = payload.get("commands")
    if not isinstance(commands, list):
        summary["validation_errors"].append("COMMANDS_COLLECTION_ABSENT")
        commands = []

    # ========================================================
    # EXTRACT THE EXPECTED UTILITY FIELDS.
    # ========================================================
    summary["utility_version"] = utility.get("version")
    summary["utility_script_sha256"] = utility.get("script_sha256")

    # ========================================================
    # EXTRACT THE EXPECTED RECONCILIATION FIELDS.
    # ========================================================
    summary["reconciliation_status"] = state.get("reconciliation_status")
    summary["local_git_clean"] = state.get("local_git_clean")
    summary["azure_subscription_matches_handoff"] = state.get(
        "azure_subscription_matches_handoff"
    )
    summary["containerapp_extension_state"] = state.get(
        "containerapp_extension_state"
    )
    summary["containerapp_extension_version"] = state.get(
        "containerapp_extension_version"
    )
    summary["resource_group_exists"] = state.get("resource_group_exists")
    summary["container_registry_name_available"] = state.get(
        "container_registry_name_available"
    )

    # ========================================================
    # LOCATE THE SINGLE AZURE ACCOUNT COMMAND RECORD.
    # ========================================================
    account_records = [
        command
        for command in commands
        if isinstance(command, dict)
        and command.get("label") == "AZURE_ACCOUNT_SHOW"
    ]

    # ========================================================
    # REQUIRE EXACTLY ONE AZURE ACCOUNT COMMAND RECORD.
    # ========================================================
    if len(account_records) != 1:
        summary["validation_errors"].append(
            f"AZURE_ACCOUNT_RECORD_COUNT_INVALID:{len(account_records)}"
        )
        account_audit: dict[str, Any] = {}
    else:
        # ====================================================
        # READ THE AZURE ACCOUNT JSON PARSER AUDIT.
        # ====================================================
        candidate_audit = account_records[0].get("json_parse_audit")
        account_audit = candidate_audit if isinstance(candidate_audit, dict) else {}
        if not account_audit:
            summary["validation_errors"].append(
                "AZURE_ACCOUNT_JSON_PARSE_AUDIT_ABSENT"
            )

    # ========================================================
    # READ THE AZURE ACCOUNT PARSER STATUS.
    # ========================================================
    summary["account_json_parse_status"] = account_audit.get("status")

    # ========================================================
    # READ THE DISCARDED AZURE ACCOUNT PREFIX SAFELY.
    # ========================================================
    prefix_value = account_audit.get("stdout_prefix_discarded")
    prefix_text = prefix_value if isinstance(prefix_value, str) else ""

    # ========================================================
    # RECORD WHETHER THE EXACT INCIDENT WARNING WAS PRESENT.
    # ========================================================
    summary["account_warning_prefix_reproduced"] = (
        EXPECTED_WARNING_NEEDLE in prefix_text
    )

    # ========================================================
    # DECLARE THE REQUIRED FIELD EXPECTATIONS.
    # ========================================================
    expected_checks: tuple[tuple[str, Any, Any], ...] = (
        ("UTILITY_VERSION", summary["utility_version"], "0.1.1"),
        (
            "UTILITY_SCRIPT_SHA256",
            summary["utility_script_sha256"],
            REQUIRED_ARTIFACTS[1].expected_sha256,
        ),
        (
            "RECONCILIATION_STATUS",
            summary["reconciliation_status"],
            "COMPLETE_BASELINE_CONFIRMED",
        ),
        ("LOCAL_GIT_CLEAN", summary["local_git_clean"], True),
        (
            "AZURE_SUBSCRIPTION_MATCHES_HANDOFF",
            summary["azure_subscription_matches_handoff"],
            True,
        ),
        (
            "CONTAINERAPP_EXTENSION_STATE",
            summary["containerapp_extension_state"],
            "INSTALLED",
        ),
        (
            "CONTAINERAPP_EXTENSION_VERSION",
            summary["containerapp_extension_version"],
            "1.3.0b5",
        ),
        ("RESOURCE_GROUP_EXISTS", summary["resource_group_exists"], False),
        (
            "CONTAINER_REGISTRY_NAME_AVAILABLE",
            summary["container_registry_name_available"],
            True,
        ),
        (
            "ACCOUNT_JSON_PARSE_STATUS",
            summary["account_json_parse_status"],
            "PARSED_WITH_PREFIX",
        ),
        (
            "ACCOUNT_WARNING_PREFIX_REPRODUCED",
            summary["account_warning_prefix_reproduced"],
            True,
        ),
    )

    # ========================================================
    # RECORD EVERY FIELD MISMATCH WITHOUT HIDING OTHER ERRORS.
    # ========================================================
    for field_name, actual_value, expected_value in expected_checks:
        if actual_value != expected_value:
            summary["validation_errors"].append(
                f"{field_name}_MISMATCH"
            )

    # ========================================================
    # RETURN SUCCESS ONLY WHEN EVERY REQUIRED CHECK PASSES.
    # ========================================================
    return len(summary["validation_errors"]) == 0, summary


# ============================================================
# PRINT ONE ARTIFACT-AUDIT SUMMARY LINE.
# ============================================================
def print_artifact_audit(audit: ArtifactAudit) -> None:
    """PRINT ONE COMPACT ARTIFACT INTEGRITY SUMMARY."""

    # ========================================================
    # RENDER THE OPTIONAL ACTUAL DIGEST.
    # ========================================================
    digest_marker = audit.actual_sha256 or "UNKNOWN"

    # ========================================================
    # RENDER THE OPTIONAL BYTE COUNT.
    # ========================================================
    byte_marker = str(audit.bytes) if audit.bytes is not None else "UNKNOWN"

    # ========================================================
    # RENDER SECRET-RULE NAMES WITHOUT SECRET VALUES.
    # ========================================================
    secret_marker = (
        ",".join(audit.high_confidence_secret_rule_names)
        if audit.high_confidence_secret_rule_names
        else "NONE"
    )

    # ========================================================
    # PRINT THE STABLE PIPE-DELIMITED SUMMARY.
    # ========================================================
    print(
        "ARTIFACT_AUDIT="
        f"{audit.filename}"
        f"|TYPE={audit.artifact_type}"
        f"|EXISTS={marker_bool(audit.exists)}"
        f"|IS_FILE={marker_bool(audit.is_file)}"
        f"|BYTES={byte_marker}"
        f"|SHA256={digest_marker}"
        f"|HASH_MATCH={marker_bool(audit.hash_matches)}"
        f"|HIGH_CONFIDENCE_SECRET_RULES={secret_marker}"
        f"|PRIVATE_METADATA_PRESENT={marker_bool(audit.private_metadata_present)}"
    )


# ============================================================
# PRINT ONE TARGET-AUDIT SUMMARY LINE.
# ============================================================
def print_target_audit(audit: TargetAudit) -> None:
    """PRINT ONE COMPACT TARGET COLLISION AND IGNORE SUMMARY."""

    # ========================================================
    # RENDER THE OPTIONAL IGNORE RULE.
    # ========================================================
    ignore_rule_marker = audit.ignore_rule or "NONE"

    # ========================================================
    # PRINT THE STABLE PIPE-DELIMITED SUMMARY.
    # ========================================================
    print(
        "TARGET_AUDIT="
        f"{audit.relative_path}"
        f"|EXISTS={marker_bool(audit.exists)}"
        f"|IGNORED={marker_bool(audit.ignored)}"
        f"|CHECK_IGNORE_EXIT_CODE={audit.check_ignore_exit_code}"
        f"|IGNORE_RULE={json.dumps(ignore_rule_marker)}"
    )


# ============================================================
# WRITE ONE IMMUTABLE JSON EVIDENCE FILE.
# ============================================================
def write_json_exclusive(path: Path, payload: dict[str, Any]) -> str:
    """WRITE JSON WITH EXCLUSIVE CREATION AND RETURN THE FILE SHA-256."""

    # ========================================================
    # REQUIRE AN EXISTING PARENT DIRECTORY.
    # ========================================================
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"JSON_OUTPUT_PARENT_NOT_FOUND:{path.parent}"
        )

    # ========================================================
    # SERIALIZE THE COMPLETE PAYLOAD DETERMINISTICALLY.
    # ========================================================
    serialized = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    ) + "\n"

    # ========================================================
    # OPEN THE OUTPUT WITH EXCLUSIVE CREATION.
    # ========================================================
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        # ====================================================
        # WRITE THE SERIALIZED EVIDENCE.
        # ====================================================
        handle.write(serialized)

    # ========================================================
    # RETURN THE WRITTEN FILE SHA-256 DIGEST.
    # ========================================================
    return sha256_file(path)


# ============================================================
# RUN PURE IN-PROCESS REGRESSION TESTS.
# ============================================================
def run_self_test() -> int:
    """VERIFY CORE PARSERS, SCANNERS, AND FAIL-CLOSED HELPERS."""

    # ========================================================
    # VERIFY MISSING TEXT NORMALIZATION.
    # ========================================================
    assert normalize_text(None) == ""

    # ========================================================
    # VERIFY BYTE TEXT NORMALIZATION.
    # ========================================================
    assert normalize_text(b"abc") == "abc"

    # ========================================================
    # VERIFY REMOTE URL NORMALIZATION.
    # ========================================================
    assert (
        normalize_remote_url("https://github.com/stevearchuleta/AJAS.git/")
        == EXPECTED_REMOTE_URL
    )

    # ========================================================
    # VERIFY A SAFE POLICY SENTENCE DOES NOT TRIGGER A SECRET RULE.
    # ========================================================
    assert scan_high_confidence_secrets(
        "No client secret, password, or publish profile is allowed."
    ) == ()

    # ========================================================
    # VERIFY A SYNTHETIC PRIVATE-KEY HEADER TRIGGERS THE CORRECT RULE.
    # ========================================================
    synthetic_private_key_header = (
        "-----BEGIN " + "PRIVATE KEY-----"
    )
    assert "PEM_PRIVATE_KEY" in scan_high_confidence_secrets(
        synthetic_private_key_header
    )

    # ========================================================
    # VERIFY A SYNTHETIC GITHUB TOKEN TRIGGERS WITHOUT EXPOSING A REAL TOKEN.
    # ========================================================
    synthetic_token = "ghp_" + ("A" * 36)
    assert "GITHUB_CLASSIC_TOKEN" in scan_high_confidence_secrets(
        synthetic_token
    )

    # ========================================================
    # VERIFY PATH-CONTAINMENT LOGIC.
    # ========================================================
    synthetic_parent = Path.cwd() / "parent"
    synthetic_child = synthetic_parent / "child" / "file.json"
    assert path_is_within(synthetic_child, synthetic_parent) is True

    # ========================================================
    # VERIFY PATH-NONCONTAINMENT LOGIC.
    # ========================================================
    synthetic_outside = Path.cwd() / "outside" / "file.json"
    assert path_is_within(synthetic_outside, synthetic_parent) is False

    # ========================================================
    # VERIFY THE UTILITY DECLARES NO FORBIDDEN GIT MUTATION PLAN.
    # ========================================================
    planned_read_only_verbs = {
        "rev-parse",
        "branch-list",
        "tag-list",
        "status",
        "ls-files",
        "remote-get-url",
        "config-get",
        "worktree-list",
        "check-ignore",
    }
    assert planned_read_only_verbs.isdisjoint(FORBIDDEN_GIT_MUTATION_TOKENS)

    # ========================================================
    # PRINT THE STABLE SELF-TEST SUCCESS MARKERS.
    # ========================================================
    print("SELF_TEST_NULL_NORMALIZATION=PASS")
    print("SELF_TEST_REMOTE_NORMALIZATION=PASS")
    print("SELF_TEST_SECRET_SCANNER=PASS")
    print("SELF_TEST_PATH_CONTAINMENT=PASS")
    print("SELF_TEST_GIT_READ_ONLY_VERB_AUDIT=PASS")
    print(f"AJAS_M1_PRESERVATION_PREFLIGHT_SELF_TEST_v{UTILITY_VERSION}=PASS")

    # ========================================================
    # RETURN A SUCCESS PROCESS EXIT CODE.
    # ========================================================
    return 0


# ============================================================
# RUN THE COMPLETE READ-ONLY PRESERVATION PREFLIGHT.
# ============================================================
def inspect_preservation_readiness(
    repository: Path,
    downloads: Path,
    json_output: Path | None,
) -> int:
    """VERIFY PRESERVATION READINESS WITHOUT MUTATING THE REPOSITORY."""

    # ========================================================
    # CAPTURE THE UTC RUN START TIME.
    # ========================================================
    run_utc = datetime.now(timezone.utc).isoformat()

    # ========================================================
    # CAPTURE THE RUNNING UTILITY IDENTITY.
    # ========================================================
    utility_digest = script_sha256()

    # ========================================================
    # RESOLVE INPUT PATHS WITHOUT REQUIRING EXISTENCE.
    # ========================================================
    repository = repository.resolve(strict=False)
    downloads = downloads.resolve(strict=False)

    # ========================================================
    # RESOLVE THE OPTIONAL OUTPUT PATH WITHOUT REQUIRING EXISTENCE.
    # ========================================================
    if json_output is not None:
        json_output = json_output.resolve(strict=False)

    # ========================================================
    # PRINT THE STRUCTURED HEADER.
    # ========================================================
    print(
        f"===== BEGIN AJAS M1 PRESERVATION PREFLIGHT v{UTILITY_VERSION} ====="
    )

    # ========================================================
    # PRINT THE RUN IDENTITY AND SAFETY MARKERS.
    # ========================================================
    print(f"RUN_UTC={run_utc}")
    print(f"UTILITY_VERSION={UTILITY_VERSION}")
    print(f"SCRIPT_SHA256={utility_digest}")
    print("MODE=INSPECT")
    print("GIT_MUTATIONS_ATTEMPTED=False")
    print("REPOSITORY_FILES_WRITTEN=False")
    print("AZURE_COMMANDS_ATTEMPTED=False")
    print("GITHUB_NETWORK_COMMANDS_ATTEMPTED=False")
    print("BILLABLE_RESOURCES_CREATED=False")

    # ========================================================
    # REJECT A JSON OUTPUT PATH INSIDE THE REPOSITORY.
    # ========================================================
    output_path_outside_repository = (
        True
        if json_output is None
        else not path_is_within(json_output, repository)
    )

    # ========================================================
    # INITIALIZE COMMAND, ARTIFACT, AND TARGET AUDIT COLLECTIONS.
    # ========================================================
    command_records: list[CommandRecord] = []
    artifact_audits: list[ArtifactAudit] = []
    target_audits: list[TargetAudit] = []

    # ========================================================
    # READ BASIC DIRECTORY STATE.
    # ========================================================
    repository_exists = repository.is_dir()
    downloads_exists = downloads.is_dir()

    # ========================================================
    # RESOLVE THE GIT EXECUTABLE.
    # ========================================================
    git_executable = resolve_executable("git")

    # ========================================================
    # INITIALIZE GIT STATE FIELDS.
    # ========================================================
    git_worktree: bool | None = None
    git_root: str | None = None
    git_branch: str | None = None
    git_head: str | None = None
    git_clean: bool | None = None
    baseline_tag_target: str | None = None
    tracked_file_count: int | None = None
    remote_url: str | None = None
    remote_matches: bool | None = None
    git_user_name_present: bool | None = None
    git_user_email_present: bool | None = None
    proposed_branch_exists: bool | None = None
    proposed_tag_exists: bool | None = None
    worktree_list_readable: bool | None = None
    proposed_worktree_registered: bool | None = None

    # ========================================================
    # BUILD THE PLANNED DISPOSABLE WORKTREE PATH.
    # ========================================================
    proposed_worktree_path = (
        repository.parent
        / f"{repository.name}-worktrees"
        / PROPOSED_WORKTREE_DIRECTORY_NAME
    )

    # ========================================================
    # READ WHETHER THE PROPOSED WORKTREE PATH ALREADY EXISTS.
    # ========================================================
    proposed_worktree_path_exists = proposed_worktree_path.exists()

    # ========================================================
    # COLLECT READ-ONLY GIT STATE WHEN PREREQUISITES EXIST.
    # ========================================================
    if repository_exists and git_executable is not None:
        # ====================================================
        # CONFIRM THE DIRECTORY IS A GIT WORKTREE.
        # ====================================================
        worktree_record = run_command(
            "GIT_WORKTREE",
            git_executable,
            ["-C", str(repository), "rev-parse", "--is-inside-work-tree"],
        )
        command_records.append(worktree_record)
        worktree_value = successful_single_line(worktree_record)
        git_worktree = (
            worktree_value.lower() == "true"
            if worktree_value is not None
            else None
        )

        # ====================================================
        # READ THE CANONICAL REPOSITORY ROOT.
        # ====================================================
        root_record = run_command(
            "GIT_ROOT",
            git_executable,
            ["-C", str(repository), "rev-parse", "--show-toplevel"],
        )
        command_records.append(root_record)
        git_root = successful_single_line(root_record)

        # ====================================================
        # READ THE CURRENT BRANCH.
        # ====================================================
        branch_record = run_command(
            "GIT_BRANCH",
            git_executable,
            ["-C", str(repository), "branch", "--show-current"],
        )
        command_records.append(branch_record)
        git_branch = successful_single_line(branch_record)

        # ====================================================
        # READ THE CURRENT HEAD COMMIT.
        # ====================================================
        head_record = run_command(
            "GIT_HEAD",
            git_executable,
            ["-C", str(repository), "rev-parse", "HEAD"],
        )
        command_records.append(head_record)
        head_value = successful_single_line(head_record)
        git_head = head_value.lower() if head_value is not None else None

        # ====================================================
        # READ TRACKED AND UNTRACKED WORKTREE DRIFT.
        # ====================================================
        status_record = run_command(
            "GIT_STATUS",
            git_executable,
            [
                "-C",
                str(repository),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
        )
        command_records.append(status_record)
        git_clean = (
            status_record.stdout == ""
            if status_record.exit_code == 0
            else None
        )

        # ====================================================
        # READ THE MILESTONE-0 TAG TARGET.
        # ====================================================
        tag_target_record = run_command(
            "GIT_BASELINE_TAG_TARGET",
            git_executable,
            [
                "-C",
                str(repository),
                "rev-list",
                "-n",
                "1",
                EXPECTED_BASELINE_TAG,
            ],
        )
        command_records.append(tag_target_record)
        tag_target_value = successful_single_line(tag_target_record)
        baseline_tag_target = (
            tag_target_value.lower()
            if tag_target_value is not None
            else None
        )

        # ====================================================
        # READ THE COMPLETE TRACKED-FILE MANIFEST.
        # ====================================================
        tracked_record = run_command(
            "GIT_TRACKED_FILES",
            git_executable,
            ["-C", str(repository), "ls-files"],
        )
        command_records.append(tracked_record)
        if tracked_record.exit_code == 0:
            tracked_file_count = len(
                [line for line in tracked_record.stdout.splitlines() if line]
            )

        # ====================================================
        # READ THE ORIGIN REMOTE URL.
        # ====================================================
        remote_record = run_command(
            "GIT_ORIGIN_REMOTE",
            git_executable,
            ["-C", str(repository), "remote", "get-url", "origin"],
        )
        command_records.append(remote_record)
        remote_url = successful_single_line(remote_record)
        remote_matches = (
            normalize_remote_url(remote_url).lower()
            == EXPECTED_REMOTE_URL.lower()
            if remote_url is not None
            else None
        )

        # ====================================================
        # READ THE CONFIGURED GIT AUTHOR NAME.
        # ====================================================
        user_name_record = run_command(
            "GIT_USER_NAME",
            git_executable,
            ["-C", str(repository), "config", "--get", "user.name"],
        )
        command_records.append(user_name_record)
        user_name_value = successful_single_line(user_name_record)
        git_user_name_present = (
            bool(user_name_value)
            if user_name_record.exit_code == 0
            else False
        )

        # ====================================================
        # READ THE CONFIGURED GIT AUTHOR EMAIL.
        # ====================================================
        user_email_record = run_command(
            "GIT_USER_EMAIL",
            git_executable,
            ["-C", str(repository), "config", "--get", "user.email"],
        )
        command_records.append(user_email_record)
        user_email_value = successful_single_line(user_email_record)
        git_user_email_present = (
            bool(user_email_value)
            if user_email_record.exit_code == 0
            else False
        )

        # ====================================================
        # READ WHETHER THE PLANNED BRANCH ALREADY EXISTS.
        # ====================================================
        proposed_branch_record = run_command(
            "GIT_PROPOSED_BRANCH",
            git_executable,
            [
                "-C",
                str(repository),
                "branch",
                "--list",
                PROPOSED_BRANCH,
            ],
        )
        command_records.append(proposed_branch_record)
        proposed_branch_exists = (
            proposed_branch_record.stdout.strip() != ""
            if proposed_branch_record.exit_code == 0
            else None
        )

        # ====================================================
        # READ WHETHER THE PLANNED TAG ALREADY EXISTS.
        # ====================================================
        proposed_tag_record = run_command(
            "GIT_PROPOSED_TAG",
            git_executable,
            [
                "-C",
                str(repository),
                "tag",
                "--list",
                PROPOSED_TAG,
            ],
        )
        command_records.append(proposed_tag_record)
        proposed_tag_exists = (
            proposed_tag_record.stdout.strip() != ""
            if proposed_tag_record.exit_code == 0
            else None
        )

        # ====================================================
        # READ ALL REGISTERED WORKTREES.
        # ====================================================
        worktree_list_record = run_command(
            "GIT_WORKTREE_LIST",
            git_executable,
            ["-C", str(repository), "worktree", "list", "--porcelain"],
        )
        command_records.append(worktree_list_record)
        worktree_list_readable = worktree_list_record.exit_code == 0
        proposed_worktree_registered = (
            str(proposed_worktree_path).lower()
            in worktree_list_record.stdout.lower()
            if worktree_list_readable
            else None
        )

    # ========================================================
    # INSPECT EVERY REQUIRED DOWNLOAD ARTIFACT.
    # ========================================================
    if downloads_exists:
        for artifact_spec in REQUIRED_ARTIFACTS:
            artifact_audits.append(
                inspect_artifact(downloads, artifact_spec)
            )

    # ========================================================
    # BUILD THE DYNAMIC PREFLIGHT-EVIDENCE TARGET PATH.
    # ========================================================
    dynamic_output_target: str | None = None
    if json_output is not None:
        dynamic_output_target = (
            "ops/evidence/private/" + json_output.name
        )

    # ========================================================
    # BUILD THE COMPLETE PLANNED TARGET PATH COLLECTION.
    # ========================================================
    planned_target_paths = [
        artifact.target_relative_path for artifact in REQUIRED_ARTIFACTS
    ]
    planned_target_paths.extend(STATIC_GENERATED_TARGETS)
    if dynamic_output_target is not None:
        planned_target_paths.append(dynamic_output_target)

    # ========================================================
    # CHECK TARGET COLLISIONS AND IGNORE RULES.
    # ========================================================
    if repository_exists and git_executable is not None:
        for target_relative_path in planned_target_paths:
            # ================================================
            # READ WHETHER THE PLANNED TARGET ALREADY EXISTS.
            # ================================================
            target_exists = (repository / target_relative_path).exists()

            # ================================================
            # ASK GIT WHETHER AN IGNORE RULE MATCHES THE TARGET.
            # ================================================
            ignore_record = run_command(
                "GIT_CHECK_IGNORE_" + re.sub(
                    r"[^A-Za-z0-9]+",
                    "_",
                    target_relative_path,
                ).strip("_").upper(),
                git_executable,
                [
                    "-C",
                    str(repository),
                    "check-ignore",
                    "--no-index",
                    "-v",
                    "--",
                    target_relative_path,
                ],
            )
            command_records.append(ignore_record)

            # ================================================
            # PARSE THE DOCUMENTED CHECK-IGNORE EXIT CODES.
            # ================================================
            if ignore_record.exit_code == 0:
                ignored: bool | None = True
                ignore_rule = ignore_record.stdout.strip() or None
            elif ignore_record.exit_code == 1:
                ignored = False
                ignore_rule = None
            else:
                ignored = None
                ignore_rule = None

            # ================================================
            # STORE THE TARGET AUDIT.
            # ================================================
            target_audits.append(
                TargetAudit(
                    relative_path=target_relative_path,
                    exists=target_exists,
                    check_ignore_exit_code=ignore_record.exit_code,
                    ignored=ignored,
                    ignore_rule=ignore_rule,
                )
            )

    # ========================================================
    # LOCATE THE VERIFIED V0.1.1 EVIDENCE SOURCE PATH.
    # ========================================================
    reconciliation_evidence_path = downloads / RECONCILIATION_EVIDENCE_NAME

    # ========================================================
    # VALIDATE THE VERIFIED V0.1.1 EVIDENCE CONTENT.
    # ========================================================
    evidence_content_valid, evidence_content_summary = (
        validate_reconciliation_evidence(reconciliation_evidence_path)
    )

    # ========================================================
    # LOCATE THE VERIFIED V0.1.2 UTILITY SOURCE PATH.
    # ========================================================
    v012_path = downloads / "ajas_m1_readonly_reconcile_v0_1_2.py"

    # ========================================================
    # RUN THE V0.1.2 IN-PROCESS REGRESSION TESTS.
    # ========================================================
    v012_self_test_record: CommandRecord | None = None
    if v012_path.is_file():
        v012_self_test_record = run_command(
            "V0_1_2_SELF_TEST",
            Path(sys.executable),
            [str(v012_path), "--mode", "self-test"],
            timeout_seconds=120,
        )
        command_records.append(v012_self_test_record)

    # ========================================================
    # DETERMINE WHETHER EVERY REQUIRED SELF-TEST MARKER EXISTS.
    # ========================================================
    v012_self_test_markers_present = (
        v012_self_test_record is not None
        and v012_self_test_record.exit_code == 0
        and all(
            marker in v012_self_test_record.stdout
            for marker in REQUIRED_V012_SELF_TEST_MARKERS
        )
    )

    # ========================================================
    # CALCULATE ARTIFACT AND TARGET SUMMARY COUNTS.
    # ========================================================
    missing_artifact_count = sum(
        1 for audit in artifact_audits if not audit.is_file
    )
    artifact_hash_mismatch_count = sum(
        1 for audit in artifact_audits if not audit.hash_matches
    )
    high_confidence_secret_finding_count = sum(
        len(audit.high_confidence_secret_rule_names)
        for audit in artifact_audits
    )
    private_metadata_artifact_count = sum(
        1 for audit in artifact_audits if audit.private_metadata_present
    )
    target_collision_count = sum(1 for audit in target_audits if audit.exists)
    target_ignore_match_count = sum(
        1 for audit in target_audits if audit.ignored is True
    )
    target_ignore_unknown_count = sum(
        1 for audit in target_audits if audit.ignored is None
    )

    # ========================================================
    # COMPARE THE LIVE REPOSITORY ROOT WITH THE REQUESTED ROOT.
    # ========================================================
    git_root_matches = (
        Path(git_root).resolve(strict=False) == repository
        if git_root is not None
        else None
    )

    # ========================================================
    # DETERMINE THE COMPLETE GIT BASELINE GATE.
    # ========================================================
    git_baseline_passes = all(
        [
            repository_exists,
            git_executable is not None,
            git_worktree is True,
            git_root_matches is True,
            git_branch == EXPECTED_BRANCH,
            git_head == EXPECTED_HEAD,
            git_clean is True,
            baseline_tag_target == EXPECTED_HEAD,
            tracked_file_count == EXPECTED_TRACKED_FILE_COUNT,
            remote_matches is True,
            git_user_name_present is True,
            git_user_email_present is True,
            proposed_branch_exists is False,
            proposed_tag_exists is False,
            worktree_list_readable is True,
            proposed_worktree_registered is False,
            proposed_worktree_path_exists is False,
        ]
    )

    # ========================================================
    # DETERMINE THE COMPLETE ARTIFACT GATE.
    # ========================================================
    artifact_gate_passes = all(
        [
            downloads_exists,
            len(artifact_audits) == len(REQUIRED_ARTIFACTS),
            missing_artifact_count == 0,
            artifact_hash_mismatch_count == 0,
            high_confidence_secret_finding_count == 0,
            evidence_content_valid,
            v012_self_test_markers_present,
        ]
    )

    # ========================================================
    # DETERMINE THE COMPLETE TARGET GATE.
    # ========================================================
    target_gate_passes = all(
        [
            len(target_audits) == len(planned_target_paths),
            target_collision_count == 0,
            target_ignore_match_count == 0,
            target_ignore_unknown_count == 0,
            output_path_outside_repository,
        ]
    )

    # ========================================================
    # DETERMINE THE FINAL PRESERVATION READINESS RESULT.
    # ========================================================
    preservation_ready = all(
        [
            git_baseline_passes,
            artifact_gate_passes,
            target_gate_passes,
        ]
    )

    # ========================================================
    # BUILD THE MACHINE-READABLE PREFLIGHT EVIDENCE PAYLOAD.
    # ========================================================
    evidence_payload: dict[str, Any] = {
        "evidence_schema_version": EVIDENCE_SCHEMA_VERSION,
        "run_utc": run_utc,
        "utility": {
            "name": "ajas_m1_preservation_preflight",
            "version": UTILITY_VERSION,
            "script_sha256": utility_digest,
            "mode": "inspect",
        },
        "safety": {
            "git_mutations_attempted": False,
            "repository_files_written": False,
            "azure_commands_attempted": False,
            "github_network_commands_attempted": False,
            "billable_resources_created": False,
            "json_output_outside_repository": output_path_outside_repository,
        },
        "plan": {
            "proposed_branch": PROPOSED_BRANCH,
            "proposed_tag": PROPOSED_TAG,
            "proposed_worktree_path": str(proposed_worktree_path),
            "planned_target_paths": planned_target_paths,
            "private_repository_required": True,
            "remote_push_deferred": True,
        },
        "git_state": {
            "repository": str(repository),
            "repository_exists": repository_exists,
            "git_executable": (
                str(git_executable) if git_executable is not None else None
            ),
            "git_worktree": git_worktree,
            "git_root": git_root,
            "git_root_matches": git_root_matches,
            "branch": git_branch,
            "head": git_head,
            "clean": git_clean,
            "baseline_tag": EXPECTED_BASELINE_TAG,
            "baseline_tag_target": baseline_tag_target,
            "tracked_file_count": tracked_file_count,
            "origin_remote": remote_url,
            "origin_remote_matches": remote_matches,
            "git_user_name_present": git_user_name_present,
            "git_user_email_present": git_user_email_present,
            "proposed_branch_exists": proposed_branch_exists,
            "proposed_tag_exists": proposed_tag_exists,
            "proposed_worktree_registered": proposed_worktree_registered,
            "proposed_worktree_path_exists": proposed_worktree_path_exists,
            "git_baseline_passes": git_baseline_passes,
        },
        "artifact_audits": [asdict(audit) for audit in artifact_audits],
        "target_audits": [asdict(audit) for audit in target_audits],
        "reconciliation_evidence_validation": {
            "valid": evidence_content_valid,
            **evidence_content_summary,
        },
        "v0_1_2_self_test": (
            asdict(v012_self_test_record)
            if v012_self_test_record is not None
            else None
        ),
        "summary": {
            "missing_artifact_count": missing_artifact_count,
            "artifact_hash_mismatch_count": artifact_hash_mismatch_count,
            "high_confidence_secret_finding_count": (
                high_confidence_secret_finding_count
            ),
            "private_metadata_artifact_count": (
                private_metadata_artifact_count
            ),
            "target_collision_count": target_collision_count,
            "target_ignore_match_count": target_ignore_match_count,
            "target_ignore_unknown_count": target_ignore_unknown_count,
            "v0_1_2_self_test_markers_present": (
                v012_self_test_markers_present
            ),
            "git_baseline_passes": git_baseline_passes,
            "artifact_gate_passes": artifact_gate_passes,
            "target_gate_passes": target_gate_passes,
            "preservation_ready": preservation_ready,
            "preflight_status": "PASS" if preservation_ready else "STOP",
        },
        "commands": [asdict(record) for record in command_records],
    }

    # ========================================================
    # PRINT THE REPOSITORY SUMMARY.
    # ========================================================
    print("===== GIT BASELINE SUMMARY BEGIN =====")
    print(f"LOCAL_REPOSITORY={repository}")
    print(f"LOCAL_REPOSITORY_EXISTS={marker_bool(repository_exists)}")
    print(f"LOCAL_GIT_WORKTREE={marker_bool(git_worktree)}")
    print(f"LOCAL_GIT_ROOT={git_root if git_root is not None else 'UNKNOWN'}")
    print(f"LOCAL_GIT_ROOT_MATCHES={marker_bool(git_root_matches)}")
    print(f"LOCAL_GIT_BRANCH={git_branch if git_branch is not None else 'UNKNOWN'}")
    print(f"LOCAL_GIT_HEAD={git_head if git_head is not None else 'UNKNOWN'}")
    print(f"LOCAL_GIT_CLEAN={marker_bool(git_clean)}")
    print(
        "MILESTONE0_TAG_TARGET="
        f"{baseline_tag_target if baseline_tag_target is not None else 'UNKNOWN'}"
    )
    print(
        "TRACKED_FILE_COUNT="
        f"{tracked_file_count if tracked_file_count is not None else 'UNKNOWN'}"
    )
    print(f"ORIGIN_REMOTE={remote_url if remote_url is not None else 'UNKNOWN'}")
    print(f"ORIGIN_REMOTE_MATCHES={marker_bool(remote_matches)}")
    print(f"GIT_USER_NAME_PRESENT={marker_bool(git_user_name_present)}")
    print(f"GIT_USER_EMAIL_PRESENT={marker_bool(git_user_email_present)}")
    print(f"PROPOSED_BRANCH={PROPOSED_BRANCH}")
    print(f"PROPOSED_BRANCH_EXISTS={marker_bool(proposed_branch_exists)}")
    print(f"PROPOSED_TAG={PROPOSED_TAG}")
    print(f"PROPOSED_TAG_EXISTS={marker_bool(proposed_tag_exists)}")
    print(f"PROPOSED_WORKTREE_PATH={proposed_worktree_path}")
    print(
        "PROPOSED_WORKTREE_REGISTERED="
        f"{marker_bool(proposed_worktree_registered)}"
    )
    print(
        "PROPOSED_WORKTREE_PATH_EXISTS="
        f"{marker_bool(proposed_worktree_path_exists)}"
    )
    print(f"GIT_BASELINE_PASSES={marker_bool(git_baseline_passes)}")
    print("===== GIT BASELINE SUMMARY END =====")

    # ========================================================
    # PRINT EVERY ARTIFACT AUDIT.
    # ========================================================
    print("===== ARTIFACT AUDIT BEGIN =====")
    for artifact_audit in artifact_audits:
        print_artifact_audit(artifact_audit)
    print("===== ARTIFACT AUDIT END =====")

    # ========================================================
    # PRINT THE VERIFIED RECONCILIATION EVIDENCE SUMMARY.
    # ========================================================
    print("===== RECONCILIATION EVIDENCE VALIDATION BEGIN =====")
    print(f"EVIDENCE_CONTENT_VALID={marker_bool(evidence_content_valid)}")
    print(
        "EVIDENCE_RECONCILIATION_STATUS="
        f"{evidence_content_summary.get('reconciliation_status') or 'UNKNOWN'}"
    )
    print(
        "EVIDENCE_ACCOUNT_JSON_PARSE_STATUS="
        f"{evidence_content_summary.get('account_json_parse_status') or 'UNKNOWN'}"
    )
    print(
        "EVIDENCE_EXACT_WARNING_REPRODUCED="
        f"{marker_bool(evidence_content_summary.get('account_warning_prefix_reproduced'))}"
    )
    validation_errors = evidence_content_summary.get("validation_errors", [])
    validation_error_marker = (
        ",".join(str(value) for value in validation_errors)
        if validation_errors
        else "NONE"
    )
    print(f"EVIDENCE_VALIDATION_ERRORS={validation_error_marker}")
    print("===== RECONCILIATION EVIDENCE VALIDATION END =====")

    # ========================================================
    # PRINT THE V0.1.2 SELF-TEST SUMMARY.
    # ========================================================
    print("===== V0.1.2 SELF-TEST SUMMARY BEGIN =====")
    print(
        "V0_1_2_SELF_TEST_EXIT_CODE="
        f"{v012_self_test_record.exit_code if v012_self_test_record is not None else 'NOT_RUN'}"
    )
    print(
        "V0_1_2_SELF_TEST_MARKERS_PRESENT="
        f"{marker_bool(v012_self_test_markers_present)}"
    )
    print("===== V0.1.2 SELF-TEST SUMMARY END =====")

    # ========================================================
    # PRINT EVERY TARGET AUDIT.
    # ========================================================
    print("===== TARGET AUDIT BEGIN =====")
    for target_audit in target_audits:
        print_target_audit(target_audit)
    print("===== TARGET AUDIT END =====")

    # ========================================================
    # PRINT THE FINAL PREFLIGHT SUMMARY.
    # ========================================================
    print("===== PREFLIGHT SUMMARY BEGIN =====")
    print(f"MISSING_ARTIFACT_COUNT={missing_artifact_count}")
    print(f"ARTIFACT_HASH_MISMATCH_COUNT={artifact_hash_mismatch_count}")
    print(
        "HIGH_CONFIDENCE_SECRET_FINDING_COUNT="
        f"{high_confidence_secret_finding_count}"
    )
    print(
        "PRIVATE_METADATA_ARTIFACT_COUNT="
        f"{private_metadata_artifact_count}"
    )
    print("PRIVATE_REPOSITORY_REQUIRED=True")
    print("REMOTE_PUSH_DEFERRED=True")
    print(f"TARGET_COLLISION_COUNT={target_collision_count}")
    print(f"TARGET_IGNORE_MATCH_COUNT={target_ignore_match_count}")
    print(f"TARGET_IGNORE_UNKNOWN_COUNT={target_ignore_unknown_count}")
    print(
        "JSON_OUTPUT_OUTSIDE_REPOSITORY="
        f"{marker_bool(output_path_outside_repository)}"
    )
    print(f"ARTIFACT_GATE_PASSES={marker_bool(artifact_gate_passes)}")
    print(f"TARGET_GATE_PASSES={marker_bool(target_gate_passes)}")
    print("===== PREFLIGHT SUMMARY END =====")

    # ========================================================
    # INITIALIZE THE OPTIONAL EVIDENCE-WRITE RESULT.
    # ========================================================
    evidence_output_status = "NOT_REQUESTED"
    evidence_output_digest: str | None = None

    # ========================================================
    # WRITE OPTIONAL IMMUTABLE JSON EVIDENCE OUTSIDE THE REPOSITORY.
    # ========================================================
    if json_output is not None:
        if not output_path_outside_repository:
            evidence_output_status = "NOT_WRITTEN"
            print("EVIDENCE_OUTPUT_STATUS=NOT_WRITTEN")
            print("EVIDENCE_OUTPUT_REASON=OUTPUT_PATH_INSIDE_REPOSITORY")
            preservation_ready = False
        else:
            try:
                output_digest = write_json_exclusive(
                    json_output,
                    evidence_payload,
                )
                evidence_output_status = "WRITTEN"
                evidence_output_digest = output_digest
                print("EVIDENCE_OUTPUT_STATUS=WRITTEN")
                print(f"EVIDENCE_OUTPUT_PATH={json_output}")
                print(f"EVIDENCE_OUTPUT_SHA256={output_digest}")
            except (OSError, ValueError) as error:
                evidence_output_status = "NOT_WRITTEN"
                print("EVIDENCE_OUTPUT_STATUS=NOT_WRITTEN")
                print(
                    "EVIDENCE_OUTPUT_REASON="
                    f"{type(error).__name__}:{error}"
                )
                preservation_ready = False

    # ========================================================
    # REQUIRE A WRITTEN EVIDENCE FILE WHEN OUTPUT WAS REQUESTED.
    # ========================================================
    if json_output is not None and evidence_output_status != "WRITTEN":
        preservation_ready = False

    # ========================================================
    # PRINT THE FINAL STATUS ONLY AFTER OPTIONAL EVIDENCE WRITING.
    # ========================================================
    print(f"PRESERVATION_READY={marker_bool(preservation_ready)}")
    print(f"PREFLIGHT_STATUS={'PASS' if preservation_ready else 'STOP'}")

    # ========================================================
    # PRINT THE STRUCTURED FOOTER.
    # ========================================================
    print(
        f"===== END AJAS M1 PRESERVATION PREFLIGHT v{UTILITY_VERSION} ====="
    )

    # ========================================================
    # RETURN SUCCESS ONLY FOR A COMPLETE PASS.
    # ========================================================
    return 0 if preservation_ready else 2


# ============================================================
# PARSE COMMAND-LINE ARGUMENTS.
# ============================================================
def parse_arguments() -> argparse.Namespace:
    """RETURN VALIDATED COMMAND-LINE ARGUMENTS."""

    # ========================================================
    # CREATE THE ARGUMENT PARSER.
    # ========================================================
    parser = argparse.ArgumentParser(
        description=(
            "Read-only AJAS Milestone-1 preservation preflight."
        )
    )

    # ========================================================
    # ADD THE EXECUTION MODE.
    # ========================================================
    parser.add_argument(
        "--mode",
        choices=("inspect", "self-test"),
        default="inspect",
        help="Run read-only inspection or pure in-process self-tests.",
    )

    # ========================================================
    # ADD THE AUTHORITATIVE REPOSITORY PATH.
    # ========================================================
    parser.add_argument(
        "--repo",
        type=Path,
        default=DEFAULT_REPOSITORY,
        help="Authoritative AJAS repository path.",
    )

    # ========================================================
    # ADD THE DOWNLOAD ARTIFACT DIRECTORY.
    # ========================================================
    parser.add_argument(
        "--downloads",
        type=Path,
        default=DEFAULT_DOWNLOADS,
        help="Directory containing reviewed source artifacts.",
    )

    # ========================================================
    # ADD THE OPTIONAL IMMUTABLE JSON OUTPUT PATH.
    # ========================================================
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Optional new JSON evidence path outside the repository.",
    )

    # ========================================================
    # RETURN THE PARSED ARGUMENTS.
    # ========================================================
    return parser.parse_args()


# ============================================================
# DISPATCH THE REQUESTED MODE.
# ============================================================
def main() -> int:
    """RUN THE REQUESTED PREFLIGHT MODE."""

    # ========================================================
    # PARSE COMMAND-LINE ARGUMENTS.
    # ========================================================
    arguments = parse_arguments()

    # ========================================================
    # RUN PURE IN-PROCESS SELF-TESTS WHEN REQUESTED.
    # ========================================================
    if arguments.mode == "self-test":
        return run_self_test()

    # ========================================================
    # RUN THE COMPLETE READ-ONLY PRESERVATION PREFLIGHT.
    # ========================================================
    return inspect_preservation_readiness(
        repository=arguments.repo,
        downloads=arguments.downloads,
        json_output=arguments.json_output,
    )


# ============================================================
# EXECUTE ONLY WHEN THE FILE RUNS AS A SCRIPT.
# ============================================================
if __name__ == "__main__":
    # ========================================================
    # RETURN THE PROGRAM EXIT CODE TO THE OPERATING SYSTEM.
    # ========================================================
    raise SystemExit(main())
