# AGENTS.md

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This file provides guidance to AI Agents (OpenCode, Claude, Gemini, etc.) when working with code in this repository.

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

## Key Scripts and Their Functions

### Core Scripts

**add_product.py** - Main script to scrape and add/update individual products
```bash
python3 add_product.py <product_name>
```
- Searches shop.dransay.com for product
- Scrapes product details (name, URL, THC%, genetics, ratings, etc.)
- Extracts cheapest prices from two categories: "top" and "all" pharmacies
- Stores complete product data with all attributes
- Creates historical price entries

**update_prices.py** - Bulk update script for all products
```bash
python3 update_prices.py
```
- Fetches all products from database
- Re-scrapes prices for each product
- Updates price history while preserving existing data

**add_products_batch.py** - Batch script to add multiple products
```bash
python3 add_products_batch.py example_products.txt
```
- Reads product names from file (one per line)
- Processes each product with add_product.py logic

**generate_overview.py** - Creates product overview markdown
```bash
python3 generate_overview.py
```
- Generates SORTEN_ÜBERSICHT.md from database
- Creates best-of lists and complete product tables
- Includes direct links to shop.dransay.com

### Data Collection Process

The add_product.py script uses a comprehensive scraping approach:

1. **Search for Product** - Searches shop.dransay.com for the product name
2. **Extract Product Details**:
   - Product name from `<h1>` element
   - THC%, CBD% percentages
   - Genetics (Indica/Sativa/Hybrid)
   - Rating and review count
   - Producer information
   - Terpene profile
   - Effects and therapeutic uses
   - Stock level and irradiation status
3. **Price Extraction (Two Categories)**:
   - **Top Pharmacies** (`vendorId=top`): Cheapest among curated top pharmacies
   - **All Pharmacies** (`vendorId=all`): Cheapest across all available pharmacies
4. **Database Storage**:
   - Complete product record with all attributes
   - Pharmacy records (created if needed)
   - Two price entries per scrape (top + all categories)
   - Historical price tracking with timestamps

## Dependencies and Setup

**Required Python packages:**
```bash
pip3 install playwright mypy
python3 -m playwright install chromium
```

**Database setup:**
```bash
sqlite3 WeedDB.db < schema.sql
```

## Type Safety

All Python code uses **strict type annotations**:
- Run type checker: `python3 -m mypy *.py --strict`
- Ensures correct function usage and prevents runtime errors

## Common Tasks

### Add New Product
```bash
python3 add_product.py 'product_name'
```

### Update All Products
```bash
python3 update_prices.py
```

### Generate Overview
```bash
python3 generate_overview.py
```

### Batch Add Products
```bash
python3 add_products_batch.py example_products.txt
```

## Database Queries

**View all products with enhanced data:**
```sql
SELECT p.name, p.genetics, p.thc_percent || '%' as THC,
       p.rating || '★' as Rating, p.review_count as Reviews,
       pr.name as Producer
FROM products p
LEFT JOIN producers pr ON p.producer_id = pr.id
ORDER BY p.rating DESC;
```

**Current prices by category:**
```sql
SELECT p.name, pr.category, pr.price_per_g, ph.name as pharmacy
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE pr.timestamp = (SELECT MAX(timestamp) FROM prices 
                      WHERE product_id = p.id AND category = pr.category)
ORDER BY p.name, pr.category;
```

## File Structure

- `schema.sql` - Database schema definition
- `add_product.py` - Individual product scraping/addition
- `update_prices.py` - Bulk price updates
- `add_products_batch.py` - Batch product addition
- `generate_overview.py` - Overview markdown generation
- `WeedDB.db` - SQLite database (auto-created)
- `example_products.txt` - Sample product list for batch processing
- `SORTEN_ÜBERSICHT.md` - Generated product overview (auto-updated)

## Important Notes

- **Price History**: Never delete old prices, always INSERT new entries
- **Product ID**: Uses shop.dransay.com's product ID as PRIMARY KEY
- **Category System**: Two price categories - "top" and "all" pharmacies
- **WebFetch Permission**: Pre-configured for shop.dransay.com in `.claude/settings.local.json`
- **Type Safety**: All scripts must pass `mypy --strict` checking
- **Overview Generation**: Run `generate_overview.py` after database changes to update SORTEN_ÜBERSICHT.md
- **CRITICAL**: The overview is only as current as the last database update and script execution!

## Troubleshooting

**If Playwright fails:**
- Ensure Chromium is installed: `python3 -m playwright install chromium`
- Check internet connection to shop.dransay.com

**If product not found:**
- Verify product name matches shop.dransay.com
- Try shorter/more generic search terms

**If scraping fails:**
- Check if shop.dransay.com changed their page structure
- Update selectors in add_product.py accordingly
- Use debug_scrape.py for page structure inspection