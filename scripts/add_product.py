#!/usr/bin/env python3
"""
Add cannabis product to WeedDB from shop.dransay.com

This script scrapes product details and the cheapest prices for a given product name
in two categories:
1. Top shipping pharmacies (vendorId=top)
2. All shipping pharmacies (vendorId=all)

Before adding, it checks if the product already exists in the database.
If it exists, it updates the product details and prices; otherwise, it adds a new product.

💡 It is recommended to use 'find_new_products.py' first to identify truly new products
before using this script to add them.
"""

import json
import sys
import re
import sqlite3
import os
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
    """Extracts product details from a given product link by parsing text content"""
    product_data: Dict[str, Any] = {}

    # Use the product link locator (which is now the main element containing all info)
    if product_link_locator:
        link_element = product_link_locator
    else:
        link_element = product_card_locator

    # Extract product URL and ID
    product_link = await link_element.get_attribute('href')
    if product_link:
        product_data['url'] = f"{BASE_URL}{product_link}" if not product_link.startswith('http') else product_link
        product_data['id'] = extract_product_id_from_url(product_data['url'])
    else:
        raise ValueError("Could not find product URL on link.")

    # Get all text from the link element and parse it
    try:
        all_text = await link_element.inner_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]

        print(f"   Debug: Link has {len(lines)} lines of text")

        # Parse the structured text - the new format is different
        # Pattern seems to be: Genetics, THC%, CBD%, Name, Variant, Rating, Reviews, Effects, Terpenes, Price
        for i, line in enumerate(lines):
            print(f"   Debug line {i}: '{line}'")

            # Genetics (Indica/Sativa/Hybrid) - more flexible matching
            if line in ['Indica', 'Sativa', 'Hybrid', 'Hybrid-Sativa', 'Hybrid-Indica']:
                product_data['genetics'] = line
                print(f"   ✅ Found genetics: {line}")

            # THC percentage - more flexible pattern
            thc_match = re.search(r'THC\s*(\d+(?:\.\d+)?)%', line)
            if thc_match:
                product_data['thc_percent'] = float(thc_match.group(1))
                print(f"   ✅ Found THC: {thc_match.group(1)}%")

            # CBD percentage - more flexible pattern
            cbd_match = re.search(r'CBD\s*(\d+(?:\.\d+)?)%', line)
            if cbd_match:
                product_data['cbd_percent'] = float(cbd_match.group(1))
                print(f"   ✅ Found CBD: {cbd_match.group(1)}%")

            # Rating (decimal number like 4.0)
            rating_match = re.match(r'^(\d+\.\d+)$', line)
            if rating_match and 'rating' not in product_data:
                product_data['rating'] = float(rating_match.group(1))
                print(f"   ✅ Found rating: {rating_match.group(1)}")

            # Review count (pattern like "(1832+)")
            review_match = re.match(r'\((\d+)\+?\)', line)
            if review_match:
                product_data['review_count'] = int(review_match.group(1))
                print(f"   ✅ Found review count: {review_match.group(1)}")

            # Price pattern
            price_match = re.search(r'from €(\d+\.\d+)', line)
            if price_match:
                product_data['price_per_g'] = float(price_match.group(1))
                print(f"   ✅ Found price: €{price_match.group(1)}/g")

        # Extract name and variant - they appear in sequence after CBD
        # Look for lines that don't match other patterns
        name_candidates = []
        for line in lines:
            if (not re.search(r'THC\s*\d+%|CBD\s*\d+%|^\d+\.\d+$|\(\d+\)|\d+%|from €|Indica|Sativa|Hybrid', line)
                and len(line) > 2 and line not in ['Inflammations', 'Limonen']):  # Skip known non-name lines
                name_candidates.append(line)

        if len(name_candidates) >= 1:
            product_data['name'] = name_candidates[0]
            print(f"   ✅ Found name: {name_candidates[0]}")

        if len(name_candidates) >= 2:
            product_data['variant'] = name_candidates[1]
            print(f"   ✅ Found variant: {name_candidates[1]}")

            # Producer name often appears in variant (e.g., "Pedanios 29/1 SRD-CA")
            variant_parts = name_candidates[1].split()
            if variant_parts:
                potential_producer = variant_parts[0]
                # Only set as producer if it looks like a brand name (not just numbers/codes)
                if len(potential_producer) > 2 and not potential_producer.replace('/', '').replace('-', '').isdigit():
                    product_data['producer_name'] = potential_producer
                    print(f"   ✅ Found producer: {potential_producer}")
                else:
                    print(f"   ⚠ Skipping potential producer: {potential_producer} (looks like code)")

    except Exception as e:
        print(f"   ⚠ Error parsing link text: {e}")
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
    # Add vendorId and deliveryMethod to URL
    if '?' in product_url:
        full_product_url = f"{product_url}&vendorId={vendor_id}&deliveryMethod=shipping"
    else:
        full_product_url = f"{product_url}?vendorId={vendor_id}&deliveryMethod=shipping"

    print(f"   🌐 Loading product page ({vendor_id})")
    
    await page.goto(full_product_url, wait_until='networkidle', timeout=30000)

    # Wait for dynamic content to load - look for price elements or buying section
    try:
        await page.wait_for_selector('[data-testid*="price"]', timeout=15000)
        print(f"   ⏳ Price elements found, waiting for full load...")
        await page.wait_for_timeout(5000)  # Additional wait for dynamic content
    except:
        print(f"   ⚠ No price elements found within timeout, proceeding anyway")
        await page.wait_for_timeout(8000)  # Longer wait as fallback

    # Step 3: Extract product details and cheapest pharmacy
    product_details: Dict[str, Any] = {}

    # Extract product ID from URL
    product_details['id'] = extract_product_id_from_url(product_url)
    product_details['url'] = product_url
    product_details['category'] = vendor_id

    # Extract product info from page with better selectors
    try:
        # Extract product info from page - updated selectors based on current site structure
        try:
            # Get full body text once for all extractions
            body_text = await page.locator('body').inner_text()

            # Product name from h1
            title_elem = page.locator('h1').first
            product_details['name'] = await title_elem.inner_text()
            print(f"   ✅ Product name: {product_details['name']}")
        except Exception as e:
            print(f"   ⚠ Could not extract product name: {e}")
            product_details['name'] = product_name.title()
            body_text = ""  # Initialize to avoid unbound variable

        # Extract genetics from text (indica/sativa/hybrid)
        try:
            if body_text and 'indica' in body_text.lower():
                product_details['genetics'] = 'Indica'
            elif body_text and 'sativa' in body_text.lower():
                product_details['genetics'] = 'Sativa'
            elif body_text and 'hybrid' in body_text.lower():
                # Check for hybrid subtypes
                if 'hybrid-indica' in body_text.lower():
                    product_details['genetics'] = 'Hybrid-Indica'
                elif 'hybrid-sativa' in body_text.lower():
                    product_details['genetics'] = 'Hybrid-Sativa'
                else:
                    product_details['genetics'] = 'Hybrid'
            if 'genetics' in product_details:
                print(f"   ✅ Found genetics: {product_details['genetics']}")
        except Exception as e:
            print(f"   ⚠ Could not extract genetics: {e}")

        # Extract THC and CBD percentages
        try:
            if body_text:
                thc_match = re.search(r'THC\s+(\d+(?:\.\d+)?)%', body_text)
                if thc_match:
                    product_details['thc_percent'] = float(thc_match.group(1))
                    print(f"   ✅ Found THC: {product_details['thc_percent']}%")
        except Exception as e:
            print(f"   ⚠ Could not extract THC: {e}")

        try:
            if body_text:
                cbd_match = re.search(r'CBD\s+(\d+(?:\.\d+)?)%', body_text)
                if cbd_match:
                    product_details['cbd_percent'] = float(cbd_match.group(1))
                    print(f"   ✅ Found CBD: {product_details['cbd_percent']}%")
        except Exception as e:
            print(f"   ⚠ Could not extract CBD: {e}")

        # Extract rating and review count
        try:
            if body_text:
                rating_match = re.search(r'(\d+\.\d+)\s*\((\d+)\+?\)', body_text)
                if rating_match:
                    product_details['rating'] = float(rating_match.group(1))
                    product_details['review_count'] = int(rating_match.group(2))
                    print(f"   ✅ Found rating: {product_details['rating']} ({product_details['review_count']} reviews)")
        except Exception as e:
            print(f"   ⚠ Could not extract rating/reviews: {e}")

        # Extract producer name
        try:
            if body_text:
                # Look for producer link or text - improved pattern
                producer_match = re.search(r'Producer\[([^\]]+)\]', body_text)
                if producer_match:
                    product_details['producer_name'] = producer_match.group(1).strip()
                    print(f"   ✅ Found producer via regex: {product_details['producer_name']}")
                else:
                    # Fallback: look for specific producer patterns that appear near product info
                    # Extract text around "Country" to find producer context
                    country_pos = body_text.find('Country')
                    if country_pos != -1:
                        # Look in the area around country for producer info
                        start_pos = max(0, country_pos - 200)
                        end_pos = min(len(body_text), country_pos + 200)
                        context = body_text[start_pos:end_pos]

                        # Look for producer patterns in this context
                        producer_patterns = [
                            r'Cantourage',
                            r'Aurora Cannabis',
                            r'Pedanios',
                            r'Cannamedical',
                            r'ZOIKS',
                            r'IMC',
                            r'Enua',
                            r'Amici',
                            r'Bathera',
                            r'420 Natural',
                            r'THC Akut',
                            r'Remexian',
                            r'Avaay',
                            r'Buuo',
                            r'Demecan',
                            r'LUANA',
                            r'Tyson',
                            r'Slouu',
                            r'Barongo',
                            r'Tannenbusch',
                            r'aleph amber',
                            r'All Nations',
                            r'enua Pharma'
                        ]
                        for pattern in producer_patterns:
                            if pattern in context:
                                product_details['producer_name'] = pattern
                                print(f"   ✅ Found producer in context: {product_details['producer_name']}")
                                break

                    # If still not found, try broader search but be more careful
                    if 'producer_name' not in product_details:
                        for pattern in ['Cantourage', 'Aurora Cannabis', 'Pedanios', 'Cannamedical', 'ZOIKS']:
                            if pattern in body_text:
                                # Make sure it's not in recommended products section
                                pattern_pos = body_text.find(pattern)
                                if pattern_pos < body_text.find('Recommended') or body_text.find('Recommended') == -1:
                                    product_details['producer_name'] = pattern
                                    print(f"   ✅ Found producer via search: {product_details['producer_name']}")
                                    break

                if 'producer_name' in product_details:
                    print(f"   ✅ Producer confirmed: {product_details['producer_name']}")
        except Exception as e:
            print(f"   ⚠ Could not extract producer: {e}")

        # Extract country
        try:
            if body_text:
                country_match = re.search(r'Country\s+([^\n]+)', body_text)
                if country_match:
                    product_details['country'] = country_match.group(1).strip()
                    print(f"   ✅ Found country: {product_details['country']}")
        except Exception as e:
            print(f"   ⚠ Could not extract country: {e}")

        # Extract irradiation
        try:
            if body_text:
                irradiation_match = re.search(r'Irradiation\s+(Yes|No)', body_text)
                if irradiation_match:
                    irradiation = irradiation_match.group(1)
                    product_details['irradiation'] = irradiation
                    print(f"   ✅ Found irradiation: {product_details['irradiation']}")
        except Exception as e:
            print(f"   ⚠ Could not extract irradiation: {e}")

        # Extract effects and complaints from structured sections
        try:
            if body_text:
                # Effects section
                effects_start = body_text.find('Effects')
                if effects_start != -1:
                    effects_section = body_text[effects_start:effects_start+500]
                    # Extract main effects (those with ratings like 4/4)
                    effect_matches = re.findall(r'([^\n]+)\s+\d+/\d+', effects_section)
                    if effect_matches:
                        product_details['effects'] = ', '.join([e.strip() for e in effect_matches[:3]])  # Take first 3
                        print(f"   ✅ Found effects: {product_details['effects']}")
        except Exception as e:
            print(f"   ⚠ Could not extract effects: {e}")

        try:
            if body_text:
                # Complaints section
                complaints_start = body_text.find('Complaints')
                if complaints_start != -1:
                    complaints_section = body_text[complaints_start:complaints_start+500]
                    # Extract main complaints
                    complaint_matches = re.findall(r'([^\n]+)\s+\d+/\d+', complaints_section)
                    if complaint_matches:
                        product_details['complaints'] = ', '.join([c.strip() for c in complaint_matches[:3]])  # Take first 3
                        print(f"   ✅ Found complaints: {product_details['complaints']}")
        except Exception as e:
            print(f"   ⚠ Could not extract complaints: {e}")

        # Set defaults for stock (not available on dransay.com)
        product_details['stock_level'] = None


        # Set defaults for stock (not available on dransay.com)
        product_details['stock_level'] = None

        # Find pharmacy name and price using improved methods
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

                # Extract price - € comes BEFORE the number, handle comma and dot
                price_match = re.search(r'€\s*(\d+[.,]\d+)\s*/\s*g', price_text)
                if price_match:
                    price_str = price_match.group(1).replace(',', '.')  # Convert German comma to dot
                    price_per_g = float(price_str)
                    print(f"   💰 Found price: €{price_per_g}/g")
            except Exception as e:
                print(f"   ⚠ Could not find price via testid: {e}")

            # If Method 1 succeeded, use result
            if pharmacy_name and price_per_g:
                print(f"   ✅ Method 1 successful: {pharmacy_name} - €{price_per_g}/g")
                product_details['cheapest_pharmacy_name'] = pharmacy_name
                product_details['cheapest_price_per_g'] = price_per_g

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

                    # Look for price in button (handle German comma, € before number)
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
                    product_details['cheapest_pharmacy_name'] = pharmacy_name
                    product_details['cheapest_price_per_g'] = price_per_g
            except Exception as e:
                print(f"   ⚠ Method 2 failed: {e}")

        # Method 3: Fallback - search all elements with €/g pattern
        if not (pharmacy_name and price_per_g):
            print(f"   📍 Method 3: Searching all elements with €/g...")
            try:
                # Search for €/g pattern (handle German comma)
                price_elements = await page.locator('text=/€.*\\/.*g/').all()
                print(f"   Found {len(price_elements)} elements with €/g pattern")

                # Debug: Print all found elements
                for i, elem in enumerate(price_elements[:3]):  # First 3 elements
                    try:
                        text = await elem.inner_text()
                        print(f"   Debug element {i}: '{text[:50]}...'")
                    except:
                        print(f"   Debug element {i}: Error getting text")

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
                    product_details['cheapest_pharmacy_name'] = pharmacy_name
                    product_details['cheapest_price_per_g'] = price_per_g
            except Exception as e:
                print(f"   ⚠ Method 3 failed: {e}")

        # Set final values
        product_details['cheapest_pharmacy_name'] = pharmacy_name
        product_details['cheapest_price_per_g'] = price_per_g

        if pharmacy_name and price_per_g:
            print(f"   💰 {pharmacy_name}: €{price_per_g}/g")
        else:
            print(f"   ⚠ Could not extract pharmacy/price")

    except Exception as e:
        print(f"   ⚠ Error extracting details: {e}")
        # Ensure values are set even if extraction failed
        if 'cheapest_pharmacy_name' not in product_details:
            product_details['cheapest_pharmacy_name'] = None
        if 'cheapest_price_per_g' not in product_details:
            product_details['cheapest_price_per_g'] = None

    # Ensure all required fields exist
    if 'cheapest_pharmacy_name' not in product_details:
        product_details['cheapest_pharmacy_name'] = None
    if 'cheapest_price_per_g' not in product_details:
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

    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'WeedDB.db'))
    cursor = conn.cursor()

    try:
        # Check if product already exists
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_data['id'],))
        existing_product = cursor.fetchone()

        if existing_product:
            print(f"ℹ️ Product '{product_data['name']}' (ID: {product_data['id']}) already exists. Updating product details and prices.")
        else:
            print(f"✨ Adding new product '{product_data['name']}' (ID: {product_data['id']}).")

        # Insert or get producer
        producer_id = None
        final_producer_name = product_data.get('producer_name')
        if final_producer_name:
            cursor.execute("INSERT OR IGNORE INTO producers (name) VALUES (?)",
                          (final_producer_name,))
            cursor.execute("SELECT id FROM producers WHERE name = ?", (final_producer_name,))
            result = cursor.fetchone()
            producer_id = result[0] if result else None

        # Insert product (using INSERT OR REPLACE to update if exists)
        cursor.execute("""
            INSERT OR REPLACE INTO products
            (id, name, variant, genetics, thc_percent, cbd_percent, producer_id,
             rating, review_count, irradiation, country, effects, complaints, url, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            product_data.get('irradiation'),
            product_data.get('country'),
            product_data.get('effects'),
            product_data.get('complaints'),
            product_data['url'],
            datetime.now()
        ))

        # Insert cheapest 'top' pharmacy price
        if product_data.get('cheapest_top_price_per_g'):
            pharmacy_name = product_data.get('cheapest_top_pharmacy_name') or "Unknown Pharmacy"
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
        if product_data.get('cheapest_all_price_per_g'):
            pharmacy_name = product_data.get('cheapest_all_pharmacy_name') or "Unknown Pharmacy"
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