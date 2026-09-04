# AJAS Incident — PowerShell Null-Valued Wrapper Stop

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
