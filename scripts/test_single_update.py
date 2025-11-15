#!/usr/bin/env python3
"""Quick test of price update for a single product"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from update_prices import update_product_prices

async def main():
    product_id = 1152  # Blue Dream
    product_name = "Blue Dream"

    print(f"Testing price update for: {product_name}")
    print("="*60)

    success = await update_product_prices(product_id, product_name)

    if success:
        print("\n✅ SUCCESS: Price extraction worked!")
    else:
        print("\n❌ FAILED: Price extraction failed")

    return success

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
