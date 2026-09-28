#!/usr/bin/env python3
"""Track the company index referenced by NextDoor.Company's public homepage."""

import argparse
import datetime as dt
import fcntl
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent
ORIGIN = "https://www.nextdoor.company"
TZ = ZoneInfo(os.environ.get("NEXTDOOR_MONITOR_TIMEZONE", "UTC"))
MIN_COMPANIES = 50
MAX_BYTES = 2_000_000


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        source = dict(attrs).get("src")
        if tag != "script" or not source:
            return
        url = urlsplit(urljoin(ORIGIN, source))
        if url.scheme == "https" and url.netloc == "www.nextdoor.company":
            if url.path.startswith("/_next/static/chunks/") and url.path.endswith(".js"):
                self.urls.append(ORIGIN + url.path)


def get(url, etag=None):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "www.nextdoor.company":
        raise ValueError("Only the public NextDoor.Company origin is allowed")
    with tempfile.TemporaryDirectory(prefix="nextdoor-index-") as folder:
        body, headers = Path(folder) / "body", Path(folder) / "headers"
        args = ["/usr/bin/curl", "--silent", "--show-error", "--proto", "=https",
                "--connect-timeout", "10", "--max-time", "25",
                "--max-filesize", str(MAX_BYTES), "--max-redirs", "0",
                "--user-agent", "PersonalCompanyIndexMonitor/1.0",
                "--dump-header", str(headers), "--output", str(body),
                "--write-out", "%{http_code}"]
        if etag:
            args += ["--header", "If-None-Match: " + etag]
        result = subprocess.run(args + [url], capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise RuntimeError(f"Public fetch failed ({result.returncode}): {result.stderr.strip()}")
        status = int(result.stdout)
        if status not in (200, 304):
            raise RuntimeError(f"HTTP {status} for {parsed.path}; no retries or bypass attempted")
        matches = re.findall(r"^etag:\s*(.+)$", headers.read_text(), re.I | re.M)
        return status, body.read_text() if body.exists() else "", matches[-1].strip() if matches else None


def extract_asset(source):
    """Parse literal identifiers/names; never execute downloaded JavaScript."""
    modules = []
    if "Failed to load company data" in source and "company_basic_information" in source:
        matches = re.findall(
            r'(?:"([^"\\]+)"|([A-Za-z_$][\w$-]*)):\(\)=>[A-Za-z_$][\w$]*\.e\((\d+)\)',
            source,
        )
        modules = sorted({quoted or bare for quoted, bare, _ in matches})
    pairs = re.findall(
        r'\{id:("(?:\\.|[^"\\])*"),name:("(?:\\.|[^"\\])*"),'
        r'logo:("(?:\\.|[^"\\])*"),coords:', source,
    )
    names = {json.loads(slug): json.loads(name) for slug, name, _ in pairs}
    return {"slugs": modules, "names": names}


def compare(previous, current):
    old, new = {c["slug"]: c for c in previous}, {c["slug"]: c for c in current}
    return {
        "added": [new[s] for s in sorted(new.keys() - old.keys())],
        "removed": [old[s] for s in sorted(old.keys() - new.keys())],
        "renamed": [{"slug": s, "before": old[s].get("name"), "after": new[s].get("name")}
                    for s in sorted(old.keys() & new.keys())
                    if old[s].get("name") and new[s].get("name")
                    and old[s]["name"] != new[s]["name"]],
    }


def validate_catalog(previous, current):
    if len(current) < MIN_COMPANIES or len({c["slug"] for c in current}) != len(current):
        raise ValueError("Invalid or unexpectedly small company index; previous snapshot preserved")
    if previous and len(current) < len(previous) * 0.75:
        raise ValueError("Company count dropped over 25%; needs review, previous snapshot preserved")


def report_text(snapshot):
    changes = snapshot["changes"]
    lines = ["# Daily company-index check", "", f"Checked: {snapshot['checked_at']}",
             f"Companies in public client index: {len(snapshot['companies'])}", "",
             f"Added: {len(changes['added'])}; removed: {len(changes['removed'])}; "
             f"renamed: {len(changes['renamed'])}.", "",
             "This tracks company-index changes, not new job postings or verified active vacancies."]
    for title, key in [("Added", "added"), ("Removed", "removed")]:
        if changes[key]:
            lines += ["", f"## {title}", ""]
            lines += [f"- {c.get('name') or c['slug']} (`{c['slug']}`)" for c in changes[key]]
    if changes["renamed"]:
        lines += ["", "## Renamed", ""]
        lines += [f"- `{c['slug']}`: {c['before']} → {c['after']}" for c in changes["renamed"]]
    return "\n".join(lines) + "\n"


def run(data_dir):
    latest_path = data_dir / "latest.json"
    previous = json.loads(latest_path.read_text()) if latest_path.exists() else {}
    cache_path = data_dir / "asset-index-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    status, homepage, etag = get(ORIGIN + "/", previous.get("homepage_etag"))
    if status == 304:
        if not previous.get("companies"):
            raise ValueError("Homepage returned 304 without a previous company snapshot")
        companies, used = previous["companies"], previous["source_assets"]
    else:
        parser = Scripts()
        parser.feed(homepage)
        urls = list(dict.fromkeys(parser.urls))
        candidates = [u for u in urls if not any(x in u for x in (
            "/webpack-", "/polyfills-", "/main-app-", "/app/layout-"))]
        old_roles = previous.get("source_assets", [])
        def priority(url):
            stem = url.rsplit("/", 1)[-1].split("-", 1)[0]
            return (0 if url in cache else 1 if any(
                old.rsplit("/", 1)[-1].split("-", 1)[0] == stem for old in old_roles) else 2)
        candidates.sort(key=priority)
        module_index = name_index = None
        used = []
        for url in candidates[:30]:
            if url not in cache:
                _, source, _ = get(url)
                cache[url] = extract_asset(source)
            asset = cache[url]
            if len(asset["slugs"]) >= MIN_COMPANIES and module_index is None:
                module_index = asset["slugs"]
                used.append(url)
            if len(asset["names"]) >= MIN_COMPANIES and name_index is None:
                name_index = asset["names"]
                used.append(url)
            if module_index is not None and name_index is not None:
                break
        if module_index is None or name_index is None:
            raise ValueError("Public bundle format changed; no valid catalog, previous snapshot preserved")
        old_names = {c["slug"]: c.get("name") for c in previous.get("companies", [])}
        companies = [{"slug": s, "name": name_index.get(s) or old_names.get(s)} for s in module_index]
        cache = {url: value for url, value in cache.items() if url in urls}
    validate_catalog(previous.get("companies", []), companies)
    now = dt.datetime.now(TZ)
    snapshot = {"checked_at": now.isoformat(), "kind": "public-client-company-index",
                "homepage_etag": etag or previous.get("homepage_etag"), "source_assets": used,
                "companies": companies, "baseline": not bool(previous),
                "changes": compare(previous.get("companies", companies), companies)}
    write_json(data_dir / "snapshots" / (now.strftime("%Y-%m-%dT%H%M%S") + ".json"), snapshot)
    write_json(latest_path, snapshot)
    write_json(cache_path, cache)
    (data_dir / "latest-report.md").write_text(report_text(snapshot))
    write_json(data_dir / "status.json", {"ok": True, "checked_at": snapshot["checked_at"],
                                        "company_count": len(companies), "changes": snapshot["changes"]})
    for folder, pattern, keep in [(data_dir / "snapshots", "*.json", 120),
                                   (data_dir / "run-logs", "*.log", 30)]:
        for old in sorted(folder.glob(pattern), reverse=True)[keep:]:
            old.unlink()
    print(f"{now.isoformat()} OK companies={len(companies)} "
          f"added={len(snapshot['changes']['added'])} removed={len(snapshot['changes']['removed'])}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=BASE / "data")
    args = parser.parse_args()
    args.data_dir.mkdir(parents=True, exist_ok=True)
    with (args.data_dir / ".lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("A company-index check is already running")
            return 0
        try:
            run(args.data_dir)
        except Exception as error:
            write_json(args.data_dir / "status.json", {"ok": False,
                "checked_at": dt.datetime.now(TZ).isoformat(), "error": str(error)})
            print(f"Company-index check failed: {error}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
