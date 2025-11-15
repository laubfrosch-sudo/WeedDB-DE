#!/usr/bin/env python3
"""
Improved price extraction function based on actual website structure.

Key findings:
1. Website uses German decimal notation: 5,69 € (not 5.69 €)
2. "Buying from" text does NOT exist on German site
3. Use data-testid attributes for reliable extraction
4. data-testid='product-price': Contains price
5. data-testid='vendor-selection-trigger-text': Contains pharmacy name
"""

import re
from typing import Optional, Dict, Any
from playwright.async_api import Page


async def extract_pharmacy_and_price(page: Page) -> Optional[Dict[str, Any]]:
    """
    Extract pharmacy name and price using reliable data-testid attributes.

    Args:
        page: Playwright page object on product page

    Returns:
        Dict with 'pharmacy_name' and 'price_per_g' or None if extraction fails
    """
    pharmacy_name = None
    price_per_g = None

    print(f"   🔍 Starting pharmacy/price extraction (improved method)...")

    try:
        # Method 1: Use data-testid attributes (most reliable)
        print(f"   📍 Method 1: Using data-testid attributes...")
        try:
            # Get pharmacy name
            pharmacy_elem = page.locator('[data-testid="vendor-selection-trigger-text"]').first
            pharmacy_name = await pharmacy_elem.inner_text()
            print(f"   🏥 Found pharmacy: {pharmacy_name}")
        except Exception as e:
            print(f"   ⚠ Could not find pharmacy via testid: {e}")

        try:
            # Get price - note: German decimal uses comma!
            price_elem = page.locator('[data-testid="product-price"]').first
            price_text = await price_elem.inner_text()
            print(f"   📄 Price text: {price_text}")

            # Extract price - handle BOTH comma and dot decimal separators
            # Pattern: digits, comma OR dot, digits, €, /, g
            price_match = re.search(r'(\d+[.,]\d+)\s*€\s*/\s*g', price_text)
            if price_match:
                price_str = price_match.group(1).replace(',', '.')  # Convert German comma to dot
                price_per_g = float(price_str)
                print(f"   💰 Found price: €{price_per_g}/g")
        except Exception as e:
            print(f"   ⚠ Could not find price via testid: {e}")

        # If Method 1 succeeded, return result
        if pharmacy_name and price_per_g:
            print(f"   ✅ Method 1 successful: {pharmacy_name} - €{price_per_g}/g")
            return {
                'pharmacy_name': pharmacy_name,
                'price_per_g': price_per_g
            }

        # Method 2: Fallback - search for button elements with pharmacy and price
        print(f"   📍 Method 2: Searching button elements...")
        try:
            buttons = await page.locator('button').all()
            for btn in buttons:
                text = await btn.inner_text()

                # Look for pharmacy in button
                if 'Apotheke' in text and not pharmacy_name:
                    # Extract pharmacy name from text
                    lines = text.split('\n')
                    for line in lines:
                        if 'Apotheke' in line:
                            pharmacy_name = line.strip()
                            print(f"   🏥 Found pharmacy in button: {pharmacy_name}")
                            break

                # Look for price in button (handle German comma)
                if '€' in text and '/g' in text.lower() and not price_per_g:
                    price_match = re.search(r'(\d+[.,]\d+)\s*€\s*/\s*g', text)
                    if price_match:
                        price_str = price_match.group(1).replace(',', '.')
                        price_per_g = float(price_str)
                        print(f"   💰 Found price in button: €{price_per_g}/g")

                if pharmacy_name and price_per_g:
                    break

            if pharmacy_name and price_per_g:
                print(f"   ✅ Method 2 successful: {pharmacy_name} - €{price_per_g}/g")
                return {
                    'pharmacy_name': pharmacy_name,
                    'price_per_g': price_per_g
                }
        except Exception as e:
            print(f"   ⚠ Method 2 failed: {e}")

        # Method 3: Fallback - search all elements with €/g pattern
        print(f"   📍 Method 3: Searching all elements with €/g...")
        try:
            # Search for €/g pattern (handle German comma)
            price_elements = await page.locator('text=/€.*\\/.*g/').all()
            print(f"   Found {len(price_elements)} elements with €/g pattern")

            if price_elements:
                # Get first price element
                first_price_elem = price_elements[0]
                price_text = await first_price_elem.inner_text()

                price_match = re.search(r'(\d+[.,]\d+)\s*€\s*/\s*g', price_text)
                if price_match:
                    price_str = price_match.group(1).replace(',', '.')
                    price_per_g = float(price_str)
                    print(f"   💰 Found price: €{price_per_g}/g")

            # Look for pharmacy name separately
            if not pharmacy_name:
                apotheke_elements = await page.locator('text=/Apotheke/').all()
                for elem in apotheke_elements:
                    text = await elem.inner_text()
                    if 'Apotheke' in text and len(text.strip()) > 8 and len(text.strip()) < 100:
                        pharmacy_name = text.strip()
                        print(f"   🏥 Found pharmacy: {pharmacy_name}")
                        break

            if pharmacy_name and price_per_g:
                print(f"   ✅ Method 3 successful: {pharmacy_name} - €{price_per_g}/g")
                return {
                    'pharmacy_name': pharmacy_name,
                    'price_per_g': price_per_g
                }
        except Exception as e:
            print(f"   ⚠ Method 3 failed: {e}")

    except Exception as e:
        print(f"   ❌ Error during pharmacy/price extraction: {e}")

    if pharmacy_name and price_per_g:
        print(f"   💰 Result: {pharmacy_name} - €{price_per_g}/g")
        return {
            'pharmacy_name': pharmacy_name,
            'price_per_g': price_per_g
        }
    else:
        print(f"   ⚠ Could not extract pharmacy/price")
        return None
