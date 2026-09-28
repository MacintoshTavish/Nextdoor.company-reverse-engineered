#!/usr/bin/env python3
"""Bounded inventory of exact public modules linked by the observed client build."""
import argparse
import ast
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

BASE = Path(__file__).resolve().parent
COMPANY_FIELDS = ['id', 'company_name_brand', 'company_name_legal', 'founded_year',
                  'website_url', 'careers_url', 'investor_portfolio_page']
ROLE_FIELDS = ['id', 'title', 'title_original', 'title_updated_by_ai', 'title_updated_timestamp',
               'apply_url', 'location_ids', 'location_id', 'location_display', 'role_department',
               'work_mode', 'salary_range', 'salary_estimated', 'experience', 'commitment',
               'posted_date', 'fetched_at', 'last_updated', 'keka_job_id', 'greenhouse_job_id',
               'ashby_job_id', 'lever_job_id', 'department_classification_status',
               'department_classification_reasoning']
LOCATION_FIELDS = ['location_id', 'office_id', 'city', 'state', 'country', 'latitude', 'longitude',
                   'exact_address', 'departments', 'employee_count']


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


def sanitize(value):
    if isinstance(value, dict):
        return {k: sanitize(v) for k, v in value.items()
                if not re.search(r'password|api.?key|access.?token|session.?token|cookie|email|phone', k, re.I)}
    if isinstance(value, list):
        return [sanitize(x) for x in value]
    if isinstance(value, str):
        value = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[REDACTED EMAIL]', value)
        value = re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', '[REDACTED TOKEN]', value)
    return value


def parse_module(text):
    literal = re.search(r'JSON\.parse\((\'(?:\\.|[^\'\\])*\')\)', text)
    if not literal:
        raise ValueError('Expected serialized JSON module not found; no JavaScript executed')
    data = json.loads(ast.literal_eval(literal.group(1)))
    if not isinstance(data, dict) or 'company_basic_information' not in data:
        raise ValueError('Unexpected company data schema')
    return data


def provenance(data):
    output = {}
    def walk(value, path=''):
        if isinstance(value, dict):
            for key, item in value.items():
                child = f'{path}.{key}' if path else key
                if any(t in key.lower() for t in ['source', 'crawl', 'generated_by', 'verified_by', 'citation']):
                    output[child] = sanitize(item)
                elif isinstance(item, (dict, list)):
                    walk(item, child)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                walk(item, f'{path}[{i}]')
    walk(data)
    return output


def normalize(entry, data, response):
    basic = data.get('company_basic_information') or {}
    job_data = data.get('job_data') or {}
    roles = job_data.get('roles') or []
    locations = data.get('location_mapping') or []
    timestamps = {}
    def walk(value, path=''):
        if isinstance(value, dict):
            for key, item in value.items():
                child = f'{path}.{key}' if path else key
                if isinstance(item, str) and any(t in key.lower() for t in ['updated', 'fetched_at', 'posted_date', 'verified']):
                    if re.match(r'^20\d\d-\d\d-\d\d', item):
                        timestamps[child] = item
                elif isinstance(item, (dict, list)):
                    walk(item, child)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                walk(item, f'{path}[{i}]')
    walk(data)
    return sanitize({
        'slug': entry['slug'], 'module_url': entry['url'], 'observed_at': now(),
        'fetch': response, 'parse_status': 'ok', 'top_level_fields': list(data),
        'company': {**{k: basic.get(k) for k in COMPANY_FIELDS if k in basic}, 'id': data.get('id')},
        'show_on_map': data.get('show_on_map'),
        'job_metadata': {k: v for k, v in job_data.items() if k != 'roles'},
        'job_count': len(roles), 'role_field_names': sorted({k for r in roles if isinstance(r, dict) for k in r}),
        'jobs': [{k: r[k] for k in ROLE_FIELDS if k in r} for r in roles if isinstance(r, dict)],
        'locations': [{k: r[k] for k in LOCATION_FIELDS if k in r} for r in locations if isinstance(r, dict)],
        'founder_count': len((data.get('leadership') or {}).get('founders') or []),
        'financial_information': data.get('financial_information'),
        'benefits_fields': list(data.get('benefits') or {}),
        'provenance': provenance(data), 'timestamps': timestamps,
    })


def fetch(entry):
    url = entry['url']
    if not re.fullmatch(r'https://www\.nextdoor\.company/_next/static/chunks/\d+\.[a-f0-9]{16}\.js', url):
        raise ValueError('Not an indexed static company asset URL')
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='nextdoor-public-audit-') as folder:
        body, headers = Path(folder) / 'body', Path(folder) / 'headers'
        result = subprocess.run(['/usr/bin/curl', '--silent', '--show-error', '--proto', '=https',
            '--connect-timeout', '10', '--max-time', '35', '--max-filesize', '2097152',
            '--user-agent', 'PublicDataQualityReview/1.0', '--dump-header', str(headers),
            '--output', str(body), '--write-out', '%{http_code}', url],
            capture_output=True, text=True, timeout=40)
        if result.returncode:
            raise RuntimeError(f'curl error {result.returncode}: {result.stderr.strip()}')
        raw = body.read_bytes()
        hdr = headers.read_text()
        selected = {}
        for line in hdr.splitlines():
            key, sep, value = line.partition(':')
            if sep and key.lower() in ['date', 'last-modified', 'cache-control', 'etag', 'content-type']:
                selected[key.lower()] = value.strip()
        meta = {'status': int(result.stdout), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                'elapsed_seconds': round(time.monotonic() - started, 3), 'headers': selected}
        if meta['status'] in [403, 429]:
            raise RuntimeError(f"Server returned {meta['status']}; stopping collection rather than retrying")
        return raw.decode('utf-8'), meta


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--limit', type=int, default=0)
    args.add_argument('--delay', type=float, default=1.0)
    opt = args.parse_args()
    index = json.loads((BASE / 'inventory' / 'module-index.json').read_text())
    entries = index['companies'][:opt.limit or None]
    folder = BASE / 'inventory' / 'companies'
    folder.mkdir(parents=True, exist_ok=True)
    outcomes = []
    for i, entry in enumerate(entries, 1):
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', entry['slug']):
            raise ValueError('Unexpected slug')
        target = folder / (entry['slug'] + '.json')
        if target.exists():
            record = json.loads(target.read_text())
            if record.get('parse_status') == 'ok' and record['module_url'] == entry['url']:
                outcomes.append({'slug': entry['slug'], 'status': 'ok', 'cached': True})
                continue
        try:
            source, meta = fetch(entry)
            if meta['status'] == 200:
                record = normalize(entry, parse_module(source), meta)
            else:
                record = {'slug': entry['slug'], 'module_url': entry['url'], 'observed_at': now(),
                          'fetch': meta, 'parse_status': 'http-error'}
            write(target, record)
            outcomes.append({'slug': entry['slug'], 'status': record['parse_status'], 'bytes': meta['bytes']})
        except (ValueError, SyntaxError, json.JSONDecodeError) as error:
            record = {'slug': entry['slug'], 'module_url': entry['url'], 'observed_at': now(),
                      'parse_status': 'parse-error', 'error': str(error)}
            write(target, record)
            outcomes.append({'slug': entry['slug'], 'status': 'parse-error'})
        except Exception as error:
            write(BASE / 'inventory' / 'progress.json', {'observed_at': now(), 'expected': len(entries),
                  'processed': i - 1, 'stopped_at': entry['slug'], 'error': str(error), 'outcomes': outcomes})
            print(f'STOP at {entry["slug"]}: {error}', flush=True)
            return 1
        if i % 10 == 0 or i == len(entries):
            write(BASE / 'inventory' / 'progress.json', {'observed_at': now(), 'expected': len(entries),
                  'processed': i, 'outcomes': outcomes})
            print(f'{i}/{len(entries)} last={entry["slug"]} parsed={sum(x["status"] == "ok" for x in outcomes)}', flush=True)
        time.sleep(max(0.5, opt.delay))
    write(BASE / 'inventory' / 'progress.json', {'observed_at': now(), 'expected': len(entries),
          'processed': len(entries), 'complete': True, 'outcomes': outcomes})
    return 0


if __name__ == '__main__':
    sys.exit(main())
