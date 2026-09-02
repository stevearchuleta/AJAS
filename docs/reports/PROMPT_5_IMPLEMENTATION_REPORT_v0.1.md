# AJAS Prompt-5 Implementation Report v0.1

**Status:** LOCAL CANDIDATE — implementation tests pass; package installation,
Windows readback, and Steve approval remain pending  
**Date:** 2026-08-30  
**Controlling specification:** `AJAS_Handoff_FINAL_v1.0.md`  
**Scope:** Track C, Prompt 5, synthetic fixture development only  
**Prompt 6:** LOCKED until every Prompt-5 completion gate in this report passes

## Outcome

The implemented deterministic path is:

`approved synthetic facts -> saved public Greenhouse fixture -> exact-board offline source policy -> saved intake and PRE_READY liveness evidence -> deterministic eligibility and explainable fit -> three verified JSON fixture artifacts -> READY_FOR_REVIEW -> committed audit batch`

`READY_FOR_REVIEW` is limited to `STAGE1_VERTICAL_SLICE_TEST`. The result reports
`productionReady: false`, `authoritativeByteStoreUsed: false`, and
`currentStatus: NOT_CHECKED`. It means only that a synthetic fixture packet passed the
local test contract and is ready for human inspection inside AJAS. It does not mean
that the posting is currently live, that a real applicant is eligible, that a
production packet exists, or that anyone should apply.

The official posting URL is retained only as saved-fixture source provenance. The
human instruction is:

> Review this synthetic fixture output inside AJAS only. Do not open an employer
> application form, contact the employer, upload files, make an attestation, or submit
> anything from this test result.

## Binding boundaries and observed side effects

| Boundary                                                         | Result                                                       |
| ---------------------------------------------------------------- | ------------------------------------------------------------ |
| Applicant data                                                   | Synthetic facts only; no Steve or Track-A applicant fixture  |
| Runtime source access                                            | Zero network methods, request budget zero, kill switch on    |
| Current liveness                                                 | Not checked; only two dated saved observations are validated |
| Employer authentication or session                               | None                                                         |
| Employer form entry, upload, attestation, contact, or submission | None                                                         |
| LinkedIn or Indeed automation                                    | None                                                         |
| Track-A or Track-B runtime read/write                            | None                                                         |
| Attended-pilot Drive folder or ledger read/write                 | None                                                         |
| Google Drive, Gmail, browser, payment, or AI provider            | No adapter or dependency                                     |
| Dependency graph                                                 | No new dependency and no `package-lock.json` change          |
| Autonomous terminal state                                        | `READY_FOR_REVIEW`; no post-READY autonomous transition      |

Two unauthenticated public Greenhouse detail reads were made during development to
create and recheck the saved fixture. Those development capture actions were not
runtime integration calls. They sent no credential or cookie, followed no redirect,
and performed no employer action.

## Saved source evidence

The fixture is bound to the exact `GREENHOUSE:greenhouse` board and posting
`8073203`, titled `FP&A Manager`.

| Evidence                  | Value                                                                     |
| ------------------------- | ------------------------------------------------------------------------- |
| Detail URL                | `https://boards-api.greenhouse.io/v1/boards/greenhouse/jobs/8073203`      |
| Canonical public URL      | `https://job-boards.greenhouse.io/greenhouse/jobs/8073203?gh_jid=8073203` |
| Fixture ID                | `greenhouse-greenhouse-8073203-capture-20260830`                          |
| Raw response bytes        | 12,618                                                                    |
| Raw response SHA-256      | `8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b`        |
| Minimized posting SHA-256 | `31802720c22f4c62d974f417f0c94bac377240ddb7d0da10b745fecd828201d9`        |
| Synthetic facts SHA-256   | `87eb5496e5850b6eb5524148b236f83ee8f8e768fc560ba80d6577536072cff2`        |
| Fixture command SHA-256   | `4b75268e8bb4c450f0121c146ed198571bfc77055e415fe99c4461b8e01fa9ce`        |

| Phase     | Observed UTC               | Request ID                         | Header-evidence SHA-256                                            | Result                 |
| --------- | -------------------------- | ---------------------------------- | ------------------------------------------------------------------ | ---------------------- |
| Intake    | `2026-08-30T05:18:58.000Z` | `2b470d8ff6f579a6df38c122c2421601` | `dc58a378cacad28fde88b5bc665b3b3481e1178ff324b78a1c1c6bcb6c720d32` | HTTP 200, 12,618 bytes |
| PRE_READY | `2026-08-30T05:22:53.000Z` | `e0af3a83d51d798fe213dfd3654925f4` | `e036352b011e055d6c59fae0cc182f40f4d05cce5225599b96d14fe33822a859` | HTTP 200, 12,618 bytes |

The exact early capture command text was not retained. This report does not invent
it. The retained evidence consists of the observed URLs, server times, request IDs,
response identity hashes, body byte count and hash, authentication/cookie/redirect
facts, and the minimized, human-reviewed derivative. The full body and response
headers were intentionally omitted from the repository. Their absence means the
human semantic review cannot be independently reperformed from repository files
alone.

Public availability is not blanket product authorization. The source record remains
`MANUAL_ONLY`; only offline `PROCESS_SAVED_FIXTURE` is allowed. The reviewed legal
entry point was inconclusive for runtime enablement.

## Exact repository delta from the Stage-0B baseline

The baseline comparison yields **38 operations: 30 `ADD` and 8 `REPLACE`** after this
report is included. Generated `.next`, `node_modules`, coverage, `tmp`, and
`*.tsbuildinfo` paths are not payload files.

### Replace operations

| Operation | Path                          | Purpose                                                      |
| --------- | ----------------------------- | ------------------------------------------------------------ |
| `REPLACE` | `.prettierignore`             | Exclude the committed golden JSON from mechanical formatting |
| `REPLACE` | `README.md`                   | Record the fixture-only Prompt-5 scope and boundaries        |
| `REPLACE` | `package.json`                | Add focused test and deterministic demo commands             |
| `REPLACE` | `packages/core/src/index.ts`  | Export the Prompt-5 typed core contracts                     |
| `REPLACE` | `packages/core/tsconfig.json` | Include the Stage-1 source modules                           |
| `REPLACE` | `tests/fixtures/README.md`    | Document synthetic fixture rules                             |
| `REPLACE` | `tests/golden/README.md`      | Document golden-output scope                                 |
| `REPLACE` | `tests/integration/README.md` | Document the fixture integration boundary                    |

### Add operations

| Operation | Path                                                             | Purpose                                                             |
| --------- | ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ADD`     | `docs/governance/STAGE_0_DURABLE_SPECIFICATION_SET_v0.1.md`      | Durable Prompt-5 governance candidate                               |
| `ADD`     | `docs/product/STAGE_1_PROMPT_5_VERTICAL_SLICE_v0.1.md`           | Slice contract and READY semantics                                  |
| `ADD`     | `docs/reports/PROMPT_5_IMPLEMENTATION_REPORT_v0.1.md`            | Exact implementation and verification report                        |
| `ADD`     | `docs/sources/GREENHOUSE_GREENHOUSE_FIXTURE_POLICY_v0.1.md`      | Exact-board fixture policy and provenance                           |
| `ADD`     | `docs/testing/STAGE_1_PROMPT_5_TEST_AND_ROLLBACK_PLAN_v0.1.md`   | Test, patch, and rollback contract                                  |
| `ADD`     | `packages/core/src/stage1/approved-facts.ts`                     | Approved-fact validation                                            |
| `ADD`     | `packages/core/src/stage1/canonical-json.ts`                     | Canonical JSON and hashing                                          |
| `ADD`     | `packages/core/src/stage1/contracts.ts`                          | Strict typed fixture contracts                                      |
| `ADD`     | `packages/core/src/stage1/screening.ts`                          | Deterministic eligibility and fit                                   |
| `ADD`     | `packages/core/src/stage1/source-policy.ts`                      | Source-policy and saved-liveness validation                         |
| `ADD`     | `packages/core/src/stage1/state-machine.ts`                      | Controlled fixture-state transitions                                |
| `ADD`     | `packages/core/src/stage1/vertical-slice.ts`                     | End-to-end fixture orchestration, artifacts, audit, and idempotency |
| `ADD`     | `scripts/run-stage1-fixture.ts`                                  | Deterministic fixture runner                                        |
| `ADD`     | `tests/contract/stage1-fixture-contract.test.ts`                 | Contract and evidence-index tests                                   |
| `ADD`     | `tests/fixtures/stage1/approved-applicant-facts.synthetic.json`  | Approved synthetic facts                                            |
| `ADD`     | `tests/fixtures/stage1/greenhouse-greenhouse-8073203.saved.json` | Minimized saved public posting fixture                              |
| `ADD`     | `tests/fixtures/stage1/greenhouse-greenhouse.source-policy.json` | Exact-board offline policy                                          |
| `ADD`     | `tests/fixtures/stage1/vertical-slice-command.synthetic.json`    | Bound synthetic fixture command                                     |
| `ADD`     | `tests/golden/stage1-greenhouse-ready-for-review.json`           | Exact expected output                                               |
| `ADD`     | `tests/golden/vertical-slice-golden.test.ts`                     | Golden determinism and hash checks                                  |
| `ADD`     | `tests/helpers/stage1-fixtures.ts`                               | Strict fixture loader and cloning helper                            |
| `ADD`     | `tests/integration/fixture-cli.test.ts`                          | Direct CLI-to-golden comparison                                     |
| `ADD`     | `tests/integration/fixture-vertical-slice.test.ts`               | Full fixture pipeline and failure integration tests                 |
| `ADD`     | `tests/security/stage1-boundaries.test.ts`                       | Injection, source, Track, secret, and employer-boundary tests       |
| `ADD`     | `tests/unit/approved-facts.test.ts`                              | Fact approval, provenance, and use tests                            |
| `ADD`     | `tests/unit/canonical-json.test.ts`                              | Unicode normalization collision tests                               |
| `ADD`     | `tests/unit/eligibility-fit.test.ts`                             | Requirement semantics and fit tests                                 |
| `ADD`     | `tests/unit/packet-state-audit.test.ts`                          | Artifact, state, audit, rollback, and idempotency tests             |
| `ADD`     | `tests/unit/source-policy-liveness.test.ts`                      | Exact policy, evidence, and liveness tests                          |
| `ADD`     | `tsconfig.tools.json`                                            | Type-check the fixture runner                                       |

The controlling handoff files, `AGENTS.md`, archive, `folder_structure.txt`,
`.env.example`, `package-lock.json`, existing app/worker sources, and the original
human-boundary module are unchanged.

`SHA256SUMS.txt` is an unchanged Stage-0B archive control file, not an installed
payload file. It is deliberately absent from the installed-tree source work copy and
is neither a Prompt-5 deletion nor an installer operation. The adjacent Prompt-5
patch carries a byte-identical `BASELINE-SHA256SUMS.txt` control and a new
`FINAL-SHA256SUMS.txt`; its release receipt records all preimage/postimage bytes and
hashes. Final patch, installer, and receipt hashes are recorded adjacent to the
release rather than inside this in-payload report, avoiding self-referential archive
and report hashes.

## Chronological command and action ledger

This ledger records every material retained command and external action. Early
exploratory read-only command text and the exact two capture-command strings were not
journaled; where exact text is unavailable, the limitation is stated rather than
reconstructed.

| Sequence | Command or action                                                                                                                                                 | Result                                                                                                                                                                                                                                                                         |
| -------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|        1 | Installer v0.1 dry run after ZIP/installer hash and PowerShell policy verification                                                                                | Safe `INTEGRITY_ABORT: ZIP_ARCHIVE_CANNOT_BE_OPENED`; zero AJAS writes, overwrite, delete, Git, dependency, or network action                                                                                                                                                  |
|        2 | Installer v0.2 dry run after compression-assembly correction                                                                                                      | Safe `PREFLIGHT_ABORT: COMPRESSION_TYPES_UNAVAILABLE`; the unreliable readiness probe stopped before the ZIP constructor; zero AJAS writes                                                                                                                                     |
|        3 | Installer v0.3 dry run                                                                                                                                            | `PLAN_READY`; 54 payload files, 34 directories, zero collisions, manifest verified                                                                                                                                                                                             |
|        4 | `& $InstallerV03 -ZipPath $AjasZip -ExpectedZipSha256 $ExpectedZipSha256 -TargetRoot $AjasRoot -Apply`                                                            | `INSTALL_STATUS=SUCCESS`; 54 files and 34 directories present; zero overwrite/delete/Git/dependency/network actions                                                                                                                                                            |
|        5 | `npm ci --ignore-scripts` on Steve's Windows AJAS root                                                                                                            | PASS; 159 packages added, 163 audited, zero vulnerabilities reported at that time                                                                                                                                                                                              |
|        6 | `npm run verify:scaffold`                                                                                                                                         | Stage-0B scaffold verification PASS                                                                                                                                                                                                                                            |
|        7 | `npm run format:check`                                                                                                                                            | Stage-0B formatting PASS                                                                                                                                                                                                                                                       |
|        8 | `npm run lint`                                                                                                                                                    | Stage-0B lint PASS                                                                                                                                                                                                                                                             |
|        9 | `npm run typecheck`                                                                                                                                               | Stage-0B web, worker, and core typecheck PASS                                                                                                                                                                                                                                  |
|       10 | `npm test`                                                                                                                                                        | Stage-0B: 3 files, 6 tests PASS                                                                                                                                                                                                                                                |
|       11 | `npm run build`                                                                                                                                                   | Stage-0B web, worker, and core build PASS                                                                                                                                                                                                                                      |
|       12 | Two public fixture-capture `GET` actions; exact command text not retained                                                                                         | Both HTTP 200; 12,618 identical body bytes; distinct times, request IDs, and header hashes; no credentials, cookies, redirect, login, form, contact, or submission                                                                                                             |
|       13 | Prompt-5 source and tests created with bounded patch edits; exact exploratory inspection commands were not retained as an exhaustive transcript                   | Initial local implementation reached 11 files and 61 tests PASS with no new dependency                                                                                                                                                                                         |
|       14 | `npm run demo:stage1` output compared directly with the golden file                                                                                               | Initial comparison failed because npm writes its command banner to stdout; the application JSON was not different                                                                                                                                                              |
|       15 | `node --import tsx scripts/run-stage1-fixture.ts` compared directly with the golden file                                                                          | PASS; the runner emits only golden JSON. A direct CLI integration test now prevents wrapper-output confusion                                                                                                                                                                   |
|       16 | Independent checker review                                                                                                                                        | Found missing report/release rollback evidence, stale unqualified Stage-0B checksum semantics, unsafe synthetic human wording, shallow parsing, failure-path audit reconstruction, artifact rollback, audit receipt, content-binding, and Unicode-key hardening gaps           |
|       17 | Bounded hardening edits and regression tests                                                                                                                      | Safe human wording added; fixture/facts/command/header/evidence pins added; strict unknown-field parsing, command/subject binding, audit receipts, failure audit history, hash-bound artifact cleanup, canonical Unicode collision rejection, and direct CLI golden test added |
|       18 | `npm run test:unit`                                                                                                                                               | Current: 6 files, 56 tests PASS                                                                                                                                                                                                                                                |
|       19 | `npm run test:contract`                                                                                                                                           | Current: 2 files, 49 tests PASS                                                                                                                                                                                                                                                |
|       20 | `npm run test:integration`                                                                                                                                        | Current: 2 files, 10 tests PASS                                                                                                                                                                                                                                                |
|       21 | `npm run test:security`                                                                                                                                           | Current: 2 files, 11 tests PASS                                                                                                                                                                                                                                                |
|       22 | `npm run test:golden`                                                                                                                                             | Current: 1 file, 3 tests PASS                                                                                                                                                                                                                                                  |
|       23 | `npm test`                                                                                                                                                        | Current aggregate: 13 files, 129 tests PASS                                                                                                                                                                                                                                    |
|       24 | `node --import tsx scripts/run-stage1-fixture.ts` and byte comparison with `tests/golden/stage1-greenhouse-ready-for-review.json`                                 | Final PASS after adding per-requirement source-evidence references; both 20,281 bytes and SHA-256 `b107a4bdc5c9ed100da910f8f6aaa0b890e7aadd31cee0e7901dd6dff907fefb`                                                                                                           |
|       25 | `npm run verify:scaffold`                                                                                                                                         | Current scaffold verification PASS                                                                                                                                                                                                                                             |
|       26 | `npm run lint`                                                                                                                                                    | Current lint PASS                                                                                                                                                                                                                                                              |
|       27 | `npm run typecheck`                                                                                                                                               | Current web, worker, core, and tool-runner typecheck PASS                                                                                                                                                                                                                      |
|       28 | `NEXT_TELEMETRY_DISABLED=1 npm run build`                                                                                                                         | Current web, worker, and core build PASS                                                                                                                                                                                                                                       |
|       29 | `npm run format:check` before this report was added                                                                                                               | Initial FAIL on `docs/governance/STAGE_0_DURABLE_SPECIFICATION_SET_v0.1.md`; no code or fixture failure                                                                                                                                                                        |
|       30 | `npm exec prettier -- --write docs/reports/PROMPT_5_IMPLEMENTATION_REPORT_v0.1.md`                                                                                | Formatted this report                                                                                                                                                                                                                                                          |
|       31 | `npx prettier --write docs/governance/STAGE_0_DURABLE_SPECIFICATION_SET_v0.1.md`                                                                                  | Corrected the sole formatting failure                                                                                                                                                                                                                                          |
|       32 | Final gate block: `npm run format:check`; lint; typecheck; scaffold verification; five required suites; aggregate; build; direct fixture runner; dependency audit | PASS throughout: 13 files and 129 tests; production build PASS; fixture runner reached `READY_FOR_REVIEW`; audit reported zero vulnerabilities                                                                                                                                 |
|       33 | Direct in-memory CLI/golden byte comparison and SHA-256 calculation                                                                                               | PASS; byte-identical at 20,281 bytes and SHA-256 `b107a4bdc5c9ed100da910f8f6aaa0b890e7aadd31cee0e7901dd6dff907fefb`                                                                                                                                                            |
|       34 | SHA-256 checks of `package-lock.json`, controlling handoff, and Stage-0B ZIP                                                                                      | PASS against the retained trust anchors; package lock `e4987148...e0b5750`, Stage-0B ZIP `14850161...75dceb`                                                                                                                                                                   |
|       35 | Initial broad prohibited-integration text scan                                                                                                                    | Non-gating false positive: it matched the required human-boundary sentence containing “contact” and “submit”; no integration code was found                                                                                                                                    |
|       36 | Refined network-client/import scan and fixture secret/personal-data scan                                                                                          | PASS; no production network client/import and no named applicant, pilot-ledger marker, or secret token pattern                                                                                                                                                                 |
|       37 | `node packaging/build-prompt5-patch.mjs --replace`; `node packaging/verify-prompt5-patch.mjs`; archive hash, structure, CRC, and source-equality checks           | Initial adjacent patch package passed, but maker-checker review found recovery/idempotency defects in installer v0.1; that installer was renamed `SUPERSEDED_DO_NOT_USE` and was never run on Steve's AJAS tree                                                                |
|       38 | Bounded installer/verifier hardening and repeated read-only maker-checker review                                                                                  | Added locked control parsing, pre-mutation recovery, partial-copy quarantine, direct same-volume ADD moves, stale-marker reconciliation, immediate destination rechecks, exact installer pinning, protected-path checks, and a no-directory-deletion rollback policy           |
|       39 | Final `node packaging/build-prompt5-patch.mjs --replace`; `node packaging/verify-prompt5-patch.mjs`; `unzip -t`; SHA-256 and byte-count checks                    | PASS; 41 archive entries, 38 payloads, 30 adds, 8 replacements, 0 deletions, exact Stage-0B source equality, and zero files written by the verifier                                                                                                                            |
|       40 | Final repeat of format, lint, typecheck, scaffold verification, five required suites, aggregate suite, build, direct runner/golden comparison, and policy scans   | PASS; 129/129 tests, production build, byte-identical 20,281-byte golden output, unchanged package lock, no runtime network client, and no installer target-temp or directory-deletion primitive                                                                               |

The npm commands emitted a local warning that the `http-proxy` npm environment
configuration will be unsupported in the next npm major version. No proxy value was
printed or recorded. The warning did not change command exit results.

## Test results

| Required class | Files | Tests | Result |
| -------------- | ----: | ----: | ------ |
| Unit           |     6 |    56 | PASS   |
| Contract       |     2 |    49 | PASS   |
| Integration    |     2 |    10 | PASS   |
| Security       |     2 |    11 | PASS   |
| Golden         |     1 |     3 | PASS   |
| Aggregate      |    13 |   129 | PASS   |

The current aggregate proves the fixture-only code path. It does not supersede
pending patch verification, Windows installation/readback, or Steve approval.

## Prompt-5 acceptance mapping

| Requirement                         | Implementation evidence                                                             | Test evidence                                                                     | Status                                          |
| ----------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------- |
| Approved applicant facts            | `approved-facts.ts`; synthetic facts fixture; facts/command policy pins             | `approved-facts.test.ts`; contract tests                                          | PASS                                            |
| One saved public Greenhouse fixture | Exact board/job identity, body hash, minimized evidence index                       | Contract identity, pin, pointer, span, and hash tests                             | PASS within saved fixture                       |
| Source policy                       | `MANUAL_ONLY`, exact board, zero methods/budget, kill switch                        | Policy drift, host/path, state, pin, and unknown-field tests                      | PASS offline only                               |
| Liveness validation                 | Two distinct saved intake/PRE_READY observations                                    | Time boundary, order, duplicate, header-hash, body-hash, and current-status tests | PASS saved evidence; current status not checked |
| Deterministic eligibility           | Two explicit eligibility rules bound to approved facts                              | Missing, negative, semantic-mismatch, and binding tests                           | PASS synthetic fixture                          |
| Explainable fit                     | Twelve ordered requirements, matched provenance, two named preferred gaps, no score | Requirement-semantics and golden tests                                            | PASS synthetic fixture                          |
| Packet metadata and readback        | Three stable JSON artifacts, batch write/read/hash verification                     | Readback mismatch, duplicate, partial-write, and rollback tests                   | PASS in-memory adapter                          |
| Controlled state                    | `DISCOVERED -> SCREENED -> SELECTED -> PREPARING -> READY_FOR_REVIEW`               | Invalid/post-READY transition and failure-state tests                             | PASS test scope                                 |
| Audit record                        | Five transition events plus committed batch receipt; failure history retained       | Audit failure, invalid receipt, replay, and correlation tests                     | PASS in-memory audit                            |
| Human boundary and Track isolation  | No employer-action capability; URL provenance-only wording                          | Injection, URL, dependency, Track-A, secret, and post-READY security tests        | PASS                                            |
| Required test classes               | Unit, contract, integration, security, and golden suites                            | 129/129 aggregate                                                                 | PASS                                            |
| Exact report and rollback           | This report and documented hash-bound release design                                | Adjacent patch/installer dry run and Windows readback                             | PENDING                                         |

## Known gaps and nonclaims

### Prompt-5 completion gates still pending

1. Run the installer dry run on Steve's unchanged Stage-0B Windows tree and confirm
   all 8 replacement preimages and 30 additions are collision-free.
2. Apply the patch attended on Windows and run full file readback, 129-test aggregate,
   build, demo/golden comparison, and rollback-readiness checks.
3. Steve reviews the installed durable specification set and explicitly approves the
   Prompt-5 result.

Prompt 5 remains active until those gates pass. Prompt 6 remains locked.

### Promotion blockers intentionally outside this slice

- no current-live source request or runtime-ratified source freshness target;
- no production-approved Greenhouse source terms or live adapter;
- no real applicant facts, CV registry, cover letter, PDF, ATS extraction, visual QA,
  or real packet;
- no PostgreSQL, migration, authentication, authorization, tenant isolation,
  deduplication, durable queue, or production audit sink;
- no separately authorized AJAS Personal Drive byte store or Drive readback;
- no retention, export, correction, erasure, backup/restore, RPO/RTO, incident,
  accessibility, cost, preview, staging, shadow, or deployment evidence; and
- no external user, billing, employer interaction, or submission capability.

### Evidence limitations

- The full public response body and headers are omitted; repository hashes and byte
  spans are tamper-evident but cannot independently reproduce the human semantic
  review.
- The exact early capture command strings and every exploratory read-only shell
  command were not retained. This report records that limitation and does not invent a
  transcript.
- Test clocks, the 3,600-second saved-evidence window, and policy expiry are fixture
  controls, not production targets or source authorization.

## Hash-bound patch and rollback method

The adjacent release uses an explicit operation manifest, not recursive copying.

### Dry run

1. Verify the target root is exactly
   `C:\Users\steve\Documents\02_CODING\AJAS` and is not a reparse path.
2. Verify the Stage-0B baseline identity and every protected handoff/archive file.
3. Acquire a target-scoped mutex.
4. Verify every `REPLACE` path against its exact Stage-0B byte count and SHA-256.
5. Require every `ADD` path to be absent.
6. Reject generated, dependency, Git, secret, reparse, Track-A, Track-B, Drive, and
   ledger targets.
7. Report the complete no-write plan, collision count, and rollback requirements.

### Apply

1. Stage verified payload bytes on the target volume.
2. Preserve each verified replacement preimage in a unique retained rollback bundle.
3. Create additions only when absent and replace only exact preimages.
4. Verify every postimage and the complete final manifest by readback.
5. Preserve rollback metadata and report zero Git, dependency, Drive, network,
   authenticated-session, employer-contact, and submission actions.

### Rollback

1. Stop if an installed file no longer matches its known Prompt-5 postimage.
2. Restore a replacement only when its retained backup matches the Stage-0B preimage.
3. Remove an addition only when it still matches the known Prompt-5 hash.
4. Never recursively delete the AJAS root, run `git reset --hard`, or overwrite an
   independently changed file.
5. Verify the original Stage-0B 54-file manifest after rollback and preserve rollback
   evidence for attended review.

Rollback deliberately performs no directory deletion. Empty directories created by
an interrupted or rolled-back install may remain and can be reviewed manually; no
pre-existing directory is inferred from contents and removed.

The patch, installer, rollback receipt, and final release hashes cannot be embedded
inside an in-payload report without creating self-reference. The adjacent release
receipt records their exact names, byte counts, SHA-256 values, verification results,
and later Windows readback.

## Final disposition

| Gate                                                        | Status         |
| ----------------------------------------------------------- | -------------- |
| Local fixture implementation                                | PASS           |
| Unit, contract, integration, security, and golden aggregate | PASS — 129/129 |
| Local lint, typecheck, and build                            | PASS           |
| Full formatting gate                                        | PASS           |
| Hash-bound patch/installer Linux static validation          | PASS           |
| Attended Windows PowerShell 5.1 installer dry run           | PENDING        |
| Windows install and file readback                           | PENDING        |
| Windows full tests/build/demo                               | PENDING        |
| Steve durable-specification review and Prompt-5 approval    | PENDING        |
| Prompt 6                                                    | LOCKED         |

`PROMPT_5=COMPLETE` may be recorded only after every pending gate above passes. No
production, external-user, live-source, Drive-runtime, employer-system, or submission
success is claimed by this report.
