#!/usr/bin/env python3
"""
Add multiple products to the database from a list.

Usage:
    python3 add_products_batch.py <product_names_file>
    python3 add_products_batch.py products.txt

File format:
    One product name per line
    Lines starting with # are treated as comments

Example products.txt:
    # Indica strains
    sourdough
    gelato
    wedding cake

    # Sativa strains
    amnesia haze
    super lemon haze
"""

import subprocess
import sys
from typing import List

def read_product_names(filename: str) -> List[str]:
    """Read product names from file, ignoring comments and empty lines"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        products = []
        for line in lines:
            # Remove whitespace
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            products.append(line)

        return products

    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

def add_product(product_name: str) -> bool:
    """Add a single product by calling add_product.py"""
    try:
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
            return True
        else:
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout adding '{product_name}' (>2 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error adding '{product_name}': {e}")
        return False

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 add_products_batch.py <product_names_file> [--yes]")
        print("\nExample:")
        print("  python3 add_products_batch.py example_products.txt")
        print("  python3 add_products_batch.py example_products.txt --yes")
        sys.exit(1)

    filename = sys.argv[1]
    auto_confirm = len(sys.argv) > 2 and sys.argv[2] == "--yes"

    filename = sys.argv[1]
    auto_confirm = len(sys.argv) > 2 and sys.argv[2] == "--yes"

    # Read product names from file
    product_names = read_product_names(filename)

    if not product_names:
        print("❌ No valid product names found in file")
        print("💡 Make sure the file contains product names (one per line)")
        sys.exit(1)

    if not product_names:
        print(f"❌ No products found in {filename}")
        print("💡 Make sure the file contains product names (one per line)")
        sys.exit(1)

    total = len(product_names)
    batch_size = 2
    batches = (total + batch_size - 1) // batch_size
    pause_time = 2 * (batches - 1) if batches > 1 else 0
    estimated_time = total * 30 + pause_time
    print(f"\n📦 Found {total} products to add")
    print(f"📦 Processing in {batches} batches of {batch_size} products each")
    print(f"⏱️  Estimated time: ~{estimated_time} seconds ({estimated_time / 60:.1f} minutes)\n")

    print("Products to add:")
    for i, name in enumerate(product_names, 1):
        print(f"  {i}. {name}")

    # Confirm before proceeding (unless --yes flag is used)
    if not auto_confirm:
        response = input("\nContinue with batch addition? [y/N]: ")
        if response.lower() not in ['y', 'yes']:
            print("❌ Cancelled by user")
            sys.exit(0)
    else:
        print("✅ Auto-confirming batch addition (--yes flag used)")

    # Add each product in very small batches to avoid timeouts
    success_count = 0
    failed_products = []
    batch_size = 1  # Process one by one to maximize reliability

    for i in range(0, total, batch_size):
        batch = product_names[i:i+batch_size]
        print(f"\n--- Processing batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size} ---")

        for j, product_name in enumerate(batch, 1):
            batch_index = i + j
            print(f"\n{'='*60}")
            print(f"[{batch_index}/{total}] Adding: {product_name}")
            print(f"{'='*60}")

            if add_product(product_name):
                success_count += 1
                print(f"✅ Successfully added '{product_name}'")
            else:
                failed_products.append(product_name)
                print(f"❌ Failed to add '{product_name}'")

        # Longer delay between batches to avoid overwhelming the system
        if i + batch_size < total:
            print("⏳ Longer pause between batches (3 seconds)...")
            import time
            time.sleep(3)

    # Print summary
    print("\n" + "="*60)
    print("📊 BATCH ADDITION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {success_count}/{total}")
    print(f"❌ Failed: {len(failed_products)}/{total}")

    if failed_products:
        print("\n❌ Failed products:")
        for name in failed_products:
            print(f"   - {name}")
        print("\n💡 You can retry failed products manually:")
        for name in failed_products:
            print(f"   python3 add_product.py '{name}'")

    print("\n✨ Batch addition complete!")

if __name__ == '__main__':
    main()
