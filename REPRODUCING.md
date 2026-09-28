# Reproduction and build notes

## Offline checks

From the repository root, with Python 3.10+ and Node.js 20+:

```sh
python3 verify_deliverables.py --check-manifest
node frontend-repros/run.mjs
python3 -m unittest discover -s daily-index-monitor -v
```

No target requests are performed. The frontend harness reads only included excerpts, supplies synthetic state and mocks network operations. Node's VM is used to execute these specific reviewed excerpts; it is not presented as a general security sandbox for arbitrary hostile JavaScript.

The monitor uses `fcntl` and targets macOS/Linux. Windows users can inspect the reports or run the tools through WSL. Source-response SHA-256 values are provenance for original captures. `evidence-manifest.json` hashes the released local files and catches accidental modification; it is not a signed attestation.

## Frozen analysis

`analyze_inventory.py` defaults to the archived `age_reference_utc` already in `inventory/analysis.json`. That keeps snapshot ages meaningful when the code is rerun months later. To deliberately calculate age at another UTC instant:

```sh
python3 analyze_inventory.py --as-of 2026-09-28T08:40:00+00:00
```

An alternate reference changes derived age statistics, not the capture timestamps or employer facts. The report builder contains narrative comparisons specific to the original audit; use it for this snapshot, not as an unattended report generator for arbitrary future collections. Reconcile those narratives manually before publishing a new dated edition.

## Report and PDF build

```sh
python3 analyze_inventory.py
python3 build_deliverables.py
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build_brief.py
```

PDF dependencies are optional for core checks. Render the PDF with Poppler (`pdftoppm -png ...`) and inspect every page after content/layout changes. The interactive inventory is self-contained HTML and reads no remote assets.

To validate the local HTML in a fresh browser, install Playwright in an isolated environment, install its Chromium browser, and run `python verify_inventory_ui.py`. This optional check blocks HTTP/HTTPS page requests and exercises search against the local file. It is not part of CI and does not use a personal browser profile.

## Manifest and archive

After all intended changes and rendering checks:

```sh
python3 build_deliverables.py --manifest
python3 verify_deliverables.py --check-manifest
python3 build_deliverables.py --package
```

Archives, runtime monitor data, local environments and rendering scratch files are ignored by Git. GitHub's source download contains the committed report, records and tools. A locally built ZIP is an optional duplicate for sharing.

## Optional live collection

`collect_public_inventory.py` reads only exact company module URLs in the pinned manifest and stops on restrictions/errors. `check_careers_links.py` checks recorded public careers URLs with bounded requests. Published statuses remain observations, not proof of live source correctness. The scripts cache results; simply rerunning them does not constitute a fresh audit.

For a new audit, use a separate dated directory, verify the new public manifest, retain new observation times, follow applicable source access terms and compare identities and content. Do not edit the old snapshot in place and present it as unchanged historical evidence.

The optional index monitor has separate setup notes in [daily-index-monitor/README.md](daily-index-monitor/README.md). It does not schedule itself and does not monitor job additions.
