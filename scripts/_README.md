# 🔧 WeedDB Scripts

Dieser Ordner enthält alle Python-Scripts für die Automatisierung und Verwaltung der WeedDB.

## 📁 Scripts-Übersicht

### Kernfunktionalität
- `add_product.py` - Einzelne Produkte hinzufügen und aktualisieren
- `add_products_batch.py` - Mehrere Produkte sequentiell in Batches hinzufügen
- `add_products_parallel.py` - **🚀 NEU**: Mehrere Produkte parallel verarbeiten (3x schneller!)
- `update_prices.py` - Alle Produktpreise aktualisieren
- `find_new_products.py` - **🔍 NEU**: Neue Produkte auf shop.dransay.com finden

### Automatisierung & Monitoring
- `scheduler.py` - **⏰ NEU**: Automatisierte Tasks (daily/weekly/monthly)
- `update_status_dashboard.py` - **📊 NEU**: Obsidian Status-Dashboard aktualisieren
- `cache_manager.py` - **🗄️ NEU**: Intelligentes Caching-System
- `error_handler.py` - **🛡️ NEU**: Robuste Fehlerbehandlung mit Retry
- `logger.py` - **📋 NEU**: Umfassendes Logging-System

### Automatisierung & Scheduling
- `scheduler.py` - **⏰ NEU**: Automatisierte Tasks (daily/weekly/monthly)
- `update_status_dashboard.py` - **📊 NEU**: Obsidian Status-Dashboard aktualisieren

### Preis-Historie
- `export_price_history.py` - Preisdaten als JSON exportieren
- `import_price_history.py` - Preisdaten aus JSON importieren
- `archive_prices.py` - Automatische Preis-Archivierung

### Hilfs-Scripts
- `fix_producers.py` - Fehlende Hersteller korrigieren
- `generate_overview.py` - SORTEN_ÜBERSICHT.md generieren

### Infrastruktur (NEU)
- `logger.py` - **📋 NEU**: Umfassendes Logging-System
- `error_handler.py` - **🛡️ NEU**: Robuste Fehlerbehandlung mit Retry
- `cache_manager.py` - **🗄️ NEU**: Intelligentes Caching-System

### Archive/Backups
- `add_product.py.backup` - Backup der ursprünglichen Version
- `retry_mechanism.py` - Retry-Logik (experimentell)

## 🚀 Häufige Befehle

### Produkte verwalten
```bash
# Einzelnes Produkt hinzufügen
python3 scripts/add_product.py "Sourdough"

# Mehrere Produkte sequentiell hinzufügen
python3 scripts/add_products_batch.py data/example_products.txt --yes

# Mehrere Produkte PARALLEL hinzufügen (3x schneller!)
python3 scripts/add_products_parallel.py data/example_products.txt --concurrency 5 --yes

# Neue Produkte auf shop.dransay.com finden
python3 scripts/find_new_products.py

# Alle Preise aktualisieren
python3 scripts/update_prices.py
```

### Automatisierte Tasks
```bash
# Cron-Scripts für automatische Ausführung erstellen
python3 scripts/scheduler.py --create-cron-scripts

# Manuelle Tasks ausführen
python3 scripts/scheduler.py daily_update      # Tägliche Preis-Updates
python3 scripts/scheduler.py weekly_overview   # Wöchentliche Übersicht
python3 scripts/scheduler.py monthly_cleanup   # Monatliche Wartung
```

### Monitoring & Status
```bash
# Obsidian Status-Dashboard aktualisieren
python3 scripts/update_status_dashboard.py

# Cache-Statistiken anzeigen
python3 -c "import asyncio; from scripts.cache_manager import get_cache_manager; print(asyncio.run(get_cache_manager().get_stats()))"

# Performance-Metriken prüfen
python3 -c "from scripts.logger import get_performance_stats; print(get_performance_stats('add_product', hours=24))"
```

### Preis-Historie
```bash
# Aktuelle Preise exportieren
python3 scripts/export_price_history.py

# Historie archivieren
python3 scripts/archive_prices.py
```

### Wartung
```bash
# Fehlende Hersteller korrigieren
python3 scripts/fix_producers.py

# Übersicht generieren
python3 scripts/generate_overview.py
```

## ⚙️ Konfiguration

Die Scripts verwenden relative Pfade zur Datenbank:
- Datenbank: `../data/WeedDB.db`
- Preis-Historie: `../data/price_history/`

## 🐛 Fehlerbehebung

Bei Problemen:
1. Überprüfe Python-Version (3.9+)
2. Stelle sicher, dass Playwright installiert ist
3. Prüfe Datenbank-Verbindungen
4. Schaue in Logs: `../data/price_history/export_errors.json`

## 🏷️ Tags

#scripts #python #automation #maintenance
