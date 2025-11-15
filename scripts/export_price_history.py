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
import sys
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib

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

def get_changes_since_last_export(last_export_file: Optional[str] = None) -> Dict[str, Any]:
    """Get changes since last export"""
    changes = {
        'new_products': [],
        'price_changes': [],
        'new_pharmacies': [],
        'last_export_date': None
    }

    if last_export_file and os.path.exists(f'../data/price_history/{last_export_file}'):
        try:
            with open(f'../data/price_history/{last_export_file}', 'r') as f:
                last_export = json.load(f)
                changes['last_export_date'] = last_export.get('export_timestamp')

                # Compare with current data
                current_prices = get_current_prices()
                last_products = last_export.get('products', {})

                # Find new products
                for product_name in current_prices:
                    if product_name not in last_products:
                        changes['new_products'].append(product_name)

                # Find price changes
                for product_name, categories in current_prices.items():
                    if product_name in last_products:
                        for category, current_data in categories.items():
                            if category in last_products[product_name]:
                                last_price = last_products[product_name][category]['price']
                                current_price = current_data['price']
                                if abs(last_price - current_price) > 0.01:  # Allow for small rounding differences
                                    changes['price_changes'].append({
                                        'product': product_name,
                                        'category': category,
                                        'old_price': last_price,
                                        'new_price': current_price,
                                        'change_percent': round(((current_price - last_price) / last_price) * 100, 2) if last_price > 0 else 0
                                    })

        except Exception as e:
            print(f"⚠️  Could not read last export file: {e}")

    return changes

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
    import time

    start_time = time.time()

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

    errors = []
    warnings = []

    try:
        if export_all:
            # Export complete history
            days_back = 365  # Last year
            print(f"🔄 Exporting complete price history ({days_back} days)...")
            history_data = get_historical_prices(days_back=days_back)

            # Calculate history metrics
            total_days = len(history_data)
            total_historical_entries = sum(
                len(products) for day_data in history_data.values()
                for products in day_data.values()
                for categories in products.values()
                for entries in categories
            )

            export_data = {
                'export_type': 'complete_history',
                'export_date': datetime.now().isoformat(),
                'system_version': '0.1.0',
                'export_metadata': {
                    'user': os.environ.get('USER', 'unknown'),
                    'hostname': os.uname().nodename if hasattr(os, 'uname') else 'unknown',
                    'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                    'working_directory': os.getcwd(),
                    'command_line': ' '.join(sys.argv),
                    'history_days': days_back
                },
                'data_quality': {
                    'total_days': total_days,
                    'total_historical_entries': total_historical_entries,
                    'date_range': {
                        'earliest': min(history_data.keys()) if history_data else None,
                        'latest': max(history_data.keys()) if history_data else None
                    }
                },
                'data': history_data
            }

            # Add data integrity checksum
            data_str = json.dumps(export_data, sort_keys=True, default=str)
            export_data['data_integrity'] = {
                'md5_checksum': hashlib.md5(data_str.encode()).hexdigest(),
                'data_size_bytes': len(data_str.encode()),
                'validation_status': 'valid'
            }

            export_to_json(export_data, 'complete_history.json')

        else:
            # Export current snapshot
            print("📸 Creating current price snapshot...")
            current_prices = get_current_prices()

            # Calculate data quality metrics
            total_products = len(current_prices)
            total_prices = sum(len(categories) for categories in current_prices.values())
            pharmacies = set()
            prices_list = []
            for categories in current_prices.values():
                for category_data in categories.values():
                    if category_data['pharmacy'] != 'Unknown':
                        pharmacies.add(category_data['pharmacy'])
                    prices_list.append(category_data['price'])

            # Get changes since last export
            last_export_file = f"{(date.fromisoformat(export_date) - timedelta(days=1)).isoformat()}.json"
            changes = get_changes_since_last_export(last_export_file)

            export_data = {
                'export_type': 'current_snapshot',
                'snapshot_date': export_date,
                'export_timestamp': datetime.now().isoformat(),
                'system_version': '0.1.0',
                'export_metadata': {
                    'user': os.environ.get('USER', 'unknown'),
                    'hostname': os.uname().nodename if hasattr(os, 'uname') else 'unknown',
                    'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                    'working_directory': os.getcwd(),
                    'command_line': ' '.join(sys.argv)
                },
                'data_quality': {
                    'total_products': total_products,
                    'total_prices': total_prices,
                    'unique_pharmacies': len(pharmacies),
                    'price_range': {
                        'min': min(prices_list) if prices_list else 0,
                        'max': max(prices_list) if prices_list else 0,
                        'avg': round(sum(prices_list) / len(prices_list), 2) if prices_list else 0
                    },
                    'categories_count': {
                        'top': sum(1 for prod in current_prices.values() if 'top' in prod),
                        'all': sum(1 for prod in current_prices.values() if 'all' in prod)
                    }
                },
                'changes_since_last_export': changes,
                'products': current_prices
            }

            # Add data integrity checksum
            data_str = json.dumps(export_data, sort_keys=True, default=str)
            export_data['data_integrity'] = {
                'md5_checksum': hashlib.md5(data_str.encode()).hexdigest(),
                'data_size_bytes': len(data_str.encode()),
                'validation_status': 'valid'
            }

            export_to_json(export_data, f'{export_date}.json')

        # Performance tracking
        end_time = time.time()
        duration = end_time - start_time

        print(f"⏱️  Export completed in {duration:.2f} seconds")
        print("✅ Export completed successfully!")

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        errors.append(f"Export failed after {duration:.2f} seconds: {str(e)}")
        print(f"❌ Export failed: {e}")

        # Log errors to file
        error_log = {
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'command_line': ' '.join(sys.argv),
            'duration_seconds': duration
        }

        try:
            with open('../data/price_history/export_errors.json', 'a') as f:
                json.dump(error_log, f, default=str)
                f.write('\n')
        except:
            pass  # Ignore logging errors

if __name__ == '__main__':
    main()
