# AJAS Handoff - FINAL v1.0

**Document ID:** `AJAS-HANDOFF-1.0-2026-08-29`  
**Version:** 1.0  
**Issued:** 2026-08-29  
**Owner and final decision authority:** Steve Archuleta  
**Status:** CONTROLLING BUILD HANDOFF - APPROVED TO BEGIN STAGE 0  
**Canonical format:** `AJAS_Handoff_FINAL_v1.0.md`  
**Rendering mirrors:** `AJAS_Handoff_FINAL_v1.0.docx` and `AJAS_Handoff_FINAL_v1.0.pdf`

**Authority boundary:** Steve's instruction to issue this final handoff authorizes the new AJAS project to begin Stage 0 specification work and safe local repository setup. It does not authorize production promotion, external-user processing, live-pilot mutation, employer authentication, employer-form interaction, employer contact, attestation, file upload to an employer, or application submission.

## How to use this handoff

1. Upload the canonical Markdown file to the new ChatGPT Project first.
2. Put the Project Instructions from section 24.2 into the new project's settings.
3. Send the startup prompts in section 24.3 one at a time.
4. Keep Track A, Track B, and Track C isolated. The new project builds Track C only.
5. Treat every `VERIFY_BEFORE_USE`, `TO_BE_RATIFIED_STAGE_0`, and deferred decision as a gate, not as permission to guess.
6. Preserve this v1.0 file unchanged. A correction creates a new version and change record.

## Contents

- Sections 1-5: executive direction, track boundaries, pilot ground truth, evidence, and engineering lessons
- Sections 6-11: architecture assessment, workflow, data authority, technical shape, safety, and roadmap
- Sections 12-16: governance, technical answers, adopted rulings, project startup, and asset inventory
- Sections 17-23: production requirements, reference architecture, agents, tools, data contracts, operations, testing, and local repository
- Section 24: new ChatGPT Project instructions and startup prompts
- Appendices A-G: state vocabulary, source register, resolution and audit traceability, permission matrix, and glossary

## Document purpose and source set

This final reconciles the following preserved source documents and records:

1. `AJAS_Handoff_GPT_v1.0_2026-08-29.md`
2. `AJAS_Handoff_Claude.md`
3. `AJAS_Handoff_Merge_Round_1__GPT_to_Claude__2026-08-29.md`
4. `AJAS_Handoff_Merge_Round_1__Claude_Response__20260829.md`
5. `AJAS_Merge_Memo_Claude_to_GPT.md`
6. `AJAS_Handoff_Merge_Round_M2__GPT_to_Claude__2026-08-29.md` - GPT-held merge record; not present in Steve's supplied archive listing on 2026-08-29
7. `AJAS_Handoff_FINAL_CANDIDATE_v0.9.md`
8. `AJAS_v0.9_Claude_Audit__20260829.md`
9. `AI_Agent_Architecture_Breakdown_and_App_for_AJAS.pdf` - verified local research copy; SHA-256 recorded in the source-copy table below
10. Companion AJAS SaaS prompt - locally captured as `Pasted markdown.md`; no canonical original upload filename was assigned
11. `Automated_Job_Application_System_Master_v1.0_SIGNED.docx`, approved by Steve on 2026-08-27, plus later amendments for the 8:00 AM/8:00 PM review windows and the controlling Friedman's employment date

Local source-copy SHA-256 record used for this assembly:

| Source copy | SHA-256 |
|---|---|
| `AJAS_Handoff_GPT_v1.0_2026-08-29.md` | `37548243d451425fc7ccfdfee60747bec950a8439147f444d2996b1528120acb` |
| `AJAS_Handoff_Claude.md` | `56879cb1a9b9082cbda00d144df469c1c5fcc2bf7e19b71a6aaac7e1eec8ff0d` |
| `AJAS_Handoff_Merge_Round_1__GPT_to_Claude__2026-08-29.md` | `b00e04aae77454b13606665440fa17c412b7bf8d988877e562037a706d2573ab` |
| `AJAS_Handoff_Merge_Round_1__Claude_Response__20260829.md` | `45db000d717a842a419286866046f2a5f5c1065637070dafa60b9df6174d1473` |
| `AJAS_Merge_Memo_Claude_to_GPT.md` | `311513c293d764ce1a1e6f92d39acd9042e03afb8ab5654906ed46facadf1db9` |
| `AJAS_Handoff_Merge_Round_M2__GPT_to_Claude__2026-08-29.md` | `cc69fd03349ef2e4f0e106d8a8ff5eb59e542d261d16652351f1f3ecadd6c7aa` |
| `AJAS_Handoff_FINAL_CANDIDATE_v0.9.md` | `71ec5c787ba43d66198217ecd8d38a31fa9f094b9c8e4fdc75c25ec5e63afbaa` |
| `AJAS_v0.9_Claude_Audit__20260829.md` | `07a9dca5059e46ff1846ca7f606e58e65d42d0a6d2236e57689db98d7c3cf7f1` |
| `AI_Agent_Architecture_Breakdown_and_App_for_AJAS.pdf` | `516b1fde8f71f84b0729a0ae1c70b91b12378cc9be3ae9ce859c9c1ec0d3ac43` |
| `Pasted markdown.md` | `d6184c33dd658914c504c39d6e1821f3617f6e593f76b8b999be7ea8ce9c340a` |
| `Automated_Job_Application_System_Master_v1.0_SIGNED.docx` | `e1962dc910c65f0f3189b374f7019e35a279fddf5201a01ea3a73d3f500517bd` |

These hashes identify the exact local copies used during assembly. They do not establish identity with any later renamed or re-exported copy.

Claude's audit reported alternate transmitted filenames for source items 1 and 4. Steve's archive listing and the hashed local copies use the filenames shown above; this final therefore uses the directly observed names and preserves Claude's discrepancy as audit provenance rather than changing the files.

Content precedence after issuance is:

1. Steve's latest explicit instruction or signed change record
2. For Track A and Track B, the signed Master v1.0 as amended, approved Evidence Bank facts, and current canonical ledger/readback
3. For Track C product development, this final handoff and later approved architecture decision records
4. Accepted Round-1 resolutions, merged R2/R13 safeguards, Round-M2 corrections, and Claude's v0.9 audit
5. Agreed material from both source handoffs
6. Architecture research and the companion SaaS prompt
7. Clearly labeled planning hypotheses and deferred decisions

Claude formally accepted 21 of GPT's 23 Round-1 resolutions. R2 and R13 were accepted as merged with the safeguards required by Steve's attended-pilot rules. Claims and decisions use these labels:

- **VERIFIED:** confirmed by direct source or readback during final assembly.
- **REPORTED:** recorded in a source handoff or operator statement but not independently confirmed during final assembly.
- **VERIFY_BEFORE_USE:** time-sensitive, platform-specific, or unresolved; verification is mandatory before operational reliance.
- **ADOPTED:** approved for the stated scope by Steve's final-output directive on 2026-08-29.
- **TO_BE_RATIFIED_STAGE_0:** a measurable target or provider choice that must be decided from evidence before the relevant promotion gate.

The source handoffs and merge memos remain preserved unchanged. This Markdown supersedes them as the controlling Track-C product-development briefing. It does not supersede approved Track-A evidence, the current pilot ledger, or the signed Master v1.0 as amended where those govern Tracks A and B. Historical sources remain provenance records.

---

## 1. Executive decision

AJAS is viable as a **human-controlled job-discovery and application-preparation system**. The strongest first product is `AJAS Personal`: a single-user application for Steve that converts the proven attended-pilot workflow into a deterministic, auditable product.

The first product does not authenticate to employer systems, enter or upload data into employer forms, make attestations or consents, contact employers, or submit applications. `READY_FOR_REVIEW` is the last autonomous state. Steve performs every employer-system action, reviews every answer, and supplies the final submission confirmation.

The 77-page architecture proposal remains useful future-product research. The proposal is not the live-pilot operating procedure and is not an implementation specification. Product development begins with requirements, a frozen state model, source-of-truth rules, a data-flow map, a threat model, and a permitted-source review - not with the entire proposed technology stack.

AJAS's defensible value is **truthfulness, claim provenance, verified packet quality, organization, explainable fit, and saved user time**. Unchecked application volume is not a product objective.

---

## 2. Three isolated AJAS tracks

### Track A - Active attended pilot

GPT and Claude independently search permitted public sources and prepare application packets. Steve reviews materials and performs every employer-system action. Track A uses the existing `ATTENDED_PILOT` Drive root and the existing Applications Log.

Track-A historical governance is anchored by `Automated_Job_Application_System_Master_v1.0_SIGNED.docx`, approved by Steve on 2026-08-27, as amended by the approved 8:00 AM and 8:00 PM review windows and the later Friedman employment-date ruling. The later ruling, **March 3, 2025-Present**, supersedes the older wording in the signed Master wherever that applicant fact is used.

### Track B - Paused legacy machine-track experiment

`AJAS_Operations` and Technical Build Package v1.1 belong to a separate, paused machine-track experiment. The blank workbook is not locked or protected; no installed production structure exists. Track B resumes only through separate Steve authorization and its staged test process.

**PARTIALLY VERIFIED BY CLAUDE - 2026-08-29; VERIFY BEFORE REACTIVATION:** Claude confirmed authorship of the v1.1 PASS review and the 47/47 local harness result. Source artifacts, review results, checksums, and current Drive state still require fresh readback before any Track-B approval or installation.

### Track C - AJAS Personal and future product

Track C is a new software product. Track C receives a separate database, separate storage authorization, separate source configuration, separate authentication, and separate audit history. Track C never reads from or mutates Track A at runtime. A controlled, versioned snapshot of approved facts may be imported only through an explicit migration and provenance process.

No track silently becomes another track. Pilot cutover requires test, shadow operation, rollback readiness, measured gates, and Steve's explicit authorization.

---

## 3. Track A ground truth: attended pilot

### 3.1 Operating model

- GPT prepares at most one qualified, non-duplicate packet during each midnight and noon Pacific shift.
- Claude prepares at most one qualified, non-duplicate packet during each 6:00 AM and 6:00 PM Pacific shift.
- Four qualified packets per day is a ceiling, not a quota. A shift with no honest fit produces no filler packet.
- Canonical business time is `America/Los_Angeles`.
- **REPORTED - VERIFY_BEFORE_USE:** Claude's current scheduler accepts UTC cron rather than a named time zone. During Pacific daylight time, the reported mappings are 13:00 UTC and 01:00 UTC on the following UTC date; during Pacific standard time, the mappings become 14:00 UTC and 02:00 UTC. A controlled daylight-saving adjustment and post-change verification are required. UTC values are implementation details, not the business schedule.
- **VERIFY_BEFORE_OPERATIONAL_RELIANCE:** GPT's midnight/noon time-zone configuration and daylight-saving behavior require separate schedule readback. Claude's platform behavior does not establish GPT's behavior, and no automatic DST claim may be inferred.
- Every fresh scheduled session reads the approved search profile, application reference, CV index, ledger rule, current Drive folders, and canonical ledger before selecting a role.
- Permitted sources include public employer career pages and public ATS postings whose current access method is allowed. LinkedIn and Indeed remain Steve's manual channels; agents never sign in to, fetch, or scrape either service.
- Steve alone handles employer login, employer-form activity, attestations, uploads, final review, and submission.

### 3.2 Canonical Drive and ledger references

| Object | Canonical reference | Verification status |
|---|---|---|
| Automated Job Application System root | `1FeG5S_9MbCixbF2u7SezhJbxwdBfBaTb` | VERIFIED by Claude readback 2026-08-29; verify before mutation |
| `00_Governance` | `1TRfE7ORK2-VCQBZ_TyKhBVEfSlteSOY2` | VERIFIED by Claude readback 2026-08-29; no final-file upload claimed by this document |
| `01_System` | `1ONO6S2U3otr7H4CNYmC_zj8LtU7Z4EGH` | VERIFIED by Claude readback 2026-08-29 |
| `02_Evidence_Bank` | `1pJ1ORAwcEEU8zSn0fUloyC4FyEbuGMYc` | VERIFIED 2026-08-29 |
| `04_Jobs` | `1DTASjXfiECXhjI-81zLQhmXlnVB2R08Y` | VERIFIED by Claude readback 2026-08-29 |
| `04_Jobs/ATTENDED_PILOT` | `1eF1fIgkgUDxwi1T5311YOhQBL5_KW2Jo` | VERIFIED 2026-08-29 |
| `GPT_Inbox` | `1K4J2E2qzQUiYyawpkQt9KWZYsqNq1cdZ` | VERIFIED by Claude readback 2026-08-29 |
| `Claude_Inbox` | `1DKZkgo1LZiAscINebbmnp6QQPApRHAyU` | VERIFIED by Claude readback 2026-08-29; parent-path detail is non-authoritative |
| `AJAS_Operations` workbook | `1yCfEeRfJmZ05NVRPW4hcbZEljesFkRhoBGEzTzYNWGA` | VERIFIED by Claude readback 2026-08-29; paused Track B, not the pilot ledger |
| Active Applications Log | `1w6wMusQSXVAJwgthySIf1jsgIGKJKb7pTjSdKZ4WUL4` | VERIFIED 2026-08-29 |
| Approved search profile | `AJAS_Search_Profile_Approved_2026-08-29.md`, ID `1N_F21o6glOy1GZvtBboz-73OVpPbBPS7` | VERIFIED 2026-08-29 |
| Approved application reference | `Steve_Archuleta_Application_Reference_v2.md`, ID `17p2hXpfvQfuTg8Txp41gqIFbqaa3-CBt` | VERIFIED 2026-08-29 |
| CV header-variant index | `CV_Header_Variant_Index_v2_2026-08-29.md`, ID `1OXETlNsT0Zx9Y_p5qAFp-h75JKHRky7i` | VERIFIED 2026-08-29 |
| Approved base CV PDF | ID `1YOxkZxAtVzFKAYFWOpiFeWHLqvoHMV6z` | VERIFIED by Claude readback 2026-08-29 |
| Attended-pilot ledger rule | ID `1UnHKKubsPKDBJTNGCW4SOx-0-CFuII-A` | VERIFIED by Claude readback 2026-08-29 |

### 3.3 Required packet and employer-upload instruction

Every packet announced READY contains:

1. `00_START_HERE__10_MINUTES.md`
2. A saved live job-description snapshot with official URL and retrieval date
3. A one-page custom cover-letter PDF
4. The matching `__ATS_APPROVED.pdf` tailored-CV variant
5. A merged `Cover_and_CV` PDF
6. Editable Markdown or source files when useful

Every required PDF must exist in the designated Drive job folder and pass Drive readback before READY. `START HERE` identifies the file or files actually requested by the employer form. A résumé-only field receives the approved CV unless the employer expressly requests another format. Separate résumé and cover-letter fields receive separate files. The merged PDF is not the automatic employer upload.

Folder names follow `YYYY-MM-DD__Company__Role`. Filenames are deterministic, role-specific, and non-overwriting.

### 3.4 R2 merged-PDF repair protocol - ACCEPTED AS MERGED

The preparing agent attempts every required upload and verifies every artifact by Drive readback. A Claude merged-PDF upload failure triggers the following exception path:

1. The packet remains `PREPARING` and receives an `UPLOAD_REPAIR_REQUIRED` operational flag.
2. Claude records the dated error and creates one idempotent `MERGE_MIRROR` request in `GPT_Inbox`.
3. The request contains the target folder ID, cover-letter source ID, tailored-CV source ID, expected output filename, observed sizes or hashes when available, exact error, and unique repair key.
4. GPT builds or uploads the merged PDF into the same job folder, verifies Drive readback, and closes the repair request.
5. READY becomes permissible only after all three PDFs pass readback.

Chat delivery or Steve's manual drag is disaster recovery only after direct upload and the authorized repair path both fail. Manual recovery still requires successful Drive readback before READY.

**VERIFIED dated size observation - 2026-08-29:** the six approved CV variants range from 600,066 to 600,098 bytes. A verified Gap Inc. merged PDF measured 630,830 bytes. **REPORTED:** Claude observed corruption or rejection of inline binary uploads above roughly 10 KB. Current sizes and connector behavior are pilot observations, not permanent product architecture.

### 3.5 Evidence, CV, and letter rules

- Use only Steve-approved facts with provenance. Never invent experience, metrics, technologies, education, credentials, dates, or outcomes.
- Friedman's Home Improvement is **March 3, 2025-Present**.
- Use only CV filenames ending in `__ATS_APPROVED.pdf`, selected through the v2 index.
- Do not dynamically rewrite the attended-pilot CV body.
- Preserve the six approved role families: Data Science/Analytics; Risk/Forecasting/Quant; Machine Learning/MLOps; GenAI/RAG/NLP; Azure Data Engineering; Financial Engineering/Quant Research.
- Cover letters use Steve's voice and only approved facts. Prohibited claims include unsupported GRPO metrics, PyTorch experience, or portfolio-coverage claims.
- Every cover letter names material gaps honestly and remains interview-defensible.
- The cover-letter PDF is exactly one page.

### 3.6 Liveness, deduplication, and ledger control

- Verify posting liveness during selection and immediately before READY.
- Deduplicate through existing job folders and the canonical Applications Log using employer, role, posting ID, and canonical URL.
- Maintain one Applications Log. Update the existing row in place; never append a duplicate status row.
- GPT writes Sheet updates directly where capability permits. Claude sends one exact, idempotent ledger-update request when direct cell editing is unavailable.
- Every ledger update requires readback.
- No second tracker, alternate pilot root, or competing canonical state is permitted.
- Mandatory cross-agent review is not required for every packet. GPT and Claude operate independently and coordinate through deduplication, the ledger, and explicit repair handoffs.

### 3.7 Conditional Gmail behavior - R13 ACCEPTED AS MERGED

**PARTIALLY VERIFIED BY CLAUDE - 2026-08-29; VERIFY_BEFORE_USE:** Claude confirmed that Gmail connector tools were present in Claude's workspace session and that Claude's v4 scheduled instructions contain an optional, conditional, read-only employer-response check. Account identity, OAuth scope, continuing authorization, and actual read behavior remain unverified for operational reliance.

The conditional check is not a guaranteed monitoring service, never blocks packet preparation, and carries no authority to send, reply, forward, label, archive, or delete email. Account identity, OAuth scope, continuing authorization, retention, connector availability, and observed read behavior require verification before any operational claim becomes VERIFIED.

Gmail is not an AJAS Personal MVP dependency. Any future email integration requires separate opt-in consent, least-privilege scope, revocation, retention, provider, account, and data-flow controls.

### 3.8 Pilot invariants

Every Track-A run must:

- read the approved search profile, application reference, CV index, and ledger rule;
- use only approved CV variants;
- select one honest, live, non-duplicate fit or report no qualified match;
- use permitted public sources only;
- complete and read back the required packet before READY;
- identify the correct employer upload;
- keep the official link and prepared answers truthful;
- update the existing ledger row idempotently;
- preserve existing files and the other agent's work;
- leave all employer-system activity and submission to Steve.

After Steve reports a submission, the responsible agent files a dated confirmation note and the supplied screenshot or receipt in the existing job folder, verifies Drive readback, and updates the same ledger row idempotently. A user report supports `SUBMITTED_BY_USER`; `SUBMISSION_CONFIRMED` requires receipt or employer evidence. A screenshot above an agent's binary-upload ceiling follows the same single, idempotent GPT repair path defined for merged PDFs. No confirmation file or ledger row is silently overwritten.

---

## 4. Results snapshot and validation evidence

The following snapshot was verified by fresh, read-only Applications Log and `ATTENDED_PILOT` folder readback on **2026-08-29 at 21:30 UTC / 14:30 PDT**:

| # | Employer - role | Agent | Verified ledger/folder state |
|---:|---|---|
| 1 | Revenue Analytics - Data Scientist | GPT | `SUBMITTED 2026-08-28` |
| 2 | OpenX - Business Intelligence Data Analyst | GPT | Ledger reports `LIVE - PACKET NOT IN DRIVE`; no OpenX folder present in the pilot root. Posting liveness requires a fresh official-link check. |
| 3 | PointClickCare - Associate Data Scientist | Claude | `SUBMITTED 2026-08-28` |
| 4 | QuestBridge - Data Analyst | Claude | `CLOSED_BEFORE_SUBMIT 2026-08-29` |
| 5 | Wpromote - Junior Data Scientist | GPT | `SUBMITTED 2026-08-29 09:58 PDT` |
| 6 | Gap Inc. - Senior Analyst, Data Science Enablement | GPT | `READY - Steve submit`; folder and all three PDFs present. The verified merged PDF is 630,830 bytes. |
| 7 | Accela - Associate Data Scientist, AI Submission Analysis | Not yet logged | **INCOMPLETE OBSERVATION - NOT READY:** an additional folder exists with START HERE, a posting snapshot, cover-letter source, cover-letter PDF, and approved CV PDF, but no merged PDF and no Applications Log row were present at readback. Preserve the folder and require completion/readback plus an idempotent ledger update before READY. |

The canonical Applications Log contained six rows; row 7 above is a folder-only observation and is deliberately not represented as a completed or logged application. The snapshot becomes historical immediately after issuance and must be refreshed before operational use. Response and interview data are useful operating evidence and product signals, not proof of product-market fit or willingness to pay.

No response or interview state appeared in the six ledger rows at readback. This was not an inbox check and does not prove that no employer message exists.

---

## 5. Twelve dated engineering lessons

These lessons explain the pilot rules. Connector behavior and size observations remain dated implementation evidence rather than permanent product requirements.

1. **Connector capabilities are asymmetric.** Text creation, native copies, binary uploads, and Sheet-cell editing differ by platform. Capability tests and readback must precede promises.
2. **Small deterministic files reduce failures.** Compact document generation can improve transport reliability, but actual file size must remain an observed metric rather than an architectural guarantee.
3. **Precompute expensive approved artifacts.** Approved CV variants can be built once and copied byte-for-byte during runtime.
4. **Stream large binaries outside model context.** Large binary content should move through file transport rather than model tokens.
5. **Postings can close quickly.** Selection-time and pre-READY liveness checks are mandatory; same-day human review remains valuable.
6. **Deduplicate every written store.** Multi-shift discovery requires one posting identity across folders, database rows, and ledger records.
7. **Scheduled preparation needs complete prompts, standing bounded authority, and durable state.** Permission dialogs and missing context can silently prevent output.
8. **One writer per artifact plus idempotent repair handoffs prevents conflicts.** A handoff is an exception path, not mandatory review of every packet.
9. **Truthfulness is a hard gate.** Approved facts, claim provenance, named gaps, and deterministic validation protect application quality.
10. **Non-destructive means authorized, auditable change - not permanent immobility.** Existing artifacts are not silently deleted, renamed, moved, or overwritten. Authorized ledger updates, versioned corrections, soft deletion, user export, and verified erasure remain possible.
11. **Automation instructions are versioned configuration.** Schedule edits require controlled changes and post-change verification.
12. **A fired schedule without a valid artifact is a failure state.** Last-run evidence, failure reasons, and repair status must remain visible.

---

## 6. Assessment of the architecture proposal

### 6.1 Concepts worth preserving

- Grounded user evidence rather than invented claims
- Separate discovery, fit, document, filing, and tracking responsibilities
- Human review before consequential action
- Durable audit history, consent, privacy, correction, and deletion controls
- Standard packet structure and controlled state
- Asynchronous jobs for longer AI work
- A web interface suitable for nontechnical users

### 6.2 Required corrections

| Proposal item | Candidate decision | Corrected direction |
|---|---|---|
| Universal auto-submission | Reject for MVP | Stop autonomous action at `READY_FOR_REVIEW`; no employer authentication or form interaction. |
| LinkedIn, Indeed, broad scraping | Reject | Use permitted public employer/ATS sources, licensed feeds, partner APIs, and user-provided URLs after source-specific review. |
| Six autonomous agents and A2A | Defer | Use testable modules inside one deterministic application service. |
| Custom MCP for every integration | Defer | Start with ordinary typed adapters. |
| LangGraph and CrewAI at launch | Defer | Use explicit functions, durable jobs, and a controlled state machine. |
| Vector database for a small evidence bank | Modify | Start with structured facts, source IDs, dates, allowed uses, and provenance. |
| Dynamic CV rewriting in the pilot | Reject | Select an approved CV variant. Future edits require user approval and versioned provenance. |
| Three-file-only packet | Modify | Preserve START HERE, live snapshot, three PDFs, and useful editable sources. |
| Alternate pilot roots or trackers | Reject | Preserve one pilot root and one pilot ledger. |
| Append-only status rows | Reject | Use idempotent update-in-place keyed by application and posting identity. |
| Human approval before every internal action | Modify | Standing authority may cover bounded search, generation, storage, and maintenance; employer-system action remains human-only. |
| Fixed 50/30/20 fit weights | Defer | Show matched evidence, unresolved requirements, named gaps, and user override; validate any future scoring. |
| Naive protected-trait or gender keyword detector | Reject | Use transparent criteria, evaluation data, adverse-impact monitoring, and expert review. |
| “Legally binding” consent hash | Reject | Store auditable consent events; legal effect requires qualified review. |
| Fixed 24-hour token rotation | Correct | Use provider-recommended OAuth, short-lived access tokens, protected refresh tokens, and revocation. |
| Blanket encryption claims | Correct | Configure, test, and document deployment-specific encryption. |
| “Never share data” claim | Correct | Maintain an accurate data-flow map and subprocessor register. |
| Twelve-week global SaaS commitment | Reject | Use staged evidence gates and measured schedules. |
| Fixed pricing and unit economics | Defer | Instrument actual costs and validate willingness to pay before billing. |

Human review is a risk control, not a legal shield or compliance guarantee. Legal, privacy, employment, and source-access claims require qualified review and current evidence.

### 6.3 Reconciled keep, defer, and drop decisions

| Keep for AJAS Personal | Defer until evidence and gates | Exclude from the current plan |
|---|---|---|
| One deterministic application service | Multi-provider or multi-source expansion | Universal auto-submission |
| Managed PostgreSQL with migrations | Optional email-response monitoring | LinkedIn or Indeed automation/scraping |
| Structured approved-facts vault | Browser-assisted prefill only after a separate ATS-specific terms, privacy, consent, autosave/transmission-boundary, rollback, and reliability design | Six independently deployed autonomous agents |
| Permitted public-source adapters | Embeddings or vector search after corpus growth | Custom MCP servers for every adapter |
| Explainable fit with named gaps | LangGraph only after demonstrated need | CrewAI at MVP |
| Deterministic packet generation and validation | Billing after willingness-to-pay evidence | Enterprise, white-label, and SSO at MVP |
| One durable-job mechanism when needed | Azure production topology after beta evidence | Multiple competing queue frameworks |
| Audit, consent, provenance, and readback | Mobile applications | PII-derived model training by default |

---

## 7. Corrected AJAS Personal workflow

### 7.1 Bounded 12-step lifecycle

1. Steve supplies or approves structured facts, evidence sources, preferences, constraints, and CV variants.
2. AJAS searches permitted configured sources and accepts user-provided posting URLs.
3. AJAS verifies posting liveness and extracts role, employer, location, compensation when stated, requirements, and source identity.
4. AJAS deduplicates by employer, role, posting ID, and canonical URL.
5. AJAS shows matched evidence, unresolved requirements, named gaps, and source citations.
6. Steve selects a role or grants bounded standing preparation authority under a policy approved in Stage 0.
7. AJAS generates a truthful packet using approved facts only.
8. AJAS validates content, provenance, filenames, page counts, ATS text, visual rendering, and required artifacts.
9. AJAS stores the packet, performs readback, rechecks the official link, and enters `READY_FOR_REVIEW` only after every gate passes.
10. Steve opens the official employer form and performs all login, entry, upload, attestation, consent, review, and submission activity.
11. Steve supplies or confirms the submission receipt.
12. AJAS stores the confirmation and advances the existing application record idempotently.

`READY_FOR_REVIEW` is the last autonomous state. Steps 10-12 complete the broader application lifecycle without giving AJAS authority over the employer system.

### 7.2 Stage-1 modules

The useful responsibilities from the proposed “six agents” become modules inside one service:

1. **Facts and evidence module:** approved facts, provenance, allowed uses, sensitivity, and version history
2. **Source module:** URL intake, allowlisted source adapters, liveness, normalization, and canonical posting identity
3. **Screening module:** deterministic eligibility checks plus explainable evidence and gaps
4. **Packet module:** cover letter, approved CV selection, merged PDF, START HERE, and source snapshot
5. **Validation module:** claim, page, filename, ATS-text, visual, link, and readback checks
6. **Application-state module:** state transitions, receipts, follow-ups, audit events, and corrections

The modules do not require A2A, CrewAI, custom MCP infrastructure, or six separate deployments.

### 7.3 Initial source strategy

Stage 0 creates a versioned allowlist of roughly 25-50 employers. Initial candidates include user-provided official URLs, selected public employer career pages, and selected Greenhouse or Lever board interfaces. The currently observed endpoint patterns include:

- `boards-api.greenhouse.io/v1/boards/{company}/jobs`
- `api.lever.co/v0/postings/{company}`

**VERIFY_AT_IMPLEMENTATION:** public visibility does not by itself establish authorized product access. Current official documentation, terms, rate limits, robots/access rules where applicable, data fields, attribution, caching, and change behavior require source-specific review before enablement. Ashby and other ATS or employer sources follow the same gate. No access-control bypass is permitted.

### 7.4 Fit and truthfulness model

The MVP does not suppress opportunities through an unvalidated numeric score. The fit view contains:

- each material requirement;
- matching approved evidence and provenance;
- unresolved or ambiguous requirements;
- named gaps;
- disqualifying constraints when present;
- user override and reason;
- extraction confidence separate from fit judgment.

Any future numeric model requires a defined target, evaluation set, calibration, error analysis, adverse-impact monitoring, and an override path.

---

## 8. Source of truth, storage, and state machine

### 8.1 Stage-1 authority

- PostgreSQL is the source of truth for users, facts, sources, jobs, applications, states, approvals, audit events, consent events, connector authorizations, artifact metadata, costs, and repair events.
- A new, separately authorized `AJAS Personal` Drive root is the sole authoritative byte store for Stage-1 packet files.
- Track-A folders are not the AJAS Personal storage root and are never a runtime dependency.
- Revoking Drive access does not erase database state or audit history. Revocation prevents future file operations until reauthorization.
- Temporary generation files follow a defined cleanup policy after successful verified storage.

### 8.2 Stage-2 authority

From private alpha onward, application-controlled object storage becomes the authoritative packet-byte store. Drive becomes optional export or sync. One artifact version has one authoritative byte location; synchronized Drive copies are user-facing derivatives with recorded source version and checksum.

Migration requires a versioned plan, byte verification, rollback, and no competing canonical copies.

### 8.3 Controlled lifecycle

Core path:

`DISCOVERED -> SCREENED -> SELECTED -> PREPARING -> READY_FOR_REVIEW -> SUBMITTED_BY_USER -> SUBMISSION_CONFIRMED`

Later lifecycle states:

- `INTERVIEWING`
- `OFFER_RECEIVED`
- `REJECTED_BY_EMPLOYER`
- `WITHDRAWN_BY_USER`

Alternate or exception outcomes:

- `REJECTED_AS_POOR_FIT`
- `CLOSED_BEFORE_SUBMIT`
- `DUPLICATE_SKIPPED`
- `ERROR_RETRYABLE`
- `ERROR_NEEDS_USER`

`SUBMITTED_BY_USER` records a user report. `SUBMISSION_CONFIRMED` requires a receipt, confirmation page, or employer acknowledgment. `INTERVIEWING` and `OFFER_RECEIVED` are later lifecycle states, not generic terminal labels. `UPLOAD_REPAIR_REQUIRED` is an operational flag under `PREPARING`, not a replacement lifecycle state.

### 8.4 Transition contract

Every transition records:

- stable user, job, posting, and application identifiers;
- prior and new state;
- timestamp in UTC plus business-zone presentation;
- actor and actor version;
- reason and evidence reference;
- idempotency key;
- authorization or consent reference when relevant;
- audit event;
- retry count and next retry when relevant.

Every generative or extraction run also records the prompt version, model/provider version, template version, parser/extractor version, validator version, approved-evidence snapshot/version, and job-posting snapshot/version. Artifact metadata links every rendered file to this reproducibility record.

Stage 0 defines valid transitions, correction and reopening rules, duplicate/repost handling, retry exhaustion, stale posting behavior, confirmation reversal, withdrawal, and user-requested erasure effects before implementation.

### 8.5 Minimal data model

Stage-1 entities include:

- `User`
- `ApprovedFact`
- `EvidenceSource`
- `PreferenceConstraint`
- `JobSourcePolicy`
- `JobPosting`
- `Application`
- `ApplicationTransition`
- `Artifact`
- `ArtifactVersion`
- `ConsentEvent`
- `ConnectorAuthorization`
- `AuditEvent`
- `BackgroundJob`
- `RepairRequest`
- `CostEvent`

Subscription, credit, enterprise, and training-data tables remain deferred until the relevant product decision exists.

---

## 9. Technical shape

### 9.1 Stage-1 components

- **Web application:** TypeScript and a current supported stable Next.js release selected at setup
- **Database:** managed PostgreSQL with migrations, backups, and authorization controls
- **Authentication:** a reputable managed identity provider or carefully implemented standards-based authentication
- **Workflow:** typed service functions and one durable background-job mechanism when asynchronous work warrants a queue
- **Documents:** deterministic templates, PDF rendering, ATS-text extraction, visual QA, provenance checks, and readback
- **Storage adapter:** Stage-1 Drive root, followed by Stage-2 object storage plus optional Drive export
- **AI adapter:** provider-neutral interface, strict structured output, citations to approved evidence, and deterministic validators
- **Observability:** structured logs, audit events, error tracking, liveness results, latency, and cost metrics
- **Source adapters:** one interface with source-specific policy, identity, rate-limit, and terms metadata

### 9.2 Development environment

- Private GitHub repository
- VS Code for editing and review
- Light local toolchain on Steve's Windows development computer; brand and model are unverified and architecturally irrelevant
- Managed development database rather than a mandatory heavy local database/container stack
- Cloud development environment as an optional fallback after current pricing and security review
- Small, reviewable commits and protected main branch
- Separate development, test, staging, shadow, and production data boundaries

Current supported runtime and framework versions are selected and recorded during Stage 0B. Old device names, fixed Node versions, provider quotas, and permanent free-tier claims do not belong in the durable architecture.

### 9.3 Preview, staging, and Azure

Vercel is the provisional Next.js preview and Stage-1 staging candidate. Stage 0 verifies current terms, pricing, plan limits, authentication needs, privacy/security behavior, regional support, runtime compatibility, and test-data restrictions before adoption. A failed gate permits an equivalent preview platform without changing the core architecture.

Production hosting remains a beta-gate decision. Azure is a later candidate for models, secrets, monitoring, storage, or workers after measured requirements justify each service. Azure credits and résumé value do not override architecture, cost, privacy, or reliability evidence.

### 9.4 Technologies postponed

- A2A
- custom MCP infrastructure
- CrewAI
- complex LangGraph workflows
- general browser automation
- employer-form prefill
- multiple queue frameworks
- vector database before retrieval scale
- Stripe, credits, enterprise features, and mobile applications

---

## 10. Security, privacy, fairness, and authorization

### 10.1 Four distinct authorization layers

1. **Product authentication:** access to the AJAS account
2. **Storage authorization:** permission for the selected Drive or object-storage operations
3. **Bounded preparation authority:** permission for configured search, screening, generation, storage, and maintenance
4. **Per-application human action:** employer login, form interaction, attestations, uploads, communication, and submission

No layer implies another layer. Standing preparation authority never becomes employer-system authority.

### 10.2 Baseline controls before external users

- Data inventory and end-to-end data-flow diagram
- Threat model and misuse cases
- Least-privilege OAuth and tested revocation
- Protected secrets and refresh tokens; no secrets in source, prompts, logs, or artifacts
- Tenant isolation and authorization tests
- File-type, size, malware, decompression, and prompt-injection defenses
- Source allowlist and dated source/terms register
- Data minimization and purpose limitation
- Retention periods for source data, facts, artifacts, receipts, logs, and backups
- Export, correction, soft deletion, verified erasure, and legal-hold behavior
- Backup, recovery, incident response, and breach procedures
- Subprocessor inventory and accurate third-party disclosure language
- No training on user application data by default
- Accessibility and support process
- Claim-level provenance and human override
- Evaluation sets, false-positive/false-negative analysis, and adverse-impact monitoring
- Qualified legal and privacy review before any external alpha user supplies personal data; public-facing policies and launch review before beta or public access

Compliance claims follow documented implementation and qualified review. GDPR, CCPA/CPRA, employment, accessibility, anti-discrimination, and source terms remain work programs rather than checklist labels.

### 10.3 Sensitive answers

Voluntary demographic answers, disability information, veteran status, salary expectations, attestations, conflict disclosures, and other sensitive or consequential fields are not inferred or reused automatically without an explicit approved policy and per-application visibility. Unknown answers remain unknown.

---

## 11. Roadmap and evidence gates

All durations are **PLANNING_HYPOTHESES**, not commitments.

### Stage 0A - Specification and validation (approximately 1-2 weeks)

- Define the narrow job-to-packet requirement
- Freeze state vocabulary and transition rules
- Define source of truth and artifact authority
- Complete data flow, threat model, and misuse cases
- Complete initial source/terms review
- Define approved-fact schema and provenance rules
- Define document and readback acceptance tests
- Resolve provider terms, OAuth consent, storage authorization, data minimization, retention, correction, export, and erasure rules before any real AJAS Personal account or Steve personal data enters Stage 1
- Record Steve's Stage-0 decisions from §14

**Gate:** every generated claim can be traced to approved evidence; autonomous authority ends before employer-system activity; source and storage authority are unambiguous.

### Stage 0B - Smallest deployable skeleton

Stage 0B begins only after Stage 0A passes. Stage 0B creates the private repository, supported runtime, database migrations, authentication skeleton, audit-event skeleton, continuous tests, and provisional preview deployment. No real pilot data enters the skeleton.

**Gate:** a sanitized test user can authenticate, create an audited test record, and complete a reversible deployment without touching Track A.

### Stage 1 - Steve-only AJAS Personal (approximately 4-6 additional weeks)

- Facts vault and approved CV registry
- User URL intake and small allowlisted source discovery
- Liveness, normalization, and deduplication
- Explainable fit and gaps
- Packet generation and deterministic validation
- Separate AJAS Personal Drive storage and readback
- Review dashboard and official-link handoff
- Manual submission confirmation and state update
- Cost, latency, failure, and repair instrumentation

Run synthetic tests, then sanitized tests, then shadow comparisons beside the attended pilot. No Track-A mutation is permitted.

**Gate:** repeated truthful, complete, non-duplicate packets; 100% required artifact readback; no unauthorized employer-system action; no unresolved high-risk security finding; promotion thresholds finalized by Steve.

### Stage 2 - Private alpha (approximately 4-8 additional weeks)

- Entry gate: legal/privacy review for external personal data, tenant-isolation tests, consent language, retention/erasure controls, incident response, and source-policy review must pass before the first invited user supplies data
- Five to ten invited users after Steve approval
- Fellow MScFE graduates are one possible invited cohort, not the assumed or exclusive market
- Tenant isolation and permissions
- Application-controlled object storage as byte authority
- Optional Drive export/sync
- Retry, recovery, support, accessibility, and audit history
- Measured reliability, time savings, user retention, cost, and quality

**Gate:** numerical reliability, cost, time-saving, retention, and security thresholds approved in Stage 0 are met.

### Stage 3 - Beta hardening (approximately 8-16 additional weeks)

- Security and privacy review
- Backup and disaster-recovery evidence
- Source governance and change monitoring
- Support and abuse prevention
- Production hosting decision
- Pricing research and willingness-to-pay validation
- Optional billing only after an approved commercial decision

**Gate:** Steve approves beta launch from measured evidence. A calendar estimate never substitutes for the gate.

### Cutover rule

AJAS Personal first runs beside the attended pilot. Steve alone authorizes any pilot reduction or retirement after shadow evidence, rollback readiness, and explicit thresholds. Failure returns AJAS Personal to the prior safe stage without changing Track A.

---

## 12. Governance carried forward

### 12.1 Product governance principles

- Approved-facts-only generation with claim provenance
- Deterministic validation before READY
- Readback for every stored artifact
- Stable IDs and idempotent updates
- Versioned corrections and non-overwriting publication
- Soft deletion plus verified user-requested erasure where applicable
- Explicit consent and authorization records
- One authoritative state store and one authoritative byte store per stage
- Staged environments and promotion gates
- Visible failures, retries, repairs, and audit history
- Steve's final authority during AJAS Personal

### 12.2 Boundaries not carried into product architecture

- No mandatory second-AI review for every application packet
- No Apps Script reconciler as a default product component
- No dual-chat-agent inbox protocol as normal product architecture
- No blanket immutability that prevents authorized correction or erasure
- No assumption that a connected tool authorizes every consequential action

### 12.3 Completed handoff maker-checker record

The finalization sequence completed as follows:

1. GPT assembled `AJAS_Handoff_FINAL_CANDIDATE_v0.9.md` from the reconciled source set.
2. Claude performed the requested factual and contradiction audit and returned five numbered, non-blocking corrections in `AJAS_v0.9_Claude_Audit__20260829.md`.
3. Steve directed GPT to issue the complete final handoff and begin the new-project transition, adopting the seven recommended startup rulings in §14.1.
4. GPT applied the audit corrections, expanded the production build contracts, generated the matching Markdown, DOCX, and PDF, and performed semantic-parity, structure, text-extraction, and visual-integrity checks.
5. Claude may perform an optional independent parity check later. That optional check does not block use of the canonical Markdown in the new project.

Delivery to Steve and later filing in `00_Governance` are separate events. This document does not claim a Google Drive governance upload. If Steve later authorizes filing, the uploader must place all three versioned files, verify content readback, and record checksums and uploader identity. No pre-final source is overwritten.

---

## 13. Thirteen technical answers

Every provider, plan, price, quota, model, endpoint, OAuth behavior, and runtime answer is **VERIFY_AT_IMPLEMENTATION** unless a dated verification record appears.

1. **Local versus cloud development:** use VS Code, Git, and focused local tests; use managed cloud services for database and preview after Stage-0 approval. A cloud development environment remains an optional fallback.
2. **Azure credits:** reserve Azure evaluation for later model, secret, monitoring, storage, or worker needs. Credits do not require an Azure-first architecture.
3. **Database:** use managed PostgreSQL. Neon, Supabase, or another suitable provider may be evaluated through security, cost, backup, region, and operational gates. Provider portability does not eliminate migration work.
4. **Models:** use a provider-neutral interface and task-specific model selection based on measured extraction accuracy, writing quality, latency, privacy, and cost. Durable architecture does not name a current model as permanent.
5. **LangGraph versus CrewAI:** neither is required for Stage 1. Explicit typed workflows and database state are easier to test. LangGraph or another graph framework requires demonstrated benefit before adoption.
6. **MCP:** not required inside the first web application. A later MCP interface may be evaluated only when several external AI hosts need the same controlled AJAS actions.
7. **A2A:** not required. A single service and queue do not need protocol-level agent federation.
8. **Cost per application:** `$0.10-$0.50` remains a **PLANNING_HYPOTHESIS**, not an established unit cost. Record model tokens, search/API expense, document work, storage, retries, support, and shared infrastructure per application.
9. **Scaling:** likely pressure points include source rate limits, document/AI workers, storage operations, retries, and support. Load tests and actual usage decide worker, cache, and database changes; round-number user claims are not architecture facts.
10. **Free-tier abuse:** external access would require verified identity, bounded quotas, rate limits, abuse monitoring, and cost controls. No free commercial tier is designed during Stage 1.
11. **OAuth scopes:** request only capabilities required for a defined function. `drive.file` may be a candidate for app-created or user-selected file workflows, but exact behavior, user interaction, file visibility, refresh-token handling, and revocation must be verified against current documentation. Email requires a separate optional consent.
12. **Database versus file storage:** PostgreSQL owns structured truth. Stage-1 AJAS Personal Drive owns packet bytes. Stage-2 object storage owns packet bytes, with Drive optional export/sync. Raw uploads follow explicit minimization and retention rules rather than a blanket “parse and discard” claim.
13. **Minimum audit event:** event ID, timestamp, user, actor and version, action, target, prior/new state when relevant, authorization or consent reference, evidence reference, idempotency key, outcome, failure code, and correlation ID. Audit storage must support export, investigation, correction linkage, retention, and access control.

---

## 14. Steve ruling record and Stage-0 decision register

Steve's 2026-08-29 directive to return the final handoff and begin the new ChatGPT Project adopts the seven startup rulings below. The adoption authorizes Stage 0 only and does not resolve the separately deferred decisions in §14.2.

### 14.1 Adopted startup rulings

| # | Adopted ruling | Status |
|---:|---|---|
| 1 | Stage 1 serves Steve only; external users wait for later gates. | `ADOPTED 2026-08-29` |
| 2 | Autonomous authority stops at `READY_FOR_REVIEW`; all employer-system interaction remains human-only. | `ADOPTED 2026-08-29` |
| 3 | Stage 1 uses PostgreSQL structured truth plus a separate AJAS Personal Drive byte store; Stage 2 uses object storage as byte authority with optional Drive export/sync. | `ADOPTED 2026-08-29` |
| 4 | Vercel is a provisional preview/staging candidate only after Stage-0 verification; production hosting remains open. | `ADOPTED 2026-08-29` |
| 5 | The merge used GPT as maker, Claude as contradiction checker, Steve as final decision authority, and GPT as final renderer and format-QA owner. Later Drive governance filing requires separate upload evidence. | `ADOPTED 2026-08-29` |
| 6 | `AJAS` remains the internal working name; public brand and domain wait for availability and conflict review. | `ADOPTED 2026-08-29` |
| 7 | Only approved, versioned facts with provenance receive automatic reuse; voluntary or sensitive answers remain manual; only verified permitted sources are enabled. | `ADOPTED 2026-08-29` |

### 14.2 Deferred Stage-0 decision register

| Decision | Owner | Must be resolved before | Required evidence |
|---|---|---|---|
| Exact retention and erasure periods by data class | Steve with security/privacy review | Any real AJAS Personal account or Steve personal data entering Stage 1 | Data inventory, purpose, provider terms, storage authorization, backup behavior, legal/privacy review |
| Monthly development and service spending cap | Steve | Any paid service or API | Provider pricing, usage estimate, alert and hard-stop design |
| Weekly development capacity | Steve | Roadmap commitment | Available hours and sustainable review cadence |
| Initial 25-50-employer/source allowlist | Steve with source-policy review | Automated source polling | Current documentation, terms, rate limits, target-role relevance |
| Standing preparation authority versus per-role selection | Steve | Unattended Stage-1 preparation | Risk analysis, notification and stop controls, acceptance criteria |
| Private-alpha cohort and invitation timing | Steve | Stage 2 | Stage-1 evidence, support capacity, privacy/security readiness |
| Numerical Stage-1, alpha, beta, and cutover gates | Steve with project review | Promotion from each stage | Reliability, readback, truthfulness, security, cost, time-saving, retention data |
| Public product name and domain | Steve | External beta or marketing | Name/domain availability and conflict review |
| Production hosting topology | Steve with technical review | Beta production deployment | Workload, region, security, reliability, and total-cost evidence |
| Optional Gmail or other email integration | Steve with privacy/security review | Any product email access | Provider, account, scope, consent, retention, revocation, and data-flow design |

### 14.3 Scope of adoption

Public branding, exact retention and erasure periods, monthly spending cap, weekly development capacity, final source allowlist, standing unattended authority, production hosting, optional email integration, and numerical promotion thresholds remain gated Stage-0 decisions. No adoption in this section authorizes a change to the live attended pilot.

---

## 15. Controlling new-project directive

The new project follows this controlling directive; section 24 provides the exact setup instructions and sequenced prompts:

> Build a future AJAS Personal product using `AJAS_Handoff_FINAL_v1.0.md` as the controlling briefing. Treat the 77-page architecture proposal and all earlier handoffs as preserved research and provenance, not controlling specifications. Maintain three isolated tracks: the active attended pilot, the paused legacy machine track, and the new AJAS Personal product. Do not read from or mutate the active pilot at runtime. Begin with Stage 0A: requirements, controlled state vocabulary, source-of-truth rules, artifact authority, data-flow map, threat model, source/terms register, authorization model, and acceptance tests. Do not scaffold production code until Stage 0A passes its gate. Autonomous product authority ends at a verified `READY_FOR_REVIEW` packet. Do not authenticate to employer systems, enter or upload employer-form data, make attestations, contact employers, or submit applications. Do not implement LinkedIn or Indeed automation, broad scraping, auto-submission, A2A, custom MCP infrastructure, CrewAI, billing, or a vector database without later evidence and explicit approval. Preserve claim provenance, named gaps, deterministic validation, one authoritative state store, one authoritative byte store, idempotency, readback, auditability, rollback, and Steve's decision authority.

---

## 16. Asset and artifact inventory

| Asset class | Track | Authority/mutability | Permitted product use |
|---|---|---|---|
| Signed governance and amendments | A/B historical governance | Versioned; no silent overwrite | Read during migration design; do not use as runtime state |
| `02_Evidence_Bank` facts and approved CVs | A canonical evidence | Protected source; versioned corrections only through authorized process | Import a controlled snapshot with provenance after Steve approval |
| `ATTENDED_PILOT` folders | A live artifacts | Existing files preserved; confirmations and authorized additions remain possible | Worked examples only; no Track-C runtime reads |
| Applications Log | A active state | Intentionally mutable through authorized idempotent updates | Historical schema/metric reference; no Track-C runtime dependency |
| `AJAS_Operations` and Technical Build Package v1.1 | B paused experiment | Separate approval and staged testing | Research input only unless Track B resumes |
| Architecture proposal | C research | Preserved source | Ideas subject to final corrections and Stage-0 gates |
| Source handoffs and merge memos | C provenance | Preserved unchanged | Historical traceability; not controlling after v1.0 issuance |
| `AJAS_Handoff_FINAL_v1.0` | C controlling briefing | Versioned governance artifact | First source and controlling product brief for the dedicated project |
| New AJAS Personal database | C operational state | Authorized, audited, backed up, correctable | Structured source of truth |
| New AJAS Personal Drive root | C Stage-1 bytes | Separate authorization; sole Stage-1 byte authority | Generated packet files only |
| Product object storage | C Stage-2+ bytes | Sole canonical byte authority after migration | Generated artifacts; Drive optional derivative export |

### 16.1 Publication controls

- Source documents remain unchanged.
- Candidate versions never overwrite final versions.
- Final Markdown, DOCX, and PDF receive matching version names.
- Semantic text, heading, list, table, and code-block parity is checked across formats.
- DOCX and PDF visual integrity is inspected page by page.
- If later filed to Drive, metadata and content readback must be verified; this handoff does not claim that filing occurred.
- An external publication record captures source documents, audit result, Steve directive date, renderer, checksums, and any later uploader/readback result. A document does not embed its own final byte checksum.

---

## 17. Production target and definition of done

### 17.1 Meaning of production-grade

Production-grade AJAS means a system that is deployable, observable, recoverable, auditable, source-compliant, privacy-preserving, cost-controlled, and safe at the human submission boundary. It does not mean maximum infrastructure, immediate worldwide launch, or a fleet of independently deployed autonomous agents.

Stage 1 is a single-user production deployment for Steve. The architecture is tenant-ready, but external-user processing remains disabled until Stage 2 gates pass. A deployment is not production-ready merely because a URL works.

### 17.2 Stage-1 product scope

In scope:

- approved applicant facts, evidence, preferences, and provenance;
- user-supplied official posting URLs and permitted automated discovery;
- source-policy enforcement, liveness, normalization, deduplication, and snapshots;
- explainable eligibility and fit with named gaps;
- approved-CV selection and truthful packet composition;
- deterministic document rendering, ATS-text checks, visual checks, hashing, storage, and readback;
- a controlled application state machine;
- user-facing READY instructions and official link;
- user-supplied submission receipts and confirmation filing;
- audit events, costs, failures, repairs, notifications, export, correction, and approved deletion behavior;
- development, test, preview, staging, shadow, and Steve-only production environments.

Out of scope for Stage 1:

- employer login, authenticated employer sessions, employer-form entry, file upload to an employer, attestations, employer communication, or submission;
- LinkedIn or Indeed automated search, fetch, parsing, scraping, session reuse, or application activity;
- CAPTCHA or bot-control bypass;
- broad web scraping or unreviewed source activation;
- multi-user tenancy in live use, billing, credits, enterprise features, SSO, mobile applications, or public marketing;
- model training on applicant data by default;
- general browser agents, self-modifying agents, runtime tool discovery, A2A, CrewAI, or custom MCP infrastructure;
- replacement, retirement, or runtime use of Track A or Track B.

### 17.3 Functional requirements

| ID | Requirement | Stage-1 acceptance evidence |
|---|---|---|
| `FR-001` | Manage approved facts as versioned records with provenance, allowed uses, sensitivity, effective dates, and correction history. | Schema tests and an evidence-to-claim trace for every generated material claim. |
| `FR-002` | Enforce a versioned source-policy registry before every network operation. | Disabled, expired, redirected, and unregistered-source tests fail closed. |
| `FR-003` | Discover or accept job URLs only from enabled sources; retain the official source identity. | Source-adapter contract tests and recorded policy decision. |
| `FR-004` | Normalize a posting without losing raw-field provenance, retrieval time, parser version, URL, and content hash. | Fixture comparison and immutable posting snapshot. |
| `FR-005` | Check liveness at intake and immediately before READY. | Dated liveness evidence within the Stage-0 freshness target. |
| `FR-006` | Deduplicate exact ATS IDs and canonical URLs and surface ambiguous reposts for review. | Database uniqueness, concurrency, and repost tests. |
| `FR-007` | Show every material requirement, matched approved evidence, unresolved item, named gap, disqualifier, and user override. | Golden fit-explanation fixtures with no hidden suppression score. |
| `FR-008` | Generate packet sources from only approved facts and selected evidence snapshot. | Unsupported-claim tests block publication. |
| `FR-009` | Render the required artifacts with deterministic names, versions, templates, and manifests. | Golden file, text, page, and filename tests. |
| `FR-010` | Validate claims, ATS text, pages, visual integrity, links, hashes, storage, readback, and completeness before READY. | A signed validation manifest with every required gate passing. |
| `FR-011` | Advance application state only through authorized, idempotent transitions. | State-machine, replay, race, and invalid-transition tests. |
| `FR-012` | Stop autonomous authority at `READY_FOR_REVIEW` and show Steve the official link and precise human steps. | Negative end-to-end tests prove no employer-action capability exists. |
| `FR-013` | Record `SUBMITTED_BY_USER` from an authenticated user report and `SUBMISSION_CONFIRMED` only from acceptable receipt evidence. | Receipt-ingestion and ambiguous-evidence tests. |
| `FR-014` | Record every action, denial, model run, tool call, artifact, transition, repair, cost, and release with a correlation ID. | Audit reconstruction of an end-to-end fixture. |
| `FR-015` | Provide visible stop controls for a source, connector, model, workflow, and all preparation. | Kill-switch tests preserve state and prevent new side effects. |
| `FR-016` | Support authorized export, correction, retention, soft deletion, and verified erasure behavior. | Stage-0-approved lifecycle tests, including backups and legal holds. |

### 17.4 Hard safety and integrity requirements

These are release blockers, not aspirational SLOs:

| Dimension | Required condition |
|---|---|
| Employer authority | Zero automated employer login, form interaction, upload, communication, attestation, or submission. |
| Claim integrity | Every automatically reused material claim resolves to an approved fact and evidence version. |
| READY integrity | Every required artifact passes completeness, content, manifest, hash, storage readback, and final-liveness gates. |
| State integrity | Every accepted transition records actor, authority, prior/new state, evidence, correlation ID, and idempotency key. |
| Source governance | Every automated fetch uses an enabled and unexpired source-policy record. |
| Exact duplicate control | Exact canonical URL and ATS-ID duplicates are blocked or linked idempotently. |
| Environment isolation | No shared live database, storage root, OAuth client, queue namespace, signing key, or secret across environments. |
| Tenant isolation | Zero cross-user authorization failures before any external user receives access. |
| Release security | No unresolved critical or high security finding at promotion. |
| Track isolation | No Track-C runtime dependency on or mutation of Track A or Track B. |

### 17.5 Operational targets to ratify in Stage 0

Stage 0 must set measured targets for availability and error budget; scheduled-run completion; queue wait; packet p50/p95 latency; liveness freshness; source-fetch success and throttling; repair and dead-letter backlog; artifact-generation latency; backup recovery point objective; recovery time objective; cost per completed packet; monthly hard stop; incident notification; accessibility; and support response. Until approved, every number is `TO_BE_RATIFIED_STAGE_0`.

---

## 18. Deployable reference architecture

### 18.1 Stage-1 topology

AJAS Stage 1 is a modular monolith plus one durable worker:

1. **Web application:** Next.js and TypeScript provide the user interface and authenticated server endpoints.
2. **Domain core:** typed modules enforce commands, policy, state transitions, evidence, and artifact rules.
3. **Worker:** a separate Node.js/TypeScript process handles source retrieval, model calls, document rendering, storage, validation, and bounded retries.
4. **PostgreSQL:** authoritative structured state, transitions, policy versions, audit metadata, costs, job leases, and artifact metadata.
5. **Durable jobs:** one PostgreSQL-backed or managed queue selected by ADR; at-least-once delivery is paired with idempotent consumers.
6. **Stage-1 byte store:** a separately authorized AJAS Personal Google Drive root behind a typed storage adapter.
7. **Source adapters:** source-specific, capability-scoped readers governed by the source-policy registry.
8. **AI gateway:** a provider-neutral, schema-constrained interface with no ambient tools or credentials.
9. **Document toolchain:** deterministic templates, rendering, PDF merge, ATS extraction, page rendering, hashing, and readback.
10. **Observability:** privacy-minimized logs, metrics, traces, error reporting, cost events, alerts, and audit export.

Each named agent in section 19 is initially a bounded module in this topology. A module becomes a separate service only when measured scaling, isolation, security, or team-ownership evidence justifies extraction.

### 18.2 End-to-end request flow

1. Steve authenticates to AJAS and submits a command or approves a bounded preparation policy.
2. The web/API layer validates identity, ownership, CSRF protection, input schema, and rate limit.
3. The Orchestrator checks policy and current state, records the command, and commits a durable job plus outbox event transactionally.
4. A worker claims the job with a lease, correlation ID, idempotency key, timeout, and retry policy.
5. Capability-scoped modules perform source, evidence, model, document, storage, and validation work.
6. PostgreSQL commits structured results and transition history; the byte store accepts versioned artifacts.
7. The validator reads stored bytes back, compares hashes and manifests, rechecks liveness, and proposes READY only after every gate passes.
8. The user interface publishes the packet, exact failure or repair reason, official application link, and numbered instructions.
9. Steve performs the employer-system activity outside AJAS.
10. AJAS processes Steve's later report or receipt and records the appropriate post-submission state.

### 18.3 Reliability mechanics

- transactional state changes and an outbox for state-dependent notifications;
- at-least-once jobs with idempotent consumers and optimistic concurrency;
- per-source concurrency, rate, response-size, timeout, and cache limits;
- bounded exponential backoff with jitter and a visible dead-letter path;
- one durable repair request per idempotency key;
- source, connector, model, workflow, and global preparation kill switches;
- temporary rendering followed by hash/readback validation and atomic manifest publication;
- immutable posting snapshots and artifact versions; corrections create new versions;
- expand-migrate-contract database changes and reviewed forward repair rather than blind destructive rollback;
- all workflow records, artifacts, logs, costs, and alerts linked by one correlation ID.

### 18.4 Environment boundaries

| Environment | Data rule | Purpose | Promotion authority |
|---|---|---|---|
| Local | Synthetic fixtures by default | Development and focused tests | Developer within approved Stage-0 scope |
| CI/Test | Ephemeral synthetic data | Automated verification | CI policy |
| Preview | Synthetic or explicitly sanitized data only | Pull-request review | CI plus reviewer |
| Staging | Separate credentials, database, queue, and storage; sanitized data until privacy gates pass | Integration, migration, release, restore, and rollback rehearsal | Authorized maintainer |
| Shadow | Approved sanitized snapshots; never Track-A runtime reads or writes | Compare behavior with known examples | Steve |
| Production Stage 1 | Steve-only AJAS Personal data and separate storage | Real single-user operation | Steve after Stage-1 gate |
| Production Stage 2+ | Tenant-isolated real user data after external-user gates | Private alpha and later product | Formal release approver |

Configuration is typed and validated at startup. Secrets never enter source control, prompts, generated artifacts, or logs. Each environment uses separate credentials and infrastructure boundaries.

### 18.5 Technology decisions and portability

- Select current supported stable Node.js, TypeScript, Next.js, package-manager, ORM, and database versions in Stage 0B; record them in ADRs, lockfiles, and the release manifest.
- Use a private GitHub repository and protected `main` branch.
- Use managed PostgreSQL after provider review. A PostgreSQL-backed durable queue is the preferred Stage-1 simplification; exact provider and library require an ADR.
- Use Vercel only as the provisional preview/staging candidate after current plan, privacy, runtime, and cost verification.
- Keep the worker deployable to a container-capable platform so document binaries and native inspection tools do not depend on short serverless limits.
- Keep source, AI, storage, queue, identity, notification, and observability providers behind typed ports.
- Treat Azure as a later deployment candidate, not a requirement. Azure credits and resume value do not override measured fit.

---

## 19. Logical AJAS agents and control services

### 19.1 Operating rule

Agent names describe bounded logical responsibilities. No natural-language A2A messaging, runtime tool discovery, self-modification, self-created credentials, or agent-selected expansion of authority is permitted. Generative models never receive direct network, database, Drive, email, or browser access. A model returns an untrusted, schema-validated proposal; deterministic code authorizes and executes every tool call and state change.

### 19.2 Agent and service catalog

| ID and module | Purpose and principal input/output | Allowed capabilities | Hard stops |
|---|---|---|---|
| `C1 Workflow Orchestrator` | Input: user command, policy, application state. Output: versioned run plan or typed failure. | State repository, policy gate, queue, clock, idempotency. | Cannot fetch sources, invent scope, bypass locks, or cross the state machine. |
| `C2 Source Policy Gate` | Input: source, URL, operation, registry version. Output: `ALLOW`, `DENY`, or `REVIEW_REQUIRED`. | Source registry, URL/security validator, kill switch. | Fails closed on missing, expired, redirected, or contradictory policy. |
| `A1 Job Scout` | Input: approved search policy or user URL. Output: candidate official posting references. | Enabled public-source adapters only. | No LinkedIn/Indeed fetch, login, CAPTCHA bypass, employer form, or general browser tool. |
| `A2 Posting Verifier` | Input: authorized response. Output: normalized posting, snapshot, canonical ID, liveness, confidence. | Safe fetcher, parser, canonicalizer, hash/snapshot. | Treats content as untrusted; cannot invent missing fields or follow an unapproved redirect. |
| `C3 Duplicate Resolver` | Input: normalized identity. Output: new record or duplicate/repost relationship. | Database uniqueness, canonical URL, conservative matcher. | Ambiguous matches require review; no silent merge. |
| `A3 Eligibility and Fit Analyst` | Input: requirements, preferences, facts. Output: requirement matrix, matches, gaps, disqualifiers, ambiguity. | Rules engine and structured AI gateway. | No protected-trait use, hidden score suppression, or unsupported qualification. |
| `A4 Evidence and Truth Guard` | Input: proposed claims and evidence snapshot. Output: approved claim map or blocking findings. | Approved-facts repository and provenance validator. | Unsupported claims fail closed; sensitive answers remain manual. |
| `A5 Packet Composer` | Input: selected posting, claim map, CV registry, templates. Output: structured packet sources. | Template engine and constrained drafting gateway. | No invented metrics, technologies, dates, credentials, or removed material gaps. |
| `A6 Artifact Renderer` | Input: validated sources and manifest request. Output: versioned files, hashes, page counts. | DOCX/PDF renderer, PDF merger, filename and temporary-file services. | No silent overwrite or substantive rewrite during rendering. |
| `A7 Quality Gatekeeper` | Input: files, manifest, claims, link. Output: PASS or exact repair findings. | ATS extraction, page rendering, visual checks, liveness, storage readback. | Cannot promote incomplete, inaccessible, stale, or unsupported work. |
| `C4 Application State Service` | Input: authorized transition and evidence. Output: transactional state/history/outbox. | PostgreSQL, transition policy, audit. | User report alone cannot create receipt-confirmed state; history is not erased. |
| `A8 Receipt and Confirmation Assistant` | Input: user report or uploaded receipt. Output: proposed confirmation facts and evidence reference. | Safe file intake, malware scan, OCR/extractor, evidence store. | Ambiguity requires user confirmation; no inference from silence. |
| `A9 User Handoff and Notification` | Input: state/outbox event. Output: deduplicated notice to the AJAS user. | In-product notification and later separately approved user email. | No employer destination or employer communication capability. |
| `A10 Optional Response Monitor` | Input: separately consented mailbox scope and known applications. Output: candidate response match. | Narrow read-only inbox adapter. | Disabled by default; no send, delete, archive, label, mark-read, or broad mailbox mining. |
| `C5 Repair and Retry Controller` | Input: typed failure, attempts, policy, current state. Output: bounded retry, repair, dead letter, or user action. | Queue, backoff, repair store, alerting. | No infinite retry, scope expansion, destructive recovery, or success fabrication. |
| `C6 Audit, Cost, and Observability` | Input: every command, tool call, model run, transition, and artifact. Output: correlated, redacted evidence. | Audit sink, metrics, traces, redaction, cost meter. | No secrets, hidden chain-of-thought, or unnecessary sensitive data in telemetry. |

### 19.3 Universal module contract

Every module defines a semantic version, owner, JSON-schema input and output, preconditions, required authorization, allowed tools, data classifications, side effects, idempotency-key construction, timeout, retry and exhaustion behavior, deterministic validators, correlation and audit fields, error taxonomy, fixtures, repair behavior, and rollback behavior.

Only A2, A3, A5, and A8 require plausible model-assisted steps. The absence of employer-action tools is an architectural control and must pass negative end-to-end tests.

---

## 20. Tool contracts and source-access policy

### 20.1 Capability-scoped tool ports

| Tool port | Required contract |
|---|---|
| `SourcePolicyRegistry` | Versioned operations, documentation and terms dates, cache/retention, attribution, limits, owner, expiry, environment, and kill switch. |
| `SafeHttpClient` | HTTPS only; host and redirect allowlist; DNS/IP SSRF protection; timeout; response-size and content-type limits; rate limit; bounded retry; no credential forwarding. |
| `SourceAdapter` | `discover`, `fetchPosting`, `checkLiveness`, and `canonicalize`; each call requires a current policy decision and returns evidence. |
| `ApprovedFactsRepository` | Versioned facts, provenance, allowed uses, sensitivity, correction history, and effective dates. |
| `RulesEngine` | Explicit eligibility, location, authorization, compensation, level, and preference rules with human-readable reasons. |
| `StructuredAIGateway` | Provider-neutral, schema-constrained output; minimum necessary data; prompt/model version; privacy setting; cost limit; timeout; no model tools. |
| `DocumentRenderer` | Versioned templates, reproducible output, font policy, page and filename rules, PDF merge, and deterministic metadata. |
| `ArtifactInspector` | Text extraction, ATS checks, page rendering, manifest comparison, link check, hash, and review hooks. |
| `ArtifactStore` | Capability-scoped create/version/read/readback/hash within the authorized root; no silent overwrite; Stage-2 object-store implementation behind the same port. |
| `StateRepository` | Transactional transitions, optimistic concurrency, uniqueness, immutable history, and outbox. |
| `JobQueue` | Leases, idempotency, retry count, backoff, dead-letter behavior, priority limits, and trace correlation. |
| `ReceiptIngestor` | Type and size validation, malware scan, decompression protection, OCR/extraction, and immutable evidence reference. |
| `ConnectorAuthorizationStore` | Encrypted tokens, scopes, expiry, revocation, environment isolation, and no model/log exposure. |
| `AuditSink` | Append-oriented events with actor, authority, versions, reasons, evidence, outcome, redaction, retention, and export. |
| `Clock` | UTC storage and `America/Los_Angeles` presentation for Steve; no implicit local-time assumption. |
| `UserNotifier` | Preference-controlled, deduplicated notices to AJAS users only; no employer-recipient API. |

### 20.2 Source-policy states

Source records use `ENABLED`, `MANUAL_ONLY`, `UNDER_REVIEW`, `DISABLED`, or `EXPIRED`. Only `ENABLED` permits a network request.

| Source class | Stage-1 policy | Permitted behavior | Prohibited behavior |
|---|---|---|---|
| User-provided official employer/ATS URL | Eligible after URL and source-policy validation | Approved GET/HEAD and liveness check | A pasted URL never bypasses policy. |
| Greenhouse and Lever public job interfaces | Board-by-board enablement after current review | Documented job listing/detail reads | No application POST, login, or blanket provider-wide approval. |
| Ashby or another ATS | `UNDER_REVIEW` until its own gate passes | None until enabled | No inference from another ATS policy. |
| CalCareers, Grainger, Gap Inc., and other official careers pages | Employer/interface-specific review | Approved public retrieval and liveness | No login, application workflow, CAPTCHA bypass, or unsupported browser workaround. |
| Licensed search provider | Optional after contract/privacy review | Discover candidate official URLs within contract | No scraping search-result pages or treating cache as current liveness proof. |
| LinkedIn and Indeed | `MANUAL_ONLY` | Record a user-supplied reference and seek an official URL | No automated fetch, parsing, scraping, login, cookies, circumvention, or applying. |
| User-pasted job text | Unverified lead | Store with user provenance and locate an official source | Cannot be labeled live or reach READY without permitted official evidence. |
| Gmail | Separate optional connector, not a job source | Narrow consented read-only match to known applications | No send, delete, archive, label, mark-read, or broad mailbox mining. |
| Google Drive | Artifact storage | Operations inside the separately authorized AJAS Personal root | No discovery role and no Track-A runtime access. |

Public availability is not authorization. Robots rules are respected but do not replace documentation, terms, privacy, copyright, or contract review. Redirects are revalidated. No access-control or bot-protection bypass is permitted. Posting content is untrusted data and never instruction text. Terms, schema, redirect, parser, or authentication changes fail closed and trigger review.

### 20.3 Critical failure semantics

- `429`, timeout, and transient `5xx`: bounded backoff with jitter, then visible dead letter.
- Expired or missing source policy: fail closed; do not retry the network call.
- Parser drift: quarantine the response, preserve permitted evidence, alert the owner, and run adapter fixtures.
- Low extraction confidence: require review; do not invent or silently omit a material requirement.
- Unsupported claim: reject the claim or packet.
- AI schema failure: one bounded structured retry if policy permits, then typed failure.
- Database/storage partial success: remain `PREPARING`; use outbox and idempotent repair.
- Hash mismatch: invalidate that artifact version, preserve evidence, and create a new version.
- Posting closes before submission: enter `CLOSED_BEFORE_SUBMIT` and do not direct the user to apply.
- Duplicate concurrent run: return the existing application/run through unique constraints and idempotency.
- Connector revocation: stop access immediately, preserve permitted audit history, and explain the blocked function.
- Ambiguous receipt or email match: require user confirmation.
- Model, prompt, template, or parser change: record a new version and pass regression evaluation before promotion.
- Cost ceiling reached: stop new paid work safely and preserve the last valid state.

---

## 21. Data, API, event, and artifact contracts

### 21.1 Structured authority

PostgreSQL owns structured truth. The Stage-1 AJAS Personal Drive root owns packet bytes. These are complementary authorities, not competing universal sources of truth. The database stores stable artifact IDs, versions, hashes, MIME types, storage references, and validation evidence; Drive stores the referenced bytes. Stage 2 changes byte authority only through a verified migration.

### 21.2 Core records and constraints

In addition to the entities in §8.5, Stage 0 specifies `SourceFetch`, `PostingSnapshot`, `Requirement`, `EvidenceMatch`, `PreparationRun`, `AgentRun`, `ToolCall`, `ModelRun`, `PromptVersion`, `ValidationResult`, `ArtifactManifest`, `PolicyVersion`, `Notification`, `ReceiptEvidence`, `ReleaseManifest`, and `IncidentRecord`.

Minimum constraints:

- all user-owned rows carry an owner ID from the first migration, even while Stage 1 has one user;
- exact posting identity uses a unique source/provider plus external posting ID where available;
- canonical URLs use normalized uniqueness with a reviewed repost relationship;
- one active application per user and canonical posting identity unless an explicit repost rule permits another;
- transitions append; correction or reversal never erases prior transition evidence;
- artifact versions are unique per application, kind, and version; approved bytes are not overwritten;
- approved facts and policies have effective versions; generated runs pin the exact snapshot used;
- idempotency keys are unique within an operation scope and return the existing result on replay;
- foreign keys and ownership checks prevent orphaned application, artifact, receipt, or audit data;
- indexes cover owner/state, source/external ID, canonical URL hash, scheduled jobs, dead letters, policy expiry, and audit correlation.

Retention class, encryption need, export behavior, erasure effect, and legal-hold effect are mandatory schema metadata or documented policy for every data class.

### 21.3 Command and event envelope

Every command, job, event, model run, and tool call carries:

- schema name and version;
- stable event or command ID;
- correlation and causation IDs;
- user, actor, actor version, and environment;
- target IDs and expected current version;
- authorization or consent reference;
- idempotency key;
- UTC creation and expiry times;
- redaction classification;
- payload hash where useful;
- retry policy and attempt for background work.

Consumers reject unknown major schema versions, stale expected versions, expired authorization, and replay with conflicting payload. At-least-once delivery cannot create duplicate artifacts, transitions, notifications, folders, or receipts.

### 21.4 Artifact manifest

Each packet has one versioned manifest containing application ID, posting-snapshot ID/hash, evidence-snapshot version, prompt/model/parser/validator/template versions, expected filenames, artifact kinds, MIME types, byte sizes, page counts, SHA-256 hashes, ATS-text results, visual-check results, storage references, readback hashes, liveness evidence, validation time, validator version, and final PASS/FAIL. `UPLOAD_REPAIR_REQUIRED` is a versioned operational flag on `PREPARING`, not a lifecycle state.

### 21.5 API and error contract

Server endpoints use authenticated ownership checks, explicit request/response schemas, bounded payloads, CSRF protection for browser mutations, rate limits, and correlation IDs. Errors are typed and safe for display:

- `VALIDATION_ERROR`
- `AUTHENTICATION_REQUIRED`
- `AUTHORIZATION_DENIED`
- `STATE_CONFLICT`
- `DUPLICATE`
- `SOURCE_POLICY_DENIED`
- `SOURCE_INDETERMINATE`
- `EVIDENCE_GAP`
- `ARTIFACT_INVALID`
- `CONNECTOR_REVOKED`
- `RETRYABLE_PROVIDER_ERROR`
- `COST_LIMIT_REACHED`
- `NEEDS_USER`

Errors never expose secrets, raw tokens, internal stack traces, hidden model reasoning, or unnecessary personal data. A server-reported success must correspond to a committed and, where required, read-back state.

---

## 22. Security, privacy, observability, and operations

### 22.1 Security and privacy baseline

- standards-based authentication; privileged MFA before external users;
- deny-by-default authorization and owner/tenant checks on every personal-data query;
- secure, short-lived sessions, CSRF protection, controlled revocation, and audit of privileged action;
- secret manager for production credentials and connector tokens;
- transport encryption and provider-managed encryption at rest, with stronger protection where the threat model requires it;
- least-privilege OAuth, separate consent per connector, visible revocation, and tested revoked-token behavior;
- egress allowlist where supported, plus SSRF, XSS, injection, path traversal, malicious-file, decompression-bomb, and oversized-file defenses;
- job text, email, documents, and uploads treated as untrusted data, never as system instructions;
- minimum-necessary model inputs and no hidden chain-of-thought retention;
- dependency lockfiles, secret scanning, static analysis, software-composition analysis, update policy, and release SBOM;
- privacy-minimized and redacted logs; never log credentials, tokens, sensitive answers, or unnecessary applicant content;
- provider privacy, training, retention, region, and subprocessor settings verified before real-data use;
- data inventory, purpose, retention, export, correction, deletion, backup, legal hold, and breach workflow approved before real personal data enters Stage 1;
- no external compliance, accessibility, fairness, encryption, or legal claim without implementation evidence and qualified review.

### 22.2 Prompt-injection containment

Source content and uploaded material are data. The system separates instructions from retrieved content, strips active markup where appropriate, enforces output schemas, refuses tool requests embedded in content, supplies no secrets or ambient credentials to models, and runs deterministic policy and evidence gates after every model call. Adversarial fixtures must prove that a posting cannot activate tools, change source policy, reveal secrets, alter states, or cross the human boundary.

### 22.3 Observability

Privacy-minimized telemetry covers source queries and results; liveness and duplicate decisions; queue age, leases, attempts, retries, and dead letters; model latency, schema failures, and cost; provenance failures; document rendering, ATS extraction, visual checks, hashes, upload, and readback; transition approval or denial; connector authorization and revocation; notifications; retention and erasure jobs; backups and restores; and releases.

Required dashboards cover workflow completion, failure and repair backlog, source health, artifact integrity, spend, security events, and promotion evidence. Alerts cover unauthorized-transition attempts, failed READY validation, policy expiry, repeated source throttling, connector revocation, cost-cap approach, audit-write failure, backup failure, restore-test failure, and retention/erasure failure.

### 22.4 Backup, recovery, and incidents

Stage 0 ratifies RPO and RTO. Backups are encrypted, monitored, access-controlled, and restored on a schedule. Restore tests must reconcile application records, transitions, policies, artifact metadata, and byte references without creating a false READY or confirmed state.

Incident response must support source, connector, model, workflow, and global kill switches; read-only/maintenance mode; evidence preservation; credential revocation; prior-build restoration; forward database repair; in-flight reconciliation; post-restore validation; root-cause record; and controlled resume. A provider outage or source change fails visibly. AJAS never compensates by weakening validation, changing to an unapproved source, inventing content, or crossing the employer boundary.

---

## 23. Testing, release, rollback, and local repository

### 23.1 Test strategy

The release test set includes:

- unit tests for state transitions, policy, constraints, provenance, redaction, filenames, and manifests;
- property tests for idempotency, replay, race handling, duplicates, and prohibited transitions;
- source-adapter contract tests against versioned fixtures, redirects, closure pages, missing fields, malformed content, and schema drift;
- structured-model evaluations with unsupported-claim traps, ambiguity, named gaps, adversarial instructions, and schema failure;
- prompt-injection tests proving retrieved content has no tool or policy authority;
- golden document tests for Markdown/PDF text, page count, fonts, links, dates, approved CV identity, form-specific upload instructions, and visual layout;
- storage tests for write, readback, hash mismatch, partial upload, repair, revocation, and idempotent versioning;
- database migration tests against production-like sanitized snapshots;
- authorization and tenant-isolation tests before every external-user release;
- common web and file-processing security tests;
- automated accessibility checks plus manual keyboard and screen-reader review before beta;
- queue timeout, worker crash, retry, dead-letter, provider outage, and cost-stop tests;
- backup restoration and audit-reconstruction exercises;
- synthetic end-to-end flow from permitted fixture to `READY_FOR_REVIEW`;
- negative end-to-end tests proving there is no employer login, form, upload, message, attestation, or submission capability;
- shadow comparisons using approved sanitized examples, never Track-A runtime access;
- bounded performance, capacity, and cost tests before each scaling claim.

### 23.2 CI/CD and release gates

A protected pull request runs formatting, linting, type checking, schema generation checks, unit/property/contract/integration tests, migration safety, secret scanning, dependency analysis, static analysis, SBOM generation, production build, document golden tests, and the synthetic human-boundary test. Preview uses no real data.

Promotion then requires reviewer approval; staging deploy; migration, restore, and rollback rehearsal; smoke tests; manual production approval; and monitored progressive release. A release manifest records Git commit, build, application and schema versions, migration checksums, prompt/model configuration, parsers, validators, templates, source-policy registry, dependencies/SBOM, test and security results, approver, deployment, and rollback references.

Release is blocked by any failed required test; high or critical unresolved security finding; unreviewed destructive migration; expired source policy; missing backup or failed restore evidence; unavailable audit pipeline; human-boundary regression; artifact-integrity regression; missing rollback; unapproved real-data use; or Track-A/B dependency.

### 23.3 Rollback procedure

1. Activate the narrowest effective kill switch and stop new job claims.
2. Preserve queues, correlation IDs, logs, audits, artifacts, and database state.
3. Enter read-only or maintenance mode for the affected capability.
4. Revoke exposed credentials or connector tokens when relevant.
5. Restore the prior immutable application build.
6. Use reviewed forward migration for schema repair; do not blindly reverse destructive changes.
7. Restore from the latest verified backup only when integrity analysis requires it.
8. Reconcile in-flight work into explicit retry, repair, or user-action status while preserving the last valid business state.
9. Re-run liveness, provenance, artifact, readback, and transition gates.
10. Record cause, impact, decisions, correction, and prevention; resume gradually after authorized approval.

Rollback never manufactures success, erases evidence, or advances an application state.

### 23.4 Canonical Windows location

The local project root is:

```text
C:\Users\steve\Documents\02_CODING\AJAS
```

Keep the three final files at that root beside the existing `folder_structure.txt`. The existing `archive` is the preservation location for prior handoffs. Do not overwrite, delete, or silently rename those historical files.

Folders to create now:

```text
AJAS\
|-- AJAS_Handoff_FINAL_v1.0.md
|-- AJAS_Handoff_FINAL_v1.0.docx
|-- AJAS_Handoff_FINAL_v1.0.pdf
|-- folder_structure.txt
|-- archive\
`-- docs\
    |-- governance\
    |-- product\
    |-- architecture\
    |-- decisions\
    |-- security\
    |-- sources\
    |-- data\
    |-- testing\
    `-- runbooks\
```

Safe PowerShell creates only missing directories:

```powershell
$ajasRoot = 'C:\Users\steve\Documents\02_CODING\AJAS'

if (-not (Test-Path -LiteralPath $ajasRoot -PathType Container)) {
    throw "AJAS root folder was not found: $ajasRoot"
}

$foldersNow = @(
    'docs\governance',
    'docs\product',
    'docs\architecture',
    'docs\decisions',
    'docs\security',
    'docs\sources',
    'docs\data',
    'docs\testing',
    'docs\runbooks'
)

foreach ($relativePath in $foldersNow) {
    $fullPath = Join-Path $ajasRoot $relativePath
    if (-not (Test-Path -LiteralPath $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath | Out-Null
    }
}

Get-ChildItem -LiteralPath $ajasRoot
```

The approved Stage-0B scaffold creates these later:

```text
AJAS\
|-- apps\
|   |-- web\
|   `-- worker\
|-- packages\
|   |-- core\
|   |-- database\
|   |-- agents\
|   |-- tools\
|   |-- documents\
|   |-- observability\
|   |-- config\
|   `-- ui\
|-- tests\
|   |-- unit\
|   |-- integration\
|   |-- contract\
|   |-- e2e\
|   |-- security\
|   |-- fixtures\
|   `-- golden\
|-- scripts\
|-- infra\
|   |-- local\
|   |-- preview\
|   |-- staging\
|   `-- production\
|-- .github\workflows\
`-- tmp\
```

Stage 0B also creates `README.md`, `AGENTS.md`, `.gitignore`, `.editorconfig`, and `.env.example`. The minimum `.gitignore` is:

```gitignore
.env
.env.*
!.env.example
node_modules/
.next/
dist/
coverage/
tmp/
*.log
Thumbs.db
.DS_Store
```

Initialize Git only after confirming the final files and folder tree:

```powershell
$ajasRoot = 'C:\Users\steve\Documents\02_CODING\AJAS'
Set-Location -LiteralPath $ajasRoot
git --version

if (-not (Test-Path -LiteralPath (Join-Path $ajasRoot '.git'))) {
    git init -b main
} else {
    git status --short --branch
}
```

Do not add a remote or push until Steve confirms that no secret or personal-data file is staged. Use explicit paths rather than `git add .` for the first commit.

### 23.5 Archive policy

The seven existing pre-final Markdown files already sit in `archive`; leave them unchanged. Keep the three v1.0 files at the root. When a future handoff supersedes v1.0, first copy all three v1.0 formats into a new dated folder such as `archive\handoffs\2026-09-15__v1.0_superseded`, verify copied hashes, and only then publish the next version at the root. Never use an overwrite flag during archival.

---

## 24. New ChatGPT Project bootstrap

### 24.1 File to upload

Upload **`AJAS_Handoff_FINAL_v1.0.md` first and treat it as canonical**. Markdown is the most reliable controlling source for the new project. The DOCX and PDF are matching human-readable mirrors and may be uploaded as references, but they never override the Markdown.

OpenAI's dated Projects guidance confirms that a Project can hold uploaded sources and Project Instructions, and that Project Instructions override global custom instructions within that Project. Interface details and file limits can change, so verify the current [OpenAI Projects help](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt) during setup.

A standard ChatGPT Project does not by itself prove access to `C:\Users\steve\Documents\02_CODING\AJAS`. The new project must state whether direct filesystem access exists. If access does not exist, the project provides exact PowerShell commands or downloadable files and never claims that local work was performed.

### 24.2 Project Instructions

Put this text in the new project's Project Instructions:

```text
AJAS_Handoff_FINAL_v1.0.md is the controlling AJAS Track-C specification. Read it completely before planning, coding, installing dependencies, editing files, or proposing deployment. Preserve every binding human-control, truthfulness, privacy, source-policy, state-machine, audit, non-destructive, and Track-isolation constraint. Never automate employer submission, authenticate to or populate an employer system, scrape prohibited sources, invent applicant facts, expose secrets, or claim that an unverified action succeeded. Treat REPORTED and VERIFY_BEFORE_USE facts according to their labels. Use deterministic modules with explicit inputs, outputs, permissions, and tests. Preserve the running attended pilot and the paused machine track while AJAS Personal is built separately.

Work in small, reviewable stages. Lead with outcomes, list files changed, run relevant tests, and stop at explicit approval or safety gates. Do not overwrite the final handoff. If direct access to Steve's Windows filesystem is unavailable, say so and provide exact PowerShell commands or downloadable files; never claim that local files were created when they were not.
```

### 24.3 First six prompts

Send these prompts one at a time.

#### Prompt 1 - Establish the governing baseline

```text
Read AJAS_Handoff_FINAL_v1.0.md completely. Do not write code or change files yet. Confirm the exact filename and version, then return:

1. The binding AJAS purpose and human-submission boundary.
2. The controlling source-of-truth hierarchy.
3. The build stages and release gates.
4. The approved agent/module and tool boundaries.
5. Every unresolved item, VERIFY_BEFORE_USE fact, and Stage 0 decision.
6. Any contradiction or ambiguity that would block implementation.
7. The smallest safe first milestone.

Do not infer missing facts. Distinguish VERIFIED, REPORTED, ADOPTED, TO_BE_RATIFIED_STAGE_0, and deferred claims. End with HANDOFF_LOADED only if the entire document was read and understood.
```

#### Prompt 2 - Audit the Windows environment

```text
Prepare a read-only Windows PowerShell environment audit for C:\Users\steve\Documents\02_CODING\AJAS. Check Git, Node.js, package managers, Docker, available PostgreSQL tooling, PowerShell version, and the existing folder tree. Do not install software, initialize Git, move files, create files, or expose secrets. Give me one safe command block to run and wait for me to paste its output before recommending exact development-tool versions.
```

#### Prompt 3 - Complete Stage 0 specifications

```text
Using the handoff and verified environment results, prepare the Stage 0 specification plan. Define the proposed files, acceptance criteria, and review order for product requirements and non-goals; actor and authorization matrix; application state machine; data model and provenance; source-policy registry; privacy and threat model; audit, observability, backup, recovery, and retention; architecture decision records; and unresolved performance, availability, RPO, RTO, cost, and accessibility targets.

Do not implement application code yet. Identify each decision requiring Steve's approval and recommend a default with its tradeoff.
```

#### Prompt 4 - Bootstrap the repository safely

```text
After Stage 0A is approved, prepare the minimal AJAS repository scaffold inside C:\Users\steve\Documents\02_CODING\AJAS using only ratified stack decisions. Preserve the existing archive and all three final handoff files. Do not move, delete, rename, or overwrite existing files. Do not add credentials or connect a live employer, Google, email, payment, or production account.

First show the exact proposed tree, files, dependencies, commands, and tests. If direct Windows filesystem access is unavailable, provide exact PowerShell commands or downloadable files and do not claim that the scaffold was created.
```

#### Prompt 5 - Build the first vertical slice

```text
After the scaffold passes review, implement the smallest tested Stage-1 vertical slice:

approved applicant facts -> one saved public Greenhouse or Lever fixture -> source-policy and liveness validation -> deterministic eligibility and explainable fit -> packet metadata -> READY_FOR_REVIEW -> audit record.

Use fixtures before live integrations. Do not submit, contact an employer, open an authenticated job-board session, or write to the attended-pilot Drive folders or ledger. Include unit, contract, integration, security, and golden-output tests. Report every file changed, command run, test result, known gap, and rollback method.
```

#### Prompt 6 - Establish the production path

```text
When the first vertical slice passes, perform a maker-checker review and produce the production-readiness backlog for development, test, preview, staging, shadow, and production. Include authentication, authorization, tenant isolation, secrets, migrations, backups, recovery, source compliance, prompt-injection defenses, observability, accessibility, CI/CD, rollback, incident response, and cost controls.

Map every release gate to evidence and an accountable human approval. Do not deploy production, add billing, enable external users, or automate employer submission until the corresponding gates in AJAS_Handoff_FINAL_v1.0.md are satisfied.
```

---

## Appendix A - Controlled state vocabulary

| State | Meaning | Minimum entry evidence |
|---|---|---|
| `DISCOVERED` | Posting candidate recorded | Canonical source and posting identity |
| `SCREENED` | Eligibility and fit review completed | Requirements, evidence, gaps, and constraints |
| `SELECTED` | Preparation authorized | Steve selection or approved standing-policy reference |
| `PREPARING` | Packet work active | Job ID, run ID, evidence version, expected manifest |
| `READY_FOR_REVIEW` | Complete packet stored and verified | All artifacts read back; final liveness check passed; no blocking error |
| `SUBMITTED_BY_USER` | Steve or another authorized user reports submission | User report with timestamp and target posting |
| `SUBMISSION_CONFIRMED` | Submission receipt captured | Confirmation page, receipt, or employer acknowledgment |
| `INTERVIEWING` | Interview process reported | Employer or user evidence |
| `OFFER_RECEIVED` | Offer reported | Offer evidence reference; sensitive content protected |
| `REJECTED_BY_EMPLOYER` | Employer rejection reported | Employer message or user evidence |
| `WITHDRAWN_BY_USER` | User ends candidacy | User instruction and reason when supplied |
| `REJECTED_AS_POOR_FIT` | Screening rejects preparation | Named disqualifier or evidence gap |
| `CLOSED_BEFORE_SUBMIT` | Posting closed before user submission | Liveness evidence |
| `DUPLICATE_SKIPPED` | Existing application/posting identity matched | Duplicate record reference |
| `ERROR_RETRYABLE` | Bounded retry may resolve failure | Error code, retry policy, next retry |
| `ERROR_NEEDS_USER` | User decision or action required | Exact blocker and permitted choices |

Corrections do not erase audit history. Reopening, reversal, retry exhaustion, duplicate merges, reposts, and erasure effects require explicit Stage-0 transition rules.

---

## Appendix B - Source and terms register schema

Each enabled source record contains:

- source/provider name;
- interface or official URL pattern;
- source type;
- documentation URL and verification date;
- terms/policy URL and review date;
- authentication requirement;
- allowed operations;
- prohibited operations;
- rate-limit and caching rules;
- attribution requirement;
- data fields collected;
- canonical posting identity method;
- liveness method;
- change-monitoring owner;
- allowlist status;
- review expiry date.

No source becomes enabled solely because a page or endpoint is publicly reachable.

---

## Appendix C - Round-1 resolution traceability

| Resolution | Formal disposition | Final location |
|---|---|---|
| R1 - no mandatory pilot cross-review | ACCEPT | §§3.6, 12.2 |
| R2 - merged PDF in Drive | ACCEPT AS MERGED | §§3.3-3.4 |
| R3 - employer upload is form-specific | ACCEPT | §3.3 |
| R4 - product storage authority | ACCEPT | §8.1-8.2 |
| R5 - specification before scaffolding | ACCEPT | §11 Stage 0A-0B |
| R6 - modules, not six autonomous agents | ACCEPT | §§7.2, 9.4 |
| R7 - explainable fit without fixed weights | ACCEPT | §7.4 |
| R8 - controlled source allowlist | ACCEPT | §7.3 |
| R9 - security and legal work before external users | ACCEPT | §10 |
| R10 - costs and free tiers are hypotheses | ACCEPT | §§9.3, 13.8, 14.2 |
| R11 - current device/runtime facts | ACCEPT | §9.2 |
| R12 - shadow operation and Steve cutover | ACCEPT | §11 Cutover rule |
| R13 - email optional and separately consented | ACCEPT AS MERGED | §3.7; §14.2 |
| R14 - Pacific intent; platform-specific UTC carve-out | ACCEPT | §3.1 |
| R15 - defined product states and transitions | ACCEPT | §8.3-8.4; Appendix A |
| R16 - verification and traceability labels | ACCEPT | Document purpose; §§3.4, 4 |
| R17 - preserve 13 technical answers | ACCEPT | §13 |
| R18 - one canonical pilot-ledger writer protocol | ACCEPT | §3.6 |
| R19 - three separate tracks | ACCEPT | §2 |
| R20 - precise non-destructive meaning | ACCEPT | §§5.10, 12.1 |
| R21 - precise OAuth wording | ACCEPT | §§10.1, 13.11 |
| R22 - no product runtime dependency on pilot | ACCEPT | §§2, 8.1 |
| R23 - four authorization layers | ACCEPT | §10.1 |

---

## Appendix D - Round-M2 correction traceability

| Round-M2 correction | Final location |
|---|---|
| 1. No merged-PDF READY exception | §3.4 |
| 2. Employer upload is form-specific | §3.3 |
| 3. Public does not automatically mean authorized | §7.3; Appendix B |
| 4. Preserve lessons with dated scope | §5 |
| 5. Cost is a hypothesis | §13.8 |
| 6. Response data is not proof of market validation | §4 |
| 7. Refresh live state at assembly | §4 |
| 8. Remove stale environment assumptions | §§3.1, 9.2-9.3 |
| 9. Email excluded as MVP dependency | §3.7 |
| 10. Keep all three tracks separate | §2 |
| 11. Define non-destructive precisely | §§5.10, 12.1 |
| 12. Use one controlled vocabulary | §8; Appendix A |
| 13. Keep Stage 0 sequential | §11 Stage 0A-0B |
| 14. Describe the 12-step workflow accurately | §7.1 |
| 15. Strengthen the human boundary | §§1, 7.1, 10.1 |
| 16. Separate authorization layers | §10.1 |
| 17. Keep live-pilot agents independent | §3.6 |
| 18. Use modules, not an autonomous-agent fleet | §7.2 |
| 19. Keep one pilot ledger | §3.6 |

---

## Appendix E - Claude v0.9 audit correction traceability

| Audit correction | Final disposition | Location |
|---|---|---|
| Source filename exactness | Resolved from the actual local source set and Steve's archive listing; provenance differences are labeled. | Document purpose and source set |
| Renderer/upload contradiction | GPT generated the three formats; optional Claude recheck is separate; no Drive upload is claimed. | §12.3; §16.1 |
| Post-submission filing omission | Dated note, supplied receipt, readback, idempotent ledger update, and large-binary repair added. | §§3.8, 7.1, Appendix A |
| Governance identity omission | Master v1.0, 2026-08-27 approval, review-window amendments, and later Friedman ruling named. | Document purpose; §2 Track A |
| Hardware-name conflict | Replaced with capability-based Windows development-computer wording. | §9.2 |

## Appendix F - Action permission matrix

| Action | Stage-1 AJAS modules | Steve | Later optional capability |
|---|---|---|---|
| Search an enabled permitted public source | Allowed within current source policy | Allowed | Additional sources only after review |
| Read LinkedIn or Indeed automatically | Prohibited | Manual use outside AJAS | Not planned |
| Evaluate fit from approved evidence | Allowed with explanation and gaps | Reviews/overrides | Validated scoring only after evidence |
| Generate packet sources and files | Allowed within approved facts and templates | Reviews | Broader templates after tests |
| Store and read back AJAS Personal artifacts | Allowed within authorized Stage-1 root | Can access/export | Object storage after migration |
| Open or authenticate to employer system | Prohibited | Human-only | No autonomous authority planned |
| Enter employer-form data | Prohibited | Human-only | Separate future design could evaluate assistive prefill, but not Stage 1 and never silent transmission |
| Upload file to employer | Prohibited | Human-only | No autonomous authority planned |
| Make attestation or consent choice | Prohibited | Human-only | No autonomous authority planned |
| Contact employer | Prohibited | Human-only | No autonomous authority planned |
| Click Submit | Prohibited | Human-only | No autonomous authority planned |
| Record user-reported submission | Allowed after authenticated report | Supplies report | - |
| Confirm submission from receipt | Allowed after valid evidence | Supplies/reviews evidence | Optional consented read-only mailbox match |
| Correct or delete AJAS data | Only through approved, audited policy | Authorizes/requests | Tenant-safe workflows before external users |
| Promote release or cut over pilot | Prohibited without gate approval | Final authority | Formal approver role after governance change |

Track-A label `READY - Steve submit` maps to Track-C `READY_FOR_REVIEW`. Both mean the packet is complete and verified and Steve must still perform every employer-system action.

## Appendix G - Glossary and final acceptance record

| Term | Meaning |
|---|---|
| AJAS | Internal working name for the Automated Job Application System. |
| AJAS Personal | Track-C Steve-only Stage-1 product. |
| Agent | A bounded logical responsibility with typed contracts; initially a module, not an autonomous deployed actor. |
| Tool | A capability-scoped deterministic adapter invoked only after policy and authorization checks. |
| Approved fact | Versioned applicant fact with provenance, allowed use, sensitivity, and correction history. |
| Posting snapshot | Dated, hashed, source-policy-compliant representation of a job posting. |
| `READY_FOR_REVIEW` | Final autonomous product state; all packet and liveness gates pass, but no employer action has occurred. |
| `SUBMITTED_BY_USER` | Authenticated user reports submission; not yet receipt-confirmed. |
| `SUBMISSION_CONFIRMED` | Receipt, confirmation page, or employer acknowledgment is stored as evidence. |
| Readback | Retrieval of stored bytes or state followed by comparison to the expected result. |
| Idempotency | Repeating the same authorized operation returns the same result without a duplicate side effect. |
| Stage gate | Evidence and human approval required before scope or environment expands. |

Final acceptance conditions for this handoff are: all seven startup rulings are adopted; all five Claude corrections are applied; human-only employer action is consistent throughout; prohibited-source automation remains excluded; production contracts are explicit; the local and new-project startup sequence is present; and the Markdown, DOCX, and PDF are generated from the same final source and pass text, structure, and visual QA.

## Final disposition

**FINAL v1.0 - APPROVED TO BEGIN STAGE 0**

This handoff is complete for new-project initialization. Production deployment, external-user data, live connectors with real personal data, and any employer-system capability remain separately gated. No live-pilot folder, spreadsheet, schedule, source file, application packet, or employer system was modified while preparing this final handoff.
