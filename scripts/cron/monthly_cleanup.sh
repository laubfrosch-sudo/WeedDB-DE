#!/bin/bash
# Monthly cleanup for WeedDB
# Run with: 0 4 1 * * /Users/lars/Desktop/Claude/WeedDB-DE/scripts/cron/monthly_cleanup.sh

cd /Users/lars/Desktop/Claude/WeedDB-DE
python3 scripts/scheduler.py monthly_cleanup

# Log completion
echo "Monthly cleanup completed at $(date)" >> data/logs/cron.log
