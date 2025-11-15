#!/bin/bash
# Weekly overview generation for WeedDB
# Run with: 0 3 * * 0 /Users/lars/Desktop/Claude/WeedDB-DE/scripts/cron/weekly_overview.sh

cd /Users/lars/Desktop/Claude/WeedDB-DE
python3 scripts/scheduler.py weekly_overview

# Log completion
echo "Weekly overview completed at $(date)" >> data/logs/cron.log
