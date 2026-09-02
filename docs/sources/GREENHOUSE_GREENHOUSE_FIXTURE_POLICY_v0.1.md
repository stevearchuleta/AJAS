# Greenhouse `greenhouse` Board Fixture Policy v0.1

**Policy state:** `MANUAL_ONLY`  
**Allowed test-policy operation:** `PROCESS_SAVED_FIXTURE`  
**Runtime network methods:** none  
**Runtime request budget:** zero  
**Current liveness claim:** `NOT_CHECKED`

## Authority and exact source identity

This record permits deterministic processing of one pinned, saved fixture in
`TEST_FIXTURE`. It does not enable Greenhouse generally or authorize a live request.

| Field                      | Value                                                                     |
| -------------------------- | ------------------------------------------------------------------------- |
| Provider and board         | `GREENHOUSE:greenhouse`                                                   |
| External posting ID        | `8073203`                                                                 |
| Internal job ID            | `3497857`                                                                 |
| Title                      | `FP&A Manager`                                                            |
| Employer                   | `Greenhouse`                                                              |
| Public detail request      | `https://boards-api.greenhouse.io/v1/boards/greenhouse/jobs/8073203`      |
| Canonical public posting   | `https://job-boards.greenhouse.io/greenhouse/jobs/8073203?gh_jid=8073203` |
| Official API documentation | `https://docs.greenhouse.io/job-board.html`                               |
| Legal review entry point   | `https://www.greenhouse.com/legal`                                        |

Official Greenhouse documentation says Job Board GET data is public and needs no
authentication. Public availability is not blanket product authorization. The terms
review is not conclusive for runtime enablement, so the policy stays `MANUAL_ONLY`, the
network kill switch stays on, and the runtime request budget stays zero.

## Trusted policy pins

The policy fails closed unless every pinned identity matches.

| Pin                                  | Approved value                                                     |
| ------------------------------------ | ------------------------------------------------------------------ |
| Fixture ID                           | `greenhouse-greenhouse-8073203-capture-20260830`                   |
| Raw response SHA-256                 | `8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b` |
| Canonical minimized posting SHA-256  | `31802720c22f4c62d974f417f0c94bac377240ddb7d0da10b745fecd828201d9` |
| Intake response-headers SHA-256      | `dc58a378cacad28fde88b5bc665b3b3481e1178ff324b78a1c1c6bcb6c720d32` |
| Pre-READY response-headers SHA-256   | `e036352b011e055d6c59fae0cc182f40f4d05cce5225599b96d14fe33822a859` |
| Approved synthetic-facts snapshot ID | `facts-synthetic-fpa-001-v1`                                       |
| Approved synthetic-facts SHA-256     | `87eb5496e5850b6eb5524148b236f83ee8f8e768fc560ba80d6577536072cff2` |
| Approved fixture-command SHA-256     | `4b75268e8bb4c450f0121c146ed198571bfc77055e415fe99c4461b8e01fa9ce` |

The minimized-posting, facts, and command pins are hashes of their defined canonical
contract values. They are not interchangeable with filesystem-byte hashes.

## Independent saved observations

Two unauthenticated public detail observations were made only to capture and recheck
the development fixture. The distinct server times, request IDs, and header hashes
preserve evidence that these were independent responses.

| Phase     | Observed UTC               | Request ID                         | HTTP |  Bytes | Response-headers SHA-256                                           | Raw response SHA-256                                               |
| --------- | -------------------------- | ---------------------------------- | ---: | -----: | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Intake    | `2026-08-30T05:18:58.000Z` | `2b470d8ff6f579a6df38c122c2421601` |  200 | 12,618 | `dc58a378cacad28fde88b5bc665b3b3481e1178ff324b78a1c1c6bcb6c720d32` | `8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b` |
| PRE_READY | `2026-08-30T05:22:53.000Z` | `e0af3a83d51d798fe213dfd3654925f4` |  200 | 12,618 | `e036352b011e055d6c59fae0cc182f40f4d05cce5225599b96d14fe33822a859` | `8f0fb60044719c9c1a262697bfd1ea159261486620935ff8315fb05cd9e9f10b` |

Both observations used `GET`, returned JSON without redirects, and sent no credentials
or cookies. The full response body and response headers are not stored in the
repository.

## Minimized requirement evidence

The repository stores human-reviewed paraphrases, not raw posting excerpts. Evidence
is anchored to the captured raw-body hash and a JSON scalar using RFC 6901. Each span
uses UTF-8 bytes after RFC 8259 JSON decoding and before HTML entity decoding or any
normalization. `startByte` is inclusive and `endByteExclusive` is exclusive.

| Pointer          | Decoded bytes | Decoded-scalar SHA-256                                             |
| ---------------- | ------------: | ------------------------------------------------------------------ |
| `/content`       |         9,788 | `615d66c346d5f51124a6f0ce5cbff0a5a8833a738b2cb64351113de89df613da` |
| `/location/name` |            29 | `138f415c86f026deedc42a6c4f614594fd08f5de0b873e7cb8c1ea519c59fc8e` |

| Evidence ID                                  | Pointer          | Byte span     | Fragment SHA-256                                                   |
| -------------------------------------------- | ---------------- | ------------- | ------------------------------------------------------------------ |
| `ev_role_location_us`                        | `/location/name` | `[0,29)`      | `138f415c86f026deedc42a6c4f614594fd08f5de0b873e7cb8c1ea519c59fc8e` |
| `ev_us_full_time_work_auth`                  | `/content`       | `[5539,5629)` | `b4a8fcbcd9e8960363032bf1c6386cc7e208638f1a6aaf6fb1417eed8b96bddf` |
| `ev_relevant_finance_years`                  | `/content`       | `[3926,3994)` | `a0f1346195c9e221bf69c555e24e2015da5f81feb8d5bec530578778624fe800` |
| `ev_high_growth_saas_or_tech`                | `/content`       | `[3996,4065)` | `80824352f5cd08a37a4343a9768b273365de4d37c48a89a76c1ad4305c1e5762` |
| `ev_business_partnering_required`            | `/content`       | `[4087,4140)` | `04283dd13a02bcc4754048c3830f8ec74e27e61e9820c85e24529a08868d2b4b` |
| `ev_marketing_software_partnering_preferred` | `/content`       | `[4141,4274)` | `4812b43be3a90b40b9f9233ba000d8309d33f5a0775df7b19bff870565135a01` |
| `ev_financial_core`                          | `/content`       | `[4296,4530)` | `fd55d67e829cc4d646fd136597cb1e100613ddbafbde5cdbc14e64009f74c7ac` |
| `ev_communication`                           | `/content`       | `[4552,4789)` | `9b5b24cb5c677c4b57b6b7ffb8233422ab6cead00e4a3b27dfabfdd075ca4f5b` |
| `ev_office_tool_groups`                      | `/content`       | `[4811,4871)` | `ff79483e51aa28a2fc164192e8cd32b9a149ef89e2ea31d266dff816e473bd81` |
| `ev_ai_fpa_automation`                       | `/content`       | `[4893,4961)` | `8a42d8c7ac9f6174f6b610cce290c882ecc87b913fccb697250b206b7e5b8794` |
| `ev_planning_tools_preferred`                | `/content`       | `[4983,5111)` | `22c1da0062e13f024fcc4ab34e392cbf778228fda4650c44f2ae52c1c9bb9a31` |
| `ev_anticipated_closing_date`                | `/content`       | `[7310,7371)` | `76aab8ac6eccd46877e8fb113ab9eaf8ae1e090c7611cc474f558182e62e45b5` |

The raw body is required to reperform semantic review. Hashes and spans are
tamper-evident traceability, not a substitute for the omitted source bytes or a new
live check.

## Closing-date discrepancy

The structured Greenhouse `application_deadline` field was `null`, while a separately
reviewed body fragment stated an anticipated closing date of `2026-08-31`. The fixture
preserves both facts without silently choosing one as canonical. The body-derived date
is posting/liveness metadata, not applicant fit, and a real workflow would require a
fresh official check before relying on it.

## Time controls and liveness meaning

`2026-08-30T05:00:00Z` policy/review timestamps, the
`2026-08-30T05:23:00Z` fixture evaluation time, the 3,600-second saved-evidence window,
and the `2026-09-29T05:00:00Z` policy expiry are deterministic test controls. They are
not ratified runtime freshness targets, service levels, source approvals, or claims
about the posting now.

The observations prove only `LIVE_AT_CAPTURE` at the two recorded times. Their
`currentStatus` remains `NOT_CHECKED`; this slice never claims `CURRENTLY_LIVE`.

## Fail-closed and human-boundary rules

Processing is denied for any missing or mismatched trusted pin, policy, provider,
board, job, host, path, evidence reference, span, hash, observation, source time,
request ID, or header hash. It is also denied for a non-HTTPS URL, redirect,
credential/cookie use, non-200 evidence, future or stale saved observation, enabled
network method, or runtime request budget above zero.

No fixture decision authorizes employer authentication, an authenticated job-board
session, form entry, upload, attestation, employer contact, or submission. A successful
fixture run creates only a synthetic packet for human review inside the test scope.
