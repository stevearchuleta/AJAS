#!/usr/bin/env python3
"""
AJAS MILESTONE 1B LOCAL PRESERVATION APPLY UTILITY, VERSION 0.1.0.

PURPOSE:
- RE-READ THE AUTHORITATIVE GIT BASELINE IMMEDIATELY BEFORE MUTATION.
- VERIFY THE EXACT DOWNLOAD ARTIFACTS AND MACHINE EVIDENCE.
- CREATE A NAMED LOCAL BRANCH IN A DISPOSABLE GIT WORKTREE.
- PRESERVE AUTHORITATIVE, SUPERSEDED, EVIDENCE, AND INCIDENT FILES.
- CREATE ONE LOCAL COMMIT AND ONE LOCAL CHECKPOINT TAG.
- LEAVE MAIN UNCHANGED AND CLEAN.
- DEFER ALL GITHUB PUSHES AND ALL AZURE OPERATIONS.

SAFETY GUARANTEES:
- NO AZURE COMMANDS.
- NO GITHUB NETWORK COMMANDS.
- NO GIT PUSH, PULL, FETCH, MERGE, RESET, CLEAN, RM, OR FORCE COMMANDS.
- NO SOURCE-REPOSITORY WORKTREE FILE WRITES.
- ALL FILE WRITES OCCUR INSIDE A NEW DISPOSABLE WORKTREE OR THE EXPLICIT
  OUTSIDE-REPOSITORY JSON EVIDENCE PATH.
- STDOUT AND STDERR REMAIN SEPARATE FOR EVERY CHILD PROCESS.
- EXPECTED STOPS PRODUCE CALM STRUCTURED OUTPUT.
- THE OLD RECONCILIATION VERSIONS REMAIN BYTE-IDENTICAL UNDER A SUPERSEDED
  DIRECTORY; V0.1.2 REMAINS THE ONLY READ-ONLY RECONCILIATION VERSION TO RUN.
"""

# ============================================================
# IMPORT STANDARD-LIBRARY MODULES ONLY.
# ============================================================
from __future__ import annotations

# ============================================================
# IMPORT ARGUMENT-PARSING SUPPORT.
# ============================================================
import argparse

# ============================================================
# IMPORT ABSTRACT-SYNTAX-TREE SUPPORT FOR REAL CALL-SITE AUDITS.
# ============================================================
import ast

# ============================================================
# IMPORT HASHING SUPPORT.
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
# IMPORT EXECUTABLE-DISCOVERY AND FILE-COPY SUPPORT.
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
# IMPORT TEMPORARY-DIRECTORY SUPPORT FOR SELF-TESTS.
# ============================================================
import tempfile

# ============================================================
# IMPORT IMMUTABLE RECORD SUPPORT.
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
from typing import Any, Final, Iterable, Sequence


# ============================================================
# DECLARE THE UTILITY VERSION.
# ============================================================
UTILITY_VERSION: Final[str] = "0.1.0"

# ============================================================
# DECLARE THE EVIDENCE SCHEMA VERSION.
# ============================================================
EVIDENCE_SCHEMA_VERSION: Final[str] = "1.0"

# ============================================================
# DECLARE THE AUTHORITATIVE REPOSITORY PATH.
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
# DECLARE THE EXPECTED REMOTE WITHOUT A TRAILING GIT SUFFIX.
# ============================================================
EXPECTED_REMOTE_URL: Final[str] = "https://github.com/stevearchuleta/AJAS"

# ============================================================
# DECLARE THE LOCAL PRESERVATION BRANCH.
# ============================================================
PRESERVATION_BRANCH: Final[str] = "milestone1-preserve-ops-evidence"

# ============================================================
# DECLARE THE LOCAL CHECKPOINT TAG.
# ============================================================
PRESERVATION_TAG: Final[str] = "milestone1b-reconciliation-complete"

# ============================================================
# DECLARE THE DISPOSABLE WORKTREE DIRECTORY NAME.
# ============================================================
WORKTREE_DIRECTORY_NAME: Final[str] = "milestone1-preserve-ops-evidence"

# ============================================================
# DECLARE THE LOCAL COMMIT MESSAGE.
# ============================================================
COMMIT_MESSAGE: Final[str] = (
    "chore(ops): preserve Milestone 1B reconciliation evidence"
)

# ============================================================
# DECLARE THE VERIFIED COLD-CACHE WARNING NEEDLE.
# ============================================================
EXPECTED_WARNING_NEEDLE: Final[str] = "cannot import name 'load_capability_host'"

# ============================================================
# DECLARE THE VERIFIED RECONCILIATION EVIDENCE FILE.
# ============================================================
RECONCILIATION_EVIDENCE_NAME: Final[str] = (
    "AJAS_M1_Reconciliation_20260904T174914819Z_v0_1_1.json"
)

# ============================================================
# DECLARE THE VERIFIED PRESERVATION PREFLIGHT EVIDENCE FILE.
# ============================================================
PREFLIGHT_EVIDENCE_NAME: Final[str] = (
    "AJAS_M1_Preservation_Preflight_20260904T185344709Z_v0_1_0.json"
)

# ============================================================
# DECLARE THE MAXIMUM ACCEPTED SOURCE-ARTIFACT SIZE.
# ============================================================
MAX_ARTIFACT_BYTES: Final[int] = 2_000_000


# ============================================================
# STORE ONE REQUIRED SOURCE ARTIFACT.
# ============================================================
@dataclass(frozen=True)
class ArtifactSpec:
    """STORE ONE EXACT DOWNLOAD ARTIFACT AND ONE REPOSITORY TARGET."""

    filename: str
    expected_sha256: str
    target_relative_path: str
    artifact_type: str


# ============================================================
# DECLARE THE EXACT DOWNLOAD ARTIFACTS AND FINAL TARGET LAYOUT.
# ============================================================
REQUIRED_ARTIFACTS: Final[tuple[ArtifactSpec, ...]] = (
    ArtifactSpec(
        filename="ajas_m1_readonly_reconcile_v0_1_0.py",
        expected_sha256=(
            "FC904C72AE779776A45079319B43D87AA38F33770208EB7CCC245FDE7BEAF736"
        ),
        target_relative_path=(
            "scripts/ops/superseded/ajas_m1_readonly_reconcile_v0_1_0.py"
        ),
        artifact_type="SUPERSEDED_PYTHON_UTILITY_KNOWN_JSON_PARSER_DEFECT",
    ),
    ArtifactSpec(
        filename="ajas_m1_readonly_reconcile_v0_1_1.py",
        expected_sha256=(
            "C2BA5134107BE5F10B0E474289486FD94D3ADF1A5C8133E4D667A587DD50E4C4"
        ),
        target_relative_path=(
            "scripts/ops/superseded/ajas_m1_readonly_reconcile_v0_1_1.py"
        ),
        artifact_type="SUPERSEDED_PYTHON_UTILITY_KNOWN_SCALAR_PARSER_DEFECT",
    ),
    ArtifactSpec(
        filename="ajas_m1_readonly_reconcile_v0_1_2.py",
        expected_sha256=(
            "2ABFC081F41EE5D31494E9AE8A3D7CF7C037EC34BD6AACB0328D364D3D504815"
        ),
        target_relative_path="scripts/ops/ajas_m1_readonly_reconcile_v0_1_2.py",
        artifact_type="AUTHORITATIVE_READ_ONLY_RECONCILIATION_UTILITY",
    ),
    ArtifactSpec(
        filename="ajas_m1_preservation_preflight_v0_1_0.py",
        expected_sha256=(
            "99F0A63A4525B566E1F7A711DE7518A2E9B730C099BD20879AF3BDF23D24A2F3"
        ),
        target_relative_path=(
            "scripts/ops/superseded/ajas_m1_preservation_preflight_v0_1_0.py"
        ),
        artifact_type="HISTORICAL_PREFLIGHT_UTILITY_ORIGINAL_TARGET_LAYOUT",
    ),
    ArtifactSpec(
        filename=RECONCILIATION_EVIDENCE_NAME,
        expected_sha256=(
            "7BA149D2F3A2392FA95340AC4EFE03F073B17A8A8099FCE194C89F576DAAB4A9"
        ),
        target_relative_path=(
            "ops/evidence/private/"
            "AJAS_M1_Reconciliation_20260904T174914819Z_v0_1_1.json"
        ),
        artifact_type="PRIVATE_MACHINE_EVIDENCE",
    ),
    ArtifactSpec(
        filename=PREFLIGHT_EVIDENCE_NAME,
        expected_sha256=(
            "D79A60FC972D2F39F968EFEA650E3A16E3996C70130F6A6B1A1D813E2BEC12B4"
        ),
        target_relative_path=(
            "ops/evidence/private/"
            "AJAS_M1_Preservation_Preflight_20260904T185344709Z_v0_1_0.json"
        ),
        artifact_type="PRIVATE_MACHINE_EVIDENCE",
    ),
)

# ============================================================
# DECLARE THE APPLY UTILITY'S FINAL REPOSITORY TARGET.
# ============================================================
SELF_TARGET_RELATIVE_PATH: Final[str] = (
    "scripts/ops/ajas_m1_preservation_apply_v0_1_0.py"
)

# ============================================================
# DECLARE GENERATED DOCUMENT TARGETS.
# ============================================================
GENERATED_TARGETS: Final[tuple[str, ...]] = (
    "scripts/ops/README.md",
    "scripts/ops/superseded/README.md",
    "ops/evidence/README.md",
    "ops/evidence/private/README.md",
    "ops/evidence/AJAS_M1_PRESERVATION_MANIFEST.sha256",
    "ops/incidents/README.md",
    "ops/incidents/AJAS_INCIDENT_2026-09-03_POWERSHELL_NULL_WRAPPER.md",
    "ops/incidents/AJAS_INCIDENT_2026-09-04_AZURE_CLI_STDOUT_CONTAMINATION.md",
)

# ============================================================
# DECLARE HIGH-CONFIDENCE SECRET RULES WITHOUT ECHOING MATCHED TEXT.
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
        "AZURE_CLIENT_SECRET_ASSIGNMENT",
        re.compile(
            r"(?i)\b(?:AZURE_CLIENT_SECRET|client_secret)\b\s*[:=]\s*[\"']?[^\s\"']{16,}"
        ),
    ),
)

# ============================================================
# DECLARE FORBIDDEN GIT VERBS FOR THE REAL AST CALL-SITE AUDIT.
# ============================================================
FORBIDDEN_GIT_PRIMARY_VERBS: Final[frozenset[str]] = frozenset(
    {
        "push",
        "pull",
        "fetch",
        "merge",
        "rebase",
        "reset",
        "clean",
        "rm",
        "checkout",
        "switch",
        "restore",
        "cherry-pick",
        "revert",
        "gc",
        "prune",
    }
)

# ============================================================
# DECLARE THE ONLY MUTATING GIT CALL LABELS AND VERBS.
# ============================================================
ALLOWED_MUTATING_GIT_CALLS: Final[dict[str, tuple[str, ...]]] = {
    "GIT_WORKTREE_ADD": ("worktree", "add", "-b"),
    "GIT_STAGE_TARGETS": ("add", "--"),
    "GIT_COMMIT": ("commit", "--no-gpg-sign", "-m"),
    "GIT_TAG_CREATE": ("tag",),
}


# ============================================================
# STORE ONE CHILD-PROCESS RECORD WITH SEPARATE STREAMS.
# ============================================================
@dataclass(frozen=True)
class CommandRecord:
    """STORE ONE PROCESS INVOCATION AND SEPARATE OUTPUT STREAMS."""

    label: str
    logical_command: str
    exit_code: int
    stdout: str
    stderr: str


# ============================================================
# STORE ONE SOURCE-ARTIFACT AUDIT.
# ============================================================
@dataclass(frozen=True)
class ArtifactAudit:
    """STORE ONE SOURCE ARTIFACT'S IDENTITY AND SAFETY RESULTS."""

    filename: str
    source_path: str
    target_relative_path: str
    artifact_type: str
    exists: bool
    is_file: bool
    is_symlink: bool
    bytes: int | None
    sha256: str | None
    hash_matches: bool
    high_confidence_secret_rules: tuple[str, ...]


# ============================================================
# STORE ONE REPOSITORY TARGET AUDIT.
# ============================================================
@dataclass(frozen=True)
class TargetAudit:
    """STORE ONE FINAL TARGET'S COLLISION AND IGNORE RESULTS."""

    relative_path: str
    exists_in_baseline: bool
    ignored: bool | None
    check_ignore_exit_code: int | None
    ignore_stderr: str


# ============================================================
# STORE ONE WRITTEN FILE IDENTITY.
# ============================================================
@dataclass(frozen=True)
class WrittenFileAudit:
    """STORE ONE DESTINATION FILE'S SIZE, HASH, AND SOURCE RELATIONSHIP."""

    relative_path: str
    bytes: int
    sha256: str
    expected_sha256: str | None
    hash_matches_expected: bool | None
    high_confidence_secret_rules: tuple[str, ...]


# ============================================================
# DEFINE A CONTROLLED STOP EXCEPTION.
# ============================================================
class ControlledStop(RuntimeError):
    """CARRY ONE MACHINE-READABLE STOP REASON WITHOUT A STACK TRACE."""


# ============================================================
# NORMALIZE POSSIBLY MISSING PROCESS TEXT.
# ============================================================
def normalize_text(value: str | bytes | None) -> str:
    """RETURN SAFE TEXT FOR MISSING, BYTE, OR STRING PROCESS OUTPUT."""

    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


# ============================================================
# RENDER A STABLE BOOLEAN MARKER.
# ============================================================
def marker_bool(value: bool | None) -> str:
    """RETURN TRUE, FALSE, OR UNKNOWN."""

    if value is None:
        return "UNKNOWN"
    return "True" if value else "False"


# ============================================================
# COMPUTE ONE FILE'S UPPERCASE SHA-256 DIGEST.
# ============================================================
def sha256_file(path: Path) -> str:
    """RETURN THE UPPERCASE SHA-256 DIGEST FOR ONE FILE."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


# ============================================================
# COMPUTE ONE BYTE PAYLOAD'S UPPERCASE SHA-256 DIGEST.
# ============================================================
def sha256_bytes(payload: bytes) -> str:
    """RETURN THE UPPERCASE SHA-256 DIGEST FOR BYTES."""

    return hashlib.sha256(payload).hexdigest().upper()


# ============================================================
# NORMALIZE A GIT REMOTE FOR STABLE COMPARISON.
# ============================================================
def normalize_remote(value: str) -> str:
    """REMOVE WHITESPACE, A TRAILING SLASH, AND A TRAILING GIT SUFFIX."""

    normalized = value.strip().rstrip("/")
    if normalized.lower().endswith(".git"):
        normalized = normalized[:-4]
    return normalized


# ============================================================
# RETURN TRUE WHEN A CANDIDATE PATH IS INSIDE A PARENT PATH.
# ============================================================
def path_is_within(candidate: Path, parent: Path) -> bool:
    """CHECK PATH CONTAINMENT WITHOUT STRING-PREFIX AMBIGUITY."""

    try:
        candidate.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


# ============================================================
# BUILD A SAFE TARGET PATH INSIDE THE DISPOSABLE WORKTREE.
# ============================================================
def safe_target_path(worktree: Path, relative_path: str) -> Path:
    """RETURN A CONTAINED TARGET PATH OR RAISE A CONTROLLED STOP."""

    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ControlledStop(f"UNSAFE_TARGET_RELATIVE_PATH:{relative_path}")
    target = worktree / relative
    if not path_is_within(target, worktree):
        raise ControlledStop(f"TARGET_ESCAPES_WORKTREE:{relative_path}")
    return target


# ============================================================
# SCAN TEXT FOR HIGH-CONFIDENCE SECRET RULE NAMES ONLY.
# ============================================================
def scan_secret_rule_names(text: str) -> tuple[str, ...]:
    """RETURN MATCHING RULE NAMES WITHOUT RETURNING SECRET-LIKE TEXT."""

    findings = [
        rule_name
        for rule_name, pattern in HIGH_CONFIDENCE_SECRET_PATTERNS
        if pattern.search(text) is not None
    ]
    return tuple(sorted(findings))


# ============================================================
# SCAN FILE BYTES AS UTF-8 WITH REPLACEMENT.
# ============================================================
def scan_file_secret_rule_names(path: Path) -> tuple[str, ...]:
    """RETURN HIGH-CONFIDENCE RULE NAMES FOR ONE FILE."""

    text = path.read_bytes().decode("utf-8", errors="replace")
    return scan_secret_rule_names(text)


# ============================================================
# RESOLVE A REQUIRED EXECUTABLE.
# ============================================================
def resolve_executable(name: str) -> Path | None:
    """RETURN A RESOLVED EXECUTABLE PATH OR NONE."""

    resolved = shutil.which(name)
    return None if resolved is None else Path(resolved)


# ============================================================
# RUN ONE CHILD PROCESS WITHOUT SHELL EXPANSION OR STREAM MERGING.
# ============================================================
def run_process(
    *,
    label: str,
    executable: Path,
    arguments: Sequence[str],
    working_directory: Path | None,
    timeout_seconds: int = 180,
) -> CommandRecord:
    """RUN ONE PROCESS AND RETURN A NULL-SAFE STRUCTURED RECORD."""

    logical_command = subprocess.list2cmdline([str(executable), *arguments])
    child_environment = os.environ.copy()
    child_environment["GIT_TERMINAL_PROMPT"] = "0"
    child_environment["GCM_INTERACTIVE"] = "Never"

    try:
        completed = subprocess.run(
            [str(executable), *arguments],
            cwd=(str(working_directory) if working_directory is not None else None),
            env=child_environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            shell=False,
            timeout=timeout_seconds,
        )
    except OSError as error:
        return CommandRecord(
            label=label,
            logical_command=logical_command,
            exit_code=126,
            stdout="",
            stderr=f"PROCESS_LAUNCH_ERROR={type(error).__name__}:{error}",
        )
    except subprocess.TimeoutExpired as error:
        stdout = normalize_text(error.stdout).strip()
        stderr = normalize_text(error.stderr).strip()
        timeout_marker = f"PROCESS_TIMEOUT_SECONDS={timeout_seconds}"
        merged_stderr = f"{stderr}\n{timeout_marker}" if stderr else timeout_marker
        return CommandRecord(
            label=label,
            logical_command=logical_command,
            exit_code=124,
            stdout=stdout,
            stderr=merged_stderr,
        )

    return CommandRecord(
        label=label,
        logical_command=logical_command,
        exit_code=completed.returncode,
        stdout=normalize_text(completed.stdout).strip(),
        stderr=normalize_text(completed.stderr).strip(),
    )


# ============================================================
# RUN ONE LOCAL GIT COMMAND AND APPEND THE AUDIT RECORD.
# ============================================================
def run_git_command(
    *,
    records: list[CommandRecord],
    label: str,
    git_executable: Path,
    repository: Path,
    arguments: Sequence[str],
    timeout_seconds: int = 180,
) -> CommandRecord:
    """RUN ONE LOCAL GIT COMMAND WITH A FULLY QUALIFIED REPOSITORY."""

    record = run_process(
        label=label,
        executable=git_executable,
        arguments=["-C", str(repository), *arguments],
        working_directory=None,
        timeout_seconds=timeout_seconds,
    )
    records.append(record)
    return record


# ============================================================
# REQUIRE A SUCCESSFUL COMMAND.
# ============================================================
def require_command_success(record: CommandRecord, reason: str) -> None:
    """RAISE A CONTROLLED STOP WHEN A COMMAND EXIT CODE IS NONZERO."""

    if record.exit_code != 0:
        raise ControlledStop(f"{reason}:EXIT_CODE={record.exit_code}")


# ============================================================
# PRINT ONE COMMAND RECORD WITH SEPARATE STREAM BOUNDARIES.
# ============================================================
def print_command_record(record: CommandRecord) -> None:
    """PRINT ONE AUDIT RECORD WITHOUT MERGING STDOUT AND STDERR."""

    print(f"COMMAND_LABEL={record.label}")
    print(f"COMMAND={record.logical_command}")
    print(f"EXIT_CODE={record.exit_code}")
    print("STDOUT_BEGIN")
    print(record.stdout)
    print("STDOUT_END")
    print("STDERR_BEGIN")
    print(record.stderr)
    print("STDERR_END")
    print("---")


# ============================================================
# READ ONE JSON FILE AS A DICTIONARY.
# ============================================================
def read_json_dict(path: Path) -> dict[str, Any]:
    """RETURN A JSON OBJECT OR RAISE A CONTROLLED STOP."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ControlledStop(
            f"JSON_FILE_READ_FAILED:{path.name}:{type(error).__name__}"
        ) from error
    if not isinstance(value, dict):
        raise ControlledStop(f"JSON_TOP_LEVEL_NOT_OBJECT:{path.name}")
    return value


# ============================================================
# VALIDATE THE RECONCILIATION EVIDENCE'S LOAD-BEARING FIELDS.
# ============================================================
def validate_reconciliation_evidence(payload: dict[str, Any]) -> tuple[bool, tuple[str, ...]]:
    """VALIDATE THE COLD-CACHE RECONCILIATION WITHOUT TRUSTING NARRATION."""

    errors: list[str] = []
    utility = payload.get("utility")
    state = payload.get("reconciled_state")
    commands = payload.get("commands")

    if not isinstance(utility, dict):
        errors.append("UTILITY_OBJECT_MISSING")
    else:
        if utility.get("version") != "0.1.1":
            errors.append("UTILITY_VERSION_NOT_V0_1_1")
        if utility.get("script_sha256") != (
            "C2BA5134107BE5F10B0E474289486FD94D3ADF1A5C8133E4D667A587DD50E4C4"
        ):
            errors.append("UTILITY_SHA256_MISMATCH")

    if not isinstance(state, dict):
        errors.append("RECONCILED_STATE_MISSING")
    else:
        expected_pairs = {
            "local_git_branch": EXPECTED_BRANCH,
            "local_git_head": EXPECTED_HEAD,
            "local_git_clean": True,
            "git_branch_matches_handoff": True,
            "git_head_matches_handoff": True,
            "git_tag_matches_handoff": True,
            "azure_subscription_matches_handoff": True,
            "containerapp_extension_state": "INSTALLED",
            "containerapp_extension_version": "1.3.0b5",
            "resource_group_exists": False,
            "container_registry_name_available": True,
            "inspection_complete": True,
            "baseline_gate_passes": True,
            "reconciliation_status": "COMPLETE_BASELINE_CONFIRMED",
        }
        for key, expected in expected_pairs.items():
            if state.get(key) != expected:
                errors.append(f"STATE_MISMATCH:{key}")

    account_records: list[dict[str, Any]] = []
    if isinstance(commands, list):
        account_records = [
            item
            for item in commands
            if isinstance(item, dict) and item.get("label") == "AZURE_ACCOUNT_SHOW"
        ]
    else:
        errors.append("COMMANDS_LIST_MISSING")

    if len(account_records) != 1:
        errors.append("AZURE_ACCOUNT_RECORD_COUNT_INVALID")
    else:
        audit = account_records[0].get("json_parse_audit")
        if not isinstance(audit, dict):
            errors.append("AZURE_ACCOUNT_PARSE_AUDIT_MISSING")
        else:
            if audit.get("status") != "PARSED_WITH_PREFIX":
                errors.append("AZURE_ACCOUNT_PARSE_STATUS_NOT_PREFIX_AWARE")
            prefix = audit.get("stdout_prefix_discarded")
            if not isinstance(prefix, str) or EXPECTED_WARNING_NEEDLE not in prefix:
                errors.append("EXACT_COLD_CACHE_WARNING_NOT_RECORDED")

    return len(errors) == 0, tuple(errors)


# ============================================================
# VALIDATE THE PRESERVATION PREFLIGHT EVIDENCE'S LOAD-BEARING FIELDS.
# ============================================================
def validate_preflight_evidence(payload: dict[str, Any]) -> tuple[bool, tuple[str, ...]]:
    """VALIDATE THE PRIOR READ-ONLY PREFLIGHT RECORD."""

    errors: list[str] = []
    utility = payload.get("utility")
    summary = payload.get("summary")
    git_state = payload.get("git_state")

    if not isinstance(utility, dict):
        errors.append("UTILITY_OBJECT_MISSING")
    else:
        if utility.get("version") != "0.1.0":
            errors.append("UTILITY_VERSION_NOT_V0_1_0")
        if utility.get("script_sha256") != (
            "99F0A63A4525B566E1F7A711DE7518A2E9B730C099BD20879AF3BDF23D24A2F3"
        ):
            errors.append("UTILITY_SHA256_MISMATCH")

    if not isinstance(summary, dict):
        errors.append("SUMMARY_MISSING")
    else:
        expected_pairs = {
            "missing_artifact_count": 0,
            "artifact_hash_mismatch_count": 0,
            "high_confidence_secret_finding_count": 0,
            "git_baseline_passes": True,
            "artifact_gate_passes": True,
            "target_gate_passes": True,
            "preservation_ready": True,
            "preflight_status": "PASS",
        }
        for key, expected in expected_pairs.items():
            if summary.get(key) != expected:
                errors.append(f"SUMMARY_MISMATCH:{key}")

    if not isinstance(git_state, dict):
        errors.append("GIT_STATE_MISSING")
    else:
        expected_pairs = {
            "branch": EXPECTED_BRANCH,
            "head": EXPECTED_HEAD,
            "clean": True,
            "baseline_tag_target": EXPECTED_HEAD,
            "tracked_file_count": EXPECTED_TRACKED_FILE_COUNT,
            "origin_remote_matches": True,
            "proposed_branch_exists": False,
            "proposed_tag_exists": False,
            "proposed_worktree_registered": False,
            "proposed_worktree_path_exists": False,
            "git_baseline_passes": True,
        }
        for key, expected in expected_pairs.items():
            if git_state.get(key) != expected:
                errors.append(f"GIT_STATE_MISMATCH:{key}")

    return len(errors) == 0, tuple(errors)


# ============================================================
# AUDIT ONE DOWNLOAD ARTIFACT.
# ============================================================
def audit_artifact(downloads: Path, spec: ArtifactSpec) -> ArtifactAudit:
    """VERIFY ONE DOWNLOAD ARTIFACT'S TYPE, SIZE, HASH, AND SECRET RULES."""

    source_path = downloads / spec.filename
    exists = source_path.exists()
    is_file = source_path.is_file()
    is_symlink = source_path.is_symlink()
    size: int | None = None
    digest: str | None = None
    findings: tuple[str, ...] = ()

    if is_file and not is_symlink:
        size = source_path.stat().st_size
        if size <= MAX_ARTIFACT_BYTES:
            digest = sha256_file(source_path)
            findings = scan_file_secret_rule_names(source_path)

    return ArtifactAudit(
        filename=spec.filename,
        source_path=str(source_path),
        target_relative_path=spec.target_relative_path,
        artifact_type=spec.artifact_type,
        exists=exists,
        is_file=is_file,
        is_symlink=is_symlink,
        bytes=size,
        sha256=digest,
        hash_matches=digest == spec.expected_sha256,
        high_confidence_secret_rules=findings,
    )


# ============================================================
# RENDER THE AUTHORITATIVE OPERATIONS README.
# ============================================================
def render_operations_readme(apply_sha256: str) -> str:
    """RETURN THE OPERATOR PRECEDENCE DOCUMENT."""

    return f"""# AJAS Operations Utilities

## Authoritative executable

`ajas_m1_readonly_reconcile_v0_1_2.py` is the only Milestone-1B read-only
reconciliation utility approved for execution.

`ajas_m1_preservation_apply_v0_1_0.py` created the local preservation branch,
commit, and checkpoint tag. A second execution must stop when the branch, tag,
or worktree already exists.

## Superseded and historical material

Older utilities remain byte-identical under `scripts/ops/superseded/` for
incident reconstruction. No utility under that directory is approved for
execution.

## Deployment boundary

GitHub-to-Azure deployment requires OIDC and short-lived tokens. Azure client
secrets, service-principal passwords, publish profiles, and long-lived access
tokens remain prohibited.

## Apply utility identity

```text
VERSION={UTILITY_VERSION}
SHA256={apply_sha256}
```
"""


# ============================================================
# RENDER THE SUPERSEDED-UTILITY README.
# ============================================================
def render_superseded_readme() -> str:
    """RETURN THE HISTORICAL-UTILITY WARNING DOCUMENT."""

    return """# Superseded and Historical AJAS Operations Utilities

**Execution prohibited.** Files in this directory exist only for chain of
custody, incident analysis, and regression-test history.

| File | Status | Reason |
|---|---|---|
| `ajas_m1_readonly_reconcile_v0_1_0.py` | Superseded | Strict whole-stdout JSON parsing failed on a valid JSON payload preceded by Azure CLI warning text. |
| `ajas_m1_readonly_reconcile_v0_1_1.py` | Superseded | JSON parsing was hardened, but Boolean TSV and nonnegative-integer scalar parsing still assumed clean whole-stdout values. |
| `ajas_m1_preservation_preflight_v0_1_0.py` | Historical | The read-only preflight passed. The final preservation target layout changed after reviewer approval so defective and historical utilities could live outside the authoritative execution directory. |

The approved reconciliation utility is:

```text
scripts/ops/ajas_m1_readonly_reconcile_v0_1_2.py
```
"""


# ============================================================
# RENDER THE EVIDENCE README.
# ============================================================
def render_evidence_readme() -> str:
    """RETURN THE EVIDENCE RETENTION AND PRIVACY DOCUMENT."""

    return """# AJAS Operational Evidence

## Scope

The evidence tree preserves immutable machine records, source-artifact hashes,
and incident lessons required for later verification and Reflection Agent
analysis.

## Privacy classification

`ops/evidence/private/` contains local paths and Azure account metadata.
Repository visibility must be verified as **private** before any push. Public
publication or public-repository transfer is prohibited without a separate
sanitization review.

## Execution precedence

The only approved Milestone-1B reconciliation utility is:

```text
scripts/ops/ajas_m1_readonly_reconcile_v0_1_2.py
```

The utilities under `scripts/ops/superseded/` are evidence, not runnable tools.

## Reflection Agent boundary

The future Reflection Agent may read sanitized evidence, identify repeated
failure patterns, and propose tests or process changes. The Reflection Agent
may not change source code, prompts, policies, production configuration,
deployments, or guardrails without explicit human review and approval.

## Evidence rules

1. Preserve stdout and stderr as separate fields.
2. Record discarded prefixes rather than silently swallowing contamination.
3. Fail closed on empty, ambiguous, malformed, or trailing-contaminated output.
4. Record utility version and SHA-256 identity.
5. Write operational evidence by exclusive creation and never overwrite an
   existing evidence record.
"""


# ============================================================
# RENDER THE PRIVATE-EVIDENCE README.
# ============================================================
def render_private_evidence_readme() -> str:
    """RETURN THE PRIVATE-EVIDENCE DIRECTORY WARNING."""

    return """# Private AJAS Machine Evidence

Files in this directory can contain local filesystem paths, subscription and
tenant identifiers, command output, and other private operational metadata.

```text
PUBLIC_EXPORT_ALLOWED=False
PUBLIC_REPOSITORY_ALLOWED=False
SANITIZATION_REQUIRED_BEFORE_EXTERNAL_SHARING=True
```

No credential, secret, password, publish profile, or long-lived token belongs
in this directory.
"""


# ============================================================
# RENDER THE INCIDENT SCHEMA README.
# ============================================================
def render_incidents_readme() -> str:
    """RETURN THE FIXED INCIDENT-RECORD SCHEMA."""

    return """# AJAS Incident Records

Every controlled stop uses the following stable sections:

```text
WHAT_WAS_ATTEMPTED
OBSERVED_OUTPUT
ROOT_CAUSE
EVIDENCE
FIX
REGRESSION_TEST_ADDED
GENERALIZED_LESSON
```

A missing or uncertain root cause must remain explicitly marked as uncertain.
Incident records support proposal-only Reflection Agent analysis and human
review; incident records do not authorize automatic production changes.
"""


# ============================================================
# RENDER THE POWERSHELL NULL-WRAPPER INCIDENT.
# ============================================================
def render_null_wrapper_incident() -> str:
    """RETURN THE SEPTEMBER 3 CONTROLLED-STOP INCIDENT RECORD."""

    return """# AJAS Incident — PowerShell Null-Valued Wrapper Stop

**Date:** 2026-09-03
**Status:** Closed by readback and replacement tooling

## WHAT_WAS_ATTEMPTED

Milestone-1B attempted repository verification, Azure subscription verification,
`containerapp` extension installation, registry-name inspection, and empty
resource-group creation.

## OBSERVED_OUTPUT

```text
MILESTONE_1B=STOP
STOP_PHASE=INSTALL_CONTAINERAPP_EXTENSION
REASON=You cannot call a method on a null-valued expression.
```

Registry-name inspection and resource-group creation were not reached.

## ROOT_CAUSE

The exact failing PowerShell source line was not printed. The supported defect
class is an unsafe method call, most likely `.Trim()`, against a null helper or
command-result field. Exact-line attribution remains intentionally unclaimed.

Later readback proved that `containerapp` installation completed before the
wrapper stopped.

## EVIDENCE

```text
Git main=df08693da3157504d7f4a10dcb840969950bd184
Git status=clean
containerapp=installed
containerapp version=1.3.0b5
resource group=absent
ACR name=available
billable AJAS resources=zero
```

## FIX

A versioned Python operations utility replaced the giant PowerShell mutation
wrapper. Child-process stdout and stderr remain separate, missing output is
normalized, and machine evidence records each command and resulting state.

## REGRESSION_TEST_ADDED

The replacement utilities include null normalization, contaminated output,
ambiguous payload, and trailing-contamination regression tests.

## GENERALIZED_LESSON

Every external producer can return empty, contaminated, or malformed output.
Method calls and parser operations require null normalization, explicit payload
location, type validation, and fail-closed ambiguity handling.
"""


# ============================================================
# RENDER THE AZURE CLI STDOUT-CONTAMINATION INCIDENT.
# ============================================================
def render_stdout_contamination_incident() -> str:
    """RETURN THE SEPTEMBER 4 CONTROLLED-EXPERIMENT INCIDENT RECORD."""

    return """# AJAS Incident — Azure CLI Stdout Contamination

**Date:** 2026-09-04
**Status:** Fixed and reproduced under controlled cold-cache conditions

## WHAT_WAS_ATTEMPTED

A read-only reconciliation requested Azure account JSON after deleting only the
disposable Azure CLI `commandIndex.json` cache.

## OBSERVED_OUTPUT

The first Azure CLI call emitted a Python import warning on stdout before a
valid JSON object. The JSON payload began on line 2. Later Azure calls were
clean after command-index rebuilding.

## ROOT_CAUSE

Reconciliation v0.1.0 called strict `json.loads(record.stdout)` against the
entire stdout stream. The leading warning caused `JSONDecodeError`, even though
the valid Azure account object followed immediately.

Reconciliation v0.1.1 fixed JSON payload discovery but retained clean-output
assumptions for Boolean TSV and nonnegative-integer scalar parsers.

## EVIDENCE

```text
Reconciliation evidence SHA256=7BA149D2F3A2392FA95340AC4EFE03F073B17A8A8099FCE194C89F576DAAB4A9
JSON_PARSE_STATUS=PARSED_WITH_PREFIX
JSON_PAYLOAD_START_LINE=2
COLD_CACHE_REPRODUCTION_STATUS=EXACT_INCIDENT_REPRODUCED_AND_HANDLED
RECONCILIATION_STATUS=COMPLETE_BASELINE_CONFIRMED
```

## FIX

Reconciliation v0.1.2 locates JSON and scalar payloads, validates expected
types, records discarded prefixes, rejects multiple payload candidates, and
rejects trailing contamination.

## REGRESSION_TEST_ADDED

```text
SELF_TEST_CONTAMINATED_AZURE_STDOUT=PASS
SELF_TEST_CONTAMINATED_TSV_BOOLEAN=PASS
SELF_TEST_CONTAMINATED_NONNEGATIVE_INTEGER=PASS
SELF_TEST_SCALAR_AMBIGUITY_FAIL_CLOSED=PASS
SELF_TEST_SCALAR_TRAILING_CONTAMINATION_FAIL_CLOSED=PASS
```

## GENERALIZED_LESSON

An external boundary must locate the payload, validate the payload type, record
all discarded material, and fail closed when more than one interpretation is
possible. The same rule applies to Azure CLI output and AJAS agent-to-agent
contracts.
"""


# ============================================================
# BUILD ALL GENERATED DOCUMENTS EXCEPT THE HASH MANIFEST.
# ============================================================
def build_generated_documents(apply_sha256: str) -> dict[str, bytes]:
    """RETURN UTF-8 DOCUMENT PAYLOADS FOR THE FINAL TARGET TREE."""

    text_documents = {
        "scripts/ops/README.md": render_operations_readme(apply_sha256),
        "scripts/ops/superseded/README.md": render_superseded_readme(),
        "ops/evidence/README.md": render_evidence_readme(),
        "ops/evidence/private/README.md": render_private_evidence_readme(),
        "ops/incidents/README.md": render_incidents_readme(),
        (
            "ops/incidents/"
            "AJAS_INCIDENT_2026-09-03_POWERSHELL_NULL_WRAPPER.md"
        ): render_null_wrapper_incident(),
        (
            "ops/incidents/"
            "AJAS_INCIDENT_2026-09-04_AZURE_CLI_STDOUT_CONTAMINATION.md"
        ): render_stdout_contamination_incident(),
    }
    return {
        relative_path: text.replace("\r\n", "\n").encode("utf-8")
        for relative_path, text in text_documents.items()
    }


# ============================================================
# BUILD THE COMPLETE FINAL TARGET LIST.
# ============================================================
def planned_target_paths() -> tuple[str, ...]:
    """RETURN EVERY PATH THAT THE APPLY STEP MAY WRITE OR STAGE."""

    paths = [spec.target_relative_path for spec in REQUIRED_ARTIFACTS]
    paths.append(SELF_TARGET_RELATIVE_PATH)
    paths.extend(GENERATED_TARGETS)
    return tuple(sorted(paths))


# ============================================================
# AUDIT ACTUAL RUN_GIT_COMMAND CALL SITES THROUGH THE PYTHON AST.
# ============================================================
def audit_git_callsites_from_source(source_text: str) -> tuple[bool, tuple[str, ...]]:
    """INSPECT REAL CALL SITES INSTEAD OF A DISCONNECTED LABEL LIST."""

    errors: list[str] = []
    tree = ast.parse(source_text)
    call_count = 0

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "run_git_command":
            continue

        call_count += 1
        keywords = {keyword.arg: keyword.value for keyword in node.keywords if keyword.arg}
        label_node = keywords.get("label")
        arguments_node = keywords.get("arguments")

        if not isinstance(label_node, ast.Constant) or not isinstance(label_node.value, str):
            errors.append("NON_LITERAL_GIT_LABEL")
            continue
        label = label_node.value

        if not isinstance(arguments_node, (ast.List, ast.Tuple)) or not arguments_node.elts:
            errors.append(f"NON_LITERAL_GIT_ARGUMENT_VECTOR:{label}")
            continue

        constant_tokens = [
            element.value
            for element in arguments_node.elts
            if isinstance(element, ast.Constant) and isinstance(element.value, str)
        ]
        if not constant_tokens:
            errors.append(f"GIT_PRIMARY_VERB_NOT_LITERAL:{label}")
            continue

        primary_verb = constant_tokens[0]
        if primary_verb in FORBIDDEN_GIT_PRIMARY_VERBS:
            errors.append(f"FORBIDDEN_GIT_VERB:{label}:{primary_verb}")

        if label in ALLOWED_MUTATING_GIT_CALLS:
            required_prefix = ALLOWED_MUTATING_GIT_CALLS[label]
            if tuple(constant_tokens[: len(required_prefix)]) != required_prefix:
                errors.append(f"MUTATING_CALL_PATTERN_MISMATCH:{label}")
        else:
            if label.startswith("GIT_") and primary_verb in {
                "worktree",
                "add",
                "commit",
                "tag",
            }:
                if label in {
                    "GIT_WORKTREE_LIST",
                    "GIT_TAG_LIST",
                    "GIT_TAG_VERIFY",
                    "GIT_TAG_TARGET_VERIFY",
                    "GIT_TAG_TARGET_RECHECK",
                }:
                    pass
                elif label not in ALLOWED_MUTATING_GIT_CALLS:
                    errors.append(f"UNDECLARED_MUTATING_GIT_CALL:{label}:{primary_verb}")

        if primary_verb == "branch" and "--show-current" not in constant_tokens and "--list" not in constant_tokens:
            errors.append(f"UNSAFE_BRANCH_CALL:{label}")
        if primary_verb == "tag" and label != "GIT_TAG_CREATE" and "--list" not in constant_tokens and "-n" not in constant_tokens:
            errors.append(f"UNSAFE_TAG_CALL:{label}")
        if primary_verb == "worktree" and label != "GIT_WORKTREE_ADD" and "list" not in constant_tokens:
            errors.append(f"UNSAFE_WORKTREE_CALL:{label}")

    if call_count == 0:
        errors.append("NO_GIT_CALLSITES_FOUND")

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                full_name = f"{node.func.value.id}.{node.func.attr}"
                if full_name in {
                    "os.system",
                    "os.remove",
                    "shutil.rmtree",
                    "subprocess.Popen",
                    "subprocess.call",
                    "subprocess.check_call",
                    "subprocess.check_output",
                }:
                    errors.append(f"FORBIDDEN_PROCESS_OR_DELETE_CALL:{full_name}")

    subprocess_run_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "subprocess"
        and node.func.attr == "run"
    ]
    if len(subprocess_run_calls) != 1:
        errors.append("SUBPROCESS_RUN_CALL_COUNT_NOT_ONE")
    else:
        keywords = {
            keyword.arg: keyword.value
            for keyword in subprocess_run_calls[0].keywords
            if keyword.arg
        }
        shell_node = keywords.get("shell")
        capture_node = keywords.get("capture_output")
        if not (
            isinstance(shell_node, ast.Constant) and shell_node.value is False
        ):
            errors.append("SUBPROCESS_RUN_SHELL_NOT_FALSE")
        if not (
            isinstance(capture_node, ast.Constant) and capture_node.value is True
        ):
            errors.append("SUBPROCESS_RUN_CAPTURE_OUTPUT_NOT_TRUE")

    return len(errors) == 0, tuple(errors)


# ============================================================
# RUN PURE SELF-TESTS WITHOUT GIT, AZURE, OR NETWORK COMMANDS.
# ============================================================
def run_self_test() -> int:
    """VERIFY PARSERS, SAFETY RULES, DOCUMENT PRECEDENCE, AND REAL CALL SITES."""

    assert normalize_text(None) == ""
    assert normalize_text(b"abc") == "abc"
    print("SELF_TEST_NULL_NORMALIZATION=PASS")

    assert normalize_remote("https://github.com/example/repo.git/") == (
        "https://github.com/example/repo"
    )
    print("SELF_TEST_REMOTE_NORMALIZATION=PASS")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        safe = safe_target_path(root, "a/b.txt")
        assert path_is_within(safe, root)
        try:
            safe_target_path(root, "../escape.txt")
        except ControlledStop:
            pass
        else:
            raise AssertionError("PATH_TRAVERSAL_WAS_NOT_REJECTED")
    print("SELF_TEST_PATH_CONTAINMENT=PASS")

    assert scan_secret_rule_names("ordinary text") == ()
    secret_fixture = "-----BEGIN " + "PRIVATE KEY-----"
    assert scan_secret_rule_names(secret_fixture) == (
        "PEM_PRIVATE_KEY",
    )
    print("SELF_TEST_SECRET_SCANNER=PASS")

    reconciliation_fixture = {
        "utility": {
            "version": "0.1.1",
            "script_sha256": (
                "C2BA5134107BE5F10B0E474289486FD94D3ADF1A5C8133E4D667A587DD50E4C4"
            ),
        },
        "reconciled_state": {
            "local_git_branch": EXPECTED_BRANCH,
            "local_git_head": EXPECTED_HEAD,
            "local_git_clean": True,
            "git_branch_matches_handoff": True,
            "git_head_matches_handoff": True,
            "git_tag_matches_handoff": True,
            "azure_subscription_matches_handoff": True,
            "containerapp_extension_state": "INSTALLED",
            "containerapp_extension_version": "1.3.0b5",
            "resource_group_exists": False,
            "container_registry_name_available": True,
            "inspection_complete": True,
            "baseline_gate_passes": True,
            "reconciliation_status": "COMPLETE_BASELINE_CONFIRMED",
        },
        "commands": [
            {
                "label": "AZURE_ACCOUNT_SHOW",
                "json_parse_audit": {
                    "status": "PARSED_WITH_PREFIX",
                    "stdout_prefix_discarded": EXPECTED_WARNING_NEEDLE,
                },
            }
        ],
    }
    valid, errors = validate_reconciliation_evidence(reconciliation_fixture)
    assert valid and errors == ()
    print("SELF_TEST_RECONCILIATION_EVIDENCE_VALIDATION=PASS")

    preflight_fixture = {
        "utility": {
            "version": "0.1.0",
            "script_sha256": (
                "99F0A63A4525B566E1F7A711DE7518A2E9B730C099BD20879AF3BDF23D24A2F3"
            ),
        },
        "summary": {
            "missing_artifact_count": 0,
            "artifact_hash_mismatch_count": 0,
            "high_confidence_secret_finding_count": 0,
            "git_baseline_passes": True,
            "artifact_gate_passes": True,
            "target_gate_passes": True,
            "preservation_ready": True,
            "preflight_status": "PASS",
        },
        "git_state": {
            "branch": EXPECTED_BRANCH,
            "head": EXPECTED_HEAD,
            "clean": True,
            "baseline_tag_target": EXPECTED_HEAD,
            "tracked_file_count": EXPECTED_TRACKED_FILE_COUNT,
            "origin_remote_matches": True,
            "proposed_branch_exists": False,
            "proposed_tag_exists": False,
            "proposed_worktree_registered": False,
            "proposed_worktree_path_exists": False,
            "git_baseline_passes": True,
        },
    }
    valid, errors = validate_preflight_evidence(preflight_fixture)
    assert valid and errors == ()
    print("SELF_TEST_PREFLIGHT_EVIDENCE_VALIDATION=PASS")

    documents = build_generated_documents("A" * 64)
    operations_text = documents["scripts/ops/README.md"].decode("utf-8")
    superseded_text = documents[
        "scripts/ops/superseded/README.md"
    ].decode("utf-8")
    assert "only Milestone-1B read-only" in operations_text
    assert "Execution prohibited" in superseded_text
    assert "v0_1_2.py" in operations_text
    print("SELF_TEST_OPERATOR_PRECEDENCE_DOCUMENTS=PASS")

    source_text = Path(__file__).read_text(encoding="utf-8")
    callsite_valid, callsite_errors = audit_git_callsites_from_source(source_text)
    assert callsite_valid, callsite_errors
    print("SELF_TEST_AST_GIT_CALLSITE_AUDIT=PASS")

    assert "ops/evidence/AJAS_M1_PRESERVATION_MANIFEST.sha256" in planned_target_paths()
    assert SELF_TARGET_RELATIVE_PATH in planned_target_paths()
    assert len(planned_target_paths()) == len(set(planned_target_paths()))
    print("SELF_TEST_TARGET_PLAN_UNIQUE=PASS")

    print(f"AJAS_M1_PRESERVATION_APPLY_SELF_TEST_v{UTILITY_VERSION}=PASS")
    return 0


# ============================================================
# WRITE ONE FILE BY EXCLUSIVE CREATION.
# ============================================================
def write_exclusive(path: Path, payload: bytes) -> None:
    """CREATE ONE NEW FILE AND REFUSE OVERWRITE."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


# ============================================================
# WRITE ONE JSON EVIDENCE FILE BY EXCLUSIVE CREATION.
# ============================================================
def write_json_exclusive(path: Path, payload: dict[str, Any]) -> str:
    """WRITE SORTED UTF-8 JSON AND RETURN THE FILE SHA-256."""

    serialized = json.dumps(
        payload,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    write_exclusive(path, serialized)
    return sha256_file(path)


# ============================================================
# VERIFY PYTHON SOURCE COMPILATION IN MEMORY.
# ============================================================
def compile_python_source(path: Path) -> None:
    """COMPILE SOURCE WITHOUT CREATING PYC OR PYCACHE FILES."""

    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec", dont_inherit=True)


# ============================================================
# CREATE THE SHA-256 MANIFEST FOR ALL NON-MANIFEST TARGETS.
# ============================================================
def build_manifest_payload(worktree: Path, target_paths: Iterable[str]) -> bytes:
    """RETURN A SORTED SHA-256 MANIFEST WITHOUT SELF-REFERENCE."""

    manifest_path = "ops/evidence/AJAS_M1_PRESERVATION_MANIFEST.sha256"
    lines: list[str] = []
    for relative_path in sorted(target_paths):
        if relative_path == manifest_path:
            continue
        target = safe_target_path(worktree, relative_path)
        lines.append(f"{sha256_file(target)}  {relative_path}")
    return ("\n".join(lines) + "\n").encode("utf-8")


# ============================================================
# RETURN ONE NORMALIZED WORKTREE PATH FROM THE MAIN REPOSITORY.
# ============================================================
def preservation_worktree_path(repository: Path) -> Path:
    """RETURN THE REVIEWED SIBLING WORKTREE PATH."""

    return repository.parent / "AJAS-worktrees" / WORKTREE_DIRECTORY_NAME


# ============================================================
# PARSE A GIT WORKTREE PORCELAIN OUTPUT FOR ONE PATH.
# ============================================================
def worktree_path_registered(output: str, candidate: Path) -> bool:
    """RETURN TRUE WHEN GIT REPORTS THE CANDIDATE WORKTREE PATH."""

    expected = os.path.normcase(os.path.normpath(str(candidate.resolve(strict=False))))
    for line in output.splitlines():
        if not line.startswith("worktree "):
            continue
        reported = line[len("worktree ") :].strip()
        normalized = os.path.normcase(os.path.normpath(reported))
        if normalized == expected:
            return True
    return False


# ============================================================
# RUN THE COMPLETE LOCAL PRESERVATION APPLY OPERATION.
# ============================================================
def apply_preservation(
    *,
    repository: Path,
    downloads: Path,
    json_output: Path,
) -> int:
    """CREATE THE LOCAL PRESERVATION BRANCH, COMMIT, TAG, AND EVIDENCE."""

    run_utc = datetime.now(timezone.utc).isoformat()
    utility_path = Path(__file__).resolve()
    utility_digest = sha256_file(utility_path)
    git_executable = resolve_executable("git")
    worktree = preservation_worktree_path(repository)
    records: list[CommandRecord] = []
    artifact_audits: list[ArtifactAudit] = []
    target_audits: list[TargetAudit] = []
    written_file_audits: list[WrittenFileAudit] = []
    phase = "INITIALIZE"
    stop_reason: str | None = None
    preservation_commit: str | None = None
    tag_target: str | None = None
    git_mutations_attempted = False
    repository_files_written = False
    worktree_created = False
    commit_created = False
    tag_created = False
    final_status = "STOP"
    evidence_hash: str | None = None

    print(f"===== BEGIN AJAS M1 PRESERVATION APPLY v{UTILITY_VERSION} =====")
    print(f"RUN_UTC={run_utc}")
    print(f"UTILITY_VERSION={UTILITY_VERSION}")
    print(f"SCRIPT_SHA256={utility_digest}")
    print("MODE=APPLY")
    print("AZURE_COMMANDS_ATTEMPTED=False")
    print("GITHUB_NETWORK_COMMANDS_ATTEMPTED=False")
    print("REMOTE_PUSH_ATTEMPTED=False")
    print("BILLABLE_RESOURCES_CREATED=False")

    try:
        phase = "VALIDATE_PATHS"
        if git_executable is None:
            raise ControlledStop("GIT_EXECUTABLE_NOT_FOUND")
        if not repository.is_dir():
            raise ControlledStop("AUTHORITATIVE_REPOSITORY_NOT_FOUND")
        if not downloads.is_dir():
            raise ControlledStop("DOWNLOAD_DIRECTORY_NOT_FOUND")
        if path_is_within(json_output, repository):
            raise ControlledStop("JSON_OUTPUT_MUST_BE_OUTSIDE_REPOSITORY")
        if json_output.exists():
            raise ControlledStop("JSON_OUTPUT_ALREADY_EXISTS")
        if path_is_within(utility_path, repository):
            raise ControlledStop("APPLY_UTILITY_SOURCE_MUST_BE_OUTSIDE_REPOSITORY")

        phase = "READ_GIT_BASELINE"
        root_record = run_git_command(
            records=records,
            label="GIT_ROOT",
            git_executable=git_executable,
            repository=repository,
            arguments=["rev-parse", "--show-toplevel"],
        )
        branch_record = run_git_command(
            records=records,
            label="GIT_BRANCH",
            git_executable=git_executable,
            repository=repository,
            arguments=["branch", "--show-current"],
        )
        head_record = run_git_command(
            records=records,
            label="GIT_HEAD",
            git_executable=git_executable,
            repository=repository,
            arguments=["rev-parse", "HEAD"],
        )
        status_record = run_git_command(
            records=records,
            label="GIT_STATUS",
            git_executable=git_executable,
            repository=repository,
            arguments=["status", "--porcelain=v1", "--untracked-files=all"],
        )
        baseline_tag_record = run_git_command(
            records=records,
            label="GIT_BASELINE_TAG_TARGET",
            git_executable=git_executable,
            repository=repository,
            arguments=["rev-list", "-n", "1", EXPECTED_BASELINE_TAG],
        )
        tracked_record = run_git_command(
            records=records,
            label="GIT_TRACKED_FILES",
            git_executable=git_executable,
            repository=repository,
            arguments=["ls-files"],
        )
        remote_record = run_git_command(
            records=records,
            label="GIT_ORIGIN_REMOTE",
            git_executable=git_executable,
            repository=repository,
            arguments=["remote", "get-url", "origin"],
        )
        user_name_record = run_git_command(
            records=records,
            label="GIT_USER_NAME",
            git_executable=git_executable,
            repository=repository,
            arguments=["config", "--get", "user.name"],
        )
        user_email_record = run_git_command(
            records=records,
            label="GIT_USER_EMAIL",
            git_executable=git_executable,
            repository=repository,
            arguments=["config", "--get", "user.email"],
        )
        branch_list_record = run_git_command(
            records=records,
            label="GIT_PROPOSED_BRANCH_LIST",
            git_executable=git_executable,
            repository=repository,
            arguments=["branch", "--list", PRESERVATION_BRANCH],
        )
        tag_list_record = run_git_command(
            records=records,
            label="GIT_TAG_LIST",
            git_executable=git_executable,
            repository=repository,
            arguments=["tag", "--list", PRESERVATION_TAG],
        )
        worktree_list_record = run_git_command(
            records=records,
            label="GIT_WORKTREE_LIST",
            git_executable=git_executable,
            repository=repository,
            arguments=["worktree", "list", "--porcelain"],
        )

        for record, reason in (
            (root_record, "GIT_ROOT_READ_FAILED"),
            (branch_record, "GIT_BRANCH_READ_FAILED"),
            (head_record, "GIT_HEAD_READ_FAILED"),
            (status_record, "GIT_STATUS_READ_FAILED"),
            (baseline_tag_record, "BASELINE_TAG_READ_FAILED"),
            (tracked_record, "TRACKED_FILE_READ_FAILED"),
            (remote_record, "ORIGIN_REMOTE_READ_FAILED"),
            (user_name_record, "GIT_USER_NAME_READ_FAILED"),
            (user_email_record, "GIT_USER_EMAIL_READ_FAILED"),
            (branch_list_record, "BRANCH_EXISTENCE_READ_FAILED"),
            (tag_list_record, "TAG_EXISTENCE_READ_FAILED"),
            (worktree_list_record, "WORKTREE_LIST_READ_FAILED"),
        ):
            require_command_success(record, reason)

        root_matches = (
            os.path.normcase(os.path.normpath(root_record.stdout))
            == os.path.normcase(os.path.normpath(str(repository.resolve())))
        )
        tracked_file_count = len(
            [line for line in tracked_record.stdout.splitlines() if line]
        )
        remote_matches = normalize_remote(remote_record.stdout) == EXPECTED_REMOTE_URL
        branch_absent = branch_list_record.stdout == ""
        tag_absent = tag_list_record.stdout == ""
        worktree_unregistered = not worktree_path_registered(
            worktree_list_record.stdout, worktree
        )

        git_baseline_passes = all(
            [
                root_matches,
                branch_record.stdout == EXPECTED_BRANCH,
                head_record.stdout.lower() == EXPECTED_HEAD,
                status_record.stdout == "",
                baseline_tag_record.stdout.lower() == EXPECTED_HEAD,
                tracked_file_count == EXPECTED_TRACKED_FILE_COUNT,
                remote_matches,
                user_name_record.stdout != "",
                user_email_record.stdout != "",
                branch_absent,
                tag_absent,
                worktree_unregistered,
                not worktree.exists(),
            ]
        )
        if not git_baseline_passes:
            raise ControlledStop("FRESH_GIT_BASELINE_GATE_FAILED")

        phase = "AUDIT_SOURCE_ARTIFACTS"
        artifact_audits = [
            audit_artifact(downloads, spec) for spec in REQUIRED_ARTIFACTS
        ]
        for audit in artifact_audits:
            if not audit.exists:
                raise ControlledStop(f"SOURCE_ARTIFACT_MISSING:{audit.filename}")
            if not audit.is_file or audit.is_symlink:
                raise ControlledStop(f"SOURCE_ARTIFACT_TYPE_INVALID:{audit.filename}")
            if audit.bytes is None or audit.bytes > MAX_ARTIFACT_BYTES:
                raise ControlledStop(f"SOURCE_ARTIFACT_SIZE_INVALID:{audit.filename}")
            if not audit.hash_matches:
                raise ControlledStop(f"SOURCE_ARTIFACT_HASH_MISMATCH:{audit.filename}")
            if audit.high_confidence_secret_rules:
                raise ControlledStop(
                    "SOURCE_ARTIFACT_SECRET_RULE_MATCH:"
                    + audit.filename
                    + ":"
                    + ",".join(audit.high_confidence_secret_rules)
                )

        self_findings = scan_file_secret_rule_names(utility_path)
        if self_findings:
            raise ControlledStop(
                "APPLY_UTILITY_SECRET_RULE_MATCH:" + ",".join(self_findings)
            )

        phase = "VALIDATE_MACHINE_EVIDENCE"
        reconciliation_path = downloads / RECONCILIATION_EVIDENCE_NAME
        preflight_path = downloads / PREFLIGHT_EVIDENCE_NAME
        reconciliation_valid, reconciliation_errors = (
            validate_reconciliation_evidence(read_json_dict(reconciliation_path))
        )
        preflight_valid, preflight_errors = validate_preflight_evidence(
            read_json_dict(preflight_path)
        )
        if not reconciliation_valid:
            raise ControlledStop(
                "RECONCILIATION_EVIDENCE_INVALID:"
                + ",".join(reconciliation_errors)
            )
        if not preflight_valid:
            raise ControlledStop(
                "PREFLIGHT_EVIDENCE_INVALID:" + ",".join(preflight_errors)
            )

        phase = "RUN_REQUIRED_REGRESSION_TESTS"
        v012_path = downloads / "ajas_m1_readonly_reconcile_v0_1_2.py"
        v012_record = run_process(
            label="PYTHON_V0_1_2_SELF_TEST",
            executable=Path(sys.executable),
            arguments=[str(v012_path), "--mode", "self-test"],
            working_directory=downloads,
            timeout_seconds=180,
        )
        records.append(v012_record)
        require_command_success(v012_record, "V0_1_2_SELF_TEST_FAILED")
        required_v012_markers = (
            "SELF_TEST_CONTAMINATED_AZURE_STDOUT=PASS",
            "SELF_TEST_CONTAMINATED_TSV_BOOLEAN=PASS",
            "SELF_TEST_CONTAMINATED_NONNEGATIVE_INTEGER=PASS",
            "SELF_TEST_SCALAR_AMBIGUITY_FAIL_CLOSED=PASS",
            "SELF_TEST_SCALAR_TRAILING_CONTAMINATION_FAIL_CLOSED=PASS",
            "AJAS_READ_ONLY_RECONCILIATION_SELF_TEST_v0.1.2=PASS",
        )
        if not all(marker in v012_record.stdout for marker in required_v012_markers):
            raise ControlledStop("V0_1_2_SELF_TEST_MARKERS_MISSING")

        phase = "AUDIT_FINAL_TARGET_PLAN"
        targets = planned_target_paths()
        for relative_path in targets:
            baseline_target = safe_target_path(repository, relative_path)
            ignore_record = run_git_command(
                records=records,
                label="GIT_TARGET_CHECK_IGNORE",
                git_executable=git_executable,
                repository=repository,
                arguments=["check-ignore", "--no-index", "--", relative_path],
            )
            ignored: bool | None
            if ignore_record.exit_code == 0:
                ignored = True
            elif ignore_record.exit_code == 1:
                ignored = False
            else:
                ignored = None
            target_audits.append(
                TargetAudit(
                    relative_path=relative_path,
                    exists_in_baseline=baseline_target.exists(),
                    ignored=ignored,
                    check_ignore_exit_code=ignore_record.exit_code,
                    ignore_stderr=ignore_record.stderr,
                )
            )

        if any(audit.exists_in_baseline for audit in target_audits):
            raise ControlledStop("TARGET_COLLISION_DETECTED")
        if any(audit.ignored is not False for audit in target_audits):
            raise ControlledStop("TARGET_IGNORE_STATE_NOT_CLEAN")

        phase = "CREATE_DISPOSABLE_WORKTREE"
        worktree.parent.mkdir(parents=True, exist_ok=True)
        git_mutations_attempted = True
        worktree_add_record = run_git_command(
            records=records,
            label="GIT_WORKTREE_ADD",
            git_executable=git_executable,
            repository=repository,
            arguments=[
                "worktree",
                "add",
                "-b",
                PRESERVATION_BRANCH,
                str(worktree),
                EXPECTED_HEAD,
            ],
            timeout_seconds=300,
        )
        require_command_success(worktree_add_record, "GIT_WORKTREE_ADD_FAILED")
        worktree_created = True

        phase = "VERIFY_NEW_WORKTREE_BASELINE"
        worktree_branch_record = run_git_command(
            records=records,
            label="GIT_WORKTREE_BRANCH_VERIFY",
            git_executable=git_executable,
            repository=worktree,
            arguments=["branch", "--show-current"],
        )
        worktree_head_record = run_git_command(
            records=records,
            label="GIT_WORKTREE_HEAD_VERIFY",
            git_executable=git_executable,
            repository=worktree,
            arguments=["rev-parse", "HEAD"],
        )
        worktree_status_record = run_git_command(
            records=records,
            label="GIT_WORKTREE_STATUS_BEFORE_WRITE",
            git_executable=git_executable,
            repository=worktree,
            arguments=["status", "--porcelain=v1", "--untracked-files=all"],
        )
        for record, reason in (
            (worktree_branch_record, "WORKTREE_BRANCH_VERIFY_FAILED"),
            (worktree_head_record, "WORKTREE_HEAD_VERIFY_FAILED"),
            (worktree_status_record, "WORKTREE_STATUS_VERIFY_FAILED"),
        ):
            require_command_success(record, reason)
        if worktree_branch_record.stdout != PRESERVATION_BRANCH:
            raise ControlledStop("WORKTREE_BRANCH_MISMATCH")
        if worktree_head_record.stdout.lower() != EXPECTED_HEAD:
            raise ControlledStop("WORKTREE_HEAD_MISMATCH")
        if worktree_status_record.stdout != "":
            raise ControlledStop("NEW_WORKTREE_NOT_CLEAN")

        phase = "WRITE_PRESERVATION_CONTENT"
        repository_files_written = True
        generated_documents = build_generated_documents(utility_digest)

        for spec in REQUIRED_ARTIFACTS:
            source = downloads / spec.filename
            target = safe_target_path(worktree, spec.target_relative_path)
            write_exclusive(target, source.read_bytes())

        self_target = safe_target_path(worktree, SELF_TARGET_RELATIVE_PATH)
        write_exclusive(self_target, utility_path.read_bytes())

        for relative_path, payload in generated_documents.items():
            target = safe_target_path(worktree, relative_path)
            write_exclusive(target, payload)

        manifest_relative_path = (
            "ops/evidence/AJAS_M1_PRESERVATION_MANIFEST.sha256"
        )
        non_manifest_targets = [
            relative_path
            for relative_path in targets
            if relative_path != manifest_relative_path
        ]
        manifest_payload = build_manifest_payload(worktree, non_manifest_targets)
        write_exclusive(
            safe_target_path(worktree, manifest_relative_path),
            manifest_payload,
        )

        phase = "VERIFY_WRITTEN_CONTENT"
        expected_hash_by_target = {
            spec.target_relative_path: spec.expected_sha256
            for spec in REQUIRED_ARTIFACTS
        }
        expected_hash_by_target[SELF_TARGET_RELATIVE_PATH] = utility_digest

        for relative_path in targets:
            target = safe_target_path(worktree, relative_path)
            if not target.is_file() or target.is_symlink():
                raise ControlledStop(f"WRITTEN_TARGET_TYPE_INVALID:{relative_path}")
            digest = sha256_file(target)
            expected_digest = expected_hash_by_target.get(relative_path)
            findings = scan_file_secret_rule_names(target)
            written_file_audits.append(
                WrittenFileAudit(
                    relative_path=relative_path,
                    bytes=target.stat().st_size,
                    sha256=digest,
                    expected_sha256=expected_digest,
                    hash_matches_expected=(
                        None if expected_digest is None else digest == expected_digest
                    ),
                    high_confidence_secret_rules=findings,
                )
            )
            if expected_digest is not None and digest != expected_digest:
                raise ControlledStop(f"WRITTEN_TARGET_HASH_MISMATCH:{relative_path}")
            if findings:
                raise ControlledStop(
                    "WRITTEN_TARGET_SECRET_RULE_MATCH:"
                    + relative_path
                    + ":"
                    + ",".join(findings)
                )

        for relative_path in targets:
            if relative_path.endswith(".py"):
                compile_python_source(safe_target_path(worktree, relative_path))

        copied_v012_record = run_process(
            label="PYTHON_COPIED_V0_1_2_SELF_TEST",
            executable=Path(sys.executable),
            arguments=[
                str(
                    safe_target_path(
                        worktree,
                        "scripts/ops/ajas_m1_readonly_reconcile_v0_1_2.py",
                    )
                ),
                "--mode",
                "self-test",
            ],
            working_directory=worktree,
            timeout_seconds=180,
        )
        records.append(copied_v012_record)
        require_command_success(
            copied_v012_record, "COPIED_V0_1_2_SELF_TEST_FAILED"
        )

        phase = "STAGE_EXACT_TARGET_SET"
        stage_record = run_git_command(
            records=records,
            label="GIT_STAGE_TARGETS",
            git_executable=git_executable,
            repository=worktree,
            arguments=["add", "--", *targets],
        )
        require_command_success(stage_record, "GIT_STAGE_FAILED")

        diff_check_record = run_git_command(
            records=records,
            label="GIT_DIFF_CACHED_CHECK",
            git_executable=git_executable,
            repository=worktree,
            arguments=["diff", "--cached", "--check"],
        )
        require_command_success(diff_check_record, "GIT_DIFF_CACHED_CHECK_FAILED")

        staged_names_record = run_git_command(
            records=records,
            label="GIT_DIFF_CACHED_NAMES",
            git_executable=git_executable,
            repository=worktree,
            arguments=[
                "diff",
                "--cached",
                "--name-only",
                "--diff-filter=ACMRTUXB",
            ],
        )
        require_command_success(staged_names_record, "STAGED_NAME_READ_FAILED")
        staged_names = tuple(
            sorted(line for line in staged_names_record.stdout.splitlines() if line)
        )
        if staged_names != targets:
            raise ControlledStop("STAGED_TARGET_SET_MISMATCH")

        phase = "COMMIT_PRESERVATION_CONTENT"
        commit_record = run_git_command(
            records=records,
            label="GIT_COMMIT",
            git_executable=git_executable,
            repository=worktree,
            arguments=["commit", "--no-gpg-sign", "-m", COMMIT_MESSAGE],
            timeout_seconds=300,
        )
        require_command_success(commit_record, "GIT_COMMIT_FAILED")
        commit_created = True

        commit_hash_record = run_git_command(
            records=records,
            label="GIT_COMMIT_HASH_VERIFY",
            git_executable=git_executable,
            repository=worktree,
            arguments=["rev-parse", "HEAD"],
        )
        require_command_success(commit_hash_record, "COMMIT_HASH_READ_FAILED")
        preservation_commit = commit_hash_record.stdout.lower()
        if not re.fullmatch(r"[0-9a-f]{40}", preservation_commit):
            raise ControlledStop("COMMIT_HASH_INVALID")

        parent_record = run_git_command(
            records=records,
            label="GIT_COMMIT_PARENT_VERIFY",
            git_executable=git_executable,
            repository=worktree,
            arguments=["rev-parse", "HEAD^"],
        )
        require_command_success(parent_record, "COMMIT_PARENT_READ_FAILED")
        if parent_record.stdout.lower() != EXPECTED_HEAD:
            raise ControlledStop("PRESERVATION_COMMIT_PARENT_MISMATCH")

        worktree_clean_record = run_git_command(
            records=records,
            label="GIT_WORKTREE_STATUS_AFTER_COMMIT",
            git_executable=git_executable,
            repository=worktree,
            arguments=["status", "--porcelain=v1", "--untracked-files=all"],
        )
        require_command_success(
            worktree_clean_record, "WORKTREE_POST_COMMIT_STATUS_FAILED"
        )
        if worktree_clean_record.stdout != "":
            raise ControlledStop("WORKTREE_NOT_CLEAN_AFTER_COMMIT")

        phase = "CREATE_LOCAL_CHECKPOINT_TAG"
        tag_recheck_record = run_git_command(
            records=records,
            label="GIT_TAG_TARGET_RECHECK",
            git_executable=git_executable,
            repository=repository,
            arguments=["tag", "--list", PRESERVATION_TAG],
        )
        require_command_success(tag_recheck_record, "TAG_RECHECK_FAILED")
        if tag_recheck_record.stdout != "":
            raise ControlledStop("PRESERVATION_TAG_APPEARED_BEFORE_CREATE")

        tag_create_record = run_git_command(
            records=records,
            label="GIT_TAG_CREATE",
            git_executable=git_executable,
            repository=repository,
            arguments=["tag", PRESERVATION_TAG, preservation_commit],
        )
        require_command_success(tag_create_record, "GIT_TAG_CREATE_FAILED")
        tag_created = True

        tag_verify_record = run_git_command(
            records=records,
            label="GIT_TAG_VERIFY",
            git_executable=git_executable,
            repository=repository,
            arguments=["tag", "--list", PRESERVATION_TAG],
        )
        tag_target_record = run_git_command(
            records=records,
            label="GIT_TAG_TARGET_VERIFY",
            git_executable=git_executable,
            repository=repository,
            arguments=["rev-list", "-n", "1", PRESERVATION_TAG],
        )
        require_command_success(tag_verify_record, "TAG_VERIFY_FAILED")
        require_command_success(tag_target_record, "TAG_TARGET_VERIFY_FAILED")
        tag_target = tag_target_record.stdout.lower()
        if tag_verify_record.stdout != PRESERVATION_TAG:
            raise ControlledStop("PRESERVATION_TAG_NAME_VERIFY_FAILED")
        if tag_target != preservation_commit:
            raise ControlledStop("PRESERVATION_TAG_TARGET_MISMATCH")

        phase = "VERIFY_MAIN_UNCHANGED"
        main_head_record = run_git_command(
            records=records,
            label="GIT_MAIN_HEAD_FINAL",
            git_executable=git_executable,
            repository=repository,
            arguments=["rev-parse", "HEAD"],
        )
        main_branch_record = run_git_command(
            records=records,
            label="GIT_MAIN_BRANCH_FINAL",
            git_executable=git_executable,
            repository=repository,
            arguments=["branch", "--show-current"],
        )
        main_status_record = run_git_command(
            records=records,
            label="GIT_MAIN_STATUS_FINAL",
            git_executable=git_executable,
            repository=repository,
            arguments=["status", "--porcelain=v1", "--untracked-files=all"],
        )
        branch_ref_record = run_git_command(
            records=records,
            label="GIT_PRESERVATION_BRANCH_REF_VERIFY",
            git_executable=git_executable,
            repository=repository,
            arguments=["rev-parse", PRESERVATION_BRANCH],
        )
        for record, reason in (
            (main_head_record, "MAIN_HEAD_FINAL_READ_FAILED"),
            (main_branch_record, "MAIN_BRANCH_FINAL_READ_FAILED"),
            (main_status_record, "MAIN_STATUS_FINAL_READ_FAILED"),
            (branch_ref_record, "PRESERVATION_BRANCH_REF_READ_FAILED"),
        ):
            require_command_success(record, reason)
        if main_head_record.stdout.lower() != EXPECTED_HEAD:
            raise ControlledStop("MAIN_HEAD_CHANGED")
        if main_branch_record.stdout != EXPECTED_BRANCH:
            raise ControlledStop("MAIN_BRANCH_CHANGED")
        if main_status_record.stdout != "":
            raise ControlledStop("MAIN_WORKTREE_DIRTY")
        if branch_ref_record.stdout.lower() != preservation_commit:
            raise ControlledStop("PRESERVATION_BRANCH_REF_MISMATCH")

        final_status = "PASS"
        phase = "COMPLETE"

    except ControlledStop as error:
        stop_reason = str(error)
    except Exception as error:  # noqa: BLE001 - CONVERT TO STRUCTURED EVIDENCE.
        stop_reason = f"UNEXPECTED_{type(error).__name__}:{error}"

    evidence_payload: dict[str, Any] = {
        "evidence_schema_version": EVIDENCE_SCHEMA_VERSION,
        "run_utc": run_utc,
        "utility": {
            "name": "ajas_m1_preservation_apply",
            "version": UTILITY_VERSION,
            "script_sha256": utility_digest,
            "mode": "apply",
        },
        "safety": {
            "azure_commands_attempted": False,
            "github_network_commands_attempted": False,
            "remote_push_attempted": False,
            "billable_resources_created": False,
            "source_repository_worktree_files_written": False,
            "json_output_outside_repository": not path_is_within(
                json_output, repository
            ),
        },
        "plan": {
            "repository": str(repository),
            "downloads": str(downloads),
            "preservation_branch": PRESERVATION_BRANCH,
            "preservation_tag": PRESERVATION_TAG,
            "worktree": str(worktree),
            "commit_message": COMMIT_MESSAGE,
            "target_paths": list(planned_target_paths()),
            "private_repository_required_before_push": True,
            "remote_push_deferred": True,
        },
        "execution": {
            "phase": phase,
            "status": final_status,
            "stop_reason": stop_reason,
            "git_mutations_attempted": git_mutations_attempted,
            "repository_files_written": repository_files_written,
            "worktree_created": worktree_created,
            "commit_created": commit_created,
            "tag_created": tag_created,
            "preservation_commit": preservation_commit,
            "tag_target": tag_target,
        },
        "artifact_audits": [asdict(audit) for audit in artifact_audits],
        "target_audits": [asdict(audit) for audit in target_audits],
        "written_file_audits": [
            asdict(audit) for audit in written_file_audits
        ],
        "commands": [asdict(record) for record in records],
    }

    try:
        evidence_hash = write_json_exclusive(json_output, evidence_payload)
        print("EVIDENCE_OUTPUT_STATUS=WRITTEN")
        print(f"EVIDENCE_OUTPUT_PATH={json_output}")
        print(f"EVIDENCE_OUTPUT_SHA256={evidence_hash}")
    except Exception as error:  # noqa: BLE001 - FINAL EVIDENCE WRITE REPORT.
        print("EVIDENCE_OUTPUT_STATUS=STOP")
        print(f"EVIDENCE_OUTPUT_ERROR={type(error).__name__}:{error}")
        if final_status == "PASS":
            final_status = "STOP"
            stop_reason = "PRESERVATION_COMPLETED_BUT_EVIDENCE_WRITE_FAILED"

    print("===== COMMAND AUDIT BEGIN =====")
    for record in records:
        print_command_record(record)
    print("===== COMMAND AUDIT END =====")

    print("===== PRESERVATION RESULT BEGIN =====")
    print(f"PRESERVATION_STATUS={final_status}")
    print(f"STOP_PHASE={phase if final_status != 'PASS' else 'NONE'}")
    print(f"STOP_REASON={stop_reason if stop_reason is not None else 'NONE'}")
    print(f"PRESERVATION_BRANCH={PRESERVATION_BRANCH}")
    print(f"PRESERVATION_COMMIT={preservation_commit or 'NONE'}")
    print(f"PRESERVATION_TAG={PRESERVATION_TAG}")
    print(f"PRESERVATION_TAG_TARGET={tag_target or 'NONE'}")
    print(f"PRESERVATION_WORKTREE={worktree}")
    print(f"WORKTREE_CREATED={marker_bool(worktree_created)}")
    print(f"COMMIT_CREATED={marker_bool(commit_created)}")
    print(f"TAG_CREATED={marker_bool(tag_created)}")
    print(f"MAIN_EXPECTED_HEAD={EXPECTED_HEAD}")
    print("MAIN_SOURCE_WORKTREE_FILES_WRITTEN=False")
    print("REMOTE_PUSH_ATTEMPTED=False")
    print("GITHUB_NETWORK_COMMANDS_ATTEMPTED=False")
    print("AZURE_COMMANDS_ATTEMPTED=False")
    print("BILLABLE_RESOURCES_CREATED=False")
    print("PRIVATE_REPOSITORY_VERIFICATION_REQUIRED_BEFORE_PUSH=True")
    print("===== PRESERVATION RESULT END =====")
    print(f"===== END AJAS M1 PRESERVATION APPLY v{UTILITY_VERSION} =====")

    return 0 if final_status == "PASS" else 2


# ============================================================
# PARSE COMMAND-LINE ARGUMENTS.
# ============================================================
def parse_arguments() -> argparse.Namespace:
    """RETURN VALIDATED COMMAND-LINE ARGUMENTS."""

    parser = argparse.ArgumentParser(
        description=(
            "Create the local AJAS Milestone-1B preservation branch, commit, "
            "tag, and evidence without Azure or GitHub network operations."
        )
    )
    parser.add_argument(
        "--mode",
        choices=("self-test", "apply"),
        required=True,
        help="Run pure self-tests or the controlled local preservation apply.",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=DEFAULT_REPOSITORY,
        help="Authoritative AJAS repository path.",
    )
    parser.add_argument(
        "--downloads",
        type=Path,
        default=DEFAULT_DOWNLOADS,
        help="Directory containing verified source artifacts and evidence.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="New outside-repository JSON evidence path required for apply mode.",
    )
    return parser.parse_args()


# ============================================================
# DISPATCH THE REQUESTED MODE.
# ============================================================
def main() -> int:
    """RUN SELF-TEST OR CONTROLLED LOCAL PRESERVATION APPLY."""

    arguments = parse_arguments()
    if arguments.mode == "self-test":
        return run_self_test()
    if arguments.json_output is None:
        print("PRESERVATION_STATUS=STOP")
        print("STOP_REASON=JSON_OUTPUT_REQUIRED_FOR_APPLY")
        return 2
    return apply_preservation(
        repository=arguments.repo.resolve(),
        downloads=arguments.downloads.resolve(),
        json_output=arguments.json_output.resolve(),
    )


# ============================================================
# EXECUTE ONLY WHEN RUN AS A SCRIPT.
# ============================================================
if __name__ == "__main__":
    raise SystemExit(main())
