import asyncio
from playwright.async_api import async_playwright

async def inspect_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Headless=False to see what's happening
        context = await browser.new_context()
        page = await context.new_page()

        # Go to a product page
        url = "https://shop.dransay.com/product/big-purple-dragon-remexian-251-bpd/174099?vendorId=top&deliveryMethod=shipping&filters=%7B%22topProducersLowPrice%22%3Atrue%7D"
        print(f"Loading: {url}")
        await page.goto(url, wait_until='networkidle', timeout=30000)

        # Wait a bit for dynamic content
        await page.wait_for_timeout(5000)

        # Look for price-related elements
        print("=== PRICE ELEMENTS ===")
        price_selectors = [
            '[data-testid*="price"]',
            'text=/€.*\\/.*g/',
            '.price',
            '[class*="price"]',
            'text=/€/',
            'button:has-text("€")',
            'div:has-text("€")'
        ]

        for selector in price_selectors:
            try:
                elements = page.locator(selector)
                count = await elements.count()
                if count > 0:
                    print(f"✅ {selector}: {count} elements")
                    # Get first element text
                    first_elem = elements.first
                    if first_elem:
                        text = await first_elem.text_content()
                        if text:
                            print(f"   Text: {text[:100]}...")
                else:
                    print(f"❌ {selector}: 0 elements")
            except Exception as e:
                print(f"⚠️  {selector}: Error - {e}")

        # Look for pharmacy/vendor information
        print("\n=== PHARMACY ELEMENTS ===")
        pharmacy_selectors = [
            '[data-testid*="vendor"]',
            '[data-testid*="pharmacy"]',
            'text=/Apotheke/',
            'text=/Pharmacy/',
            '[class*="vendor"]',
            '[class*="pharmacy"]'
        ]

        for selector in pharmacy_selectors:
            try:
                elements = page.locator(selector)
                count = await elements.count()
                if count > 0:
                    print(f"✅ {selector}: {count} elements")
                    first_elem = elements.first
                    if first_elem:
                        text = await first_elem.text_content()
                        if text:
                            print(f"   Text: {text[:100]}...")
                else:
                    print(f"❌ {selector}: 0 elements")
            except Exception as e:
                print(f"⚠️  {selector}: Error - {e}")

        # Take a screenshot for manual inspection
        await page.screenshot(path="debug_screenshot.png")
        print("\n📸 Screenshot saved as debug_screenshot.png")

        await browser.close()

asyncio.run(inspect_page())