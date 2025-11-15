#!/bin/bash
# Daily price update for WeedDB
# Run with: 0 2 * * * /Users/lars/Desktop/Claude/WeedDB-DE/scripts/cron/daily_update.sh

cd /Users/lars/Desktop/Claude/WeedDB-DE
python3 scripts/scheduler.py daily_update

# Log completion
echo "Daily update completed at $(date)" >> data/logs/cron.log
