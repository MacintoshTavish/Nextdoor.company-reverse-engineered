# Public inventory: source, freshness, and data-quality review

Observed 2026-09-28. Parsed **460/460** current-index company modules, containing **22,579 job rows**. Coverage of the inspected frontend company index is complete.

This is a complete analysis of the collected normalized records, not the unpublished database or scraper code. Source labels and timestamps are publisher-provided metadata. Remote-job expansion can intentionally produce multiple rows or city associations. A zero-job result alone does not establish a broken scraper.

The 22,579 job rows resolve to 21,478 distinct canonical application URLs when counted within each company. **Rows are not unique openings**: for example, one upstream posting may be expanded into `#loc-0` and `#loc-1` records. Canonical URL count is a useful proxy, not guaranteed unique-posting truth.

Ages use the analysis-time reference `2026-09-28T08:39:25.592273+00:00`; collection timestamps are stored per module.

Deployment: `dpl_61q2eRds91tsmLHyLviEXEzLfxWA`. Index source: https://www.nextdoor.company/_next/static/chunks/14401-24a4271828265f87.js.

## Key measured facts

- Sources: 35 distinct recorded job-source labels; 127 careers hostnames; 137 application hostnames.
- Crawl status: success: 460.
- Zero jobs: 23 companies, including 23 marked `success`. Verify against the employer before calling these extraction failures.
- Refresh age in days: {"n": 460, "min": 0.111, "median": 9.687, "p90": 13.941, "max": 140.931}. A refresh timestamp is not an employer's publication date.
- Refresh older than 10 days: 158 companies; older than 30 days: 6.
- Valid recorded `posted_date`: 19,732/22,579; missing/invalid: 2,847.
- 11,715 rows have a recorded posted date matching the company refresh day; all rows do so at 158 companies.
- 311 rows have title-enrichment timestamps earlier than their recorded posted day. This undermines treating `posted_date` as first publication, although reposting can explain individual cases.
- 885 rows have `title_updated_by_ai=true`; 800 differ from `title_original`.
- 28 rows carry salary estimates; 587 carry nonempty `salary_range`. Estimates must not be represented as employer offers.
- 1 salary estimate(s) contain non-URL citations; Sarvam AI is the observed example. Citation identifiers require resolution before they can substantiate a user-facing number.
- 11 rows refer to absent location IDs. There are 621 additional narrowly detected city-name mismatch candidates; aliases/regions require manual review.
- 36 rows with one displayed country point to locations in other countries. Including multi-country eligibility records with incomplete references, the broader country-inclusion candidate set has 63 rows; every case is retained for review.
- `show_on_map`: {"True": 460}. Presence in the frontend index does not imply visibility on the map.

## Complete recorded job-source inventory

| Recorded source | Companies | Job rows | Zero-job companies | Median refresh age (days) |
|---|---:|---:|---:|---:|
| Ashby Jobs Board | 144 | 9,247 | 3 | 9.707 |
| Greenhouse Jobs | 90 | 7,626 | 4 | 8.139 |
| Lever Jobs Board | 39 | 979 | 3 | 9.696 |
| Keka ATS | 32 | 645 | 1 | 7.664 |
| Kula ATS | 22 | 498 | 2 | 9.692 |
| Darwinbox | 21 | 484 | 1 | 8.653 |
| Y Combinator Jobs | 15 | 137 | 2 | 9.695 |
| Freshteam Jobs | 11 | 137 | 3 | 3.925 |
| Workable | 10 | 347 | 1 | 7.161 |
| Comeet Jobs | 8 | 350 | 0 | 9.171 |
| Workday | 7 | 385 | 1 | 9.69 |
| SmartRecruiters | 6 | 782 | 0 | 9.687 |
| Trakstar | 6 | 72 | 0 | 9.17 |
| BambooHR | 4 | 55 | 0 | 3.916 |
| PyjamHR ATS | 4 | 39 | 0 | 6.672 |
| Reczee | 4 | 14 | 1 | 4.319 |
| Rippling | 4 | 57 | 0 | 12.214 |
| Gem Jobs | 3 | 31 | 0 | 1.599 |
| MyNextHire ATS | 3 | 43 | 0 | 13.81 |
| Recruitee | 3 | 103 | 0 | 11.608 |
| Teamtailor | 3 | 31 | 0 | 51.871 |
| TurboHire | 3 | 80 | 1 | 8.651 |
| WordPress Jobs | 3 | 28 | 0 | 3.922 |
| Jobvite | 2 | 32 | 0 | 6.188 |
| SAP ATS | 2 | 120 | 0 | 3.917 |
| ZohoRecruit | 2 | 38 | 0 | 128.701 |
| Custom ATS (TestZeus) | 1 | 3 | 0 | 1.598 |
| Custom Ashby Embed | 1 | 133 | 0 | 13.971 |
| Deel | 1 | 5 | 0 | 12.821 |
| Freshteam | 1 | 1 | 0 | 4.627 |
| JazzHR | 1 | 11 | 0 | 9.688 |
| Manatal | 1 | 10 | 0 | 8.649 |
| RippleHire | 1 | 6 | 0 | 9.691 |
| Scout ATS | 1 | 18 | 0 | 8.655 |
| SenseHQ | 1 | 32 | 0 | 3.905 |

Crawl methods: `automated+browser` (327 companies); `selective_scrape` (125 companies); `api` (4 companies); `automated+api` (4 companies).

These labels identify the recorded job source, not how the original company universe was selected. Career URLs, every company/source mapping, application-host inventories, provenance labels, and citation-host inventories are in `inventory/analysis.json`.

## Refresh timing and posting-date reliability

| Company refresh date | Companies |
|---|---:|
| 2026-05-10 | 1 |
| 2026-05-11 | 1 |
| 2026-05-22 | 1 |
| 2026-06-02 | 1 |
| 2026-06-03 | 1 |
| 2026-08-07 | 1 |
| 2026-09-14 | 118 |
| 2026-09-15 | 9 |
| 2026-09-16 | 25 |
| 2026-09-18 | 75 |
| 2026-09-19 | 36 |
| 2026-09-20 | 5 |
| 2026-09-21 | 22 |
| 2026-09-22 | 3 |
| 2026-09-23 | 3 |
| 2026-09-24 | 104 |
| 2026-09-25 | 5 |
| 2026-09-26 | 39 |
| 2026-09-28 | 10 |

Company refresh ages: `{">7-14 days": 269, ">2-7 days": 136, "0-2 days": 49, ">30-90 days": 1, ">90-180 days": 5}`.

Recorded posting ages: `{">14-30 days": 5570, ">7-14 days": 4691, ">30-90 days": 3932, ">2-7 days": 3888, "missing": 2847, ">180 days": 666, ">90-180 days": 736, "0-2 days": 249}`.

| Oldest company refreshes | Timestamp | Age (days) | Job rows |
|---|---|---:|---:|
| slice | 2026-05-10T10:18:16.850Z | 140.931 | 24 |
| qure-ai | 2026-05-11T14:45:54.392Z | 139.746 | 15 |
| moveworks | 2026-05-22T13:04:48.111Z | 128.816 | 85 |
| playsimple-games | 2026-06-02T16:54:29.549Z | 117.656 | 23 |
| zenyum | 2026-06-03T09:07:24.625Z | 116.981 | 9 |
| lindy | 2026-08-07T11:45:50.397Z | 51.871 | 2 |
| 1x | 2026-09-14T09:17:53.878Z | 13.973 | 87 |
| altimate | 2026-09-14T09:18:19.192Z | 13.973 | 6 |
| articul8 | 2026-09-14T09:18:32.031Z | 13.973 | 23 |
| aspora | 2026-09-14T09:19:00.256Z | 13.973 | 5 |

**Cadence cannot be established from a single snapshot.** Same-day clusters suggest batch processing, but neither daily nor weekly scheduling is proven. The public files expose only the latest stored refresh per company; a daily external monitor can measure publication changes, not every backend crawl. Immutable asset HTTP Last-Modified dates must not be substituted for job-data refresh times.

| Source | Rows with recorded posting date | Posting date equals refresh day | Earlier title enrichment |
|---|---:|---:|---:|
| Ashby Jobs Board | 9247 | 2362 | 46 |
| Greenhouse Jobs | 7626 | 7550 | 193 |
| Lever Jobs Board | 979 | 813 | 40 |
| Keka ATS | 122 | 0 | 1 |
| Kula ATS | 498 | 471 | 13 |
| Darwinbox | 10 | 0 | 0 |
| Y Combinator Jobs | 137 | 13 | 0 |
| Freshteam Jobs | 0 | 0 | 0 |
| Workable | 347 | 347 | 3 |
| Comeet Jobs | 350 | 35 | 6 |
| Workday | 0 | 0 | 0 |
| SmartRecruiters | 0 | 0 | 0 |
| Trakstar | 0 | 0 | 0 |
| BambooHR | 55 | 55 | 5 |
| PyjamHR ATS | 39 | 39 | 1 |
| Reczee | 14 | 14 | 2 |
| Rippling | 0 | 0 | 0 |
| Gem Jobs | 0 | 0 | 0 |
| MyNextHire ATS | 0 | 0 | 0 |
| Recruitee | 0 | 0 | 0 |
| Teamtailor | 26 | 0 | 0 |
| TurboHire | 80 | 0 | 0 |
| WordPress Jobs | 0 | 0 | 0 |
| Jobvite | 0 | 0 | 0 |
| SAP ATS | 0 | 0 | 0 |
| ZohoRecruit | 38 | 3 | 0 |
| Custom ATS (TestZeus) | 3 | 3 | 0 |
| Custom Ashby Embed | 133 | 0 | 0 |
| Deel | 0 | 0 | 0 |
| Freshteam | 0 | 0 | 0 |
| JazzHR | 0 | 0 | 0 |
| Manatal | 10 | 10 | 0 |
| RippleHire | 0 | 0 | 0 |
| Scout ATS | 18 | 0 | 1 |
| SenseHQ | 0 | 0 | 0 |

A title can be enriched before a job is reposted, but large numbers of earlier title timestamps combined with identical per-company posted days make publication-date provenance a priority. Preserve separate employer `published_at`, crawler `first_seen_at`, `last_seen_at`, and `last_successful_fetch_at`; leave unknown publication dates null.

## Data integrity and representative cases

### SuperK: internally contradictory location mapping

12/12 rows have a simple display/mapped-city mismatch. See the exact per-job values in `companies[slug=superk].simple_city_mismatch_candidates`. Bengaluru display text with a Denver location reference is an internal contradiction; the company's upstream job page should establish which value is correct.

Fix: validate resolved location country/city against source location before publishing; keep remote eligibility separate from office locations; quarantine conflicting mappings rather than silently falling back to an unrelated office.

### Anthropic: geocoding of a remote-work phrase

The public dataset includes `friendly_office` / Friendly, United States. The Fellows Program records associate this with actual office locations, and other roles display `Remote, Friendly`. The separate primary-source verification confirms the employer Greenhouse API says `Remote-Friendly, United States`, with an office label `Remote-Friendly US (Travel Required)` and no office location. The same job has an employer first-published date of 2026-04-09, whereas this dataset records 2026-09-24 as its posted date. See `source-verification.md` and its JSON evidence for the current endpoint response.

Fix: classify remote/hybrid terms and geographic eligibility before geocoding; require confidence and an explicit place span; never geocode isolated adjectives from remote-work labels.

### HomeLane: duplicate rows and an unresolved location ID

The module has 5 exact application-URL duplicate groups and 1 row(s) referencing an absent location ID. Examples include duplicate Design Consultant rows for the same Nagpur application URL; `Senior Business Manager` references `burdwan_office`, which is absent from the company location table. These are internal consistency defects, independent of employer availability.

Fix: upsert by stable employer posting ID, normalize location arrays into sets, and require every referenced location key to resolve before publishing the snapshot.

- `count_mismatches`: 0 affected companies.
- `dangling_location_refs`: 3 affected companies: homelane, multiplier, tekion.
- `display_reference_country_conflicts`: 7 affected companies: checkout-com, databricks, navan, reka-ai, superk, uniphore, zenoti.
- `duplicate_location_ids`: 3 affected companies: cato-networks, ixigo, superkalam.
- `duplicate_exact_apply_urls`: 3 affected companies: homelane, profound, purplle.
- `duplicate_canonical_apply_urls`: 55 affected companies: 1password, anyscale, architect-labs, articul8, baseten, betterup, bubble, character-ai, checkout-com, clickup, clipboard-health, cognition, cohere, commure, crusoe, dualentry, eliseai, encord, evenup, firecrawl, freecharge, handshake, heidi-health, highbeam, hippocratic-ai ….
- `duplicate_job_ids`: 52 affected companies: 1password, anyscale, architect-labs, articul8, baseten, betterup, bubble, character-ai, checkout-com, clickup, clipboard-health, cognition, cohere, commure, crusoe, dualentry, eliseai, encord, evenup, firecrawl, handshake, heidi-health, highbeam, hippocratic-ai, inworld-ai ….
- `invalid_or_missing_apply_urls`: 0 affected companies.

Cross-company canonical application URL groups: 15. Cross-company job-ID candidate groups: 15. Numeric IDs can overlap between employer tenants; ID collisions alone are not duplicate proof. Canonicalization removes fragments and common referral parameters, so location variants must be distinguished from duplicate openings.

Across the full observed inventory, 21,449 distinct canonical application URLs remain after cross-company deduplication. Shared careers-board groups: `{"https://jobs.lever.co/fampay": ["fam", "famapp-by-trio", "fampay"]}`. Shared public website hosts: `{"fampay.in": ["famapp-by-trio", "fampay"]}`. Shared internal company IDs: `{}`. Some brands may legitimately share a parent company's board; employer identity must be confirmed before merging.

## Zero-job companies to verify

aftershoot, aizen, bharatpe, datachain, datacurve, drinkprime, google-deepmind, inc42, kaagaz, marketfeed, mintifi, pine-labs, plana-earth, plivo, postman, regrello, starsling, tessell, thena, thoughtspot, uniqode, yupp, zipstack

Do not conflate true zero openings, an inaccessible upstream source, a parser failure, intentional filtering, and removed company support. A healthy pipeline should record distinct statuses, retain the last known good snapshot when fetching fails, and alert on unexpected transitions to zero.

## Enrichment provenance and presentation

The analysis preserves exact per-company `provenance_by_category` and `timestamps_by_category` dictionaries. A source label records a claimed method or provider; it does not prove that external provider supplied a particular fact. A timestamp without a source is not evidence of provenance.

| Data category | Companies with source/verification metadata | Typical recorded labels |
|---|---:|---|
| company_identity | 0 | No source/verification label observed |
| job_ingestion | 460 | success, automated+browser, Ashby Jobs Board, selective_scrape, Greenhouse Jobs, Lever Jobs Board, Keka ATS, Kula ATS |
| job_enrichment | 42 | searchapi, ai, deterministic_country_token, orphan_id_mapping_upsert, ats_region_code_apj, company_fallback, company_region_fallback |
| leadership | 459 | linkedin_profile, perplexity-sonar-pro, ai, sankalp, claude-co-work, direct_navigation, cowork, claude-manual |
| social_verification | 421 | ai, sankalp, claude-co-work, direct_navigation, cowork, claude-manual, agent_manual, claude_cowork |
| company_description_and_industry | 456 | searchapi-google-ai-mode, perplexity-sonar-pro-searchapi, manual-edit, claude-co-work-review, claude-co-work-research, manual_correction_name_collision, manual — India's leading on-demand intra-city and inter-city goods transport platform serving MSMEs and individuals |
| locations | 242 | perplexity, ai_inference_upsert, searchapi-maps, reexpand_overexpanded_phase2_2026_05_08, searchapi-maps-backfill-2026-05-24, searchapi-maps-backfill-2026-05-24-strict, reexpand_city_anchored_phase9_2026_05_09, orphan_id_mapping_upsert |
| financial_information | 3 | company_reported, industry_estimate |
| benefits | 427 | job_description, levels_fyi, glassdoor, job_description + careers_page, job_description_gemini |

Careers URLs and their recorded last-updated timestamps are preserved for every company where present; original company discovery/selection is not established by an ATS URL. Financial records may contain funding values and update dates without a retrievable source citation; do not infer an upstream funding database from those fields.

Source metadata records the following short provenance labels (including human verification labels). The complete mapping to fields and companies is machine-readable:

| Label | Companies | Recorded occurrences | Field examples |
|---|---:|---:|---|
| success | 460 | 460 | job_data.crawl_status |
| linkedin_profile | 436 | 969 | leadership.founders[].image_source |
| perplexity-sonar-pro | 433 | 987 | leadership.founders[].description_source |
| searchapi-google-ai-mode | 429 | 438 | business_details.industry_domains_source, leadership.founders[].description_source |
| job_description | 411 | 411 | benefits._sources_checked, benefits.benefits_scraping_source |
| automated+browser | 327 | 327 | job_data.crawl_method |
| sankalp | 227 | 774 | leadership.founders[].linkedin_verified_by, leadership.founders[].x_twitter_verified_by, social_media.instagram_url_verified_by |
| ai | 221 | 1002 | job_data.roles[].location_inference_source, leadership.founders[].linkedin_url_verified_by, leadership.founders[].linkedin_verified_by |
| Ashby Jobs Board | 144 | 144 | job_data.source |
| perplexity-sonar-pro-searchapi | 144 | 144 | business_details.short_description_generated_by |
| perplexity | 142 | 622 | location_mapping[].location_source |
| claude-co-work | 128 | 871 | leadership.current_leadership[].linkedin_verified_by, leadership.founders[].linkedin_verified_by, leadership.founders[].verified_by |
| selective_scrape | 125 | 125 | job_data.crawl_method |
| Greenhouse Jobs | 90 | 90 | job_data.source |
| levels_fyi | 84 | 84 | benefits._sources_checked, benefits.benefits_scraping_source |
| ai_inference_upsert | 63 | 253 | location_mapping[].source |
| searchapi-maps | 47 | 142 | location_mapping[].location_source |
| Lever Jobs Board | 39 | 39 | job_data.source |
| Keka ATS | 32 | 32 | job_data.source |
| reexpand_overexpanded_phase2_2026_05_08 | 25 | 369 | location_mapping[].source |
| searchapi | 25 | 30 | job_data.roles[].salary_estimated.source, leadership.founders[].linkedin_verified_by |
| Kula ATS | 22 | 22 | job_data.source |
| Darwinbox | 21 | 21 | job_data.source |
| direct_navigation | 21 | 93 | leadership.founders[].linkedin_verified_by, leadership.founders[].x_twitter_verified_by, social_media.instagram_url_verified_by |
| manual-edit | 16 | 16 | business_details.industry_domains_source |
| Y Combinator Jobs | 15 | 15 | job_data.source |
| Freshteam Jobs | 11 | 11 | job_data.source |
| Workable | 10 | 10 | job_data.source |
| cowork | 10 | 42 | leadership.founders[].linkedin_verified_by, leadership.founders[].x_twitter_url_verified_by, leadership.founders[].x_twitter_verified_by |
| Comeet Jobs | 8 | 8 | job_data.source |
| Workday | 7 | 7 | job_data.source |
| searchapi-maps-backfill-2026-05-24 | 7 | 38 | location_mapping[].source |
| SmartRecruiters | 6 | 6 | job_data.source |
| Trakstar | 6 | 6 | job_data.source |
| orphan_id_mapping_upsert | 6 | 6 | job_data.roles[].location_inference_source, location_mapping[].source |
| reexpand_city_anchored_phase9_2026_05_09 | 6 | 8 | location_mapping[].source |
| searchapi-maps-backfill-2026-05-24-strict | 6 | 9 | location_mapping[].source |
| agent_manual | 5 | 19 | leadership.founders[].linkedin_verified_by, leadership.founders[].x_twitter_verified_by, social_media.instagram_url_verified_by |
| bare_remote_company_fallback | 5 | 63 | location_mapping[].source |
| claude-co-work-review | 5 | 5 | business_details.industry_domains_source |
| claude-manual | 5 | 31 | leadership.founders[].linkedin_verified_by, leadership.founders[].x_twitter_verified_by, social_media.instagram_url_verified_by |
| inferred | 5 | 18 | location_mapping[].location_source |
| BambooHR | 4 | 4 | job_data.source |
| PyjamHR ATS | 4 | 4 | job_data.source |
| Reczee | 4 | 4 | job_data.source |
| Rippling | 4 | 4 | job_data.source |
| api | 4 | 4 | job_data.crawl_method |
| automated+api | 4 | 4 | job_data.crawl_method |
| city-inference | 4 | 15 | location_mapping[].location_source |
| claude-co-work-research | 4 | 4 | business_details.industry_domains_source |
| manual-fix | 4 | 12 | location_mapping[].location_source |
| Gem Jobs | 3 | 3 | job_data.source |
| MyNextHire ATS | 3 | 3 | job_data.source |
| Recruitee | 3 | 3 | job_data.source |
| Teamtailor | 3 | 3 | job_data.source |
| TurboHire | 3 | 3 | job_data.source |
| WordPress Jobs | 3 | 3 | job_data.source |
| city-default-fallback | 3 | 3 | location_mapping[].location_source |
| manual_research | 3 | 3 | location_mapping[].location_source |
| rescrape_workflow_orphan_id_fix_2026_08_17 | 3 | 3 | location_mapping[].source |
| Jobvite | 2 | 2 | job_data.source |
| SAP ATS | 2 | 2 | job_data.source |
| ZohoRecruit | 2 | 2 | job_data.source |
| company_region_fallback | 2 | 12 | job_data.roles[].location_inference_source, location_mapping[].source |
| data_fix | 2 | 2 | location_mapping[].source |
| deterministic_country_token | 2 | 7 | job_data.roles[].location_inference_source |
| direct_job_posting_inspection | 2 | 2 | location_mapping[].location_source |
| glassdoor | 2 | 2 | benefits.benefits_scraping_source |
| job_description + careers_page | 2 | 2 | benefits.benefits_scraping_source |
| job_location | 2 | 38 | location_mapping[].location_source |
| manual_verification_websearch | 2 | 5 | location_mapping[].location_source |
| phase3_residual_resolution | 2 | 8 | location_mapping[].source |
| x-profile | 2 | 4 | leadership.founders[].image_source |
| 1x office san carlos | 1 | 1 | location_mapping[].location_source_query |
| 2026-08-03T18:25:00.000Z | 1 | 2 | location_mapping[].location_source_last_updated |
| Applied miami | 1 | 1 | location_mapping[].location_source_query |
| Applied office Fort Walton Beach Florida | 1 | 1 | location_mapping[].location_source_query |
| Applied office austin Texas | 1 | 1 | location_mapping[].location_source_query |
| Applied office boston | 1 | 1 | location_mapping[].location_source_query |
| Aquasec office Hyderabad Telangana | 1 | 1 | location_mapping[].location_source_query |
| Arcticwolf office Toronto Ontario | 1 | 1 | location_mapping[].location_source_query |
| Blockchain office buenos aires | 1 | 1 | location_mapping[].location_source_query |
| Blockchain office new york | 1 | 1 | location_mapping[].location_source_query |
| Carousell West Jakarta | 1 | 1 | location_mapping[].location_source_query |
| Carousell office subang jaya | 1 | 1 | location_mapping[].location_source_query |
| Carta office chicago | 1 | 1 | location_mapping[].location_source_query |
| Cognition delhi | 1 | 1 | location_mapping[].location_source_query |
| Cognition office Tokyo Tokyo Metropolis | 1 | 1 | location_mapping[].location_source_query |
| Cognition office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Cognition office chennai | 1 | 1 | location_mapping[].location_source_query |
| Cohere office miami | 1 | 1 | location_mapping[].location_source_query |
| Cohere singapore | 1 | 1 | location_mapping[].location_source_query |
| Crusoe Chicago | 1 | 1 | location_mapping[].location_source_query |
| Crusoe miami | 1 | 1 | location_mapping[].location_source_query |
| Crusoe office Sunnyvale California | 1 | 1 | location_mapping[].location_source_query |
| Crusoe office los angeles | 1 | 1 | location_mapping[].location_source_query |
| Custom ATS (TestZeus) | 1 | 1 | job_data.source |
| Custom Ashby Embed | 1 | 1 | job_data.source |
| Deel | 1 | 1 | job_data.source |
| Dezerv office hyderabad | 1 | 1 | location_mapping[].location_source_query |
| Dialogue AI office Los Angeles | 1 | 1 | location_mapping[].location_source_query |
| Drivetrain austin | 1 | 1 | location_mapping[].location_source_query |
| Drivetrain chennai | 1 | 1 | location_mapping[].location_source_query |
| Drivetrain los angeles | 1 | 1 | location_mapping[].location_source_query |
| Drivetrain office Seattle Washington | 1 | 1 | location_mapping[].location_source_query |
| Farmart delhi | 1 | 1 | location_mapping[].location_source_query |
| Farther austin | 1 | 1 | location_mapping[].location_source_query |
| Figure office Irvine California | 1 | 1 | location_mapping[].location_source_query |
| Figure office pasadena California | 1 | 1 | location_mapping[].location_source_query |
| Figure office reno | 1 | 1 | location_mapping[].location_source_query |
| Fireworks office Chicago Illinois | 1 | 1 | location_mapping[].location_source_query |
| Fireworks office Seattle Washington | 1 | 1 | location_mapping[].location_source_query |
| Fireworks office austin | 1 | 1 | location_mapping[].location_source_query |
| Fireworks office denver | 1 | 1 | location_mapping[].location_source_query |
| Fireworks office miami Florida | 1 | 1 | location_mapping[].location_source_query |
| Flobiz office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Freehand bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Freehand office chennai | 1 | 1 | location_mapping[].location_source_query |
| Freehand office pune | 1 | 1 | location_mapping[].location_source_query |
| Freshteam | 1 | 1 | job_data.source |
| Goodera office mumbai | 1 | 1 | location_mapping[].location_source_query |
| Harvey guadalajara | 1 | 1 | location_mapping[].location_source_query |
| Harvey office Dallas Texas | 1 | 1 | location_mapping[].location_source_query |
| Harvey office Seattle Washington | 1 | 1 | location_mapping[].location_source_query |
| Harvey office austin | 1 | 1 | location_mapping[].location_source_query |
| Harvey office boston | 1 | 1 | location_mapping[].location_source_query |
| Harvey office chicago Illinois | 1 | 1 | location_mapping[].location_source_query |
| Harvey office denver | 1 | 1 | location_mapping[].location_source_query |
| Harvey office london | 1 | 1 | location_mapping[].location_source_query |
| Harvey office los angeles | 1 | 1 | location_mapping[].location_source_query |
| Harvey office singapore | 1 | 1 | location_mapping[].location_source_query |
| Harvey office stockholm | 1 | 1 | location_mapping[].location_source_query |
| JazzHR | 1 | 1 | job_data.source |
| Jodo office Delhi Delhi | 1 | 1 | location_mapping[].location_source_query |
| K2space office san francisco California | 1 | 1 | location_mapping[].location_source_query |
| Lambda Aligned DFW-04 data center Plano Texas | 1 | 1 | location_mapping[].location_source_query |
| Lambda Querétaro | 1 | 1 | location_mapping[].location_source_query |
| Lambda data center Quincy Washington | 1 | 1 | location_mapping[].location_source_query |
| Lambda office Atlanta Georgia | 1 | 1 | location_mapping[].location_source_query |
| Lambda office Elk Grove Village Illinois | 1 | 1 | location_mapping[].location_source_query |
| Lambda office Los Angeles California | 1 | 1 | location_mapping[].location_source_query |
| Lambda office Quebec City Quebec | 1 | 1 | location_mapping[].location_source_query |
| Lambda office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Lambda office boston | 1 | 1 | location_mapping[].location_source_query |
| Lambda office miami | 1 | 1 | location_mapping[].location_source_query |
| M2pfintech office Bengaluru Karnataka | 1 | 1 | location_mapping[].location_source_query |
| M2pfintech office hyderabad | 1 | 1 | location_mapping[].location_source_query |
| M2pfintech office mumbai | 1 | 1 | location_mapping[].location_source_query |
| Manatal | 1 | 1 | job_data.source |
| Metropolis office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Metropolis office jacksonville | 1 | 1 | location_mapping[].location_source_query |
| Metropolis office raleigh North Carolina | 1 | 1 | location_mapping[].location_source_query |
| Metropolis office san francisco | 1 | 1 | location_mapping[].location_source_query |
| Modular office Denver Colorado | 1 | 1 | location_mapping[].location_source_query |
| Nanonets office mumbai | 1 | 1 | location_mapping[].location_source_query |
| Nas Tel Aviv | 1 | 1 | location_mapping[].location_source_query |
| Neuron7 office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Nobroker office Chennai Tamil Nadu | 1 | 1 | location_mapping[].location_source_query |
| Nobroker office Hyderabad Telangana | 1 | 1 | location_mapping[].location_source_query |
| Observe office austin | 1 | 1 | location_mapping[].location_source_query |
| Observe office boston | 1 | 1 | location_mapping[].location_source_query |
| Openhouse office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Orkes office los angeles California | 1 | 1 | location_mapping[].location_source_query |
| Pharmeasy office jammu Jammu and Kashmir | 1 | 1 | location_mapping[].location_source_query |
| Pice delhi | 1 | 1 | location_mapping[].location_source_query |
| Purplle office Bengaluru Karnataka | 1 | 1 | location_mapping[].location_source_query |
| Purplle office Chennai Tamil Nadu | 1 | 1 | location_mapping[].location_source_query |
| Purplle office Hubli Karnataka | 1 | 1 | location_mapping[].location_source_query |
| Purplle office Hyderabad Telangana | 1 | 1 | location_mapping[].location_source_query |
| Purplle office kolkata | 1 | 1 | location_mapping[].location_source_query |
| Reka office new york | 1 | 1 | location_mapping[].location_source_query |
| RippleHire | 1 | 1 | job_data.source |
| Rox office austin Texas | 1 | 1 | location_mapping[].location_source_query |
| Sayweee office Milpitas California | 1 | 1 | location_mapping[].location_source_query |
| Scale dammam | 1 | 1 | location_mapping[].location_source_query |
| Scale miami | 1 | 1 | location_mapping[].location_source_query |
| Scale office Abu Dhabi Abu Dhabi | 1 | 1 | location_mapping[].location_source_query |
| Scale office Budapest | 1 | 1 | location_mapping[].location_source_query |
| Scale office Manchester Greater Manchester | 1 | 1 | location_mapping[].location_source_query |
| Scale office Washington Washington | 1 | 1 | location_mapping[].location_source_query |
| Scale office atlanta | 1 | 1 | location_mapping[].location_source_query |
| Scale office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Scale office birmingham | 1 | 1 | location_mapping[].location_source_query |
| Scale office chennai | 1 | 1 | location_mapping[].location_source_query |
| Scale office chicago | 1 | 1 | location_mapping[].location_source_query |
| Scale office delhi | 1 | 1 | location_mapping[].location_source_query |
| Scale office doha | 1 | 1 | location_mapping[].location_source_query |
| Scale office dubai | 1 | 1 | location_mapping[].location_source_query |
| Scale office edinburgh | 1 | 1 | location_mapping[].location_source_query |
| Scale office honolulu | 1 | 1 | location_mapping[].location_source_query |
| Scale office jeddah | 1 | 1 | location_mapping[].location_source_query |
| Scale office london | 1 | 1 | location_mapping[].location_source_query |
| Scale office los angeles | 1 | 1 | location_mapping[].location_source_query |
| Scale office montreal | 1 | 1 | location_mapping[].location_source_query |
| Scale office pune | 1 | 1 | location_mapping[].location_source_query |
| Scale office riyadh | 1 | 1 | location_mapping[].location_source_query |
| Scale office seattle | 1 | 1 | location_mapping[].location_source_query |
| Scout ATS | 1 | 1 | job_data.source |
| SenseHQ | 1 | 1 | job_data.source |
| Sierra montreal | 1 | 1 | location_mapping[].location_source_query |
| Sierra office Seattle | 1 | 1 | location_mapping[].location_source_query |
| Sierra office madrid | 1 | 1 | location_mapping[].location_source_query |
| Sierra vancouver | 1 | 1 | location_mapping[].location_source_query |
| Tabs austin | 1 | 1 | location_mapping[].location_source_query |
| Tabs office boston | 1 | 1 | location_mapping[].location_source_query |
| Tabs office chicago | 1 | 1 | location_mapping[].location_source_query |
| Tabs office los angeles | 1 | 1 | location_mapping[].location_source_query |
| Together office London England | 1 | 1 | location_mapping[].location_source_query |
| Together office bengaluru | 1 | 1 | location_mapping[].location_source_query |
| Together office chennai | 1 | 1 | location_mapping[].location_source_query |
| Together office delhi | 1 | 1 | location_mapping[].location_source_query |
| Together office mumbai | 1 | 1 | location_mapping[].location_source_query |
| Together office pune | 1 | 1 | location_mapping[].location_source_query |
| Tokopedia office lampung | 1 | 1 | location_mapping[].location_source_query |
| Tokopedia office makassar | 1 | 1 | location_mapping[].location_source_query |
| Tokopedia office samarinda | 1 | 1 | location_mapping[].location_source_query |
| Treebo office Chandigarh Chandigarh | 1 | 1 | location_mapping[].location_source_query |
| Treebo office Dehradun Uttarakhand | 1 | 1 | location_mapping[].location_source_query |
| Treebo office Jodhpur Rajasthan | 1 | 1 | location_mapping[].location_source_query |
| Treebo office Mumbai Maharashtra | 1 | 1 | location_mapping[].location_source_query |
| Treebo office Thiruvananthapuram Kerala | 1 | 1 | location_mapping[].location_source_query |
| Treebo office raipur | 1 | 1 | location_mapping[].location_source_query |
| Verily Miami | 1 | 1 | location_mapping[].location_source_query |
| Verily San Bruno office 999 Bayhill Dr | 1 | 2 | location_mapping[].location_source_query |
| Verily los angeles | 1 | 1 | location_mapping[].location_source_query |
| Verily office Toronto Ontario | 1 | 1 | location_mapping[].location_source_query |
| Waabi office Dallas Texas | 1 | 1 | location_mapping[].location_source_query |
| Wise office Berlin Berlin | 1 | 1 | location_mapping[].location_source_query |
| Wise office Johannesburg | 1 | 1 | location_mapping[].location_source_query |
| Wise office hyderabad | 1 | 1 | location_mapping[].location_source_query |
| Zeni office Lehi Utah | 1 | 1 | location_mapping[].location_source_query |
| agent-6 | 1 | 1 | location_mapping[].location_source |
| alloy.com | 1 | 1 | location_mapping[].location_source |
| ats_region_code_apj | 1 | 6 | job_data.roles[].location_inference_source |
| browser_verified | 1 | 1 | location_mapping[].location_source |
| browser_verified_2026-09-16 | 1 | 1 | location_mapping[].source |
| city_default_fallback | 1 | 1 | location_mapping[].source |
| classifier-fallback | 1 | 1 | location_mapping[].location_source |
| claude-co-work correction (city-level fallback) | 1 | 1 | location_mapping[].location_source |
| claude-cowork | 1 | 2 | leadership.founders[].x_twitter_verified_by |
| claude_cowork | 1 | 7 | leadership.founders[].linkedin_verified_by, leadership.founders[].x_twitter_verified_by, social_media.instagram_url_verified_by |
| company_fallback | 1 | 2 | job_data.roles[].location_inference_source |
| company_reported | 1 | 2 | financial_information.revenue_metrics.current_revenue.source, financial_information.revenue_metrics.previous_revenue.source |
| company_website | 1 | 2 | leadership.founders[].description_source, leadership.founders[].image_source |
| default-city-fallback | 1 | 1 | location_mapping[].location_source |
| derived-from-dallas-office | 1 | 1 | location_mapping[].location_source |
| google_images_crunchbase | 1 | 1 | leadership.founders[].image_source |
| google_images_linkedin | 1 | 3 | leadership.founders[].image_source |
| greenhouse-job-listing | 1 | 1 | location_mapping[].location_source |
| greenhouse_job_postings | 1 | 2 | location_mapping[].location_source |
| human | 1 | 1 | leadership.founders[].linkedin_verified_by |
| industry_estimate | 1 | 2 | financial_information.revenue_metrics.current_revenue.source, financial_information.revenue_metrics.previous_revenue.source |
| job-board-inferred | 1 | 3 | location_mapping[].location_source |
| job_description_gemini | 1 | 1 | benefits.benefits_scraping_source |
| linkedin | 1 | 1 | leadership.founders[].description_source |
| manual-correction-2026-09-21 | 1 | 3 | location_mapping[].location_source |
| manual-normalisation | 1 | 1 | location_mapping[].location_source |
| manual_correction_name_collision | 1 | 1 | business_details.industry_domains_source |
| manual_duplicate_id_fix | 1 | 1 | location_mapping[].source |
| manual_search | 1 | 1 | leadership.founders[].image_source |
| metro_alias_unify_thane_to_mumbai | 1 | 1 | location_mapping[].source |
| middle-europe-region-expansion | 1 | 6 | location_mapping[].location_source |
| perplexity-api | 1 | 1 | leadership.founders[].linkedin_verified_by |
| perplexity-verified-agent6 | 1 | 2 | location_mapping[].location_source |
| phase4_residual_mapping_upsert | 1 | 1 | location_mapping[].source |
| province_capital_representative | 1 | 1 | location_mapping[].location_source |
| public-profile | 1 | 1 | leadership.founders[].description_source |
| rescrape_workflow_real_location_restore | 1 | 1 | location_mapping[].source |
| scraper-address-normalisation | 1 | 1 | location_mapping[].location_source |
| state_capital_representative | 1 | 2 | location_mapping[].location_source |
| web_search | 1 | 1 | leadership.founders[].x_twitter_verified_by |
| x_twitter_profile | 1 | 1 | leadership.founders[].image_source |

### Complete observed citation-domain inventory

| Citation domain | Companies | Recorded citation occurrences | Field categories |
|---|---:|---:|---|
| www.ambitionbox.com | 15 | 48 | job_data.roles[].salary_estimated.citations |
| www.levels.fyi | 12 | 14 | job_data.roles[].salary_estimated.citations |
| www.glassdoor.co.in | 9 | 13 | job_data.roles[].salary_estimated.citations |
| 6figr.com | 7 | 12 | job_data.roles[].salary_estimated.citations |
| www.weekday.works | 6 | 6 | job_data.roles[].salary_estimated.citations |
| www.repvue.com | 3 | 4 | job_data.roles[].salary_estimated.citations |
| remote.io | 2 | 2 | job_data.roles[].salary_estimated.citations |
| www.glassdoor.com | 2 | 3 | job_data.roles[].salary_estimated.citations |
| www.linkedin.com | 2 | 3 | job_data.roles[].salary_estimated.citations |
| bettsrecruiting.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| bloomberry.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| browserstack.wd3.myworkdayjobs.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| fde.academy | 1 | 1 | job_data.roles[].salary_estimated.citations |
| flutebyte.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| jobs.lever.co | 1 | 1 | job_data.roles[].salary_estimated.citations |
| kidat.in | 1 | 1 | job_data.roles[].salary_estimated.citations |
| omnivoo.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| pathvio.in | 1 | 1 | job_data.roles[].salary_estimated.citations |
| plane.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| remotive.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| startup.jobs | 1 | 1 | job_data.roles[].salary_estimated.citations |
| tripleten.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.adzuna.in | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.ayautomate.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.comparably.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.glassdoor.co.uk | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.grapevine.in | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.hackerrank.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.jobbyrecruit.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.jobleads.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.kore1.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.mbacrystalball.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.naukri.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.salary.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.softlogicsys.in | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.theladders.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.uplers.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.youtube.com | 1 | 1 | job_data.roles[].salary_estimated.citations |
| www.ziprecruiter.com | 1 | 1 | job_data.roles[].salary_estimated.citations |

Benefits are extracted/enriched separately from job ingestion; an old benefits timestamp does not imply a newly fetched job offers that benefit. Preserve per-benefit source, observed date, employer/role scope, and confidence. The normalized collector retains benefit field names and provenance, not every benefit value, so this analysis cannot verify whether each displayed benefit is substantiated.

Keep the original job title as the primary label or show it alongside any simplified title. Department classification and salary estimates are model outputs, not employer statements. Validate them separately and show source/date/confidence.

Location provenance includes inferred and representative-city records, such as `ai_inference_upsert`, `company_fallback`, `state_capital_representative`, and `province_capital_representative` where present. A remote job mapped to a representative city is not evidence that the employer has an office there. Separate physical offices, job locations, eligible remote regions, and map display anchors in both data schema and UI.

## Complete company-to-source and freshness ledger

| Company | Recorded source | Careers host | Job rows | Last refresh UTC | Map flag |
|---|---|---|---:|---|---|
| 100ms (`100ms`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/100ms) | 9 | 2026-09-14T13:09:35.614Z | True |
| 1Password (`1password`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/1password) | 106 | 2026-09-18T15:39:09.851Z | True |
| 1X (`1x`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/1x) | 87 | 2026-09-14T09:17:53.878Z | True |
| Abridge (`abridge`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/abridge) | 47 | 2026-09-24T09:31:47.935Z | True |
| Acceldata (`acceldata`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/acceldata) | 40 | 2026-09-24T10:11:47.269Z | True |
| ACKO (`acko`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/acko) | 15 | 2026-09-26T18:12:06.317Z | True |
| Aegis Ventures (`aegis-ventures`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/aegisventures) | 12 | 2026-09-18T15:47:29.705Z | True |
| Aftershoot (`aftershoot`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/aftershoot) | 0 | 2026-09-18T16:01:44.064Z | True |
| AiDash (`aidash`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=aidashinc) | 8 | 2026-09-24T09:53:34.478Z | True |
| Aikido Security (`aikido-security`) | Recruitee | [aikidosecurity.recruitee.com](https://aikidosecurity.recruitee.com/careers) | 79 | 2026-09-16T18:04:15.286Z | True |
| Aizen (`aizen`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/aizen) | 0 | 2026-09-26T17:52:13.130Z | True |
| Alchemy (`alchemy`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/alchemy) | 20 | 2026-09-19T16:38:01.520Z | True |
| Aledade (`aledade`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/aledade) | 34 | 2026-09-18T15:54:53.041Z | True |
| Alloy (`alloy`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/alloy) | 26 | 2026-09-19T16:50:32.876Z | True |
| Altimate (`altimate`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/altimate) | 6 | 2026-09-14T09:18:19.192Z | True |
| Amagi (`amagi`) | MyNextHire ATS | [amagi.mynexthire.com](https://amagi.mynexthire.com/employer/jobs) | 15 | 2026-09-14T13:13:17.049Z | True |
| Ambience Healthcare (`ambience-healthcare`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/ambiencehealthcare) | 17 | 2026-09-24T09:32:19.836Z | True |
| Anthropic (`anthropic`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/anthropic) | 448 | 2026-09-24T09:54:47.086Z | True |
| Anyscale (`anyscale`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/anyscale) | 25 | 2026-09-23T19:43:41.532Z | True |
| Apna (`apna`) | Workable | [apply.workable.com](https://apply.workable.com/apna) | 107 | 2026-09-28T05:44:50.167Z | True |
| Apollo.io (`apollo-io`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/apolloio) | 48 | 2026-09-18T15:48:03.373Z | True |
| Appier (`appier`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/appier) | 71 | 2026-09-24T09:55:49.660Z | True |
| Applied (`applied`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/applied) | 292 | 2026-09-19T16:39:41.242Z | True |
| AppsForBharat (`appsforbharat`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/appsforbharat) | 24 | 2026-09-24T10:15:00.194Z | True |
| AppZen (`appzen`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/appzen) | 22 | 2026-09-14T13:09:58.024Z | True |
| Aqua Security (`aqua-security`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/aquasec/91.001) | 9 | 2026-09-19T16:58:42.464Z | True |
| Architect Labs (`architect-labs`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/architect) | 15 | 2026-09-25T09:32:03.417Z | True |
| Arctic Wolf (`arctic-wolf`) | Workday | [arcticwolf.wd1.myworkdayjobs.com](https://arcticwolf.wd1.myworkdayjobs.com/External) | 107 | 2026-09-20T16:28:11.583Z | True |
| Arena (`arena`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/arena) | 20 | 2026-09-15T12:57:05.425Z | True |
| Array (`array`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/array) | 14 | 2026-09-14T12:52:32.689Z | True |
| Arta Finance (`arta-finance`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/artafinance) | 11 | 2026-09-18T15:39:21.008Z | True |
| Articul8 (`articul8`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/articul8) | 23 | 2026-09-14T09:18:32.031Z | True |
| Ashby (`ashby`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/ashby) | 70 | 2026-09-24T09:33:00.188Z | True |
| Aspora (`aspora`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Aspora) | 5 | 2026-09-14T09:19:00.256Z | True |
| AssetPlus (`assetplus`) | Keka ATS | [assetplus.keka.com](https://assetplus.keka.com/careers) | 15 | 2026-09-18T16:03:29.019Z | True |
| At-Bay (`at-bay`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/atbayjobs) | 32 | 2026-09-14T12:53:19.912Z | True |
| Atlan (`atlan`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/atlan) | 8 | 2026-09-14T09:19:31.956Z | True |
| Atlys (`atlys`) | Recruitee | [atlys.recruitee.com](https://atlys.recruitee.com) | 23 | 2026-09-14T13:16:07.482Z | True |
| Atomicwork (`atomicwork`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/atomicwork) | 27 | 2026-09-24T09:56:11.488Z | True |
| Atoms (`atoms`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/cssmerge) | 269 | 2026-09-24T09:57:10.047Z | True |
| Attentive.ai (`attentive-ai`) | Keka ATS | [attentiveos.keka.com](https://attentiveos.keka.com/careers) | 19 | 2026-09-24T10:20:10.926Z | True |
| Avoma (`avoma`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/avoma) | 26 | 2026-09-24T10:16:16.874Z | True |
| Awfis (`awfis`) | Keka ATS | [awfis.keka.com](https://awfis.keka.com/careers) | 6 | 2026-09-21T16:30:01.238Z | True |
| Axion (`axionray`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/axion) | 12 | 2026-09-14T12:23:18.946Z | True |
| Axonius (`axonius`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/axonius) | 19 | 2026-09-26T18:49:15.591Z | True |
| Base Power (`base-power`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/base-power) | 190 | 2026-09-18T15:41:20.494Z | True |
| Baseten (`baseten`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/baseten) | 202 | 2026-09-21T16:19:48.564Z | True |
| Beacon Software (`beacon-software`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/beaconsoftware) | 48 | 2026-09-21T16:20:22.577Z | True |
| BetterUp (`betterup`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/betterup) | 27 | 2026-09-24T09:33:44.315Z | True |
| BharatPe (`bharatpe`) | Darwinbox | [bharatpe.darwinbox.in](https://bharatpe.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 0 | 2026-09-24T10:26:31.591Z | True |
| BIK (`bik`) | Keka ATS | [comida.keka.com](https://comida.keka.com/careers) | 8 | 2026-09-16T18:18:30.361Z | True |
| BlinkOps (`blinkops`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/blinkops/C7.004) | 13 | 2026-09-22T10:00:58.817Z | True |
| Blockchain.com (`blockchain-com`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/blockchain) | 39 | 2026-09-24T09:57:45.315Z | True |
| Bloomreach (`bloomreach`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/bloomreach) | 77 | 2026-09-24T09:58:29.508Z | True |
| Bluevine (`bluevine`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/bluevineindia) | 7 | 2026-09-24T09:58:41.716Z | True |
| Bobobox (`bobobox`) | Teamtailor | [bobobox.teamtailor.com](https://bobobox.teamtailor.com/jobs) | 20 | 2026-09-18T16:09:11.272Z | True |
| Bright Money (`bright-money`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/brightmoney) | 21 | 2026-09-24T10:17:20.029Z | True |
| Brigit (`brigit`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/brigit) | 18 | 2026-09-14T12:24:21.633Z | True |
| BrowserStack (`browserstack`) | Workday | [browserstack.wd3.myworkdayjobs.com](https://browserstack.wd3.myworkdayjobs.com/External) | 35 | 2026-09-24T10:23:25.210Z | True |
| Bubble (`bubble`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/bubble) | 14 | 2026-09-14T09:19:59.623Z | True |
| Buildots (`buildots`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/buildots/36.004) | 49 | 2026-09-14T12:47:47.027Z | True |
| Bureau (`bureau`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/bureau) | 16 | 2026-09-14T09:20:25.703Z | True |
| CarDekho (`cardekho`) | Darwinbox | [cardekho.darwinbox.in](https://cardekho.darwinbox.in/ms/candidate/606876f7e2c79/careers) | 17 | 2026-09-14T13:34:28.025Z | True |
| Carousell (`carousell`) | SmartRecruiters | [jobs.smartrecruiters.com](https://jobs.smartrecruiters.com/CarousellGroup) | 62 | 2026-09-14T13:17:56.244Z | True |
| Carta (`carta`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/carta) | 75 | 2026-09-24T09:59:26.313Z | True |
| Cartesia (`cartesia`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/cartesia) | 30 | 2026-09-21T16:21:02.330Z | True |
| Casca (`casca`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/casca) | 7 | 2026-09-18T15:41:53.558Z | True |
| Cashfree (`cashfree`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/cashfree) | 35 | 2026-09-24T10:17:40.929Z | True |
| Cato Networks (`cato-networks`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/catonetworks) | 101 | 2026-09-18T15:48:48.787Z | True |
| Celonis (`celonis`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=celonis) | 251 | 2026-09-19T16:51:20.104Z | True |
| CertiK (`certik`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/certik) | 28 | 2026-09-24T10:12:06.506Z | True |
| Chai Discovery (`chai-discovery`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/chaidiscovery) | 17 | 2026-09-26T17:52:41.369Z | True |
| Chainguard (`chainguard`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/chainguard) | 87 | 2026-09-24T10:00:10.078Z | True |
| Character.AI (`character-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/character) | 14 | 2026-09-14T09:20:39.142Z | True |
| Chargebee (`chargebee`) | SAP ATS | [jobs.chargebee.com](https://jobs.chargebee.com/) | 1 | 2026-09-24T10:28:27.595Z | True |
| Checkout.com (`checkout-com`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/checkout.com) | 170 | 2026-09-20T10:24:02.481Z | True |
| Claim Health (`claim-health`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/claim-health) | 8 | 2026-09-14T09:20:51.252Z | True |
| Clay (`clay`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/claylabs) | 58 | 2026-09-24T09:34:25.648Z | True |
| Clear (`clear`) | Darwinbox | [clear.darwinbox.in](https://clear.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 15 | 2026-09-18T16:06:36.664Z | True |
| CleverTap (`clevertap`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/clevertap) | 14 | 2026-09-18T16:01:55.146Z | True |
| ClickHouse (`clickhouse`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/clickhouse) | 206 | 2026-09-18T15:43:54.721Z | True |
| ClickUp (`clickup`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/clickup) | 96 | 2026-09-14T09:45:58.926Z | True |
| Clipboard Health (`clipboard-health`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/clipboard) | 49 | 2026-09-14T12:24:59.551Z | True |
| Coding Ninjas (`coding-ninjas`) | Darwinbox | [codingninjas.darwinbox.in](https://codingninjas.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 6 | 2026-09-18T16:06:47.452Z | True |
| Coefficient (`coefficient`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/coefficient) | 6 | 2026-09-26T18:01:57.607Z | True |
| Cognida.ai (`cognida-ai`) | Keka ATS | [cognida.keka.com](https://cognida.keka.com/careers) | 9 | 2026-09-14T09:22:12.674Z | True |
| Cognition (`cognition`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/cognition) | 105 | 2026-09-19T16:40:30.386Z | True |
| Cohere (`cohere`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/cohere) | 148 | 2026-09-14T09:46:52.200Z | True |
| CommerceIQ (`commerceiq`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/commerceiq) | 11 | 2026-09-24T10:01:04.529Z | True |
| Commure (`commure`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/commure) | 82 | 2026-09-24T09:35:28.796Z | True |
| Composio (`composio`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/composio) | 31 | 2026-09-14T09:47:19.068Z | True |
| Confluent (`confluent`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/confluent) | 21 | 2026-09-21T16:21:14.497Z | True |
| Corgi (`corgi`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/corgi/jobs) | 60 | 2026-09-14T13:25:59.528Z | True |
| CRED (`cred`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/cred) | 11 | 2026-09-16T18:00:51.504Z | True |
| Crusoe (`crusoe`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Crusoe) | 465 | 2026-09-21T17:30:45.201Z | True |
| Cyera (`cyera`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/cyera/17.008) | 211 | 2026-09-18T16:06:23.259Z | True |
| Daloopa (`daloopa`) | Rippling | [ats.rippling.com](https://ats.rippling.com/daloopa/jobs) | 18 | 2026-09-16T18:04:34.251Z | True |
| Darwinbox (`darwinbox`) | Darwinbox | [dbx.darwinbox.in](https://dbx.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 34 | 2026-09-28T05:42:43.945Z | True |
| Databricks (`databricks`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/databricks) | 889 | 2026-09-14T18:11:22.346Z | True |
| Datachain (`datachain`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/iterative) | 0 | 2026-09-18T15:55:18.160Z | True |
| Datacurve (`datacurve`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/datacurve) | 0 | 2026-09-14T09:47:51.860Z | True |
| Daybreak Health (`daybreak-health`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/daybreakhealth) | 27 | 2026-09-19T16:51:51.365Z | True |
| DealMaker (`dealmaker`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/DealMaker) | 8 | 2026-09-19T16:41:08.020Z | True |
| Decagon (`decagon`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/decagon) | 140 | 2026-09-14T09:48:39.088Z | True |
| DeepAware AI (`deepaware-ai`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/deepaware-ai/jobs) | 7 | 2026-09-18T15:57:53.605Z | True |
| DeepL (`deepl`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/DeepL) | 58 | 2026-09-14T09:49:10.032Z | True |
| DeepScribe (`deepscribe`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/deepscribe) | 3 | 2026-09-18T16:02:03.259Z | True |
| Delhivery (`delhivery`) | Darwinbox | [delhivery.darwinbox.in](https://delhivery.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 7 | 2026-09-19T16:59:09.825Z | True |
| Dexterity (`dexterity`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/dexterity) | 30 | 2026-09-19T16:55:43.948Z | True |
| Dezerv (`dezerv`) | Scout ATS | [scout.dezerv.in](https://scout.dezerv.in/careers/jobs) | 18 | 2026-09-19T16:56:12.855Z | True |
| Dialogue (`dialogue`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/dialogueai) | 3 | 2026-09-19T16:41:38.043Z | True |
| Digantara (`digantara`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/digantara) | 64 | 2026-09-24T10:18:06.252Z | True |
| Distyl (`distyl`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Distyl) | 24 | 2026-09-14T09:49:37.414Z | True |
| Doctronic (`doctronic`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/doctronic) | 14 | 2026-09-14T09:50:06.353Z | True |
| Dodopayments (`dodopayments`) | PyjamHR ATS | [jobs.pyjamahr.com](https://jobs.pyjamahr.com/dodo-payments) | 4 | 2026-09-24T10:24:02.776Z | True |
| Domu (`domu-technology-inc`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/domu-technology-inc/jobs) | 8 | 2026-09-18T15:58:02.786Z | True |
| doola (`doola`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/doola) | 4 | 2026-09-14T13:11:13.593Z | True |
| DrinkPrime (`drinkprime`) | Freshteam Jobs | [drinkprime.freshteam.com](https://drinkprime.freshteam.com/jobs) | 0 | 2026-09-24T10:26:55.743Z | True |
| Drip Capital (`drip-capital`) | Trakstar | [dripcapital.hire.trakstar.com](https://dripcapital.hire.trakstar.com/jobs) | 4 | 2026-09-19T16:59:38.121Z | True |
| Drivetrain (`drivetrain`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/drivetrain) | 33 | 2026-09-24T10:12:14.234Z | True |
| Druva (`druva`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=druva) | 38 | 2026-09-14T12:53:59.935Z | True |
| DualEntry (`dualentry`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/dualentry) | 94 | 2026-09-24T09:36:06.104Z | True |
| Durable (`durable`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/durable) | 4 | 2026-09-14T12:54:12.391Z | True |
| Dynatrace (`dynatrace`) | SAP ATS | [www.dynatrace.com](https://www.dynatrace.com/careers/jobs) | 119 | 2026-09-24T10:50:28.667Z | True |
| Elementor (`elementor`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/Elementor/A3.00F) | 1 | 2026-09-16T18:05:16.619Z | True |
| ElevenLabs (`elevenlabs`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/elevenlabs) | 246 | 2026-09-14T09:51:06.381Z | True |
| EliseAI (`eliseai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/EliseAI) | 177 | 2026-09-19T16:42:33.947Z | True |
| Emergent (`emergent`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/emergentlabsinc) | 33 | 2026-09-18T15:49:17.635Z | True |
| Encord (`encord`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/encord) | 48 | 2026-09-25T09:32:42.968Z | True |
| Eon (`eon`) | Greenhouse Jobs | [job-boards.eu.greenhouse.io](https://job-boards.eu.greenhouse.io/eonio) | 26 | 2026-09-19T16:52:24.531Z | True |
| Epic Games (`epic-games`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=epicgames) | 150 | 2026-09-19T16:53:01.726Z | True |
| Eudia (`eudia`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/eudia) | 18 | 2026-09-14T12:54:43.121Z | True |
| EvenUp (`evenup`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/evenup) | 64 | 2026-09-14T12:25:52.269Z | True |
| Everstage (`everstage`) | Freshteam Jobs | [everstage.freshteam.com](https://everstage.freshteam.com/jobs) | 9 | 2026-09-14T12:49:49.090Z | True |
| Exa (`exa`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/exa) | 52 | 2026-09-24T09:36:40.748Z | True |
| Exabeam (`exabeam`) | Jobvite | [jobs.jobvite.com](https://jobs.jobvite.com/exabeam) | 2 | 2026-09-22T15:47:15.936Z | True |
| Exponent Energy (`exponent-energy`) | Workable | [apply.workable.com](https://apply.workable.com/exponent-energy) | 48 | 2026-09-24T10:30:11.007Z | True |
| ezCater (`ezcater`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/ezcaterinc) | 28 | 2026-09-24T10:01:39.529Z | True |
| Faire (`faire`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/faire) | 73 | 2026-09-24T10:02:45.320Z | True |
| FalconX (`falconx`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/falconx) | 16 | 2026-09-26T18:02:34.872Z | True |
| Fam (`fam`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/fampay) | 15 | 2026-09-26T18:10:33.907Z | True |
| FamApp (`famapp-by-trio`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/fampay) | 15 | 2026-09-24T10:12:30.572Z | True |
| FamPay (`fampay`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/fampay) | 14 | 2026-09-18T15:55:32.919Z | True |
| FarMart (`farmart`) | Trakstar | [farmart.hire.trakstar.com](https://farmart.hire.trakstar.com) | 14 | 2026-09-14T09:23:15.996Z | True |
| Farther (`farther`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/fartherfinance) | 31 | 2026-09-24T10:03:23.111Z | True |
| Federato (`federato`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/federato) | 7 | 2026-09-14T12:55:18.002Z | True |
| Fello (`fello`) | Rippling | [fello.rippling-ats.com](https://fello.rippling-ats.com/jobs) | 5 | 2026-09-14T13:16:50.108Z | True |
| Fiddler AI (`fiddler-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/fiddler-ai) | 7 | 2026-09-21T16:21:40.745Z | True |
| Figma (`figma`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=figma) | 152 | 2026-09-19T16:53:43.561Z | True |
| Figure (`figure`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/figureai) | 97 | 2026-09-26T18:03:14.681Z | True |
| FinBox (`finbox`) | Reczee | [jobs.reczee.com](https://jobs.reczee.com/finbox) | 3 | 2026-09-26T18:17:48.194Z | True |
| Finix (`finix`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/finix) | 15 | 2026-09-14T13:11:36.040Z | True |
| Firecrawl (`firecrawl`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/firecrawl) | 36 | 2026-09-19T17:14:15.012Z | True |
| Fireworks AI (`fireworks-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/fireworks) | 79 | 2026-09-19T16:44:27.580Z | True |
| FloBiz (`flobiz`) | Keka ATS | [valorem.keka.com](https://valorem.keka.com/careers) | 11 | 2026-09-24T10:20:23.379Z | True |
| Flynote (`flynote`) | Freshteam | [flynote.freshteam.com](https://flynote.freshteam.com/jobs) | 1 | 2026-09-23T17:36:01.680Z | True |
| Freecharge (`freecharge`) | RippleHire | [freecharge.ripplehire.com](https://freecharge.ripplehire.com/candidate/?token=IoV5vvUSMKLwmaa1Suou&source=CAREERSITE#list) | 6 | 2026-09-18T16:04:33.041Z | True |
| Freed (`freed`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/freed) | 3 | 2026-09-24T09:36:52.938Z | True |
| Freehand (`freehand`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/freehand) | 13 | 2026-09-16T17:52:51.519Z | True |
| Freshworks (`freshworks`) | SmartRecruiters | [jobs.smartrecruiters.com](https://jobs.smartrecruiters.com/Freshworks) | 123 | 2026-09-28T05:45:35.758Z | True |
| Gaiafamily (`gaiafamily`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/gaiafamily) | 4 | 2026-09-14T09:51:33.803Z | True |
| Gamma (`gamma`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/gamma) | 31 | 2026-09-14T12:26:05.999Z | True |
| Giga (`giga`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/gigaml) | 32 | 2026-09-14T09:52:02.585Z | True |
| Glean (`glean`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/gleanwork) | 120 | 2026-09-16T18:22:17.856Z | True |
| GoHighLevel (`gohighlevel`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/gohighlevel) | 96 | 2026-09-18T15:55:47.805Z | True |
| GoKwik (`gokwik`) | Keka ATS | [gokwik.keka.com](https://gokwik.keka.com/careers) | 23 | 2026-09-18T16:03:37.434Z | True |
| GoMotive (`gomotive`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/gomotive) | 157 | 2026-09-26T18:04:05.039Z | True |
| Goodera (`goodera`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/goodera) | 20 | 2026-09-14T13:08:11.551Z | True |
| Goodfire (`goodfire`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/goodfire) | 26 | 2026-09-19T16:54:14.501Z | True |
| Goodnotes (`goodnotes`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/goodnotes) | 3 | 2026-09-18T15:49:28.443Z | True |
| Google DeepMind (`google-deepmind`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/deepmind) | 0 | 2026-09-14T12:56:03.387Z | True |
| GoTo (`goto`) | Workday | [goto.wd5.myworkdayjobs.com](https://goto.wd5.myworkdayjobs.com/gotocareers) | 16 | 2026-09-18T16:04:59.042Z | True |
| Grafana Labs (`grafana-labs`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/grafanalabs) | 148 | 2026-09-26T18:04:48.074Z | True |
| Granola (`granola`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/granola) | 15 | 2026-09-14T09:52:16.956Z | True |
| Greylabs (`greylabs`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/greylabs) | 18 | 2026-09-24T10:18:24.121Z | True |
| Growfin (`growfin`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/growfin) | 1 | 2026-09-24T10:18:41.034Z | True |
| Groww (`groww`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/groww) | 8 | 2026-09-18T15:49:58.727Z | True |
| Gushwork (`gushwork`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/gushwork) | 12 | 2026-09-24T10:12:46.565Z | True |
| Habyt (`habyt`) | BambooHR | [habyt.bamboohr.com](https://habyt.bamboohr.com/careers) | 6 | 2026-09-24T10:56:18.941Z | True |
| HackerRank (`hackerrank`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/hackerrank) | 27 | 2026-09-26T18:05:26.755Z | True |
| Handshake (`handshake`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/handshake) | 82 | 2026-09-24T09:38:12.396Z | True |
| Harvey (`harvey`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/harvey) | 299 | 2026-09-21T16:59:34.494Z | True |
| Headout (`headout`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=headoutcareers) | 22 | 2026-09-18T15:50:29.315Z | True |
| HeadSpin (`headspin`) | BambooHR | [headspin.bamboohr.com](https://headspin.bamboohr.com/careers) | 8 | 2026-09-14T12:46:29.364Z | True |
| Heidi Health (`heidi-health`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/heidihealth.com.au) | 110 | 2026-09-14T09:53:40.817Z | True |
| Helion Energy (`helion-energy`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/helion) | 62 | 2026-09-24T09:41:30.689Z | True |
| Helsing (`helsing`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/helsing) | 154 | 2026-09-24T10:04:08.556Z | True |
| Hevo Data (`hevo-data`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/hevodata) | 47 | 2026-09-18T15:56:03.964Z | True |
| Highbeam (`highbeam`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/highbeam) | 11 | 2026-09-14T16:39:46.262Z | True |
| HighRadius (`highradius`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=highradius) | 82 | 2026-09-28T05:41:17.906Z | True |
| Hippocratic AI (`hippocratic-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Hippocratic%20AI) | 37 | 2026-09-26T17:55:01.191Z | True |
| Homelane (`homelane`) | Darwinbox | [homelane.darwinbox.in](https://homelane.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 58 | 2026-09-28T05:46:03.737Z | True |
| Hook (`hook`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/hook) | 3 | 2026-09-19T16:44:39.983Z | True |
| Hyperbound (`hyperbound`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/hyperbound/jobs) | 4 | 2026-09-18T15:58:25.723Z | True |
| HyperGuest (`hyperguest`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/hyperguest/09.00B) | 5 | 2026-09-14T12:48:04.167Z | True |
| iBASEt (`ibaset`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/ibase-t) | 13 | 2026-09-16T18:01:43.765Z | True |
| IMT Care (`imt-care`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/imt-care/jobs) | 1 | 2026-09-18T15:58:37.660Z | True |
| Inc42 (`inc42`) | Freshteam Jobs | [inc42.freshteam.com](https://inc42.freshteam.com/jobs) | 0 | 2026-09-16T18:05:49.514Z | True |
| Infinity (`infinity`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/infinity/jobs) | 1 | 2026-09-18T15:58:49.033Z | True |
| Inflection (`inflection`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/inflectionio) | 2 | 2026-09-14T09:53:54.806Z | True |
| Innovaccer (`innovaccer`) | Workable | [apply.workable.com](https://apply.workable.com/innovaccer-analytics) | 35 | 2026-09-24T10:30:42.677Z | True |
| Interfere (`interfere`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/interfere/jobs) | 4 | 2026-09-24T10:14:17.008Z | True |
| Inworld AI (`inworld-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/inworld-ai) | 22 | 2026-09-18T15:44:07.373Z | True |
| Ivy (`ivy`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Augustus) | 9 | 2026-09-19T16:44:51.457Z | True |
| ixigo (`ixigo`) | SmartRecruiters | [jobs.smartrecruiters.com](https://jobs.smartrecruiters.com/ixigo) | 8 | 2026-09-18T16:09:37.070Z | True |
| Jar (`jar`) | JazzHR | [changejar.applytojob.com](https://changejar.applytojob.com) | 11 | 2026-09-18T16:08:40.022Z | True |
| Jodo (`jodo`) | Keka ATS | [jodo.keka.com](https://jodo.keka.com/careers) | 5 | 2026-09-26T18:12:19.038Z | True |
| Josys (`josys`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/josys) | 26 | 2026-09-18T15:44:31.084Z | True |
| Juniper Square (`juniper-square`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/junipersquare) | 42 | 2026-09-14T12:26:56.290Z | True |
| Jupiter (`jupiter`) | Keka ATS | [jupiter.keka.com](https://jupiter.keka.com/careers) | 12 | 2026-09-14T13:03:59.655Z | True |
| K2 Space (`k2-space`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/k2spacecorporation) | 231 | 2026-09-16T17:58:01.663Z | True |
| Kaagaz (`kaagaz`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/kaagaz/jobs) | 0 | 2026-09-18T15:59:12.668Z | True |
| Karius (`karius`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/kariusdx) | 19 | 2026-09-26T18:10:55.054Z | True |
| Ketryx (`ketryx`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/ketryx) | 15 | 2026-09-26T18:06:05.426Z | True |
| Ketto (`ketto`) | Keka ATS | [ketto.keka.com](https://ketto.keka.com/careers) | 34 | 2026-09-24T10:20:41.817Z | True |
| Khatabook (`khatabook`) | TurboHire | [khatabook.turbohire.co](https://khatabook.turbohire.co/dashboardv2) | 18 | 2026-09-19T17:01:50.728Z | True |
| Kodiak AI (`kodiak-ai`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/kodiak) | 68 | 2026-09-24T10:04:47.202Z | True |
| Kong (`kong`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/kong) | 80 | 2026-09-24T09:45:25.217Z | True |
| KreditBee (`kreditbee`) | Darwinbox | [kreditbee.darwinbox.in](https://kreditbee.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 13 | 2026-09-18T16:07:39.117Z | True |
| Kutumb (`kutumb`) | Keka ATS | [primetrace.keka.com](https://primetrace.keka.com/careers) | 23 | 2026-09-15T17:35:41.607Z | True |
| Lambda (`lambda`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/lambda) | 195 | 2026-09-15T10:20:45.864Z | True |
| LambdaTest (`lambdatest`) | Keka ATS | [lambdatest.keka.com](https://lambdatest.keka.com/careers) | 4 | 2026-09-24T10:20:45.423Z | True |
| Landeed (`landeed`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/landeed/jobs) | 24 | 2026-09-28T05:49:06.636Z | True |
| LangChain (`langchain`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/langchain) | 108 | 2026-09-14T09:54:44.364Z | True |
| Leap Finance (`leap-finance`) | Freshteam Jobs | [leapfinance.freshteam.com](https://leapfinance.freshteam.com/jobs) | 45 | 2026-09-24T10:27:35.309Z | True |
| lemon.markets (`lemon-markets`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/lemon-markets) | 20 | 2026-09-16T17:53:30.542Z | True |
| Level AI (`level-ai`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/levelai) | 19 | 2026-09-14T13:11:49.398Z | True |
| Liminal Custody (`liminal-custody`) | Keka ATS | [liminal.keka.com](https://liminal.keka.com/careers) | 13 | 2026-09-14T09:22:28.714Z | True |
| Lindy (`lindy`) | Teamtailor | [careers.lindy.ai](https://careers.lindy.ai/) | 2 | 2026-08-07T11:45:50.397Z | True |
| Lokalapps (`lokalapps`) | Workable | [apply.workable.com](https://apply.workable.com/lokal-app) | 61 | 2026-09-14T13:23:09.673Z | True |
| Loop Health (`loop-health`) | Keka ATS | [loop.keka.com](https://loop.keka.com/careers) | 10 | 2026-09-18T16:03:50.560Z | True |
| Lovable (`lovable`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/lovable) | 81 | 2026-09-14T09:59:17.612Z | True |
| Luma (`luma`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/lumaai/) | 40 | 2026-09-19T16:45:31.913Z | True |
| Lyzr (`lyzr`) | Keka ATS | [lyzr.keka.com](https://lyzr.keka.com/careers) | 16 | 2026-09-24T10:20:47.867Z | True |
| M2P Fintech (`m2p-fintech`) | Darwinbox | [m2p.darwinbox.in](https://m2p.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 31 | 2026-09-26T18:13:48.617Z | True |
| MakeMyTrip (`makemytrip`) | Darwinbox | [gommt.darwinbox.in](https://gommt.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 72 | 2026-09-18T16:08:04.986Z | True |
| Marketfeed (`marketfeed`) | Reczee | [jobs.reczee.com](https://jobs.reczee.com/marketfeed) | 0 | 2026-09-21T07:41:44.115Z | True |
| Matillion (`matillion`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/matillion) | 18 | 2026-09-18T15:56:16.770Z | True |
| Meesho (`meesho`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/meesho) | 49 | 2026-09-16T18:01:11.647Z | True |
| Mem0 (`mem0`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/mem0) | 2 | 2026-09-24T09:45:41.706Z | True |
| Meragi (`meragi`) | Keka ATS | [meragi.keka.com](https://meragi.keka.com/careers) | 21 | 2026-09-16T18:03:41.427Z | True |
| Metaforms (`metaforms`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/metaforms) | 3 | 2026-09-18T15:44:41.975Z | True |
| Metropolis (`metropolis`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/metropolis) | 87 | 2026-09-20T17:42:49.542Z | True |
| Midjourney (`midjourney`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/midjourney) | 22 | 2026-09-19T16:46:08.787Z | True |
| MindTickle (`mindtickle`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/mindtickle) | 19 | 2026-09-18T15:56:29.971Z | True |
| Mintifi (`mintifi`) | Keka ATS | [mintifi.keka.com](https://mintifi.keka.com/careers) | 0 | 2026-09-21T16:30:39.255Z | True |
| Mistral AI (`mistral-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/mistral.ai) | 199 | 2026-09-19T16:48:17.106Z | True |
| Mitti Labs (`mitti-labs`) | Workable | [apply.workable.com](https://apply.workable.com/mitti-labs) | 4 | 2026-09-14T09:23:49.544Z | True |
| Mobbin (`mobbin`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/mobbin.com) | 4 | 2026-09-24T09:46:12.056Z | True |
| Modular (`modular`) | Gem Jobs | [jobs.gem.com](https://jobs.gem.com/modular) | 17 | 2026-09-26T18:17:19.711Z | True |
| MoEngage (`moengage`) | Trakstar | [moengage.hire.trakstar.com](https://moengage.hire.trakstar.com) | 23 | 2026-09-14T13:20:03.399Z | True |
| Moment (`moment`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/moment) | 12 | 2026-09-25T09:36:02.478Z | True |
| Mosaic Wellness (`mosaic-wellness`) | Keka ATS | [mosaicwellness.keka.com](https://mosaicwellness.keka.com/careers) | 29 | 2026-09-14T13:05:12.266Z | True |
| Motion (`motion`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/motion) | 3 | 2026-09-18T16:02:17.820Z | True |
| Moveworks (`moveworks`) | SmartRecruiters | [www.moveworks.com](https://www.moveworks.com/us/en/company/careers) | 85 | 2026-05-22T13:04:48.111Z | True |
| Mudrex (`mudrex`) | Manatal | [mudrex.careers-page.com](https://mudrex.careers-page.com/) | 10 | 2026-09-19T17:04:10.506Z | True |
| Multiplier (`multiplier`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/usemultiplier) | 99 | 2026-09-16T18:02:49.051Z | True |
| Multiverse (`multiverse`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/multiverse) | 19 | 2026-09-21T16:22:24.757Z | True |
| Mysten Labs (`mysten-labs`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/mystenlabs) | 2 | 2026-09-14T09:59:32.620Z | True |
| Nabla (`nabla`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/nabla) | 19 | 2026-09-24T09:47:03.779Z | True |
| Nanonets (`nanonets`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/nanonets) | 5 | 2026-09-26T17:55:17.480Z | True |
| Nas (`nas`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/nascompany) | 6 | 2026-09-14T09:22:22.442Z | True |
| Navan (`navan`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/tripactions) | 212 | 2026-09-26T18:07:04.227Z | True |
| Neara (`neara`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/neara) | 57 | 2026-09-14T10:00:12.199Z | True |
| Neko Health (`neko-health`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/neko-health) | 102 | 2026-09-26T17:56:48.920Z | True |
| Netomi (`netomi`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/netomi) | 23 | 2026-09-24T13:18:35.310Z | True |
| Neuralink (`neuralink`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/neuralink) | 77 | 2026-09-18T15:51:13.066Z | True |
| Neuron7.ai (`neuron7-ai`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/neuron7) | 18 | 2026-09-16T18:01:21.043Z | True |
| Newtrace (`newtrace`) | Reczee | [jobs.reczee.com](https://jobs.reczee.com/newtrace) | 6 | 2026-09-19T16:59:16.579Z | True |
| Nexthop AI (`nexthop-ai`) | BambooHR | [nexthopai.bamboohr.com](https://nexthopai.bamboohr.com/careers) | 38 | 2026-09-24T10:56:07.476Z | True |
| Neysa (`neysa`) | WordPress Jobs | [neysa.ai](https://neysa.ai/careers/job-openings/) | 20 | 2026-09-14T15:15:26.438Z | True |
| Ninjacart (`ninjacart`) | Freshteam Jobs | [ninjacart.freshteam.com](https://ninjacart.freshteam.com/jobs) | 23 | 2026-09-28T05:47:13.546Z | True |
| Nium (`nium`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/nium) | 26 | 2026-09-18T15:56:43.372Z | True |
| NoBroker (`nobroker`) | Darwinbox | [nobroker.darwinbox.in](https://nobroker.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 3 | 2026-09-24T10:26:43.959Z | True |
| Notable Health (`notable-health`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/notable) | 11 | 2026-09-24T09:47:34.221Z | True |
| Nothing (`nothing`) | Greenhouse Jobs | [job-boards.eu.greenhouse.io](https://job-boards.eu.greenhouse.io/embed/job_board?for=nothing) | 9 | 2026-09-23T21:14:51.419Z | True |
| Notion (`notion`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/notion) | 172 | 2026-09-14T10:01:06.830Z | True |
| Nox Metals (`nox-metals`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/nox-metals/jobs) | 6 | 2026-09-18T16:00:01.615Z | True |
| Observe.AI (`observe-ai`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/observeai) | 17 | 2026-09-14T12:56:58.059Z | True |
| Ocrolus (`ocrolus`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/ocrolusinc) | 8 | 2026-09-26T18:07:20.921Z | True |
| Olema Oncology (`olema-oncology`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/olema) | 17 | 2026-09-14T12:57:36.830Z | True |
| Oligo Security (`oligo-security`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/oligosecurity/5A.00B) | 9 | 2026-09-25T09:35:33.314Z | True |
| Oneleet (`oneleet`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/oneleet) | 19 | 2026-09-14T10:01:18.331Z | True |
| OnePay (`onepay`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/oneapp) | 44 | 2026-09-14T10:01:55.476Z | True |
| OneTrust (`onetrust`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/onetrust) | 93 | 2026-09-14T12:58:14.555Z | True |
| Ontic (`ontic`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Ontic) | 23 | 2026-09-14T12:27:35.724Z | True |
| OpenAI (`openai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/openai) | 836 | 2026-09-21T16:34:05.778Z | True |
| Openhouse (`openhouse`) | Freshteam Jobs | [openhouse-talent.freshteam.com](https://openhouse-talent.freshteam.com/jobs) | 3 | 2026-09-14T12:50:16.471Z | True |
| OpenTable (`opentable`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/opentable) | 104 | 2026-09-24T10:05:31.408Z | True |
| Orca Bio (`orca-bio`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/orcabiosystems) | 44 | 2026-09-18T15:57:01.931Z | True |
| Orkes (`orkes`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/orkes) | 21 | 2026-09-19T16:55:02.435Z | True |
| Outset (`outset`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/outset) | 18 | 2026-09-14T10:02:29.533Z | True |
| Pacific Fusion (`pacificfusion`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/pacificfusion) | 30 | 2026-09-24T10:06:09.000Z | True |
| Pareto (`pareto`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/pareto-ai) | 2 | 2026-09-14T10:02:43.629Z | True |
| Payhawk (`payhawk`) | Greenhouse Jobs | [job-boards.eu.greenhouse.io](https://job-boards.eu.greenhouse.io/payhawkio) | 50 | 2026-09-24T10:06:44.191Z | True |
| Pebble (`pebble`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/pebblelife) | 8 | 2026-09-14T13:08:36.749Z | True |
| Pepper Content (`pepper-content`) | Freshteam Jobs | [peppercontent-talent.freshteam.com](https://peppercontent-talent.freshteam.com/jobs) | 9 | 2026-09-24T10:28:02.817Z | True |
| Periodic Labs (`periodic-labs`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/periodic-labs) | 28 | 2026-09-14T10:03:15.312Z | True |
| Perplexity (`perplexity`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Perplexity) | 121 | 2026-09-24T09:49:05.331Z | True |
| Phantom (`phantom`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/phantom) | 11 | 2026-09-14T10:03:44.909Z | True |
| PharmEasy (`pharmeasy`) | Darwinbox | [myhr.darwinbox.in](https://myhr.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 8 | 2026-09-18T16:08:16.120Z | True |
| PhonePe (`phonepe`) | SmartRecruiters | [jobs.smartrecruiters.com](https://jobs.smartrecruiters.com/PHONEPELIMITED) | 79 | 2026-09-18T16:10:28.053Z | True |
| Pice (`pice`) | Reczee | [jobs.reczee.com](https://jobs.reczee.com/pice) | 5 | 2026-09-26T18:17:51.766Z | True |
| Pine Labs (`pine-labs`) | TurboHire | [pinelabsgroup.turbohire.co](https://pinelabsgroup.turbohire.co) | 0 | 2026-09-14T15:16:05.133Z | True |
| Pixxel (`pixxel`) | Darwinbox | [pixxel.darwinbox.in](https://pixxel.darwinbox.in/ms/candidatev2/main/careers/home) | 10 | 2026-09-14T12:48:37.798Z | True |
| PlanA.Earth (`plana-earth`) | Workable | [apply.workable.com](https://apply.workable.com/plana) | 0 | 2026-09-14T13:23:37.333Z | True |
| Plane (`plane`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/plane) | 33 | 2026-09-14T12:28:10.100Z | True |
| PlaySimple Games (`playsimple-games`) | ZohoRecruit | [careers.playsimple.in](https://careers.playsimple.in/jobs/Careers) | 23 | 2026-06-02T16:54:29.549Z | True |
| Plivo (`plivo`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/plivo) | 0 | 2026-09-14T13:12:17.037Z | True |
| Plum (`plum`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/plumhq) | 44 | 2026-09-14T13:09:02.733Z | True |
| Polar Analytics (`polar-analytics`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/polar) | 2 | 2026-09-14T12:28:25.581Z | True |
| Porter (`porter`) | Darwinbox | [porter.darwinbox.in](https://porter.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 10 | 2026-09-28T05:46:54.408Z | True |
| Posh (`posh`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/posh-ai) | 5 | 2026-09-14T12:28:41.942Z | True |
| Postman (`postman`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/postman) | 0 | 2026-09-26T18:08:16.770Z | True |
| Procol (`procol`) | WordPress Jobs | [www.procol.ai](https://www.procol.ai/careers/) | 6 | 2026-09-24T10:31:19.055Z | True |
| Profound (`profound`) | Custom Ashby Embed | [www.tryprofound.com](https://www.tryprofound.com/careers) | 133 | 2026-09-14T09:21:35.470Z | True |
| Progress (`progress`) | Jobvite | [jobs.jobvite.com](https://jobs.jobvite.com/progress/jobs) | 30 | 2026-09-21T16:31:56.229Z | True |
| PromptQL (`promptql`) | Gem Jobs | [jobs.gem.com](https://jobs.gem.com/promptql) | 4 | 2026-09-26T18:17:42.170Z | True |
| Proxima Fusion (`proxima-fusion`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/proxima-fusion) | 45 | 2026-09-18T15:45:12.959Z | True |
| Purplle (`purplle`) | TurboHire | [purplle.turbohire.co](https://purplle.turbohire.co/dashboardv2?orgId=3ed17e54-f66f-4ade-90b9-ef064dc6fbd6&type=0) | 62 | 2026-09-28T05:59:05.751Z | True |
| Qoala (`qoala`) | Darwinbox | [qoala.darwinbox.com](https://qoala.darwinbox.com/ms/candidatev2/main/careers/allJobs) | 64 | 2026-09-24T10:10:33.947Z | True |
| Qure.ai (`qure-ai`) | ZohoRecruit | [career.qure.ai](https://career.qure.ai/jobs/Careers) | 15 | 2026-05-11T14:45:54.392Z | True |
| Rain (`rain`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/rain) | 44 | 2026-09-18T15:45:45.861Z | True |
| Ramp (`ramp`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/ramp) | 158 | 2026-09-26T17:58:58.050Z | True |
| Raven (`raven`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/raven/jobs) | 1 | 2026-09-18T16:00:15.219Z | True |
| Razorpay (`razorpay`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/razorpaysoftwareprivatelimited) | 16 | 2026-09-18T15:51:52.597Z | True |
| Redpanda (`redpanda`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/redpanda-data/) | 19 | 2026-09-18T15:46:09.949Z | True |
| Reducto (`reducto`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/reducto) | 40 | 2026-09-14T12:29:17.987Z | True |
| Reflection (`reflection`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/reflectionai) | 49 | 2026-09-14T12:29:50.585Z | True |
| Regrello (`regrello`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/regrello) | 0 | 2026-09-14T13:12:49.414Z | True |
| Reka AI (`reka-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Reka) | 10 | 2026-09-22T15:46:50.938Z | True |
| Relevance AI (`relevance-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/relevanceai) | 4 | 2026-09-15T12:57:19.396Z | True |
| Replit (`replit`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/replit) | 77 | 2026-09-24T09:50:11.894Z | True |
| Resolve AI (`resolve-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/resolveai) | 15 | 2026-09-26T19:13:48.994Z | True |
| Revefi (`revefi`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/revefi) | 4 | 2026-09-26T18:11:07.273Z | True |
| Rippling (`rippling`) | Rippling | [ats.rippling.com](https://ats.rippling.com/rippling/jobs) | 27 | 2026-09-26T18:13:20.768Z | True |
| RobCo (`robco`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/robco) | 42 | 2026-09-26T18:00:38.013Z | True |
| Rocketlane (`rocketlane`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/rocketlane) | 51 | 2026-09-24T10:18:59.194Z | True |
| Roofstock (`roofstock`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/roofstock) | 17 | 2026-09-16T17:58:45.598Z | True |
| Rothy's (`rothy-s`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Rothys) | 76 | 2026-09-14T12:30:40.073Z | True |
| Rox (`rox`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Rox-Data-Corp) | 23 | 2026-09-15T18:56:48.475Z | True |
| SaaS Labs (`saas-labs`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/saas-labs) | 18 | 2026-09-18T16:02:32.374Z | True |
| SailPoint (`sailpoint`) | Workday | [sailpoint.wd1.myworkdayjobs.com](https://sailpoint.wd1.myworkdayjobs.com/SailPoint) | 116 | 2026-09-19T16:58:28.185Z | True |
| SambaNova (`sambanova`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=sambanovasystems) | 55 | 2026-09-19T16:55:34.757Z | True |
| Sanity (`sanity`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/sanity) | 46 | 2026-09-14T12:31:30.171Z | True |
| Sarasanalytics (`sarasanalytics`) | Keka ATS | [sarasanalytics.keka.com](https://sarasanalytics.keka.com/careers) | 4 | 2026-09-14T15:14:36.180Z | True |
| Saronic Technologies (`saronic-technologies`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/saronic) | 253 | 2026-09-21T17:01:30.788Z | True |
| Sarvam AI (`sarvam-ai`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/sarvam) | 61 | 2026-09-24T09:50:45.758Z | True |
| Saviynt (`saviynt`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/saviynt) | 83 | 2026-09-24T10:13:03.089Z | True |
| Scale AI (`scale-ai`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/scaleai) | 210 | 2026-09-24T10:07:34.613Z | True |
| ScaleOps (`scaleops`) | Comeet Jobs | [www.comeet.com](https://www.comeet.com/jobs/scaleops/99.003) | 53 | 2026-09-24T10:25:37.971Z | True |
| Scrut (`scrut`) | Keka ATS | [scrut.keka.com](https://scrut.keka.com/careers) | 8 | 2026-09-24T10:21:06.232Z | True |
| Semgrep (`semgrep`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/semgrep) | 10 | 2026-09-16T17:54:24.078Z | True |
| ShareChat (`sharechat`) | MyNextHire ATS | [sharechat.mynexthire.com](https://sharechat.mynexthire.com/employer/jobs) | 4 | 2026-09-24T10:22:59.712Z | True |
| Shiprocket (`shiprocket`) | WordPress Jobs | [careers.shiprocket.in](https://careers.shiprocket.in) | 2 | 2026-09-24T10:31:48.912Z | True |
| ShopDeck (`shopdeck`) | PyjamHR ATS | [app.pyjamahr.com](https://app.pyjamahr.com/careers?company=ShopDeck&company_uuid=AA7DCF5D05) | 10 | 2026-09-21T16:31:07.844Z | True |
| Sibros (`sibros`) | Rippling | [ats.rippling.com](https://ats.rippling.com/sibros-technologies/jobs) | 7 | 2026-09-15T12:58:24.515Z | True |
| Sierra (`sierra`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/sierra) | 210 | 2026-09-14T12:33:20.585Z | True |
| SiftHub (`sifthub`) | Trakstar | [sifthub.hire.trakstar.com](https://sifthub.hire.trakstar.com) | 5 | 2026-09-18T16:10:48.758Z | True |
| Sigmoid (`sigmoid`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/sigmoid) | 35 | 2026-09-26T18:08:55.003Z | True |
| Skild AI (`skild-ai`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/skildai-careers) | 43 | 2026-09-24T10:08:10.597Z | True |
| slice (`slice`) | MyNextHire ATS | [slice.bank.in](https://slice.bank.in/careers/open-positions/) | 24 | 2026-05-10T10:18:16.850Z | True |
| smallcase (`smallcase`) | PyjamHR ATS | [jobs.pyjamahr.com](https://jobs.pyjamahr.com/smallcase) | 15 | 2026-09-16T18:05:03.135Z | True |
| Snitch (`snitch`) | Keka ATS | [snitch.keka.com](https://snitch.keka.com/careers) | 29 | 2026-09-24T10:21:09.305Z | True |
| Snorkel AI (`snorkel-ai`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/snorkelai) | 39 | 2026-09-18T15:52:25.790Z | True |
| SolarSquare (`solarsquare`) | Keka ATS | [solarsquare.keka.com](https://solarsquare.keka.com/careers) | 174 | 2026-09-14T13:05:40.322Z | True |
| Solidroad (`solidroad`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/solidroad) | 7 | 2026-09-24T09:51:06.306Z | True |
| Spinny (`spinny`) | Darwinbox | [spinzone.darwinbox.in](https://spinzone.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 14 | 2026-09-15T19:05:51.129Z | True |
| SpotDraft (`spotdraft`) | Darwinbox | [spotdraft.darwinbox.in](https://spotdraft.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 1 | 2026-09-18T16:08:27.097Z | True |
| Sprinto (`sprinto`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/Sprinto) | 37 | 2026-09-18T15:57:14.807Z | True |
| Spyne (`spyne`) | Keka ATS | [spyneai.keka.com](https://spyneai.keka.com/careers) | 24 | 2026-09-24T10:21:36.997Z | True |
| SquadStack (`squadstack`) | Keka ATS | [squadrun.keka.com](https://squadrun.keka.com/careers) | 12 | 2026-09-24T10:21:50.916Z | True |
| Stacks (`stacks`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/stacks) | 9 | 2026-09-16T17:54:52.368Z | True |
| Starling Bank (`starling-bank`) | Workable | [apply.workable.com](https://apply.workable.com/starling-bank) | 55 | 2026-09-20T17:02:50.846Z | True |
| StarSling (`starsling`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/starsling/jobs) | 0 | 2026-09-14T13:26:33.855Z | True |
| StashAway (`stashaway`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/stashaway) | 11 | 2026-09-18T16:03:12.279Z | True |
| Strava (`strava`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/strava) | 27 | 2026-09-14T12:34:00.736Z | True |
| Stripe (`stripe`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/stripe) | 671 | 2026-09-21T16:29:20.338Z | True |
| Suger (`suger`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/suger) | 13 | 2026-09-18T15:57:27.711Z | True |
| Suki (`suki`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/embed/job_board?for=suki) | 11 | 2026-09-24T10:08:49.164Z | True |
| Suno (`suno`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/suno) | 66 | 2026-09-14T12:34:54.937Z | True |
| Supabase (`supabase`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/supabase) | 59 | 2026-09-14T12:35:29.832Z | True |
| SuperK (`superk`) | Keka ATS | [superk.keka.com](https://superk.keka.com/careers) | 12 | 2026-09-24T10:22:01.440Z | True |
| SuperKalam (`superkalam`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/superkalam/jobs) | 11 | 2026-09-18T16:00:29.717Z | True |
| Synthesia (`synthesia`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/synthesia) | 63 | 2026-09-24T09:51:46.631Z | True |
| Synthflow AI (`synthflow-ai`) | Deel | [jobs.deel.com](https://jobs.deel.com/synthflow-ai) | 5 | 2026-09-15T12:57:45.532Z | True |
| Synthio Labs (`synthio-labs`) | Gem Jobs | [jobs.gem.com](https://jobs.gem.com/synthio-labs) | 10 | 2026-09-21T16:32:42.468Z | True |
| Tabs (`tabs`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/Tabs) | 20 | 2026-09-21T16:27:56.575Z | True |
| Tala (`tala`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/tala) | 6 | 2026-09-24T10:13:23.279Z | True |
| Tamara (`tamara`) | Greenhouse Jobs | [job-boards.eu.greenhouse.io](https://job-boards.eu.greenhouse.io/tamara) | 32 | 2026-09-24T10:09:22.756Z | True |
| Tata 1mg (`tata-1mg`) | Darwinbox | [1mg.darwinbox.in](https://1mg.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 10 | 2026-09-16T18:05:34.277Z | True |
| Tekion (`tekion`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/tekion) | 127 | 2026-09-19T16:49:29.190Z | True |
| Temporal (`temporal`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/temporal) | 103 | 2026-09-24T09:52:44.297Z | True |
| Tennr (`tennr`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/tennr) | 23 | 2026-09-14T12:36:12.989Z | True |
| TensorWave (`tensorwave`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/tensorwave) | 42 | 2026-09-16T17:55:24.475Z | True |
| Tessell (`tessell`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/tessellinc) | 0 | 2026-09-24T10:10:17.699Z | True |
| Testzeus (`testzeus`) | Custom ATS (TestZeus) | [testzeus.com](https://testzeus.com/jobs) | 3 | 2026-09-26T18:18:08.291Z | True |
| The/Nudge Institute (`the-nudge-institute`) | Keka ATS | [thenudge.keka.com](https://thenudge.keka.com/careers) | 41 | 2026-09-19T16:56:08.174Z | True |
| The Whole Truth Foods (`the-whole-truth-foods`) | Keka ATS | [thewholetruthfoods.keka.com](https://thewholetruthfoods.keka.com/careers) | 16 | 2026-09-14T13:05:53.903Z | True |
| Thena (`thena`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/thena) | 0 | 2026-09-26T18:10:09.647Z | True |
| Thinking Machines Lab (`thinking-machines-lab`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/ThinkingMachines) | 38 | 2026-09-14T13:28:47.683Z | True |
| ThoughtSpot (`thoughtspot`) | Workday | [thoughtspot.wd5.myworkdayjobs.com](https://thoughtspot.wd5.myworkdayjobs.com/careers) | 0 | 2026-09-18T16:05:21.489Z | True |
| Thunkable (`thunkable`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/thunkable) | 2 | 2026-09-26T18:11:26.224Z | True |
| Tide (`tide`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/tide) | 85 | 2026-09-14T12:58:55.082Z | True |
| Tilt (`tilt`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/tilthq) | 35 | 2026-09-14T12:36:57.035Z | True |
| Toddle (`toddle`) | Keka ATS | [toddle.keka.com](https://toddle.keka.com/careers) | 24 | 2026-09-18T16:04:01.657Z | True |
| Together AI (`together-ai`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/togetherai) | 68 | 2026-09-16T18:15:01.830Z | True |
| Tokopedia (`tokopedia`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/GoToGroup) | 35 | 2026-09-25T09:35:06.075Z | True |
| Tracxn (`tracxn`) | Trakstar | [tracxn.hire.trakstar.com](https://tracxn.hire.trakstar.com/jobs) | 1 | 2026-09-24T10:29:25.592Z | True |
| Treebo Hotels (`treebo-hotels`) | Darwinbox | [treebo.darwinbox.in](https://treebo.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 80 | 2026-09-21T16:32:26.080Z | True |
| Truecaller (`truecaller`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/truecaller) | 28 | 2026-09-18T15:52:57.101Z | True |
| Truewind (`truewind`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/truewind/jobs) | 6 | 2026-09-18T16:00:41.261Z | True |
| Tubi (`tubi`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/tubitv) | 26 | 2026-09-24T10:10:57.887Z | True |
| Twin Health (`twin-health`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/twinhealth) | 35 | 2026-09-18T15:53:30.362Z | True |
| Typeface (`typeface`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/typeface) | 16 | 2026-09-14T12:59:34.553Z | True |
| UiPath (`uipath`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/uipath) | 214 | 2026-09-14T12:44:01.018Z | True |
| Unacademy (`unacademy`) | Darwinbox | [unacademy.darwinbox.in](https://unacademy.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 7 | 2026-09-26T18:14:55.341Z | True |
| Uniphore (`uniphore`) | Workday | [uniphore.wd503.myworkdayjobs.com](https://uniphore.wd503.myworkdayjobs.com/Uniphore) | 35 | 2026-09-18T16:05:55.702Z | True |
| Uniqode (`uniqode`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/uniqode) | 0 | 2026-09-24T10:19:59.000Z | True |
| Upstox (`upstox`) | Darwinbox | [upstox.darwinbox.in](https://upstox.darwinbox.in/ms/candidatev2/main/careers/allJobs) | 24 | 2026-09-26T18:16:24.806Z | True |
| Vegapay (`vegapay`) | Keka ATS | [vegapay.keka.com](https://vegapay.keka.com/careers) | 6 | 2026-09-14T13:06:10.823Z | True |
| Venn (`venn`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/venncity) | 9 | 2026-09-18T15:54:01.866Z | True |
| Vercel (`vercel`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/vercel) | 85 | 2026-09-18T15:54:36.019Z | True |
| Verily (`verily`) | Workday | [verily.wd1.myworkdayjobs.com](https://verily.wd1.myworkdayjobs.com/Verily_Careers) | 76 | 2026-09-15T09:30:29.526Z | True |
| Verkada (`verkada`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/verkada) | 293 | 2026-09-14T13:00:44.675Z | True |
| Versa Networks (`versa-networks`) | Workable | [apply.workable.com](https://apply.workable.com/versa-networks/) | 30 | 2026-09-19T17:02:34.809Z | True |
| Waabi (`waabi`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/waabi) | 86 | 2026-09-24T10:13:41.065Z | True |
| Wayground (`wayground`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/Wayground) | 10 | 2026-09-18T16:29:57.735Z | True |
| Weee! (`weee`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/weee) | 13 | 2026-09-21T16:29:51.128Z | True |
| Whatfix (`whatfix`) | Trakstar | [whatfix101.hire.trakstar.com](https://whatfix101.hire.trakstar.com/jobs) | 25 | 2026-09-26T18:18:32.556Z | True |
| Whatnot (`whatnot`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/whatnot) | 144 | 2026-09-16T17:56:31.591Z | True |
| Wheel (`wheel`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/wheel) | 6 | 2026-09-14T09:21:16.427Z | True |
| Willow Voice (`willow-voice`) | Y Combinator Jobs | [www.ycombinator.com](https://www.ycombinator.com/companies/willow/jobs) | 4 | 2026-09-24T10:14:31.322Z | True |
| Wingify (`wingify`) | Keka ATS | [wingify.keka.com](https://wingify.keka.com/careers) | 18 | 2026-09-24T10:22:22.479Z | True |
| Wintermute (`wintermute`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/wintermute-trading) | 21 | 2026-09-19T16:55:57.463Z | True |
| Wise (`wise`) | SmartRecruiters | [jobs.smartrecruiters.com](https://jobs.smartrecruiters.com/wise) | 425 | 2026-09-20T09:12:33.603Z | True |
| Wishlink (`wishlink`) | Keka ATS | [wishlink.keka.com](https://wishlink.keka.com/careers) | 11 | 2026-09-24T10:22:42.296Z | True |
| Wisprflow (`wisprflow`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/wispr-flow) | 29 | 2026-09-14T12:44:54.906Z | True |
| Wiz (`wiz`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/wizinc) | 139 | 2026-09-16T18:00:33.843Z | True |
| WorkOS (`workos`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/workos) | 31 | 2026-09-19T16:49:42.329Z | True |
| Writer (`writer`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/writer) | 88 | 2026-09-18T15:46:56.428Z | True |
| xAI (`xai`) | Greenhouse Jobs | [boards.greenhouse.io](https://boards.greenhouse.io/xai) | 255 | 2026-09-14T13:01:47.672Z | True |
| Xflow (`xflow`) | Freshteam Jobs | [xflowpay.freshteam.com](https://xflowpay.freshteam.com/jobs) | 12 | 2026-09-26T18:16:55.274Z | True |
| Yoga Bar (`yoga-bar`) | Freshteam Jobs | [yogabars.freshteam.com](https://yogabars.freshteam.com/jobs) | 17 | 2026-09-14T12:50:33.234Z | True |
| You (`you`) | Workable | [apply.workable.com](https://apply.workable.com/youtrip) | 5 | 2026-09-24T10:31:06.535Z | True |
| Yugabyte (`yugabyte`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/yugabyte) | 15 | 2026-09-24T10:11:35.941Z | True |
| Yupp (`yupp`) | Ashby Jobs Board | [jobs.ashbyhq.com](https://jobs.ashbyhq.com/yupp-ai) | 0 | 2026-09-14T12:45:35.639Z | True |
| Zamp (`zamp`) | Kula ATS | [careers.kula.ai](https://careers.kula.ai/zamp-ai) | 10 | 2026-09-14T13:09:16.493Z | True |
| Zeni (`zeni`) | BambooHR | [zeni.bamboohr.com](https://zeni.bamboohr.com/careers) | 3 | 2026-09-24T10:25:02.620Z | True |
| Zenoti (`zenoti`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/zenoti) | 49 | 2026-09-28T05:41:59.578Z | True |
| Zenyum (`zenyum`) | Teamtailor | [careers.zenyum.com](https://careers.zenyum.com) | 9 | 2026-06-03T09:07:24.625Z | True |
| Zeotap (`zeotap`) | Recruitee | [zeotap.com](https://zeotap.com/careers/) | 1 | 2026-09-18T16:04:21.057Z | True |
| Zeta (`zeta`) | Lever Jobs Board | [jobs.lever.co](https://jobs.lever.co/zeta) | 22 | 2026-09-24T10:13:57.894Z | True |
| Zetwerk (`zetwerk`) | SenseHQ | [zetwerk.sensehq.com](https://zetwerk.sensehq.com/careers/jobs) | 32 | 2026-09-24T10:56:32.407Z | True |
| Zilo (`zilo`) | Workable | [apply.workable.com](https://apply.workable.com/zilo-1) | 2 | 2026-09-21T16:33:12.108Z | True |
| Zipstack (`zipstack`) | Freshteam Jobs | [zipstack.freshteam.com](https://zipstack.freshteam.com/jobs) | 0 | 2026-09-24T10:28:15.371Z | True |
| Zluri (`zluri`) | Keka ATS | [zluri.keka.com](https://zluri.keka.com/careers) | 8 | 2026-09-26T18:12:51.802Z | True |
| Zoca (`zoca`) | PyjamHR ATS | [app.pyjamahr.com](https://app.pyjamahr.com/careers?company=ZOCAAI&company_uuid=6FFECB46A0) | 10 | 2026-09-21T16:31:36.834Z | True |
| Zolve (`zolve`) | Freshteam Jobs | [zolve.freshteam.com](https://zolve.freshteam.com/jobs) | 19 | 2026-09-16T18:06:06.441Z | True |
| Zscaler (`zscaler`) | Greenhouse Jobs | [job-boards.greenhouse.io](https://job-boards.greenhouse.io/zscaler) | 372 | 2026-09-14T13:03:31.824Z | True |

## Limits and proof discipline

- This report concerns data quality and observability. It does not establish a paid-data entitlement bypass or a private-user-data leak.
- Static client-side assets can establish what is publicly shipped; they cannot establish backend scheduler timing, retry logic, scraper source code, or database freshness.
- Every anomaly remains a candidate unless the underlying records themselves conflict or the separate primary-source verification reproduces the discrepancy.
- No outbound notifications, applications, login actions, destructive actions, or private-account access were used for this inventory analysis.
