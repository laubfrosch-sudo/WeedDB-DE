---
created: 2024-01-15
updated: 2025-11-15
version: 1.5.0
author: laubfrosch-sudo
status: stable
description: Technical documentation and guidelines for Claude AI when working with WeedDB
sync_with: GEMINI.md, docs/ai-assistants/CLAUDE.md
---

<div align="center">
  <img src="../assets/icons/WeedDB.jpeg" alt="WeedDB Logo" width="300"/>
</div>

# CLAUDE.md

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> *Logo created with Google Gemini*

**IMPORTANT FOR AI ASSISTANTS:** When editing this file (CLAUDE.md), always synchronize the corresponding instructions in GEMINI.md. All files must remain consistent regarding schema definitions, dependencies, and core functionality.

**VERSION 1.4.0 UPDATE:** Enhanced batch processing, auto-recovery features, and improved data extraction reliability.

**OBSIDIAN INTEGRATION:** This repository is optimized for Obsidian.md knowledge management with structured folders, cross-links, and navigation guides.

## 📝 Documentation Metadata Policy

**CRITICAL FOR AI ASSISTANTS:** When editing ANY Markdown file in this repository, you **MUST** update the YAML frontmatter:

1. **Update the `updated` field** to today's date (YYYY-MM-DD format)
2. **Verify the `version` field** matches the current WeedDB version (1.5.0)
3. **Check the `status` field** (stable/draft/deprecated)

**Example:**
```yaml
---
created: 2024-01-15
updated: 2025-11-15  # ← Update this to TODAY'S date!
version: 1.5.0        # ← Verify this matches current WeedDB version
status: stable
---
```

**Full guidelines:** See `docs/DOCUMENTATION_MAINTENANCE.md`

**Files that require frontmatter metadata:**
- ✅ All files in `docs/user-guides/`
- ✅ All files in `docs/ai-assistants/`
- ✅ All files in `docs/development/`
- ✅ README.md, START.md, CLAUDE.md, GEMINI.md
- ✅ ANLEITUNG.md, INSTRUCTIONS.md
- ❌ Auto-generated files (`docs/generated/SORTEN_ÜBERSICHT.md`)
- ❌ Python scripts (*.py), SQL files, data files

**When syncing CLAUDE.md ↔ GEMINI.md:**
- Both files must have the **same** `updated` date
- Both files must have the **same** `version` number

---

## Project Overview

WeedDB is a cannabis product database that tracks medical cannabis strains and their prices across multiple pharmacies (Versandapotheken) in Germany. The primary data source is shop.dransay.com, which aggregates cannabis product listings from various licensed pharmacies.

## Database Schema

WeedDB uses a **SQLite database** in **3rd Normal Form (3NF)** for data integrity and complex analysis capabilities. The schema is defined in `data/schema.sql`.

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
- `country` - Country of origin
- `effects` - Reported effects (e.g., "entspannend, schmerzlindernd")
- `complaints` - Reported complaints/conditions it helps with (e.g., "Schlafstörungen, chronische Schmerzen")
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
- `product_id`, `effect_id`, `strength` (0-4, optional)

**therapeutic_uses** - Master list of medical applications
- `id`, `name` (UNIQUE)

**product_therapeutic_uses** - Links products to therapeutic uses (Many-to-Many)
- `product_id`, `therapeutic_use_id`, `strength` (0-4, optional)

**pharmacies** - German Versandapotheken
- `id`, `name` (UNIQUE), `location`

**prices** - Historical price data with category tracking
- `id`, `product_id`, `pharmacy_id`, `price_per_g`, `category`, `timestamp`
- `category` - Either "top" (top pharmacies) or "all" (all pharmacies)
- Stores only the cheapest price for each category at each timestamp
- Enables price trend analysis over time

### Price Tracking Strategy

The database stores **only the cheapest price** for each product in two categories:

1. **Top Pharmacies** (`category='top'`) - Best price among curated "top" pharmacies
2. **All Pharmacies** (`category='all'`) - Best price across all available pharmacies

This approach minimizes storage while capturing the most relevant price information. Each scrape creates two new price entries with the current cheapest pharmacy name and price for each category.

## Data Collection from shop.dransay.com

### Workflow for Adding Products

**Use the `add_product.py` script** to automatically scrape and add products by product name:

```bash
python3 add_product.py <product_name>
```

**Examples:**
```bash
python3 add_product.py 'sourdough'
python3 add_product.py 'gelato'
python3 add_product.py 'wedding cake'
```

### How the Script Works

The script uses a **two-category approach** to find the best prices:

**Step-by-Step Process:**

1. **Search for Product** - Searches shop.dransay.com for the product name
2. **For "Top Pharmacies" (vendorId=top)**:
   - Navigates to product page with `vendorId=top` parameter
   - Extracts the cheapest pharmacy name and price shown (site automatically displays cheapest)
   - Stores: pharmacy name, price, category='top'
3. **For "All Pharmacies" (vendorId=all)**:
   - Navigates to product page with `vendorId=all` parameter
   - Extracts the cheapest pharmacy name and price shown
   - Stores: pharmacy name, price, category='all'
4. **Database Insert**:
   - Creates product record (ID, name, URL)
   - Creates pharmacy records if they don't exist
   - Inserts two price entries (one for each category) with timestamps

**Key Features:**

- **Minimal Storage**: Only 2 price entries per product per scrape
- **Real Pharmacy Names**: Actual pharmacy names (e.g., "Paracelsus Apotheke") instead of generic placeholders
- **Automatic Comparison**: The website's `vendorId` parameter automatically shows the cheapest option
- **Historical Tracking**: Re-running the script adds new timestamped entries, preserving price history
- **Clean Output**: Shows exactly which pharmacy has the best price in each category

**Example Output:**
```
=== Scraping Top Pharmacies ===
🔍 Searching for 'sourdough' (top)
   ✅ Found product
   🌐 Loading product page (top)
   💰 Sanvivo Cannabis Apotheke (=Senftenauer): €6.77/g

=== Scraping All Pharmacies ===
🔍 Searching for 'sourdough' (all)
   ✅ Found product
   🌐 Loading product page (all)
   💰 Paracelsus Apotheke: €5.69/g
```

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

**Update all products in database:**
```bash
python3 update_prices.py
```
This script:
- Fetches all products from the database
- Re-scrapes prices for each product
- Shows progress and provides summary

**Add multiple products from file (Enhanced in v1.4.0):**
```bash
python3 add_products_batch.py example_products.txt --yes
```
File format: one product name per line (see `data/example_products.txt`)
- **New in v1.4.0**: Processes products individually with 3-second pauses to avoid timeouts

**Fix missing producer data (New in v1.4.0):**
```bash
python3 fix_producers.py
```
Automatically corrects missing producer information by re-scraping product pages.

### Querying Price Data

**View prices for a specific product:**

```bash
sqlite3 WeedDB.db "SELECT p.name, pr.price_per_g, pr.category, ph.name as pharmacy, pr.timestamp
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE p.name LIKE '%sourdough%'
ORDER BY pr.category, pr.price_per_g"
```

**Example output:**
```
Sourdough|5.69|all|Paracelsus Apotheke|2025-11-14 18:56:24
Sourdough|6.77|top|Sanvivo Cannabis Apotheke (=Senftenauer)|2025-11-14 18:56:24
```

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
- `data/schema.sql` - Database schema (run once to create DB)
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
python3 add_product.py 'sourdough'
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

**Current prices by category:**
```sql
sqlite3 WeedDB.db "SELECT p.name, pr.category, pr.price_per_g, ph.name as pharmacy
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE pr.timestamp = (SELECT MAX(timestamp) FROM prices WHERE product_id = p.id AND category = pr.category)
ORDER BY p.name, pr.category"
```

**Price history for a product (by category):**
```sql
sqlite3 WeedDB.db "SELECT pr.timestamp, pr.category, ph.name, pr.price_per_g
FROM prices pr
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE pr.product_id = 973
ORDER BY pr.timestamp DESC, pr.category"
```

**Find cheapest products overall:**
```sql
sqlite3 WeedDB.db "SELECT p.name, MIN(pr.price_per_g) as min_price, ph.name as pharmacy, pr.category
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
GROUP BY p.id
ORDER BY min_price"
```

## Architecture Notes

### Data Model
- **SQLite database** with simple product and price tracking
- **Product ID as PRIMARY KEY**: Uses shop.dransay.com's product ID
- **Category-based price tracking**: Two price entries per scrape (top/all)
- **Historical price tracking**: Never delete prices, always INSERT new entries with timestamps
- **Automatic de-duplication**: `INSERT OR IGNORE` for pharmacies

### Web Scraping Implementation
- **Playwright (headless Chromium)** for JavaScript-rendered pages
- **Two-step scraping process**:
  1. Search page → Find product URL
  2. Product page with `vendorId` parameter → Extract cheapest pharmacy
- **Data extraction strategy**:
  - **Product Name**: From page `<h1>` element
  - **Producer, Country, Irradiation, Genetics, Effects, Complaints, THC, CBD, Rating, Review Count**: Extracted using specific Playwright selectors targeting visible elements on the product page. This replaces previous brittle methods like regex parsing of embedded JSON or general page text.
  - **Pharmacy Name**: Text search for "Apotheke" keyword in DOM
  - **Price**: Regex pattern `€\s*(\d+\.\d+)\s*/\s*g`
- **Category differentiation**: Uses `vendorId=top` and `vendorId=all` URL parameters

### Key Design Decisions
- **Minimal storage approach**: Only 2 prices per product per scrape (top + all categories)
- **Leverages website logic**: Shop.dransay.com automatically displays cheapest pharmacy based on `vendorId` parameter
- **Real pharmacy names**: Stores actual pharmacy names instead of generic placeholders
- **Simplified scraping**: No need to parse multiple pharmacy cards - website does the filtering
- **Price history preservation**: Re-running script adds new timestamped entries for trend analysis

## Troubleshooting

**If Playwright fails:**
- Ensure Chromium is installed: `python3 -m playwright install chromium`
- Check for headless browser errors in terminal output
- Verify internet connection to shop.dransay.com

**If product not found:**
- Verify the product name matches what appears on shop.dransay.com
- Try a shorter or more generic search term (e.g., "sourdough" instead of "sourdough pedanios")
- Check if the product is actually available on the website

**If price/pharmacy extraction fails:**
- Pharmacy name extraction looks for "Apotheke" keyword in page text
- If shop.dransay.com changes their page structure, selectors in `add_product.py` may need updating
- Price pattern expects format: "€X.XX / g" or "€X.XX/g"

**If producer or price data is incorrect in database:**
- **Manual Correction Method**: When scraping fails to extract correct data, manually verify and update:
  1. Check product page directly: `https://shop.dransay.com/product/p/{product_id}`
  2. Identify correct producer from "Producer[Name]" section
  3. Note correct price from "Buying from" section
  4. Update database directly:
     ```bash
     # Add missing producer
     sqlite3 WeedDB.db "INSERT OR IGNORE INTO producers (name) VALUES ('Correct Producer Name');"

     # Update product producer_id
     sqlite3 WeedDB.db "UPDATE products SET producer_id = (SELECT id FROM producers WHERE name = 'Correct Producer Name') WHERE id = {product_id};"

     # Add missing pharmacy
     sqlite3 WeedDB.db "INSERT OR IGNORE INTO pharmacies (name) VALUES ('Correct Pharmacy Name');"

     # Add correct prices
     sqlite3 WeedDB.db "INSERT INTO prices (product_id, pharmacy_id, price_per_g, category, timestamp) VALUES ({product_id}, (SELECT id FROM pharmacies WHERE name = 'Correct Pharmacy Name'), {price}, '{category}', datetime('now'));"
     ```
  5. Regenerate overview: `python3 generate_overview.py`

## Database Queries

**For comprehensive query examples, see `QUERY_EXAMPLES.md`** - includes multi-pharmacy price comparison, product search by terpenes/effects, statistics, and advanced analytics.

**Open SQLite CLI:**
```bash
sqlite3 WeedDB.db
```

**Useful CLI commands:**
- `.schema` - Show all table definitions
- `.tables` - List all tables and views
- `.mode column` - Format output as columns
- `.headers on` - Show column headers
- `.width 30 10 10 10` - Set column widths for better formatting

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

**Multi-pharmacy price comparison (NEW):**
```sql
sqlite3 WeedDB.db "SELECT
  product_name,
  pharmacy_count as 'Pharmacies',
  min_price || '€' as 'Cheapest',
  max_price || '€' as 'Most Expensive',
  price_spread || '€' as 'Price Difference'
FROM product_price_stats
WHERE pharmacy_count > 1
ORDER BY price_spread DESC
LIMIT 10"
```

**Top 10 cheapest pharmacies overall:**
```sql
sqlite3 WeedDB.db "SELECT
  pharmacy_name,
  products_offered as 'Products',
  avg_price_per_g || '€' as 'Avg Price',
  times_cheapest as '# Times Cheapest'
FROM pharmacy_price_ranking
LIMIT 10"
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

**Wichtiger Hinweis:** Die Datei `docs/generated/SORTEN_ÜBERSICHT.md` wird mit dem Skript `generate_overview.py` aus der `WeedDB.db` Datenbank generiert. 

**Nach dem Hinzufügen oder Aktualisieren von Produkten MUSS das Skript ausgeführt werden:**

```bash
python3 generate_overview.py
```

Das Skript erstellt eine sortierte Übersicht aller Produkte mit:
- Bestenliste (höchster THC, bester Preis, Community-Liebling, etc.)
- Vollständige Produkttabelle sortiert nach Bewertungsanzahl
- Direkte Links zu allen Produktseiten auf shop.dransay.com
- Automatischen Timestamp der letzten Aktualisierung

**WICHTIG:** Die Übersicht ist nur so aktuell wie die Daten in der Datenbank und die letzte Ausführung des Skripts!