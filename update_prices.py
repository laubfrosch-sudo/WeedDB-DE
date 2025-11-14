#!/usr/bin/env python3
"""
Update prices for all products in the database.

This script queries all existing products from the database and
re-scrapes their prices by running add_product.py with the product name.

Usage:
    python3 update_prices.py
"""

import sqlite3
import subprocess
import sys
from typing import List, Tuple

def get_all_products() -> List[Tuple[int, str]]:
    """Fetch all products from database"""
    conn = sqlite3.connect('WeedDB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM products ORDER BY name")
    products = cursor.fetchall()

    conn.close()
    return products

def update_product_prices(product_name: str) -> bool:
    """Update prices for a single product by calling add_product.py"""
    try:
        print(f"\n{'='*60}")
        print(f"Updating: {product_name}")
        print(f"{'='*60}")

        result = subprocess.run(
            ['python3', 'add_product.py', product_name],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout per product
        )

        # Print output
        if result.stdout:
            print(result.stdout)

        if result.returncode == 0:
            print(f"✅ Successfully updated '{product_name}'")
            return True
        else:
            print(f"❌ Failed to update '{product_name}'")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout updating '{product_name}' (>2 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error updating '{product_name}': {e}")
        return False

def main() -> None:
    """Main function to update all products"""
    print("📊 WeedDB Price Update Script")
    print("="*60)

    # Get all products
    products = get_all_products()

    if not products:
        print("❌ No products found in database!")
        print("💡 Add products first using: python3 add_product.py '<product_name>'")
        sys.exit(1)

    total = len(products)
    print(f"\n📦 Found {total} products in database")
    print(f"⏱️  Estimated time: ~{total * 30} seconds ({total * 0.5:.1f} minutes)\n")

    # Confirm before proceeding
    response = input("Continue with price update? [y/N]: ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Cancelled by user")
        sys.exit(0)

    # Update each product
    success_count = 0
    failed_products = []

    for i, (product_id, product_name) in enumerate(products, 1):
        print(f"\n[{i}/{total}] Processing...")

        if update_product_prices(product_name):
            success_count += 1
        else:
            failed_products.append(product_name)

    # Print summary
    print("\n" + "="*60)
    print("📊 UPDATE SUMMARY")
    print("="*60)
    print(f"✅ Successful: {success_count}/{total}")
    print(f"❌ Failed: {len(failed_products)}/{total}")

    if failed_products:
        print("\n❌ Failed products:")
        for name in failed_products:
            print(f"   - {name}")

    print("\n✨ Update complete!")

if __name__ == '__main__':
    main()
