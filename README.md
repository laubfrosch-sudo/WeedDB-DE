# WeedDB v1.4.0

A comprehensive cannabis product price tracking database for the German market. Scrapes and manages product data from `shop.dransay.com` with intelligent price comparison across pharmacy categories.

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

---

## 🌟 Features

- **🧠 Intelligent Price Tracking**: Automatically finds the cheapest pharmacy in two categories:
  - 🏆 **Top Pharmacies** - Curated selection of trusted pharmacies
  - 🌍 **All Pharmacies** - Complete market overview
- **🏥 Real Pharmacy Names**: Stores actual pharmacy names (e.g., "Paracelsus Apotheke")
- **📈 Historical Data**: Track price changes over time with full audit trail
- **💾 Optimized Storage**: Only 2 price entries per product per scrape
- **⚡ SQLite Database**: Fast, portable, zero-configuration
- **🔄 Batch Processing**: Reliable bulk operations with timeout protection
- **🔧 Auto-Recovery**: Automatic correction of missing data
- **📊 Smart Analytics**: Best-value calculations and market insights

---

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB
```

### 2. Install Dependencies
```bash
pip3 install playwright mypy
python3 -m playwright install chromium
```

### 3. Initialize Database
```bash
sqlite3 WeedDB.db < schema.sql
```

### 4. Add Your First Product
```bash
python3 add_product.py 'sourdough'
```

**Example Output:**
```
=== Scraping Top Pharmacies ===
🔍 Searching for 'sourdough' (top)
   ✅ Found product
   🌐 Loading product page (top)
   ✅ Product name: Sourdough
   ✅ Found genetics: Indica
   ✅ Found THC: 29.0%
   ✅ Found CBD: 1.0%
   ✅ Found rating: 4.0 (1832 reviews)
   ✅ Found producer: Aurora Cannabis
   ✅ Found country: Canada
   🔍 Method 0: Trying 'Buying from' section...
   📄 Found buying section
   💰 Sanvivo Cannabis Apotheke (=Senftenauer): €6.77/g

=== Scraping All Pharmacies ===
🔍 Searching for 'sourdough' (all)
   ✅ Found product
   🌐 Loading product page (all)
   💰 Paracelsus Apotheke: €5.69/g

============================================================
📋 Summary for: Sourdough
============================================================
   ID: 973
   URL: https://shop.dransay.com/product/sourdough-pedanios-291-srd-ca/973

💰 Cheapest Prices:
   🏆 Top Pharmacies: €6.77/g
       → Sanvivo Cannabis Apotheke (=Senftenauer)
   🌍 All Pharmacies: €5.69/g
       → Paracelsus Apotheke
============================================================

✅ Successfully added 'Sourdough' to database with cheapest prices.
```

### 5. Query the Database
```bash
sqlite3 WeedDB.db "SELECT p.name, pr.price_per_g, pr.category, ph.name as pharmacy
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE p.name LIKE '%sourdough%'
ORDER BY pr.category, pr.price_per_g"
```

**Output:**
```
Sourdough|5.69|all|Paracelsus Apotheke
Sourdough|6.77|top|Sanvivo Cannabis Apotheke (=Senftenauer)
```

---

## 📖 Documentation

- **`CLAUDE.md`** - Complete technical documentation and architecture (for Claude AI)
- **`GEMINI.md`** - Technical documentation (for Gemini AI)
- **`AGENTS.md`** - Comprehensive AI assistant guidelines
- **`QUERY_EXAMPLES.md`** - SQL query examples for price analysis (60+ examples)
- **`INSTRUCTIONS.md`** (English) / **`ANLEITUNG.md`** (Deutsch) - Usage instructions
- **`schema.sql`** - Database schema definition
- **`SORTEN_ÜBERSICHT.md`** - Auto-generated product overview (run `generate_overview.py`)
- **`fix_producers.py`** - Auto-recovery script for missing producer data (v1.4.0)

---

## 💡 Usage Examples

### Add Multiple Products
```bash
python3 add_product.py 'gelato'
python3 add_product.py 'wedding cake'
python3 add_product.py 'amnesia haze'
```

### Update Existing Product (Refresh Prices)
Simply run the script again:
```bash
python3 add_product.py 'sourdough'
```
This adds new price entries with current timestamp while preserving historical data.

### Update All Products (Bulk Price Refresh)
```bash
python3 update_prices.py
```
This script:
- Fetches all products from the database
- Re-scrapes prices for each product with improved reliability
- Shows detailed progress with batch processing
- Provides comprehensive summary of successful/failed updates
- **New in v1.4.0**: Enhanced error handling and recovery

### Add Multiple Products from File (Recommended Method)
Create a text file with product names (one per line):
```bash
# Create products.txt
cat > products.txt << EOF
gelato
wedding cake
amnesia haze
EOF

# Run batch addition (processes in small batches of 2 to avoid timeouts)
python3 add_products_batch.py products.txt --yes
```
See `example_products.txt` for file format.

**Note**: The script automatically processes products in batches of 2 with pauses between batches to avoid timeouts and overwhelming the website.

### Generate Product Overview
After adding or updating products, generate the overview markdown file:
```bash
python3 generate_overview.py
```
This creates/updates `SORTEN_ÜBERSICHT.md` with:
- Best-of list (highest THC, best price, community favorite, etc.)
- Complete product table sorted by review count
- Direct links to all products on shop.dransay.com
- **New in v1.4.0**: Enhanced producer information and data completeness

### Fix Missing Data (New in v1.4.0)
Automatically correct missing producer information:
```bash
python3 fix_producers.py
```
This script:
- Scans products with missing producer data
- Re-scrapes product pages to find producer information
- Updates the database with corrected data
- Provides detailed progress reporting

### View All Products in Database
```bash
sqlite3 WeedDB.db "SELECT name, id FROM products ORDER BY name"
```

### Find Cheapest Products Overall
```bash
sqlite3 WeedDB.db "SELECT p.name, MIN(pr.price_per_g) as min_price, ph.name as pharmacy
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
GROUP BY p.id
ORDER BY min_price
LIMIT 10"
```

---

## 🛠️ How It Works

1. **Search**: Script searches shop.dransay.com for the product name
2. **Top Pharmacies**: Loads product page with `vendorId=top` and extracts cheapest pharmacy
3. **All Pharmacies**: Loads product page with `vendorId=all` and extracts cheapest pharmacy
4. **Database**: Stores 2 price entries (one per category) with pharmacy name, price, and timestamp

**Key Advantage**: The website automatically shows the cheapest pharmacy based on the `vendorId` parameter, so we don't need to parse all listings!

---

## 📊 Database Schema

**Complete 3NF Schema** (defined in `schema.sql`) with enhanced data integrity:

```sql
products (
    id INTEGER PRIMARY KEY,        -- Product ID from shop.dransay.com
    name TEXT NOT NULL,            -- Product name
    variant TEXT,                  -- Full variant descriptor
    genetics TEXT,                 -- Indica/Sativa/Hybrid
    thc_percent REAL,             -- THC percentage
    cbd_percent REAL,             -- CBD percentage
    producer_id INTEGER,          -- Foreign key to producers (enhanced in v1.4.0)
    stock_level INTEGER,          -- Current stock units
    rating REAL,                  -- User rating (e.g., 4.1)
    review_count INTEGER,         -- Number of reviews
    irradiation TEXT,             -- Yes/No
    country TEXT,                 -- Country of origin (added in v1.3.0)
    effects TEXT,                 -- Reported effects (added in v1.3.0)
    complaints TEXT,              -- Medical complaints (added in v1.3.0)
    url TEXT UNIQUE,              -- Product URL
    created_at DATETIME,
    last_updated DATETIME,
    FOREIGN KEY (producer_id) REFERENCES producers(id)
)

producers (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,     -- Producer name (24+ known producers in v1.4.0)
    origin TEXT                   -- Country of origin
)

pharmacies (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,     -- e.g., "Paracelsus Apotheke"
    location TEXT
)

prices (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    pharmacy_id INTEGER NOT NULL,
    price_per_g REAL NOT NULL,
    category TEXT CHECK(category IN ('top', 'all')),  -- Category
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id)
)
```

---

## 🔧 Requirements

- **Python 3.9+**
- **SQLite3**
- **Playwright** (for web scraping)
- **Internet connection** (to access shop.dransay.com)

---

## 📝 License

This is a personal project for educational purposes. Please respect the terms of service of shop.dransay.com when scraping.

---

---

# WeedDB Projekt

Eine Cannabis-Produkt-Preisdatenbank für den deutschen Markt. Scrapt und verwaltet Produktdaten von `shop.dransay.com` mit intelligentem Preisvergleich über Apotheken-Kategorien.

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

---

## 🌟 Funktionen

- **Intelligente Preisverfolgung**: Findet automatisch die günstigste Apotheke in zwei Kategorien:
  - 🏆 **Top-Apotheken** - Kuratierte Auswahl vertrauenswürdiger Apotheken
  - 🌍 **Alle Apotheken** - Vollständige Marktübersicht
- **Echte Apothekennamen**: Speichert tatsächliche Apothekennamen (z.B. "Paracelsus Apotheke")
- **Historische Daten**: Verfolge Preisänderungen über die Zeit
- **Minimaler Speicherplatz**: Nur 2 Preiseinträge pro Produkt pro Scrape
- **SQLite Datenbank**: Schnell, portabel, ohne Konfiguration

---

## Schnellstart

### 1. Repository klonen
```bash
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB
```

### 2. Abhängigkeiten installieren
```bash
pip3 install playwright mypy
python3 -m playwright install chromium
```

### 3. Datenbank initialisieren
```bash
sqlite3 WeedDB.db < schema.sql
```

### 4. Erstes Produkt hinzufügen
```bash
python3 add_product.py 'sourdough'
```

### 5. Datenbank abfragen
```bash
sqlite3 WeedDB.db "SELECT p.name, pr.price_per_g, pr.category, ph.name as apotheke
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE p.name LIKE '%sourdough%'
ORDER BY pr.category, pr.price_per_g"
```

---

## 📖 Dokumentation

- **`CLAUDE.md`** - Vollständige technische Dokumentation
- **`QUERY_EXAMPLES.md`** - SQL-Abfrage-Beispiele für Preisanalysen
- **`ANLEITUNG.md`** (Deutsch) / **`INSTRUCTIONS.md`** (Englisch) - Nutzungsanleitung
- **`schema.sql`** - Datenbankschema-Definition

---

## 💡 Verwendungsbeispiele

### Mehrere Produkte hinzufügen
```bash
python3 add_product.py 'gelato'
python3 add_product.py 'wedding cake'
python3 add_product.py 'amnesia haze'
```

### Bestehendes Produkt aktualisieren (Preise aktualisieren)
Einfach das Skript erneut ausführen:
```bash
python3 add_product.py 'sourdough'
```
Dies fügt neue Preiseinträge mit aktuellem Zeitstempel hinzu und bewahrt historische Daten.

### Alle Produkte aktualisieren (Massen-Preisaktualisierung)
```bash
python3 update_prices.py
```
Dieses Skript:
- Lädt alle Produkte aus der Datenbank
- Scrapt Preise für jedes Produkt neu
- Zeigt Fortschritt (z.B. `[5/10]`)
- Bietet Zusammenfassung erfolgreicher/fehlgeschlagener Updates

### Mehrere Produkte aus Datei hinzufügen
Erstelle eine Textdatei mit Produktnamen (einer pro Zeile):
```bash
# products.txt erstellen
cat > products.txt << EOF
gelato
wedding cake
amnesia haze
EOF

# Massen-Hinzufügung ausführen
python3 add_products_batch.py products.txt
```
Siehe `example_products.txt` für das Dateiformat.

### Produktübersicht generieren
Nach dem Hinzufügen oder Aktualisieren von Produkten, generiere die Übersichtsdatei:
```bash
python3 generate_overview.py
```
Dies erstellt/aktualisiert `SORTEN_ÜBERSICHT.md` mit:
- Bestenliste (höchster THC, bester Preis, Community-Liebling, etc.)
- Vollständige Produkttabelle sortiert nach Bewertungsanzahl
- Direkte Links zu allen Produkten auf shop.dransay.com

---

## 🛠️ Funktionsweise

1. **Suche**: Skript sucht auf shop.dransay.com nach dem Produktnamen
2. **Top-Apotheken**: Lädt Produktseite mit `vendorId=top` und extrahiert günstigste Apotheke
3. **Alle Apotheken**: Lädt Produktseite mit `vendorId=all` und extrahiert günstigste Apotheke
4. **Datenbank**: Speichert 2 Preiseinträge (einen pro Kategorie) mit Apothekennamen, Preis und Zeitstempel

**Vorteil**: Die Website zeigt automatisch die günstigste Apotheke basierend auf dem `vendorId`-Parameter!

---

## 🔧 Anforderungen

- **Python 3.9+**
- **SQLite3**
- **Playwright** (für Web-Scraping)
- **Internetverbindung** (für Zugriff auf shop.dransay.com)
