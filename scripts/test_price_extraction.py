#!/usr/bin/env python3
"""
Test price extraction methods on a known product.
"""

import asyncio
import re
from playwright.async_api import async_playwright

BASE_URL = "https://shop.dransay.com"

async def test_price_extraction():
    """Test different price extraction methods on a known product"""

    # Use a known product - Sourdough (ID: 973)
    product_url = "https://shop.dransay.com/product/p/973?vendorId=all&deliveryMethod=shipping"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=False to see what's happening
        page = await browser.new_page()

        print(f"🌐 Loading product page...")
        await page.goto(product_url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)  # Extra wait for dynamic content

        print("\n" + "="*60)
        print("Testing Different Price Extraction Methods")
        print("="*60 + "\n")

        # Method 1: Look for "Buying from" text
        print("📍 Method 1: 'Buying from' text search")
        try:
            buying_elements = await page.locator('text=/Buying from/').all()
            print(f"   Found {len(buying_elements)} 'Buying from' elements")
            for i, elem in enumerate(buying_elements):
                text = await elem.inner_text()
                print(f"   Element {i+1}: {text[:100]}...")

                price_match = re.search(r'€(\d+\.\d+)\s*/\s*g', text)
                if price_match:
                    print(f"   ✅ Found price: €{price_match.group(1)}/g")

                pharmacy_match = re.search(r'([^\n]*Apotheke[^\n]*)', text)
                if pharmacy_match:
                    print(f"   ✅ Found pharmacy: {pharmacy_match.group(1)}")
        except Exception as e:
            print(f"   ❌ Method 1 failed: {e}")

        # Method 2: Look for elements containing €/g pattern
        print("\n📍 Method 2: Elements with €/g pattern")
        try:
            price_elements = await page.locator('text=/€.*\\/.*g/').all()
            print(f"   Found {len(price_elements)} elements with €/g")
            for i, elem in enumerate(price_elements[:5]):  # Show first 5
                text = await elem.inner_text()
                print(f"   Element {i+1}: {text}")
        except Exception as e:
            print(f"   ❌ Method 2 failed: {e}")

        # Method 3: Look for button elements (buying buttons)
        print("\n📍 Method 3: Button elements")
        try:
            buttons = await page.locator('button').all()
            print(f"   Found {len(buttons)} button elements")
            for i, btn in enumerate(buttons):
                text = await btn.inner_text()
                if '€' in text or 'Buy' in text or 'Kaufen' in text:
                    print(f"   Button {i+1}: {text[:100]}")
        except Exception as e:
            print(f"   ❌ Method 3 failed: {e}")

        # Method 4: Search body text for all prices
        print("\n📍 Method 4: Body text search for all prices")
        try:
            body_text = await page.locator('body').inner_text()
            price_matches = list(re.finditer(r'€\s*(\d+\.\d+)\s*/\s*g', body_text))
            print(f"   Found {len(price_matches)} price patterns in body text")

            for i, match in enumerate(price_matches[:5]):  # Show first 5
                price = match.group(1)
                # Get context around the price
                start = max(0, match.start() - 50)
                end = min(len(body_text), match.end() + 50)
                context = body_text[start:end].replace('\n', ' ')
                print(f"   Price {i+1}: €{price}/g | Context: ...{context}...")
        except Exception as e:
            print(f"   ❌ Method 4 failed: {e}")

        # Method 5: Look for specific data-testid patterns
        print("\n📍 Method 5: Data-testid patterns")
        try:
            testid_elements = await page.locator('[data-testid]').all()
            print(f"   Found {len(testid_elements)} elements with data-testid")

            # Show relevant testid elements
            for elem in testid_elements[:20]:
                testid = await elem.get_attribute('data-testid')
                if any(keyword in testid.lower() for keyword in ['buy', 'price', 'pharmacy', 'vendor', 'cart']):
                    text = await elem.inner_text()
                    print(f"   testid='{testid}': {text[:80]}")
        except Exception as e:
            print(f"   ❌ Method 5 failed: {e}")

        print("\n" + "="*60)
        print("Test Complete - Browser will close in 10 seconds...")
        print("="*60)
        await page.wait_for_timeout(10000)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_price_extraction())
