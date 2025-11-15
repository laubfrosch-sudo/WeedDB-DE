#!/usr/bin/env python3
"""
Find new products on shop.dransay.com that are not yet in the WeedDB database.

This script scrapes product names and IDs from the product overview page,
compares them with existing products in the database, and lists new ones.
It supports filtering by vendor, producer, and search term.

Usage:
    python3 find_new_products.py [--vendorId <id>] [--producerId <id>] [--search <term>]
    
Options:
    --vendorId <id>: Filter by vendor ID (e.g., 'all', 'top'). Default: 'all'
    --producerId <id>: Filter by producer ID. Can be a comma-separated list (e.g., '37,56').
    --search <term>: Search for a specific product name (e.g., 'Lemon Haze').

Example:
    python3 find_new_products.py
    python3 find_new_products.py --vendorId top --search "Haze"
    python3 find_new_products.py --producerId 37,56
"""

import asyncio
import sqlite3
import os
import sys
from typing import Dict, List, Any, Optional, Set
from playwright.async_api import async_playwright, Page, Locator
import json
import re

BASE_URL = "https://shop.dransay.com"
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'WeedDB.db')

def get_existing_product_ids() -> Set[int]:
    """Fetch all existing product IDs from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM products")
    existing_ids = {row[0] for row in cursor.fetchall()}
    conn.close()
    return existing_ids

def construct_product_list_url(
    vendor_id: str = "all",
    producer_ids: Optional[List[int]] = None,
    search_term: Optional[str] = None
) -> str:
    """Constructs the product list URL with various filters."""
    filters: Dict[str, Any] = {"topProducersLowPrice": False} # Default filter

    if producer_ids:
        filters["producers"] = producer_ids
        # If specific producers are selected, topProducersLowPrice might need to be true
        # depending on how the site handles it. For now, keep it as false unless specified.

    url_params = {
        "vendorId": vendor_id,
        "deliveryMethod": "shipping",
        "filters": json.dumps(filters) # Filters need to be JSON stringified
    }
    
    if search_term:
        url_params["search"] = search_term.replace(' ', '+')

    # Manually construct query string to avoid issues with Playwright's goto
    query_string = "&".join([f"{k}={v}" for k, v in url_params.items()])
    
    # Special handling for filters to ensure it's properly URL-encoded
    # Playwright's page.goto usually handles this, but explicit is better for complex filters
    final_url = f"{BASE_URL}/products?{query_string}"
    
    # Re-encode the filters part specifically if it contains special characters
    # This is often handled by the browser, but if issues arise, this is where to look.
    # For now, assume json.dumps and direct string concatenation is sufficient.
    
    return final_url

async def scrape_product_names_from_page(page: Page) -> List[Dict[str, Any]]:
    """Extracts product names and IDs from the current page."""
    products_on_page: List[Dict[str, Any]] = []
    
    # Wait for product cards to load
    try:
        await page.wait_for_selector('[data-testid*="product-"]', timeout=10000)
    except Exception:
        print("   ❌ No product cards found on page.")
        return []

    product_card_links = await page.locator('[data-testid*="product-"]').all()
    
    for link_locator in product_card_links:
        try:
            product_url = await link_locator.get_attribute('href')
            if not product_url:
                continue
            
            # Ensure URL is absolute
            if not product_url.startswith('http'):
                product_url = f"{BASE_URL}{product_url}"
            
            product_id = int(product_url.split('/')[-1].split('?')[0]) # Extract ID from URL
            
            # Extract product name from URL path
            # Example: /product/sour-cherry-punch-avaay-291-scp/164
            # Desired: Sour Cherry Punch
            url_path_segments = product_url.split('/')
            # The segment before the ID is usually the name with hyphens
            name_segment = url_path_segments[-2] 
            
            # Replace hyphens with spaces and title case it
            product_name = name_segment.replace('-', ' ').title()
            
            # Further refine: remove producer/variant info if present in the name segment
            # This is a heuristic and might need adjustment
            # Example: "Sour Cherry Punch Avaay 291 Scp" -> "Sour Cherry Punch"
            # Use regex to remove common patterns like producer names, THC/CBD percentages, codes
            product_name = re.sub(r'\b(Avaay|Pedanios|Cannamedical|Aurora|ZOIKS|IMC|Enua|Amici|Bathera|Slouu|Barongo|Demecan|LUANA|Tyson|Tannenbusch|aleph amber|enua Pharma)\b', '', product_name, flags=re.IGNORECASE)
            product_name = re.sub(r'\b\d{2,3}/\d{1,2}\b', '', product_name) # e.g., 291/SCP
            product_name = re.sub(r'\b\d{2,3}\b', '', product_name) # e.g., 291
            product_name = re.sub(r'\b[A-Z]{2,5}\b', '', product_name) # e.g., SCP, CRL, PND
            product_name = re.sub(r'\s+', ' ', product_name).strip() # Remove extra spaces
            
            if not product_name:
                product_name = "Unknown Product" # Fallback if extraction fails
            
            products_on_page.append({
                "id": product_id,
                "name": product_name,
                "url": product_url
            })
        except Exception as e:
            print(f"   ⚠ Error extracting product from card: {e}")
            continue
            
    return products_on_page

async def find_new_products(
    vendor_id: str = "all",
    producer_ids: Optional[List[int]] = None,
    search_term: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Finds new products on shop.dransay.com by scraping and comparing with the database.
    """
    existing_product_ids = get_existing_product_ids()
    new_products_found: List[Dict[str, Any]] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        page_num = 1
        while True:
            url = construct_product_list_url(vendor_id, producer_ids, search_term)
            # Add pagination if the site supports it (e.g., &page=X)
            # For now, assume a single page or that the initial load shows enough.
            # If the site uses infinite scroll, this logic needs to be more complex.
            
            print(f"🔍 Scraping page {page_num}: {url}")
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(2000) # Give some time for dynamic content to load
            except Exception as e:
                print(f"   ❌ Error navigating to {url}: {e}. Skipping this page.")
                break

            products_on_page = await scrape_product_names_from_page(page)
            if not products_on_page:
                print("   No more products found on this page or no products matching criteria.")
                break

            for product in products_on_page:
                if product["id"] not in existing_product_ids:
                    new_products_found.append(product)
                    existing_product_ids.add(product["id"]) # Add to set to avoid duplicates in this run

            # Check for next page button/link (this is highly site-specific)
            # For shop.dransay.com, it seems to load all on one page or use infinite scroll.
            # If there's a "Load More" button or pagination, this needs to be implemented.
            # For now, assume one page is sufficient or that the initial load covers enough.
            # If the site uses infinite scroll, this would involve scrolling down and re-scraping.
            
            # For simplicity, break after first page for now.
            break 
            # If pagination exists, uncomment and implement:
            # next_button = await page.locator('a.next-page-button').first.is_visible()
            # if next_button:
            #     page_num += 1
            #     # Logic to click next button or construct next page URL
            # else:
            #     break

        await browser.close()
    return new_products_found

async def main() -> None:
    vendor_id = "all"
    producer_ids: Optional[List[int]] = None
    search_term: Optional[str] = None

    # Parse command line arguments
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--vendorId" and i + 1 < len(args):
            vendor_id = args[i+1]
            i += 2
        elif arg == "--producerId" and i + 1 < len(args):
            producer_ids = [int(pid) for pid in args[i+1].split(',')]
            i += 2
        elif arg == "--search" and i + 1 < len(args):
            search_term = args[i+1]
            i += 2
        else:
            print(f"Unknown argument: {arg}")
            print(__doc__) # Print docstring for usage
            sys.exit(1)

    print("🔎 Searching for new products on shop.dransay.com...")
    print(f"   Vendor ID: {vendor_id}")
    if producer_ids:
        print(f"   Producer IDs: {producer_ids}")
    if search_term:
        print(f"   Search Term: '{search_term}'")
    print("-" * 40)

    new_products = await find_new_products(vendor_id, producer_ids, search_term)

    if new_products:
        print("\n✨ Found new products not in database:")
        for product in new_products:
            print(f"   - {product['name']} (ID: {product['id']}) - {product['url']}")
        print("\n💡 To add these products, use 'python3 add_product.py <product_name>' for each.")
    else:
        print("\n✅ No new products found matching criteria.")

if __name__ == '__main__':
    asyncio.run(main())
