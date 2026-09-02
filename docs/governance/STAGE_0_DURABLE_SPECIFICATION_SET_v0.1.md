# AJAS Stage-0 Durable Specification Set v0.1

**Status:** REVIEW CANDIDATE — implemented and locally testable; not a production or release-gate approval  
**Date:** 2026-08-30  
**Controlling specification:** `AJAS_Handoff_FINAL_v1.0.md`  
**Scope:** Track C, Prompt 5, synthetic fixture development only

## Authority and boundaries

Steve authorized Prompt-5 implementation in the AJAS ChatGPT Project thread after the verified Stage-0B local scaffold apply. That authorization permits local Track-C fixture development. It does not authorize production deployment, real applicant data, live connectors, employer authentication, form entry, file upload, attestation, communication, or submission.

The autonomous terminal state remains `READY_FOR_REVIEW`. Prompt 6 is excluded until Prompt 5 has passed both package verification and the attended Windows readback.

## Ratified-for-this-slice decisions

| Area                     | Prompt-5 decision                                                                                                                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Data                     | Synthetic applicant facts only; every fact is versioned, approved, use-scoped, effective-dated, and provenance-linked.                                                                             |
| Source                   | One minimized dated Greenhouse capture from the exact `GREENHOUSE:greenhouse` board.                                                                                                               |
| Runtime source authority | `MANUAL_ONLY`; only offline `PROCESS_SAVED_FIXTURE` is allowed. Network budget and allowed network methods are zero.                                                                               |
| Liveness                 | Two saved unauthenticated HTTP-200 capture observations are validated with an injected fixed clock. Output says `LIVE_AT_CAPTURE` and `currentStatus: NOT_CHECKED`.                                |
| Screening                | Explicit rules only; eligibility is separate from explainable fit. No score, weight, rank, or hidden suppression.                                                                                  |
| Packet                   | Three deterministic JSON artifacts are written to and read from an in-memory fixture store; hashes and byte counts must match.                                                                     |
| READY scope              | `STAGE1_VERTICAL_SLICE_TEST`, `productionReady: false`, and no authoritative Stage-1 byte store.                                                                                                   |
| State                    | `DISCOVERED -> SCREENED -> SELECTED -> PREPARING -> READY_FOR_REVIEW`; no post-READY autonomous transition.                                                                                        |
| Audit                    | Atomic in-memory receipt for every completed transition; parsed execution denials include prior transitions plus denial. Malformed pre-entry input is rejected without fabricating audit identity. |
| Idempotency              | Same key and same canonical input returns the stored result; conflicting payload fails closed.                                                                                                     |

## Controlled contracts

- `ajas.approved-facts.v1`
- `ajas.source-policy.v1`
- `ajas.saved-greenhouse-fixture.v1`
- `ajas.stage1-fixture-command.v1`
- `ajas.packet-metadata.v1`
- `ajas.audit-event.v1`
- `ajas.stage1-vertical-slice-result.v1`

Unknown major versions are rejected. The core accepts no clock, random ID, network client, Drive client, browser, email, or employer-action capability.

## Promotion blockers intentionally unresolved

This set does not ratify PostgreSQL, migrations, authentication, authorization, tenant isolation, a durable queue, the AJAS Personal Drive root, live source terms, retention, backup/recovery, RPO/RTO, costs, accessibility, deployment, or production audit storage. Those gaps block production promotion but do not invalidate the local synthetic fixture proof.

## Review evidence

The implementation, fixture provenance, test matrix, golden output, and hash-bound rollback design are defined by:

- `docs/product/STAGE_1_PROMPT_5_VERTICAL_SLICE_v0.1.md`
- `docs/sources/GREENHOUSE_GREENHOUSE_FIXTURE_POLICY_v0.1.md`
- `docs/testing/STAGE_1_PROMPT_5_TEST_AND_ROLLBACK_PLAN_v0.1.md`
- `docs/reports/PROMPT_5_IMPLEMENTATION_REPORT_v0.1.md`

This document becomes durable approval evidence only after Steve reviews the verified installed result. No earlier approval is backfilled or inferred.
