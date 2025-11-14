# 💾 WeedDB Data

Dieser Ordner enthält alle Datenbankdateien und Beispieldateien des WeedDB-Projekts.

## 📁 Inhalt

### Datenbank
- `WeedDB.db` - SQLite-Datenbank mit allen Produkt- und Preisdaten
- `schema.sql` - Datenbankschema-Definition

### Beispieldateien
- `example_products.txt` - Beispiel-Produktliste für Batch-Imports
- `new_products.txt` - Liste neu hinzugefügter Produkte
- `test_batch.txt` - Testdaten für Batch-Operationen

### Preis-Historie
- `price_history/` - JSON-Exporte der Preis-Historie
  - `{YYYY-MM-DD}.json` - Tägliche Preis-Snapshots
  - `complete_history.json` - Vollständige Historie

## 🔧 Verwendung

### Datenbank-Operationen
```bash
# Datenbank inspizieren
sqlite3 WeedDB.db ".tables"
sqlite3 WeedDB.db "SELECT name FROM products;"

# Schema anzeigen
cat schema.sql
```

### Preis-Historie
```bash
# Aktuelle Preise exportieren
python3 scripts/export_price_history.py

# Historie importieren
python3 scripts/import_price_history.py price_history/2025-11-14.json
```

## ⚠️ Wichtig

- **Nicht die Datenbank direkt bearbeiten** - verwende die Scripts
- **Regelmäßige Backups** der `WeedDB.db` erstellen
- **Preis-Historie** wird automatisch archiviert

## 🏷️ Tags

#data #database #sqlite #price-history
