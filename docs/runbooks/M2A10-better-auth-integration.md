# M2A-10 - Better Auth exact-lock installation and runtime integration

## Scope

Install Better Auth 1.7.3 into a new `milestone2-better-auth-integration` worktree from `65a96b8288b539bbf8e005b95850a09dcdad3c08`. Preserve primary main, existing worktrees, prior ADRs, and evidence. No commit, push, PR, merge, Azure action, Google configuration, credential file, database migration, or Neon provisioning belongs to this installer.

This batch adds a real Better Auth runtime factory, typed Google-only options, the authentication secret-provider interface, telemetry-off launch settings, and regression tests. **No public HTTP auth handler or live Google flow is enabled by this batch.** The factory is deliberately not connected to route handlers until the private bootstrap storage, enrollment helper, scope/body restrictions, result page, and session-response filtering arrive together in the next reviewed source batch. No repeated dependency inspection is needed if the reviewed hashes still match.

## Exact dependency contract

The approved candidate lockfile is preserved under the M2A-9 evidence directory. The expected SHA-256 is:

`e8a189ad0c073b462b2f7398e7b4a384e932b0fdb606c807d8d3141642028df5`

The baseline lockfile SHA-256 is:

`e4987148d5b1aec52c7c1a7e2c631113d3ace5da1d599e96ac0a1270ae0b5750`

The reviewed graph adds 22 package entries, removes zero, and changes 39 existing entries with field histogram `dependencies: 1`, `dev: 38`, `devOptional: 37`. The only workspace dependency addition is `apps/web` gaining exact `better-auth: 1.7.3`. Existing version, resolved source, and integrity fields must remain unchanged.

The installer copies the already-reviewed lockfile into the new worktree, runs `npm install --package-lock-only --ignore-scripts --save-exact better-auth@1.7.3 --workspace @ajas/web`, requires byte identity, and only then runs `npm ci --ignore-scripts`. This seeds the approved graph rather than intentionally resolving against newer transitive ranges. The lock must also match after package materialization and full local CI. A different hash is an unexplained change requiring reconciliation; a mismatch does not by itself prove registry movement.

All package lifecycle scripts remain disabled. Existing dependencies may already declare lifecycle scripts; the zero-declaration assertion applies to the 22 newly added packages. Their extracted package manifests are checked before project code, Prettier, or tests execute. Npm itself is the existing trusted toolchain; later validation intentionally executes the inspected package code.

Fresh npm audit results are accepted only with valid nonnegative counts. High/critical findings stop validation; low/moderate findings remain visible for review. A zero audit count is a dated advisory result, not a guarantee of security.

## Runtime and privacy contract

- Read private credentials only when the server invokes the async factory. Module import and Next.js build require no real secrets.
- Preserve the existing centralized, exact-subject admission policy. Production remains deny-all. Replace the local development path through a separately reviewed M2B production design; never merely delete the development gate.
- Explicit `telemetry: { enabled: false, debug: false }` and both launchers force `BETTER_AUTH_TELEMETRY=0` and `BETTER_AUTH_TELEMETRY_DEBUG=0`. Runtime configuration fails if telemetry is not explicitly off.
- Use `better-auth/minimal` without dependency deletion or npm overrides. The five vendor adapter packages remain in the approved dependency graph. Bundled/traced runtime inclusion must be measured, not inferred from lockfile membership.
- Keep both approved `@better-auth/utils` versions (0.4.2 and nested 0.5.0) under vulnerability tracking. No forced deduplication.
- Request only openid, email, profile; disable default-scope duplication, offline access, incremental scope inheritance, email/password login, and account linking.
- Retain CSRF, origin, state-cookie and library token validation. A direct call to the admission callback is not authentication.
- Explicit 900-second encrypted stateless sessions, no automatic refresh, no account-token cookie. Actual session issuance/expiry/logout remains a later live-flow gate.
- The private candidate-capture port has no production file adapter in this batch. Missing capture support rejects discovery before runtime initialization; hook-level failures also reject. Tests use in-memory synthetic captures only.
- Raw vendor logging is disabled. Fixed event codes contain no private payloads. The validation hook never claims that a permitted identity already has a created session.
- The options' error URL reserves the reviewed local result route, but the route is not shipped yet. Enabling Google before the result/capture/request wrapper exists is prohibited.
- Never export the library handler or full getSession payload directly to the browser. The next route batch must reject scope/authorization parameter expansion, sanitize session responses, and show capture completion only with server-side evidence.
- `apps/web/.env.example` contains blank names only. Do not copy values into tracked examples. Existing root `.env.example` and `verify-scaffold.mjs` remain unchanged.

## Tests and promotion

The new test files cover configuration denial, secret-provider failures, exact provider admission, all-discovery denial, failed/missing capture, fixed errors/events, telemetry settings, short encrypted session options, actual Better Auth initialization, absent/forged-session rejection, and blank-example/source invariants. Runtime tests prohibit fetch and use synthetic values. No test claims real Google token verification, Windows ACL correctness, private-file capture, a bound localhost socket, or live sign-in.

The installer runs pinned Prettier on exact touched TS/MJS/JSON/Markdown paths, excluding the byte-pinned lockfile; then existing scaffold verification, full `npm run ci`, and `git diff --check`. No tsconfig or CI strictness reduction is authorized. Node 24 / GitHub CI and container build evidence remain subsequent gates.

M2A, M2, and the complete authentication spike remain open after this batch.

## Measured local Better Auth runtime evidence

The successful local Node 22.16.0 gate on 2026-09-09 ran all 214 Vitest tests and completed the Next.js production build with Better Auth 1.7.3 installed. `tests/security/m2-better-auth-runtime.test.ts` completed all three tests in 2,622 ms after the real-library initialization test received its 60,000 ms per-test ceiling.

The preceding first materialized-package run reached Vitest's 5,000 ms default ceiling. The later 2,622 ms measurement is consistent with first-load/cold-start overhead and shows that 60,000 ms is headroom rather than observed steady-state duration. It is not a production latency target, and the evidence does not establish one exclusive cause for the first timeout.

## Dated reference basis

Source read on 2026-09-09:

- Better Auth v1.7.3 package: https://raw.githubusercontent.com/better-auth/better-auth/v1.7.3/packages/better-auth/package.json
- Tagged auth option types: https://raw.githubusercontent.com/better-auth/better-auth/v1.7.3/packages/core/src/types/init-options.ts
- Tagged stateless defaults: https://raw.githubusercontent.com/better-auth/better-auth/v1.7.3/packages/better-auth/src/context/create-context.ts
- Tagged Google provider: https://raw.githubusercontent.com/better-auth/better-auth/v1.7.3/packages/core/src/social-providers/google.ts
- Telemetry controls: https://better-auth.com/docs/reference/telemetry

Vendor documentation is a design input. Installed-package compilation, tests, and readback are the implementation evidence.
