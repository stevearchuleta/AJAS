# AJAS Stage-0B Scaffold Manifest

**Manifest ID:** `AJAS-STAGE0B-SCAFFOLD-0.1-2026-08-30`  
**Status:** REVIEW CANDIDATE  
**Scope:** Synthetic, connector-free repository skeleton

This is a Prompt-4 scaffold review candidate. It does not claim that the full Stage-0B release gate has passed.

## Stage-0B review-candidate baseline

- TypeScript modular monorepo using npm workspaces
- Node.js 22.16.0 supported for Steve's immediate local verification
- Node.js 24 LTS used in continuous integration and targeted for later deployment
- Next.js 16.3.3 Active LTS security release
- React and React DOM 19.2.0
- TypeScript 6.0.3, ESLint 10.9.1, and `typescript-eslint` 8.68.0; TypeScript is compatibility-pinned to the lint parser peer range
- No database, ORM, identity, queue, AI, Google, Gmail, payment, browser-agent, employer, LinkedIn, or Indeed dependency

## Safety boundary

The scaffold exposes no employer-system capability. Autonomous authority ends at `READY_FOR_REVIEW`.

## Known deferred decisions

- Managed PostgreSQL provider, region, ORM, migrations, and queue library
- Authentication provider and session implementation
- AI provider and evaluation set
- Document-rendering toolchain
- Stage-1 artifact-storage authorization
- Preview, worker, staging, and production providers
- Notification provider

## Remaining Stage-0B gate evidence

- Approved migration skeleton and reversible synthetic migration proof
- Approved authentication and authorization skeleton
- Provider-neutral audit-event schema and sanitized audit record
- Reversible preview with synthetic data only
- Protected `main` configuration after GitHub initialization is separately approved
- Governance definitions, control inventory, change control, temporary-file cleanup, state-machine clarifications, and liveness controls identified in Stage 0A review

The shared Google Drive `AJAS` folder is a development mirror. It is not the separately authorized Stage-1 runtime byte store.

## Required checks

1. `npm run verify:scaffold`
2. `npm run format:check`
3. `npm run lint`
4. `npm run typecheck`
5. `npm test`
6. `npm run build`

## Rollback

Before Git initialization, rollback consists of removing only the exact new scaffold files after confirming that no pre-existing file was overwritten. The supplied installer aborts on any file collision. If an apply fails after creating a target object, it deliberately retains that object for attended review instead of issuing a target-delete command; Steve must paste the output before any cleanup is authorized.
