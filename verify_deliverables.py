#!/usr/bin/env python3
"""Offline consistency checks for the shareable audit, not a target scanner."""
import hashlib
import json
import re
import argparse
from pathlib import Path

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check-manifest', action='store_true', help='Verify all released file hashes')
parser.add_argument('--write-summary', action='store_true', help='Update the committed validation summary')
options = parser.parse_args()
analysis = json.loads((BASE / 'inventory/analysis.json').read_text())
index = json.loads((BASE / 'company-source-index.json').read_text())
jobs = json.loads((BASE / 'job-inventory.json').read_text())
records = [json.loads(p.read_text()) for p in (BASE / 'inventory/companies').glob('*.json')]
slugs = {x['slug'] for x in index['companies']}
assert len(records) == len(slugs) == 460
assert sum(len(x['jobs']) for x in records) == jobs['role_location_rows'] == analysis['totals']['jobs'] == 22579
assert sum(v['company_count'] for v in analysis['source_inventory'].values()) == 460
assert sum(v['job_count'] for v in analysis['source_inventory'].values()) == 22579
assert len(analysis['source_inventory']) == 35
assert all(x['parse_status'] == 'ok' for x in records)
assert all((BASE / x['details_file']).exists() for x in index['companies'])
assert len({x['slug'] for x in jobs['companies']}) == 460
for line in (BASE / 'company-source-index.md').read_text().splitlines():
    if line.startswith('|'):
        assert len(re.findall(r'(?<!\\)\|', line)) == 11, line[:80]
issues = []
for file in BASE.rglob('*'):
    if not file.is_file() or file.suffix not in {'.json', '.md', '.mjs', '.html', '.txt'}:
        continue
    if any(x in {'.git', '.venv', 'tmp', '__pycache__', 'node_modules'} for x in file.relative_to(BASE).parts):
        continue
    value = file.read_text()
    if re.search(r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}', value):
        issues.append(str(file.relative_to(BASE)) + ': JWT-like value')
    if re.search(r'(?:x-api-key|api[_-]?key)["\s:\\=]+["\s\\]*[a-f0-9]{64}', value, re.I):
        issues.append(str(file.relative_to(BASE)) + ': credential-like value')
assert not issues, issues
if options.check_manifest:
    manifest = json.loads((BASE / 'evidence-manifest.json').read_text())
    for entry in manifest['files']:
        path = (BASE / entry['path']).resolve()
        assert path.is_relative_to(BASE), 'Manifest path escapes repository'
        assert path.is_file(), f"Missing artifact: {entry['path']}"
        assert path.stat().st_size == entry['bytes'], f"Size changed: {entry['path']}"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], f"Hash changed: {entry['path']}"
result = {'date': '2026-09-28', 'company_modules': 460, 'job_location_rows': 22579,
          'source_labels': 35, 'coverage_and_arithmetic': 'pass', 'markdown_table_columns': 'pass',
          'credential_pattern_scan': 'pass',
          'limits': 'Pattern checks supplement deliberately sanitized collection; not a proof of all sensitive-data absence.'}
if options.write_summary:
    (BASE / 'validation-summary.json').write_text(json.dumps(result, indent=2) + '\n')
if options.check_manifest:
    result['manifest_hashes'] = 'pass'
print(json.dumps(result, indent=2))
