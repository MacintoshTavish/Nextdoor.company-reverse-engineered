#!/usr/bin/env python3
"""Check only the recorded public career URLs; no enumeration or form submission."""
import argparse
import concurrent.futures
import datetime as dt
import ipaddress
import json
import re
import socket
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import urljoin, urlsplit

BASE = Path(__file__).resolve().parent
LOCK = threading.Lock()
NEXT_GLOBAL = 0.0
NEXT_HOST = {}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def public_address(host):
    candidates = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    addresses = list(dict.fromkeys(row[4][0] for row in candidates))
    if not addresses or not all(ipaddress.ip_address(ip).is_global for ip in addresses):
        raise ValueError('Nonpublic/unresolved destination excluded')
    return next((ip for ip in addresses if ':' not in ip), addresses[0])


def pace(host):
    global NEXT_GLOBAL
    with LOCK:
        start = max(time.monotonic(), NEXT_GLOBAL, NEXT_HOST.get(host, 0))
        NEXT_GLOBAL = start + 0.5
        NEXT_HOST[host] = start + 1.0
    time.sleep(max(0, start - time.monotonic()))


def request(url, method):
    parsed = urlsplit(url)
    if parsed.scheme not in ['https', 'http'] or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Only public HTTP(S) career URLs without credentials are checked')
    if parsed.port and parsed.port not in [80, 443]:
        raise ValueError('Nonstandard port excluded')
    address = public_address(parsed.hostname)
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    pin = f'[{address}]' if ':' in address else address
    pace(parsed.hostname)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='career-reachability-') as folder:
        headers, body = Path(folder) / 'headers', Path(folder) / 'body'
        args = ['/usr/bin/curl', '--silent', '--show-error', '--proto', '=http,https',
                '--connect-timeout', '7', '--max-time', '15', '--max-filesize', '262144',
                '--resolve', f'{parsed.hostname}:{port}:{pin}',
                '--user-agent', 'PublicCareerLinkReview/1.0', '--dump-header', str(headers),
                '--output', str(body), '--write-out', '%{http_code}']
        if method == 'HEAD':
            args += ['--head']
        else:
            args += ['--range', '0-131071']
        result = subprocess.run(args + [url], capture_output=True, text=True, timeout=20)
        status = int(result.stdout) if result.stdout.strip().isdigit() else 0
        lines = headers.read_text().splitlines() if headers.exists() else []
        selected = {}
        for line in lines:
            key, colon, value = line.partition(':')
            if colon and key.lower() in ['location', 'content-type', 'content-length', 'server']:
                selected[key.lower()] = value.strip()
        return {'method': method, 'url': url, 'status': status,
                'elapsed_seconds': round(time.monotonic() - started, 3), 'headers': selected,
                'curl_exit_code': result.returncode,
                'error': result.stderr.strip()[:350] if result.returncode else None}


def check(record):
    origin = record['company'].get('careers_url')
    result = {'slug': record['slug'], 'recorded_careers_url': origin,
              'recorded_source': record.get('job_metadata', {}).get('source'),
              'checked_at': now(), 'requests': []}
    if not origin:
        return {**result, 'classification': 'missing-url'}
    current = origin
    seen = set()
    try:
        for _ in range(5):
            if current in seen:
                result['classification'] = 'redirect-loop'
                break
            seen.add(current)
            response = request(current, 'HEAD')
            result['requests'].append(response)
            if response['status'] in [404, 405, 501]:
                response = request(current, 'GET')
                result['requests'].append(response)
            status = response['status']
            result['final_url'], result['final_status'] = current, status
            if status in [301, 302, 303, 307, 308] and response['headers'].get('location'):
                current = urljoin(current, response['headers']['location'])
                continue
            if status in [200, 204, 206, 304]:
                result['classification'] = 'responded'
            elif status in [404, 410]:
                result['classification'] = 'not-found'
            elif status in [401, 403, 429]:
                result['classification'] = 'access-limited-inconclusive'
            elif status >= 500:
                result['classification'] = 'server-error-observed'
            else:
                result['classification'] = 'inconclusive'
            break
        else:
            result['classification'] = 'redirect-limit'
    except Exception as error:
        result['classification'] = 'request-error-inconclusive'
        result['error'] = str(error)[:350]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--follow-collection', action='store_true')
    opts = parser.parse_args()
    destination = BASE / 'inventory' / 'career-link-checks.json'
    results = json.loads(destination.read_text()).get('results', []) if destination.exists() else []
    done = {r['slug'] for r in results}
    def save():
        temp = destination.with_suffix('.tmp')
        temp.write_text(json.dumps({'checked_at': now(), 'method': 'HEAD with GET confirmation for 404/405/501; public URLs only',
            'limitation': 'An HTTP200 proves response, not correct jobs. Access challenges and transport errors are inconclusive.',
            'results': sorted(results, key=lambda r: r['slug'])}, indent=2) + '\n')
        temp.replace(destination)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            records = [json.loads(p.read_text()) for p in (BASE / 'inventory' / 'companies').glob('*.json')]
            pending = [r for r in records if r['slug'] not in done and r.get('parse_status') == 'ok']
            if opts.limit:
                pending = pending[:max(0, opts.limit - len(results))]
            futures = {executor.submit(check, r): r['slug'] for r in pending}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
                done.add(result['slug'])
                save()
                if len(results) % 20 == 0:
                    print(f'Career links checked: {len(results)}; last={result["slug"]} {result["classification"]}', flush=True)
            if opts.limit or not opts.follow_collection:
                break
            progress = json.loads((BASE / 'inventory' / 'progress.json').read_text())
            if progress.get('complete'):
                # Confirm no new completed records arrived during this batch.
                current_records = [json.loads(p.read_text()) for p in (BASE / 'inventory' / 'companies').glob('*.json')]
                if all(r['slug'] in done for r in current_records if r.get('parse_status') == 'ok'):
                    break
            if progress.get('error'):
                break
            time.sleep(10)
    save()
    print(f'Finished career URL reachability pass: {len(results)} records', flush=True)


if __name__ == '__main__':
    main()
