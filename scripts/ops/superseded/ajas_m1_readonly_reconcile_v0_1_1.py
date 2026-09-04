#!/usr/bin/env python3
"""
AJAS MILESTONE 1 READ-ONLY RECONCILIATION UTILITY, VERSION 0.1.1.

PURPOSE:
- READ THE CURRENT LOCAL GIT CHECKPOINT.
- READ THE CURRENT AZURE SUBSCRIPTION CONTEXT.
- READ THE INSTALLED CONTAINERAPP EXTENSION STATE AND VERSION.
- READ THE AJAS RESOURCE-GROUP EXISTENCE AND RESOURCE COUNT.
- READ THE PROPOSED AZURE CONTAINER REGISTRY NAME AVAILABILITY.

SAFETY GUARANTEES:
- NO GIT MUTATION COMMANDS.
- NO AZURE CREATE, UPDATE, DELETE, SET, ADD, INSTALL, OR LOGIN COMMANDS.
- NO BILLABLE RESOURCE CREATION.
- NO FILE OUTPUT UNLESS --json-output EXPLICITLY REQUESTS AN EVIDENCE FILE.
- JSON PAYLOADS MAY FOLLOW AUDITED NON-JSON STDOUT PREFIX TEXT.
- ANY DISCARDED STDOUT PREFIX IS RECORDED; NO PREFIX IS SILENTLY SWALLOWED.
- STDOUT AND STDERR REMAIN SEPARATE FOR EVERY CHILD PROCESS.
- MISSING STDOUT AND STDERR VALUES ARE NORMALIZED BEFORE STRING OPERATIONS.
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
# IMPORT HASHING SUPPORT FOR SCRIPT IDENTITY.
# ============================================================
import hashlib

# ============================================================
# IMPORT JSON PARSING AND SERIALIZATION SUPPORT.
# ============================================================
import json

# ============================================================
# IMPORT OPERATING-SYSTEM SUPPORT.
# ============================================================
import os

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
# IMPORT IMMUTABLE COMMAND-RECORD SUPPORT.
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
UTILITY_VERSION: Final[str] = "0.1.1"

# ============================================================
# DECLARE THE AUTHORITATIVE AJAS REPOSITORY PATH.
# ============================================================
DEFAULT_REPOSITORY: Final[Path] = Path(r"C:\Users\steve\Code\AJAS")

# ============================================================
# DECLARE THE EXPECTED MILESTONE-0 BRANCH.
# ============================================================
EXPECTED_BRANCH: Final[str] = "main"

# ============================================================
# DECLARE THE EXPECTED MILESTONE-0 COMMIT.
# ============================================================
EXPECTED_HEAD: Final[str] = "df08693da3157504d7f4a10dcb840969950bd184"

# ============================================================
# DECLARE THE EXPECTED MILESTONE-0 TAG.
# ============================================================
EXPECTED_TAG: Final[str] = "milestone0-complete"

# ============================================================
# DECLARE THE EXPECTED AZURE SUBSCRIPTION IDENTIFIER.
# ============================================================
EXPECTED_SUBSCRIPTION_ID: Final[str] = "efe2c2b2-d541-4b47-952d-e1af59db9910"

# ============================================================
# DECLARE THE PROPOSED AJAS RESOURCE-GROUP NAME.
# ============================================================
RESOURCE_GROUP_NAME: Final[str] = "rg-ajas-personal-alpha-wus3"

# ============================================================
# DECLARE THE PROPOSED AZURE CONTAINER REGISTRY NAME.
# ============================================================
CONTAINER_REGISTRY_NAME: Final[str] = "acrajas59db9910"

# ============================================================
# DECLARE THE AZURE CLI EXTENSION NAME UNDER INSPECTION.
# ============================================================
CONTAINERAPP_EXTENSION_NAME: Final[str] = "containerapp"


# ============================================================
# STORE EACH CHILD-PROCESS RESULT WITHOUT MERGING OUTPUT STREAMS.
# ============================================================
@dataclass(frozen=True)
class CommandRecord:
    """STORE ONE READ-ONLY COMMAND INVOCATION AND SEPARATE OUTPUT STREAMS."""

    # ========================================================
    # STORE A STABLE COMMAND LABEL.
    # ========================================================
    label: str

    # ========================================================
    # STORE THE HUMAN-READABLE LOGICAL COMMAND.
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
# STORE JSON-PARSER EVIDENCE WITHOUT ALTERING THE COMMAND RECORD.
# ============================================================
@dataclass(frozen=True)
class JsonParseAudit:
    """STORE PAYLOAD DISCOVERY, TYPE VALIDATION, AND PREFIX EVIDENCE."""

    # ========================================================
    # STORE THE PARSER RESULT STATUS.
    # ========================================================
    status: str

    # ========================================================
    # STORE THE REQUIRED TOP-LEVEL JSON CONTAINER TYPE.
    # ========================================================
    expected_type: str

    # ========================================================
    # STORE THE OBSERVED TOP-LEVEL JSON TYPE WHEN AVAILABLE.
    # ========================================================
    actual_type: str

    # ========================================================
    # STORE THE ONE-BASED LINE NUMBER WHERE THE JSON PAYLOAD BEGAN.
    # ========================================================
    payload_start_line: int | None

    # ========================================================
    # STORE ANY NON-JSON STDOUT PREFIX REMOVED BEFORE PARSING.
    # ========================================================
    stdout_prefix_discarded: str

    # ========================================================
    # STORE A CALM PARSER ERROR DESCRIPTION WHEN PARSING FAILS.
    # ========================================================
    error: str


# ============================================================
# NORMALIZE A POSSIBLY MISSING TEXT VALUE.
# ============================================================
def normalize_text(value: str | bytes | None) -> str:
    """CONVERT A MISSING OR BYTE OUTPUT VALUE TO SAFE TEXT."""

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
    # RETURN THE ORIGINAL TEXT FOR A PRESENT STRING.
    # ========================================================
    return value


# ============================================================
# CONVERT A BOOLEAN VALUE TO A STABLE MARKER.
# ============================================================
def marker_bool(value: bool | None) -> str:
    """RENDER TRUE, FALSE, OR UNKNOWN WITHOUT AMBIGUOUS BLANKS."""

    # ========================================================
    # RETURN UNKNOWN FOR A MISSING BOOLEAN.
    # ========================================================
    if value is None:
        return "UNKNOWN"

    # ========================================================
    # RETURN TRUE FOR A TRUE BOOLEAN.
    # ========================================================
    if value:
        return "True"

    # ========================================================
    # RETURN FALSE FOR A FALSE BOOLEAN.
    # ========================================================
    return "False"


# ============================================================
# RENDER OPTIONAL TEXT AS A SINGLE MACHINE-READABLE FIELD VALUE.
# ============================================================
def marker_text(value: str | None) -> str:
    """RENDER NONE OR JSON-ESCAPED TEXT WITHOUT MULTILINE FIELD BREAKAGE."""

    # ========================================================
    # RETURN NONE FOR A MISSING OR EMPTY VALUE.
    # ========================================================
    if value is None or value == "":
        return "NONE"

    # ========================================================
    # RETURN JSON-ESCAPED TEXT ON ONE PHYSICAL OUTPUT LINE.
    # ========================================================
    return json.dumps(value, ensure_ascii=False)


# ============================================================
# COMPUTE THE SHA-256 DIGEST OF THE RUNNING SCRIPT.
# ============================================================
def script_sha256() -> str:
    """RETURN A MACHINE-READABLE SCRIPT IDENTITY DIGEST."""

    # ========================================================
    # RESOLVE THE RUNNING SCRIPT PATH.
    # ========================================================
    script_path = Path(__file__).resolve()

    # ========================================================
    # READ THE SCRIPT BYTES.
    # ========================================================
    script_bytes = script_path.read_bytes()

    # ========================================================
    # RETURN THE UPPERCASE SHA-256 DIGEST.
    # ========================================================
    return hashlib.sha256(script_bytes).hexdigest().upper()


# ============================================================
# FIND A REQUIRED EXECUTABLE WITHOUT CHANGING SYSTEM STATE.
# ============================================================
def resolve_executable(name: str) -> Path | None:
    """RETURN AN EXECUTABLE PATH OR NONE WHEN THE EXECUTABLE IS ABSENT."""

    # ========================================================
    # ASK THE OPERATING SYSTEM TO SEARCH THE CURRENT PATH.
    # ========================================================
    resolved = shutil.which(name)

    # ========================================================
    # RETURN NONE WHEN DISCOVERY FAILS.
    # ========================================================
    if resolved is None:
        return None

    # ========================================================
    # RETURN A NORMALIZED PATH WHEN DISCOVERY SUCCEEDS.
    # ========================================================
    return Path(resolved)


# ============================================================
# BUILD A DIRECT PROCESS ARGUMENT VECTOR.
# ============================================================
def build_execution_argv(executable: Path, arguments: Sequence[str]) -> list[str]:
    """RETURN A FULLY QUALIFIED EXECUTABLE AND TRUSTED ARGUMENT SEQUENCE."""

    # ========================================================
    # RETURN THE FULL EXECUTABLE PATH AND SEPARATE ARGUMENTS.
    # ========================================================
    return [str(executable), *arguments]


# ============================================================
# RUN ONE READ-ONLY COMMAND WITH SEPARATE OUTPUT STREAMS.
# ============================================================
def run_read_only_command(
    label: str,
    executable: Path,
    arguments: Sequence[str],
    working_directory: Path | None = None,
) -> CommandRecord:
    """EXECUTE ONE FIXED READ-ONLY COMMAND AND RETURN A STRUCTURED RECORD."""

    # ========================================================
    # BUILD THE HUMAN-READABLE LOGICAL COMMAND.
    # ========================================================
    logical_command = subprocess.list2cmdline([str(executable), *arguments])

    # ========================================================
    # BUILD THE OPERATING-SYSTEM-SAFE ARGUMENT VECTOR.
    # ========================================================
    execution_argv = build_execution_argv(executable, arguments)

    # ========================================================
    # COPY THE CURRENT ENVIRONMENT WITHOUT EDITING GLOBAL STATE.
    # ========================================================
    child_environment = os.environ.copy()

    # ========================================================
    # DISABLE AZURE CLI DYNAMIC EXTENSION INSTALLATION FOR THIS PROCESS TREE.
    # ========================================================
    child_environment["AZURE_EXTENSION_USE_DYNAMIC_INSTALL"] = "no"

    # ========================================================
    # DISABLE AZURE CLI TELEMETRY FOR THIS PROCESS TREE.
    # ========================================================
    child_environment["AZURE_CORE_COLLECT_TELEMETRY"] = "no"

    # ========================================================
    # EXECUTE WITHOUT SHELL EXPANSION OR STREAM MERGING.
    # ========================================================
    try:
        completed = subprocess.run(
            execution_argv,
            cwd=str(working_directory) if working_directory is not None else None,
            env=child_environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            shell=False,
            timeout=120,
        )

    # ========================================================
    # CONVERT A PROCESS-LAUNCH FAILURE INTO STRUCTURED OUTPUT.
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
    # CONVERT A COMMAND TIMEOUT INTO STRUCTURED OUTPUT.
    # ========================================================
    except subprocess.TimeoutExpired as error:
        timeout_stdout = normalize_text(error.stdout).strip()
        timeout_stderr = normalize_text(error.stderr).strip()
        timeout_message = "PROCESS_TIMEOUT_SECONDS=120"
        combined_stderr = (
            f"{timeout_stderr}\n{timeout_message}"
            if timeout_stderr != ""
            else timeout_message
        )
        return CommandRecord(
            label=label,
            logical_command=logical_command,
            exit_code=124,
            stdout=timeout_stdout,
            stderr=combined_stderr,
        )

    # ========================================================
    # NORMALIZE STANDARD OUTPUT BEFORE STRING OPERATIONS.
    # ========================================================
    normalized_stdout = normalize_text(completed.stdout).strip()

    # ========================================================
    # NORMALIZE STANDARD ERROR BEFORE STRING OPERATIONS.
    # ========================================================
    normalized_stderr = normalize_text(completed.stderr).strip()

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
# CREATE A SYNTHETIC RECORD WHEN AN EXECUTABLE IS ABSENT.
# ============================================================
def missing_executable_record(label: str, executable_name: str) -> CommandRecord:
    """RETURN A STRUCTURED FAILURE WITHOUT RAISING A STACK TRACE."""

    # ========================================================
    # RETURN A CALM, MACHINE-READABLE MISSING-TOOL RESULT.
    # ========================================================
    return CommandRecord(
        label=label,
        logical_command=executable_name,
        exit_code=127,
        stdout="",
        stderr=f"REQUIRED_EXECUTABLE_NOT_FOUND={executable_name}",
    )


# ============================================================
# LOCATE, PARSE, AND TYPE-CHECK A JSON OBJECT OR ARRAY IN STDOUT.
# ============================================================
def parse_json_record(
    record: CommandRecord,
    expected_type: type[dict[Any, Any]] | type[list[Any]],
) -> tuple[Any | None, JsonParseAudit]:
    """RETURN A VALIDATED JSON VALUE PLUS AN AUDIT OF PAYLOAD DISCOVERY."""

    # ========================================================
    # REJECT AN UNSUPPORTED EXPECTED TOP-LEVEL TYPE.
    # ========================================================
    if expected_type not in (dict, list):
        raise ValueError("EXPECTED_JSON_TYPE_MUST_BE_DICT_OR_LIST")

    # ========================================================
    # STORE THE EXPECTED TYPE NAME FOR STRUCTURED EVIDENCE.
    # ========================================================
    expected_type_name = expected_type.__name__

    # ========================================================
    # REJECT A FAILED COMMAND.
    # ========================================================
    if record.exit_code != 0:
        return None, JsonParseAudit(
            status="COMMAND_FAILED",
            expected_type=expected_type_name,
            actual_type="UNKNOWN",
            payload_start_line=None,
            stdout_prefix_discarded="",
            error=f"COMMAND_EXIT_CODE={record.exit_code}",
        )

    # ========================================================
    # REJECT EMPTY STANDARD OUTPUT.
    # ========================================================
    if record.stdout == "":
        return None, JsonParseAudit(
            status="EMPTY_STDOUT",
            expected_type=expected_type_name,
            actual_type="UNKNOWN",
            payload_start_line=None,
            stdout_prefix_discarded="",
            error="STDOUT_WAS_EMPTY",
        )

    # ========================================================
    # PRESERVE LINE ENDINGS SO THE PREFIX CAN BE RECONSTRUCTED.
    # ========================================================
    stdout_lines = record.stdout.splitlines(keepends=True)

    # ========================================================
    # INITIALIZE THE FIRST JSON-CONTAINER CANDIDATE LOCATION.
    # ========================================================
    payload_line_index: int | None = None

    # ========================================================
    # FIND THE FIRST LINE BEGINNING WITH A JSON OBJECT OR ARRAY TOKEN.
    # ========================================================
    for line_index, stdout_line in enumerate(stdout_lines):
        # ====================================================
        # IGNORE LEADING WHITESPACE DURING PAYLOAD DISCOVERY.
        # ====================================================
        candidate_line = stdout_line.lstrip()

        # ====================================================
        # ACCEPT ONLY AN OBJECT OR ARRAY AS THE TOP-LEVEL PAYLOAD.
        # ====================================================
        if candidate_line.startswith("{") or candidate_line.startswith("["):
            payload_line_index = line_index
            break

    # ========================================================
    # REJECT OUTPUT WITHOUT A JSON OBJECT OR ARRAY CANDIDATE.
    # ========================================================
    if payload_line_index is None:
        return None, JsonParseAudit(
            status="JSON_PAYLOAD_NOT_FOUND",
            expected_type=expected_type_name,
            actual_type="UNKNOWN",
            payload_start_line=None,
            stdout_prefix_discarded=record.stdout,
            error="NO_LINE_STARTED_WITH_JSON_OBJECT_OR_ARRAY_TOKEN",
        )

    # ========================================================
    # CAPTURE EVERY PREFIX CHARACTER BEFORE THE JSON PAYLOAD LINE.
    # ========================================================
    stdout_prefix = "".join(stdout_lines[:payload_line_index]).strip()

    # ========================================================
    # CAPTURE THE JSON CANDIDATE FROM THE DISCOVERED LINE TO STDOUT END.
    # ========================================================
    json_candidate = "".join(stdout_lines[payload_line_index:]).strip()

    # ========================================================
    # PARSE THE CANDIDATE AS ONE COMPLETE JSON DOCUMENT.
    # ========================================================
    try:
        parsed_value = json.loads(json_candidate)

    # ========================================================
    # RETURN A STRUCTURED PARSER FAILURE WITHOUT A STACK TRACE.
    # ========================================================
    except json.JSONDecodeError as error:
        return None, JsonParseAudit(
            status="INVALID_JSON_PAYLOAD",
            expected_type=expected_type_name,
            actual_type="UNKNOWN",
            payload_start_line=payload_line_index + 1,
            stdout_prefix_discarded=stdout_prefix,
            error=(
                f"JSON_DECODE_ERROR={error.msg};"
                f"LINE={error.lineno};COLUMN={error.colno};POSITION={error.pos}"
            ),
        )

    # ========================================================
    # RECORD THE OBSERVED TOP-LEVEL TYPE.
    # ========================================================
    actual_type_name = type(parsed_value).__name__

    # ========================================================
    # REJECT A VALID JSON VALUE WITH THE WRONG TOP-LEVEL TYPE.
    # ========================================================
    if not isinstance(parsed_value, expected_type):
        return None, JsonParseAudit(
            status="JSON_TYPE_MISMATCH",
            expected_type=expected_type_name,
            actual_type=actual_type_name,
            payload_start_line=payload_line_index + 1,
            stdout_prefix_discarded=stdout_prefix,
            error=(
                f"EXPECTED_TOP_LEVEL_TYPE={expected_type_name};"
                f"ACTUAL_TOP_LEVEL_TYPE={actual_type_name}"
            ),
        )

    # ========================================================
    # DISTINGUISH CLEAN JSON FROM JSON PRECEDED BY AUDITED NOISE.
    # ========================================================
    parse_status = "PARSED_WITH_PREFIX" if stdout_prefix != "" else "PARSED"

    # ========================================================
    # RETURN THE VALIDATED VALUE AND COMPLETE PARSER AUDIT.
    # ========================================================
    return parsed_value, JsonParseAudit(
        status=parse_status,
        expected_type=expected_type_name,
        actual_type=actual_type_name,
        payload_start_line=payload_line_index + 1,
        stdout_prefix_discarded=stdout_prefix,
        error="",
    )


# ============================================================
# PARSE A LOWERCASE TRUE OR FALSE VALUE.
# ============================================================
def parse_tsv_boolean(record: CommandRecord) -> bool | None:
    """RETURN A BOOLEAN OR NONE FOR A FAILED OR UNEXPECTED RESULT."""

    # ========================================================
    # REJECT A FAILED COMMAND.
    # ========================================================
    if record.exit_code != 0:
        return None

    # ========================================================
    # NORMALIZE THE ALREADY NON-NULL OUTPUT.
    # ========================================================
    normalized_value = record.stdout.strip().lower()

    # ========================================================
    # RETURN TRUE FOR THE EXPECTED TRUE MARKER.
    # ========================================================
    if normalized_value == "true":
        return True

    # ========================================================
    # RETURN FALSE FOR THE EXPECTED FALSE MARKER.
    # ========================================================
    if normalized_value == "false":
        return False

    # ========================================================
    # RETURN NONE FOR ANY UNEXPECTED VALUE.
    # ========================================================
    return None


# ============================================================
# PARSE A NONNEGATIVE INTEGER VALUE.
# ============================================================
def parse_nonnegative_integer(record: CommandRecord) -> int | None:
    """RETURN A NONNEGATIVE INTEGER OR NONE FOR AN INVALID RESULT."""

    # ========================================================
    # REJECT A FAILED COMMAND.
    # ========================================================
    if record.exit_code != 0:
        return None

    # ========================================================
    # ATTEMPT INTEGER PARSING.
    # ========================================================
    try:
        parsed_value = int(record.stdout.strip())

    # ========================================================
    # RETURN NONE FOR NON-INTEGER OUTPUT.
    # ========================================================
    except ValueError:
        return None

    # ========================================================
    # REJECT NEGATIVE COUNTS.
    # ========================================================
    if parsed_value < 0:
        return None

    # ========================================================
    # RETURN THE VALID COUNT.
    # ========================================================
    return parsed_value


# ============================================================
# PRINT ONE COMMAND RECORD WITH SEPARATE STREAM BOUNDARIES.
# ============================================================
def print_command_record(
    record: CommandRecord,
    json_parse_audit: JsonParseAudit | None = None,
) -> None:
    """PRINT ONE COMMAND, SEPARATE STREAMS, AND OPTIONAL JSON-PARSER EVIDENCE."""

    # ========================================================
    # PRINT THE COMMAND LABEL.
    # ========================================================
    print(f"COMMAND_LABEL={record.label}")

    # ========================================================
    # PRINT THE LOGICAL COMMAND.
    # ========================================================
    print(f"COMMAND={record.logical_command}")

    # ========================================================
    # PRINT THE EXIT CODE.
    # ========================================================
    print(f"EXIT_CODE={record.exit_code}")

    # ========================================================
    # OPEN THE STANDARD-OUTPUT BOUNDARY.
    # ========================================================
    print("STDOUT_BEGIN")

    # ========================================================
    # PRINT STANDARD OUTPUT, INCLUDING A BLANK RESULT.
    # ========================================================
    print(record.stdout)

    # ========================================================
    # CLOSE THE STANDARD-OUTPUT BOUNDARY.
    # ========================================================
    print("STDOUT_END")

    # ========================================================
    # OPEN THE STANDARD-ERROR BOUNDARY.
    # ========================================================
    print("STDERR_BEGIN")

    # ========================================================
    # PRINT STANDARD ERROR, INCLUDING A BLANK RESULT.
    # ========================================================
    print(record.stderr)

    # ========================================================
    # CLOSE THE STANDARD-ERROR BOUNDARY.
    # ========================================================
    print("STDERR_END")

    # ========================================================
    # PRINT JSON-PARSER EVIDENCE WHEN A JSON PARSE WAS ATTEMPTED.
    # ========================================================
    if json_parse_audit is not None:
        # ====================================================
        # PRINT THE PARSER STATUS.
        # ====================================================
        print(f"JSON_PARSE_STATUS={json_parse_audit.status}")

        # ====================================================
        # PRINT THE REQUIRED AND OBSERVED TOP-LEVEL TYPES.
        # ====================================================
        print(f"JSON_EXPECTED_TYPE={json_parse_audit.expected_type}")
        print(f"JSON_ACTUAL_TYPE={json_parse_audit.actual_type}")

        # ====================================================
        # PRINT THE PAYLOAD START LINE OR NONE.
        # ====================================================
        payload_start_line = (
            str(json_parse_audit.payload_start_line)
            if json_parse_audit.payload_start_line is not None
            else "NONE"
        )
        print(f"JSON_PAYLOAD_START_LINE={payload_start_line}")

        # ====================================================
        # PRINT ANY DISCARDED PREFIX AS ONE JSON-ESCAPED FIELD.
        # ====================================================
        print(
            "STDOUT_PREFIX_DISCARDED="
            f"{marker_text(json_parse_audit.stdout_prefix_discarded)}"
        )

        # ====================================================
        # PRINT ANY PARSER ERROR AS ONE JSON-ESCAPED FIELD.
        # ====================================================
        print(f"JSON_PARSE_ERROR={marker_text(json_parse_audit.error)}")

    # ========================================================
    # PRINT A RECORD SEPARATOR.
    # ========================================================
    print("---")


# ============================================================
# WRITE AN OPT-IN JSON EVIDENCE FILE WITH EXCLUSIVE CREATION.
# ============================================================
def write_json_evidence(
    output_path: Path,
    evidence_payload: dict[str, Any],
) -> tuple[Path | None, str | None, str | None]:
    """CREATE ONE NEW EVIDENCE FILE OR RETURN A STRUCTURED FAILURE."""

    # ========================================================
    # EXPAND THE OPERATOR-SUPPLIED PATH WITHOUT TOUCHING AZURE OR GIT.
    # ========================================================
    resolved_output_path = output_path.expanduser().resolve()

    # ========================================================
    # CREATE THE EXPLICITLY REQUESTED PARENT DIRECTORY WHEN NEEDED.
    # ========================================================
    try:
        resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    # ========================================================
    # RETURN A CALM DIRECTORY-CREATION FAILURE.
    # ========================================================
    except OSError as error:
        return (
            None,
            None,
            f"EVIDENCE_PARENT_CREATE_ERROR={type(error).__name__}:{error}",
        )

    # ========================================================
    # SERIALIZE WITH STABLE INDENTATION AND A TRAILING NEWLINE.
    # ========================================================
    serialized_payload = (
        json.dumps(evidence_payload, indent=2, ensure_ascii=False, sort_keys=True)
        + "\n"
    )

    # ========================================================
    # TRACK WHETHER THIS INVOCATION CREATED THE DESTINATION PATH.
    # ========================================================
    output_created = False

    # ========================================================
    # CLAIM THE DESTINATION ATOMICALLY WITHOUT OVERWRITING AN EXISTING FILE.
    # ========================================================
    try:
        file_descriptor = os.open(
            resolved_output_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        output_created = True

        # ====================================================
        # WRITE, FLUSH, AND SYNC THE EXCLUSIVELY CREATED FILE.
        # ====================================================
        with os.fdopen(
            file_descriptor,
            "w",
            encoding="utf-8",
            newline="\n",
        ) as handle:
            handle.write(serialized_payload)
            handle.flush()
            os.fsync(handle.fileno())

    # ========================================================
    # RETURN A DISTINCT IMMUTABILITY STOP FOR AN EXISTING PATH.
    # ========================================================
    except FileExistsError:
        return None, None, "EVIDENCE_OUTPUT_ALREADY_EXISTS"

    # ========================================================
    # REMOVE A PARTIAL FILE AFTER ANY OTHER WRITE FAILURE.
    # ========================================================
    except OSError as error:
        if output_created:
            try:
                resolved_output_path.unlink(missing_ok=True)
            except OSError:
                pass
        return None, None, f"EVIDENCE_WRITE_ERROR={type(error).__name__}:{error}"

    # ========================================================
    # COMPUTE THE EVIDENCE FILE SHA-256 DIGEST.
    # ========================================================
    try:
        evidence_digest = hashlib.sha256(
            resolved_output_path.read_bytes()
        ).hexdigest().upper()

    # ========================================================
    # RETURN A CALM DIGEST FAILURE WITHOUT DELETING VALID EVIDENCE.
    # ========================================================
    except OSError as error:
        return (
            resolved_output_path,
            None,
            f"EVIDENCE_DIGEST_ERROR={type(error).__name__}:{error}",
        )

    # ========================================================
    # RETURN THE WRITTEN PATH, DIGEST, AND NO ERROR.
    # ========================================================
    return resolved_output_path, evidence_digest, None


# ============================================================
# RUN THE COMPLETE READ-ONLY RECONCILIATION.
# ============================================================
def inspect_current_state(repository: Path, json_output: Path | None = None) -> int:
    """COLLECT ALL REQUIRED GIT AND AZURE READBACKS WITHOUT MUTATION."""

    # ========================================================
    # CAPTURE THE UTC START TIME.
    # ========================================================
    inspection_utc = datetime.now(timezone.utc).isoformat()

    # ========================================================
    # CAPTURE THE RUNNING SCRIPT IDENTITY ONCE FOR THIS RUN.
    # ========================================================
    inspection_script_digest = script_sha256()

    # ========================================================
    # RESOLVE THE GIT EXECUTABLE.
    # ========================================================
    git_executable = resolve_executable("git")

    # ========================================================
    # RESOLVE THE AZURE CLI EXECUTABLE.
    # ========================================================
    azure_executable = resolve_executable("az")

    # ========================================================
    # CREATE THE COMMAND-AUDIT COLLECTION.
    # ========================================================
    records: list[CommandRecord] = []

    # ========================================================
    # CREATE THE JSON-PARSER AUDIT COLLECTION BY COMMAND LABEL.
    # ========================================================
    json_parse_audits: dict[str, JsonParseAudit] = {}

    # ========================================================
    # INITIALIZE GIT SUMMARY VALUES.
    # ========================================================
    repository_exists = repository.is_dir()
    git_worktree: bool | None = None
    git_branch: str | None = None
    git_head: str | None = None
    git_tag_exists: bool | None = None
    git_tag_target: str | None = None
    git_clean: bool | None = None

    # ========================================================
    # COLLECT GIT READBACKS WHEN GIT AND THE REPOSITORY EXIST.
    # ========================================================
    if git_executable is not None and repository_exists:
        # ====================================================
        # CONFIRM THE DIRECTORY IS A GIT WORKTREE.
        # ====================================================
        worktree_record = run_read_only_command(
            "GIT_WORKTREE",
            git_executable,
            ["-C", str(repository), "rev-parse", "--is-inside-work-tree"],
        )
        records.append(worktree_record)
        git_worktree = parse_tsv_boolean(worktree_record)

        # ====================================================
        # READ THE CURRENT BRANCH WITHOUT CHECKOUT OR RESET.
        # ====================================================
        branch_record = run_read_only_command(
            "GIT_BRANCH",
            git_executable,
            ["-C", str(repository), "branch", "--show-current"],
        )
        records.append(branch_record)
        if branch_record.exit_code == 0:
            git_branch = branch_record.stdout

        # ====================================================
        # READ THE CURRENT HEAD COMMIT.
        # ====================================================
        head_record = run_read_only_command(
            "GIT_HEAD",
            git_executable,
            ["-C", str(repository), "rev-parse", "HEAD"],
        )
        records.append(head_record)
        if head_record.exit_code == 0 and head_record.stdout != "":
            git_head = head_record.stdout.lower()

        # ====================================================
        # READ THE EXPECTED TAG NAME WITHOUT CHANGING REFS.
        # ====================================================
        tag_list_record = run_read_only_command(
            "GIT_TAG_LIST",
            git_executable,
            ["-C", str(repository), "tag", "--list", EXPECTED_TAG],
        )
        records.append(tag_list_record)
        if tag_list_record.exit_code == 0:
            git_tag_exists = EXPECTED_TAG in tag_list_record.stdout.splitlines()

        # ====================================================
        # READ THE TAG TARGET WHEN THE TAG EXISTS.
        # ====================================================
        if git_tag_exists:
            tag_target_record = run_read_only_command(
                "GIT_TAG_TARGET",
                git_executable,
                ["-C", str(repository), "rev-list", "-n", "1", EXPECTED_TAG],
            )
            records.append(tag_target_record)
            if tag_target_record.exit_code == 0 and tag_target_record.stdout != "":
                git_tag_target = tag_target_record.stdout.lower()

        # ====================================================
        # READ TRACKED AND UNTRACKED WORKTREE DRIFT.
        # ====================================================
        status_record = run_read_only_command(
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
        records.append(status_record)
        if status_record.exit_code == 0:
            git_clean = status_record.stdout == ""

    # ========================================================
    # RECORD A MISSING GIT EXECUTABLE WITHOUT RAISING.
    # ========================================================
    elif git_executable is None:
        records.append(missing_executable_record("GIT_DISCOVERY", "git"))

    # ========================================================
    # RECORD A MISSING REPOSITORY WITHOUT RAISING.
    # ========================================================
    else:
        records.append(
            CommandRecord(
                label="REPOSITORY_DISCOVERY",
                logical_command=str(repository),
                exit_code=2,
                stdout="",
                stderr="AUTHORITATIVE_REPOSITORY_NOT_FOUND",
            )
        )

    # ========================================================
    # INITIALIZE AZURE SUMMARY VALUES.
    # ========================================================
    selected_subscription_id: str | None = None
    selected_subscription_name: str | None = None
    selected_subscription_state: str | None = None
    selected_subscription_is_default: bool | None = None
    extension_state = "UNKNOWN"
    extension_version: str | None = None
    resource_group_exists: bool | None = None
    resource_group_resource_count: int | None = None
    acr_name_available: bool | None = None
    acr_name_reason: str | None = None
    acr_name_message: str | None = None

    # ========================================================
    # COLLECT AZURE READBACKS WHEN THE AZURE CLI EXISTS.
    # ========================================================
    if azure_executable is not None:
        # ====================================================
        # READ THE CURRENTLY SELECTED AZURE SUBSCRIPTION.
        # ====================================================
        account_record = run_read_only_command(
            "AZURE_ACCOUNT_SHOW",
            azure_executable,
            [
                "account",
                "show",
                "--query",
                "{id:id,name:name,state:state,isDefault:isDefault}",
                "--output",
                "json",
                "--only-show-errors",
            ],
        )
        records.append(account_record)
        account_json, account_parse_audit = parse_json_record(account_record, dict)
        json_parse_audits[account_record.label] = account_parse_audit
        if isinstance(account_json, dict):
            account_id_value = account_json.get("id")
            account_name_value = account_json.get("name")
            account_state_value = account_json.get("state")
            account_default_value = account_json.get("isDefault")
            if isinstance(account_id_value, str):
                selected_subscription_id = account_id_value.lower()
            if isinstance(account_name_value, str):
                selected_subscription_name = account_name_value
            if isinstance(account_state_value, str):
                selected_subscription_state = account_state_value
            if isinstance(account_default_value, bool):
                selected_subscription_is_default = account_default_value

        # ====================================================
        # READ INSTALLED EXTENSIONS WITHOUT INSTALLING OR UPDATING ANYTHING.
        # ====================================================
        extension_record = run_read_only_command(
            "AZURE_EXTENSION_LIST",
            azure_executable,
            [
                "extension",
                "list",
                "--query",
                f"[?name=='{CONTAINERAPP_EXTENSION_NAME}'].{{name:name,version:version}}",
                "--output",
                "json",
                "--only-show-errors",
            ],
        )
        records.append(extension_record)
        extension_json, extension_parse_audit = parse_json_record(
            extension_record, list
        )
        json_parse_audits[extension_record.label] = extension_parse_audit
        if isinstance(extension_json, list):
            if len(extension_json) == 0:
                extension_state = "ABSENT"
            elif isinstance(extension_json[0], dict):
                extension_state = "INSTALLED"
                extension_version_value = extension_json[0].get("version")
                if isinstance(extension_version_value, str):
                    extension_version = extension_version_value

        # ====================================================
        # READ RESOURCE-GROUP EXISTENCE IN THE EXPECTED SUBSCRIPTION.
        # ====================================================
        group_exists_record = run_read_only_command(
            "AZURE_RESOURCE_GROUP_EXISTS",
            azure_executable,
            [
                "group",
                "exists",
                "--name",
                RESOURCE_GROUP_NAME,
                "--subscription",
                EXPECTED_SUBSCRIPTION_ID,
                "--output",
                "tsv",
                "--only-show-errors",
            ],
        )
        records.append(group_exists_record)
        resource_group_exists = parse_tsv_boolean(group_exists_record)

        # ====================================================
        # READ THE RESOURCE COUNT ONLY WHEN THE GROUP EXISTS.
        # ====================================================
        if resource_group_exists:
            resource_count_record = run_read_only_command(
                "AZURE_RESOURCE_GROUP_RESOURCE_COUNT",
                azure_executable,
                [
                    "resource",
                    "list",
                    "--resource-group",
                    RESOURCE_GROUP_NAME,
                    "--subscription",
                    EXPECTED_SUBSCRIPTION_ID,
                    "--query",
                    "length(@)",
                    "--output",
                    "tsv",
                    "--only-show-errors",
                ],
            )
            records.append(resource_count_record)
            resource_group_resource_count = parse_nonnegative_integer(resource_count_record)

        # ====================================================
        # READ GLOBAL ACR NAME VALIDITY AND AVAILABILITY.
        # ====================================================
        acr_name_record = run_read_only_command(
            "AZURE_ACR_CHECK_NAME",
            azure_executable,
            [
                "acr",
                "check-name",
                "--name",
                CONTAINER_REGISTRY_NAME,
                "--subscription",
                EXPECTED_SUBSCRIPTION_ID,
                "--query",
                "{nameAvailable:nameAvailable,reason:reason,message:message}",
                "--output",
                "json",
                "--only-show-errors",
            ],
        )
        records.append(acr_name_record)
        acr_name_json, acr_name_parse_audit = parse_json_record(
            acr_name_record, dict
        )
        json_parse_audits[acr_name_record.label] = acr_name_parse_audit
        if isinstance(acr_name_json, dict):
            acr_available_value = acr_name_json.get("nameAvailable")
            acr_reason_value = acr_name_json.get("reason")
            acr_message_value = acr_name_json.get("message")
            if isinstance(acr_available_value, bool):
                acr_name_available = acr_available_value
            if isinstance(acr_reason_value, str):
                acr_name_reason = acr_reason_value
            if isinstance(acr_message_value, str):
                acr_name_message = acr_message_value

    # ========================================================
    # RECORD A MISSING AZURE CLI EXECUTABLE WITHOUT RAISING.
    # ========================================================
    else:
        records.append(missing_executable_record("AZURE_CLI_DISCOVERY", "az"))

    # ========================================================
    # COMPARE THE LIVE GIT BRANCH WITH THE HANDOFF BASELINE.
    # ========================================================
    git_branch_matches = (
        None if git_branch is None else git_branch == EXPECTED_BRANCH
    )

    # ========================================================
    # COMPARE THE LIVE GIT HEAD WITH THE HANDOFF BASELINE.
    # ========================================================
    git_head_matches = None if git_head is None else git_head == EXPECTED_HEAD

    # ========================================================
    # COMPARE THE LIVE TAG TARGET WITH THE HANDOFF BASELINE.
    # ========================================================
    if git_tag_exists is None:
        git_tag_matches: bool | None = None
    elif git_tag_exists is False:
        git_tag_matches = False
    elif git_tag_target is None:
        git_tag_matches = None
    else:
        git_tag_matches = git_tag_target == EXPECTED_HEAD

    # ========================================================
    # COMPARE THE LIVE AZURE CONTEXT WITH THE HANDOFF BASELINE.
    # ========================================================
    subscription_matches = (
        None
        if selected_subscription_id is None
        else selected_subscription_id == EXPECTED_SUBSCRIPTION_ID
    )

    # ========================================================
    # DETERMINE WHETHER EVERY REQUIRED LIVE FIELD IS KNOWN.
    # ========================================================
    inspection_complete = all(
        [
            git_worktree is True,
            git_branch is not None,
            git_head is not None,
            git_tag_exists is not None,
            git_clean is not None,
            selected_subscription_id is not None,
            extension_state in {"ABSENT", "INSTALLED"},
            resource_group_exists is not None,
            acr_name_available is not None,
        ]
    )

    # ========================================================
    # REQUIRE A TAG TARGET WHEN THE EXPECTED TAG EXISTS.
    # ========================================================
    if git_tag_exists is True and git_tag_target is None:
        inspection_complete = False

    # ========================================================
    # REQUIRE AN EXTENSION VERSION WHEN THE EXTENSION IS INSTALLED.
    # ========================================================
    if extension_state == "INSTALLED" and extension_version is None:
        inspection_complete = False

    # ========================================================
    # REQUIRE A RESOURCE COUNT WHEN THE RESOURCE GROUP EXISTS.
    # ========================================================
    if resource_group_exists is True and resource_group_resource_count is None:
        inspection_complete = False

    # ========================================================
    # DETERMINE WHETHER THE REPOSITORY AND SUBSCRIPTION GATES PASS.
    # ========================================================
    baseline_gate_passes = all(
        [
            git_branch_matches is True,
            git_head_matches is True,
            git_tag_matches is True,
            git_clean is True,
            subscription_matches is True,
        ]
    )

    # ========================================================
    # RENDER THE RESOURCE COUNT WITHOUT CONFLATING ABSENCE AND UNKNOWN STATE.
    # ========================================================
    if resource_group_exists is False:
        resource_group_resource_count_marker = "NOT_APPLICABLE"
    elif resource_group_resource_count is None:
        resource_group_resource_count_marker = "UNKNOWN"
    else:
        resource_group_resource_count_marker = str(resource_group_resource_count)

    # ========================================================
    # DETERMINE THE FINAL RECONCILIATION STATUS ONCE.
    # ========================================================
    if inspection_complete and baseline_gate_passes:
        reconciliation_status = "COMPLETE_BASELINE_CONFIRMED"
    elif inspection_complete:
        reconciliation_status = "COMPLETE_BASELINE_DRIFT_STOP"
    else:
        reconciliation_status = "INCOMPLETE_READBACK_STOP"

    # ========================================================
    # BUILD THE DURABLE MACHINE EVIDENCE PAYLOAD.
    # ========================================================
    evidence_payload: dict[str, Any] = {
        "evidence_schema_version": "1.0",
        "run_utc": inspection_utc,
        "utility": {
            "name": "ajas_m1_readonly_reconcile",
            "version": UTILITY_VERSION,
            "script_sha256": inspection_script_digest,
            "mode": "inspect",
        },
        "safety": {
            "azure_mutations_attempted": False,
            "git_mutations_attempted": False,
            "billable_resources_created": False,
            "oidc_required_for_future_github_deployment": True,
            "long_lived_azure_credentials_allowed": False,
        },
        "commands": [
            {
                **asdict(record),
                "json_parse_audit": (
                    asdict(json_parse_audits[record.label])
                    if record.label in json_parse_audits
                    else None
                ),
            }
            for record in records
        ],
        "reconciled_state": {
            "local_repository": str(repository),
            "local_repository_exists": repository_exists,
            "local_git_worktree": git_worktree,
            "local_git_branch": git_branch,
            "local_git_head": git_head,
            "local_git_clean": git_clean,
            "milestone0_tag_name": EXPECTED_TAG,
            "milestone0_tag_exists": git_tag_exists,
            "milestone0_tag_target": git_tag_target,
            "git_branch_matches_handoff": git_branch_matches,
            "git_head_matches_handoff": git_head_matches,
            "git_tag_matches_handoff": git_tag_matches,
            "azure_selected_subscription_id": selected_subscription_id,
            "azure_selected_subscription_name": selected_subscription_name,
            "azure_selected_subscription_state": selected_subscription_state,
            "azure_selected_subscription_is_default": (
                selected_subscription_is_default
            ),
            "azure_subscription_matches_handoff": subscription_matches,
            "containerapp_extension_state": extension_state,
            "containerapp_extension_version": extension_version,
            "resource_group_name": RESOURCE_GROUP_NAME,
            "resource_group_exists": resource_group_exists,
            "resource_group_resource_count": resource_group_resource_count,
            "container_registry_name": CONTAINER_REGISTRY_NAME,
            "container_registry_name_available": acr_name_available,
            "container_registry_name_reason": acr_name_reason,
            "container_registry_name_message": acr_name_message,
            "inspection_complete": inspection_complete,
            "baseline_gate_passes": baseline_gate_passes,
            "reconciliation_status": reconciliation_status,
        },
    }

    # ========================================================
    # PRINT THE STRUCTURED HEADER.
    # ========================================================
    print(
        f"===== BEGIN AJAS MILESTONE 1 READ-ONLY RECONCILIATION v{UTILITY_VERSION} ====="
    )

    # ========================================================
    # PRINT THE UTILITY IDENTITY AND SAFETY MARKERS.
    # ========================================================
    print(f"RUN_UTC={inspection_utc}")
    print(f"UTILITY_VERSION={UTILITY_VERSION}")
    print(f"SCRIPT_SHA256={inspection_script_digest}")
    print("MODE=INSPECT")
    print("AZURE_MUTATIONS_ATTEMPTED=False")
    print("GIT_MUTATIONS_ATTEMPTED=False")
    print("BILLABLE_RESOURCES_CREATED=False")
    print("OIDC_REQUIREMENT=MANDATORY_FOR_FUTURE_GITHUB_DEPLOYMENT")
    print("LONG_LIVED_AZURE_CREDENTIALS_ALLOWED=False")

    # ========================================================
    # PRINT THE COMMAND-AUDIT SECTION.
    # ========================================================
    print("===== COMMAND AUDIT BEGIN =====")
    for record in records:
        print_command_record(record, json_parse_audits.get(record.label))
    print("===== COMMAND AUDIT END =====")

    # ========================================================
    # PRINT THE REQUIRED RECONCILED STATE.
    # ========================================================
    print("===== RECONCILED STATE BEGIN =====")
    print(f"LOCAL_REPOSITORY={repository}")
    print(f"LOCAL_REPOSITORY_EXISTS={marker_bool(repository_exists)}")
    print(f"LOCAL_GIT_WORKTREE={marker_bool(git_worktree)}")
    print(f"LOCAL_GIT_BRANCH={git_branch if git_branch is not None else 'UNKNOWN'}")
    print(f"LOCAL_GIT_HEAD={git_head if git_head is not None else 'UNKNOWN'}")
    print(f"LOCAL_GIT_CLEAN={marker_bool(git_clean)}")
    print(f"MILESTONE0_TAG_NAME={EXPECTED_TAG}")
    print(f"MILESTONE0_TAG_EXISTS={marker_bool(git_tag_exists)}")
    print(
        "MILESTONE0_TAG_TARGET="
        f"{git_tag_target if git_tag_target is not None else 'UNKNOWN'}"
    )
    print(f"GIT_BRANCH_MATCHES_HANDOFF={marker_bool(git_branch_matches)}")
    print(f"GIT_HEAD_MATCHES_HANDOFF={marker_bool(git_head_matches)}")
    print(f"GIT_TAG_MATCHES_HANDOFF={marker_bool(git_tag_matches)}")
    print(
        "AZURE_SELECTED_SUBSCRIPTION_ID="
        f"{selected_subscription_id if selected_subscription_id is not None else 'UNKNOWN'}"
    )
    print(
        "AZURE_SELECTED_SUBSCRIPTION_NAME="
        f"{selected_subscription_name if selected_subscription_name is not None else 'UNKNOWN'}"
    )
    print(
        "AZURE_SELECTED_SUBSCRIPTION_STATE="
        f"{selected_subscription_state if selected_subscription_state is not None else 'UNKNOWN'}"
    )
    print(
        "AZURE_SELECTED_SUBSCRIPTION_IS_DEFAULT="
        f"{marker_bool(selected_subscription_is_default)}"
    )
    print(
        "AZURE_SUBSCRIPTION_MATCHES_HANDOFF="
        f"{marker_bool(subscription_matches)}"
    )
    print(f"CONTAINERAPP_EXTENSION_STATE={extension_state}")
    print(
        "CONTAINERAPP_EXTENSION_VERSION="
        f"{extension_version if extension_version is not None else 'NONE'}"
    )
    print(f"RESOURCE_GROUP_NAME={RESOURCE_GROUP_NAME}")
    print(f"RESOURCE_GROUP_EXISTS={marker_bool(resource_group_exists)}")
    print(
        "RESOURCE_GROUP_RESOURCE_COUNT="
        f"{resource_group_resource_count_marker}"
    )
    print(f"CONTAINER_REGISTRY_NAME={CONTAINER_REGISTRY_NAME}")
    print(f"CONTAINER_REGISTRY_NAME_AVAILABLE={marker_bool(acr_name_available)}")
    print(
        "CONTAINER_REGISTRY_NAME_REASON="
        f"{acr_name_reason if acr_name_reason is not None else 'NONE'}"
    )
    print(
        "CONTAINER_REGISTRY_NAME_MESSAGE="
        f"{acr_name_message if acr_name_message is not None else 'NONE'}"
    )
    print(f"INSPECTION_COMPLETE={marker_bool(inspection_complete)}")
    print(f"BASELINE_GATE_PASSES={marker_bool(baseline_gate_passes)}")

    # ========================================================
    # PRINT A CALM FINAL STATUS MARKER.
    # ========================================================
    print(f"RECONCILIATION_STATUS={reconciliation_status}")

    # ========================================================
    # CLOSE THE RECONCILED-STATE SECTION.
    # ========================================================
    print("===== RECONCILED STATE END =====")

    # ========================================================
    # WRITE AN EVIDENCE FILE ONLY AFTER AN EXPLICIT OUTPUT REQUEST.
    # ========================================================
    evidence_write_failed = False
    if json_output is not None:
        written_path, written_digest, write_error = write_json_evidence(
            json_output, evidence_payload
        )
        if write_error is None and written_path is not None and written_digest is not None:
            print("EVIDENCE_OUTPUT_STATUS=WRITTEN")
            print(f"EVIDENCE_OUTPUT_PATH={written_path}")
            print(f"EVIDENCE_OUTPUT_SHA256={written_digest}")
        else:
            evidence_write_failed = True
            print("EVIDENCE_OUTPUT_STATUS=WRITE_FAILED")
            print(f"EVIDENCE_OUTPUT_ERROR={marker_text(write_error)}")

    # ========================================================
    # PRINT THE STRUCTURED FOOTER.
    # ========================================================
    print(
        f"===== END AJAS MILESTONE 1 READ-ONLY RECONCILIATION v{UTILITY_VERSION} ====="
    )

    # ========================================================
    # RETURN A DISTINCT CODE WHEN AN EXPLICIT EVIDENCE WRITE FAILED.
    # ========================================================
    if evidence_write_failed:
        return 4

    # ========================================================
    # RETURN SUCCESS ONLY FOR A COMPLETE, BASELINE-MATCHING READBACK.
    # ========================================================
    if inspection_complete and baseline_gate_passes:
        return 0

    # ========================================================
    # RETURN A DISTINCT CODE FOR COMPLETE BASELINE DRIFT.
    # ========================================================
    if inspection_complete:
        return 3

    # ========================================================
    # RETURN A DISTINCT CODE FOR AN INCOMPLETE INSPECTION.
    # ========================================================
    return 2


# ============================================================
# RUN NULL-SAFETY AND PARSING SELF-TESTS WITHOUT EXTERNAL COMMANDS.
# ============================================================
def run_self_test() -> int:
    """VERIFY NULL NORMALIZATION, CONTAMINATED JSON, AND TYPE CHECKING."""

    # ========================================================
    # VERIFY NULL TEXT NORMALIZATION.
    # ========================================================
    assert normalize_text(None) == ""

    # ========================================================
    # VERIFY PRESENT TEXT PRESERVATION.
    # ========================================================
    assert normalize_text("abc") == "abc"

    # ========================================================
    # VERIFY TRUE BOOLEAN PARSING.
    # ========================================================
    assert parse_tsv_boolean(CommandRecord("T", "x", 0, "true", "")) is True

    # ========================================================
    # VERIFY FALSE BOOLEAN PARSING.
    # ========================================================
    assert parse_tsv_boolean(CommandRecord("F", "x", 0, "false", "")) is False

    # ========================================================
    # VERIFY UNKNOWN BOOLEAN PARSING.
    # ========================================================
    assert parse_tsv_boolean(CommandRecord("U", "x", 0, "", "")) is None

    # ========================================================
    # VERIFY ZERO COUNT PARSING.
    # ========================================================
    assert parse_nonnegative_integer(CommandRecord("Z", "x", 0, "0", "")) == 0

    # ========================================================
    # VERIFY INVALID COUNT REJECTION.
    # ========================================================
    assert parse_nonnegative_integer(CommandRecord("I", "x", 0, "bad", "")) is None

    # ========================================================
    # VERIFY CLEAN JSON DICTIONARY PARSING.
    # ========================================================
    clean_value, clean_audit = parse_json_record(
        CommandRecord("J", "x", 0, '{"a": 1}', ""),
        dict,
    )
    assert clean_value == {"a": 1}
    assert clean_audit.status == "PARSED"
    assert clean_audit.stdout_prefix_discarded == ""
    assert clean_audit.payload_start_line == 1

    # ========================================================
    # STORE THE EXACT CONTAMINATED AZURE ACCOUNT OUTPUT FROM THE INCIDENT.
    # ========================================================
    contaminated_stdout = (
        "cannot import name 'load_capability_host' from "
        "'azure.ai.ml.entities._load_functions' "
        "(C:\\Users\\steve\\anaconda3\\Lib\\site-packages\\azure\\ai\\ml\\entities\\_load_functions.py)\n"
        "{\n"
        '  "id": "efe2c2b2-d541-4b47-952d-e1af59db9910",\n'
        '  "isDefault": true,\n'
        '  "name": "stevearchuleta-payasyougo",\n'
        '  "state": "Enabled"\n'
        "}"
    )

    # ========================================================
    # VERIFY THE EXACT CONTAMINATED OUTPUT PARSES AND RETAINS THE PREFIX.
    # ========================================================
    contaminated_value, contaminated_audit = parse_json_record(
        CommandRecord("CONTAMINATED_ACCOUNT", "x", 0, contaminated_stdout, ""),
        dict,
    )
    assert isinstance(contaminated_value, dict)
    assert (
        contaminated_value["id"]
        == "efe2c2b2-d541-4b47-952d-e1af59db9910"
    )
    assert contaminated_audit.status == "PARSED_WITH_PREFIX"
    assert contaminated_audit.payload_start_line == 2
    assert contaminated_audit.stdout_prefix_discarded.startswith(
        "cannot import name 'load_capability_host'"
    )
    assert contaminated_audit.error == ""

    # ========================================================
    # VERIFY A VALID ARRAY PASSES ARRAY TYPE VALIDATION.
    # ========================================================
    array_value, array_audit = parse_json_record(
        CommandRecord("A", "x", 0, '[{"name": "containerapp"}]', ""),
        list,
    )
    assert isinstance(array_value, list)
    assert array_audit.status == "PARSED"

    # ========================================================
    # VERIFY A VALID OBJECT FAILS CLOSED WHEN AN ARRAY IS REQUIRED.
    # ========================================================
    mismatch_value, mismatch_audit = parse_json_record(
        CommandRecord("M", "x", 0, '{"a": 1}', ""),
        list,
    )
    assert mismatch_value is None
    assert mismatch_audit.status == "JSON_TYPE_MISMATCH"
    assert mismatch_audit.expected_type == "list"
    assert mismatch_audit.actual_type == "dict"

    # ========================================================
    # VERIFY EMPTY JSON REJECTION.
    # ========================================================
    empty_value, empty_audit = parse_json_record(
        CommandRecord("E", "x", 0, "", ""),
        dict,
    )
    assert empty_value is None
    assert empty_audit.status == "EMPTY_STDOUT"

    # ========================================================
    # VERIFY TRAILING NON-JSON CONTAMINATION FAILS CLOSED.
    # ========================================================
    trailing_value, trailing_audit = parse_json_record(
        CommandRecord("TRAILING", "x", 0, '{"a": 1}\nwarning', ""),
        dict,
    )
    assert trailing_value is None
    assert trailing_audit.status == "INVALID_JSON_PAYLOAD"

    # ========================================================
    # PRINT INDIVIDUAL REGRESSION MARKERS.
    # ========================================================
    print("SELF_TEST_CONTAMINATED_AZURE_STDOUT=PASS")
    print(
        "SELF_TEST_CONTAMINATED_PREFIX="
        f"{marker_text(contaminated_audit.stdout_prefix_discarded)}"
    )
    print("SELF_TEST_JSON_TYPE_VALIDATION=PASS")
    print("SELF_TEST_TRAILING_CONTAMINATION_FAIL_CLOSED=PASS")

    # ========================================================
    # PRINT THE SELF-TEST SUCCESS MARKER.
    # ========================================================
    print(f"AJAS_READ_ONLY_RECONCILIATION_SELF_TEST_v{UTILITY_VERSION}=PASS")

    # ========================================================
    # RETURN A SUCCESS EXIT CODE.
    # ========================================================
    return 0


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
            "Read-only AJAS Milestone-1 Git and Azure state reconciliation."
        )
    )

    # ========================================================
    # ADD THE MODE SELECTION.
    # ========================================================
    parser.add_argument(
        "--mode",
        choices=("inspect", "self-test"),
        default="inspect",
        help="Run live read-only inspection or internal parser self-tests.",
    )

    # ========================================================
    # ADD THE AUTHORITATIVE REPOSITORY PATH OVERRIDE.
    # ========================================================
    parser.add_argument(
        "--repo",
        type=Path,
        default=DEFAULT_REPOSITORY,
        help="Authoritative AJAS repository path.",
    )

    # ========================================================
    # ADD AN OPTIONAL DURABLE JSON EVIDENCE OUTPUT PATH.
    # ========================================================
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help=(
            "Write one new exclusive JSON evidence file; existing files are not "
            "overwritten."
        ),
    )

    # ========================================================
    # RETURN THE PARSED ARGUMENTS.
    # ========================================================
    return parser.parse_args()


# ============================================================
# DISPATCH THE REQUESTED MODE.
# ============================================================
def main() -> int:
    """RUN THE REQUESTED READ-ONLY UTILITY MODE."""

    # ========================================================
    # PARSE THE COMMAND-LINE ARGUMENTS.
    # ========================================================
    arguments = parse_arguments()

    # ========================================================
    # RUN THE INTERNAL SELF-TEST MODE.
    # ========================================================
    if arguments.mode == "self-test":
        return run_self_test()

    # ========================================================
    # RUN THE LIVE READ-ONLY INSPECTION MODE.
    # ========================================================
    return inspect_current_state(arguments.repo, arguments.json_output)


# ============================================================
# EXECUTE THE PROGRAM ONLY WHEN RUN AS A SCRIPT.
# ============================================================
if __name__ == "__main__":
    # ========================================================
    # RETURN THE PROGRAM EXIT CODE TO THE OPERATING SYSTEM.
    # ========================================================
    raise SystemExit(main())
