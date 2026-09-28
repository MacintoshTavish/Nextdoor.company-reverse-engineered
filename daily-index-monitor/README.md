# Daily company-index monitor

Tracks additions, removals, and name changes in the company index shipped with
NextDoor.Company's public homepage. It does not collect detailed company datasets,
use the discovered notification key, log in, or scrape job records.

The initial baseline is the 460-entry public client index observed on September 28,
2026. This is not a verified export of the full backend database.

## Daily schedule and output

This copy does not install a schedule. The original audit machine had a macOS
LaunchAgent running at 09:00 Asia/Kolkata; `verified-status.json` records that
historical verification, not a schedule installed on the reader's machine.

Python 3.10+ and curl are required on macOS/Linux. The runner resolves its own
directory and defaults to `python3` on PATH; set `PYTHON_BIN` to an absolute
interpreter path for a scheduler with a restricted PATH. Optional environment
variables: `MONITOR_DATA_DIR` for output and `NEXTDOOR_MONITOR_TIMEZONE` for report
timestamps (default UTC). A timestamp timezone does not change cron's schedule.

After reviewing the source access terms, an optional user-crontab entry is:

```cron
0 9 * * * PYTHON_BIN=/absolute/path/to/python3 /absolute/path/to/repo/daily-index-monitor/run-daily.sh
```

Replace both paths. This runs at 09:00 in the scheduler's local timezone and
requires the machine to be available and connected. No GitHub workflow schedules
this collection. Runtime data is ignored by Git.

- `data/latest-report.md`: latest additions, removals, and name changes.
- `data/latest.json`: latest complete public company index and change details.
- `data/status.json`: last check succeeded/failed and timestamp.
- `data/snapshots/`: last 120 successful snapshots.
- `data/run-logs/`: last 30 run logs after successful checks.

There are no emails, external notifications, or uploads. An unchanged check still
updates the local check timestamp. A name first becoming known is not counted as
a newly added company. A parser failure, blocked request, or large index drop
preserves the last successful snapshot and records an error.

Ordinarily the monitor makes one conditional homepage GET. If referenced company
index/name assets change, it reads those public scripts. It can inspect up to 30
referenced scripts to recover after a frontend restructuring; each is capped at
2 MB and 25 seconds. It never follows redirects or downloads the individual
company data modules. Extracted identifiers/names are cached; script bodies,
cookies, and keys are not retained.

Manual check:

```sh
python3 monitor.py
```

Verification:

```sh
python3 -m unittest -v
```

## Data freshness

Company-index changes do not indicate newly posted jobs. In the samples checked
on September 28, SuperK's crawl timestamp was September 24 with 12 jobs but no
posting dates. Postman's September 26 record had zero jobs, while its own current
careers page listed 38 openings. Employer careers pages are the better source for
active vacancies and new-job monitoring.

## Published access terms

NextDoor.Company's published terms prohibit systematic extraction without express
written permission. This is a technical company-index monitor, not evidence of
permission or an official integration. Arrange permission/an approved feed for
ongoing collection: https://www.nextdoor.company/terms
