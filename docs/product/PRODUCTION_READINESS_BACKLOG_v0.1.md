# AJAS Production-Readiness Backlog

**Document ID:** `AJAS-P6-BACKLOG-0.1-2026-09-02`
**Status:** DRAFT FOR STEVE RATIFICATION (`_v0.1`; promotes to `_v1.0` on approval)
**Date:** 2026-09-02
**Controlling specification:** `AJAS_Handoff_FINAL_v1.0.md`
**Companion:** `docs/testing/RELEASE_GATE_EVIDENCE_MATRIX_v0.1.md`

## Standing prohibitions (restated, non-negotiable)

No production deployment, no billing, no external users, and no automated employer submission until the corresponding gates in the controlling handoff are satisfied. Autonomous authority ends at `READY_FOR_REVIEW`. Steve performs every employer-system action. No LinkedIn or Indeed automation. Retrieved content is never an instruction. These prohibitions change only through a dated, versioned, Steve-approved governance record (S0-D01), never through an ordinary chat message.

## Current state (evidence-backed, 2026-09-02)

- `main` at merge `a848746` (tag `prompt5-complete`); baseline `8eee2ab` (tag `stage0b-baseline`); 86 tracked files; working tree clean.
- Verified: 129/129 tests in five classes; web, worker, core builds; pinned lockfile; deterministic fixture-only vertical slice with `MANUAL_ONLY` source policy and zero runtime network.
- Not yet built: database, migrations, queue, authentication, authorization, durable audit sink, artifact byte store, live source adapters, AI gateway, deployment of any kind.
- Open environment facts: Drive OAuth grant scope unverified (DRIVE-004); GitHub repository still REPORTED, unverified; Documents tree Google-Drive-synced (sync paused per CHG-P5-003-A1; handle interference observed 2026-09-02 during branch switch); Git pinned to Anaconda mingw64 with Git for Windows also present; installer v0.9 frozen; two rollback bundles preserved under `tmp/`.

## How to read the backlog

Each item: **ID | work | exit evidence**. Every phase ends at a gate in the companion matrix; the accountable approver for every gate is **Steve**, with the partner LLM as maker-checker. Phases are ordered by dependency; items inside a phase may proceed in parallel. One reviewable change at a time, on a branch, with tests, evidence, and rollback, exactly as Prompt 5 was done.

## Phase A - Repository, delivery foundation, and environment closure (completes Stage 0B scope)

- A1 | Verify the GitHub repository exists, is Private, has zero commits/forks, and confirm the exact URL verbatim from Steve | screenshot or API evidence recorded in decision register
- A2 | Review `ci.yml` before first push: actions pinned to commit SHAs, least-privilege `permissions:`, no `pull_request_target`, no secrets in logs | reviewed file diff + checker PASS
- A3 | Connect remote and push `main` with tags; enable branch protection on `main` (PR required, no force-push, no deletion); enable secret scanning and Dependabot alerts | protection-settings evidence
- A4 | CI green on GitHub for `npm ci`, lint, typecheck, full test suite, build | first green run URL/ID
- A5 | ADR-0002 Git executable: adopt Git for Windows (`C:\Program Files\Git`) or formally pin Anaconda Git; record `core.autocrlf` interplay with repo config | ADR merged
- A6 | Drive sync decision (closes CHG-P5-003-A1): exclude the AJAS root from Google Drive sync, or relocate to an unsynced root; required before sync resumes and before any real personal data | decision + verification evidence
- A7 | Resolve DRIVE-004: read the Google grant for the connected assistant(s); record exact scope wording; if broad `drive`, revoke and re-grant narrowly; revoke Gmail/Calendar grants per S0-D12 | grant-scope evidence in decision register
- A8 | Sign PowerShell operational scripts or adopt a no-download execution path; retire the unblock-then-run pattern | signing decision + first signed script
- A9 | Definitions and control inventory: define "material claim", "completed packet", "employer-system activity", "consequential state advancement"; list binding controls with IDs so later documents cannot silently weaken one | two short docs merged
- A10 | Rollback-bundle retirement decision: preserve indefinitely as forensic evidence or archive outside the tree via governance record | dated decision

## Phase B - Data authority and state durability

- B1 | Managed PostgreSQL provider ADR under the S0-D05 cost cap, RPO <= 1h capable (PITR), region and privacy terms verified fresh | ADR + provider evidence
- B2 | Initial schema and migrations: applications, postings, approved facts (versioned, provenance, sensitivity class per S0-D22/handoff 8.3), artifacts metadata, audit events, source policies; migration tool ADR | migrations apply and roll back cleanly on a scratch database
- B3 | Full Appendix-A state machine: complete permitted-transition table with guards, actors, evidence requirements, compensating transitions (S0-D19), reopening, withdrawal, repost, duplicate merge, `CLOSED_BEFORE_SUBMIT`, `UPLOAD_REPAIR_REQUIRED` flag semantics, and a READY staleness rule measured from the final liveness recheck | property tests: idempotency, replay, prohibited transitions
- B4 | PostgreSQL-backed durable queue with transactional outbox (S0-D27); idempotency keys; retry policy with dead-letter limit | integration tests incl. crash-mid-write
- B5 | Local/CI test-database strategy (Docker client 29.4.1 present; daemon health unverified): testcontainers, docker compose, or CI-only | documented and exercised in CI

## Phase C - Identity and authorization

- C1 | Managed standards-based identity provider ADR (S0-D28): Steve allowlist, secure sessions, revocation, MFA-ready | ADR + cost check
- C2 | Authentication skeleton wired to web app; sanitized test user can sign in | Stage-0B gate test passes
- C3 | Authorization layers per handoff 10.1 implemented distinctly: product authentication, storage authorization, bounded preparation authority (per-role selection per S0-D08), per-application human action; no layer implies another | boundary tests per layer

## Phase D - Audit and observability

- D1 | Durable `AuditSink`: append-only events with S0-D20 content policy (identifiers, versions, hashes, decisions, outcomes, error codes; no secrets, tokens, chain-of-thought, or unnecessary bodies); audit failure blocks consequential state advancement | audit-failure test
- D2 | Retention reconciliation: raise audit metadata retention to >= artifact retention (fixes the 12-month vs 24-month inversion in S0-D04) or record explicit acceptance | amended S0-D04 record
- D3 | Logs, metrics, correlation IDs, dashboards, alert channel; name the notification channel for the 15-minute critical-security target and confirm it needs no Gmail scope | alert test fired and received
- D4 | Model-call audit design (pre-implementation): prompt template ID+version, model+validator versions, injected fact IDs, output hash - no raw text retention | design doc merged

## Phase E - Storage and artifact authority

- E1 | Create the separately authorized Stage-1 byte root (S0-D14, handoff 8.1): distinct grant/credential, exact-root allowlist, per-batch change IDs (S0-D15); define what "separate authorization" concretely is | grant evidence + isolation test
- E2 | `ArtifactStore` with write, SHA-256 readback, size/MIME checks, and temp-file cleanup policy (handoff 8.1) | readback and cleanup tests
- E3 | Packet manifest contract per S0-D17 + handoff 3.3: START HERE semantics (names the files the employer form actually requests; merged PDF is not the automatic upload), editable sources preserved, validation manifest fields per handoff 17 | contract tests
- E4 | Erasure design: reconcile verified erasure with Drive Trash, version history, backups, audit history, legal holds | runbook merged

## Phase F - Source compliance and egress security

- F1 | Single egress control for all outbound HTTP (`SafeHttpClient`), implementing S0-D21 in full: HTTPS allowlist, no cookies, deny loopback/RFC1918/link-local, IPv6 equivalents (`::1`, `fe80::/10`, `fc00::/7`, IPv4-mapped), alternate IP encodings, `0.0.0.0`, cloud metadata endpoints, DNS-pinned connect, redirect count/scheme/host limits, response size cap, decompression defense, timeouts | SSRF test catalog passes
- F2 | Egress observability: logged outbound hosts so "zero employer-system activity" is measured, not asserted | log evidence in gate matrix
- F3 | `SourcePolicyRegistry` runtime enforcement: states, expiry, review cadence, kill switch, fail-closed on unknown fields (extends the Prompt-5 policy module) | policy drift tests
- F4 | Greenhouse board-by-board terms review for the first live candidates; then Lever; public visibility alone is insufficient; liveness definition distinguishes "posting present" from HTTP 200 (login walls, soft-404s) | per-board register entries
- F5 | Initial source allowlist proposal (S0-D07: review 25, enable 5) for Steve ratification | ratified list
- F6 | Prompt-injection defenses as invariants: retrieved content carries no instruction, tool, credential, policy, or state authority; injection acceptance set exercised against intake and screening | security suite extension green

## Phase G - AI gateway and model evaluation (S0-D29: nothing live until this phase)

- G1 | `StructuredAIGateway`: provider-neutral, schema-constrained I/O, per-run token ceiling, per-day spend stop, month-to-date circuit breaker that reconciles the daily $5 stop with the $50 monthly cap | breaker unit tests
- G2 | Provider ADR: current plans, prices, privacy, data-use terms verified fresh; within cost cap | ADR
- G3 | Deterministic truth backstop: every material claim in generated text resolves to an approved fact ID or fails closed; named gaps preserved 100% (never silently removed); A4/A7 checking independent of A5 lineage | fabrication and gap-preservation tests
- G4 | Model evaluation sets: prompt-injection acceptance, fabrication detection, claim-provenance scoring, golden comparisons | evaluation report

## Phase H - Backups, recovery, incidents, kill switches

- H1 | Backup and restore runbook: PITR configuration, restore rehearsal on scratch instance, RPO <= 1h / RTO <= 4h demonstrated | timed rehearsal evidence
- H2 | Incident response runbook: severity ladder, 15-minute critical notification, evidence preservation, controlled recovery | tabletop exercise
- H3 | Kill switches: per-source, connector, model, workflow, global; each tested | switch tests
- H4 | Rollback rehearsals: application release rollback and database migration rollback, each exercised once | rehearsal records

## Phase I - Delivery environments and CI/CD

- I1 | Environment ADRs: development, test (CI), preview, staging, shadow, production Stage 1; promotion requires evidence + Steve approval per the gate matrix | ADR set
- I2 | Vercel verification (S0-D30, handoff 9.3): current terms, pricing, runtime limits, privacy, test-data restrictions; adopt or select equivalent | verification record
- I3 | Preview deployment with synthetic data only; sanitization standard per S0-D22 frozen first | deployed preview + Stage-0B gate demo (sanitized test user authenticates, creates audited test record, reversible deployment, zero Track-A contact)
- I4 | Staging + shadow harness: shadow comparison design against Track-A outputs using sanitized/synthetic examples only; Track C never reads Track A at runtime - comparison inputs are exported by Steve through a versioned, approved migration | shadow design doc
- I5 | CD with rollback: one-command rollback to previous release, exercised | rollback demo

## Phase J - Accessibility and support

- J1 | WCAG 2.2 AA target: keyboard and screen-reader review of the Stage-1 dashboard before any external user | review checklist
- J2 | Support-response targets and channel (same business day Stage 1) | recorded in gate matrix

## Phase K - Governance, cost, and legal closure before real data

- K1 | Steve ratifies the numerical targets table (companion matrix section 3) or amends it | dated ratification
- K2 | Cost controls end-to-end: alerts at 50/75/90%, discretionary stop at 100%, non-discretionary floor defined (database and backups keep running) | breaker + alert evidence
- K3 | Qualified legal/privacy review (S0-D31) before any real applicant data enters Stage 1 | reviewer identity, scope, dated evidence
- K4 | Retention/erasure procedures live per class (S0-D04 as amended by D2) | erasure demonstration on synthetic data
- K5 | Decision-register sweep: every VERIFY_BEFORE_USE item in handoff section 20 closed or explicitly carried with an owner and date | register at zero unowned items

## Stage-1 entry (after A-K gates)

Steve-only real use begins only when the Stage-1 gate in the companion matrix passes: repeated truthful, non-duplicate packets on the ratified sample; 100% claim provenance and artifact readback; measured zero employer-system activity and zero Track-A/B runtime access; no unresolved high-risk finding; Steve's dated approval. AJAS then prepares packets and stops at `READY_FOR_REVIEW`; Steve performs every employer action manually.

## Explicitly deferred beyond this backlog

Private alpha (S0-D09), beta hardening, pilot cutover, public name/domain (S0-D10), production hosting topology (S0-D11), billing, multi-user features, email integration (S0-D12 stands: none in Stage 1), vector search, browser-assisted prefill, mobile applications.
