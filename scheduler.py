#!/usr/bin/env python3
"""
Autonomous 24/7 Gaming Shorts Scheduler
Runs two daily posting cycles with 12-hour gap at peak viral times:
- Roblox:    08:00 AM & 08:00 PM IST
- Minecraft: 09:00 AM & 09:00 PM IST
"""

import time
import sys
import os
import schedule
from auto_shorts_publisher import run_pipeline

def job_roblox():
    print(f"\n⏰ [TRIGGER] Scheduled Roblox Generation & Upload at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        run_pipeline("roblox")
    except Exception as e:
        print(f"❌ Error in Roblox scheduled job: {e}")

def job_minecraft():
    print(f"\n⏰ [TRIGGER] Scheduled Minecraft Generation & Upload at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        run_pipeline("minecraft")
    except Exception as e:
        print(f"❌ Error in Minecraft scheduled job: {e}")

def main():
    print("=" * 65)
    print("🤖 Autonomous YouTube Shorts Daily 12-Hour Scheduler Daemon Started")
    print("=" * 65)
    print("📅 Scheduled Times (Peak Viral Gaming Windows):")
    print("   🎮 ROBLOX:    08:00 AM & 08:00 PM (12-hour gap)")
    print("   ⛏️  MINECRAFT: 09:00 AM & 09:00 PM (12-hour gap)")
    print("=" * 65)
    
    # Schedule Roblox: 08:00 and 20:00 (8:00 AM and 8:00 PM)
    schedule.every().day.at("08:00").do(job_roblox)
    schedule.every().day.at("20:00").do(job_roblox)
    
    # Schedule Minecraft: 09:00 and 21:00 (9:00 AM and 9:00 PM)
    schedule.every().day.at("09:00").do(job_minecraft)
    schedule.every().day.at("21:00").do(job_minecraft)

    print(f"Daemon active and waiting for next scheduled slot... (Current Time: {time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    main()
