# ADR-0001: Runtime and Package Manager

**Status:** SELECTED FOR STAGE-0B REVIEW  
**Date:** 2026-08-30  
**Authority:** Selection prepared under Steve's Prompt-4 authorization; final ratification remains a human review gate

## Context

Steve's verified Windows environment contains Node.js 22.16.0 and npm 10.9.2. Official Node.js release information identifies Node.js 22 and 24 as supported LTS lines on 2026-08-30. Next.js 16.3.3 is the current Active-LTS security release and requires Node.js 20.9.0 or later.

## Decision

- Use npm workspaces.
- Permit Node.js 22.16.0 through Node.js 24 for scaffold verification.
- Use Node.js 24 in CI and target Node.js 24 for later deployments.
- Use npm 10.9.2 as the declared package manager for compatibility with Steve's current environment.
- Do not install pnpm or Yarn.
- Pin TypeScript 6.0.3 because it is the newest stable release inside the current `typescript-eslint` peer range (`>=4.8.4 <6.1.0`).
- Use supported ESLint 10.9.1 with `typescript-eslint` 8.68.0 and a minimal deterministic flat configuration. Do not add `eslint-config-next` until its complete transitive plugin set accepts ESLint 10 without an invalid peer tree.
- Defer TypeScript 7 until the full lint toolchain declares compatible peer ranges and the AJAS checks pass against the upgrade.

## Consequences

Steve can verify the scaffold immediately without a runtime upgrade. CI provides a current LTS baseline. The compatibility pin and minimal lint configuration avoid accepting an invalid dependency tree merely to add framework-specific lint presets. Framework-specific Next.js lint rules remain a later reviewed addition. A later security-maintenance decision may require upgrading Steve's local Node.js patch version before real data or deployment.

## Rollback

Delete the generated lockfile and change only the versioned ADR and package metadata through an approved change. No application data migration is involved.
