# Employer-source verification for NextDoor.Company
Observed: 28 September 2026, approximately 08:25–08:39 UTC (13:55–14:09 IST).
Scope: fourteen employer sources (some sampled at one role or source availability), their public NextDoor static records, and official ATS documentation. This is a sample audit, not a claim about the remaining company catalog.

## Findings to show the founder

| Finding | Evidence | Practical consequence | Confidence |
|---|---|---|---|
| Postman's recorded source is obsolete | NextDoor points to Greenhouse and records 0 jobs with crawl_status=success; the old board responds 404. Postman's official careers page renders 38 roles, all linking to Workday. | An employer with dozens of advertised openings appears as having no roles in this public NextDoor snapshot. | High for present mismatch; inferred cause is stale source configuration. |
| All 12 SuperK roles reference the wrong country internally | Official Keka locations are CO-Bangalore, India. NextDoor displays Bengaluru, India but references denver_office, mapped to Denver, Colorado, United States. | Geographic filtering or map assignment using location_ids can be wrong. The underlying data inconsistency is proved; authenticated UI impact is not yet tested. | High |
| Posting dates are discarded for SuperK | Keka's public feed supplies publishedOn for all 12 roles. NextDoor has posted_date=null for all 12. | NextDoor cannot answer how old these jobs are even though the source supplies dates. | High for current field mismatch |
| Some original fields are overwritten or stale | Three SuperK titles differ; two are substantive changes, one is a spelling correction. AI-title metadata is present. The source also supplies salary amounts for several jobs where NextDoor's salary_range is null. | Users may see changed role meaning and less source information. | High for mismatch; source changes since NextDoor's crawl remain possible. |

## Postman: demonstrable source migration mismatch

NextDoor's observed public record:

- careers_url: https://job-boards.greenhouse.io/postman
- careers_url_last_updated: 2025-12-12T10:41:03.728Z
- total_roles: 0
- crawl_status: success
- source: Greenhouse Jobs
- crawl_method: automated+browser
- job_data.last_updated: 2026-09-26T18:08:16.770Z

A fresh anonymous browser loaded the [official Postman careers page](https://www.postman.com/company/careers/open-positions/) with HTTP 200. After client-side rendering, it displayed **38 open positions / 38 jobs found**, and contained 38 job links to postman.wd108.myworkdayjobs.com. This resolves the earlier ambiguity from a raw HTML/SSR-only fetch that contained no jobs.

The page requested this public JSON asset, which independently returned 38 jobs:

https://www.postman.com/_mk-www-next/api-cache/careers-jobs.json

The feed's metadata records total=38, source=workday_cxs, careersUrl=https://postman.wd108.myworkdayjobs.com/careers, and updated_at=2026-09-25T21:39:17.588Z. Its latest individual updated_at value is also 25 September. These are **update timestamps**, not established original posting dates.

The old Greenhouse URL returned **HTTP 404**, response dated Mon, 28 Sep 2026 08:27:04 GMT. We did not open every Workday job or establish the precise migration date. One public Workday job was subsequently verified below.

**Conclusion:** the present mismatch is confirmed. The likely cause is an obsolete board URL or connector failing to detect a move to Workday. The evidence does not prove precisely how the crawler converted that condition into success; its backend implementation and logs were unavailable. It is also possible that source conditions differed at the 26 September crawl. Either way, a successful-looking zero result is not reliable evidence that this employer has no jobs.

**Concrete fix:**

1. Update this employer's canonical careers URL to the employer's current official career page and register the observed Workday tenant/site.
2. For this employer, parse its currently published JSON feed or the same public listing surface used by its careers page. Treat the observed api-cache path as a vendor implementation detail with a monitored fallback, not a guaranteed third-party API contract.
3. Separate fetch status, parse status, source identity, and semantic validation. A 404 is source_missing, not a successful empty catalog. A changed ATS host is source_changed. A missing jobs component or invalid schema is parse_failed.
4. If a previously nonempty feed becomes empty, retain the last good snapshot as stale/verification pending until a source-specific empty-state check passes. An HTTP 200 by itself is insufficient.
5. Record original URL, final URL, HTTP status, parsed count, previous count, connector version, source hash, checked_at, last_success_at, and an error reason so the failure can be diagnosed immediately.

## SuperK: count is correct; locations and fields are not

The [official SuperK Keka page](https://superk.keka.com/careers) rendered 12 jobs, and all 12 source job IDs match the 12 NextDoor apply URLs. This is a positive control: the SuperK listing count and presence are useful in this sample.

The browser's own public listing feed is:

https://superk.keka.com/careers/api/embedjobs/default/active/53cf4854-a0f2-4488-bc66-eda9b4670bfb

It returned 12 published public job records. All have jobLocations containing city=Bangalore, countryName=India, and name=CO-Bangalore. NextDoor's 12 roles instead point to location_ids=[denver_office], despite their own location_display=Bengaluru, India. That location ID resolves to latitude 39.7392, longitude -104.9903, city Denver, country United States.

**Fix:** derive the canonical job location from structured ATS city/state/country values. Maintain Bangalore/Bengaluru as aliases for one city. Require the display text, country, and referenced location record to agree. If location normalization is uncertain, keep the original location text and leave the map location unresolved rather than choosing an unrelated office. Test specifically that these 12 IDs map to Bangalore/Bengaluru, India. Do not infer physical company offices merely from a remote job's eligible location.

### How old are the actual source jobs?

All 12 NextDoor posted_date fields are null. The employer source does provide publication timestamps:

| Public job | ID | Keka publishedOn (UTC date) | Source's publishedSinceDays |
|---|---:|---|---:|
| Sr. Associate/Associate - HR | 141229 | 2026-09-18 | 10 |
| Lead - Digital Marketing | 141768 | 2026-09-15 | 13 |
| Digital & CRM Executive | 141669 | 2026-09-15 | 13 |
| Creative Designer - Growth | 140821 | 2026-09-04 | 24 |
| Full Stack Developer | 19635 | 2026-08-24 | 35 |
| Category Manager - Food & Beverages | 137741 | 2026-08-14 | 45 |
| Catgeory Manager - Staples | 133631 | 2026-07-27 | 63 |
| Lead – Business Finance | 133580 | 2026-07-02 | 88 |
| Category Manager - F&V (Quick Commerce) | 128830 | 2026-05-13 | 138 |
| Category Lead | 127148 | 2026-04-29 | 152 |
| Financial Controller (Omni-Channel Retail) | 93565 | 2026-04-02 | 179 |
| Head of Marketing | 90100 | 2025-07-02 | 453 |

The newest Keka publication is about 10 days old; the oldest is about 15 months old. The oldest is still on the employer's active public feed, so age alone does not establish a closed or invalid listing. Publication can also change if an employer republishes a job.

NextDoor's SuperK snapshot says it was updated on 24 September at 10:22 UTC, about four days before this observation. That is the dataset crawl/update age, not the age of every job.

**Fix:** retain source_published_at separately from source_updated_at, first_seen_at, last_seen_at, last_checked_at, and last_success_at. Show source publication age when known, and label freshness separately. Do not populate posted_date with the crawl timestamp.

### Title and compensation quality

Three current source titles differ from NextDoor:

| ID | Current source | NextDoor | Interpretation |
|---:|---|---|---|
| 133631 | Catgeory Manager - Staples | Category Manager - Staples | Spelling correction |
| 128830 | Category Manager - F&V (Quick Commerce) | Category Lead - Fruits & Vegetables Operations | Changes Manager to Lead and rephrases scope |
| 127148 | Category Lead | Category Lead - Private Label Staples | Adds a specialization absent from the current source title |

NextDoor includes title_updated_by_ai=true and title_original metadata. The stored original for the latter two also differs from the current source, so the differences may combine AI normalization with later employer edits. We cannot identify the exact sequence without crawl history.

**Fix:** preserve the latest source title verbatim in source_title. Put a normalized title in a separate field, with transformation provenance. Make original job title authoritative in the application flow. Never silently change seniority.

The Keka feed additionally carries salary ranges absent from NextDoor salary_range. Examples: Lead - Digital Marketing has INR 2,500,000–3,500,000, and Digital & CRM Executive INR 400,000–800,000. The feed has mixed numeric salaryPeriod values, one tiny INR 12–18 range, and a zero range. Do not guess units or blindly publish all numeric values.

**Fix:** preserve original currency/amount/period/raw text, validate plausible values, and only normalize periods when their meaning is established. Keep source-provided salary separate from an AI market estimate. A null or invalid source salary is preferable to inventing a unit.

## Connector changes supported by official documentation

- **Greenhouse:** its [official Job Board API documentation](https://docs.greenhouse.io/job-board.html) states that public GET endpoints need no authentication. Listing provides stable IDs, URLs, locations, and updated_at; individual job records include first_published. Prefer this structured source over brittle page text when the employer actually uses Greenhouse. It does not fix a stale board identity by itself.
- **Keka:** its [official embed documentation](https://help.keka.com/hc/en-us/articles/39946782104721-How-to-Use-the-Embed-Code-for-Your-Career-Site-in-Keka-Hire) describes publishing job listings through career-site embeds. The SuperK public endpoint above was observed directly in the embed's browser traffic. Its URL/schema is not established as a stable documented API contract.
- **Private Keka API is different:** the [documented hire/jobs API](https://developers.keka.com/reference/get_v1-hire-jobs) uses OAuth2 and can return confidential and archived jobs as well as published jobs. It was not called and must not be treated as a public scrape replacement. A direct employer integration would require appropriate authorization and published-job filtering.

## Cadence: what we can and cannot establish

These snapshots establish latest recorded update times. They do **not** reveal a scheduler, the intended fetch interval, retry behavior, whether last_updated advances on a failed attempt, or whether a deploy delayed publishing.

A daily read-only monitor should retain each day's source and content hash, job IDs, job count, connector identity, and all reported timestamps. It can then measure observed changes and lags. It still cannot prove the backend cron frequency without server-side job configuration or run history.

For NextDoor's founder, the useful internal questions are: Which job last wrote each record? Which HTTP status and final URL did it see? What distinguishes a valid zero-job result from a failed fetch? Are AI-enriched fields revalidated when the source changes? Does the publication step use the same dataset as the authenticated API?

## Evidence and limitations

Structured source metadata and exact comparison fields are in [source-verification-evidence.json](./source-verification-evidence.json). Original observed NextDoor module files were nextdoor-company-module-superk.txt and nextdoor-company-module-postman.txt. The audit confirmed those two module hashes remained unchanged after the live deployment change. Other comparisons use records under inventory/companies.

No login, job application, employer contact, notification, or private-user-data endpoint was used. This document describes product/data quality findings. None establishes a security vulnerability or bounty eligibility.

## Additional live source verification

The initial sample below covers ten companies and six source families: Greenhouse, Keka, Workday, Ashby, Lever, and Kula. The later follow-up adds Lindy/Teamtailor, Google DeepMind/Google Careers, Plivo, and Regrello. Some checks verify one role or an empty state rather than a full employer count.

### Anthropic: false location and posting date

For [Anthropic Fellows Program, AI Safety & Security](https://job-boards.greenhouse.io/anthropic/jobs/5183044008), Greenhouse's public detail API reports first_published=2026-04-09T20:28:23-04:00 and updated_at=2026-09-18T03:03:59-04:00. NextDoor posted_date=2026-09-24 matches neither; it matches NextDoor's crawl date. The role was first published approximately 171 days earlier, not four days earlier.

The official source includes Remote-Friendly, United States and an office named Remote-Friendly US (Travel Required) with location=null. NextDoor displays Friendly, United States, creates friendly_office, and resolves that ID to a San Francisco address. This is a false locality/office identity.

The source department is AI Research & Engineering; NextDoor uses hr. The source's generic Location Type says On-Site even though job-specific text permits remote fellows in selected countries. Do not attribute that work-mode conflict solely to NextDoor.

**Fix:** parse remote eligibility separately from physical offices; never tokenize a hyphenated qualifier into a city. Preserve first_published separately from updated_at and crawl time. Exact backend parser code is unavailable.

### Additional geographic errors

| Employer / role | Employer source | NextDoor referenced location | Finding |
|---|---|---|---|
| Applied Intuition — Director of Government Affairs | Washington, D.C.; structured address Arlington, Virginia | washington_office → White Salmon, Washington (45.7289, -121.4865) | D.C. metro maps to Washington state |
| Atoms — Delivery Driver, ID8457904002 | Boston, Massachusetts in text and structured office | boston_office → Brooklyn, New York | Wrong city/state |
| Checkout.com — Analyst I, Merchant Configuration | Home-based, Mexico; structured city Ciudad de Mexico | home_office → London, United Kingdom | Remote qualifier maps to a different country's office |

Sources: [Applied role](https://jobs.ashbyhq.com/applied/96a7e0e1-37c6-4ee6-9cb6-dddfa48e87ed), [Atoms role](https://job-boards.greenhouse.io/cssmerge/jobs/8457904002), [Checkout.com role](https://jobs.ashbyhq.com/checkout.com/4ef4c78f-e913-403d-acca-c190fb1e8759). Exact ATS fields and NextDoor coordinates are in the evidence JSON.

Atoms' role has first_published=2026-03-10 and updated_at=2026-09-22; NextDoor posted_date=2026-09-24 matches neither. Checkout's last publishedAt is 8 September while NextDoor records 20 September. Applied's last publishedAt is 17 September while NextDoor records 22 August; that last difference could reflect a repost.

**Fix:** location identity must include locality, region, and country. Keep remote eligibility outside the office table. Reject source-country versus resolved-country conflicts. Job geography and company office geography need separate models.

### 1Password: 106 rows are not 106 unique postings

The live [1Password board](https://jobs.ashbyhq.com/1password) renders 64 open positions, matching its [public posting API](https://api.ashbyhq.com/posting-api/job-board/1password).

NextDoor's 106 rows contain **61 distinct ashby_job_id values**; 90 row URLs have #loc-N fragments. Many postings expand into location-specific rows. Canonical ID comparison yields 56 shared, 5 NextDoor-only, and 8 current-source-only. This is drift, not evidence that all 106 records are stale or that 42 jobs closed. NextDoor reports an 18 September crawl and crawl_method=selective_scrape; its selection policy is unknown, and one absent source item is a Future Opportunities pipeline. Several current roles were published later. Individual closure pages were not checked for all five absent IDs.

The source location Remote (United States | Canada) becomes malformed strings Remote (United States and Canada). The US row references ten cities, and the Canadian row Toronto, even though broad remote-country eligibility does not establish a physical job office in those cities.

**Fix:** store one posting with location eligibility as an array. If the UI expands locations, label/count those rows separately. Deduplicate by ATS ID; strip URL fragments and normalize application suffixes when falling back to URLs. Prefer structured locations over punctuation splitting.

The newest source publishedAt is 25 September 2026 at 23:14 UTC, about 2.4 days before observation. Per [Ashby's official docs](https://developers.ashbyhq.com/docs/public-job-posting-api), this means last published, not first-ever posted. Filter isListed=false from public lists. The API also provides workplaceType and optional compensation.

### 100ms: unchanged count hides a job change

The [100ms Lever feed](https://api.lever.co/v0/postings/100ms?mode=json) and NextDoor both contain nine jobs, but only eight IDs match. Security and Compliance Lead, ID c9c30415-77d2-4610-8455-9c18a3c0068a, appears only in NextDoor. Sales Development Representative - US Healthcare (India, US Hours), ID 97578a15-8f09-4dc1-af39-75a05a164e2d, appears only in the current feed. NextDoor reports 14 September as its last update.

**Fix:** compare ID sets and per-job hashes, not only totals. Lever createdAt must not automatically be relabeled as publication time. Its [official public-posting documentation](https://github.com/lever/postings-api) supplies pagination, IDs, location, workplace, and salary fields.

### Zero jobs: missing board versus healthy empty board

**Aizen:** its [configured Ashby board](https://jobs.ashbyhq.com/aizen) serves an HTTP 200 app shell but renders Page not found. The public posting API returns 404. NextDoor records zero jobs/success on 26 September. Current source validity is broken; no alternate openings or missed-job count was established.

**Aftershoot:** its [Kula page](https://careers.kula.ai/aftershoot) returns HTTP 200 and explicitly renders No jobs found. That is a valid empty-state control consistent with NextDoor's zero. No failure is inferred.

**Fix:** distinguish a known board's explicit empty state from missing tenants, JavaScript shells, access challenges, and parse failures.

### Postman: actual publication age confirmed

The public [Senior Engineer - AI Workday job](https://postman.wd108.myworkdayjobs.com/careers/job/Bangalore-India/Senior-Engineer---AI_JR1000054) displays Posted 3 Days Ago, requisition JR1000054, Bangalore. The public JSON requested by the page supplies startDate=2026-09-25 and postedOn=Posted 3 Days Ago. A current role roughly three days old is absent from NextDoor's zero-job snapshot. No application was started.

### Hypothesis rejected

The suggestion that Atoms' cssmerge board belongs to an unrelated business is unsupported. Current [atoms.co](https://atoms.co/) describes a physical-automation group including CloudKitchens, Otter and Picnic, consistent with the board. It is not the shoe brand in this observation. Keep the verified mapping error; do not report a company-identity mismatch.

## Staleness and migration follow-up

### Lindy: six current jobs missing from a roughly 52-day-old snapshot

The dedicated [Lindy jobs page](https://careers.lindy.ai/jobs) currently lists **eight jobs**. Its homepage shows only five featured roles, so a homepage-only scrape would still undercount the employer.

NextDoor records two roles and last_updated=2026-08-07T11:45:50.397Z, roughly 52 days before the observation. Both recorded jobs are still on the employer's list; six current canonical job URLs are missing:

- Senior Software Engineer
- Senior Engineering Manager
- Head of Engineering
- Growth Product Manager
- Full Stack Software Engineer (Early Career)
- Staff Software Engineer

The missing [Senior Software Engineer](https://careers.lindy.ai/jobs/689900-senior-software-engineer) page's JobPosting JSON-LD contains datePosted=2026-08-27T15:10:09-07:00, approximately 32 days before observation. This is a confirmed missing role with source publication metadata, not just an old crawl timestamp. Full exact URLs are in the evidence JSON.

**Confidence:** high for current count, six missing IDs, and recorded age; exact cause of the stalled refresh is unknown.

**Fix:** use the full /jobs listing with its count/pagination controls, not the featured homepage subset. Alert when last_success_at exceeds the allowed age regardless of a historic success label; queue the employer for retry or connector review. Preserve useful JobPosting structured metadata before HTML text extraction. Investigate whether this company was skipped, its fetch failed, or publishing stopped using current data.

### Google DeepMind: second confirmed change of job platform

The official [Google DeepMind careers page](https://deepmind.google/careers/) sends View open roles to [Google Careers filtered to DeepMind](https://www.google.com/about/careers/applications/jobs/results?company=DeepMind). A fresh anonymous browser returned HTTP 200, showed **74 jobs matched**, and showed the first 20 of 74 results.

NextDoor still points at job-boards.greenhouse.io/deepmind, has zero jobs, crawl_status=success, and last_updated=2026-09-14T12:56:03.387Z. The coordinator's direct GET check confirmed the former board returns 404. We did not fetch all 74 role details.

**Confidence:** high for source migration mismatch and the current official count.

**Fix:** replace the obsolete board with the source linked by the employer. For custom career platforms, record the actual source identity and validate rendered results/pagination instead of reusing a Greenhouse connector. Revalidate board links periodically and on unexpected empty results.

### Plivo: a 404 hosted board does not prove lost jobs

Plivo's [own careers page](https://www.plivo.com/jobs/) renders zero roles with no location/department filters applied. The browser itself requests [Lever's public JSON feed](https://api.lever.co/v0/postings/plivo?mode=json), which returns **HTTP 200 and an empty array**; a separate read confirmed this at 08:38 UTC. This agrees with NextDoor's current zero count, despite the hosted Lever board returning 404.

**Confidence:** high that the observed employer page and public feed are empty. No missed jobs or migration is proved.

**Fix:** use the actual employer feed and its semantics. Keep hosted-page reachability distinct from feed validity. Do not mark all HTTP 404 board links as job-loss findings without this cross-check.

### Regrello: broken official link, no verified replacement

Regrello's [official careers page](https://www.regrello.com/careers) still links Explore open roles to jobs.lever.co/regrello, which returns 404. NextDoor uses that same URL and records zero roles.

**Confidence:** high for the broken link; replacement source and current openings are unknown. There is no basis here to claim the company is closed or quantify lost jobs.

**Fix:** mark source verification required and seek a current employer-confirmed listing destination. Avoid silently converting source failure into a statement about hiring activity.

## Cross-check coverage and limits

Fourteen companies were inspected at differing depths. Postman, SuperK, 1Password, 100ms, Lindy and DeepMind had current counts or full public listing metadata compared; Anthropic, Applied Intuition, Atoms and Checkout.com had targeted role metadata compared; Aizen, Aftershoot, Plivo and Regrello supplied source-validity/empty-state controls.

The sample does not establish a global job-error rate, an exact internal cron interval, the accuracy of every company's funding or founder details, or behavior of authenticated NextDoor APIs. The public evidence is enough to prioritize connector refresh, timestamp semantics, canonical job counting, location validation, and freshness monitoring.
