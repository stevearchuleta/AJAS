---
document_id: AJAS-PERSONAL-ALPHA-FAST-TRACK-001
version: 1.0.0
status: PROPOSED_BUILD_DIRECTIVE
owner_and_final_authority: Steve Archuleta
created_utc: 2026-09-02
current_verified_main_commit: 790e2c1
current_verified_state: locally_tested_not_deployed
primary_objective: deploy_a_practically_usable_steve_only_ajas_web_application
---

# AJAS Personal Alpha Fast-Track Productization Directive

## From a Verified Core Prototype to Steve's Practically Usable Job-Application Website

## 1. Executive correction

The completed startup sequence produced a verified software foundation, not the daily-use product Steve expected to open in a browser.

The current AJAS repository contains:

- a Next.js and TypeScript web scaffold;
- a worker scaffold;
- a typed domain core;
- a deterministic fixture workflow;
- approved-fact, screening, source-policy, state-machine, audit, and packet contracts;
- 129 passing automated tests;
- successful web, worker, and core builds;
- a clean Git repository with 89 tracked files;
- a production-readiness backlog and release-gate matrix.

The current AJAS repository does not yet contain:

- a practical approved-facts editor;
- real user authentication;
- a managed database;
- a Google Drive OAuth connector;
- real AI-provider calls;
- a job-entry and processing dashboard;
- résumé and cover-letter generation;
- Google Drive artifact publication;
- a deployed public or private URL;
- a batch workflow for hundreds of job opportunities.

The implementation therefore completed the written fixture-and-roadmap assignment, but the implementation did not complete Steve's immediate product vision. The next build phase must correct that priority mismatch.

## 2. Product outcome that now governs the build

The next milestone is not complete until Steve can perform the following workflow from a browser:

1. Open the deployed AJAS website.
2. Sign in through an account restricted to Steve during the Personal Alpha.
3. Enter, edit, approve, retire, and review Sources of Truth.
4. Connect Google Drive through explicit OAuth consent.
5. Select a dedicated `AJAS Personal` Drive folder and selected evidence files.
6. Paste an official job-posting URL or approved job-description text.
7. Click **Analyze Job**.
8. Review eligibility, fit, named gaps, and claim-to-evidence links.
9. Click **Prepare Application Packet**.
10. Review a truthful résumé recommendation, tailored résumé content, cover letter, and application instructions.
11. Approve or edit generated content.
12. Save versioned DOCX/PDF/Markdown artifacts to the authorized Drive folder.
13. Open the official employer application link.
14. Submit manually outside AJAS.
15. Record the result, receipt, and later application status inside AJAS.

A passing test suite remains required. A test suite alone no longer constitutes milestone completion.

## 3. Meaning of “AI assistants have access to Google Drive”

The product must provide persistent, authorized Google Drive access without giving model providers raw credentials or unrestricted Drive authority.

Required architecture:

```text
Steve grants OAuth consent
        ↓
AJAS backend stores an encrypted connector authorization
        ↓
DriveConnector reads only authorized files or folders
        ↓
AJAS extracts and versions relevant evidence
        ↓
StructuredAIGateway receives only minimum necessary facts and excerpts
        ↓
AI provider returns a schema-constrained proposal
        ↓
Deterministic AJAS code validates every claim and action
        ↓
ArtifactStore writes approved generated files to the authorized Drive root
        ↓
AJAS reads stored bytes back and verifies identity
```

The AI model must never receive:

- Google OAuth access tokens;
- Google OAuth refresh tokens;
- database credentials;
- unrestricted Drive browsing capability;
- a general-purpose browser tool;
- employer login credentials;
- autonomous permission to create, delete, move, share, or overwrite arbitrary Drive files.

For the Personal Alpha, the preferred Google access design is:

- Google Picker for selecting evidence files;
- `drive.file` for files selected by Steve or created by AJAS;
- a dedicated `AJAS Personal` folder for generated packet artifacts;
- secure refresh-token storage for persistent access;
- separate explicit approval before any broader Drive scope.

A temporary Steve-only broad read scope may be evaluated only when required source files cannot be handled through file selection. Such an exception must remain disabled for friends, family, and commercial users until a separate privacy and verification gate passes.

## 4. Fast-track architecture decision

The build must avoid another prolonged provider-selection exercise. The following initial stack is selected for the Personal Alpha unless a concrete implementation blocker appears.

| Concern | Personal Alpha decision | Expansion path |
|---|---|---|
| Source repository | Private GitHub repository | Protected branches, required checks, signed releases |
| Local clone | `C:\Code\AJAS` or another non-synchronized development root | Separate developer clones |
| Web application | Existing Next.js/TypeScript app | Retain modular monolith until measured need changes |
| Background processing | Existing Node.js/TypeScript worker | Separate scaling policy later |
| Hosting | Azure Container Apps for web and worker | Multiple environments and revisions |
| Structured state | Azure Database for PostgreSQL Flexible Server | High availability and stronger isolation later |
| Personal Alpha queue | PostgreSQL-backed durable job queue | Azure Service Bus only after measured need |
| Secrets | Azure Key Vault and managed identity | Key rotation and environment-specific vaults |
| Stage-1 packet bytes | Dedicated `AJAS Personal` Google Drive root | Azure Blob Storage becomes canonical for multiuser product |
| Google evidence access | OAuth, Google Picker, `drive.file`, selected files | Per-user connectors and verification for public release |
| AI provider | One provider first through `StructuredAIGateway` | Add a second provider after the usable alpha works |
| Initial model integration | OpenAI Responses API with schema-constrained output and explicit privacy settings | Provider evaluation and task-specific routing later |
| Authentication | Google sign-in restricted to Steve's approved account | Invite-only tenant accounts, then external identity platform |
| Observability | Structured application logs, correlation IDs, cost events, error summaries | Azure Monitor/Application Insights and alerting |
| Employer action | Manual only | Remains manual unless a later explicit governance change occurs |

The first practical release must not introduce LangGraph, CrewAI, A2A, custom MCP infrastructure, a vector database, billing, or autonomous employer interaction.

## 5. Source-of-truth user experience

### 5.1 Required screens

The Personal Alpha must provide the following routes or equivalent screens:

```text
/dashboard
/facts
/evidence
/jobs/new
/jobs
/applications/[applicationId]
/settings/connectors
/settings/profile
```

### 5.2 Approved-facts editor

Each approved fact must include:

- category;
- fact text or structured value;
- status: `REPORTED`, `VERIFIED`, `ADOPTED`, `RETIRED`, or another approved vocabulary value;
- evidence source;
- Google Drive file identifier when applicable;
- evidence excerpt or locator;
- allowed-use categories;
- sensitivity classification;
- effective date;
- version;
- correction history;
- Steve approval timestamp.

The AI system may propose a new fact. Only Steve can approve a new source-of-truth fact during Personal Alpha.

### 5.3 Evidence screen

The evidence screen must allow Steve to:

- connect Google Drive;
- choose files through a picker;
- label each file;
- extract readable text;
- inspect the extracted text;
- link evidence to approved facts;
- revoke file access;
- refresh a changed file into a new version;
- see the last successful readback and hash.

## 6. Job-processing workflow

### 6.1 Initial input modes

The Personal Alpha must support:

1. one official job-posting URL;
2. pasted job-description text labeled as user-provided and not independently live-verified;
3. batch import of official URLs through CSV after the single-job workflow passes.

Initial official-source support should prioritize Greenhouse and Lever. LinkedIn and Indeed remain manual reference sources, not automated scraping targets.

### 6.2 Processing sequence

```text
DISCOVERED
  → source validation and snapshot
SCREENED
  → deterministic eligibility
  → AI-assisted requirement extraction and fit explanation
SELECTED
  → Steve authorizes packet preparation
PREPARING
  → résumé selection and tailoring
  → cover-letter generation
  → artifact rendering and inspection
READY_FOR_REVIEW
  → Steve reviews and manually applies
SUBMITTED_BY_USER
  → Steve records submission
SUBMISSION_CONFIRMED
  → receipt or confirmation evidence stored
```

### 6.3 Required output for every analyzed job

- employer;
- role title;
- canonical official URL;
- posting identifier;
- posting snapshot timestamp;
- source-policy result;
- hard eligibility result;
- requirement list;
- approved evidence mapped to each requirement;
- named gaps;
- truthful fit explanation;
- recommended résumé baseline;
- prohibited or unsupported claims;
- estimated AI cost;
- application priority;
- exact next human steps.

## 7. AI implementation rule

The first usable release should use one model provider. A second model provider should not block the product.

Required model pattern:

1. Deterministic code selects approved facts and relevant evidence.
2. Deterministic code retrieves authorized Drive content.
3. AJAS builds a minimum-necessary structured request.
4. `StructuredAIGateway` calls the provider.
5. The provider returns JSON matching a strict schema.
6. AJAS rejects unsupported claims.
7. AJAS preserves named gaps rather than hiding gaps.
8. AJAS records provider, model, prompt version, token use, cost, latency, and outcome.
9. Steve reviews every generated packet before any employer action.

The model must not decide which external tool to call. The model must not directly browse Drive. The model must not write files. Deterministic adapters perform every external action after authorization checks.

## 8. Build milestones and visible completion evidence

### Milestone 0 — clean professional development path

**Goal:** end local release-script fragility before real data enters AJAS.

Required work:

- push current clean repository to a private GitHub repository;
- clone into a non-Google-Drive-synchronized development root;
- preserve the current milestone tags;
- configure GitHub Actions to run dependency installation, formatting check, lint, typecheck, tests, and build;
- require pull-request checks before merge;
- stop using chat-generated ZIP installers and giant pasted PowerShell blocks.

Visible evidence:

- private repository exists;
- current commit and tags match the verified local source;
- one pull request passes CI;
- primary development clone exists outside consumer sync.

### Milestone 1 — deployed preview shell

**Goal:** make AJAS visible through a browser URL.

Required work:

- containerize the web and worker applications;
- deploy a preview environment to Azure Container Apps;
- deploy from GitHub Actions;
- expose `/api/health`;
- display build version and environment on the dashboard;
- add centralized structured error reporting.

Visible evidence:

- Steve opens a private preview URL;
- health endpoint passes;
- a Git commit automatically creates a new Azure revision;
- rollback to the prior revision is demonstrated.

### Milestone 2 — authentication, database, and approved facts

**Goal:** replace fixtures with Steve-controlled real structured data.

Required work:

- create PostgreSQL schema and migrations;
- implement Steve-only authentication;
- implement user, approved fact, evidence source, preference, audit event, and connector-authorization records;
- implement `/facts` and `/evidence` screens;
- log every create, edit, approve, retire, and correction action;
- retain synthetic fixtures for tests.

Visible evidence:

- Steve signs in;
- Steve enters and approves real facts;
- data survives logout and redeployment;
- unauthorized accounts cannot enter Personal Alpha;
- audit history reconstructs every fact change.

### Milestone 3 — Google Drive connector

**Goal:** allow AJAS to use Steve-authorized Drive evidence and save generated artifacts.

Required work:

- implement Google OAuth authorization;
- implement Google Picker file selection;
- implement secure refresh-token storage;
- implement selected-file read, metadata, export/download, version detection, and revocation;
- create or select the dedicated `AJAS Personal` root;
- implement versioned artifact create and readback;
- never overwrite a final artifact silently.

Visible evidence:

- Steve connects Google Drive through the website;
- Steve selects one résumé and one project-evidence document;
- AJAS extracts and displays text;
- AJAS links evidence to an approved fact;
- AJAS creates a test artifact in the dedicated folder and reads the same bytes back;
- revocation blocks subsequent access with a clear message.

### Milestone 4 — real job analysis and AI drafting

**Goal:** deliver the first genuinely useful end-to-end application workflow.

Required work:

- implement `/jobs/new` and application detail screens;
- accept an official Greenhouse or Lever URL;
- snapshot and normalize the job posting;
- run deterministic eligibility rules;
- call the AI gateway for requirement extraction, fit explanation, and drafting;
- show claim provenance and named gaps;
- allow Steve to approve, reject, or edit outputs;
- preserve all prompts, model versions, costs, and validation outcomes.

Visible evidence:

- one real current job URL enters AJAS;
- one complete analysis appears in the browser;
- every material claim resolves to an approved fact and evidence source;
- unsupported claims are blocked;
- Steve can approve the job for packet preparation.

### Milestone 5 — packet generation and manual-application workflow

**Goal:** create the practical output needed for a real application.

Required work:

- select an approved résumé baseline;
- generate truthful tailored résumé content;
- generate a cover letter;
- render Markdown, DOCX, and PDF as approved;
- run ATS text and basic visual checks;
- save versioned artifacts to the authorized Drive folder;
- read back and verify artifacts;
- show the official employer link and numbered submission instructions;
- allow Steve to record submission and upload a receipt.

Visible evidence:

- Steve completes one real application packet from the website;
- final files appear in the dedicated Drive folder;
- AJAS verifies stored artifacts;
- AJAS stops at `READY_FOR_REVIEW`;
- Steve performs submission manually;
- AJAS records the later result.

### Milestone 6 — 350-job operating mode

**Goal:** support Steve's active search at practical volume.

Required work:

- batch import official URLs by CSV;
- deduplicate by canonical URL and ATS identifier;
- create a queue and dashboard;
- separate inexpensive screening from expensive full drafting;
- prioritize high-fit jobs;
- apply daily and monthly model-cost ceilings;
- support pause, resume, retry, and visible dead-letter handling;
- generate full packets only after Steve selection or an explicitly approved policy;
- export application status.

Visible evidence:

- at least 25 representative URLs process as a batch;
- duplicates are safely linked or skipped;
- failures remain visible and recoverable;
- cost totals are visible before full drafting;
- Steve can move selected opportunities through packet preparation without terminal commands.

## 9. Multiuser and commercial expansion

The Personal Alpha must remain Steve-only until the end-to-end workflow works reliably with real jobs.

The database schema should still include `tenant_id` or an equivalent ownership boundary from the beginning. External users remain disabled.

### Invite-only friends-and-family beta

Required additions:

- per-user authentication;
- per-user Google OAuth authorization;
- strict tenant isolation in database queries and object namespaces;
- cross-tenant negative tests;
- invitation and account-revocation controls;
- user-specific facts, evidence, preferences, jobs, packets, and audit history;
- support and incident workflows;
- privacy notice and consent records.

### Commercial pilot

Required additions:

- product-controlled object storage as canonical packet storage;
- billing and entitlements;
- terms, privacy, data-retention, deletion, and legal review;
- abuse controls and rate limits;
- customer support and incident response;
- backup and restore exercises;
- security review and vulnerability management;
- model and source cost accounting;
- accessibility validation;
- controlled release and rollback process.

Commercial work must not delay the Steve-only practical alpha.

## 10. Required engineering-process correction

Every future builder LLM, checker LLM, and human engineer must follow these rules:

1. Use Git branches, commits, pull requests, and CI. Do not distribute source-tree mutations through bespoke ZIP installers.
2. Test every operator command on the exact supported platform before Steve receives the command.
3. Keep the source repository outside Google Drive, OneDrive, Dropbox, and similar consumer synchronization roots.
4. Generate manifests and hashes by code. Do not manually transcribe cryptographic digests.
5. Pin one Git executable and one supported toolchain.
6. Use noninteractive release automation. Use the website for product approvals.
7. Require no more than one operator command per normal gate.
8. Return a concise result summary and an evidence artifact after each gate.
9. Classify failures with mutation state, repository state, recovery requirement, and next action.
10. Do not ask Steve to debug untested shell code.
11. Do not treat a local build as a deployed product.
12. Do not let governance work expand the active critical path unless a concrete safety, corruption, authorization, or verification blocker exists.
13. Demonstrate a visible user capability in every product milestone.
14. Keep the current 129 tests and add tests for every new feature.
15. Add end-to-end browser tests for the exact Steve workflow.

## 11. What `npm test`, `npm run build`, and `npm run dev` mean

These commands remain useful to developers:

- `npm test` verifies automated behavior.
- `npm run build` proves that source code compiles into deployable artifacts.
- `npm run dev` starts a local development website.

These commands are not the intended AJAS user experience.

After Personal Alpha deployment:

- GitHub Actions runs tests and builds automatically;
- Azure hosts the application;
- Steve opens the website in a browser;
- Steve performs product work through forms, dashboards, review screens, and buttons;
- terminal commands remain exceptional maintenance tools.

## 12. Immediate builder assignment

Start from the clean verified `main` state at commit `790e2c1` and create a new branch for the Personal Alpha fast track.

Return a concrete implementation plan for Milestones 0 through 5, but begin implementation with Milestone 0 and Milestone 1 immediately after Steve approves the plan.

The first builder response must include:

1. exact current-repository readback commands that do not mutate source;
2. the proposed private GitHub and non-synchronized clone process;
3. the proposed Azure resource list and names;
4. the exact files to add or modify for containerization and deployment;
5. the GitHub Actions workflow design;
6. the preview-environment acceptance tests;
7. cost-control defaults requiring Steve approval;
8. one concise operator action at a time;
9. no source-tree installer;
10. no broad audit unrelated to the deployed preview goal.

The builder must then produce code through reviewable commits or a pull request. The checker must review the commit, CI evidence, and deployed revision—not a pasted transcript.

## 13. Personal Alpha definition of done

The Personal Alpha is complete only when all statements below are true:

```text
DEPLOYED_PRIVATE_URL=True
STEVE_AUTHENTICATION=True
APPROVED_FACTS_UI=True
PERSISTENT_POSTGRESQL=True
GOOGLE_DRIVE_OAUTH=True
SELECTED_EVIDENCE_IMPORT=True
DEDICATED_DRIVE_ARTIFACT_ROOT=True
REAL_OFFICIAL_JOB_INPUT=True
DETERMINISTIC_ELIGIBILITY=True
AI_ASSISTED_FIT_AND_DRAFTING=True
CLAIM_PROVENANCE_VISIBLE=True
NAMED_GAPS_PRESERVED=True
DOCX_OR_PDF_PACKET_GENERATED=True
DRIVE_WRITE_AND_READBACK_VERIFIED=True
READY_FOR_REVIEW_UI=True
OFFICIAL_APPLICATION_LINK_VISIBLE=True
EMPLOYER_SUBMISSION_AUTOMATION=False
APPLICATION_STATUS_TRACKING=True
AUDIT_TRAIL=True
COST_TRACKING=True
CI_PASS=True
END_TO_END_BROWSER_TEST_PASS=True
STEVE_REAL_JOB_PILOT_PASS=True
```

A result containing only `npm test`, `npm run build`, a health endpoint, architecture documents, or a backlog does not satisfy this definition.

## 14. Final directive

> Build the smallest real AJAS website that Steve can use for a genuine job application. Preserve the verified core. Connect approved facts, selected Google Drive evidence, one official job, one schema-constrained AI provider, deterministic validation, versioned Drive artifacts, and a human review boundary. Deploy that workflow. Only afterward add batch scale, friends-and-family tenancy, and commercial controls.
