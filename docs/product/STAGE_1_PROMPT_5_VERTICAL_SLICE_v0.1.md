# Stage-1 Prompt-5 Vertical Slice v0.1

## Outcome

The smallest implemented path is:

`approved synthetic facts -> saved public Greenhouse fixture -> offline source-policy and saved-evidence validation -> deterministic eligibility and explainable fit -> verified packet metadata -> READY_FOR_REVIEW -> audit events`

`READY_FOR_REVIEW` is reached only inside `STAGE1_VERTICAL_SLICE_TEST`. It means a
synthetic, fixture-only packet is ready for human inspection. It does not mean that a
real applicant is eligible, the posting is currently live, the packet is production
ready, or an application should be submitted.

The slice cannot authenticate to an employer system, open an authenticated job-board
session, populate a form, upload a file, make an attestation, contact an employer, or
submit an application.

## Preconditions

1. The command is `FIXTURE_ONLY` in `TEST_FIXTURE` and matches the policy-pinned
   command hash.
2. Applicant facts are `SYNTHETIC`, approved, effective, use-scoped,
   provenance-linked, and match the pinned snapshot ID and canonical hash.
3. The source policy matches the exact provider, board, source key, URLs, posting ID,
   fixture ID, raw-response hash, minimized-posting hash, and two response-header
   hashes.
4. Policy state is `MANUAL_ONLY`; `PROCESS_SAVED_FIXTURE` is the only allowed
   operation; the network kill switch is on and the request budget is zero.
5. Both independent saved observations have distinct timestamps, request IDs, and
   response-header hashes; each reports `LIVE_AT_CAPTURE` and `currentStatus:
NOT_CHECKED`.
6. Every requirement resolves from approved synthetic facts according to its required
   or preferred semantics and its byte-span evidence reference.
7. Three packet artifacts pass actual in-memory byte/hash readback.
8. The audit sink accepts the complete transition batch.

Any failed precondition produces a typed denial and cannot return
`READY_FOR_REVIEW`.

## Twelve reviewed requirements

The source-derived requirements are human-reviewed paraphrases. Each links to a
byte-span/hash evidence record rather than retaining raw posting text.

| Requirement ID                            | Gate          | Materiality | Deterministic meaning                                                  | Evidence reference                           |
| ----------------------------------------- | ------------- | ----------- | ---------------------------------------------------------------------- | -------------------------------------------- |
| `req_us_work_location_compatible`         | `ELIGIBILITY` | `REQUIRED`  | Explicit approved fact confirms compatibility with the U.S. role scope | `ev_role_location_us`                        |
| `req_us_full_time_work_authorization`     | `ELIGIBILITY` | `REQUIRED`  | Explicit approved full-time U.S. work authorization                    | `ev_us_full_time_work_auth`                  |
| `req_7_years_relevant_finance`            | `FIT`         | `REQUIRED`  | At least seven years in FP&A or Corporate Finance                      | `ev_relevant_finance_years`                  |
| `req_high_growth_saas_or_technology`      | `FIT`         | `REQUIRED`  | At least one approved high-growth SaaS or technology context           | `ev_high_growth_saas_or_tech`                |
| `req_business_partnering`                 | `FIT`         | `REQUIRED`  | Significant business-partnering experience                             | `ev_business_partnering_required`            |
| `req_financial_core`                      | `FIT`         | `REQUIRED`  | All four named financial-core skill categories                         | `ev_financial_core`                          |
| `req_communication`                       | `FIT`         | `REQUIRED`  | Approved evidence of strong communication                              | `ev_communication`                           |
| `req_spreadsheet_tools`                   | `FIT`         | `REQUIRED`  | At least one supported spreadsheet tool                                | `ev_office_tool_groups`                      |
| `req_presentation_tools`                  | `FIT`         | `REQUIRED`  | At least one supported presentation tool                               | `ev_office_tool_groups`                      |
| `req_ai_fpa_automation`                   | `FIT`         | `REQUIRED`  | Approved use of AI to automate FP&A workflows                          | `ev_ai_fpa_automation`                       |
| `req_marketing_leadership_software_cloud` | `FIT`         | `PREFERRED` | Direct Marketing-leadership partnership in software or cloud           | `ev_marketing_software_partnering_preferred` |
| `req_planning_platforms`                  | `FIT`         | `PREFERRED` | At least one FP&A or marketing-planning platform category              | `ev_planning_tools_preferred`                |

The location row does not infer a residence requirement from the role-location
string. It requires an explicitly approved compatibility fact. The financial-years
row respects the source's FP&A-or-Corporate-Finance alternative. The spreadsheet and
presentation rows model alternatives within each tool category rather than requiring
all four products. The business-partnering row is required, while the separately
worded Marketing/software/cloud experience is preferred. The AI row is specific to
FP&A workflow automation rather than generic AI use.

Required missing or semantically inapplicable facts are `UNRESOLVED`. An explicit,
semantically compatible negative fact can be a `DISQUALIFIER`. Preferred nonmatches
are visible named gaps and never disqualifiers. The successful synthetic fixture has
two preferred gaps and uses no numerical score.

## Evidence and trust contract

Requirement evidence is bound to raw response SHA-256
`8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b`.
The fixture stores RFC 6901 pointers, UTF-8 half-open byte spans, decoded-scalar hashes,
and fragment hashes, but no raw source excerpts or response headers. This provides
tamper-evident traceability. It cannot independently reproduce the human semantic
review without the omitted raw capture.

The source policy also pins the canonical minimized posting, approved synthetic facts,
fixture command, and two distinct response-header evidence hashes. No provider-wide
fallback is allowed.

## Saved liveness and closing date

The two observations occurred at `2026-08-30T05:18:58.000Z` and
`2026-08-30T05:22:53.000Z`, with different request IDs and response-header hashes.
They establish only that the posting was live at capture. The result preserves
`currentStatus: NOT_CHECKED` and makes no current-liveness claim.

The structured API deadline was `null`; a reviewed body span supplied an anticipated
closing date of `2026-08-31`. Both are preserved, and neither is silently promoted over
the other. The body-derived date is posting/liveness metadata, not an applicant-fit
criterion.

The fixed policy/review time, fixture evaluation time, 3,600-second evidence window,
and test expiry make the golden run reproducible. They are test controls, not ratified
runtime freshness targets or source-policy approval.

## Fit contract

Every requirement is returned in fixture order with:

- requirement ID and human-reviewed paraphrase;
- eligibility or fit gate;
- required or preferred materiality;
- `MATCHED`, `GAP`, `UNRESOLVED`, or `DISQUALIFIER`;
- matched fact ID, fact version, evidence reference, and approval reference;
- extraction confidence;
- source evidence references; and
- a named gap when evidence does not resolve the requirement.

## Packet metadata contract

The fixture packet contains `posting-snapshot.json`, `fit-explanation.json`, and
`review-handoff.json`. Each has a stable ID, deterministic filename, MIME type, UTF-8
byte count, SHA-256, readback SHA-256, and `PASS` readback state.

This demonstrates the integrity gate with real bytes in an in-memory test adapter. It
does not claim a CV, cover letter, PDF, ATS extraction, visual validation, PostgreSQL
transaction, authorized Drive readback, production authorization, or live source
integration.

## State and human boundary

The fixture-only state path is:

`DISCOVERED -> SCREENED -> SELECTED -> PREPARING -> READY_FOR_REVIEW`

The result always reports:

- `readinessScope: STAGE1_VERTICAL_SLICE_TEST`;
- `productionReady: false`;
- `currentLiveness: NOT_CHECKED`;
- `employerActionPermitted: false`;
- `employerActionsPerformed: []`;
- `nextAutonomousAction: null`; and
- the official posting URL solely as saved-fixture provenance, not as a current-liveness
  claim or instruction to open an employer form or apply.

No exported transition permits an autonomous post-READY state. No output directs a
human to submit the synthetic fixture as an application.
