# AJAS Release-Gate Evidence Matrix

**Document ID:** `AJAS-P6-GATES-0.1-2026-09-02`
**Status:** DRAFT FOR STEVE RATIFICATION (`_v0.1`; numeric targets remain `TO_BE_RATIFIED_STAGE_0` until section 3 is signed)
**Date:** 2026-09-02
**Controlling specification:** `AJAS_Handoff_FINAL_v1.0.md`
**Companion:** `docs/product/PRODUCTION_READINESS_BACKLOG_v0.1.md`

Accountable approver for every gate below: **Steve Archuleta**. Maker-checker on every gate's evidence: the partner LLM not holding the builder seat. No gate passes on assertion; each names the artifact that proves it.

## 1. Environments

| Environment | Purpose | Data permitted | Promotion into it requires |
| --- | --- | --- | --- |
| development (local) | build and test on Steve's machine | synthetic only | n/a |
| test (CI) | every push/PR | synthetic only | CI configured (A2-A4) |
| preview | reviewable deploys | synthetic only | Gate G-0B |
| staging | pre-production rehearsal | sanitized per frozen S0-D22 standard | Gate G-STG |
| shadow | comparison vs Track-A outputs | sanitized/synthetic exports approved by Steve | Gate G-SHW |
| production Stage 1 | Steve-only real use | Steve's real data after K3 legal review | Gate G-S1 |
| production Stage 2+ | invited users | per later governance | out of scope here |

## 2. Gates

| Gate | Passes when | Required evidence artifacts | Approver |
| --- | --- | --- | --- |
| G-P5 (closed 2026-09-02) | vertical slice verified locally | maker-checker record `AJAS-P5-MAKER-CHECKER-2026-09-02`; commits `71a06b1`, `a848746`; 129/129 tests; builds | Steve (ratified via CHG-P6-002) |
| G-A repo/foundation | Phase A items A1-A10 done | branch-protection settings, first green CI run ID, ADR-0002, Drive-scope and sync-decision records, signing decision | Steve |
| G-0B Stage-0B completion | handoff 11 skeleton whole | migrations apply+rollback log, sanitized test-user auth demo, audited test record, reversible preview deploy demo, zero Track-A contact in egress log | Steve |
| G-B data/state | Phase B done | schema+migration review, property-test run, queue crash-recovery test | Steve |
| G-C identity/authz | Phase C done | per-layer boundary test results | Steve |
| G-D audit/observability | Phase D done | audit-failure-blocks-advancement test, alert delivery record, amended retention decision | Steve |
| G-E storage | Phase E done | separate-grant evidence, readback+cleanup tests, manifest contract tests | Steve |
| G-F sources/egress | Phase F done | SSRF catalog run, outbound-host log sample, per-board terms register, ratified 5-source allowlist, injection acceptance run | Steve |
| G-G AI gateway | Phase G done | breaker tests, provider ADR, fabrication+gap-preservation test run, evaluation report | Steve |
| G-H operations | Phase H done | timed restore rehearsal, tabletop record, kill-switch tests, rollback rehearsals | Steve |
| G-STG staging entry | sanitization standard frozen + G-0B..G-H relevant items | S0-D22 standard doc, sanitization verification on sample | Steve |
| G-SHW shadow entry | shadow design approved; exports via versioned Steve-approved migration only | shadow design doc, export migration record | Steve |
| G-S1 Stage-1 production | section 3 targets met on the ratified sample; K1-K5 closed | target-by-target evidence table, legal-review record, decision-register at zero unowned VERIFY items, Steve's dated integrated approval | Steve |
| G-ALPHA / G-BETA / G-CUT | deferred | per handoff 11; defined before use | Steve |

## 3. Numerical targets for G-S1 (all `TO_BE_RATIFIED_STAGE_0`)

Measurement definitions are part of the target; a number without its measurement method does not count as met.

| Target | Proposed value | Measured by |
| --- | --- | --- |
| Pre-promotion sample | 25 representative cases; the final 20 must be consecutive passes (ambiguity resolved: one 25-case sequence) | test ledger |
| Claim provenance | 100% of material claims resolve to approved fact IDs | deterministic resolver report |
| Named-gap preservation | 100% of named gaps present in delivered packet | gap-diff check |
| Required-artifact readback | 100% with SHA-256, size, MIME, page, text, visual, storage-reference checks | readback report per packet |
| Employer-system capability/activity | 0, measured by egress allowlist + logged outbound hosts | egress log audit |
| Track-A/B runtime access | 0, measured by credential separation + path/file-ID assertion log | isolation log audit |
| Unsupported material claims | 0 per the A9 definition | resolver + checker sample |
| READY liveness evidence | no older than 10 minutes, measured from the final recheck at the READY transition; staleness rule applies after | transition audit record |
| Scheduled/background-job completion | >= 95% within approved window; a run correctly producing zero packets counts as completed | job ledger |
| Queue wait | p95 <= 60 s | metrics |
| Packet preparation | p50 <= 5 min, p95 <= 15 min | metrics |
| Artifact generation | p95 <= 3 min | metrics |
| Availability | 99.0% monthly (probe and window defined at G-D) | uptime probe |
| Source-fetch success | >= 95% eligible; zero policy/rate violations | egress + policy logs |
| Dead-letter age | no unresolved blocking item older than one business day | queue report |
| RPO / RTO | <= 1 h / <= 4 h, demonstrated in H1 rehearsal | rehearsal timing |
| Variable cost | <= $0.50 per completed packet | cost ledger |
| Paid-work stops | $1.00 per run; $5.00 per day; month-to-date breaker subordinate to the $50 monthly cap; non-discretionary floor exempt | breaker logs |
| Critical-security notification | <= 15 minutes from detection, via the channel named at G-D | alert timestamps |
| Accessibility | WCAG 2.2 AA review before any external user | J1 checklist |
| Support response | same business day (Stage 1) | ticket log |

Quality, truthfulness, and safety are never weakened to meet a latency or cost number.

## 4. Standing rule

Every promotion, and every change to a binding control, requires: named evidence artifacts, a maker-checker PASS from the non-building partner LLM, and Steve's dated approval token recorded in the decision register. A calendar estimate never substitutes for a gate.
