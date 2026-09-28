# Concrete repair specification

Proposed changes for the owner, based on the 28 September 2026 public audit. These are implementation and acceptance criteria, not claims that NextDoor's backend has been patched.

## 1. Model a source run independently from published jobs

Keep one record per employer/source attempt:

```text
employer_id, source_id, connector_version
requested_url, final_url, http_status, response_hash
attempted_at, completed_at, last_success_at
state: success | valid_empty | fetch_failed | access_limited |
       source_missing | source_changed | parse_failed | validation_failed
parsed_job_count, previous_job_count, added_ids, removed_ids
schema_version, validation_errors, published_snapshot_id
```

An HTTP 200 application shell can be a missing board (Aizen). A 404 hosted board can coexist with a healthy empty feed (Plivo). Evaluate the actual source used by the employer, not one HTTP status in isolation.

Publish a candidate snapshot only after source identity, response schema, job identifiers, date semantics and location references pass validation. An unexplained drop to zero should be held for verification; retain the previous snapshot marked stale. A confirmed explicit empty state may replace it. The threshold for smaller count drops should depend on employer size and observed history, not an arbitrary universal percentage.

Backoff and retry transient failures within each provider's supported limits. Stop retrying permanent missing tenants until the registry is corrected. Honor access restrictions; don't solve them with evasion. Record attempted_at on failures without changing last_success_at or claiming data freshness.

## 2. Repair the verified employer records

| Employer | Owner change | Acceptance check |
|---|---|---|
| Postman | Replace the obsolete Greenhouse registration with the current official careers page and Workday tenant/site. The current page exposes a public JSON cache, but that path is an implementation detail. | Compare current official IDs/count with the ingested candidate. The audit observed 38; don't hardcode that number into future tests. |
| Google DeepMind | Replace the former Greenhouse registration with the current Google Careers destination linked by DeepMind. Implement pagination or use a supported integration. | Collect all results, not just the first 20. The audit observed 74 matches; compare live identities at repair time. |
| Lindy | Refresh from the complete `/jobs` listing, not the featured homepage subset. Investigate why the published snapshot stopped advancing. | Both existing IDs remain; the six missing canonical URLs in the evidence are accounted for if still active. Preserve JobPosting datePosted. |
| Aizen | Verify the current employer-confirmed board before publishing a hiring claim. | Missing tenant is represented as source unavailable, not success/zero. |
| Regrello | Request or locate an employer-confirmed replacement; its own page also links to the dead board. | No assertion about company closure or missed count without current evidence. |
| SuperK | Map all 12 source Bangalore/India roles to the correct canonical location; restore publication dates where present. | No role points to Denver. Source IDs match; dates preserve Keka publishedOn semantics. |

Do not rewrite a valid empty board to manufacture jobs. Aftershoot and Plivo are regression controls.

## 3. Store one opening with multiple location relationships

Use a stable key such as `(employer_id, source_system, source_job_id)`. URL canonicalization is a fallback: remove location fragments and normalize known application suffixes while retaining semantically important query parameters. Keep alias relationships explicit for companies sharing one ATS board; a shared URL is not sufficient to merge legal entities automatically.

```text
job
  source_title, normalized_title, source_description_hash
  source_published_at, source_updated_at
  first_seen_at, last_seen_at, last_checked_at, last_success_at
  source_apply_url, source_location_text
  workplace_type, eligible_regions[]
  normalized_locations[]
  employer_salary {raw, currency, min, max, period}
  estimated_salary {value, model/provider, citations, confidence, generated_at}

location
  id, type: physical_office | job_location | remote_region | map_anchor
  country_code, region, city, coordinates
  evidence_url, observed_at, confidence, normalization_version
```

Enforce unique location IDs and valid foreign keys. Normalize Bangalore/Bengaluru as aliases, but do not treat a token such as CO as sufficient country/state evidence. Parentheses and remote-country separators need structured handling; don't split every `|` or dash into a physical office. Null/unresolved is better than a confidently wrong place.

Expose location type in the UI. A representative state-capital point must not be labeled a verified office address. Preserve source job titles as authoritative in application flows. An AI rewrite must not silently change seniority, specialization, or employer compensation.

## 4. Give dates explicit semantics

Never fill posted_date with a crawl timestamp. Greenhouse first_published, Ashby last publishedAt, Workday startDate, Keka publishedOn and Lever createdAt do not necessarily mean the same event. Document each connector's mapping. Keep unknowns null and show freshness independently from publication age.

When a job reappears, preserve first_seen and record the latest source event separately. A prior AI edit before a recorded publication date can reflect a repost, so use history and official source comparisons before labeling the date false.

## 5. Fix checkout and submission contracts

Validate both production Dodo listing product IDs before shipping. Inspect whether values were unset at build time or accesses were not statically inlined; public code proves the resulting undefined URL, not which source configuration error caused it. Prefer a validated server-created checkout session when appropriate.

Route company and alert forms through a first-party persistence endpoint with validation and an idempotency key. Return a durable ID and explicit accepted status. Queue notification delivery separately. The browser should confirm only accepted persistence, retain form data on failure and show a retryable error. Google Apps Script `no-cors` responses are opaque; testing response.ok on that opaque response is not a persistence contract.

Use one owner for success state and analytics. Check non-OK HTTP status explicitly; promise resolution alone is insufficient. Emit successful-submission events only after acknowledgement. A failed notification should not undo an already accepted submission.

Cache leadership data only after successful validated responses. Distinguish valid empty, failed and loading states, and retry non-OK HTTP responses. Network exceptions and HTTP error responses currently take different paths; test both.

## 6. Decide and enforce the public data boundary

If the full curated records require membership, build a deliberately limited public preview and serve complete records only after server authorization. Removing visible links in the client does not protect values already in public chunks. Review old deployed assets and caches; changing a filename does not retract copies already downloaded.

If these records are intentionally public, document that and keep user-specific information behind independent authorization. Do not frame expected public SDK identifiers as secret leaks. Inspect the notification key's actual authority, HTML text sinks, and replay masking with owner access. Escape plain text, sanitize intentional rich HTML, and verify sensitive-input masking using an owned test session.

## 7. Regression matrix

| Fixture or scenario | Required result |
|---|---|
| Valid board with zero jobs | valid_empty; no false source error |
| 200 HTML shell saying page not found | source_missing/invalid board; never successful empty |
| Source moved to another ATS | registry review/source_changed; no silent replacement with zero |
| 429, timeout, 5xx | bounded provider-appropriate retry; last good data retained and marked stale |
| Missing jobs component or malformed JSON | parse_failed with diagnostic evidence |
| Pagination beyond first page | all public listed IDs accounted for |
| Same count, different job ID | add/remove delta recorded, as in 100ms |
| One job in multiple locations | one canonical opening, explicit location rows |
| Ambiguous remote-country text | preserved eligibility; no fabricated physical office |
| Missing/duplicate location ID | validation fails before publication |
| Original date absent | null publication date; crawl timestamp remains separate |
| AI title/salary enrichment | source value retained; enriched value labeled/provenanced |
| Checkout ID absent | build/config failure or explicit disabled state; never /buy/undefined |
| Form 400/429/500/network error | no success state; entered data preserved |
| Durable form accepted, notification fails | accepted state with background retry |
| Leadership HTTP error then recovery | later retry succeeds; no permanent empty cache |
| Failed crawl with zero rows | source unavailable, not an unqualified NOT HIRING label |
| Inert HTML characters in source fields | rendered as text unless allowed sanitized markup |

## 8. Cadence and monitoring

Choose cadence using source limits, employer volatility and a measurable freshness promise. The inspected weekly/ten-day claims conflict; select one supported promise and measure source-to-published lag. A daily health check can be lighter than a full expensive enrichment run. Re-run enrichment only for changed inputs where possible.

Dashboard: attempt/success age, connector error rate, invalid empty transitions, pagination counts, pending source migrations, job-ID additions/removals, location validation failures, publication lag, paid checkout validity and acknowledged form conversion. Make the public snapshot carry a version ID and derive counters from that same version.

The existing local 09:00 monitor tracks only the public company index. It cannot substitute for owner-side source/job health monitoring or prove the internal schedule.
