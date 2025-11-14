#!/usr/bin/env python3
"""
Add cannabis product to WeedDB from shop.dransay.com
Extracts product data and featured pharmacy pricing using Playwright
"""

import sys
import re
import sqlite3
from datetime import datetime
from typing import Any, Dict, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def extract_product_id_from_url(url: str) -> Optional[int]:
    """Extract product ID from dransay URL"""
    match = re.search(r'/product/[^/]+/(\d+)', url)
    return int(match.group(1)) if match else None

def ensure_vendor_all(url: str) -> str:
    """Ensure URL has vendorId=all parameter"""
    if 'vendorId=' not in url:
        separator = '&' if '?' in url else '?'
        url = url.split('?')[0] + '?vendorId=all&deliveryMethod=shipping&filters=%7B%22topProducersLowPrice%22%3Afalse%7D'
    elif 'vendorId=top' in url:
        url = url.replace('vendorId=top', 'vendorId=all')
    return url

def scrape_product_data(url: str) -> Optional[Dict[str, Any]]:
    """Scrape product data from shop.dransay.com using Playwright"""

    url = ensure_vendor_all(url)
    print(f"🌐 Fetching: {url}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_selector('h1', timeout=10000)

            # Extract product data
            product_data: Dict[str, Any] = {}

            # Basic info
            product_data['id'] = extract_product_id_from_url(url)
            product_data['name'] = page.locator('h1').first.inner_text().strip()
            product_data['url'] = url

            print(f"📦 Product: {product_data['name']} (ID: {product_data['id']})")

            # Try to extract variant (often in subtitle or product name)
            try:
                subtitle = page.locator('h2, .subtitle, [class*="variant"]').first.inner_text().strip()
                product_data['variant'] = subtitle
            except:
                product_data['variant'] = None

            # Extract THC/CBD percentages
            try:
                thc_text = page.locator('text=/THC.*?\\d+%/').first.inner_text()
                thc_match = re.search(r'(\d+(?:\.\d+)?)%', thc_text)
                product_data['thc_percent'] = float(thc_match.group(1)) if thc_match else None
            except:
                product_data['thc_percent'] = None

            try:
                cbd_text = page.locator('text=/CBD.*?\\d+%/').first.inner_text()
                cbd_match = re.search(r'(\d+(?:\.\d+)?)%', cbd_text)
                product_data['cbd_percent'] = float(cbd_match.group(1)) if cbd_match else None
            except:
                product_data['cbd_percent'] = None

            # Extract genetics (Indica/Sativa/Hybrid)
            try:
                genetics_text = page.locator('text=/Indica|Sativa|Hybrid/i').first.inner_text()
                if 'Indica' in genetics_text:
                    product_data['genetics'] = 'Indica'
                elif 'Sativa' in genetics_text:
                    product_data['genetics'] = 'Sativa'
                elif 'Hybrid' in genetics_text:
                    product_data['genetics'] = 'Hybrid'
            except:
                product_data['genetics'] = None

            # Extract rating and review count
            try:
                # Get all text from page to search for rating
                page_text = page.content()

                # Look for escaped JSON format: \"rating\",\"4.1278244028405423\"
                rating_match = re.search(r'\\?"rating\\?",\\?"(\d+\.\d+)\\?"', page_text)
                if rating_match:
                    rating_value = float(rating_match.group(1))
                    # Round to 1 decimal place like the UI shows
                    product_data['rating'] = round(rating_value, 1)
                else:
                    # Fallback: look for unescaped JSON
                    rating_match = re.search(r'"rating"\s*:\s*"?(\d+\.\d+)"?', page_text)
                    if rating_match:
                        rating_value = float(rating_match.group(1))
                        product_data['rating'] = round(rating_value, 1)
                    else:
                        product_data['rating'] = None

                # Look for escaped JSON format: \"ratingCount\",\"1549\"
                review_match = re.search(r'\\?"ratingCount\\?",\\?"(\d+)\\?"', page_text)
                if review_match:
                    product_data['review_count'] = int(review_match.group(1))
                else:
                    # Fallback: look for unescaped JSON
                    review_match = re.search(r'"ratingCount"\s*:\s*"?(\d+)"?', page_text)
                    if review_match:
                        product_data['review_count'] = int(review_match.group(1))
                    else:
                        product_data['review_count'] = None
            except Exception as e:
                print(f"   ⚠ Rating extraction failed: {e}")
                product_data['rating'] = None
                product_data['review_count'] = None

            # Extract producer/manufacturer
            try:
                # First try: Look for in title tag like "Black Cherry Punch: enua 22/1 BCP CA - enua Pharma"
                title_match = re.search(r'<title>[^<]+-\s*([^<]+?)</title>', page_text)
                if title_match:
                    title_producer = title_match.group(1).strip()
                    # Clean up common suffixes
                    title_producer = re.sub(r'\s*\|.*$', '', title_producer)  # Remove " | DrAnsay" etc
                    if len(title_producer) > 3 and 'shop' not in title_producer.lower():
                        product_data['producer_name'] = title_producer
                    else:
                        product_data['producer_name'] = None
                else:
                    # Fallback: look for escaped JSON or other patterns
                    producer_match = re.search(r'"producer"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"', page_text)
                    if producer_match:
                        product_data['producer_name'] = producer_match.group(1).strip()
                    else:
                        product_data['producer_name'] = None
            except Exception as e:
                print(f"   ⚠ Producer extraction failed: {e}")
                product_data['producer_name'] = None

            # Extract terpenes
            product_data['terpenes'] = []
            try:
                # Look for common terpene names
                terpene_names = ['Limonen', 'Linalool', 'Beta-Caryophyllen', 'Caryophyllen', 'Beta-Myrcen',
                                'Myrcen', 'Pinene', 'Pinen', 'Humulen', 'Terpinolen', 'Ocimene']
                for terpene in terpene_names:
                    if terpene.lower() in page_text.lower():
                        # Normalize name
                        normalized = terpene.replace('Beta-', '').replace('Alpha-', '')
                        if normalized not in product_data['terpenes']:
                            product_data['terpenes'].append(normalized)
            except Exception as e:
                print(f"   ⚠ Terpene extraction failed: {e}")

            # Extract effects
            product_data['effects'] = []
            try:
                effect_keywords = {
                    'relaxing': ['relaxing', 'relaxation', 'entspannend'],
                    'euphoric': ['euphoric', 'euphorisch', 'mood enhancement'],
                    'sedative': ['sedative', 'sedierend', 'sleep'],
                    'uplifting': ['uplifting', 'energizing', 'energetisch'],
                    'creative': ['creative', 'kreativ'],
                    'focused': ['focus', 'focused', 'konzentration'],
                    'pain relief': ['pain relief', 'schmerzlindernd', 'analgesic'],
                    'anti-inflammatory': ['anti-inflammatory', 'entzündungshemmend'],
                    'anxiety relief': ['anxiety', 'anxiolytic', 'angstlösend']
                }
                page_lower = page_text.lower()
                for effect, keywords in effect_keywords.items():
                    if any(kw.lower() in page_lower for kw in keywords):
                        product_data['effects'].append(effect)
            except Exception as e:
                print(f"   ⚠ Effect extraction failed: {e}")

            # Extract therapeutic uses
            product_data['therapeutic_uses'] = []
            try:
                therapeutic_keywords = {
                    'chronic pain': ['chronic pain', 'chronische schmerzen'],
                    'anxiety': ['anxiety', 'angst'],
                    'depression': ['depression'],
                    'insomnia': ['insomnia', 'schlafstörung', 'sleep disorder'],
                    'inflammation': ['inflammation', 'entzündung'],
                    'stress': ['stress'],
                    'PTSD': ['ptsd', 'post-traumatic'],
                    'ADHD': ['adhd', 'attention deficit'],
                    'appetite loss': ['appetite', 'appetit'],
                    'nausea': ['nausea', 'übelkeit'],
                    'migraine': ['migraine', 'migräne'],
                    'arthritis': ['arthritis', 'arthrose'],
                    'Parkinson': ['parkinson'],
                    'epilepsy': ['epilepsy', 'epilepsie']
                }
                page_lower = page_text.lower()
                for use, keywords in therapeutic_keywords.items():
                    if any(kw.lower() in page_lower for kw in keywords):
                        product_data['therapeutic_uses'].append(use)
            except Exception as e:
                print(f"   ⚠ Therapeutic use extraction failed: {e}")

            # Extract featured pharmacy name and price
            try:
                # Look for price per gram display
                price_elem = page.locator('text=/€\\s*\\d+\\.\\d+\\s*\\/\\s*g/').first
                price_text = price_elem.inner_text()
                price_match = re.search(r'€\s*(\d+\.\d+)', price_text)
                product_data['price_per_g'] = float(price_match.group(1)) if price_match else None

                # Try to find pharmacy name (often in a select/dropdown or label nearby)
                try:
                    pharmacy_elem = page.locator('[data-testid*="vendor"], [class*="pharmacy"], [class*="vendor"]').first
                    product_data['pharmacy_name'] = pharmacy_elem.inner_text().strip().split('\n')[0]
                except:
                    product_data['pharmacy_name'] = None

            except:
                product_data['price_per_g'] = None
                product_data['pharmacy_name'] = None

            browser.close()

            # Display extracted data
            print(f"   Variant: {product_data.get('variant', 'N/A')}")
            print(f"   Genetics: {product_data.get('genetics', 'N/A')}")
            print(f"   Producer: {product_data.get('producer_name', 'N/A')}")
            print(f"   THC: {product_data.get('thc_percent', 'N/A')}%")
            print(f"   CBD: {product_data.get('cbd_percent', 'N/A')}%")
            print(f"   Rating: {product_data.get('rating', 'N/A')} ({product_data.get('review_count', 'N/A')} reviews)")

            if product_data.get('terpenes'):
                print(f"   Terpenes: {', '.join(product_data['terpenes'])}")
            if product_data.get('effects'):
                print(f"   Effects: {', '.join(product_data['effects'][:3])}...")
            if product_data.get('therapeutic_uses'):
                print(f"   Therapeutic: {', '.join(product_data['therapeutic_uses'][:3])}...")

            print(f"\n💰 Featured Pharmacy:")
            print(f"   {product_data.get('pharmacy_name', 'N/A')}")
            print(f"   €{product_data.get('price_per_g', 'N/A')}/g")

            return product_data

        except PlaywrightTimeout as e:
            print(f"❌ Timeout: {e}")
            browser.close()
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            browser.close()
            return None

def insert_product_to_db(product_data: Optional[Dict[str, Any]], producer_name: Optional[str] = None, origin: Optional[str] = None) -> bool:
    """Insert product data into WeedDB"""

    if not product_data:
        print("❌ No product data to insert")
        return False

    conn = sqlite3.connect('WeedDB.db')
    cursor = conn.cursor()

    try:
        # Insert or get producer (from parameter or extracted data)
        producer_id = None
        final_producer_name = producer_name or product_data.get('producer_name')
        if final_producer_name:
            cursor.execute("INSERT OR IGNORE INTO producers (name, origin) VALUES (?, ?)",
                          (final_producer_name, origin))
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

        # Insert pharmacy and price (if available)
        if product_data.get('pharmacy_name') and product_data.get('price_per_g'):
            cursor.execute("INSERT OR IGNORE INTO pharmacies (name) VALUES (?)",
                          (product_data['pharmacy_name'],))
            cursor.execute("SELECT id FROM pharmacies WHERE name = ?",
                          (product_data['pharmacy_name'],))
            pharmacy_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO prices (product_id, pharmacy_id, price_per_g, timestamp)
                VALUES (?, ?, ?, ?)
            """, (product_data['id'], pharmacy_id, product_data['price_per_g'], datetime.now()))

        # Insert terpenes
        if product_data.get('terpenes'):
            for terpene_name in product_data['terpenes']:
                # Insert terpene if not exists
                cursor.execute("INSERT OR IGNORE INTO terpenes (name) VALUES (?)", (terpene_name,))
                cursor.execute("SELECT id FROM terpenes WHERE name = ?", (terpene_name,))
                terpene_id = cursor.fetchone()[0]

                # Link to product (delete old links first to avoid duplicates on re-run)
                cursor.execute("DELETE FROM product_terpenes WHERE product_id = ? AND terpene_id = ?",
                              (product_data['id'], terpene_id))
                cursor.execute("INSERT INTO product_terpenes (product_id, terpene_id) VALUES (?, ?)",
                              (product_data['id'], terpene_id))

        # Insert effects
        if product_data.get('effects'):
            for effect_name in product_data['effects']:
                cursor.execute("INSERT OR IGNORE INTO effects (name) VALUES (?)", (effect_name,))
                cursor.execute("SELECT id FROM effects WHERE name = ?", (effect_name,))
                effect_id = cursor.fetchone()[0]

                cursor.execute("DELETE FROM product_effects WHERE product_id = ? AND effect_id = ?",
                              (product_data['id'], effect_id))
                cursor.execute("INSERT INTO product_effects (product_id, effect_id) VALUES (?, ?)",
                              (product_data['id'], effect_id))

        # Insert therapeutic uses
        if product_data.get('therapeutic_uses'):
            for use_name in product_data['therapeutic_uses']:
                cursor.execute("INSERT OR IGNORE INTO therapeutic_uses (name) VALUES (?)", (use_name,))
                cursor.execute("SELECT id FROM therapeutic_uses WHERE name = ?", (use_name,))
                use_id = cursor.fetchone()[0]

                cursor.execute("DELETE FROM product_therapeutic_uses WHERE product_id = ? AND therapeutic_use_id = ?",
                              (product_data['id'], use_id))
                cursor.execute("INSERT INTO product_therapeutic_uses (product_id, therapeutic_use_id) VALUES (?, ?)",
                              (product_data['id'], use_id))

        conn.commit()
        print(f"\n✅ Successfully added '{product_data['name']}' to database")

        # Show what was inserted
        cursor.execute("""
            SELECT p.name, p.genetics, p.thc_percent, p.rating,
                   ph.name as pharmacy, pr.price_per_g
            FROM products p
            LEFT JOIN prices pr ON p.id = pr.product_id
            LEFT JOIN pharmacies ph ON pr.pharmacy_id = ph.id
            WHERE p.id = ?
            ORDER BY pr.timestamp DESC
            LIMIT 1
        """, (product_data['id'],))

        result = cursor.fetchone()
        if result:
            print(f"   Product: {result[0]} ({result[1]})")
            print(f"   THC: {result[2]}%")
            print(f"   Rating: {result[3]}★")
            if result[4] and result[5]:
                print(f"   Price: €{result[5]}/g at {result[4]}")

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        conn.close()
        return False

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python add_product.py <product_url> [producer_name] [origin]")
        print("\nExample:")
        print("  python add_product.py 'https://shop.dransay.com/product/black-cherry-punch-enua-221-bcp-ca/698'")
        print("  python add_product.py 'https://shop.dransay.com/product/...' 'Aurora Cannabis' 'Canada'")
        sys.exit(1)

    url = sys.argv[1]
    producer_name = sys.argv[2] if len(sys.argv) > 2 else None
    origin = sys.argv[3] if len(sys.argv) > 3 else None

    # Scrape product data
    product_data = scrape_product_data(url)

    if not product_data:
        print("\n❌ Failed to scrape product data")
        sys.exit(1)

    # Insert into database
    success = insert_product_to_db(product_data, producer_name, origin)

    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
