"""
Automated scheduler for WeedDB maintenance tasks.

Provides cron-like functionality for regular database maintenance,
price updates, and reporting tasks.

Features:
- Daily price updates
- Weekly overview generation
- Monthly cleanup tasks
- Configurable schedules
- Logging and error handling

Usage:
    python3 scheduler.py daily_update
    python3 scheduler.py weekly_overview
    python3 scheduler.py monthly_cleanup
"""

import asyncio
import sys
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
import logging
import argparse

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('scheduler')

class TaskScheduler:
    """Scheduler for automated WeedDB tasks"""

    def __init__(self):
        self.logger = logger

    async def run_task(self, task_name: str, task_func: Callable, *args, **kwargs) -> bool:
        """Run a task with error handling and logging"""
        start_time = time.time()

        try:
            self.logger.info(f"Starting task: {task_name}")
            await task_func(*args, **kwargs)
            duration = time.time() - start_time
            self.logger.info(f"Task completed successfully: {task_name} ({duration:.1f}s)")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Task failed: {task_name} ({duration:.1f}s): {e}")
            return False

    async def daily_price_update(self) -> None:
        """Update prices for all products (daily task)"""
        self.logger.info("Starting daily price update")

        # Run update_prices.py
        result = await self._run_subprocess(
            [sys.executable, str(SCRIPT_DIR / "update_prices.py")],
            timeout=3600  # 1 hour timeout
        )

        if result:
            self.logger.info("Daily price update completed")
        else:
            raise Exception("Daily price update failed")

    async def weekly_overview_generation(self) -> None:
        """Generate product overview (weekly task)"""
        self.logger.info("Starting weekly overview generation")

        # Run generate_overview.py
        result = await self._run_subprocess(
            [sys.executable, str(SCRIPT_DIR / "generate_overview.py")],
            timeout=600  # 10 minutes timeout
        )

        if result:
            self.logger.info("Weekly overview generation completed")
        else:
            raise Exception("Weekly overview generation failed")

    async def monthly_cleanup(self) -> None:
        """Perform monthly maintenance tasks"""
        self.logger.info("Starting monthly cleanup")

        tasks = [
            self._cleanup_old_logs,
            self._optimize_database,
            self._cleanup_cache,
            self._generate_monthly_report
        ]

        for task in tasks:
            try:
                await task()
            except Exception as e:
                self.logger.error(f"Monthly cleanup task failed: {e}")
                # Continue with other tasks

        self.logger.info("Monthly cleanup completed")

    async def _cleanup_old_logs(self) -> None:
        """Clean up old log files (keep last 30 days)"""
        log_dir = PROJECT_ROOT / "data" / "logs"
        if not log_dir.exists():
            return

        cutoff_date = datetime.now() - timedelta(days=30)

        for log_file in log_dir.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()
                self.logger.info(f"Deleted old log file: {log_file.name}")

    async def _optimize_database(self) -> None:
        """Optimize SQLite database"""
        db_path = PROJECT_ROOT / "data" / "WeedDB.db"
        if not db_path.exists():
            return

        # Run SQLite optimization
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            conn.execute("VACUUM")
            conn.execute("ANALYZE")
            self.logger.info("Database optimized")

    async def _cleanup_cache(self) -> None:
        """Clean up expired cache entries"""
        self.logger.info("Cache cleanup not implemented yet")

    async def _generate_monthly_report(self) -> None:
        """Generate monthly statistics report"""
        try:
            # Basic report for now
            report = {
                'generated_at': datetime.now().isoformat(),
                'message': 'Monthly report generation not fully implemented yet'
            }

            # Save report
            report_dir = PROJECT_ROOT / "data" / "reports"
            report_dir.mkdir(exist_ok=True)

            report_file = report_dir / f"monthly_report_{datetime.now().strftime('%Y%m')}.json"

            import json
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)

            self.logger.info(f"Monthly report generated: {report_file}")

        except Exception as e:
            self.logger.error(f"Failed to generate monthly report: {e}")

    async def _run_subprocess(self, cmd: List[str], timeout: int = 300) -> bool:
        """Run a subprocess with timeout and error handling"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=PROJECT_ROOT
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise Exception(f"Process timed out after {timeout}s")

            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Process failed with code {process.returncode}: {error_msg}")

            return True

        except Exception as e:
            self.logger.error(f"Subprocess execution failed: {e}")
            return False

    async def run_scheduled_task(self, task_type: str) -> bool:
        """Run a scheduled task by type"""
        task_map = {
            'daily_update': self.daily_price_update,
            'weekly_overview': self.weekly_overview_generation,
            'monthly_cleanup': self.monthly_cleanup,
        }

        if task_type not in task_map:
            self.logger.error(f"Unknown task type: {task_type}")
            available = ', '.join(task_map.keys())
            self.logger.error(f"Available tasks: {available}")
            return False

        task_func = task_map[task_type]
        return await self.run_task(task_type, task_func)

def create_cron_scripts():
    """Create cron-compatible shell scripts for common tasks"""

    cron_dir = PROJECT_ROOT / "scripts" / "cron"
    cron_dir.mkdir(exist_ok=True)

    # Daily update script
    daily_script = cron_dir / "daily_update.sh"
    daily_script.write_text(f"""#!/bin/bash
# Daily price update for WeedDB
# Run with: 0 2 * * * {daily_script}

cd {PROJECT_ROOT}
python3 scripts/scheduler.py daily_update

# Log completion
echo "Daily update completed at $(date)" >> data/logs/cron.log
""")
    daily_script.chmod(0o755)

    # Weekly overview script
    weekly_script = cron_dir / "weekly_overview.sh"
    weekly_script.write_text(f"""#!/bin/bash
# Weekly overview generation for WeedDB
# Run with: 0 3 * * 0 {weekly_script}

cd {PROJECT_ROOT}
python3 scripts/scheduler.py weekly_overview

# Log completion
echo "Weekly overview completed at $(date)" >> data/logs/cron.log
""")
    weekly_script.chmod(0o755)

    # Monthly cleanup script
    monthly_script = cron_dir / "monthly_cleanup.sh"
    monthly_script.write_text(f"""#!/bin/bash
# Monthly cleanup for WeedDB
# Run with: 0 4 1 * * {monthly_script}

cd {PROJECT_ROOT}
python3 scripts/scheduler.py monthly_cleanup

# Log completion
echo "Monthly cleanup completed at $(date)" >> data/logs/cron.log
""")
    monthly_script.chmod(0o755)

    print("Cron scripts created in scripts/cron/")
    print("To install cron jobs, run:")
    print(f"  crontab -e")
    print("And add these lines:")
    print(f"  0 2 * * * {daily_script}          # Daily at 2:00")
    print(f"  0 3 * * 0 {weekly_script}         # Weekly at 3:00 (Sunday)")
    print(f"  0 4 1 * * {monthly_script}        # Monthly at 4:00 (1st of month)")

def main():
    parser = argparse.ArgumentParser(
        description="WeedDB automated task scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scheduler.py daily_update
  python3 scheduler.py weekly_overview
  python3 scheduler.py monthly_cleanup

Cron Setup:
  python3 scheduler.py --create-cron-scripts
        """
    )

    parser.add_argument('task', nargs='?', help='Task to run (daily_update, weekly_overview, monthly_cleanup)')
    parser.add_argument('--create-cron-scripts', action='store_true',
                       help='Create cron-compatible shell scripts')

    args = parser.parse_args()

    if args.create_cron_scripts:
        create_cron_scripts()
        return

    if not args.task:
        parser.print_help()
        sys.exit(1)

    # Run the scheduler
    scheduler = TaskScheduler()

    try:
        success = asyncio.run(scheduler.run_scheduled_task(args.task))
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\nScheduler interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Scheduler failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()