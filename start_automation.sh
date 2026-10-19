#!/bin/bash
# Start YouTube Shorts Automation Daemon
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PID_FILE="$DIR/.scheduler.pid"
LOG_FILE="$DIR/scheduler.log"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️ Automation scheduler is already running with PID $PID"
        exit 0
    fi
fi

nohup /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 "$DIR/scheduler.py" > "$LOG_FILE" 2>&1 &
PID=$!
echo $PID > "$PID_FILE"
echo "✅ Autonomous Shorts Scheduler started successfully with PID $PID"
echo "📄 Logs: $LOG_FILE"
