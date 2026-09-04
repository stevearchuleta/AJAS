# Superseded and Historical AJAS Operations Utilities

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
