#!/bin/bash
# Stop YouTube Shorts Automation Daemon
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PID_FILE="$DIR/.scheduler.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        rm -f "$PID_FILE"
        echo "🛑 Stopped Automation Scheduler (PID $PID)"
        exit 0
    fi
    rm -f "$PID_FILE"
fi

echo "⚠️ Automation scheduler is not running."
