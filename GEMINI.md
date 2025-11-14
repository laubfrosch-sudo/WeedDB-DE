# WeedDB Project

## Project Overview

**Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This project consists of a set of Python scripts designed to scrape, store, and manage data for cannabis products from the website `shop.dransay.com`. It uses a SQLite database (`WeedDB.db`) to persist the information.

The core of the project is a web scraper built with the `playwright` library. It extracts detailed product information, including THC/CBD percentages, genetics, producer, user ratings, and pricing from various pharmacies.

**Key Technologies:**
*   **Language:** Python 3
*   **Database:** SQLite
*   **Web Scraping:** Playwright

**Architecture:**
*   `WeedDB.db`: A SQLite database that stores all product information. The schema is defined in `schema.sql` and includes tables for products, producers, prices, terpenes, and effects, along with performant views for querying current prices.
*   `add_product.py`: The core script for scraping a single product's URL and inserting/updating its data in the database.
*   `update_all_products.py`: A utility script that fetches all product URLs from the database and runs `add_product.py` for each one, effectively refreshing the entire dataset. It uses concurrency to speed up the process.
*   `add_batch_products.py`: A script to add multiple products from a text file of URLs.

## Building and Running

This is a Python scripting project and does not have a traditional build step. The main requirements are Python 3 and the `playwright` library.

### 1. Setup

First, install the necessary Python library and browser binaries for Playwright:

```bash
# Install the playwright library
pip install playwright

# Download the necessary browser binaries
python3 -m playwright install
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

*   **Database Schema:** The database schema is managed in the `schema.sql` file. Any changes to the data structure should be reflected there.
*   **Data Scraping:** The scraping logic in `add_product.py` relies on the specific HTML structure and content of the target website. Changes to the website may require updates to the selectors and data extraction logic in the `scrape_product_data` function.
*   **Type Hinting:** The project uses Python type hints. It is recommended to use a static type checker like `mypy` during development to ensure type safety.

---

## Dynamische Übersichtsdateien

**Wichtiger Hinweis:** Die Datei `SORTEN_ÜBERSICHT.md` wird automatisch aus der `WeedDB.db` Datenbank generiert. Jegliche Änderungen an der Datenbank (Hinzufügen, Ändern oder Löschen von Einträgen) führen dazu, dass sich der Inhalt dieser Markdown-Datei bei der nächsten Aktualisierung ebenfalls ändert. Sowohl die "Bestenliste" als auch die Haupttabelle enthalten jetzt direkte Links zu den jeweiligen Produktseiten.