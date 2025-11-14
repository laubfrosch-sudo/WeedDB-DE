#!/usr/bin/env python3
"""Update all products in database with enhanced data"""

import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

def get_all_product_urls() -> List[Tuple[int, str]]:
    """Get all product URLs from database"""
    conn = sqlite3.connect('WeedDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, url FROM products ORDER BY id")
    results = cursor.fetchall()
    conn.close()
    return results

def update_product(product_id: int, url: str) -> Tuple[int, bool, str]:
    """Update a single product by running add_product.py"""
    try:
        result = subprocess.run(
            ['python3', 'add_product.py', url],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return (product_id, True, "Success")
        else:
            return (product_id, False, result.stderr)
    except subprocess.TimeoutExpired:
        return (product_id, False, "Timeout")
    except Exception as e:
        return (product_id, False, str(e))

def main() -> None:
    products = get_all_product_urls()
    total = len(products)

    print(f"📊 Updating {total} products with enhanced data...")
    print(f"   This will take approximately {total * 5 / 60:.1f} minutes\n")

    # Process in batches of 5 concurrent requests
    batch_size = 5
    success_count = 0
    failed = []

    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        # Submit all tasks
        futures = {executor.submit(update_product, pid, url): (pid, url) for pid, url in products}

        # Process results as they complete
        for i, future in enumerate(as_completed(futures), 1):
            product_id, url = futures[future]
            pid, success, message = future.result()

            if success:
                success_count += 1
                print(f"✅ [{i}/{total}] Product {pid} updated successfully")
            else:
                failed.append((pid, url, message))
                print(f"❌ [{i}/{total}] Product {pid} failed: {message}")

    print(f"\n📊 Summary:")
    print(f"   Total: {total}")
    print(f"   Success: {success_count}")
    print(f"   Failed: {len(failed)}")

    if failed:
        print(f"\n❌ Failed products:")
        for pid, url, msg in failed:
            print(f"   Product {pid}: {msg}")

if __name__ == '__main__':
    main()
