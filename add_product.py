#!/usr/bin/env python3
"""
Add cannabis product to WeedDB from shop.dransay.com
Finds the cheapest price for a given product name in two categories:
1. Top shipping pharmacies (vendorId=top)
2. All shipping pharmacies (vendorId=all)
"""

import sys
import re
import sqlite3
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout, Page, Locator

BASE_URL = "https://shop.dransay.com"

def extract_product_id_from_url(url: str) -> Optional[int]:
    """Extract product ID from dransay URL"""
    match = re.search(r'/product/[^/]+/(\d+)', url)
    return int(match.group(1)) if match else None

def construct_search_url(product_name: str, vendor_id: str) -> str:
    """Constructs a search URL for dransay.com"""
    encoded_product_name = product_name.replace(' ', '%20')
    return f"{BASE_URL}/products?vendorId={vendor_id}&deliveryMethod=shipping&filters=%7B%22topProducersLowPrice%22:false%7D&search={encoded_product_name}"

async def _scrape_product_details_from_card(page: Page, product_card_locator: Locator, product_link_locator: Optional[Locator] = None) -> Dict[str, Any]:
    """Extracts product details from a given product card locator by parsing text content"""
    product_data: Dict[str, Any] = {}

    # Extract product URL and ID
    if product_link_locator:
        product_link = await product_link_locator.get_attribute('href')
    else:
        product_link = await product_card_locator.get_attribute('href')

    if product_link:
        product_data['url'] = f"{BASE_URL}{product_link}" if not product_link.startswith('http') else product_link
        product_data['id'] = extract_product_id_from_url(product_data['url'])
    else:
        raise ValueError("Could not find product URL on card.")

    # Get all text from the card and parse it
    try:
        all_text = await product_card_locator.inner_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]

        print(f"   Debug: Card has {len(lines)} lines of text")

        # Parse the structured text
        # Pattern: genetics, THC%, CBD%, Name, Variant, Rating, (Reviews), ...
        found_cbd = False
        for i, line in enumerate(lines):
            # Genetics (Indica/Sativa/Hybrid)
            if line in ['Indica', 'Sativa', 'Hybrid', 'Hybrid-Sativa', 'Hybrid-Indica']:
                product_data['genetics'] = line

            # THC percentage
            thc_match = re.match(r'THC\s+(\d+(?:\.\d+)?)%', line)
            if thc_match:
                product_data['thc_percent'] = float(thc_match.group(1))

            # CBD percentage
            cbd_match = re.match(r'CBD\s+(\d+(?:\.\d+)?)%', line)
            if cbd_match:
                product_data['cbd_percent'] = float(cbd_match.group(1))
                found_cbd = True
                # Name comes right after CBD
                if i + 1 < len(lines):
                    product_data['name'] = lines[i + 1]
                # Variant comes after name
                if i + 2 < len(lines):
                    product_data['variant'] = lines[i + 2]

            # Rating (decimal number like 4.0)
            rating_match = re.match(r'^(\d+\.\d+)$', line)
            if rating_match and 'rating' not in product_data:
                product_data['rating'] = float(rating_match.group(1))

            # Review count (pattern like "(1832+)")
            review_match = re.match(r'\((\d+)\+?\)', line)
            if review_match:
                product_data['review_count'] = int(review_match.group(1))

        # If name not found, use fallback
        if 'name' not in product_data and len(lines) > 3:
            # Usually: genetics, THC%, CBD%, name, variant...
            for line in lines[3:]:
                if not re.search(r'\d+%|\(\d+\+?\)|^\d+\.\d+$|€', line) and len(line) > 2:
                    product_data['name'] = line
                    break

        # Producer name often appears in variant (e.g., "Pedanios 29/1 SRD-CA")
        if product_data.get('variant'):
            variant_parts = product_data['variant'].split()
            if variant_parts:
                product_data['producer_name'] = variant_parts[0]

    except Exception as e:
        print(f"   ⚠ Error parsing card text: {e}")
        product_data['name'] = None
        product_data['variant'] = None
        product_data['thc_percent'] = None
        product_data['cbd_percent'] = None
        product_data['genetics'] = None
        product_data['rating'] = None
        product_data['review_count'] = None
        product_data['producer_name'] = None

    return product_data

async def _scrape_cheapest_price_from_search_page(page: Page, product_name: str, vendor_id: str) -> Optional[Dict[str, Any]]:
    """
    Finds the product URL from search, then navigates to product page with vendorId
    to extract the cheapest pharmacy and price for that category.
    """
    # Step 1: Find product URL from search page
    search_url = construct_search_url(product_name, vendor_id)
    print(f"🔍 Searching for '{product_name}' ({vendor_id})")

    await page.goto(search_url, wait_until='networkidle', timeout=30000)

    # Find product link
    try:
        await page.wait_for_selector('a[href*="/product/"]', timeout=30000)
    except:
        print(f"   ❌ No products found")
        return None

    product_links = await page.locator('a[href*="/product/"]').all()
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
    # Add vendorId and deliveryMethod to URL
    if '?' in product_url:
        full_product_url = f"{product_url}&vendorId={vendor_id}&deliveryMethod=shipping"
    else:
        full_product_url = f"{product_url}?vendorId={vendor_id}&deliveryMethod=shipping"

    print(f"   🌐 Loading product page ({vendor_id})")
    await page.goto(full_product_url, wait_until='networkidle', timeout=30000)
    await page.wait_for_timeout(2000)

    # Step 3: Extract product details and cheapest pharmacy
    product_details: Dict[str, Any] = {}

    # Extract product ID from URL
    product_details['id'] = extract_product_id_from_url(product_url)
    product_details['url'] = product_url
    product_details['category'] = vendor_id

    # Extract product info from page
    try:
        page_content = await page.content()

        # Extract detailed product information
        try:
            # Product name
            title_elem = page.locator('h1').first
            product_details['name'] = await title_elem.inner_text()
        except:
            product_details['name'] = product_name.title()

        # Extract product details from the page
        # Look for THC/CBD percentages
        try:
            thc_elements = await page.locator(r'text=/THC\s+\d+\.?\d*%/').all()
            for elem in thc_elements:
                thc_text = await elem.inner_text()
                thc_match = re.search(r'THC\s+(\d+(?:\.\d+)?)%', thc_text)
                if thc_match:
                    product_details['thc_percent'] = float(thc_match.group(1))
                    break
        except:
            pass

        try:
            cbd_elements = await page.locator(r'text=/CBD\s+\d+\.?\d*%/').all()
            for elem in cbd_elements:
                cbd_text = await elem.inner_text()
                cbd_match = re.search(r'CBD\s+(\d+(?:\.\d+)?)%', cbd_text)
                if cbd_match:
                    product_details['cbd_percent'] = float(cbd_match.group(1))
                    break
        except:
            pass

        # Extract genetics
        try:
            genetics_elements = await page.locator(r'text=/^(Indica|Sativa|Hybrid|Hybrid-Sativa|Hybrid-Indica)$/').all()
            for elem in genetics_elements:
                genetics_text = await elem.inner_text()
                if genetics_text in ['Indica', 'Sativa', 'Hybrid', 'Hybrid-Sativa', 'Hybrid-Indica']:
                    product_details['genetics'] = genetics_text
                    break
        except:
            pass

        # Extract rating and review count
        try:
            # Look for rating patterns like "4.2 (183+)"
            rating_elements = await page.locator(r'text=/\d+\.\d+\s*\(\d+\+?\)/').all()
            for elem in rating_elements:
                rating_text = await elem.inner_text()
                rating_match = re.search(r'(\d+\.\d+)\s*\((\d+)\+?\)', rating_text)
                if rating_match:
                    product_details['rating'] = float(rating_match.group(1))
                    product_details['review_count'] = int(rating_match.group(2))
                    break
        except:
            pass

        # Extract producer/variant info
        try:
            # Look for variant information in product details
            variant_elements = await page.locator('[class*="variant"], [class*="producer"], [data-testid*="variant"]').all()
            for elem in variant_elements:
                variant_text = await elem.inner_text()
                if '/' in variant_text and any(char.isdigit() for char in variant_text):
                    product_details['variant'] = variant_text
                    # Extract producer name (usually first word)
                    producer_name = variant_text.split()[0]
                    if len(producer_name) > 2:
                        product_details['producer_name'] = producer_name
                    break
        except:
            pass

        # Find pharmacy name and price
        # Look for elements containing "Apotheke"
        apotheke_elements = await page.locator('text=/Apotheke/').all()

        pharmacy_name = None
        price_per_g = None

        for elem in apotheke_elements:
            try:
                elem_text = await elem.inner_text()
                parent = elem.locator('..')
                parent_text = await parent.inner_text()

                # Extract pharmacy name
                pharmacy_match = re.search(r'([^\n]+Apotheke[^\n]*)', elem_text)
                if pharmacy_match:
                    pharmacy_name = pharmacy_match.group(1).strip()

                # Extract price from parent
                price_match = re.search(r'€\s*(\d+\.\d+)\s*/\s*g', parent_text)
                if price_match:
                    price_per_g = float(price_match.group(1))

                if pharmacy_name and price_per_g:
                    break

            except:
                continue

        product_details['cheapest_pharmacy_name'] = pharmacy_name
        product_details['cheapest_price_per_g'] = price_per_g

        if pharmacy_name and price_per_g:
            print(f"   💰 {pharmacy_name}: €{price_per_g}/g")
        else:
            print(f"   ⚠ Could not extract pharmacy/price")

    except Exception as e:
        print(f"   ⚠ Error extracting details: {e}")
        product_details['cheapest_pharmacy_name'] = None
        product_details['cheapest_price_per_g'] = None

    return product_details

async def scrape_product_data(product_name: str) -> Optional[Dict[str, Any]]:
    """
    Scrapes product data and the cheapest prices for 'top' and 'all' categories.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        product_data: Dict[str, Any] = {}

        # Scrape for 'top' pharmacies
        print(f"\n=== Scraping Top Pharmacies ===")
        top_data = await _scrape_cheapest_price_from_search_page(page, product_name, "top")
        if top_data:
            product_data.update(top_data)
            product_data['cheapest_top_pharmacy_name'] = top_data['cheapest_pharmacy_name']
            product_data['cheapest_top_price_per_g'] = top_data['cheapest_price_per_g']
        else:
            print(f"❌ Failed to get 'top' pharmacy data for {product_name}")
            await browser.close()
            return None

        # Scrape for 'all' pharmacies
        print(f"\n=== Scraping All Pharmacies ===")
        all_data = await _scrape_cheapest_price_from_search_page(page, product_name, "all")
        if all_data:
            # Update product details only if they are missing from 'top_data'
            for key, value in all_data.items():
                if key not in product_data and key not in ['cheapest_pharmacy_name', 'cheapest_price_per_g', 'category']:
                    product_data[key] = value

            product_data['cheapest_all_pharmacy_name'] = all_data['cheapest_pharmacy_name']
            product_data['cheapest_all_price_per_g'] = all_data['cheapest_price_per_g']
        else:
            print(f"❌ Failed to get 'all' pharmacy data for {product_name}")
            await browser.close()
            return None

        await browser.close()

        # Display extracted data
        print(f"\n{'='*60}")
        print(f"📋 Summary for: {product_data.get('name', product_name)}")
        print(f"{'='*60}")
        print(f"   ID: {product_data.get('id', 'N/A')}")
        print(f"   URL: {product_data.get('url', 'N/A')}")
        print(f"\n💰 Cheapest Prices:")
        print(f"   🏆 Top Pharmacies: €{product_data.get('cheapest_top_price_per_g', 'N/A')}/g")
        print(f"       → {product_data.get('cheapest_top_pharmacy_name', 'N/A')}")
        print(f"   🌍 All Pharmacies: €{product_data.get('cheapest_all_price_per_g', 'N/A')}/g")
        print(f"       → {product_data.get('cheapest_all_pharmacy_name', 'N/A')}")
        print(f"{'='*60}\n")

        return product_data

def insert_product_to_db(product_data: Optional[Dict[str, Any]]) -> bool:
    """Insert product data into WeedDB"""

    if not product_data:
        print("❌ No product data to insert")
        return False

    conn = sqlite3.connect('WeedDB.db')
    cursor = conn.cursor()

    try:
        # Insert or get producer
        producer_id = None
        final_producer_name = product_data.get('producer_name')
        if final_producer_name:
            cursor.execute("INSERT OR IGNORE INTO producers (name) VALUES (?)",
                          (final_producer_name,))
            cursor.execute("SELECT id FROM producers WHERE name = ?", (final_producer_name,))
            result = cursor.fetchone()
            producer_id = result[0] if result else None

        # Insert product
        cursor.execute("""
            INSERT OR REPLACE INTO products
            (id, name, variant, genetics, thc_percent, cbd_percent, producer_id,
             rating, review_count, url, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_data['id'],
            product_data['name'],
            product_data.get('variant'),
            product_data.get('genetics'),
            product_data.get('thc_percent'),
            product_data.get('cbd_percent'),
            producer_id,
            product_data.get('rating'),
            product_data.get('review_count'),
            product_data['url'],
            datetime.now()
        ))

        # Insert cheapest 'top' pharmacy price
        if product_data.get('cheapest_top_pharmacy_name') and product_data.get('cheapest_top_price_per_g'):
            pharmacy_name = product_data['cheapest_top_pharmacy_name']
            price_per_g = product_data['cheapest_top_price_per_g']
            category = "top"

            cursor.execute("INSERT OR IGNORE INTO pharmacies (name) VALUES (?)", (pharmacy_name,))
            cursor.execute("SELECT id FROM pharmacies WHERE name = ?", (pharmacy_name,))
            pharmacy_result = cursor.fetchone()
            if pharmacy_result:
                pharmacy_id = pharmacy_result[0]
                cursor.execute("""
                    INSERT INTO prices (product_id, pharmacy_id, price_per_g, category, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_data['id'], pharmacy_id, price_per_g, category, datetime.now()))

        # Insert cheapest 'all' pharmacy price
        if product_data.get('cheapest_all_pharmacy_name') and product_data.get('cheapest_all_price_per_g'):
            pharmacy_name = product_data['cheapest_all_pharmacy_name']
            price_per_g = product_data['cheapest_all_price_per_g']
            category = "all"

            cursor.execute("INSERT OR IGNORE INTO pharmacies (name) VALUES (?)", (pharmacy_name,))
            cursor.execute("SELECT id FROM pharmacies WHERE name = ?", (pharmacy_name,))
            pharmacy_result = cursor.fetchone()
            if pharmacy_result:
                pharmacy_id = pharmacy_result[0]
                cursor.execute("""
                    INSERT INTO prices (product_id, pharmacy_id, price_per_g, category, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_data['id'], pharmacy_id, price_per_g, category, datetime.now()))

        conn.commit()
        print(f"\n✅ Successfully added '{product_data['name']}' to database with cheapest prices.")
        return True

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        conn.close()
        return False

async def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python add_product.py <product_name>")
        print("\nExample:")
        print("  python add_product.py 'sourdough'")
        sys.exit(1)

    product_name = sys.argv[1]

    # Scrape product data
    product_data = await scrape_product_data(product_name)

    if not product_data:
        print("\n❌ Failed to scrape product data")
        sys.exit(1)

    # Insert into database
    success = insert_product_to_db(product_data)

    if not success:
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())