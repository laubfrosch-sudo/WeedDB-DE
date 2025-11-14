# WeedDB Project

**IMPORTANT FOR AI ASSISTANTS:** When editing this file (GEMINI.md), always synchronize the corresponding instructions in CLAUDE.md. Both files must remain consistent regarding schema definitions, dependencies, and core functionality.

## Project Overview

**Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This project consists of a set of Python scripts designed to scrape, store, and manage data for cannabis products from the website `shop.dransay.com`. It uses a SQLite database (`WeedDB.db`) to persist the information.

The core of the project is a web scraper built with the `playwright` library. It extracts detailed product information, including THC/CBD percentages, genetics, producer, user ratings, terpenes, effects, therapeutic uses, and pricing from ALL pharmacies displayed on the product page.

**Key Technologies:**
*   **Language:** Python 3
*   **Database:** SQLite
*   **Web Scraping:** Playwright

**Architecture:**
*   `WeedDB.db`: A SQLite database that stores all product information. The schema is defined in `schema.sql` and includes tables for products, producers, prices, terpenes, and effects, along with performant views for querying current prices.
*   `add_product.py`: The core script for scraping a single product's URL and inserting/updating its data in the database. **Now extracts prices from ALL pharmacies** on the page (using `vendorId=all`), not just the cheapest one.
*   `update_all_products.py`: A utility script that fetches all product URLs from the database and runs `add_product.py` for each one, effectively refreshing the entire dataset. It uses concurrency to speed up the process.
*   `add_batch_products.py`: A script to add multiple products from a text file of URLs.

**Multi-Pharmacy Price Tracking:**
*   The scraper uses `vendorId=all` in the URL to display ALL pharmacies offering a product
*   Multiple scraping strategies are employed to find pharmacy listings (vendor cards, price elements with context)
*   ALL pharmacy prices are stored in the `prices` table with timestamps
*   This enables comprehensive price comparison across the German cannabis pharmacy market
*   Historical pricing is preserved - each scrape adds new entries for all pharmacies found
*   New database views provide multi-pharmacy analytics:
    - `product_pharmacy_prices` - All prices per product with ranking
    - `product_price_stats` - Price statistics (min/max/avg/spread/pharmacy count)
    - `pharmacy_price_ranking` - Pharmacy ranking by price competitiveness

**Query Examples:**
See `QUERY_EXAMPLES.md` for comprehensive SQL query examples including:
*   Multi-pharmacy price comparisons
*   Product search by terpenes, effects, and therapeutic uses
*   Statistics and analytics
*   Advanced queries for price trends and pharmacy competition

## Building and Running

This is a Python scripting project and does not have a traditional build step. The main requirements are Python 3 and the `playwright` library.

### 1. Setup

First, install the necessary Python libraries and browser binaries:

```bash
# Install playwright and mypy (static type checker)
pip3 install playwright mypy

# Download the necessary browser binaries (Chromium)
python3 -m playwright install chromium
```

### 2. Key Scripts

The primary way to interact with the project is by running the Python scripts.

**To add or update a single product:**
Provide the product URL from `shop.dransay.com`.

```bash
python3 add_product.py "<product_url>"
```

**To update all products already in the database:**
This script will iterate through all existing products and re-scrape their data.

```bash
python3 update_all_products.py
```

**To add a batch of new products:**
Create a text file (e.g., `new_products.txt`) with one product URL per line and run:

```bash
python3 add_batch_products.py new_products.txt
```

## Development Conventions

*   **Database Schema:** The database schema is managed in the `schema.sql` file (SQLite, 3rd Normal Form). Any changes to the data structure should be reflected there. Key constraints:
    - `product_effects.strength`: INTEGER CHECK(strength BETWEEN 0 AND 4)
    - `product_therapeutic_uses.strength`: INTEGER CHECK(strength BETWEEN 0 AND 4)
*   **Data Scraping:** The scraping logic in `add_product.py` relies on the specific HTML structure and content of the target website. Changes to the website may require updates to the selectors and data extraction logic in the `scrape_product_data` function.
*   **Type Safety:** The project uses strict Python type annotations (Python 3.9+ compatible). Run `python3 -m mypy *.py --strict` to verify type correctness before committing changes.

---

## Dynamische Übersichtsdateien

**Wichtiger Hinweis:** Die Datei `SORTEN_ÜBERSICHT.md` wird automatisch aus der `WeedDB.db` Datenbank generiert. Jegliche Änderungen an der Datenbank (Hinzufügen, Ändern oder Löschen von Einträgen) führen dazu, dass sich der Inhalt dieser Markdown-Datei bei der nächsten Aktualisierung ebenfalls ändert. Sowohl die "Bestenliste" als auch die Haupttabelle enthalten jetzt direkte Links zu den jeweiligen Produktseiten.