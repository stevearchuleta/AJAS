# AJAS Incident — Azure CLI Stdout Contamination

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
