# M2A-6 - Authentication foundation (first implementation batch)

Status: source implementation only; no live authentication is enabled by this batch.

## Implemented scope

The shared Personal Alpha policy defaults to disabled, denies every discovery session, compares exact Google subjects after explicit enrollment, and returns only fixed decision fields. The policy requires identity supplied by a trusted provider callback or an authoritative server-side session check. The policy does not validate OIDC tokens and must never receive identity claims directly from request JSON.

The shared auth-event writer generates correlation IDs internally and accepts only fixed event codes. Provider profiles, subjects, tokens, cookies, URLs and raw exceptions are not logging inputs.

The separate `dev:auth-spike` launcher fixes the listener to `localhost:3000`, rejects extra command arguments and CI/production invocation, and does not run on module import. Actual socket reachability remains a later runtime test. The normal development command is preserved; the normal command must not be used for real discovery.

The current `NODE_ENV === "development"` admission gate is temporary local-spike scaffolding: production remains intentionally deny-all until M2B introduces a separately reviewed production admission path; production enablement must replace the local-spike gate by design and must never be achieved by merely relaxing or deleting the development check.

Next.js development logging is disabled with `logging: false`; existing HTTP security headers remain. This is not a blanket guarantee that arbitrary application code or third-party code cannot log sensitive information. Better Auth logging and callback/error sentinel tests remain required in the integration batch.

Recursive Docker exclusions cover nested environment files and credential/key patterns. Existing Git ignore rules remain unchanged because the observed candidate checks already passed. A Docker-context canary exercise remains required before any direct filesystem-context build containing real secrets.

## Execution boundary

A separately reviewed Python installer creates `milestone2-auth-spike` in the existing external worktree directory, materializes this exact source batch, restores the existing locked dependencies with lifecycle scripts disabled, formats touched source with repository-pinned Prettier, runs the existing scaffold check and full CI command, and verifies unchanged primary-main and lockfile state. No commit, push, PR, merge or deployment occurs.

Dependency restoration reads GitHub/npm and writes the new worktree plus normal package cache and an external evidence directory. No Better Auth dependency is added during this batch. A failed dependency restore is a stop, not permission to enable install scripts or force dependency resolution.

## Next integration gate

The next code batch verifies exact published Better Auth 1.7.3 metadata before dependency mutation and adds lazy server initialization, safe auth routes, Google-only online scopes, deliberate-rejection UI, private candidate capture and enrollment helpers, stateless-session limits, and provider-flow tests. No Google client, local credential file, private capture directory, Neon resource or production-auth change is authorized here.

The approved ADR-001 v0.2 still governs the full spike. Passing this batch does not establish that OAuth works, that an identity was observed, or that M2 is complete.

## Failure recovery

On any installer STOP, preserve the feature worktree and external evidence. Do not rerun, delete the worktree, force-install dependencies or reset main. Return the fixed stop code and nonsecret command evidence for reconciliation. Windows full-CI results are authoritative for this repository and are not inferred from builder-side fixtures.
