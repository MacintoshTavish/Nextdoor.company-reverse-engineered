#!/usr/bin/env python3
"""Read the sanitized public inventory and derive reproducible quality metrics.

No network requests. Preserves source claims separately from inferred anomalies.
"""
import collections
import argparse
import datetime as dt
import json
import math
import re
import statistics
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

BASE = Path(__file__).resolve().parent
OUT = BASE / 'inventory' / 'analysis.json'
NOW = dt.datetime.now(dt.timezone.utc)


def host(url):
    try:
        return (urlsplit(str(url)).hostname or '').lower()
    except ValueError:
        return ''


def date(value):
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return parsed.replace(tzinfo=dt.timezone.utc) if parsed.tzinfo is None else parsed.astimezone(dt.timezone.utc)
    except (ValueError, TypeError):
        return None


def days(value):
    parsed = date(value)
    return round((NOW - parsed).total_seconds() / 86400, 3) if parsed else None


def quantiles(values):
    values = sorted(x for x in values if isinstance(x, (int, float)))
    if not values:
        return {'n': 0}
    return {'n': len(values), 'min': values[0], 'median': round(statistics.median(values), 3),
            'p90': values[max(0, math.ceil(.9 * len(values)) - 1)], 'max': values[-1]}


def age_buckets(values):
    output = collections.Counter()
    for value in values:
        output['missing' if value is None else 'future' if value < 0 else '0-2 days' if value <= 2
               else '>2-7 days' if value <= 7 else '>7-14 days' if value <= 14
               else '>14-30 days' if value <= 30 else '>30-90 days' if value <= 90
               else '>90-180 days' if value <= 180 else '>180 days'] += 1
    return dict(output)


def flatten(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from flatten(child)
    elif isinstance(value, list):
        for child in value:
            yield from flatten(child)
    elif value is not None:
        yield value


def canonical_url(value):
    try:
        p = urlsplit(str(value))
        query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                 if not k.lower().startswith('utm_') and k not in ['source', 'src', 'ref']]
        return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), urlencode(sorted(query)), ''))
    except ValueError:
        return str(value)


def normalized_city(value):
    value = ''.join(ch for ch in unicodedata.normalize('NFKD', str(value)) if not unicodedata.combining(ch))
    value = re.sub(r'[^a-z0-9]+', ' ', str(value).lower()).strip()
    return {'bangalore': 'bengaluru', 'new york city': 'new york', 'gurgaon': 'gurugram',
            'bombay': 'mumbai', 'san francisco bay area': 'san francisco', 'nyc': 'new york',
            'kebonjeruk': 'kebon jeruk', 'kobenhavn': 'copenhagen', 'bay area': 'san francisco'}.get(value, value)


def normalized_country(value):
    value = str(value).strip().lower()
    return {'us': 'united states', 'usa': 'united states', 'u.s.': 'united states',
            'uk': 'united kingdom', 'uae': 'united arab emirates', 'viet nam': 'vietnam',
            'korea, republic of': 'south korea', 'republic of korea': 'south korea',
            'republic of ireland': 'ireland'}.get(value, value)


def job_ref(slug, n, job):
    return {'slug': slug, 'index': n, 'title': job.get('title'), 'apply_url': job.get('apply_url')}


def md(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def provenance_category(path):
    if path.startswith('job_data.roles'):
        return 'job_enrichment'
    return {'company_basic_information': 'company_identity', 'leadership': 'leadership',
            'social_media': 'social_verification', 'business_details': 'company_description_and_industry',
            'financial_information': 'financial_information', 'location_mapping': 'locations',
            'job_data': 'job_ingestion', 'benefits': 'benefits'}.get(path.split('.')[0].split('[')[0], 'other')


def analyze():
    index = json.loads((BASE / 'inventory' / 'module-index.json').read_text())
    expected = {x['slug']: x for x in index['companies']}
    records = []
    errors = []
    for path in sorted((BASE / 'inventory' / 'companies').glob('*.json')):
        record = json.loads(path.read_text())
        if record['slug'] not in expected or record.get('module_url') != expected[record['slug']]['url']:
            errors.append({'file': path.name, 'error': 'not current indexed module'})
        elif record.get('parse_status') != 'ok':
            errors.append({'file': path.name, 'error': record.get('parse_status'), 'details': record.get('error')})
        else:
            records.append(record)

    companies = []
    source_groups = collections.defaultdict(list)
    careers_hosts = collections.defaultdict(list)
    apply_hosts = collections.defaultdict(lambda: {'jobs': 0, 'companies': set()})
    provenance_labels = collections.defaultdict(lambda: {'occurrences': 0, 'companies': set(), 'paths': set()})
    provenance_domains = collections.defaultdict(lambda: {'occurrences': 0, 'companies': set(), 'paths': set()})
    timestamp_groups = collections.defaultdict(list)
    url_groups = collections.defaultdict(list)
    exact_url_groups = collections.defaultdict(list)
    id_groups = collections.defaultdict(list)
    role_fields = collections.Counter()
    job_ages = []
    totals = collections.Counter()
    anomalies = collections.defaultdict(list)
    salary_providers = collections.Counter()
    salary_confidence = collections.Counter()
    classifier_status = collections.Counter()
    method_groups = collections.defaultdict(list)
    status_groups = collections.defaultdict(list)
    benefit_keys = collections.Counter()
    same_careers = collections.defaultdict(list)
    same_company_ids = collections.defaultdict(list)
    same_websites = collections.defaultdict(list)
    categories = collections.defaultdict(lambda: {'companies': set(), 'fields': collections.Counter(),
                                                  'labels': collections.defaultdict(set)})
    region_labels = {'south america', 'latin america', 'north america', 'southern europe', 'europe', 'worldwide',
                     'global', 'apac', 'asia', 'emea', 'americas'}
    known_countries = {normalized_country(l.get('country')) for d in records for l in d.get('locations', [])
                       if l.get('country') and not re.search(r'\d', str(l.get('country')))} - region_labels

    for data in records:
        slug = data['slug']
        jobs = data['jobs']
        meta = data.get('job_metadata') or {}
        company = data.get('company') or {}
        if company.get('careers_url'):
            same_careers[canonical_url(company['careers_url'])].append(slug)
        if company.get('website_url'):
            same_websites[host(company['website_url']).removeprefix('www.')].append(slug)
        if company.get('id') is not None:
            same_company_ids[str(company['id'])].append(slug)
        source = str(meta.get('source') or '(missing)')
        source_groups[source].append(slug)
        careers_hosts[host(company.get('careers_url')) or '(missing)'].append(slug)
        method_groups[str(meta.get('crawl_method') or '(missing)')].append(slug)
        status_groups[str(meta.get('crawl_status') or '(missing)')].append(slug)
        role_fields.update(data.get('role_field_names') or [])
        location_map = {str(l.get('location_id', l.get('office_id'))): l for l in data.get('locations', [])}
        location_ids = [str(l.get('location_id', l.get('office_id'))) for l in data.get('locations', [])]
        duplicate_location_ids = [v for v, n in collections.Counter(location_ids).items() if n > 1]
        duplicate_location_records = {v: [l for l in data.get('locations', [])
                                          if str(l.get('location_id', l.get('office_id'))) == v]
                                      for v in duplicate_location_ids}
        invalid_coordinates = [l for l in data.get('locations', [])
                               if (isinstance(l.get('latitude'), (int, float)) and not -90 <= l['latitude'] <= 90)
                               or (isinstance(l.get('longitude'), (int, float)) and not -180 <= l['longitude'] <= 180)]
        malformed_countries = [l for l in data.get('locations', []) if re.search(r'\d', str(l.get('country')))]
        regional_countries = [l for l in data.get('locations', []) if normalized_country(l.get('country')) in region_labels]
        dangling = []
        city_mismatches = []
        country_mismatches = []
        salaries = []
        ai_titles = []
        counts = collections.Counter()
        posts = collections.Counter()
        company_urls = collections.defaultdict(list)
        company_exact_urls = collections.defaultdict(list)
        company_ids = collections.defaultdict(list)
        invalid_urls = []
        apply_domains = collections.Counter()
        post_before_title = []
        duplicate_refs = []
        company_provenance = collections.defaultdict(dict)
        company_timestamps = collections.defaultdict(dict)
        for n, job in enumerate(jobs):
            ref = job_ref(slug, n, job)
            url = job.get('apply_url')
            h = host(url)
            apply_domains[h or '(missing)'] += 1
            if not url or not h or not str(url).startswith(('https://', 'http://')):
                invalid_urls.append(ref)
            if h:
                apply_hosts[h]['jobs'] += 1
                apply_hosts[h]['companies'].add(slug)
                canonical = canonical_url(url)
                url_groups[canonical].append(ref)
                exact_url_groups[url].append(ref)
                company_urls[canonical].append(n)
                company_exact_urls[url].append(n)
            for key in ['id', 'greenhouse_job_id', 'ashby_job_id', 'lever_job_id', 'keka_job_id']:
                if job.get(key) is not None:
                    company_ids[(key, str(job[key]))].append(n)
                    # Numeric ATS IDs may overlap across tenants: cross-company groups are candidates only.
                    id_groups[(key, str(job[key]))].append(ref)
            post = job.get('posted_date')
            parsed_post = date(post)
            job_ages.append(days(post))
            counts['posted_date_present' if parsed_post else 'posted_date_missing_or_invalid'] += 1
            if parsed_post:
                posts[parsed_post.date().isoformat()] += 1
                if str(post)[:10] == str(meta.get('last_updated', ''))[:10]:
                    counts['posted_date_equals_company_refresh_day'] += 1
                title_date = date(job.get('title_updated_timestamp'))
                if title_date and title_date.date() < parsed_post.date():
                    post_before_title.append({**ref, 'posted_date': post,
                                              'title_updated_timestamp': job['title_updated_timestamp']})
            if job.get('fetched_at'):
                counts['role_fetched_at_present'] += 1
            if job.get('last_updated'):
                counts['role_last_updated_present'] += 1
            if job.get('salary_range'):
                counts['salary_range_nonempty'] += 1
            if job.get('salary_estimated'):
                estimate = job['salary_estimated']
                counts['salary_estimated_nonempty'] += 1
                salaries.append({**ref, 'estimate': estimate})
                if isinstance(estimate, dict):
                    salary_confidence[str(estimate.get('confidence'))] += 1
                    salary_providers[str(estimate.get('source', estimate.get('provider')))] += 1
                    citations = estimate.get('citations') or []
                    if citations and any(not isinstance(c, str) or not c.startswith(('https://', 'http://')) for c in citations):
                        counts['salary_estimates_with_non_url_citations'] += 1
            if job.get('title_updated_by_ai') is True:
                counts['ai_title_flagged'] += 1
                if job.get('title_original') != job.get('title'):
                    counts['ai_title_changed'] += 1
                    ai_titles.append({**ref, 'title_original': job.get('title_original')})
            classifier_status[str(job.get('department_classification_status') or '(missing)')] += 1
            refs = job.get('location_ids', [job.get('location_id')] if job.get('location_id') else [])
            refs = refs if isinstance(refs, list) else [refs]
            if len(refs) != len(set(str(x) for x in refs)):
                duplicate_refs.append({**ref, 'location_ids': refs})
            bad = [x for x in refs if str(x) not in location_map]
            if bad:
                dangling.append({**ref, 'missing_location_ids': bad})
            if not refs:
                counts['jobs_without_location_reference'] += 1
            mapped = [location_map[str(x)] for x in refs if str(x) in location_map]
            display = job.get('location_display') or ''
            if mapped and ',' in display and ' / ' not in display and not re.search(r'global|worldwide', display, re.I):
                shown_country = normalized_country(display.rsplit(',', 1)[-1])
                mapped_countries = [normalized_country(x.get('country')) for x in mapped]
                hong_kong_compat = shown_country == 'hong kong' and any(
                    normalized_country(x.get('country')) == 'china' and normalized_city(x.get('city')) == 'hong kong' for x in mapped)
                if (shown_country in known_countries and shown_country not in mapped_countries and not hong_kong_compat
                    and all(c in known_countries for c in mapped_countries)):
                    displayed_countries = [normalized_country(piece) for piece in display.split(',')
                                           if normalized_country(piece) in known_countries]
                    country_mismatches.append({**ref, 'location_display': display, 'work_mode': job.get('work_mode'),
                        'displayed_countries': displayed_countries,
                        'mapped_locations': [{k: x.get(k) for k in ['location_id', 'city', 'country', 'latitude', 'longitude']} for x in mapped],
                        'classification': 'single-country display/reference conflict; validate source location' if len(set(displayed_countries)) == 1
                        else 'multi-country eligibility not fully represented; candidate, may reflect remote expansion policy'})
            # Deliberately narrow heuristic: one explicit city before comma; non-remote jobs only.
            if mapped and ',' in display and ' / ' not in display and not re.search(r'remote|global|hybrid', display, re.I):
                shown_city = normalized_city(display.split(',')[0])
                mapped_cities = [normalized_city(x.get('city')) for x in mapped]
                if shown_city not in mapped_cities and all(shown_city not in c and c not in shown_city for c in mapped_cities if c):
                    city_mismatches.append({**ref, 'location_display': display,
                        'mapped_locations': [{k: x.get(k) for k in ['location_id', 'city', 'country', 'latitude', 'longitude']} for x in mapped],
                        'classification': 'candidate; aliases/regions need manual review'})
            if '(' in display and display.count('(') != display.count(')'):
                counts['unbalanced_location_parentheses'] += 1

        for key, value in data.get('provenance', {}).items():
            canonical_path = re.sub(r'\[\d+\]', '[]', key)
            category = provenance_category(key)
            company_provenance[category][key] = value
            categories[category]['companies'].add(slug)
            categories[category]['fields'][canonical_path] += 1
            for scalar in flatten(value):
                if isinstance(scalar, str) and scalar.startswith(('https://', 'http://')):
                    group = provenance_domains[host(scalar)]
                elif 'citation' in canonical_path.lower():
                    continue
                elif isinstance(scalar, (str, bool, int, float)) and len(str(scalar)) <= 160:
                    group = provenance_labels[str(scalar)]
                    categories[category]['labels'][str(scalar)].add(slug)
                else:
                    continue
                group['occurrences'] += 1
                group['companies'].add(slug)
                group['paths'].add(canonical_path)
        for key, value in data.get('timestamps', {}).items():
            timestamp_groups[re.sub(r'\[\d+\]', '[]', key)].append(value)
            company_timestamps[provenance_category(key)][key] = value
        benefit_keys.update(data.get('benefits_fields') or [])
        duplicate_urls = {u: ns for u, ns in company_urls.items() if len(ns) > 1}
        duplicate_exact_urls = {u: ns for u, ns in company_exact_urls.items() if len(ns) > 1}
        duplicate_ids = [{'field': k[0], 'value': k[1], 'job_indexes': ns}
                         for k, ns in company_ids.items() if len(ns) > 1]
        mismatch = meta.get('total_roles') is not None and meta.get('total_roles') != len(jobs)
        summary = {
            'slug': slug, 'name': company.get('company_name_brand'), 'company_id': company.get('id'),
            'module_url': data['module_url'], 'observed_at': data.get('observed_at'),
            'website_url': company.get('website_url'), 'careers_url': company.get('careers_url'),
            'careers_host': host(company.get('careers_url')), 'source': source,
            'careers_url_last_updated': data.get('timestamps', {}).get('company_basic_information.careers_url_last_updated'),
            'careers_url_source_fields': {k: v for k, v in data.get('provenance', {}).items() if 'careers_url' in k},
            'crawl_status': meta.get('crawl_status'), 'crawl_method': meta.get('crawl_method'),
            'last_updated': meta.get('last_updated'), 'refresh_age_days': days(meta.get('last_updated')),
            'job_count': len(jobs), 'declared_total_roles': meta.get('total_roles'), 'count_mismatch': mismatch,
            'distinct_canonical_apply_urls': len(company_urls), 'distinct_exact_apply_urls': len(company_exact_urls),
            'distinct_job_ids_by_field': dict(collections.Counter(key[0] for key in company_ids)),
            'show_on_map': data.get('show_on_map'), 'location_count': len(location_map),
            'duplicate_location_ids': duplicate_location_ids, 'founder_count': data.get('founder_count'),
            'duplicate_location_records': duplicate_location_records, 'invalid_location_coordinates': invalid_coordinates,
            'malformed_location_country_fields': malformed_countries, 'region_used_as_location_country': regional_countries,
            'apply_hosts': dict(apply_domains), 'posted_date_counts': dict(posts), 'job_field_counts': dict(counts),
            'salary_estimate_examples': salaries[:3], 'ai_title_examples': ai_titles[:3],
            'title_enrichment_before_claimed_posted_date_count': len(post_before_title),
            'title_enrichment_before_claimed_posted_date_examples': post_before_title[:3],
            'all_posted_dates_equal_refresh_day': bool(jobs) and counts['posted_date_equals_company_refresh_day'] == len(jobs),
            'all_nonmissing_posted_dates_identical': bool(posts) and len(posts) == 1,
            'dangling_location_references': dangling, 'simple_city_mismatch_candidates': city_mismatches,
            'display_reference_country_conflicts': country_mismatches,
            'duplicate_location_references_within_job': duplicate_refs,
            'duplicate_canonical_apply_urls': duplicate_urls, 'duplicate_exact_apply_urls': duplicate_exact_urls,
            'duplicate_job_ids': duplicate_ids, 'invalid_or_missing_apply_urls': invalid_urls,
            'benefits_fields': data.get('benefits_fields'), 'job_metadata_extra': {k: v for k, v in meta.items()
                if k not in ['source', 'crawl_status', 'crawl_method', 'last_updated', 'total_roles']},
            'provenance_by_category': dict(company_provenance), 'timestamps_by_category': dict(company_timestamps),
        }
        companies.append(summary)
        totals.update(counts)
        totals['jobs'] += len(jobs)
        totals['distinct_canonical_apply_urls_summed_by_company'] += len(company_urls)
        totals['distinct_exact_apply_urls_summed_by_company'] += len(company_exact_urls)
        totals['location_records'] += len(data.get('locations', []))
        totals['founder_records'] += data.get('founder_count') or 0
        totals['jobs_with_dangling_location_refs'] += len(dangling)
        totals['simple_city_mismatch_candidates'] += len(city_mismatches)
        totals['display_reference_country_conflicts'] += len(country_mismatches)
        totals['single_country_display_reference_conflicts'] += sum(len(set(x['displayed_countries'])) == 1 for x in country_mismatches)
        totals['jobs_with_repeated_location_refs'] += len(duplicate_refs)
        totals['malformed_location_country_fields'] += len(malformed_countries)
        totals['region_used_as_location_country'] += len(regional_countries)
        totals['title_enrichment_before_claimed_posted_date'] += len(post_before_title)
        for kind, value in [('count_mismatches', mismatch), ('duplicate_location_ids', duplicate_location_ids),
                            ('dangling_location_refs', dangling), ('simple_city_mismatch_candidates', city_mismatches),
                            ('display_reference_country_conflicts', country_mismatches),
                            ('duplicate_location_references_within_job', duplicate_refs),
                            ('invalid_location_coordinates', invalid_coordinates),
                            ('malformed_location_country_fields', malformed_countries),
                            ('region_used_as_location_country', regional_countries),
                            ('duplicate_canonical_apply_urls', duplicate_urls), ('duplicate_exact_apply_urls', duplicate_exact_urls),
                            ('duplicate_job_ids', duplicate_ids), ('invalid_or_missing_apply_urls', invalid_urls)]:
            if value:
                anomalies[kind].append({'slug': slug, 'detail': value})

    def groups(mapping):
        return {key: {'company_count': len(slugs), 'companies': sorted(slugs)}
                for key, slugs in sorted(mapping.items(), key=lambda item: (-len(item[1]), item[0]))}

    def provenance_groups(mapping):
        return {key: {**value, 'company_count': len(value['companies']),
                      'companies': sorted(value['companies']), 'paths': sorted(value['paths'])}
                for key, value in sorted(mapping.items(), key=lambda item: (-len(item[1]['companies']), item[0]))}

    cross_urls = {u: refs for u, refs in url_groups.items() if len({r['slug'] for r in refs}) > 1}
    cross_ids = [{'field': k[0], 'value': k[1], 'records': refs}
                 for k, refs in id_groups.items() if len({r['slug'] for r in refs}) > 1]
    source_summary = groups(source_groups)
    for source, info in source_summary.items():
        subset = [x for x in companies if x['source'] == source]
        info.update({'job_count': sum(c['job_count'] for c in subset),
                     'zero_job_companies': [c['slug'] for c in subset if not c['job_count']],
                     'refresh_age_days': quantiles([c['refresh_age_days'] for c in subset]),
                     'careers_hosts': dict(collections.Counter(c['careers_host'] for c in subset)),
                     'posted_date_present_rows': sum(c['job_field_counts'].get('posted_date_present', 0) for c in subset),
                     'posted_date_equals_refresh_day_rows': sum(c['job_field_counts'].get('posted_date_equals_company_refresh_day', 0) for c in subset),
                     'title_enrichment_before_claimed_posted_date_rows': sum(c['title_enrichment_before_claimed_posted_date_count'] for c in subset)})
    result = {
        'analyzed_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'age_reference_utc': NOW.isoformat(),
        'deployment': index.get('deployment'), 'module_index_source': index.get('source'),
        'expected_companies': len(expected), 'parsed_companies': len(companies),
        'coverage_complete': len(companies) == len(expected) and not errors,
        'missing_companies': sorted(set(expected) - {c['slug'] for c in companies}), 'errors': errors,
        'scope_note': 'All collected current-index sanitized company modules; source labels are data claims. No backend, private account, or original scraper access.',
        'totals': dict(totals), 'source_inventory': source_summary, 'careers_host_inventory': groups(careers_hosts),
        'apply_host_inventory': {key: {**value, 'companies': sorted(value['companies']), 'company_count': len(value['companies'])}
                                 for key, value in sorted(apply_hosts.items(), key=lambda item: -item[1]['jobs'])},
        'crawl_methods': groups(method_groups), 'crawl_statuses': groups(status_groups),
        'zero_jobs': [c['slug'] for c in companies if not c['job_count']],
        'zero_jobs_success': [c['slug'] for c in companies if not c['job_count'] and c['crawl_status'] == 'success'],
        'show_on_map': dict(collections.Counter(str(c['show_on_map']) for c in companies)),
        'refresh_age_days': quantiles([c['refresh_age_days'] for c in companies]),
        'refresh_older_than_days': {str(threshold): sum(c['refresh_age_days'] is not None and c['refresh_age_days'] > threshold for c in companies)
                                  for threshold in [1, 2, 7, 10, 14, 30, 60, 90, 180]},
        'oldest_refresh_companies': [{'slug': c['slug'], 'last_updated': c['last_updated'], 'age_days': c['refresh_age_days'], 'source': c['source'], 'job_count': c['job_count']}
                                    for c in sorted(companies, key=lambda c: date(c['last_updated']) or dt.datetime.max.replace(tzinfo=dt.timezone.utc))[:10]],
        'newest_refresh_companies': [{'slug': c['slug'], 'last_updated': c['last_updated'], 'age_days': c['refresh_age_days'], 'source': c['source'], 'job_count': c['job_count']}
                                    for c in sorted(companies, key=lambda c: date(c['last_updated']) or dt.datetime.min.replace(tzinfo=dt.timezone.utc), reverse=True)[:10]],
        'refresh_age_buckets': age_buckets([c['refresh_age_days'] for c in companies]),
        'refresh_date_counts': dict(sorted(collections.Counter(str(c['last_updated'])[:10] for c in companies).items())),
        'recorded_posted_age_days': quantiles(job_ages), 'recorded_posted_age_buckets': age_buckets(job_ages),
        'all_posted_dates_equal_refresh_day_companies': [c['slug'] for c in companies if c['all_posted_dates_equal_refresh_day']],
        'salary_providers': dict(salary_providers), 'salary_confidence': dict(salary_confidence),
        'department_classification_status': dict(classifier_status), 'benefits_field_company_counts': dict(benefit_keys),
        'role_field_company_counts': dict(role_fields), 'provenance_labels': provenance_groups(provenance_labels),
        'provenance_category_inventory': {k: {'company_count': len(v['companies']), 'companies': sorted(v['companies']),
                                             'field_occurrences': dict(v['fields']),
                                             'labels': {label: {'company_count': len(slugs), 'companies': sorted(slugs)} for label, slugs in v['labels'].items()}}
                                           for k, v in categories.items()},
        'provenance_citation_domains': provenance_groups(provenance_domains),
        'timestamps_by_field': {key: {'n': len(values), 'min': min(values), 'max': max(values),
                                   'age_days': quantiles([days(v) for v in values])}
                                for key, values in sorted(timestamp_groups.items())},
        'anomalies': dict(anomalies), 'cross_company_canonical_url_groups': cross_urls,
        'cross_company_job_id_candidates': cross_ids,
        'shared_careers_url_groups': {k: v for k, v in same_careers.items() if len(v) > 1},
        'shared_company_id_groups': {k: v for k, v in same_company_ids.items() if len(v) > 1},
        'shared_website_host_groups': {k: v for k, v in same_websites.items() if len(v) > 1},
        'globally_distinct_canonical_apply_urls': len(url_groups),
        'companies': companies,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    write_report(result)
    print(json.dumps({'companies': len(companies), 'complete': result['coverage_complete'],
                      'jobs': totals['jobs'], 'sources': len(source_summary), 'zero_jobs': len(result['zero_jobs']),
                      'anomaly_company_counts': {k: len(v) for k, v in anomalies.items()}}, indent=2))


def write_report(a):
    n, jobs, totals = a['parsed_companies'], a['totals']['jobs'], a['totals']
    lines = ['# Public inventory: source, freshness, and data-quality review', '',
             f"Observed 2026-09-28. Parsed **{n}/{a['expected_companies']}** current-index company modules, containing **{jobs:,} job rows**. "
             + ('Coverage of the inspected frontend company index is complete.' if a['coverage_complete'] else '**Collection is still in progress; all counts below are provisional.**'), '',
             'This is a complete analysis of the collected normalized records, not the unpublished database or scraper code. Source labels and timestamps are publisher-provided metadata. Remote-job expansion can intentionally produce multiple rows or city associations. A zero-job result alone does not establish a broken scraper.', '',
             f"The {jobs:,} job rows resolve to {totals.get('distinct_canonical_apply_urls_summed_by_company', 0):,} distinct canonical application URLs when counted within each company. **Rows are not unique openings**: for example, one upstream posting may be expanded into `#loc-0` and `#loc-1` records. Canonical URL count is a useful proxy, not guaranteed unique-posting truth.", '',
             f"Ages use the analysis-time reference `{a['age_reference_utc']}`; collection timestamps are stored per module.", '',
             f"Deployment: `{a.get('deployment')}`. Index source: {a.get('module_index_source')}.", '',
             '## Key measured facts', '',
             f"- Sources: {len(a['source_inventory'])} distinct recorded job-source labels; {len(a['careers_host_inventory'])} careers hostnames; {len(a['apply_host_inventory'])} application hostnames.",
             '- Crawl status: ' + ', '.join('{}: {}'.format(k, v['company_count']) for k, v in a['crawl_statuses'].items()) + '.',
             f"- Zero jobs: {len(a['zero_jobs'])} companies, including {len(a['zero_jobs_success'])} marked `success`. Verify against the employer before calling these extraction failures.",
             f"- Refresh age in days: {json.dumps(a['refresh_age_days'])}. A refresh timestamp is not an employer's publication date.",
             f"- Refresh older than 10 days: {a['refresh_older_than_days']['10']} companies; older than 30 days: {a['refresh_older_than_days']['30']}.",
             f"- Valid recorded `posted_date`: {totals.get('posted_date_present', 0):,}/{jobs:,}; missing/invalid: {totals.get('posted_date_missing_or_invalid', 0):,}.",
             f"- {totals.get('posted_date_equals_company_refresh_day', 0):,} rows have a recorded posted date matching the company refresh day; all rows do so at {len(a['all_posted_dates_equal_refresh_day_companies'])} companies.",
             f"- {totals.get('title_enrichment_before_claimed_posted_date', 0):,} rows have title-enrichment timestamps earlier than their recorded posted day. This undermines treating `posted_date` as first publication, although reposting can explain individual cases.",
             f"- {totals.get('ai_title_flagged', 0):,} rows have `title_updated_by_ai=true`; {totals.get('ai_title_changed', 0):,} differ from `title_original`.",
             f"- {totals.get('salary_estimated_nonempty', 0):,} rows carry salary estimates; {totals.get('salary_range_nonempty', 0):,} carry nonempty `salary_range`. Estimates must not be represented as employer offers.",
             f"- {totals.get('salary_estimates_with_non_url_citations', 0)} salary estimate(s) contain non-URL citations; Sarvam AI is the observed example. Citation identifiers require resolution before they can substantiate a user-facing number.",
             f"- {totals.get('jobs_with_dangling_location_refs', 0):,} rows refer to absent location IDs. There are {totals.get('simple_city_mismatch_candidates', 0):,} additional narrowly detected city-name mismatch candidates; aliases/regions require manual review.",
             f"- {totals.get('single_country_display_reference_conflicts', 0):,} rows with one displayed country point to locations in other countries. Including multi-country eligibility records with incomplete references, the broader country-inclusion candidate set has {totals.get('display_reference_country_conflicts', 0):,} rows; every case is retained for review.",
             f"- `show_on_map`: {json.dumps(a['show_on_map'])}. Presence in the frontend index does not imply visibility on the map.", '',
             '## Complete recorded job-source inventory', '',
             '| Recorded source | Companies | Job rows | Zero-job companies | Median refresh age (days) |',
             '|---|---:|---:|---:|---:|']
    for source, s in a['source_inventory'].items():
        lines.append(f"| {md(source)} | {s['company_count']} | {s['job_count']:,} | {len(s['zero_job_companies'])} | {s['refresh_age_days'].get('median', 'unknown')} |")
    lines += ['', 'Crawl methods: ' + '; '.join(f"`{k}` ({v['company_count']} companies)" for k, v in a['crawl_methods'].items()) + '.', '',
              'These labels identify the recorded job source, not how the original company universe was selected. Career URLs, every company/source mapping, application-host inventories, provenance labels, and citation-host inventories are in `inventory/analysis.json`.', '',
              '## Refresh timing and posting-date reliability', '',
              '| Company refresh date | Companies |', '|---|---:|']
    for key, value in a['refresh_date_counts'].items():
        lines.append(f'| {key} | {value} |')
    lines += ['', 'Company refresh ages: `' + json.dumps(a['refresh_age_buckets']) + '`.', '',
              'Recorded posting ages: `' + json.dumps(a['recorded_posted_age_buckets']) + '`.', '',
              '| Oldest company refreshes | Timestamp | Age (days) | Job rows |', '|---|---|---:|---:|']
    for c in a['oldest_refresh_companies']:
        lines.append(f"| {c['slug']} | {c['last_updated']} | {c['age_days']} | {c['job_count']} |")
    lines += ['',
              '**Cadence cannot be established from a single snapshot.** Same-day clusters suggest batch processing, but neither daily nor weekly scheduling is proven. The public files expose only the latest stored refresh per company; a daily external monitor can measure publication changes, not every backend crawl. Immutable asset HTTP Last-Modified dates must not be substituted for job-data refresh times.', '',
              '| Source | Rows with recorded posting date | Posting date equals refresh day | Earlier title enrichment |',
              '|---|---:|---:|---:|']
    for source, s in a['source_inventory'].items():
        lines.append(f"| {md(source)} | {s['posted_date_present_rows']} | {s['posted_date_equals_refresh_day_rows']} | {s['title_enrichment_before_claimed_posted_date_rows']} |")
    lines += ['',
              'A title can be enriched before a job is reposted, but large numbers of earlier title timestamps combined with identical per-company posted days make publication-date provenance a priority. Preserve separate employer `published_at`, crawler `first_seen_at`, `last_seen_at`, and `last_successful_fetch_at`; leave unknown publication dates null.', '',
              '## Data integrity and representative cases', '']
    by_slug = {c['slug']: c for c in a['companies']}
    if 'superk' in by_slug:
        s = by_slug['superk']
        lines += [f"### SuperK: internally contradictory location mapping", '',
                  f"{len(s['simple_city_mismatch_candidates'])}/{s['job_count']} rows have a simple display/mapped-city mismatch. See the exact per-job values in `companies[slug=superk].simple_city_mismatch_candidates`. Bengaluru display text with a Denver location reference is an internal contradiction; the company's upstream job page should establish which value is correct.", '',
                  'Fix: validate resolved location country/city against source location before publishing; keep remote eligibility separate from office locations; quarantine conflicting mappings rather than silently falling back to an unrelated office.', '']
    if 'anthropic' in by_slug:
        lines += ['### Anthropic: geocoding of a remote-work phrase', '',
                  'The public dataset includes `friendly_office` / Friendly, United States. The Fellows Program records associate this with actual office locations, and other roles display `Remote, Friendly`. The separate primary-source verification confirms the employer Greenhouse API says `Remote-Friendly, United States`, with an office label `Remote-Friendly US (Travel Required)` and no office location. The same job has an employer first-published date of 2026-04-09, whereas this dataset records 2026-09-24 as its posted date. See `source-verification.md` and its JSON evidence for the current endpoint response.', '',
                  'Fix: classify remote/hybrid terms and geographic eligibility before geocoding; require confidence and an explicit place span; never geocode isolated adjectives from remote-work labels.', '']
    if 'homelane' in by_slug:
        s = by_slug['homelane']
        lines += ['### HomeLane: duplicate rows and an unresolved location ID', '',
                  f"The module has {len(s['duplicate_exact_apply_urls'])} exact application-URL duplicate groups and {len(s['dangling_location_references'])} row(s) referencing an absent location ID. Examples include duplicate Design Consultant rows for the same Nagpur application URL; `Senior Business Manager` references `burdwan_office`, which is absent from the company location table. These are internal consistency defects, independent of employer availability.", '',
                  'Fix: upsert by stable employer posting ID, normalize location arrays into sets, and require every referenced location key to resolve before publishing the snapshot.', '']
    for kind in ['count_mismatches', 'dangling_location_refs', 'display_reference_country_conflicts', 'duplicate_location_ids', 'duplicate_exact_apply_urls', 'duplicate_canonical_apply_urls', 'duplicate_job_ids', 'invalid_or_missing_apply_urls']:
        values = a['anomalies'].get(kind, [])
        lines.append(f"- `{kind}`: {len(values)} affected companies" + (': ' + ', '.join(v['slug'] for v in values[:25]) + (' …' if len(values) > 25 else '') if values else '') + '.')
    lines += ['', f"Cross-company canonical application URL groups: {len(a['cross_company_canonical_url_groups'])}. Cross-company job-ID candidate groups: {len(a['cross_company_job_id_candidates'])}. Numeric IDs can overlap between employer tenants; ID collisions alone are not duplicate proof. Canonicalization removes fragments and common referral parameters, so location variants must be distinguished from duplicate openings.", '',
              f"Across the full observed inventory, {a['globally_distinct_canonical_apply_urls']:,} distinct canonical application URLs remain after cross-company deduplication. Shared careers-board groups: `{json.dumps(a['shared_careers_url_groups'])}`. Shared public website hosts: `{json.dumps(a['shared_website_host_groups'])}`. Shared internal company IDs: `{json.dumps(a['shared_company_id_groups'])}`. Some brands may legitimately share a parent company's board; employer identity must be confirmed before merging.", '',
              '## Zero-job companies to verify', '', ', '.join(a['zero_jobs']) or 'None.', '',
              'Do not conflate true zero openings, an inaccessible upstream source, a parser failure, intentional filtering, and removed company support. A healthy pipeline should record distinct statuses, retain the last known good snapshot when fetching fails, and alert on unexpected transitions to zero.', '',
              '## Enrichment provenance and presentation', '',
              'The analysis preserves exact per-company `provenance_by_category` and `timestamps_by_category` dictionaries. A source label records a claimed method or provider; it does not prove that external provider supplied a particular fact. A timestamp without a source is not evidence of provenance.', '',
              '| Data category | Companies with source/verification metadata | Typical recorded labels |', '|---|---:|---|']
    for category in ['company_identity', 'job_ingestion', 'job_enrichment', 'leadership', 'social_verification', 'company_description_and_industry', 'locations', 'financial_information', 'benefits']:
        entry = a['provenance_category_inventory'].get(category, {'company_count': 0, 'labels': {}})
        labels = sorted(entry['labels'], key=lambda k: -entry['labels'][k]['company_count'])
        lines.append(f"| {category} | {entry['company_count']} | {md(', '.join(labels[:8])) or 'No source/verification label observed'} |")
    lines += ['',
              'Careers URLs and their recorded last-updated timestamps are preserved for every company where present; original company discovery/selection is not established by an ATS URL. Financial records may contain funding values and update dates without a retrievable source citation; do not infer an upstream funding database from those fields.', '',
              'Source metadata records the following short provenance labels (including human verification labels). The complete mapping to fields and companies is machine-readable:', '',
              '| Label | Companies | Recorded occurrences | Field examples |', '|---|---:|---:|---|']
    for label, value in a['provenance_labels'].items():
        if len(label) <= 80:
            lines.append(f"| {md(label)} | {value['company_count']} | {value['occurrences']} | {md(', '.join(value['paths'][:3]))} |")
    lines += ['', '### Complete observed citation-domain inventory', '',
              '| Citation domain | Companies | Recorded citation occurrences | Field categories |', '|---|---:|---:|---|']
    for domain, value in a['provenance_citation_domains'].items():
        lines.append(f"| {md(domain)} | {value['company_count']} | {value['occurrences']} | {md(', '.join(value['paths']))} |")
    lines += ['', 'Benefits are extracted/enriched separately from job ingestion; an old benefits timestamp does not imply a newly fetched job offers that benefit. Preserve per-benefit source, observed date, employer/role scope, and confidence. The normalized collector retains benefit field names and provenance, not every benefit value, so this analysis cannot verify whether each displayed benefit is substantiated.', '',
              'Keep the original job title as the primary label or show it alongside any simplified title. Department classification and salary estimates are model outputs, not employer statements. Validate them separately and show source/date/confidence.', '',
              'Location provenance includes inferred and representative-city records, such as `ai_inference_upsert`, `company_fallback`, `state_capital_representative`, and `province_capital_representative` where present. A remote job mapped to a representative city is not evidence that the employer has an office there. Separate physical offices, job locations, eligible remote regions, and map display anchors in both data schema and UI.', '',
              '## Complete company-to-source and freshness ledger', '',
              '| Company | Recorded source | Careers host | Job rows | Last refresh UTC | Map flag |', '|---|---|---|---:|---|---|']
    for c in a['companies']:
        lines.append(f"| {md(c['name'] or c['slug'])} (`{c['slug']}`) | {md(c['source'])} | [{md(c['careers_host'] or 'missing')}]({c['careers_url'] or ''}) | {c['job_count']} | {md(c['last_updated'])} | {c['show_on_map']} |")
    lines += ['', '## Limits and proof discipline', '',
              '- This report concerns data quality and observability. It does not establish a paid-data entitlement bypass or a private-user-data leak.',
              '- Static client-side assets can establish what is publicly shipped; they cannot establish backend scheduler timing, retry logic, scraper source code, or database freshness.',
              '- Every anomaly remains a candidate unless the underlying records themselves conflict or the separate primary-source verification reproduces the discrepancy.',
              '- No outbound notifications, applications, login actions, destructive actions, or private-account access were used for this inventory analysis.', '']
    (BASE / 'data-quality.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--as-of', help='Explicit ISO-8601 age reference; default preserves the archived reference')
    args = parser.parse_args()
    archived = json.loads(OUT.read_text()) if OUT.exists() else {}
    reference = args.as_of or archived.get('age_reference_utc')
    if reference:
        NOW = date(reference)
        if NOW is None:
            parser.error('--as-of must be an ISO-8601 timestamp')
    analyze()
