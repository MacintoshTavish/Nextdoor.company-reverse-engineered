#!/bin/sh
set -eu
MONITOR_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MONITOR_DATA_DIR=${MONITOR_DATA_DIR:-"$MONITOR_DIR/data"}
PYTHON_BIN=${PYTHON_BIN:-python3}
mkdir -p "$MONITOR_DATA_DIR/run-logs"
MONITOR_LOG="$MONITOR_DATA_DIR/run-logs/$(TZ=UTC date +%Y-%m-%dT%H%M%S).log"
exec "$PYTHON_BIN" "$MONITOR_DIR/monitor.py" --data-dir "$MONITOR_DATA_DIR" > "$MONITOR_LOG" 2>&1
