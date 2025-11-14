# WeedDB Project

**IMPORTANT FOR AI ASSISTANTS:** When editing this file (GEMINI.md), always synchronize the corresponding instructions in CLAUDE.md. Both files must remain consistent regarding schema definitions, dependencies, and core functionality.

## Project Overview

**Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This project consists of a set of Python scripts designed to scrape, store, and manage data for cannabis products from the website `shop.dransay.com`. It uses a SQLite database (`WeedDB.db`) to persist the information.

The core of the project is a web scraper built with the `playwright` library. It extracts product information and tracks the cheapest pharmacy price in two categories: "top pharmacies" and "all pharmacies".

**Key Technologies:**
*   **Language:** Python 3
*   **Database:** SQLite
*   **Web Scraping:** Playwright

**Architecture:**
*   `WeedDB.db`: A SQLite database that stores product information and price history. The schema is defined in `schema.sql`.
*   `add_product.py`: The core script that searches for a product by name and extracts the cheapest price for two categories:
    - **Top Pharmacies** (`vendorId=top`) - Curated "top" pharmacies
    - **All Pharmacies** (`vendorId=all`) - All available pharmacies
*   Each scrape creates 2 price entries (one per category) with the pharmacy name and price

**Price Tracking Strategy:**
*   **Minimal Storage:** Only stores the cheapest price for each category
*   **Real Pharmacy Names:** Actual pharmacy names (e.g., "Paracelsus Apotheke") are stored
*   **Leverages Website Logic:** shop.dransay.com automatically displays the cheapest pharmacy based on the `vendorId` parameter
*   **Historical Tracking:** Re-running the script adds new timestamped entries for price trend analysis
*   **Category-based:** Prices table includes a `category` column ("top" or "all")

**Query Examples:**
See `QUERY_EXAMPLES.md` for comprehensive SQL query examples including:
*   Multi-pharmacy price comparisons
*   Product search by terpenes, effects, and therapeutic uses
*   Statistics and analytics
*   Advanced queries for price trends and pharmacy competition

## Building and Running

This is a Python scripting project and does not have a traditional build step. The main requirements are Python 3 and `playwright` library.

### 1. Setup

First, install necessary Python libraries and browser binaries:

```bash
# Install playwright and mypy (static type checker)
pip3 install playwright mypy
python3 -m playwright install chromium

# Create database
sqlite3 WeedDB.db < schema.sql

# Add first product
python3 add_product.py 'sourdough'

# Download the necessary browser binaries (Chromium)
python3 -m playwright install chromium
```

### 2. Key Scripts

The primary way to interact with the project is by running the Python scripts.

**To add or update a single product:**
Provide the product name as it appears on `shop.dransay.com`.

```bash
python3 add_product.py '<product_name>'
```

**Examples:**
```bash
python3 add_product.py 'sourdough'
python3 add_product.py 'gelato'
python3 add_product.py 'wedding cake'
```

**Update all products:**
```bash
python3 update_prices.py
```

**Add multiple products from file:**
```bash
python3 add_products_batch.py example_products.txt
```

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

## Development Conventions

*   **Database Schema:** The database schema is managed in the `schema.sql` file (SQLite). Any changes to the data structure should be reflected there. Key schema elements:
    - `prices` table includes `category` column (either "top" or "all")
    - Each scrape creates 2 price entries: one for top pharmacies, one for all pharmacies
    - Price history is preserved with timestamps
*   **Data Scraping:** The scraping logic in `add_product.py` relies on the specific HTML structure and content of the target website. Changes to the website may require updates to the selectors and data extraction logic in the `scrape_product_data` function.
*   **Type Safety:** The project uses strict Python type annotations (Python 3.9+ compatible). Run `python3 -m mypy *.py --strict` to verify type correctness before committing changes.

---

## Dynamische Übersichtsdateien

**Wichtiger Hinweis:** Die Datei `SORTEN_ÜBERSICHT.md` wird mit dem Skript `generate_overview.py` aus der `WeedDB.db` Datenbank generiert. Nach dem Hinzufügen oder Aktualisieren von Produkten sollte das Skript ausgeführt werden:

```bash
python3 generate_overview.py
```

Das Skript erstellt eine sortierte Übersicht aller Produkte mit:
- Bestenliste (höchster THC, bester Preis, Community-Liebling, etc.)
- Vollständige Produkttabelle sortiert nach Bewertungsanzahl
- Direkte Links zu allen Produktseiten auf shop.dransay.com

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