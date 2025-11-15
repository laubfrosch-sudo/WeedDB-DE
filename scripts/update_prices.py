#!/usr/bin/env python3
"""
Update prices for all products in the database.

This script queries all existing products from the database and
re-scrapes only their prices, preserving all other product data.

Usage:
    python3 update_prices.py
"""

import sqlite3
import asyncio
import sqlite3
import sys
import os
import re
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout, Page

# Setup basic logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('update_prices')

# Try to import enhanced modules
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from logger import get_logger as get_enhanced_logger
    from error_handler import get_error_handler, RetryConfig
    logger = get_enhanced_logger('update_prices')
    error_handler = get_error_handler()
except ImportError:
    # Fallback to basic logging
    error_handler = None
    RetryConfig = None

BASE_URL = "https://shop.dransay.com"

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'WeedDB.db')

def extract_product_id_from_url(url: str) -> Optional[int]:
    """Extract product ID from dransay URL"""
    match = re.search(r'/product/[^/]+/(\d+)', url)
    return int(match.group(1)) if match else None

def construct_search_url(product_name: str, vendor_id: str) -> str:
    """Constructs a search URL for dransay.com"""
    encoded_product_name = product_name.replace(' ', '%20')
    return f"{BASE_URL}/products?vendorId={vendor_id}&deliveryMethod=shipping&filters=%7B%22topProducersLowPrice%22:false%7D&search={encoded_product_name}"

async def scrape_price_for_product(page: Page, product_name: str, vendor_id: str) -> Optional[Dict[str, Any]]:
    """
    Scrape only the price and pharmacy for a specific product and category.
    Returns minimal data needed for price update.
    """
    try:
        # Step 1: Find product URL from search page
        search_url = construct_search_url(product_name, vendor_id)
        print(f"   🔍 Searching for '{product_name}' ({vendor_id})")

        await page.goto(search_url, wait_until='networkidle', timeout=30000)

        # Find product link
        try:
            await page.wait_for_selector('a[data-testid*="product-"]', timeout=30000)
        except:
            print(f"   ❌ No products found")
            return None

        product_links = await page.locator('a[data-testid*="product-"]').all()
        product_url = None

        for link in product_links:
            try:
                link_text = await link.inner_text()
                if product_name.lower() in link_text.lower():
                    href = await link.get_attribute('href')
                    if href:
                        product_url = f"{BASE_URL}{href}" if not href.startswith('http') else href
                        print(f"   ✅ Found product")
                        break
            except:
                continue

        if not product_url:
            print(f"   ❌ Product '{product_name}' not found")
            return None

        # Step 2: Navigate to product page with correct vendorId
        if '?' in product_url:
            full_product_url = f"{product_url}&vendorId={vendor_id}&deliveryMethod=shipping"
        else:
            full_product_url = f"{product_url}?vendorId={vendor_id}&deliveryMethod=shipping"

        print(f"   🌐 Loading product page ({vendor_id})")

        await page.goto(full_product_url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)

        # Extract only price and pharmacy using improved methods
        pharmacy_name = None
        price_per_g = None

        print(f"   🔍 Starting pharmacy/price extraction (improved)...")
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
                # NOTE: € comes BEFORE the number in German format
                price_match = re.search(r'€\s*(\d+[.,]\d+)\s*/\s*g', price_text)
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
                    'price_per_g': price_per_g,
                    'category': vendor_id
                }

        except Exception as e:
            print(f"   ⚠ Method 1 failed: {e}")

        # Method 2: Fallback - search for button elements with pharmacy and price
        if not (pharmacy_name and price_per_g):
            print(f"   📍 Method 2: Searching button elements...")
            try:
                buttons = await page.locator('button').all()
                for btn in buttons:
                    text = await btn.inner_text()

                    # Look for pharmacy in button
                    if 'Apotheke' in text and not pharmacy_name:
                        lines = text.split('\n')
                        for line in lines:
                            if 'Apotheke' in line:
                                pharmacy_name = line.strip()
                                print(f"   🏥 Found pharmacy in button: {pharmacy_name}")
                                break

                    # Look for price in button (handle German comma)
                    if '€' in text and '/g' in text.lower() and not price_per_g:
                        price_match = re.search(r'€\s*(\d+[.,]\d+)\s*/\s*g', text)
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
                        'price_per_g': price_per_g,
                        'category': vendor_id
                    }
            except Exception as e:
                print(f"   ⚠ Method 2 failed: {e}")

        # Method 3: Fallback - search all elements with €/g pattern
        if not (pharmacy_name and price_per_g):
            print(f"   📍 Method 3: Searching all elements with €/g...")
            try:
                # Search for €/g pattern (handle German comma)
                price_elements = await page.locator('text=/€.*\\/.*g/').all()
                print(f"   Found {len(price_elements)} elements with €/g pattern")

                if price_elements:
                    # Get first price element
                    first_price_elem = price_elements[0]
                    price_text = await first_price_elem.inner_text()

                    price_match = re.search(r'€\s*(\d+[.,]\d+)\s*/\s*g', price_text)
                    if price_match:
                        price_str = price_match.group(1).replace(',', '.')
                        price_per_g = float(price_str)
                        print(f"   💰 Found price: €{price_per_g}/g")

                # Look for pharmacy name separately
                if not pharmacy_name:
                    apotheke_elements = await page.locator('text=/Apotheke/').all()
                    for elem in apotheke_elements:
                        text = await elem.inner_text()
                        if 'Apotheke' in text and 8 < len(text.strip()) < 100:
                            pharmacy_name = text.strip()
                            print(f"   🏥 Found pharmacy: {pharmacy_name}")
                            break

                if pharmacy_name and price_per_g:
                    print(f"   ✅ Method 3 successful: {pharmacy_name} - €{price_per_g}/g")
                    return {
                        'pharmacy_name': pharmacy_name,
                        'price_per_g': price_per_g,
                        'category': vendor_id
                    }
            except Exception as e:
                print(f"   ⚠ Method 3 failed: {e}")

        if pharmacy_name and price_per_g:
            print(f"   💰 {pharmacy_name}: €{price_per_g}/g")
            return {
                'pharmacy_name': pharmacy_name,
                'price_per_g': price_per_g,
                'category': vendor_id
            }
        else:
            print(f"   ⚠ Could not extract pharmacy/price")
            return None

    except Exception as e:
        print(f"   ❌ Error scraping price: {e}")
        return None

def get_all_products() -> List[Tuple[int, str, str]]:
    """Fetch all products from database with their URLs"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, url FROM products ORDER BY name")
    products = cursor.fetchall()

    conn.close()
    return products

def update_product_price(product_id: int, pharmacy_name: str, price_per_g: float, category: str) -> bool:
    """Update price for a specific product"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Insert or get pharmacy
        cursor.execute("INSERT OR IGNORE INTO pharmacies (name) VALUES (?)", (pharmacy_name,))
        cursor.execute("SELECT id FROM pharmacies WHERE name = ?", (pharmacy_name,))
        pharmacy_result = cursor.fetchone()
        if pharmacy_result:
            pharmacy_id = pharmacy_result[0]

            # Insert new price entry
            cursor.execute("""
                INSERT INTO prices (product_id, pharmacy_id, price_per_g, category, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, pharmacy_id, price_per_g, category, datetime.now()))

            conn.commit()
            return True
        else:
            return False

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

async def update_product_prices(product_id: int, product_name: str) -> bool:
    """Update prices for a single product by scraping both categories"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        success_count = 0

        # Scrape for 'top' pharmacies
        print(f"\n=== Updating Top Pharmacies ===")
        top_data = await scrape_price_for_product(page, product_name, "top")
        if top_data:
            if update_product_price(product_id, top_data['pharmacy_name'], top_data['price_per_g'], top_data['category']):
                success_count += 1
                print(f"✅ Updated top price for '{product_name}'")
            else:
                print(f"❌ Failed to save top price for '{product_name}'")

        # Scrape for 'all' pharmacies
        print(f"\n=== Updating All Pharmacies ===")
        all_data = await scrape_price_for_product(page, product_name, "all")
        if all_data:
            if update_product_price(product_id, all_data['pharmacy_name'], all_data['price_per_g'], all_data['category']):
                success_count += 1
                print(f"✅ Updated all price for '{product_name}'")
            else:
                print(f"❌ Failed to save all price for '{product_name}'")

        await browser.close()
        return success_count > 0

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
    print(f"⏱️  Estimated time: ~{total * 15} seconds ({total * 0.25:.1f} minutes)\n")

    # Auto-confirm for automated execution
    print("🚀 Starting price update...")

    # Update each product
    success_count = 0
    failed_products = []

    for i, (product_id, product_name, product_url) in enumerate(products, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{total}] Updating: {product_name}")
        print(f"{'='*60}")

        try:
            if asyncio.run(update_product_prices(product_id, product_name)):
                success_count += 1
                print(f"✅ Successfully updated prices for '{product_name}'")
            else:
                failed_products.append(product_name)
                print(f"❌ Failed to update prices for '{product_name}'")
        except Exception as e:
            failed_products.append(product_name)
            print(f"❌ Error updating '{product_name}': {e}")

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
