# AJAS Operational Evidence

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
