# AJAS Operations Utilities

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
VERSION=0.1.0
SHA256=4007486455F4FD85A369FB369C3794FABB1070B11CFFE54B8742DA1A7DB5058B
```
