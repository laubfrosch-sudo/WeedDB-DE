# CLAUDE.md

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WeedDB is a cannabis product database that tracks medical cannabis strains and their prices across multiple pharmacies (Versandapotheken) in Germany. The primary data source is shop.dransay.com, which aggregates cannabis product listings from various licensed pharmacies.

## Database Schema

WeedDB uses a **SQLite database** in **3rd Normal Form (3NF)** for data integrity and complex analysis capabilities. The schema is defined in `schema.sql`.

### Core Tables

**products** - Main product information
- `id` - Product ID from shop.dransay.com (PRIMARY KEY)
- `name` - Cannabis strain name
- `variant` - Full variant descriptor (e.g., "Barongo 30/1 Cali Motion")
- `genetics` - Indica, Sativa, Hybrid-Sativa, Hybrid-Indica, or Hybrid
- `thc_percent`, `cbd_percent` - Cannabinoid percentages
- `producer_id` - Foreign key to producers table
- `stock_level` - Current stock units
- `rating` - User rating (e.g., 4.1)
- `review_count` - Number of reviews (e.g., 312)
- `irradiation` - Yes/No
- `url` - Product URL (UNIQUE)
- `created_at`, `last_updated` - Timestamps

**producers** - Cannabis producers/manufacturers
- `id`, `name` (UNIQUE), `origin`

**terpenes** - Master list of terpenes
- `id`, `name` (UNIQUE)

**product_terpenes** - Links products to terpenes (Many-to-Many)
- `product_id`, `terpene_id`, `percentage`

**effects** - Master list of effects
- `id`, `name` (UNIQUE)

**product_effects** - Links products to effects (Many-to-Many)
- `product_id`, `effect_id`, `strength` (0-3, optional)

**therapeutic_uses** - Master list of medical applications
- `id`, `name` (UNIQUE)

**product_therapeutic_uses** - Links products to therapeutic uses (Many-to-Many)
- `product_id`, `therapeutic_use_id`, `strength` (0-3, optional)

**pharmacies** - German Versandapotheken
- `id`, `name` (UNIQUE), `location`

**prices** - Historical price data
- `id`, `product_id`, `pharmacy_id`, `price_per_g`, `timestamp`
- Enables price trend analysis over time

### Views for Common Queries

**current_prices** - Latest price for each product-pharmacy combination

**cheapest_current_prices** - Current lowest price per product with pharmacy info

## Data Collection from shop.dransay.com

### Critical URL Format

**Always use `vendorId=all` in the URL to see ALL pharmacies**, not just the cheapest:

```
https://shop.dransay.com/product/{product-name}/{product-id}?vendorId=all&deliveryMethod=shipping&filters=%7B%22topProducersLowPrice%22%3Afalse%7D
```

**Wrong approach:**
- `vendorId=top` - Only shows pre-selected "top" pharmacies
- Without `vendorId=all` - May filter out cheaper options

### Workflow for Adding Products

**Use the `add_product.py` script** to automatically scrape and add products:

```bash
python3 add_product.py <product_url> [producer_name] [origin]
```

**Example:**
```bash
python3 add_product.py "https://shop.dransay.com/product/black-cherry-punch-enua-221-bcp-ca/698" "enua Pharma" "Canada"
```

**What the script does:**

1. **Ensures correct URL format**: Automatically converts URL to use `vendorId=all`
2. **Scrapes product data** using Playwright (headless browser):
   - Product ID, name, variant, genetics (Indica/Sativa/Hybrid)
   - THC%, CBD% percentages
   - Rating and review count (extracted from JSON data in page)
   - Producer name (extracted from HTML title tag)
   - **Terpenes**: Limonen, Linalool, Caryophyllen, Myrcen, Pinen, Humulen, Terpinolen
   - **Effects**: relaxing, euphoric, sedative, uplifting, creative, focused, pain relief, anti-inflammatory, anxiety relief
   - **Therapeutic uses**: chronic pain, anxiety, depression, insomnia, inflammation, stress, PTSD, ADHD, appetite loss, nausea, migraine, arthritis, Parkinson, epilepsy
   - Featured pharmacy name and price per gram
3. **Inserts into database**:
   - Creates/updates product record with all extracted data
   - Creates producer record (auto-extracted or from parameter)
   - Links terpenes, effects, and therapeutic uses via junction tables
   - Creates pharmacy record and inserts price with timestamp
4. **Automatic duplicate handling**: If product ID already exists, updates the record and adds new price entry

**Important Notes:**

- **Featured Pharmacy Only**: The script extracts only the featured/cheapest pharmacy shown on the product page
- Historical pricing is preserved - re-running the script adds a new price entry with current timestamp
- Producer name and origin are optional parameters - if not provided, the script attempts to extract from page title
- Terpenes, effects, and therapeutic uses are automatically extracted by keyword matching in page content

### Duplicate Prevention

Use `product_id` (from shop.dransay.com) as the PRIMARY KEY in products table. The same strain may appear with different IDs if it's from different producers or batches.

Running `add_product.py` with an existing product ID will update the product info and add a new price entry (historical tracking).

### Data Integrity Rules

- Price history is preserved - never delete old prices, always INSERT new ones
- When re-adding a product, `last_updated` timestamp is updated
- Pharmacies are identified by unique name
- Producer records are created with INSERT OR IGNORE (won't duplicate)

## WebFetch Configuration

The repository includes pre-configured permission for shop.dransay.com in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": ["WebFetch(domain:shop.dransay.com)"]
  }
}
```

This allows automated fetching of product data without manual approval for each request.

### Bulk Operations

**Update all existing products with latest data:**

```bash
python3 update_all_products.py
```

This script:
- Processes all products in the database concurrently (5 at a time)
- Re-scrapes each product page to get latest ratings, reviews, prices
- Updates terpenes, effects, and therapeutic uses
- Preserves price history by adding new entries
- Takes approximately 1-2 minutes for 100 products
- Outputs progress and summary statistics

**Add multiple new products from a list:**

```bash
python3 add_batch_products.py
```

This script demonstrates batch addition of products:
- Edit the `product_ids` list in the script with new product IDs from shop.dransay.com
- Automatically generates placeholder URLs with product IDs
- Processes products sequentially with error handling
- Shows progress counter (e.g., [5/36])
- Provides final summary of successful/failed additions
- Example: Successfully added 36 new products in ~4 minutes

## Prerequisites

Before setting up WeedDB, ensure you have the following software installed on your system:

**Required Software:**

1. **Python 3.9 or higher**
   - Check version: `python3 --version`
   - Download: https://www.python.org/downloads/

2. **SQLite3**
   - **macOS**: Pre-installed (check with `sqlite3 --version`)
   - **Linux**: Usually pre-installed, or install via package manager:
     - Ubuntu/Debian: `sudo apt-get install sqlite3`
     - Fedora: `sudo dnf install sqlite`
   - **Windows**: Download from https://sqlite.org/download.html
     - Add to PATH environment variable after installation

3. **pip3 (Python package manager)**
   - Usually included with Python 3.9+
   - Check: `pip3 --version`

4. **Internet connection**
   - Required for scraping shop.dransay.com
   - Required for downloading Playwright browser binaries

**Python Packages** (installed in setup steps below):
- `playwright` - Headless browser automation for web scraping
- `mypy` - Static type checker for Python code

**Browser Engine** (installed via Playwright):
- Chromium - Headless browser for rendering JavaScript pages

## Dependencies and Setup

**Required Python packages:**
```bash
pip3 install playwright mypy
python3 -m playwright install chromium
```

**Files:**
- `schema.sql` - Database schema (run once to create DB)
- `add_product.py` - Main script to scrape and add/update individual products
- `update_all_products.py` - Bulk update script for all products
- `add_batch_products.py` - Batch script to add multiple new products from a list of product IDs
- `debug_scrape.py` - Debug utility to inspect page structure when extraction fails
- `WeedDB.db` - SQLite database (auto-created)

**First-time setup:**
```bash
# Install dependencies
pip3 install playwright mypy
python3 -m playwright install chromium

# Create database
sqlite3 WeedDB.db < schema.sql

# Add first product
python3 add_product.py "https://shop.dransay.com/product/..." "Producer Name" "Origin"
```

## Type Safety

All Python code uses **strict type annotations** (Python 3.9+ compatible):
- Functions have fully typed signatures with `Optional`, `Dict`, `List`, `Tuple` from `typing`
- Run type checker: `python3 -m mypy *.py --strict`
- Type checking ensures correct function usage and prevents runtime errors

## Common Database Queries

**View all products with enhanced data:**
```sql
sqlite3 WeedDB.db "SELECT
  p.name, p.genetics, p.thc_percent || '%' as THC,
  p.rating || '★' as Rating, p.review_count as Reviews,
  pr.name as Producer
FROM products p
LEFT JOIN producers pr ON p.producer_id = pr.id
ORDER BY p.rating DESC"
```

**Find products by terpene profile:**
```sql
sqlite3 WeedDB.db "SELECT DISTINCT p.name, p.genetics,
  GROUP_CONCAT(t.name, ', ') as terpenes
FROM products p
JOIN product_terpenes pt ON p.id = pt.product_id
JOIN terpenes t ON pt.terpene_id = t.id
WHERE t.name = 'Myrcen'
GROUP BY p.id"
```

**Find products by therapeutic use:**
```sql
sqlite3 WeedDB.db "SELECT DISTINCT p.name, p.genetics, p.thc_percent,
  GROUP_CONCAT(tu.name, ', ') as uses
FROM products p
JOIN product_therapeutic_uses ptu ON p.id = ptu.product_id
JOIN therapeutic_uses tu ON ptu.therapeutic_use_id = tu.id
WHERE tu.name = 'chronic pain'
GROUP BY p.id
ORDER BY p.rating DESC"
```

**Find products with specific effects:**
```sql
sqlite3 WeedDB.db "SELECT p.name, p.genetics, p.rating,
  GROUP_CONCAT(e.name, ', ') as effects
FROM products p
JOIN product_effects pe ON p.id = pe.product_id
JOIN effects e ON pe.effect_id = e.id
WHERE e.name IN ('relaxing', 'pain relief')
GROUP BY p.id
ORDER BY p.rating DESC"
```

**Current prices (cheapest per product):**
```sql
sqlite3 WeedDB.db "SELECT p.name, MIN(pr.price_per_g) as min_price, ph.name as pharmacy
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
GROUP BY p.id
ORDER BY min_price"
```

**Price history for a product:**
```sql
sqlite3 WeedDB.db "SELECT pr.timestamp, ph.name, pr.price_per_g
FROM prices pr
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE pr.product_id = 698
ORDER BY pr.timestamp"
```

## Architecture Notes

### Data Model
- **3NF SQLite database** with junction tables for many-to-many relationships (terpenes, effects, therapeutic uses)
- **Product ID as PRIMARY KEY**: Uses shop.dransay.com's product ID, same strain from different producers has different IDs
- **Historical price tracking**: Never delete prices, always INSERT new entries with timestamps
- **Automatic de-duplication**: `INSERT OR REPLACE` for products, `INSERT OR IGNORE` for producers/pharmacies

### Web Scraping Implementation
- **Playwright (headless Chromium)** for JavaScript-rendered pages
- **Data extraction strategy**:
  - **Ratings/Reviews**: Extracted from escaped JSON in page HTML (`\"rating\",\"4.1278244028405423\"`)
  - **Producer**: Extracted from HTML `<title>` tag (format: "Product Name - Producer Name")
  - **Terpenes/Effects/Therapeutic Uses**: Keyword matching in page content
- **URL normalization**: Automatically ensures `vendorId=all` parameter for complete pharmacy listings
- **Concurrent processing**: `update_all_products.py` uses ThreadPoolExecutor (5 workers) for bulk updates

### Key Design Decisions
- **Featured pharmacy only**: Only tracks the featured/cheapest pharmacy per product (intentional simplification)
- **Many-to-many via junction tables**: Enables flexible queries like "all products with Myrcen terpene"
- **Keyword-based extraction**: Terpenes, effects, and therapeutic uses extracted by matching known keywords in page text
- **Price history preservation**: Historical pricing enables trend analysis without separate archival process

## Troubleshooting

**If Playwright fails:**
- Ensure Chromium is installed: `python3 -m playwright install chromium`
- Check for headless browser errors in terminal output
- Verify internet connection to shop.dransay.com

**If data extraction fails:**
- Rating/review extraction relies on JSON format in page HTML - if shop.dransay.com changes their Next.js data structure, regex patterns in `add_product.py` may need updating
- Producer extraction from `<title>` tag assumes format: "Product Name - Producer Name"
- Terpene/effect/therapeutic use extraction is keyword-based - new terms need to be added to the keyword lists in `add_product.py`
- Use `debug_scrape.py` to inspect page structure and identify what data is available

**If some products have missing data:**
- Not all products have ratings/reviews (new products may have `NULL` values)
- Producer extraction may fail if title format doesn't match expected pattern
- Use `update_all_products.py` to refresh all products with latest data from shop.dransay.com

## Database Queries

**Open SQLite CLI:**
```bash
sqlite3 WeedDB.db
```

**Useful CLI commands:**
- `.schema` - Show all table definitions
- `.tables` - List all tables
- `.mode column` - Format output as columns
- `.headers on` - Show column headers

**Get database statistics:**
```sql
sqlite3 WeedDB.db "SELECT
  COUNT(*) as Total,
  COUNT(CASE WHEN genetics = 'Indica' THEN 1 END) as Indica,
  COUNT(CASE WHEN genetics = 'Sativa' THEN 1 END) as Sativa,
  COUNT(CASE WHEN genetics = 'Hybrid' THEN 1 END) as Hybrid,
  COUNT(DISTINCT producer_id) as Producers,
  ROUND(AVG(thc_percent), 1) as 'Avg THC%',
  ROUND(AVG(rating), 2) as 'Avg Rating'
FROM products"
```

**List all pharmacies with statistics:**
```sql
sqlite3 WeedDB.db "SELECT
  ph.name as Pharmacy,
  COUNT(DISTINCT pr.product_id) as Products,
  ROUND(MIN(pr.price_per_g), 2) as 'Min €/g',
  ROUND(AVG(pr.price_per_g), 2) as 'Avg €/g'
FROM pharmacies ph
LEFT JOIN prices pr ON ph.id = pr.pharmacy_id
GROUP BY ph.id
ORDER BY COUNT(DISTINCT pr.product_id) DESC"
```

**Find products by therapeutic use with prices:**
```sql
sqlite3 WeedDB.db "SELECT
  p.name,
  p.genetics,
  p.thc_percent || '%' as THC,
  p.rating || '★' as Rating,
  MIN(pr.price_per_g) as 'Min €/g',
  ph.name as Pharmacy
FROM products p
JOIN product_therapeutic_uses ptu ON p.id = ptu.product_id
JOIN therapeutic_uses tu ON ptu.therapeutic_use_id = tu.id
LEFT JOIN prices pr ON p.id = pr.product_id
LEFT JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE tu.name = 'insomnia'
GROUP BY p.id
ORDER BY p.rating DESC"
```

---

## Dynamische Übersichtsdateien

**Wichtiger Hinweis:** Die Datei `SORTEN_ÜBERSICHT.md` wird automatisch aus der `WeedDB.db` Datenbank generiert. Jegliche Änderungen an der Datenbank (Hinzufügen, Ändern oder Löschen von Einträgen) führen dazu, dass sich der Inhalt dieser Markdown-Datei bei der nächsten Aktualisierung ebenfalls ändert. Sowohl die "Bestenliste" als auch die Haupttabelle enthalten jetzt direkte Links zu den jeweiligen Produktseiten.