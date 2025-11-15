"""
Scrape all available product names from shop.dransay.com product listing pages.

This script extracts all product names from the main product listing pages
to get a comprehensive list of available strains for adding to the database.

Usage:
    python3 scripts/scrape_product_list.py [--flowers-only]
"""

import asyncio
import json
from typing import List, Set
from playwright.async_api import async_playwright, Page


async def scrape_product_names(url: str) -> Set[str]:
    """Scrape product names from a product listing page (first page only)"""
    product_names = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"🌐 Loading product listing page: {url}")
        await page.goto(url, wait_until='networkidle', timeout=30000)

        # Wait for products to load
        await page.wait_for_timeout(5000)

        # Extract product names from the first page
        product_elements = await page.locator('[data-testid*="product-"]').all()

        print(f"📦 Found {len(product_elements)} product elements")

        for elem in product_elements:
            try:
                name = await elem.inner_text()
                # Filter for clean product names (not UI elements or long descriptions)
                if (name and
                    len(name.strip()) > 2 and
                    len(name.strip()) < 50 and  # Not too long
                    not any(skip in name.lower() for skip in ['category', 'slide', 'from €', 'thc', 'cbd', 'hybrid', 'indica', 'sativa']) and
                    not name.strip().startswith('€') and
                    not name.strip().endswith('%') and
                    not '(' in name):  # Avoid entries with ratings like (202+)
                    product_names.add(name.strip())
            except:
                continue

        await browser.close()

    return product_names


async def main():
    """Main function to scrape product names from different pages"""

    # URLs to scrape - focus on flowers category
    urls = [
        "https://shop.dransay.com/products?vendorId=all&deliveryMethod=shipping&filters={%22topProducersLowPrice%22:false,%22category%22:[1]}"
    ]

    all_product_names = set()

    for i, url in enumerate(urls, 1):
        print(f"\n🔍 Scraping page {i}/{len(urls)}: Flowers category")
        try:
            product_names = await scrape_product_names(url)
            all_product_names.update(product_names)
            print(f"✅ Found {len(product_names)} products on this page")
        except Exception as e:
            print(f"❌ Error scraping page {i}: {e}")

    # Remove duplicates and sort
    unique_names = sorted(list(all_product_names))

    print(f"\n📊 Total unique product names found: {len(unique_names)}")

    # Save to file
    with open('available_products.json', 'w', encoding='utf-8') as f:
        json.dump(unique_names, f, ensure_ascii=False, indent=2)

    print("💾 Saved product names to 'available_products.json'")

    # Print first 20 examples
    print("\n📝 First 20 product names:")
    for name in unique_names[:20]:
        print(f"  - {name}")


if __name__ == "__main__":
    asyncio.run(main())