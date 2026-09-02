# AJAS

AJAS Personal is a human-controlled job-discovery and application-preparation system for Steve Archuleta.

## Binding boundary

AJAS autonomous authority ends at `READY_FOR_REVIEW`. AJAS must never authenticate to an employer system, populate an employer form, upload a file to an employer, make an attestation, contact an employer, or submit an application.

The controlling specification is `AJAS_Handoff_FINAL_v1.0.md`. The controlling file must remain unchanged.

## Current stage

This repository contains the tested Prompt-5 fixture-only Stage-1 vertical slice. It is not a production release or a passed Stage-1 gate. The implementation contains no live database, authentication, source connector, Google Drive, Gmail, payment, AI-provider, or employer integration.

The slice uses only synthetic applicant facts and a minimized saved public Greenhouse fixture. Its source policy is `MANUAL_ONLY`; runtime network access is disabled. `READY_FOR_REVIEW` is scoped to `STAGE1_VERTICAL_SLICE_TEST`, uses verified in-memory fixture byte readback, and explicitly reports `productionReady: false`.

The Stage-0B gate still requires the approved migration, authentication, audit-event, preview, and sanitized audit-record evidence described by the controlling handoff. No preview or deployment is authorized by this scaffold.

The shared Google Drive `AJAS` folder is a development mirror. It is not the separately authorized Stage-1 runtime byte store.

## Local verification

```powershell
npm ci
npm run verify:scaffold
npm run format:check
npm run lint
npm run typecheck
npm test
npm run build
npm run --silent demo:stage1
```

Focused suites are also available as `test:unit`, `test:contract`, `test:integration`, `test:security`, and `test:golden`.

## Human submission boundary

The web scaffold displays the boundary. Deterministic tests also verify the prohibited employer-action inventory and the absence of prohibited direct dependencies.

Prompt 6 has not started. See `docs/product/STAGE_1_PROMPT_5_VERTICAL_SLICE_v0.1.md` for the implemented contract and known gaps.
