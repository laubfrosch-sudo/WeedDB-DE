---
created: 2024-04-01
updated: 2025-11-15
version: 0.1.2
author: laubfrosch-sudo
status: alpha
description: Universal guidelines for all AI assistants working with WeedDB
related_docs: [CLAUDE.md, GEMINI.md, KI_LÖSUNGSANSATZ.md]
---

# AGENTS.md - WeedDB Development Guidelines

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB-DE](https://github.com/laubfrosch-sudo/WeedDB-DE)

**IMPORTANT FOR AI ASSISTANTS:** When editing this file (AGENTS.md), always synchronize the corresponding instructions in GEMINI.md and CLAUDE.md. All files must remain consistent regarding schema definitions, dependencies, and core functionality.

**🚨 RELEASE CHECKLIST:** Before any git push or release, ALWAYS consult and complete `RELEASE_CHECKLIST.md`. This ensures code quality, security, and anonymity standards are maintained.

**🎯 RELEASE STATUS:** WeedDB v0.1.1 is ready for release! All tests passed, documentation updated, and cleanup completed.

## 🔧 Development Commands

### Build & Lint
```bash
# Type checking (strict mode)
python3 -m mypy scripts/*.py --ignore-missing-imports

# Syntax validation
python3 -m py_compile scripts/*.py

# Import validation
python3 -c "import scripts.add_product; import scripts.logger"
```

### Testing
```bash
# Run specific script test
python3 scripts/add_product.py "Test Product"  # Integration test

# Test parallel processing
python3 scripts/add_products_parallel.py test_batch.txt --concurrency 2 --yes

# Validate database integrity
sqlite3 data/WeedDB.db "PRAGMA integrity_check;"

# Test cache functionality
python3 -c "import asyncio; from scripts.cache_manager import get_cache_manager; print(asyncio.run(get_cache_manager().get_stats()))"
```

## 📋 Code Style Guidelines

### Imports & Structure
- **Absolute imports only**: `from scripts.logger import get_logger`
- **Group imports**: Standard library, third-party, local modules
- **No wildcard imports**: Explicit imports preferred
- **Type hints required**: All functions/methods must have type annotations

### Naming Conventions
- **Functions**: `snake_case` (e.g., `process_batch_data()`)
- **Classes**: `PascalCase` (e.g., `BatchProcessor`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`)
- **Variables**: `snake_case` (e.g., `product_data`)

### Error Handling
- **Try-except blocks**: Always catch specific exceptions
- **Logging**: Use structured logging with context
- **Graceful degradation**: Continue operation when possible
- **No bare except**: Always specify exception types

### Formatting & Types
- **Line length**: Max 100 characters
- **Docstrings**: Google-style for all public functions
- **Type hints**: Strict typing with `mypy --strict` compatibility
- **Async/await**: Use asyncio for I/O operations

### Database & Security
- **Parameterized queries**: Never use string formatting for SQL
- **Input validation**: Validate all user inputs
- **No secrets**: Never hardcode credentials or API keys
- **Anonymity**: No personal data in code or commits



**OBSIDIAN OPTIMIZATION:** This repository is fully optimized for Obsidian.md knowledge management. The folder structure, cross-links, and documentation are designed for seamless Obsidian integration.

This file provides guidance to AI Agents (OpenCode, Claude, Gemini, etc.) when working with code in this repository.

## Obsidian Integration

This repository is fully optimized for [Obsidian.md](https://obsidian.md/) knowledge management:

### Folder Structure for AI Agents
```
WeedDB/
├── 🔗 *.md (symbolic links to docs/)
├── 📁 .obsidian/ - Obsidian configuration
├── 📁 data/ - Database and price history
├── 📁 docs/ - Documentation (Obsidian vault)
│   ├── _README.md - Main navigation hub
│   ├── ai-assistants/ - AI-specific docs
│   ├── user-guides/ - User documentation
│   ├── development/ - Technical docs
│   ├── generated/ - Auto-generated reports
│   ├── assets/ - Media files
│   ├── templates/ - Reusable snippets
│   └── notes/ - Personal notes
├── 📁 scripts/ - Python automation
└── 📁 CHANGELOG/ - Version history
```

### Working with Obsidian Structure
- **Navigation**: Use `_README.md` files in each folder for orientation
- **Cross-links**: Follow `[[link]]` syntax for document connections
- **Tags**: Search using `#tag` system for categorization
- **Templates**: Use `docs/templates/` for consistent documentation
- **Assets**: Store media in `docs/assets/` with subfolders

### AI Agent Guidelines
1. **Respect Structure**: Maintain the logical folder organization
2. **Use Templates**: Leverage existing templates for new documentation
3. **Cross-link**: Create meaningful connections between related documents
4. **Tag Appropriately**: Use relevant tags for discoverability
5. **Update Navigation**: Keep `_README.md` files current

## Project Overview

WeedDB is a cannabis product database that tracks medical cannabis strains and their prices across multiple pharmacies (Versandapotheken) in Germany. The primary data source is shop.dransay.com, which aggregates cannabis product listings from various licensed pharmacies.

**New:**
- Enhanced batch processing with timeout protection
- Automatic data correction for missing producers
- Extended producer recognition (24+ known manufacturers)
- Robust price extraction with multiple fallback methods

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
python3 add_products_batch.py example_products.txt --yes
```
- Reads product names from file (one per line)
- Processes each product individually with 3-second pauses to avoid timeouts
- Use --yes flag to skip confirmation prompt

**fix_producers.py** - Auto-recovery script for missing producer data
```bash
python3 fix_producers.py
```
- Automatically scans and corrects missing producer information
- Re-scrapes product pages to identify manufacturers
- Updates database with corrected producer relationships

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

## Type Safety

All Python code uses **strict type annotations**:
- Run type checker: `python3 -m mypy *.py --strict`
- Ensures correct function usage and prevents runtime errors

## Common Tasks

**⚠️ WICHTIG:** Bevor neue Sorten von shop.dransay.com gescraped werden, MUSS die Datenbank überprüft werden um zu vermeiden, dass bereits vorhandene Produkte doppelt hinzugefügt werden!

```bash
# Überprüfe vorhandene Produkte
sqlite3 data/WeedDB.db "SELECT name FROM products ORDER BY name;"

# Oder zähle Produkte
sqlite3 data/WeedDB.db "SELECT COUNT(*) FROM products;"
```

### Add New Product
```bash
python3 scripts/add_product.py 'product_name'
```

### Parallel Batch Add Products (⚡ NEU - 3x schneller!)
```bash
# Parallele Verarbeitung mit konfigurierbarer Concurrency
python3 scripts/add_products_parallel.py products.txt --concurrency 5 --yes

# Optionen:
# --concurrency N    : Max parallele Verbindungen (default: 3)
# --timeout N        : Timeout pro Produkt in Sekunden (default: 120)
# --yes              : Bestätigung überspringen
# --output FILE      : Detaillierten Report speichern
```

### Sequential Batch Add Products (Legacy)
```bash
python3 scripts/add_products_batch.py example_products.txt
```

### Update All Products
```bash
python3 scripts/update_prices.py
```

**New Option:**
*   `Automatically correct missing manufacturer data.`

### Generate Overview
```bash
python3 scripts/generate_overview.py
```

### Find New Products (⚡ NEU)
```bash
# Finde Produkte auf shop.dransay.com die noch nicht in DB sind
python3 scripts/find_new_products.py

# Mit Filtern:
python3 scripts/find_new_products.py --vendorId top --search "Haze"
```

### Automated Scheduling (⚡ NEU)
```bash
# Cron-Scripts erstellen
python3 scripts/scheduler.py --create-cron-scripts

# Manuelle Tasks:
python3 scripts/scheduler.py daily_update      # Tägliche Preis-Updates
python3 scripts/scheduler.py weekly_overview   # Wöchentliche Übersicht
python3 scripts/scheduler.py monthly_cleanup   # Monatliche Wartung
```

### Cache Management (⚡ NEU)
```bash
# Cache-Statistiken anzeigen
python3 -c "import asyncio; from scripts.cache_manager import get_cache_manager; cache = get_cache_manager(); stats = asyncio.run(cache.get_stats()); print(f'Entries: {stats[\"total_entries\"]}, Expired: {stats[\"expired_entries\"]}')"

# Cache leeren
python3 -c "import asyncio; from scripts.cache_manager import get_cache_manager; cache = get_cache_manager(); asyncio.run(cache.clear_expired())"
```

### Logging & Monitoring (⚡ NEU)
```bash
# Performance-Statistiken anzeigen
python3 -c "from scripts.logger import get_performance_stats; stats = get_performance_stats('add_product', hours=24); print(f'Avg duration: {stats[\"avg_duration_ms\"]:.1f}ms, Success rate: {(stats[\"successful_operations\"]/max(1,stats[\"total_operations\"]))*100:.1f}%')"

# Logs verfolgen
tail -f data/logs/add_product.log
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

## File Structure (Obsidian-Optimized)

**Root Level (Symbolic Links):**
- `README.md` → `docs/README.md` - Main project documentation
- `AGENTS.md` → `docs/ai-assistants/AGENTS.md` - AI assistant guidelines
- `CLAUDE.md` → `docs/ai-assistants/CLAUDE.md` - Claude-specific docs
- `GEMINI.md` → `docs/ai-assistants/GEMINI.md` - Gemini-specific docs
- `SORTEN_ÜBERSICHT.md` → `docs/generated/SORTEN_ÜBERSICHT.md` - Product overview

**Core Folders:**
- `data/` - Database and price history (see `data/_README.md`)
- `docs/` - Complete documentation vault (see `docs/_README.md`)
- `scripts/` - Python automation scripts (see `scripts/_README.md`)
- `CHANGELOG/` - Version history (see `CHANGELOG/_README.md`)
- `.obsidian/` - Obsidian workspace configuration

**Key Files:**
- `data/schema.sql` - Database schema definition
- `scripts/add_product.py` - Individual product scraping/addition
- `scripts/update_prices.py` - Bulk price updates
- `scripts/add_products_batch.py` - Batch product addition
- `scripts/generate_overview.py` - Overview markdown generation
- `data/WeedDB.db` - SQLite database (auto-created)
- `data/example_products.txt` - Sample product list for batch processing

## Important Notes

- **Price History**: Never delete old prices, always INSERT new entries
- **Product ID**: Uses shop.dransay.com's product ID as PRIMARY KEY
- **Category System**: Two price categories - "top" and "all" pharmacies
- **Obsidian Integration**: Repository optimized for Obsidian.md with `_README.md` navigation files
- **WebFetch Permission**: Pre-configured for shop.dransay.com in `.claude/settings.local.json`
- **Type Safety**: All scripts must pass `mypy --strict` checking
- **Overview Generation**: Run `generate_overview.py` after database changes to update SORTEN_ÜBERSICHT.md
- **CRITICAL**: The overview is only as current as the last database update and script execution!

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