# AJAS

AJAS Personal is a human-controlled job-discovery and application-preparation system for Steve Archuleta.

## Binding boundary

AJAS autonomous authority ends at `READY_FOR_REVIEW`. AJAS must never authenticate to an employer system, populate an employer form, upload a file to an employer, make an attestation, contact an employer, or submit an application.

The controlling specification is `AJAS_Handoff_FINAL_v1.0.md`. The controlling file must remain unchanged.

## Current stage

This repository is a Prompt-4 Stage-0B scaffold candidate, not a passed Stage-0B release gate. The skeleton contains no live database, authentication, source, Google Drive, Gmail, payment, AI-provider, or employer integration.

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
```

## Human submission boundary

The web scaffold displays the boundary. Deterministic tests also verify the prohibited employer-action inventory and the absence of prohibited direct dependencies.
