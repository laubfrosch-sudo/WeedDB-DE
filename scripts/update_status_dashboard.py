"""
Update the Obsidian process status dashboard with current batch processing information.

This script reads the latest batch reports and updates PROCESS_STATUS.md with
live information about the current processing state.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import sqlite3

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
STATUS_FILE = PROJECT_ROOT / "PROCESS_STATUS.md"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = DATA_DIR / "logs"
REPORTS_DIR = DATA_DIR / "reports"

def get_database_stats() -> Dict[str, Any]:
    """Get current database statistics"""
    db_path = DATA_DIR / "WeedDB.db"
    if not db_path.exists():
        return {"total_products": 0, "last_updated": "Never"}

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Total products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]

        # Last updated
        cursor.execute("SELECT MAX(last_updated) FROM products")
        last_updated = cursor.fetchone()[0]

        conn.close()

        return {
            "total_products": total_products,
            "last_updated": last_updated or "Unknown"
        }
    except Exception as e:
        return {"total_products": 0, "error": str(e)}

def get_latest_batch_report() -> Dict[str, Any]:
    """Get information from the latest batch processing report"""
    if not REPORTS_DIR.exists():
        return {"found": False}

    try:
        # Find latest batch report
        batch_reports = list(REPORTS_DIR.glob("batch_report_*.json"))
        if not batch_reports:
            return {"found": False}

        latest_report = max(batch_reports, key=lambda x: x.stat().st_mtime)

        with open(latest_report, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            "found": True,
            "timestamp": data.get("timestamp", "Unknown"),
            "total_products": data.get("total_products", 0),
            "successful": data.get("successful", 0),
            "failed": data.get("failure_count", 0),
            "total_duration": data.get("total_duration", 0),
            "concurrency": data.get("concurrency", 1),
            "results": data.get("results", [])
        }
    except Exception as e:
        return {"found": False, "error": str(e)}

def get_cache_stats() -> Dict[str, Any]:
    """Get cache performance statistics"""
    try:
        # Basic cache stats - could be enhanced later
        cache_db = DATA_DIR / "cache.db"
        if cache_db.exists():
            size_mb = round(cache_db.stat().st_size / (1024 * 1024), 2)
            return {
                "total_entries": "Unknown",  # Would need cache_manager
                "expired_entries": 0,
                "db_size_mb": size_mb
            }
        return {"total_entries": 0, "expired_entries": 0, "db_size_mb": 0}
    except Exception:
        return {"total_entries": 0, "expired_entries": 0, "db_size_mb": 0}

def get_performance_stats() -> Dict[str, Any]:
    """Get basic performance statistics"""
    # For now, return placeholder data
    # This could be enhanced to read from log files directly
    return {
        "add_product": {"avg_duration_ms": 0, "success_rate": 0, "total_operations": 0},
        "add_products_parallel": {"avg_duration_ms": 0, "success_rate": 0, "total_operations": 0},
        "update_prices": {"avg_duration_ms": 0, "success_rate": 0, "total_operations": 0}
    }

def update_status_file():
    """Update the PROCESS_STATUS.md file with current information"""

    # Gather all data
    db_stats = get_database_stats()
    batch_stats = get_latest_batch_report()
    cache_stats = get_cache_stats()
    perf_stats = get_performance_stats()

    # Read current status file
    if STATUS_FILE.exists():
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# Default content will be replaced"

    # Update database stats
    total_products = db_stats.get("total_products", 0)
    content = content.replace(
        "**📊 Gesamtprodukte in DB**: `= length(this.file.inlinks)`",
        f"**📊 Gesamtprodukte in DB**: {total_products}"
    )

    # Update batch status
    if batch_stats.get("found"):
        successful = batch_stats.get("successful", 0)
        failed = batch_stats.get("failed", 0)
        total = batch_stats.get("total_products", 0)
        duration = batch_stats.get("total_duration", 0)

        content = content.replace(
            "**📊 Verarbeitete Produkte**: 0",
            f"**📊 Verarbeitete Produkte**: {total}"
        )
        content = content.replace(
            "**✅ Erfolgreich**: 0",
            f"**✅ Erfolgreich**: {successful}"
        )
        content = content.replace(
            "**❌ Fehlgeschlagen**: 0",
            f"**❌ Fehlgeschlagen**: {failed}"
        )

        # Calculate speed
        if duration > 0:
            speed = round((total / duration) * 60, 1)  # products per minute
            content = content.replace(
                "**⚡ Durchschnittliche Geschwindigkeit**: 0 Produkte/Minute",
                f"**⚡ Durchschnittliche Geschwindigkeit**: {speed} Produkte/Minute"
            )

    # Update cache stats
    cache_entries = cache_stats.get("total_entries", 0)
    cache_size = cache_stats.get("db_size_mb", 0)

    content = content.replace(
        "**🗄️ Cache-Effizienz**: 85% Hit-Rate",
        f"**🗄️ Cache-Effizienz**: {cache_entries} Einträge"
    )
    content = content.replace(
        "**💾 Speicherersparnis**: 3.2MB Cache-Daten",
        f"**💾 Speicherersparnis**: {cache_size}MB Cache-Daten"
    )

    # Update performance table
    perf_table = "| Script | ⏱️ Avg Duration | 📈 Success Rate | 🔢 Total Ops |\n|--------|----------------|-----------------|--------------|\n"

    for script, stats in perf_stats.items():
        duration = stats.get("avg_duration_ms", 0)
        success_rate = stats.get("success_rate", 0)
        total_ops = stats.get("total_operations", 0)

        perf_table += f"| {script} | {duration}ms | {success_rate}% | {total_ops} |\n"

    # Find and replace the performance table
    start_marker = "```dataview\nTABLE WITHOUT ID\nrows.file.link AS \"Script\",\nrows.\"Avg Duration (ms)\" AS \"⏱️ Avg Duration\",\nrows.\"Success Rate (%)\" AS \"📈 Success Rate\",\nrows.\"Total Operations\" AS \"🔢 Total Ops\"\nFROM \"data/logs/performance_stats.json\"\nFLATTEN file.lists AS rows\nWHERE rows.file = this.file\nSORT rows.\"Success Rate (%)\" DESC\n```"
    end_marker = "### Cache-Performance"

    if start_marker in content:
        content = content.replace(start_marker, perf_table, 1)

    # Update timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = content.replace(
        "*📊 Diese Datei wird automatisch von den Processing-Scripts aktualisiert. Letzte Aktualisierung: `= dateformat(this.file.mtime, \"yyyy-MM-dd HH:mm:ss\")`*",
        f"*📊 Diese Datei wird automatisch von den Processing-Scripts aktualisiert. Letzte Aktualisierung: {now}*"
    )

    # Write updated content
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Status-Datei aktualisiert: {STATUS_FILE}")

def main():
    """Main function"""
    try:
        update_status_file()
        print("✅ Process status dashboard updated successfully!")
    except Exception as e:
        print(f"❌ Error updating status dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()