#!/usr/bin/env python3
import sys
"""
Automatic price archiving script.

Creates daily snapshots of current prices and manages historical data.
Designed to be run automatically (e.g., via cron job).

Usage:
    python3 scripts/archive_prices.py [--cleanup-days N]
    
Options:
    --cleanup-days N: Remove history older than N days (default: 365)
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def create_price_snapshot(date_str: Optional[str] = None) -> bool:
    """Create a price snapshot"""
    if date_str is None:
        date_str = datetime.now().date().isoformat()
    
    try:
        # Get current prices
        conn = sqlite3.connect('../data/WeedDB.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                p.name as product_name,
                pr.price_per_g,
                pr.category,
                ph.name as pharmacy_name,
                pr.timestamp
            FROM products p
            JOIN prices pr ON p.id = pr.product_id
            LEFT JOIN pharmacies ph ON pr.pharmacy_id = ph.id
            WHERE pr.timestamp = (
                SELECT MAX(timestamp) 
                FROM prices 
                WHERE product_id = p.id AND category = pr.category
            )
            ORDER BY p.name, pr.category
        """)
        
        prices_data: Dict[str, Dict[str, Any]] = {}
        for row in cursor.fetchall():
            product_name, price, category, pharmacy, timestamp = row
            
            if product_name not in prices_data:
                prices_data[product_name] = {}
            
            prices_data[product_name][category] = {
                'price': price,
                'pharmacy': pharmacy or 'Unknown',
                'timestamp': timestamp
            }
        
        conn.close()
        
        # Export to JSON
        os.makedirs('../data/price_history', exist_ok=True)
        
        export_data = {
            'export_type': 'current_snapshot',
            'snapshot_date': date_str,
            'export_timestamp': datetime.now().isoformat(),
            'products': prices_data
        }
        
        filepath = f'../data/price_history/{date_str}.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Price snapshot created: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Snapshot creation failed: {e}")
        return False

def cleanup_old_history(days_to_keep: int = 365) -> int:
    """Remove price history older than specified days"""
    conn = sqlite3.connect('../data/WeedDB.db')
    cursor = conn.cursor()
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    try:
        cursor.execute("DELETE FROM price_history WHERE recorded_at < ?", (cutoff_date,))
        deleted_count = cursor.rowcount
        conn.commit()
        
        print(f"🧹 Cleaned up {deleted_count} old price history entries")
        return deleted_count
    except Exception as e:
        conn.rollback()
        print(f"❌ Cleanup failed: {e}")
        return 0
    finally:
        conn.close()

def cleanup_old_files(days_to_keep: int = 90) -> int:
    """Remove old export files"""
    history_dir = Path('../data/price_history')
    if not history_dir.exists():
        return 0
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = 0
    
    for file_path in history_dir.glob('*.json'):
        if file_path.name in ['complete_history.json']:
            continue
            
        try:
            date_str = file_path.stem
            file_date = datetime.fromisoformat(date_str)
            
            if file_date < cutoff_date:
                file_path.unlink()
                deleted_count += 1
        except:
            continue
    
    if deleted_count > 0:
        print(f"🧹 Cleaned up {deleted_count} old export files")
    
    return deleted_count

def main() -> None:
    print("📦 WeedDB Automatic Price Archiving")
    print(f"🕒 Started at: {datetime.now()}")
    print()
    
    # Parse arguments
    cleanup_days = 365
    
    if len(sys.argv) > 1 and sys.argv[1].startswith('--cleanup-days='):
        try:
            cleanup_days = int(sys.argv[1].split('=')[1])
        except ValueError:
            print("❌ Invalid cleanup days value")
            return
    
    print(f"🗂️  History retention: {cleanup_days} days")
    print()
    
    # Step 1: Create today's snapshot
    print("📸 Step 1: Creating daily price snapshot...")
    today = datetime.now().date().isoformat()
    if create_price_snapshot(today):
        print("✅ Daily snapshot completed")
    else:
        print("❌ Daily snapshot failed")
        return
    
    print()
    
    # Step 2: Cleanup old data
    print("🧹 Step 2: Cleaning up old data...")
    db_cleaned = cleanup_old_history(cleanup_days)
    files_cleaned = cleanup_old_files(90)
    
    print(f"✅ Cleanup completed ({db_cleaned} DB entries, {files_cleaned} files)")
    print()
    
    print("🎉 Automatic archiving completed successfully!")
    print(f"🏁 Finished at: {datetime.now()}")

if __name__ == '__main__':
    main()
