# NextDoor.Company: public frontend and API review

Observed 28 September 2026. This review found four reproducible product defects in the shipped frontend: paid company-listing buttons construct an undefined product URL; free company submissions can report success after both delivery requests fail; job-alert signup reports success after HTTP or network errors; and a failed founder lookup is cached as an empty result. These are stronger founder-facing fixes than an unqualified vulnerability claim.

The public static company-data path is also confirmed by the earlier review. Several security and privacy issues need owner verification before their impact can be established. No notifications, signups, applications, payments, private-account requests, or external reports were sent during this review.

## Evidence and scope

Read and searched the retained public homepage, intro, login, company redirect, job redirect, and their first-party bundles. Directly inspected the relevant request handlers, preview loader, cache, HTML renderer, version checker, and analytics setup. All literal first-party `/api/` references in this retained corpus were inventoried. This is not a review of the complete authenticated application or server source; library internals and every visual component were not read line by line.

The homepage changed deployments during the review. The earlier capture referenced `dpl_H7ZzEn2SQQ8KinUn6moQXkiZxe4v`; a fresh homepage referenced `dpl_61q2eRds91tsmLHyLviEXEzLfxWA`. Relevant changed bundles were fetched again. The layout, listing form, company HTML renderer, leadership cache, and free-access bundles retained the same content-hashed paths. The current signup parent and child callbacks were used in the offline tests.

Machine-readable evidence, source URLs, local hashes, offsets, and test results are in [frontend-evidence.json](./frontend-evidence.json). The reproducible, network-free tests are in [frontend-repros/run.mjs](./frontend-repros/run.mjs), with [instructions](./frontend-repros/README.md) and [captured results](./frontend-repros/results.json). The retained listing source had already been credential-redacted; its local hash is explicitly labeled as a hash of redacted evidence.

## Highest-confidence product fixes

| Priority | Issue | Proof | Practical effect |
| --- | --- | --- | --- |
| 1 | Paid company checkout product ID is undefined | Original checkout builder + actual browser process modules evaluated locally | Both paid plans construct `/buy/undefined?quantity=1` |
| 1 | Free company submission reports success after failure | Both fetches mocked to reject; repeated with HTTP 503 | Founder can lose submitted leads while customer sees success |
| 1 | Job-alert signup reports success after failure | Current parent and child handlers tested with HTTP 500, network rejection, and HTTP 200 control | False confirmation and inflated successful-submission analytics |
| 2 | Failed leadership lookup cached as empty | First response 503; second attempt never fetches again | Founder details stay missing until module/browser state resets |

### 1. Both paid company-listing plans construct an invalid checkout URL

In [listing bundle 51563](https://www.nextdoor.company/_next/static/chunks/51563-d17f6911d2f6dfdf.js), module 94840 reads these browser environment values:

```text
NEXT_PUBLIC_DODO_PAYMENTS_ADD_COMPANY_SUBSCRIPTION_GROWTH_PRODUCT_ID
NEXT_PUBLIC_DODO_PAYMENTS_ADD_COMPANY_ONETIME_PRODUCT_ID
```

It concatenates the selected value into `https://checkout.dodopayments.com/buy/{value}?quantity=1`. The current [framework bundle](https://www.nextdoor.company/_next/static/chunks/81348-125864d88bdda329.js), modules 68867 and 29596, resolves to a browser process object with an empty `env`. Evaluating those actual modules and the original builder produced this for **both** plans:

```text
https://checkout.dodopayments.com/buy/undefined?quantity=1
```

No payment page was opened and no checkout was created. This proves the shipped code's URL construction in the ordinary browser environment; it does not claim a payment provider response was tested.

**Fix:** Set and validate both product IDs in the production build environment. Use a statically analyzable `process.env.NEXT_PUBLIC_...` access or have the server create a checkout session. Reject a missing ID before opening a tab and present a useful error. The public bundle cannot distinguish an unset build variable from a source access pattern that prevented inlining, so inspect both. Next.js documents that browser environment values are embedded at build time and dynamic environment lookups are not inlined. [Next.js environment variables](https://nextjs.org/docs/app/guides/environment-variables).

**Acceptance:** Build the production artifact, exercise both plan URL builders without navigation, and require a configured product identifier rather than `undefined`, an empty string, or a placeholder.

### 2. Free company submissions can fail completely and still show success

The same listing handler stores the form in browser storage, records `company_listing_free_submitted`, sends a `no-cors` Google Apps Script request, and sends a notification request. Both requests have separate catches that only log errors. The notification request does not inspect its HTTP status. After either or both fail, the code still sets success state and invokes `onCompanySubmitted`.

The offline reproduction supplied synthetic company details and made both fetches throw. It still observed `success: true` and the submitted callback. A second run with error HTTP responses produced the same result. This is a control-flow defect; no claim is made that any specific customer's submission was actually lost.

**Fix:** Persist the submission once through a first-party server endpoint and return a durable submission ID. Confirm success only after that response. Send notifications asynchronously after persistence, with retries and failure monitoring, rather than treating a notification as the database. Preserve the entered form and show retryable errors when persistence fails. Record successful-submission analytics after confirmed persistence.

The direct Apps Script response is opaque under `no-cors`; frontend code cannot inspect its body or response headers. Simply adding `response.ok` to that opaque response is not a fix. [MDN request mode](https://developer.mozilla.org/en-US/docs/Web/API/Request/mode).

**Acceptance:** Simulate network failure, 400 validation error, 429, 500, notification-only failure, and successful durable write. Only durable write should confirm acceptance; notification failure should not discard an already accepted application.

### 3. Desktop job-alert signup reports success after server or network failure

The current [homepage parent handler](https://www.nextdoor.company/_next/static/chunks/36340-b746d71e2b4461c9.js) posts to `/api/email-signup`. On a non-OK response it simply resolves; on a network error it logs and also resolves. The current [modal child handler](https://www.nextdoor.company/_next/static/chunks/71727-c70de6767316cd1a.js) awaits that parent and, because it did not throw, sets success, clears anonymous form fields, and records `job_alert_signup_submitted`.

Tests using the original handlers reproduced that success state for HTTP 500 and network rejection. A 200 control also succeeded and additionally triggered the parent success event and close action. The defect can mislead the applicant and contaminate conversion metrics.

**Fix:** Return an explicit accepted result or throw from the parent on every failed response. Check the endpoint's success schema, not merely promise resolution. Have one component own success state and analytics. Keep the form values on error. Fetch does not reject automatically for error HTTP statuses, so those must be checked explicitly. [MDN Fetch behavior](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).

The mobile/legacy intro path submits job alerts directly to a different Google Apps Script receiver with `no-cors`. It cannot verify server persistence either. Consolidating both frontend variants behind the same first-party response contract would remove this difference.

### 4. A failed founder request becomes a permanent empty result for the loaded module

[Bundle 18067](https://www.nextdoor.company/_next/static/chunks/18067-c3c16e46a0af0f3d.js), module 61639, caches leadership data by company ID. For any non-OK HTTP response it substitutes `{founders: []}` and then caches that array. An empty array is truthy, so later calls immediately return it. The module has no observed TTL or invalidation for this cache.

An offline test configured a 503 first response and a successful founder response on the next fetch. Two load attempts returned empty arrays with only one fetch call. Network exceptions follow a different path and do not populate this cache; the reproduced fault is specifically non-OK HTTP handling.

**Fix:** Cache valid successful responses only. Represent unavailable, loading, legitimately empty, and failed states separately. Allow a bounded retry and clear/version the cache when authentication or the data version changes. Include the company slug/data version in identity if company IDs are not stable across datasets.

## Public and protected data surfaces

The earlier review verified `/api/discover-map-data` and `/api/company-leadership` return 401 anonymously, while targeted public company JavaScript modules return detailed records. The homepage's loader index exposes the company-module map. Its preview selects ten datasets, gives other markers masked labels, and disables links in the client. Those controls do not remove the original records from the public static files.

The static sample response uses `Cache-Control: public,max-age=31536000,immutable`. Public availability is established; whether it violates the product's intended data policy is still an owner decision. Do not describe it as customer-data exposure or a proven paid entitlement bypass. See the prior [catalog finding](./public-data-boundary.md).

**Fix if the data is meant to require membership:** Generate an explicitly limited preview dataset and serve full records through a server authorization check. Exclude restricted fields from client imports and static build artifacts. Identify and remove previously published restricted artifacts through the hosting provider where possible. Anything already fetched by a public client must be treated as previously public.

**Fix if the data is intentionally public:** Make that product decision explicit and protect account-specific information separately; the login UI should not imply confidentiality that the data architecture does not provide.

### First-party API inventory

Statuses below are the minimal anonymous checks retained from earlier on 28 September. Uninvoked writes are only observed frontend references. This inventory is complete for literal API references found in the inspected public corpus, not all backend routes.

| Method | Route | Purpose | Anonymous evidence |
| --- | --- | --- | --- |
| GET | `/api/company/{slug}` | Company redirect metadata | 200 for `superk` |
| POST | `/api/job-leads-companies` | Details for supplied public slugs | 200 for `superk`; read operation |
| GET | `/api/auth/check` | Authentication status | 200, false |
| GET | `/api/user/profile` | Current profile | 401 |
| GET | `/api/app-version` | Data/code version | 200 |
| GET | `/api/detect-location` | Location/currency choice | 200 |
| POST | `/api/auth/sign-in` | Google/LinkedIn OAuth start | Uninvoked |
| POST | `/api/job-leads-accessed` | Record viewed lead | Uninvoked |
| GET | `/api/white-glove-jd?slug=…` | Advertised job description | 200 for one known role |
| POST | `/api/apply-to-hvt` | Resume/application | Uninvoked |
| POST | `/api/send-company-listing-notification` | Company-listing notification | Uninvoked |
| GET | `/api/discover-map-data` | Discovery directory | 401 |
| GET | `/api/company-leadership?id=…&slug=…` | Founder profiles | 401 for known public company |
| GET | `/api/company/{slug}/role/{roleSlug}` | Job redirect metadata | Old Atlan example 404 |
| GET | `/api/get-user-country` | Country lookup | Uninvoked |
| GET | `/api/ph-upvotes` | Product Hunt count | Uninvoked |
| POST | `/api/email-signup` | Job-alert signup | Uninvoked |

The discovery loader also reads `X-Account-Status`, `X-Subscription-Type`, and `X-Subscription-End-Date` response headers. Their presence is architecture information, not evidence of a bypass. The browser Supabase client reads `users` with `.select('*').eq('id', userId).single()`; server grants and RLS were not inspected or queried.

Public UI routes include `/`, `/intro`, `/login`, `/is/{slug}`, and `/is/{slug}/{roleSlug}`. Navigation also references `/discover`, `/job-tracker`, `/resume-builder`, and `/upgrade`. Earlier anonymous `/discover`, `/robots.txt`, `/sitemap.xml`, and `/.well-known/security.txt` all redirected to `/login`; the last three therefore did not serve their usual public purposes.

## Refresh cadence, caching, and failure presentation

**The actual scraper schedule is not visible in this frontend.** Two product claims disagree: the current feature list says job openings are updated weekly; the tracker tips say jobs are updated every ten days. Company-listing copy promises careers-page synchronization. These are claims, not execution logs or a cron schedule.

The app separately polls `/api/app-version` every **15 minutes** (`900000 ms`), on focus, and when the document becomes visible. Its route predicate covers discovery, job tracking, and resume building. It compares version/dataVersion/codeVersion against browser storage and can offer an app refresh or data refresh. This is a UI version check, not a scrape. User-profile caching in the shared auth helper lasts 60 seconds and uses an 8-second fallback timeout; leadership caching is a different mechanism described above.

The current feature bundle embeds **22,579 jobs and 460 companies**; the earlier bundle embedded 22,689 and 460. These are build-time counters in the inspected code, not fresh aggregate API results. The changed deployment and counter show publication changed during observation; they do not establish when any individual job was last checked.

Specifically, module 15644 in current bundle 80969 exports those two numeric constants; root bundle 36340 imports that module and renders `f.P4` / `f.D9` directly. The hero also assigns `eu=f.P4, ey=f.D9`. The exact source excerpts are retained in the evidence JSON.

The company details UI labels data with `job_data.last_updated || company_basic_information.last_updated`. That fallback combines two different freshness concepts. It also labels a company actively hiring when its stored role count is positive and a careers URL is present; otherwise it labels it not hiring. There is no `crawl_status` check in that banner condition. If a failed crawl is published as zero roles, that renderer can turn a retrieval failure into an apparent hiring status. Whether the ingestion system actually publishes zero in that circumstance must be verified against the data pipeline.

**Fix:** Define and expose `last_attempt_at`, `last_success_at`, `source_published_at`, and `next_scheduled_at` separately. Preserve last-known-good jobs after failed collection. Mark unknown/stale states explicitly, and show hiring status from successful recent evidence. Derive the aggregate counts and freshness label from the same published snapshot. Align the marketing cadence with the measured service level.

### Old deployment assets and swallowed preview errors

The earlier framework asset `81348-a7f886a831f75d0e.js` now returned 404 both with and without the original `?dpl=dpl_H7ZzEn2SQQ8KinUn6moQXkiZxe4v` query. Its current replacement returned 200. The current homepage and all newly requested current bundles returned 200; this does not demonstrate a current site-wide outage.

Separately, the preview's ten-company dynamic loader uses `try/catch` with an empty catch around each import. Failed imports therefore reduce the loaded preview records without a user-visible retry or diagnostic. The observed old asset unavailability makes deployment skew a credible failure scenario for a stale page, but a live stale-session failure was not reproduced.

**Fix:** Handle `ChunkLoadError` with one controlled refresh/retry, keep a deployment/version boundary for loaded data, and show a recoverable failure state. Preserve old assets for the intended session lifetime if supported by the hosting configuration. A monitoring client must read the current homepage/index/runtime on every run instead of retaining old content hashes indefinitely.

### Other inspected failure paths

The job and company redirect pages treat all non-OK responses and network exceptions as “not found”; transient server failures are therefore indistinguishable from a genuinely removed role. The job redirect defaults to a 20-second countdown and provides a manual link. Retain a true 404 state, but use a retryable service-error state for 429/5xx/network failures and abort outdated requests after the route changes.

The homepage location lookup has a three-second fallback and ignores a response arriving after the fallback has won. That explains a visitor seeing a default region on a slow connection; it is deliberate current control flow, not an established geolocation defect. The evidence cannot establish country-detection accuracy without owned cross-region tests.

### Source metadata and transformations visible in the browser

The browser consumes pre-enriched company files. In module 4269, it builds lookup maps from `city_canonical`, `country_canonical`, `department_categories`, role `department_category`, `location_display_normalized`, `industry_domains_classified`, and `industry_domain_buckets`. Missing entries fall back to the original location text, the `other` department, or no industry bucket. These are display/filter normalization steps, not evidence of the scraper or AI enrichment running in the browser.

The company renderer explicitly omits benefit keys beginning with `_` and `benefits_scraping_source` from visible benefit rows. It displays a general beta accuracy caveat. No Perplexity or SearchAPI request is made by this renderer; their names in company datasets describe upstream provenance. The actual upstream prompts, retrieval settings, verification rules, and scheduler remain unavailable.

The homepage also contains a separate fixed Figma demo fixture, with placeholder links and a February 2026 date, plus synthetic job-tracker examples. Do not mix these marketing-demo fixtures into the measured 460-company catalog or use their dates as evidence of real listing freshness.

### Representative locations are presented with office terminology

The data review found `state_capital_representative` provenance for Databricks' `queensland_office` record: a Brisbane point and a city/state/country address stand in for the broader Queensland job location. The normalized inventory preserves the address in `locations` and the source at `provenance['location_mapping[110].location_source']`. [Databricks inventory](./inventory/companies/databricks.json).

The renderer labels that field **Office address** and groups locations under **Office network (i.e. hiring in N locations)**. The job-leads modal also says **Hiring in N office locations**. An offline synthetic fixture using this public representative-location shape confirmed that the renderer displays the office labels and representative address while omitting `location_source`. This does not verify where Databricks actually has an office; it demonstrates that the UI loses the distinction its own data records.

**Fix:** Distinguish verified workplaces, hiring regions, and representative map points. A state/country/remote eligibility area should not imply a physical workplace or a commute estimate. Show an explicit approximation label where points stand in for regions, and count unique source jobs separately from expanded location rows. Use “hiring locations” unless a physical office is verified.

## Security and privacy review items

### Raw data enters an HTML string and then `innerHTML`

The company renderer concatenates company names, descriptions, and job text into HTML. The sidebar assigns its result to `innerHTML`. A local synthetic fixture containing an inert `<b>` marker appeared twice unescaped in the output. No HTML was sent to production, no script was executed, and no attacker-controlled production ingest path was established.

**Validity:** Missing output escaping at these sinks is reproduced. **Security severity:** Unassigned pending a controllable source path and ingestion behavior. **Payout odds:** Unknown. **Dismissal risk:** High for an XSS report without persistence/control proof. **Priority:** Owner code review now; hold a vulnerability claim.

**Fix:** Render text through React/textContent, validate `http`/`https` links, and sanitize intentional rich HTML with an allowlist. Inspect every scraped or AI-produced field before assuming it is trustworthy. Do not rely on manual curation as the only sink protection. An owner-controlled staging fixture is sufficient to verify the fix without publishing a live payload.

### Notification key exposed in the client

The listing form includes a fixed `x-api-key` value. The value is redacted in the retained repro and was never replayed. It cannot be a secret from the client that uses it, but its server authority remains unknown.

**Validity:** Exposure of a client value is established; unauthorized privilege is not. **Severity:** Unassigned. **Payout:** Unknown. **Dismissal risk:** High without meaningful impact. **Priority:** Hold; owner should inspect server handling and abuse controls. If privileged, rotate and move it server-side. If it merely identifies a public form, use explicit public-form validation, recipient restrictions, throttling, and idempotency.

### Recording configuration deserves review around personal data

The shared layout configures PostHog `maskAllInputs: false`, with password masking enabled but email, telephone, text, textarea, select, and other input types unmasked. Session recording is disabled at initialization, then explicitly started for authenticated users; anonymous sampling is controlled through a feature flag. The layout also identifies users with email and, when present, name, phone number, account status, and LinkedIn-related profile fields. Microsoft Clarity is initialized and identified as well.

This establishes the shipped configuration, not the exact production recordings or remote project settings. Do not describe it as proven leakage or a legal violation. The recorder component has no explicit sign-out stop branch, although other code resets PostHog identity; actual SDK behavior after sign-out needs owner verification.

**Fix:** Mask inputs by default and block application/resume/free-access forms from replay unless a documented need justifies capture. Minimize analytics event properties, verify recording retention/access controls, and inspect an owned test session for masking. PostHog supports masking text, inputs, and complete elements before recording. [PostHog Session Replay](https://posthog.com/docs/session-replay).

### Free-access video hostname validation accepts lookalike domains

The free-access frontend classifies URLs using `hostname.includes('instagram.com')` and the equivalent TikTok check. Local tests accepted `https://instagram.com.example.invalid/reel/owned-fixture/` and a corresponding TikTok lookalike as valid platform video links. This is a frontend validation defect, not proof of a granted subscription or server-side fetch vulnerability.

**Fix:** Require the exact allowed hostname or a dot-delimited subdomain, enforce HTTPS, and repeat validation server-side. If a backend fetches supplied links, independently constrain destinations and redirects there. Review submissions manually until the actual granting workflow is verified.

### Public integrations visible in the inspected frontend

| Integration | Observed role | Limits |
| --- | --- | --- |
| `zgnnobaelrlglfmspker.supabase.co` | Browser auth; own-profile query | No database reads or RLS testing performed; public anon key alone is expected |
| `us.i.posthog.com` | Product analytics and session replay | Configuration inspected; captured contents not accessed |
| `www.clarity.ms` | Microsoft Clarity loader | Identifier setup inspected; project settings unknown |
| `www.googletagmanager.com` | Google Analytics loader | Loading reference only |
| Mapbox, including `api.mapbox.com` | Map SDK and custom style | Public browser map token omitted; public token is not itself a secret leak |
| `script.google.com` | Four distinct Apps Script form receivers: company listing, legacy job alerts, white-glove details, free-access video submission | No receiver invoked; persistence/access controls unknown |
| `checkout.dodopayments.com` | Paid company-listing checkout | URL construction tested only |
| Razorpay / Dodo Payments | Pricing configuration names India and international gateways | Authenticated purchase flows not inspected |
| `cdn.jsdelivr.net` | Phosphor icon styles | Dependency reference only |
| YouTube and image hosts | Marketing video and music player | Public media references |
| LinkedIn, Instagram, X, Product Hunt, LinkToDM | Social, proof, traffic, and lead-distribution links | Links are not evidence of scraping integrations |
| `reallygood.cv`, `topfloor.company`, Gumroad | Related product or promotional navigation | No account relationship inferred |

The third-party SDK's own `/api/surveys`, early-access, and experiment URLs belong to PostHog, not NextDoor.Company's first-party API inventory. Similarly, a company called Firecrawl in the catalog is not evidence that Firecrawl powers their scraping.

## What the founder must supply to settle the remaining questions

The public frontend cannot reveal the scraper's cron expression, actual run history, retry logic, hosting job limits, parser failures, per-source rate limits, or why a backend job failed. A version poll, a deployment timestamp, and a job's update timestamp are different clocks.

For a conclusive operations review, inspect the scheduler configuration; the last several crawl-run summaries by source; last-attempt and last-success state; failure/zero-result safeguards; the promotion job that creates the frontend snapshot; source job-ID and expiry logic; webhook delivery/persistence logs; production build environment validation; and authorization/RLS definitions. These checks should use owner access and staging fixtures, not guessed private endpoints.

The present evidence supports concrete frontend fixes and targeted owner investigation. No exploitable account takeover, cross-user data access, live stored XSS, unauthorized payment action, or verified notification abuse has been established.
