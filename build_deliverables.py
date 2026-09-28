#!/usr/bin/env python3
"""Create the shareable inventory and report from the frozen public audit."""
import collections
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def cell(value):
    return str(value if value is not None else 'Unknown').replace('|', '\\|').replace('\n', ' ')


def main():
    analysis = json.loads((BASE / 'inventory/analysis.json').read_text())
    progress = json.loads((BASE / 'inventory/progress.json').read_text())
    links = json.loads((BASE / 'inventory/career-link-checks.json').read_text())
    assert analysis['coverage_complete'] and progress.get('complete'), 'Finish collection and analysis first'
    companies = analysis['companies']
    assert len(companies) == 460 and len(links['results']) == 460
    by_link = {x['slug']: x for x in links['results']}
    records = [json.loads((BASE / 'inventory/companies' / (c['slug'] + '.json')).read_text()) for c in companies]
    total = sum(x['job_count'] for x in records)
    assert total == analysis['totals']['jobs']
    source_counts = analysis['source_inventory']
    link_counts = collections.Counter(x['classification'] for x in links['results'])
    missing = analysis['totals']['posted_date_missing_or_invalid']
    same_day = analysis['totals']['posted_date_equals_company_refresh_day']
    refresh = analysis['refresh_age_days']
    old = sorted((x for x in companies if (x.get('refresh_age_days') or 0) > 30), key=lambda c: c['refresh_age_days'], reverse=True)
    failed = [x for x in links['results'] if x['classification'] == 'not-found']
    inventory = []
    rows = []
    for c in companies:
        check = by_link[c['slug']]
        record = next(x for x in records if x['slug'] == c['slug'])
        item = {k: c.get(k) for k in ['slug', 'name', 'company_id', 'website_url', 'careers_url', 'source',
                'crawl_method', 'crawl_status', 'last_updated', 'refresh_age_days', 'job_count',
                'distinct_canonical_apply_urls', 'show_on_map', 'careers_url_last_updated', 'module_url']}
        item.update({'link_check': check, 'module_sha256': record['fetch'].get('sha256'),
                     'details_file': 'inventory/companies/' + c['slug'] + '.json'})
        inventory.append(item)
        company_link = f"[{c['name']}](inventory/companies/{c['slug']}.json)"
        rows.append('| ' + ' | '.join(cell(v) for v in [company_link, c['slug'], c['source'], c['careers_url'],
            c['crawl_method'], c['crawl_status'], c['last_updated'], c['job_count'],
            c['distinct_canonical_apply_urls'], check['classification']]) + ' |')
    dump(BASE / 'company-source-index.json', {'observed_date': '2026-09-28', 'deployment': analysis['deployment'],
        'scope': 'All 460 company modules in the pinned public client index; backend parity unknown.',
        'companies': inventory})
    (BASE / 'company-source-index.md').write_text('# All 460 companies and their recorded sources\n\n'
        'Observed 28 September 2026. Source and crawl fields are claims in the published data, not backend logs. '
        'Rows are role/location records; canonical URL counts remove fragments and do not guarantee distinct vacancies. '
        'A responding careers URL does not prove a valid board; access restrictions and transport failures are inconclusive.\n\n'
        '| Company | Slug | Recorded source | Careers URL | Method | Crawl status | Last updated (UTC) | Role rows | Canonical URLs | URL check |\n'
        '|---|---|---|---|---|---|---|---:|---:|---|\n' + '\n'.join(rows) + '\n')
    dump(BASE / 'job-inventory.json', {'observed_date': '2026-09-28', 'role_location_rows': total,
        'note': 'Sanitized public job metadata. Original publication dates may be absent or incorrect; no private-user data.',
        'companies': [{'slug': x['slug'], 'company': x['company']['company_name_brand'], 'source': x['job_metadata'],
                       'jobs': x['jobs'], 'locations': x['locations']} for x in records]})
    html_rows = []
    for c in inventory:
        esc = html.escape
        url = c['careers_url'] or ''
        safe = url.startswith(('https://', 'http://'))
        anchor = '<a href="' + esc(url, quote=True) + '" target="_blank" rel="noopener noreferrer">' + esc(url) + '</a>' if safe else esc(url)
        html_rows.append('<tr>' + ''.join('<td>' + v + '</td>' for v in [esc(c['name']), esc(c['slug']),
            esc(c['source'] or 'Unknown'), anchor, str(c['job_count']),
            esc(c['last_updated'] or 'Unknown'), esc(c['link_check']['classification']),
            '<a href="' + c['details_file'] + '">Evidence JSON</a>']) + '</tr>')
    (BASE / 'company-source-index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>NextDoor.Company | 460-company source inventory</title>
<style>body{font:15px system-ui,sans-serif;margin:36px;color:#182632;background:#f6f8fa}h1{font-size:30px}p{max-width:1000px;line-height:1.6}input{font:inherit;padding:12px;width:min(600px,90%);border:1px solid #abc;border-radius:6px}table{border-collapse:collapse;background:white;margin-top:22px;width:100%}th,td{text-align:left;padding:12px;border-bottom:1px solid #dce3e8;vertical-align:top}th{background:#153344;color:white;position:sticky;top:0}td:nth-child(4){overflow-wrap:anywhere;max-width:350px}a{color:#146884}.meta{color:#526577}#count{font-weight:600}tr[hidden]{display:none}</style>
<h1>Every company in the public index</h1><p class="meta">Observed 28 September 2026 • 460 companies • ''' + f'{total:,}' + ''' role/location rows</p>
<p>Search by company, ATS, source URL, date, or link result. The recorded source is metadata published by NextDoor; it is not a backend execution trace. A responding URL may still contain an empty or invalid board. All source URLs and individual sanitized evidence records are linked below.</p>
<label for="search">Filter the inventory</label><p><input id="search" type="search" placeholder="Company, Ashby, Greenhouse, not-found…" autocomplete="off"> <span id="count">460 companies</span></p>
<table><thead><tr><th>Company</th><th>Slug</th><th>Recorded source</th><th>Careers URL</th><th>Role rows</th><th>Last update UTC</th><th>URL check</th><th>Details</th></tr></thead><tbody>''' + ''.join(html_rows) + '''</tbody></table>
<script>const input=document.getElementById('search');const rows=[...document.querySelectorAll('tbody tr')];input.addEventListener('input',()=>{const q=input.value.toLowerCase().trim();let n=0;for(const row of rows){row.hidden=!row.textContent.toLowerCase().includes(q);if(!row.hidden)n++}document.getElementById('count').textContent=n+' companies'});</script></html>''')

    stats = {'companies': 460, 'role_rows': total, 'source_labels': len(source_counts), 'missing_dates': missing,
             'same_day_dates': same_day, 'refresh': refresh, 'link_classifications': dict(link_counts)}
    dump(BASE / 'summary-metrics.json', stats)
    sources_md = '\n'.join('| ' + cell(k) + ' | ' + str(v['company_count']) + ' | ' + str(v['job_count']) + ' |'
                           for k, v in source_counts.items())
    old_md = '\n'.join(f'| {c["name"]} | {c["last_updated"]} | {c["refresh_age_days"]:.1f} | {c["job_count"]} |' for c in old)
    failed_md = '\n'.join('| ' + cell(x['slug']) + ' | ' + cell(x['recorded_careers_url']) + ' | ' + str(x['final_status']) + ' |' for x in failed)
    report = f'''# NextDoor.Company: founder audit

Observed **28 September 2026**. This package covers **all 460 company modules in the pinned public client index**, **{total:,} published role/location rows**, every recorded careers URL, sampled official employer feeds, and the public frontend. It does not claim parity with the authenticated database or access to the backend scraper.

## Assessment

The directory is useful for discovering employers and following their original application links. It is not currently a dependable source of job age, geographic eligibility, or complete live openings without checking the employer. The verified issues affect data trust, lead capture, and paid-listing conversion. No account takeover or cross-user data breach was established.

The strongest example is Postman: NextDoor reports a successful Greenhouse crawl and zero jobs; its recorded board now returns 404, while Postman's official Workday-backed page and public feed list 38 openings. SuperK is a useful positive control: all 12 job IDs match its official Keka feed, but every job references a Denver office despite the official location being Bangalore, India.

## Read this package

- [Founder brief (PDF)](output/pdf/nextdoor-founder-brief.pdf): concise decision and repair brief.
- [Searchable 460-company source index](company-source-index.html), [Markdown index](company-source-index.md), [JSON index](company-source-index.json).
- [Full sanitized job metadata](job-inventory.json): every published role/location row in these modules.
- [Catalog-wide data analysis](data-quality.md) and [machine-readable analysis](inventory/analysis.json).
- [Primary employer comparisons](source-verification.md), with exact source URLs and timestamps.
- [Frontend/API findings](frontend-audit.md), [offline reproductions](frontend-repros/README.md), and [test results](frontend-repros/results.json).
- [Engineering repair specification](ENGINEERING-FIX-PLAN.md): data contracts, employer repairs, rollout order and regression acceptance criteria.
- [Public data boundary evidence](public-data-boundary.md): login preview versus public static records, with screenshots and API controls.
- [Careers URL checks](inventory/career-link-checks.json), [pinned manifest](inventory/module-index.json), and individual records under `inventory/companies/`.

## Where the listings and enrichment come from

The public records name **{len(source_counts)} source labels**. These are labels, not necessarily {len(source_counts)} different vendors: for example, Freshteam/Freshteam Jobs and Ashby/Custom Ashby Embed overlap. The complete employer-to-source mapping is in the linked index. Job application URLs and stable ATS IDs corroborate the source family in sampled cases; the exact internal request path and implementation are not public for every connector.

| Recorded source label | Companies | Role/location rows |
|---|---:|---:|
{sources_md}

Most listings originate from employer ATS boards, not from a single hidden master list. Keka, Greenhouse, Ashby, Lever, Workday, Kula, and other career systems are represented. Some sources are employer-specific pages or Y Combinator listings. Employer identities and careers URLs appear curated into individual records and then refreshed/enriched, but the original company-discovery process cannot be reconstructed from these records alone.

The records also explicitly attribute descriptions to `perplexity-sonar-pro` or `perplexity-sonar-pro-searchapi`, industry classification to `searchapi-google-ai-mode`, some salary estimates to `searchapi`, and social-link verification to `ai`. Salary citations include Naukri, Glassdoor and AmbitionBox in the SuperK sample. LinkedIn appears as a profile/image source. Benefits metadata names job descriptions, Levels.fyi, Glassdoor, and careers pages. Location provenance includes Perplexity, SearchAPI Maps, manual review and AI/city/region fallback rules. Labels also mention Claude Co-work research/review and a Gemini benefits extraction; those labels do not expose prompts, API logs or model versions. This is published provenance, not proof of direct scraping of every cited site or a current subscription to each provider. All observed provenance labels, citation domains and field timestamps are retained in the detailed analysis and individual JSON.

The frontend reads already-generated data. It does not establish that Perplexity/SearchAPI runs in the visitor's browser. Financial fields and office records do not uniformly carry independent citations; dates alone do not verify their accuracy.

## How fresh is it, and how often do they fetch?

- Median recorded company job-snapshot age: **{refresh['median']:.1f} days**. Youngest: **{refresh['min']:.1f} days**; oldest: **{refresh['max']:.1f} days**, measured at the analysis reference time in `inventory/analysis.json`.
- **158 snapshots are older than 10 days**; the 90th percentile is about **{refresh['p90']:.1f} days**. Six are older than 30 days.
- **{missing:,} of {total:,} role/location rows ({missing / total:.1%}) lack a usable posted date.**
- **{same_day:,} rows ({same_day / total:.1%}) have a posted date on the company's crawl/update day.** This pattern alone is a warning, not proof every such date is false. Individual official comparisons prove some are not original publication dates.
- SuperK's latest employer publication is **18 September 2026**, about 10 days old. Its oldest still-active listing is **2 July 2025**, about 453 days old. An old active listing is not automatically closed.
- A current Postman Workday example has **startDate 25 September 2026** and displays "Posted 3 Days Ago". It is absent from NextDoor's zero-job Postman snapshot.
- Anthropic Greenhouse job `5183044008` was first published **9 April 2026**, updated **18 September**, but NextDoor records `posted_date` as **24 September**, its crawl day. The authenticated UI's date rendering was not inspected.

The site advertises both **"updated weekly"** and **"Jobs updated every 10 days"** in inspected public bundles. Neither establishes the actual scheduler. Its **15-minute `/api/app-version` poll** refreshes client version awareness; it is not a scraper cron. We cannot infer fetch frequency from one timestamp per company. Source families have clustered update dates and some severe outliers, documented below.

| Company with snapshot older than 30 days | Recorded update UTC | Age in days | Role rows |
|---|---|---:|---:|
{old_md}

## What is failing now

### 1. Source identity and empty-result validation

**Confirmed:** Postman's obsolete Greenhouse URL returns 404 while its official Workday-backed source publishes 38 jobs. Aizen's Ashby HTML returns 200 but displays "Page not found"; its public posting feed returns 404. Conversely, Aftershoot's Kula page genuinely displays no jobs. Therefore, HTTP 200, `crawl_status=success`, and zero rows are each insufficient by themselves.

**Second migration:** DeepMind's official careers page now links to Google Careers, which showed 74 matching jobs, while NextDoor retains the obsolete Greenhouse board and zero roles. **Stale snapshot:** Lindy's dedicated Teamtailor jobs page has eight current openings versus two in NextDoor; six canonical URLs are missing. Its snapshot is about 52 days old, and one missing role has an employer publication date of 27 August 2026.

**Controls:** Plivo's hosted Lever board returns 404, but its own official careers page loads a valid public Lever feed containing zero jobs; missing roles are not demonstrated there. Regrello's own careers page still links to the same missing Lever board, so a replacement or missed count is unknown. All 460 NextDoor records say `crawl_status=success`, including all 23 zero-job records; the label does not establish current source health.

The full link pass yielded: **{', '.join(f'{n} {k}' for k, n in sorted(link_counts.items()))}**. These are point-in-time reachability results. Some checks use HEAD; 404/405/501 were confirmed with bounded GET. HTTP 200 is not semantic validation, and 403/429/network limitations are inconclusive rather than confirmed broken sources.

The following recorded careers URLs returned 404/410 during the bounded checks:

| Company slug | Recorded URL | Status |
|---|---|---:|
{failed_md}

**Fix:** Maintain a versioned employer-to-ATS registry; detect redirects and source migrations; separate `fetch_failed`, `source_missing`, `parse_failed`, `valid_empty`, and `success`. Validate board identity and schema, compare stable job IDs and previous counts, and quarantine unexplained empty results. Retain the last good snapshot with an explicit stale status. Use the current public employer feed where available, with monitored fallbacks and appropriate source terms.

### 2. Location normalization and referential integrity

**Confirmed against official sources:** SuperK Bangalore jobs reference Denver; Applied Washington DC/Arlington jobs reference White Salmon, Washington; an Atoms Boston role references Brooklyn; a Checkout.com Mexico role references London. Anthropic's "Remote-Friendly" becomes a spurious "Friendly" location identity. These errors affect records; their exact effect on authenticated map/filter interactions was not exercised.

1Password's source location `Remote (United States | Canada)` is split into malformed location fragments. Its 106 NextDoor rows represent 61 distinct Ashby job IDs, so comparing that row count directly with 64 live jobs would overstate staleness. All internal integrity candidates, duplicate IDs, missing references and examples are in the data analysis; heuristic mismatch candidates are not all established defects.

**Fix:** Treat structured country/region/city as authoritative. Preserve original text and remote eligibility separately from actual offices. Parse delimiters contextually. Enforce unique location IDs and valid references; reject conflicting display/country/coordinate mappings. Send unresolved locations to review rather than choosing the nearest-looking office. Canonicalize an opening by employer/source/job ID and attach many locations to it.

The shipped renderer also labels representative map points as "Office address" and an "Office network". A Databricks record explicitly identifies its point as a state-capital representative. An offline fixture confirms the renderer drops that distinction. Fix the schema/UI to distinguish verified physical offices, job locations, remote eligibility, and approximate map anchors.

### 3. Job age and AI enrichment blur source truth

**Confirmed:** SuperK's source has publication dates for all 12 jobs; NextDoor drops all 12. Anthropic's individual official dates disprove the recorded publication date. Some titles change seniority or specialization. Source changes since the prior crawl can explain part of a title difference, so not every difference is attributable solely to AI.

**Fix:** Store `source_published_at`, `source_updated_at`, `first_seen_at`, `last_seen_at`, `last_checked_at`, and `last_success_at` separately. A crawl time must never fill a missing publication date. Preserve source title/location/compensation verbatim and store normalized or AI-estimated fields separately with provenance and confidence. Do not present an estimated salary as employer compensation. Establish currency and period before normalization.

### 4. Paid listing conversion and lead delivery

**Reproduced from shipped code with offline mocks:** Both paid listing builders produce `https://checkout.dodopayments.com/buy/undefined?quantity=1`; free company submission shows success when both delivery requests fail; the desktop alert signup shows success after HTTP 500 or a network failure; a non-OK HTTP founder response is cached as an empty array without retry for the module lifetime. Network exceptions take a different path and do not populate that cache. No actual checkout or form was submitted.

**Fix:** Validate production payment product IDs and build-time variable access, or create checkout sessions server-side. Persist forms through one first-party endpoint, return a durable receipt, and send notifications after persistence. Propagate errors to the UI, keep entered values for retry, and record conversion analytics only after acknowledgement. Cache only successful leadership responses and give failures a retry path.

The public counters **460 companies / 22,579 jobs** are literals in the shipped counter module, not a browser computation over current datasets. **They exactly match this complete pinned snapshot.** That agreement is a build-consistency check, not evidence of live freshness or distinct vacancies. There are **21,449 distinct fragment-stripped application URLs across the snapshot**, also not a guaranteed vacancy count. Generate counters from the same validated snapshot and distinguish distinct openings from location rows. The renderer can also label a failed-crawl/zero-role fixture "NOT HIRING"; show source unavailable when freshness is unknown.

## Security findings and realistic reportability

| Observation | Established evidence | Reporting position / fix |
|---|---|---|
| Full company records in public static modules despite login UI | All 460 indexed modules fetched and parsed; discovery/leadership APIs reject anonymous requests | Intended-policy dependent. If membership is meant to protect these fields, serve only a limited preview publicly and authorize full data server-side. No customer-data breach established. |
| Raw fields interpolated into HTML / innerHTML | Inert markup survives unescaped in an offline fixture | Missing escaping confirmed; attacker control and stored XSS not demonstrated. Escape text, sanitize intentional HTML, validate URLs; test owner-controlled staging input. |
| Fixed notification x-api-key shipped to clients | Source reference, credential value redacted; never replayed | Authority unknown. Review server trust, rotate only if privileged, move secrets server-side; add public-form abuse controls. |
| Session recording/input masking configuration | Public layout disables most input masking and starts authenticated recording | Configuration concern; actual captured sensitive data not inspected. Mask by default and inspect an owned test session. |
| Social-video URL validator accepts lookalike hosts | Local lookalike-domain fixtures accepted | Client validation bug; no entitlement bypass or server-side fetch exploit proved. Exact hostname/subdomain allowlist and server validation. |
| Supabase anon key, Mapbox token, analytics IDs | Browser integration references | Expected public identifiers alone are not vulnerabilities. Backend grants/RLS require owner review. |

No confirmed exploitable account takeover, cross-user data exposure, unauthorized payment, live notification abuse, or stored XSS was established. No public paid bounty program for this exact domain was found in the bounded search. Do not confuse `nextdoor.company` with `nextdoor.com`. The general contact in the site's terms is available to the user, but no direct disclosure message has been sent.

## Public API and architecture map

The [frontend report](frontend-audit.md) inventories **17 first-party route patterns** and their observed methods/statuses, plus four distinct Apps Script receivers and analytics/auth/payment integrations. Anonymous public reads included company redirect metadata, auth state, app version, location choice and a known advertised job description. Profile, discover-map and leadership reads returned 401. Write routes were observed in code and left uninvoked. This is complete for literal references in the inspected public bundle corpus, not all server routes.

Observed architecture: employer career sources -> externally generated/enriched company records -> content-hashed JavaScript company modules -> client preview/map/HTML renderer; protected APIs coexist with those public assets. Supabase supports auth/profile access; PostHog, Clarity and Google Analytics appear in the layout; Google Apps Script handles several forms; Dodo Payments and Razorpay are referenced in payment configuration. A provider name in the company catalog is not proof that provider powers the scraper.

The deployment changed during the review. The old framework chunk returned 404 even with its original deployment query, while the current chunk returned 200. That proves old asset unavailability, not a reproduced stale-session outage. Retain compatible assets long enough for existing sessions or implement a tested one-time chunk-load recovery path. Pin company manifest and counters to a single data version.

## Concrete implementation order

1. **Immediate product fixes:** repair both checkout IDs/build validation; propagate signup/submission errors; move submissions to durable server acknowledgement; correct Postman's source; correct SuperK's job-location mapping.
2. **Next ingestion release:** introduce source health states and last-good snapshot protection, stable job IDs, explicit date semantics, location referential integrity, and source migration monitoring. Backfill verified bad records and recompute counts.
3. **Quality and privacy controls:** distinguish source facts from AI estimates, review HTML sinks, mask recording inputs, inspect notification authorization, and decide the intended public data boundary. Normalize company aliases without erasing legal/source distinctions.
4. **Operational monitoring:** daily small source-health checks; scheduler intervals chosen per provider and acceptable lag; bounded retries/backoff; connector failure alerts; count-drop and staleness alerts; source-to-published latency tracking; fixture tests for each connector and each reproduced regression.

These are proposed fixes. No NextDoor production code or backend configuration was changed.

## What requires the founder's backend access

To identify the exact operational root cause and cadence, obtain: scheduler definitions and per-source run history; last attempt/success/error and source response metadata; parser versions and zero-result rules; employer-to-board registry history; snapshot build/promotion logs and authenticated API parity; AI prompts/model/version and normalization rules; source-to-office identity logic; checkout build configuration; durable submission/webhook logs; authorization/RLS policies; replay project masking/retention settings. Each item corresponds to a concrete observed uncertainty above.

## Daily collection already installed locally

A macOS LaunchAgent named `local.nextdoor-company-index` runs at **09:00 local time (currently Asia/Kolkata)**. The original audit machine used a separate local installation; the portable code is under [daily-index-monitor/](daily-index-monitor/README.md). Cloning this repository does not install that schedule. It snapshots the public company index, records additions/removals and metadata changes, handles hashed asset changes, and preserves the previous good snapshot on errors. Five focused tests and a launchd run passed. It successfully handled the deployment change during this audit.

This recurring monitor collects the **company index**, not the full job feed or every company body. The complete job inventory in this package is a dated audit snapshot. A full daily job feed would need explicit source-policy decisions and a separate job-ID delta pipeline; this report does not imply that has been scheduled. Scheduled runs also depend on this Mac being available and connected.

## Evidence method and limits

All 460 module URLs came from one pinned, already-served public loader manifest, rather than guessed object identifiers. Each has a recorded fetch/parse outcome, source URL and response hash. Company modules were parsed as serialized data without evaluating their JavaScript. Career checks followed only recorded public URLs with bounded requests. The separate frontend reproduction harness evaluates extracted code offline with synthetic state and mocked network. Primary-source comparisons cover **14 companies and eight source families** at varying depth; this is a sample, not a live validation of every job.

This package retains relevant company/job/source metadata and redacted evidence, not account records or a verbatim mirror of the whole site. Founder personal profile bodies, cookies, credential values and visitor IPs are excluded. This is a dated public research snapshot, not a supported production feed. Public terms restrict systematic extraction; any future integration should settle source permissions and supported access with the owner. See NOTICE.md for source and reuse context.

Observation timestamps matter: employers and deployments can change after this report. For exact URLs, response statuses, field values, source offsets, hashes and limitations, use the linked evidence rather than relying on a screenshot alone.
'''
    (BASE / 'FOUNDER-REPORT.md').write_text(report)
    print(json.dumps(stats, indent=2))


def package(make_archive=True):
    allowed = {'.md', '.json', '.html', '.py', '.mjs', '.pdf', '.png', '.txt', '.sh', '.yml', '.yaml'}
    files = [p for p in BASE.rglob('*') if p.is_file() and (p.suffix in allowed or p.name in {'.gitignore', '.gitattributes'})
             and not any(part in {'.git', '.venv', '__pycache__', 'tmp', 'node_modules'} for part in p.relative_to(BASE).parts)
             and not str(p.relative_to(BASE)).startswith('daily-index-monitor/data/')
             and p.name not in {'evidence-manifest.json'}]
    dump(BASE / 'evidence-manifest.json', {'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(),
        'files': [{'path': str(p.relative_to(BASE)), 'bytes': p.stat().st_size,
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]})
    files.append(BASE / 'evidence-manifest.json')
    if make_archive:
        with zipfile.ZipFile(BASE / 'nextdoor-founder-audit-2026-09-28.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
            for p in files:
                archive.write(p, 'nextdoor-founder-audit/' + str(p.relative_to(BASE)))
    print('Manifest covers', len(files) - 1, 'files')


if __name__ == '__main__':
    import sys
    if '--package' in sys.argv:
        package()
    elif '--manifest' in sys.argv:
        package(make_archive=False)
    else:
        main()
