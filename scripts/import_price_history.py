#!/usr/bin/env python3
"""
Import price history data from JSON files.

Allows importing price data from external sources or
previously exported WeedDB price history files.

Usage:
    python3 scripts/import_price_history.py <json_file>
    
Example:
    python3 scripts/import_price_history.py ../data/price_history/2025-11-14.json
"""

import sqlite3
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

def validate_price_data(data: Dict[str, Any]) -> bool:
    """Validate the structure of imported price data"""
    if 'export_type' not in data:
        print("❌ Missing 'export_type' field")
        return False
    
    if data['export_type'] == 'current_snapshot':
        if 'products' not in data:
            print("❌ Missing 'products' field in snapshot")
            return False
    elif data['export_type'] == 'complete_history':
        if 'data' not in data:
            print("❌ Missing 'data' field in history")
            return False
    else:
        print(f"❌ Unknown export_type: {data['export_type']}")
        return False
    
    return True

def import_current_snapshot(data: Dict[str, Any]) -> int:
    """Import a current price snapshot"""
    conn = sqlite3.connect('../data/WeedDB.db')
    cursor = conn.cursor()
    
    imported_count = 0
    
    try:
        for product_name, categories in data['products'].items():
            # Get product ID
            cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
            product_result = cursor.fetchone()
            
            if not product_result:
                print(f"⚠️  Product '{product_name}' not found, skipping")
                continue
            
            product_id = product_result[0]
            
            for category, price_data in categories.items():
                price = price_data['price']
                pharmacy_name = price_data['pharmacy']
                
                # Get or create pharmacy
                cursor.execute("INSERT OR IGNORE INTO pharmacies (name) VALUES (?)", (pharmacy_name,))
                cursor.execute("SELECT id FROM pharmacies WHERE name = ?", (pharmacy_name,))
                pharmacy_result = cursor.fetchone()
                pharmacy_id = pharmacy_result[0] if pharmacy_result else None
                
                # Insert price (will update if exists due to our logic)
                cursor.execute("""
                    INSERT INTO prices (product_id, pharmacy_id, price_per_g, category, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_id, pharmacy_id, price, category, datetime.now()))
                
                imported_count += 1
        
        conn.commit()
        print(f"✅ Imported {imported_count} price entries from snapshot")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Import failed: {e}")
        return 0
    finally:
        conn.close()
    
    return imported_count

def import_complete_history(data: Dict[str, Any]) -> int:
    """Import complete price history"""
    conn = sqlite3.connect('../data/WeedDB.db')
    cursor = conn.cursor()
    
    imported_count = 0
    
    try:
        for date_str, products in data['data'].items():
            for product_name, categories in products.items():
                # Get product ID
                cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
                product_result = cursor.fetchone()
                
                if not product_result:
                    print(f"⚠️  Product '{product_name}' not found, skipping")
                    continue
                
                product_id = product_result[0]
                
                for category, price_entries in categories.items():
                    for entry in price_entries:
                        price = entry['price']
                        pharmacy_name = entry['pharmacy']
                        timestamp = entry['timestamp']
                        
                        # Get or create pharmacy
                        cursor.execute("INSERT OR IGNORE INTO pharmacies (name) VALUES (?)", (pharmacy_name,))
                        cursor.execute("SELECT id FROM pharmacies WHERE name = ?", (pharmacy_name,))
                        pharmacy_result = cursor.fetchone()
                        pharmacy_id = pharmacy_result[0] if pharmacy_result else None
                        
                        # Insert into price_history
                        cursor.execute("""
                            INSERT INTO price_history 
                            (product_id, pharmacy_id, price_per_g, category, recorded_at, pharmacy_name)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (product_id, pharmacy_id, price, category, timestamp, pharmacy_name))
                        
                        imported_count += 1
        
        conn.commit()
        print(f"✅ Imported {imported_count} historical price entries")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Import failed: {e}")
        return 0
    finally:
        conn.close()
    
    return imported_count

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/import_price_history.py <json_file>")
        print("Example: python3 scripts/import_price_history.py ../data/price_history/2025-11-14.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    print(f"📥 WeedDB Price History Import")
    print(f"📄 File: {json_file}")
    print()
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Data type: {data.get('export_type', 'unknown')}")
        
        if not validate_price_data(data):
            sys.exit(1)
        
        if data['export_type'] == 'current_snapshot':
            imported = import_current_snapshot(data)
        elif data['export_type'] == 'complete_history':
            imported = import_complete_history(data)
        else:
            print(f"❌ Unsupported export type: {data['export_type']}")
            sys.exit(1)
        
        if imported > 0:
            print(f"✅ Successfully imported {imported} price entries")
        else:
            print("⚠️  No data was imported")
            
    except FileNotFoundError:
        print(f"❌ File not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
