# Stage-1 Prompt-5 Test and Rollback Plan v0.1

## Required test classes

| Class       | Principal evidence                                                                                                                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Unit        | Fact approval/provenance, exact-board policy and pins, two saved-liveness observations, twelve requirement semantics, named gaps, artifact readback, state transitions, audit, and idempotency.                          |
| Contract    | Strict schema and unknown-field rejection, evidence-ref resolution, RFC 6901 pointer allowlist, byte-span bounds, SHA-256 shape, exact fixture identity, trusted policy pins, result envelopes, and boundary vocabulary. |
| Integration | Full synthetic fixture-to-READY path, gate failures, zero network, idempotent replay, unavailable audit sink, and current-liveness preservation.                                                                         |
| Security    | Prompt-injection containment, hostile URL rejection, fixed filenames, no post-READY capability, no Track-A/personal/secret fixture, and no employer action.                                                              |
| Golden      | Exact canonical output, insertion-order independence, twelve ordered requirements, preferred gaps, policy pins, fixture hashes, artifact hashes, `NOT_CHECKED`, and safe synthetic-review wording.                       |

The complete gate also runs scaffold verification, Prettier, ESLint, TypeScript, all
Vitest suites, the web/core/worker build, and the deterministic demo.

## Evidence-traceability tests

The fixture omits the raw response body and response headers. Contract tests therefore
validate the minimized evidence index rather than pretend to reparse unavailable
bytes:

1. The capture is pinned to 12,618 bytes and raw-body SHA-256
   `8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b`.
2. `/content` is pinned to 9,788 UTF-8 bytes and decoded-scalar SHA-256
   `615d66c346d5f51124a6f0ce5cbff0a5a8833a738b2cb64351113de89df613da`.
3. `/location/name` is pinned to 29 UTF-8 bytes and decoded-scalar SHA-256
   `138f415c86f026deedc42a6c4f614594fd08f5de0b873e7cb8c1ea519c59fc8e`.
4. Every evidence record has a unique ID, an allowed RFC 6901 pointer, a nonempty
   half-open byte span within its pointer value, an exact byte-length equation, and a
   lowercase 64-hex fragment hash.
5. Every one of the twelve requirements has at least one evidence reference, and each
   referenced ID resolves to exactly one evidence record. A reviewed fragment may
   support more than one requirement, as the office-tool fragment does.
6. Raw posting excerpts are absent. Posting content is inert data and cannot alter
   policy, tools, state, IDs, audit, or the human boundary.

These checks establish internal consistency and tamper-evident traceability. Because
the source bytes are deliberately excluded, CI does not claim to reproduce the human
semantic review or recalculate fragment hashes from raw text.

## Policy-pin and capture tests

The policy pins and validates:

- fixture ID `greenhouse-greenhouse-8073203-capture-20260830`;
- raw-body SHA-256
  `8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b`;
- canonical minimized-posting SHA-256
  `31802720c22f4c62d974f417f0c94bac377240ddb7d0da10b745fecd828201d9`;
- synthetic-facts snapshot ID `facts-synthetic-fpa-001-v1` and canonical SHA-256
  `87eb5496e5850b6eb5524148b236f83ee8f8e768fc560ba80d6577536072cff2`;
- fixture-command canonical SHA-256
  `4b75268e8bb4c450f0121c146ed198571bfc77055e415fe99c4461b8e01fa9ce`;
- intake header-evidence SHA-256
  `dc58a378cacad28fde88b5bc665b3b3481e1178ff324b78a1c1c6bcb6c720d32`;
  and
- PRE_READY header-evidence SHA-256
  `e036352b011e055d6c59fae0cc182f40f4d05cce5225599b96d14fe33822a859`.

The two capture records must remain distinct:

| Phase     | Observed UTC               | Request ID                         | Header-evidence SHA-256                                            |
| --------- | -------------------------- | ---------------------------------- | ------------------------------------------------------------------ |
| Intake    | `2026-08-30T05:18:58.000Z` | `2b470d8ff6f579a6df38c122c2421601` | `dc58a378cacad28fde88b5bc665b3b3481e1178ff324b78a1c1c6bcb6c720d32` |
| PRE_READY | `2026-08-30T05:22:53.000Z` | `e0af3a83d51d798fe213dfd3654925f4` | `e036352b011e055d6c59fae0cc182f40f4d05cce5225599b96d14fe33822a859` |

Tests reject a duplicate timestamp, request ID, header hash, wrong observation order,
or a mismatch against the policy pins.

## Requirement-semantics tests

The ordered fixture contains exactly twelve requirements: two required eligibility
rows, eight required fit rows, and two preferred fit rows.

Tests prove that:

- role location requires an explicit approved compatibility fact and is not inferred
  from residence;
- authorization specifically covers full-time U.S. work;
- FP&A and Corporate Finance are alternatives for the seven-year criterion;
- high-growth SaaS and technology are alternatives;
- general business partnering is required, while direct Marketing-leadership
  partnership in software/cloud is preferred;
- forecasting, financial modeling, budgeting, and variance analysis are all required;
- spreadsheet and presentation tools are separate categories, with alternatives
  inside each category;
- AI evidence is specific to automating FP&A workflows;
- planning-platform experience is preferred and does not block readiness;
- required missing or semantically incompatible evidence is unresolved and blocks;
- only an explicit compatible negative becomes a disqualifier; and
- preferred nonmatches produce named gaps without a numeric score.

## Deterministic time and liveness tests

The policy/review time `2026-08-30T05:00:00Z`, evaluation time
`2026-08-30T05:23:00Z`, 3,600-second saved-evidence window, and policy expiry
`2026-09-29T05:00:00Z` are fixed test controls. The two observation ages at evaluation
are 242 seconds and 7 seconds. Boundary tests cover future evidence, equality at the
test maximum, one second beyond it, and expired policy behavior.

Those values are not runtime source approval, a ratified liveness-freshness target, an
availability objective, or a service level. A passing test proves only that the saved
observations satisfy the deterministic fixture rule. Both observations and the result
must continue to report `currentStatus: NOT_CHECKED`; no test may relabel them
`CURRENTLY_LIVE`.

The structured `application_deadline: null` and separately reviewed anticipated date
`2026-08-31` must both survive parsing, hashing, packet metadata, and golden output.
Tests reject silent promotion of the body-derived date into the structured API field.
A runtime workflow would require a fresh official liveness/deadline check.

## Safe synthetic-review and boundary tests

The successful result is limited to `readinessScope:
STAGE1_VERTICAL_SLICE_TEST`, reports `productionReady: false`, and describes a
synthetic fixture packet ready for independent human inspection. Tests require:

- `currentLiveness: NOT_CHECKED`;
- `employerActionPermitted: false`;
- `employerActionsPerformed: []`;
- `nextAutonomousAction: null`;
- no instruction to apply or submit;
- no employer authentication, authenticated session, form, upload, attestation,
  contact, or submission operation; and
- no attended-pilot Drive or ledger reference or write.

## Patch safety contract

The Windows patch is version-specific. Its manifest classifies each operation as `ADD`
or `REPLACE` and pins preimage/postimage byte counts and SHA-256 values. A dry run must
verify the complete Stage-0B baseline and every operation before any write.

Apply must:

1. acquire a target-scoped mutex;
2. reject protected handoff/archive, reparse, secret, Git, dependency, and generated
   paths;
3. stage on the target volume;
4. preserve verified replacement preimages in a rollback bundle;
5. create additions only when absent and replace only exact preimages;
6. verify every postimage and final manifest;
7. report zero Git, dependency, Drive, network, authenticated-session,
   employer-contact, and submission actions.

## Rollback

Rollback is hash-bound and attended. It restores a replacement only when the installed
file still matches the known Prompt-5 postimage and its retained backup matches the
Stage-0B preimage. It removes an added file only when that file still matches its known
Prompt-5 hash. It never recursively deletes the AJAS root and never overwrites an
independently changed file.

After rollback, the original Stage-0B 54-file manifest must verify. Rollback evidence
remains preserved for review.

## Known gaps

No live source connector, current-liveness request, runtime-ratified source freshness,
PostgreSQL, durable queue, production audit sink, authentication, authorization,
tenant isolation, real document rendering, ATS/visual check, AJAS Personal Drive
adapter, backup/restore, preview, staging, deployment, employer contact, or submission
is included. The minimized fixture cannot independently reperform semantic review
without the omitted raw capture. Prompt 6 remains out of scope.
