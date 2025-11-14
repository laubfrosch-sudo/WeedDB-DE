#!/usr/bin/env python3
"""Debug script to see what data is available on the page"""

from playwright.sync_api import sync_playwright
import re

url = "https://shop.dransay.com/product/black-cherry-punch-enua-221-bcp-ca/698?vendorId=all"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until='networkidle', timeout=30000)
    page.wait_for_selector('h1', timeout=10000)

    content = page.content()

    # Search for rating
    print("=== RATING SEARCH ===")
    rating_patterns = [
        r'"rating"\s*:\s*"?(\d+\.\d+)"?',
        r'rating.*?(\d+\.\d+)',
        r'(\d+\.\d+).*?stars',
    ]
    for pattern in rating_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"Pattern: {pattern}")
            print(f"Matches: {matches[:5]}")  # Show first 5 matches
            print()

    # Search for review count
    print("=== REVIEW COUNT SEARCH ===")
    review_patterns = [
        r'"ratingCount"\s*:\s*"?(\d+)"?',
        r'(\d{3,})\+?\s*(?:reviews|ratings)',
    ]
    for pattern in review_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"Pattern: {pattern}")
            print(f"Matches: {matches[:5]}")
            print()

    # Search for producer
    print("=== PRODUCER SEARCH ===")
    producer_patterns = [
        r'"producer"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"',
        r'producer.*?"([A-Za-z\s]+Pharma)"',
        r'enua\s+Pharma',
    ]
    for pattern in producer_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"Pattern: {pattern}")
            print(f"Matches: {matches[:5]}")
            print()

    # Also check if "enua Pharma" literally exists
    if "enua Pharma" in content:
        print("✓ 'enua Pharma' found in content")
        # Find context around it
        idx = content.find("enua Pharma")
        print(f"Context: ...{content[max(0,idx-100):idx+100]}...")

    # Search for producer JSON structure
    print("\n=== SEARCHING FOR PRODUCER JSON ===")
    if '"producer"' in content:
        idx = content.find('"producer"')
        print(f"Producer JSON context: ...{content[idx:idx+200]}...")

    # Search for rating JSON structure
    print("\n=== SEARCHING FOR RATING JSON ===")
    if '"rating"' in content:
        idx = content.find('"rating"')
        print(f"Rating JSON context: ...{content[idx:idx+100]}...")

    # Search for ratingCount
    print("\n=== SEARCHING FOR RATING COUNT ===")
    if '"ratingCount"' in content:
        idx = content.find('"ratingCount"')
        print(f"RatingCount JSON context: ...{content[idx:idx+100]}...")
    else:
        print("'ratingCount' not found - searching for 1549...")
        if "1549" in content:
            idx = content.find("1549")
            print(f"1549 context: ...{content[max(0,idx-50):idx+50]}...")

    # Search for __NEXT_DATA__ (Next.js data)
    print("\n=== SEARCHING FOR __NEXT_DATA__ ===")
    if '__NEXT_DATA__' in content:
        idx = content.find('__NEXT_DATA__')
        next_data_end = content.find('</script>', idx)
        next_data = content[idx:next_data_end]
        print(f"Found __NEXT_DATA__ (first 500 chars): {next_data[:500]}")

        # Try to extract rating and producer from it
        import json
        try:
            json_start = next_data.find('{')
            json_str = next_data[json_start:]
            data = json.loads(json_str)
            print(f"\n__NEXT_DATA__ parsed successfully!")
            print(f"Keys: {list(data.keys())[:10]}")
        except Exception as e:
            print(f"Failed to parse __NEXT_DATA__: {e}")

    browser.close()
