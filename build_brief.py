#!/usr/bin/env python3
"""Render the founder's concise PDF; the full inventory remains separate."""
import html
import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

BASE = Path(__file__).resolve().parent
OUT = BASE / 'output/pdf/nextdoor-founder-brief.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
A = json.loads((BASE / 'inventory/analysis.json').read_text())
S = json.loads((BASE / 'summary-metrics.json').read_text())
NAVY = colors.HexColor('#153344')
TEAL = colors.HexColor('#087f8c')
GRAY = colors.HexColor('#526577')
PALE = colors.HexColor('#eff5f7')
STYLES = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=29, leading=33, textColor=NAVY, spaceAfter=15),
    'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=21, leading=25, textColor=NAVY, spaceAfter=12),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=TEAL, spaceBefore=12, spaceAfter=6),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14.3, textColor=NAVY, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='Helvetica', fontSize=8.3, leading=11.3, textColor=GRAY, spaceAfter=6),
    'table': ParagraphStyle('table', fontName='Helvetica', fontSize=8.7, leading=11.2, textColor=NAVY),
    'head': ParagraphStyle('head', fontName='Helvetica-Bold', fontSize=8.6, leading=11, textColor=colors.white),
    'metric': ParagraphStyle('metric', fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=TEAL),
}
story = []


def clean(text):
    return text.replace('\u2013', '-').replace('\u2014', '-').replace('\u2011', '-').replace('\u2019', "'")


def p(text, style='body'):
    return Paragraph(clean(text), STYLES[style])


def add(text, style='body'):
    story.append(p(text, style))


def page(title, subtitle=None):
    if story:
        story.append(PageBreak())
    add(title, 'h1')
    if subtitle:
        add(subtitle, 'small')


def table(headers, rows, widths, font='table'):
    data = [[p(html.escape(str(v)), 'head') for v in headers]]
    data += [[p(html.escape(str(v)), font) for v in row] for row in rows]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE]),
        ('LINEBELOW', (0, -1), (-1, -1), .5, colors.HexColor('#c8d6de')),
    ]))
    story.append(t)
    story.append(Spacer(1, 7 * mm))


add('NextDoor.Company', 'title')
add('Public data and product audit', 'h1')
add('Founder brief | 28 September 2026 | Public research edition', 'small')
add('Useful employer discovery, with verified failures in source freshness, location mapping and submission feedback. The highest-value fixes are operational and product defects; no account takeover or cross-user data breach was established.')
metrics = Table([[p('460', 'metric'), p('22,579', 'metric'), p('35', 'metric'), p('9.7 days', 'metric')],
                 [p('Companies inspected', 'small'), p('Role/location rows', 'small'), p('Recorded source labels', 'small'), p('Median snapshot age', 'small')]],
                colWidths=[43*mm]*4)
metrics.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [metrics, Spacer(1, 8*mm)]
table(['Verified finding', 'Immediate action'], [
    ['Postman: 0 NextDoor / 38 official jobs. DeepMind: 0 / 74.', 'Replace obsolete source boards; validate source identity and empty results.'],
    ['SuperK: all 12 Bangalore jobs reference Denver internally.', 'Correct mappings; enforce country/city/reference consistency.'],
    ['Both paid listing builders produce /buy/undefined.', 'Validate product IDs in the production build or create checkout on the server.'],
    ['Company submission and alert signup can report success after failure.', 'Require durable server acknowledgement; propagate errors.'],
    ['Recorded posting dates can be missing or substituted by crawl day.', 'Separate publication, source update and crawler timestamps.'],
], [98, 74])
add('Coverage and confidence', 'h2')
add('All 460 modules in one pinned public manifest were fetched and parsed. Every recorded careers URL received a bounded reachability check. Official-source comparisons cover 14 companies and eight source families at varying depth. Eleven offline frontend scenarios provide reproducible evidence without production writes.', 'small')
add('This is complete for the inspected public company index. It is not a claim of complete backend coverage, authenticated database parity, or a proven scraper schedule.', 'small')

page('Where the listings come from', 'Exact employer URLs: company-source-index.html / .md / .json in the accompanying package.')
add('Jobs mostly come from employer career systems. These are 35 recorded labels, with overlapping vendors such as Freshteam and Ashby. They identify the recorded job source; they do not reveal how the founder originally selected the companies.')
sources = list(A['source_inventory'].items())
rows = []
for i in range(18):
    left = sources[i] if i < len(sources) else ('', {})
    right = sources[i+18] if i+18 < len(sources) else ('', {})
    rows.append([left[0], left[1].get('company_count',''), right[0], right[1].get('company_count','')])
table(['Recorded source', 'Cos.', 'Recorded source', 'Cos.'], rows, [69, 17, 69, 17])
add('Enrichment is a separate layer', 'h2')
add('Published metadata names Perplexity Sonar, SearchAPI Google AI Mode, SearchAPI Maps, AI and manual review, LinkedIn profile/image sources, and occasional Claude Co-work/Gemini labels. Benefits provenance mentions job descriptions, Levels.fyi, Glassdoor and careers pages. Salary estimates can cite Naukri, Glassdoor and AmbitionBox.', 'small')
add('These are attribution fields, not provider request logs. Original company discovery and most funding-data provenance remain unknown. The package preserves every observed label, citation domain and per-field timestamp.', 'small')

page('Freshness: three different clocks')
add('A job publication date, a source modification time and the last crawler snapshot are different facts. The present data does not consistently preserve that distinction.')
table(['Measured in the public snapshot', 'Result'], [
    ['Median / 90th percentile snapshot age', f"{S['refresh']['median']:.1f} / {S['refresh']['p90']:.1f} days"],
    ['Snapshots older than 10 / 30 days', '158 / 6 companies'],
    ['Missing or unusable posted_date', '2,847 rows (12.6%)'],
    ['posted_date falls on company update day', '11,715 rows (51.9%); warning pattern, not proof all are false'],
    ['Status labels', 'All 460 say success, including all 23 zero-job records'],
], [99, 73])
old = sorted([x for x in A['companies'] if x['refresh_age_days'] > 30], key=lambda x:x['refresh_age_days'], reverse=True)
table(['Oldest snapshots', 'Age, days', 'Rows'], [[x['name'],f"{x['refresh_age_days']:.1f}",x['job_count']] for x in old], [112, 30, 30])
add('How old are real current jobs?', 'h2')
add('SuperK: newest source publication 18 September 2026 (about 10 days); oldest active source publication 2 July 2025 (about 453 days). Postman: a verified Workday example has startDate 25 September 2026. Anthropic job 5183044008: first published 9 April, source updated 18 September, but NextDoor records posted_date 24 September. Authenticated date rendering was not inspected.', 'small')
add('How often do they fetch?', 'h2')
add('Public claims conflict: "updated weekly" and "every 10 days". The 15-minute app-version poll is a client refresh mechanism. Exact cron intervals, failed attempts and source-to-published lag require scheduler and run logs. One last_updated value per company cannot establish cadence.', 'small')

page('Source failures and positive controls')
table(['Case', 'Verified comparison', 'What follows'], [
    ['Postman', 'Old Greenhouse board 404; NextDoor 0. Official Workday-backed page/feed 38.', 'Obsolete source mapping; why the historical crawl says success needs logs.'],
    ['Google DeepMind', 'Old Greenhouse board 404; NextDoor 0. Official Google Careers filter 74.', 'A second confirmed ATS/source migration.'],
    ['Lindy', 'NextDoor 2; dedicated employer jobs page 8. Snapshot about 52 days old.', 'Six current canonical URLs absent; one missing job was posted 27 August.'],
    ['Aizen', 'Ashby HTML 200 says Page not found; posting feed 404.', 'Status 200 is not semantic source success. Missing-role count unknown.'],
    ['Aftershoot / Plivo', 'Official source currently empty. Plivo hosted board still returns 404.', 'Zero jobs can be legitimate; a 404 alone does not prove lost jobs.'],
    ['Regrello', 'Own careers page still links to the missing Lever board.', 'No replacement or current missed-job count established.'],
], [28, 77, 67])
add('All 460 recorded careers URLs checked', 'h2')
add('445 responded; 6 returned not found; 3 were access-limited; 1 returned a server error; 5 had other inconclusive request outcomes. Checks used HEAD, with bounded GET confirmation for 404/405/501. A responding URL can still contain an invalid board. Restrictions and timeouts are not treated as confirmed defects.', 'small')
add('Repair the ingestion contract', 'h2')
add('Track fetch status, final URL, board identity, schema validity, parsed count and prior count. Distinguish valid_empty from source_missing, parse_failed and fetch_failed. Quarantine unexplained count collapses, retain the last good snapshot with a stale flag, and alert on source moves. Prefer the employer\'s structured public source where available; monitor undocumented feed changes.', 'small')

page('Locations, titles and counts')
table(['Company', 'Official source location', 'NextDoor reference'], [
    ['SuperK', 'Bangalore, India - all 12 roles', 'Denver, Colorado, United States'],
    ['Applied', 'Washington DC / Arlington VA', 'White Salmon, Washington state'],
    ['Atoms', 'Boston, Massachusetts', 'Brooklyn, New York'],
    ['Checkout.com', 'Mexico / Mexico City', 'London, United Kingdom'],
    ['Anthropic', 'Remote-Friendly United States', 'Spurious Friendly identity, mapped to a San Francisco office'],
], [32, 70, 70])
add('Office claims need their own evidence', 'h2')
add('Some location provenance describes AI inference, city fallbacks or representative state capitals. The shipped renderer still presents a representative-point fixture as "Office address" and "Office network". A map anchor, eligible remote region and verified physical office must be separate types.', 'small')
add('Count openings before expanding locations', 'h2')
add('All 22,579 rows exactly match the hardcoded homepage total, but the snapshot has 21,449 globally distinct fragment-stripped application URLs. Neither number guarantees distinct vacancies. For 1Password, 106 rows are 61 distinct Ashby IDs; its current source has 64. Location expansion explains most of the row difference. Shared employer boards and aliases also require explicit identity handling.', 'small')
add('Concrete integrity checks', 'h2')
add('The audit found 11 rows with missing location references and 265 with repeated references. There are 36 single-country display/reference conflict candidates; primary-source checks establish the examples above, not every heuristic candidate. Enforce unique location IDs, valid references and structured country/city agreement. Preserve uncertain original text rather than inventing an office.', 'small')
add('Keep source facts separate from normalization', 'h2')
add('885 rows carry an AI-title flag; 800 have changed text. These are not automatically incorrect. Preserve source_title verbatim, normalized_title separately, and source/AI salary provenance. Do not silently change seniority or infer currency/period from ambiguous salary numbers. Retain first publication independently from crawl timestamps.', 'small')

page('Frontend defects reproduced offline', 'Eleven scenarios; extracted shipped code, synthetic state, mocked fetch. No production forms or payments sent.')
table(['Defect', 'Observed behavior', 'Fix / acceptance'], [
    ['Paid listing plans', 'Both construct /buy/undefined?quantity=1.', 'Validate both build product IDs; require real IDs before navigation. Public code cannot distinguish unset values from failed build-time inlining.'],
    ['Free company submission', 'Both delivery requests fail; success state and callback still run.', 'Persist server-side once and return a durable receipt. Queue notifications after acceptance.'],
    ['Desktop job alert', 'HTTP 500 or network rejection still leads to success and submitted analytics.', 'Throw or return an explicit failed result; preserve form values. Test error and 200 controls.'],
    ['Leadership lookup', 'Non-OK HTTP response cached as []; second call never retries.', 'Cache successful results only; distinct error/empty states and retry. Network exceptions are not cached.'],
    ['Hiring label', 'Zero roles plus a failed-crawl fixture renders NOT HIRING.', 'Use source unavailable or stale when a valid empty result is not established.'],
    ['Office label', 'Representative map point displayed as office address/network.', 'Surface location type and provenance.'],
], [33, 62, 77])
add('Build and deployment observations', 'h2')
add('The 460 / 22,579 counters are literal build values and exactly match this pinned snapshot. That is consistency, not live freshness. Generate counters from the validated snapshot and label role rows accurately.', 'small')
add('Deployment changed during review. An old framework chunk returned 404 even with its old deployment query; the current chunk returned 200. Stale-session failure was not reproduced. Retain compatible assets or implement a tested one-time chunk recovery path.', 'small')
add('Reproduce: node frontend-repros/run.mjs. The included source excerpt hashes and offsets tie each scenario to the inspected build.', 'small')

page('Security: facts versus open questions')
table(['Observation', 'Evidence and appropriate action'], [
    ['Public full company modules behind a login-oriented preview', 'All 460 indexed records are publicly readable; protected discover/leadership APIs return 401. If these fields are intended to require membership, remove them from public builds and authorize server-side. Public-preview intent remains an owner decision.'],
    ['Unescaped data enters innerHTML', 'Inert local markup survives. No attacker-controlled production ingest or stored XSS proved. Escape text, sanitize rich HTML and validate URLs; verify in owner-controlled staging.'],
    ['Fixed notification x-api-key in frontend', 'Value redacted and never replayed. Authority unknown. Review server trust and abuse controls; rotate/move server-side if privileged.'],
    ['Session recording configuration', 'Most input masking disabled in shipped configuration; authenticated recording started. Actual recordings were not inspected. Mask by default and review owned test sessions.'],
    ['Lookalike social-video hosts accepted', 'Local frontend validator accepts instagram.com.example.invalid. No access grant or server exploit proved. Use exact host/subdomain checks server-side too.'],
    ['Public SDK keys and identifiers', 'Supabase anon key, Mapbox and analytics identifiers alone are not vulnerabilities. Authorization/RLS and server privileges require owner access.'],
], [49, 123])
add('Reportability', 'h2')
add('The defensible founder report leads with confirmed product/data defects. Treat the public-data boundary as policy dependent, and HTML/key/recording observations as owner review items. No confirmed account takeover, private account exposure, payment abuse, live notification abuse or stored XSS was established. No public bounty for this exact domain was found in the bounded search.', 'small')
add('nextdoor.company is the job-discovery target. Do not apply nextdoor.com\'s program or policies to it. No direct disclosure message has been sent to the operator.', 'small')

page('Public API and integration inventory')
table(['Method', 'Route / route pattern', 'Anonymous evidence'], [
    ['GET','/api/company/{slug}','200 for superk'],
    ['POST','/api/job-leads-companies','200; one public-slug read'],
    ['GET','/api/auth/check','200; unauthenticated'],
    ['GET','/api/user/profile','401'],
    ['GET','/api/app-version','200'],
    ['GET','/api/detect-location','200; visitor IP omitted'],
    ['POST','/api/auth/sign-in','Code reference; uninvoked'],
    ['POST','/api/job-leads-accessed','Code reference; uninvoked'],
    ['GET','/api/white-glove-jd?slug=...','200; known public job'],
    ['POST','/api/apply-to-hvt','Code reference; uninvoked'],
    ['POST','/api/send-company-listing-notification','Code reference; uninvoked'],
    ['GET','/api/discover-map-data','401'],
    ['GET','/api/company-leadership?id=...&slug=...','401'],
    ['GET','/api/company/{slug}/role/{roleSlug}','404; old known Atlan role'],
    ['GET','/api/get-user-country','Code reference; uninvoked'],
    ['GET','/api/ph-upvotes','Code reference; uninvoked'],
    ['POST','/api/email-signup','Code reference; uninvoked'],
], [19, 98, 55])
add('Complete for literal first-party API references in the inspected public corpus, not all backend routes. Third-party SDK routes were excluded. /discover, /robots.txt, /sitemap.xml and /.well-known/security.txt redirected to login in the anonymous checks.', 'small')
add('Visible integrations: Supabase auth/profile; PostHog, Clarity and Google Analytics; Mapbox; four Apps Script form receivers; Dodo Payments and Razorpay configuration; public social/media links. These references do not prove database access or private integration behavior.', 'small')

page('Repair order and owner evidence')
table(['Order', 'Work', 'Acceptance evidence'], [
    ['Immediate', 'Checkout configuration; honest form feedback; Postman/DeepMind source registry; SuperK mapping.', 'Valid product IDs, failed-write UI controls, current public source IDs, correct Bangalore references.'],
    ['Next ingest release', 'Source health states, last-good protection, stable IDs, date semantics, location types, publication consistency.', 'Connector fixtures for valid empty/404/schema changes; no silent data wipe; job/location FK checks; counters from one snapshot.'],
    ['Trust and privacy', 'Source versus AI fields; office claims; HTML sinks; recording masking; notification authority; public-data policy.', 'Owned staging fixtures, reviewed server rules, verified masked test replay, intentional preview schema.'],
    ['Ongoing operations', 'Per-source cadence, bounded retries, count-drop and stale-source alerts, source-to-published lag.', 'Run history with attempt/success/error; connector dashboards and regression fixtures.'],
], [24, 82, 66])
add('To explain the exact backend failure and frequency', 'h2')
add('Request scheduler definitions and recent run logs; employer-to-board registry history; HTTP/final URL/schema/count evidence; parser versions and zero-result rules; snapshot promotion logs and API parity; AI normalization prompts/model versions; production checkout variables; durable form/webhook logs; RLS/authorization; recording project settings. The public client cannot supply these facts.', 'small')
add('Daily monitor already installed locally', 'h2')
add('macOS LaunchAgent local.nextdoor-company-index runs at 09:00 local time (currently Asia/Kolkata). It tracks the public company index and additions/removals, preserves good state on failure and handles hashed asset changes. Five focused tests and a launchd run passed. The full job inventory here is a dated audit snapshot, not a scheduled daily job-feed collector.', 'small')
add('Full evidence and primary sources', 'h2')
add('Open FOUNDER-REPORT.md, company-source-index.html, data-quality.md, source-verification.md and frontend-audit.md. Exact upstream URLs, timestamps, source hashes, field comparisons and limitations are in the accompanying JSON and offline harness.', 'small')
for label, url in [
    ('Postman official careers', 'https://www.postman.com/company/careers/open-positions/'),
    ('Google DeepMind careers', 'https://deepmind.google/careers/'),
    ('SuperK official Keka board', 'https://superk.keka.com/careers'),
    ('Greenhouse Job Board API documentation', 'https://docs.greenhouse.io/job-board.html'),
]:
    add(f'<link href="{url}" color="#087f8c">{label}</link>', 'small')


def footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(colors.HexColor('#ccd8df'))
    canvas.line(19*mm, 17*mm, w-19*mm, 17*mm)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(19*mm, 12*mm, 'NEXTDOOR.COMPANY / PUBLIC-SOURCE REVIEW / 28 SEP 2026')
    canvas.drawRightString(w-19*mm, 12*mm, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=19*mm, leftMargin=19*mm,
                        topMargin=20*mm, bottomMargin=23*mm, title='NextDoor.Company founder audit',
                        author='Public-source review', subject='Data sources, freshness, product defects and fixes')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
