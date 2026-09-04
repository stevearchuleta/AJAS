#!/usr/bin/env python3
"""
AJAS MILESTONE 1 READ-ONLY RECONCILIATION UTILITY, VERSION 0.1.0.

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
- NO FILE OUTPUT UNLESS A FUTURE VERSION EXPLICITLY ADDS AN OPT-IN OUTPUT FLAG.
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
from dataclasses import dataclass

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
# PARSE JSON ONLY AFTER SUCCESSFUL, NONEMPTY OUTPUT.
# ============================================================
def parse_json_record(record: CommandRecord) -> Any | None:
    """RETURN PARSED JSON OR NONE FOR ANY NON-PARSEABLE RESULT."""

    # ========================================================
    # REJECT A FAILED COMMAND.
    # ========================================================
    if record.exit_code != 0:
        return None

    # ========================================================
    # REJECT EMPTY STANDARD OUTPUT.
    # ========================================================
    if record.stdout == "":
        return None

    # ========================================================
    # ATTEMPT STRICT JSON PARSING.
    # ========================================================
    try:
        return json.loads(record.stdout)

    # ========================================================
    # RETURN NONE FOR INVALID JSON WITHOUT RAISING A STACK TRACE.
    # ========================================================
    except json.JSONDecodeError:
        return None


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
def print_command_record(record: CommandRecord) -> None:
    """PRINT ONE COMMAND, EXIT CODE, STDOUT, AND STDERR SEPARATELY."""

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
    # PRINT A RECORD SEPARATOR.
    # ========================================================
    print("---")


# ============================================================
# RUN THE COMPLETE READ-ONLY RECONCILIATION.
# ============================================================
def inspect_current_state(repository: Path) -> int:
    """COLLECT ALL REQUIRED GIT AND AZURE READBACKS WITHOUT MUTATION."""

    # ========================================================
    # CAPTURE THE UTC START TIME.
    # ========================================================
    inspection_utc = datetime.now(timezone.utc).isoformat()

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
        account_json = parse_json_record(account_record)
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
        extension_json = parse_json_record(extension_record)
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
        acr_name_json = parse_json_record(acr_name_record)
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
    print(f"SCRIPT_SHA256={script_sha256()}")
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
        print_command_record(record)
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
        f"{resource_group_resource_count if resource_group_resource_count is not None else 'NOT_APPLICABLE_OR_UNKNOWN'}"
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
    if inspection_complete and baseline_gate_passes:
        print("RECONCILIATION_STATUS=COMPLETE_BASELINE_CONFIRMED")
    elif inspection_complete:
        print("RECONCILIATION_STATUS=COMPLETE_BASELINE_DRIFT_STOP")
    else:
        print("RECONCILIATION_STATUS=INCOMPLETE_READBACK_STOP")

    # ========================================================
    # CLOSE THE RECONCILED-STATE SECTION.
    # ========================================================
    print("===== RECONCILED STATE END =====")

    # ========================================================
    # PRINT THE STRUCTURED FOOTER.
    # ========================================================
    print(
        f"===== END AJAS MILESTONE 1 READ-ONLY RECONCILIATION v{UTILITY_VERSION} ====="
    )

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
    """VERIFY NULL NORMALIZATION AND CORE PARSERS."""

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
    assert (
        parse_tsv_boolean(CommandRecord("T", "x", 0, "true", "")) is True
    )

    # ========================================================
    # VERIFY FALSE BOOLEAN PARSING.
    # ========================================================
    assert (
        parse_tsv_boolean(CommandRecord("F", "x", 0, "false", "")) is False
    )

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
    # VERIFY JSON DICTIONARY PARSING.
    # ========================================================
    assert parse_json_record(CommandRecord("J", "x", 0, '{"a": 1}', "")) == {
        "a": 1
    }

    # ========================================================
    # VERIFY EMPTY JSON REJECTION.
    # ========================================================
    assert parse_json_record(CommandRecord("E", "x", 0, "", "")) is None

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
    return inspect_current_state(arguments.repo)


# ============================================================
# EXECUTE THE PROGRAM ONLY WHEN RUN AS A SCRIPT.
# ============================================================
if __name__ == "__main__":
    # ========================================================
    # RETURN THE PROGRAM EXIT CODE TO THE OPERATING SYSTEM.
    # ========================================================
    raise SystemExit(main())
