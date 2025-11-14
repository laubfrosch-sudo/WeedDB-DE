#!/usr/bin/env python3
"""
Fix missing producers in the database by re-scraping product pages.
"""

import sqlite3
import asyncio
from playwright.async_api import async_playwright
import re

async def fix_missing_producers():
    """Find products with missing producers and try to fix them"""
    
    # Get products with missing producers
    conn = sqlite3.connect('WeedDB.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.name, p.url 
        FROM products p 
        WHERE p.producer_id IS NULL 
        ORDER BY p.name
    """)
    
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        print("✅ No products with missing producers found!")
        return
    
    print(f"🔧 Found {len(products)} products with missing producers")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for product_id, product_name, product_url in products:
            print(f"\n🔍 Checking: {product_name}")
            
            try:
                page = await browser.new_page()
                await page.goto(product_url, wait_until='networkidle', timeout=30000)
                
                # Extract producer from page
                body_text = await page.locator('body').inner_text()
                
                # Try to find producer
                producer_name = None
                
                # Method 1: Look for "Producer[...]" pattern
                producer_match = re.search(r'Producer\[([^\]]+)\]', body_text)
                if producer_match:
                    producer_name = producer_match.group(1).strip()
                    print(f"   ✅ Found producer: {producer_name}")
                
                # Method 2: Look in context around country
                if not producer_name:
                    country_pos = body_text.find('Country')
                    if country_pos != -1:
                        start_pos = max(0, country_pos - 200)
                        end_pos = min(len(body_text), country_pos + 200)
                        context = body_text[start_pos:end_pos]
                        
                        producer_patterns = [
                            r'enua Pharma', r'Cantourage', r'Aurora Cannabis', r'Pedanios',
                            r'Cannamedical', r'ZOIKS', r'All Nations', r'IMC', r'Enua',
                            r'Amici', r'Bathera', r'420 Natural', r'THC Akut', r'Remexian',
                            r'Avaay', r'Buuo', r'Demecan', r'LUANA', r'Tyson', r'Slouu',
                            r'Barongo', r'Tannenbusch', r'aleph amber'
                        ]
                        
                        for pattern in producer_patterns:
                            if pattern in context:
                                producer_name = pattern
                                print(f"   ✅ Found producer in context: {producer_name}")
                                break
                
                # If found, update database
                if producer_name:
                    conn = sqlite3.connect('WeedDB.db')
                    cursor = conn.cursor()
                    
                    # Insert producer if not exists
                    cursor.execute("INSERT OR IGNORE INTO producers (name) VALUES (?)", (producer_name,))
                    
                    # Get producer ID
                    cursor.execute("SELECT id FROM producers WHERE name = ?", (producer_name,))
                    result = cursor.fetchone()
                    
                    if result:
                        producer_id_db = result[0]
                        # Update product
                        cursor.execute("UPDATE products SET producer_id = ? WHERE id = ?", 
                                     (producer_id_db, product_id))
                        conn.commit()
                        print(f"   ✅ Updated database: {product_name} -> {producer_name}")
                    else:
                        print(f"   ❌ Could not get producer ID for {producer_name}")
                    
                    conn.close()
                else:
                    print(f"   ⚠ No producer found for {product_name}")
                
                await page.close()
                
            except Exception as e:
                print(f"   ❌ Error processing {product_name}: {e}")
        
        await browser.close()
    
    print("\n🎉 Producer fix complete!")

if __name__ == '__main__':
    asyncio.run(fix_missing_producers())
