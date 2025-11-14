#!/usr/bin/env python3
"""
Export price history data for external use.

Exports current prices and historical data in JSON format
for easy integration with other programs and analysis tools.

Usage:
    python3 scripts/export_price_history.py [--date YYYY-MM-DD] [--all]
    
Options:
    --date YYYY-MM-DD: Export data for specific date (default: today)
    --all: Export complete history instead of current snapshot
"""

import sqlite3
import json
import os
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from pathlib import Path

def get_current_prices() -> Dict[str, Any]:
    """Get current prices snapshot"""
    conn = sqlite3.connect('../data/WeedDB.db')
    cursor = conn.cursor()
    
    # Get latest prices for each product/category combination
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
    
    prices_data = {}
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
    return prices_data

def get_historical_prices(days_back: int = 30) -> Dict[str, Any]:
    """Get historical price data"""
    conn = sqlite3.connect('../data/WeedDB.db')
    cursor = conn.cursor()
    
    # Get price history for the last N days
    cursor.execute("""
        SELECT 
            DATE(ph.recorded_at) as date,
            p.name as product_name,
            ph.price_per_g,
            ph.category,
            ph.pharmacy_name,
            ph.recorded_at
        FROM price_history ph
        JOIN products p ON ph.product_id = p.id
        WHERE DATE(ph.recorded_at) >= DATE('now', '-{} days')
        ORDER BY ph.recorded_at DESC, p.name, ph.category
    """.format(days_back))
    
    history_data = {}
    for row in cursor.fetchall():
        date_str, product_name, price, category, pharmacy, timestamp = row
        
        if date_str not in history_data:
            history_data[date_str] = {}
        
        if product_name not in history_data[date_str]:
            history_data[date_str][product_name] = {}
        
        if category not in history_data[date_str][product_name]:
            history_data[date_str][product_name][category] = []
        
        history_data[date_str][product_name][category].append({
            'price': price,
            'pharmacy': pharmacy or 'Unknown',
            'timestamp': timestamp
        })
    
    conn.close()
    return history_data

def export_to_json(data: Dict[str, Any], filename: str) -> None:
    """Export data to JSON file"""
    os.makedirs('../data/price_history', exist_ok=True)
    
    filepath = f'../data/price_history/{filename}'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ Exported to {filepath}")

def main():
    import sys
    
    # Parse arguments
    export_date = date.today().isoformat()
    export_all = False
    
    if len(sys.argv) > 1:
        if '--all' in sys.argv:
            export_all = True
        elif sys.argv[1].startswith('--date='):
            export_date = sys.argv[1].split('=')[1]
        elif len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
            export_date = sys.argv[1]
    
    print(f"📊 WeedDB Price History Export")
    print(f"📅 Date: {export_date}")
    print(f"📈 Mode: {'Complete History' if export_all else 'Current Snapshot'}")
    print()
    
    if export_all:
        # Export complete history
        print("🔄 Exporting complete price history...")
        history_data = get_historical_prices(days_back=365)  # Last year
        
        export_data = {
            'export_type': 'complete_history',
            'export_date': datetime.now().isoformat(),
            'data': history_data
        }
        
        export_to_json(export_data, 'complete_history.json')
        
    else:
        # Export current snapshot
        print("📸 Creating current price snapshot...")
        current_prices = get_current_prices()
        
        export_data = {
            'export_type': 'current_snapshot',
            'snapshot_date': export_date,
            'export_timestamp': datetime.now().isoformat(),
            'products': current_prices
        }
        
        export_to_json(export_data, f'{export_date}.json')
    
    print("✅ Export completed successfully!")

if __name__ == '__main__':
    main()
