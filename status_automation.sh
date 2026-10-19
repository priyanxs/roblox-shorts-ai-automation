#!/bin/bash
# Check YouTube Shorts Automation Status
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PID_FILE="$DIR/.scheduler.pid"
LOG_FILE="$DIR/scheduler.log"

echo "=== YouTube Shorts Autonomous System Status ==="
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "🟢 Status: RUNNING (PID $PID)"
    else
        echo "🔴 Status: STOPPED (Stale PID file found)"
    fi
else
    echo "🔴 Status: STOPPED"
fi

echo ""
echo "=== Peak Viral Schedule ==="
echo "🎮 Roblox:    08:00 AM & 08:00 PM (12-hour gap)"
echo "⛏️  Minecraft: 09:00 AM & 09:00 PM (12-hour gap)"
echo ""
if [ -f "$LOG_FILE" ]; then
    echo "=== Recent Logs (Last 15 lines) ==="
    tail -n 15 "$LOG_FILE"
fi
