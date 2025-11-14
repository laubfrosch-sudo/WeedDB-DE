# 🔧 WeedDB Scripts

Dieser Ordner enthält alle Python-Scripts für die Automatisierung und Verwaltung der WeedDB.

## 📁 Scripts-Übersicht

### Kernfunktionalität
- `add_product.py` - Einzelne Produkte hinzufügen und aktualisieren
- `add_products_batch.py` - Mehrere Produkte in Batches hinzufügen
- `update_prices.py` - Alle Produktpreise aktualisieren

### Preis-Historie
- `export_price_history.py` - Preisdaten als JSON exportieren
- `import_price_history.py` - Preisdaten aus JSON importieren
- `archive_prices.py` - Automatische Preis-Archivierung

### Hilfs-Scripts
- `fix_producers.py` - Fehlende Hersteller korrigieren
- `generate_overview.py` - SORTEN_ÜBERSICHT.md generieren

### Archive/Backups
- `add_product.py.backup` - Backup der ursprünglichen Version
- `retry_mechanism.py` - Retry-Logik (experimentell)

## 🚀 Häufige Befehle

### Produkte verwalten
```bash
# Einzelnes Produkt hinzufügen
python3 scripts/add_product.py "Sourdough"

# Mehrere Produkte hinzufügen
python3 scripts/add_products_batch.py data/example_products.txt --yes

# Alle Preise aktualisieren
python3 scripts/update_prices.py
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
