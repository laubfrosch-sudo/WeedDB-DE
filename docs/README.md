---
created: 2024-01-15
updated: 2025-11-15
version: 0.1.1
author: laubfrosch-sudo
status: alpha
description: WeedDB - Cannabis Preis-Tracking Datenbank für den deutschen medizinischen Markt
repository: https://github.com/laubfrosch-sudo/WeedDB-DE
---

<div align="center">
  <img src="docs/assets/icons/WeedDB.jpeg" alt="WeedDB Logo" width="300"/>
</div>

# 🌿 WeedDB v0.1.2 - Cannabis Preis-Tracking für Deutschland

**🎯 Finde die besten Cannabis-Preise in Deutschland automatisch!**

WeedDB ist ein intelligentes Preis-Tracking-System für medizinisches Cannabis in Deutschland. Es scrapt kontinuierlich `shop.dransay.com`, vergleicht Preise über 30+ Apotheken und liefert dir die besten Angebote mit nur einem Befehl.

**✨ Warum WeedDB?**
- **🚀 3x schnellere Preis-Updates** mit paralleler Verarbeitung
- **🗄️ 80% weniger Web-Requests** durch intelligentes Caching
- **🌐 Modernes Web-Interface** mit Live-Dashboard
- **📊 Umfassende Preis-Analysen** und Markt-Insights
- **⏰ Automatisierte Updates** via Cron-Jobs

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB-DE](https://github.com/laubfrosch-sudo/WeedDB-DE)

> *Logo created with Google Gemini*

---

## 🚨 Wichtige Hinweise

**Für Entwickler:** Vor jedem `git push` oder Release die [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) vollständig durchführen!

---

## ⚡ Was WeedDB kann

### 🎯 **Kernfunktionen**
- **🔍 Automatische Preis-Suche**: Finde die günstigsten Cannabis-Preise in Deutschland
- **📊 Intelligente Analyse**: Vergleicht Preise über 30+ zertifizierte Apotheken
- **📈 Preis-Historie**: Verfolge Preisänderungen über Monate
- **🏆 Beste Angebote**: "Top-Apotheken" vs. "Alle Apotheken" Kategorien

### 🚀 **Performance & Automation**
- **⚡ 3x schnellere Updates**: Parallele Verarbeitung mit konfigurierbarer Concurrency
- **🗄️ Smart Caching**: 80% weniger Web-Requests durch intelligente Zwischenspeicherung
- **⏰ Automatisierte Tasks**: Tägliche Preis-Updates via Cron-Jobs
- **📋 Vollständiges Monitoring**: Live-Status und Performance-Metriken

### 🌐 **Moderne Benutzeroberfläche**
- **💻 Web-Dashboard**: Responsive Interface mit Live-Metriken
- **🔄 Echtzeit-Updates**: Automatische Daten-Aktualisierung
- **📊 Erweiterte APIs**: Filtern, Sortieren, Paginierung
- **🔗 CLI ↔ Web Integration**: Nahtlose Zusammenarbeit

### 🛠️ **Entwickler-Features**
- **🐍 Python-basiert**: SQLite Datenbank, kein externer Server nötig
- **📝 Vollständige Logs**: Strukturiertes JSON-Logging
- **🔧 Obsidian Integration**: Knowledge-Management mit Live-Status
- **📚 Open Source**: Vollständig dokumentiert und erweiterbar

---

## 🚀 Schnellstart - In 3 Minuten einsatzbereit

### 1. Repository klonen & Setup
```bash
git clone https://github.com/laubfrosch-sudo/WeedDB-DE.git
cd WeedDB-DE
pip install -r requirements.txt
```

### 2. Erste Preis-Suche
```bash
# Einzelnes Produkt suchen
python3 scripts/add_product.py "Sourdough"

# Mehrere Produkte parallel verarbeiten
python3 scripts/add_products_parallel.py data/example_products.txt --concurrency 3 --yes
```

### 3. Web-Interface starten
```bash
cd web
python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
# Öffne: http://localhost:8000
```

### 4. Automatisierung einrichten
```bash
# Cron-Jobs für automatische Updates erstellen
python3 scripts/scheduler.py --create-cron-scripts
```

**🎉 Fertig!** Dein persönliches Cannabis-Preis-Tracking-System läuft.

---

## 💡 Warum WeedDB wählen?

| Problem | WeedDB Lösung |
|---------|---------------|
| **Teure Apotheken-Suche** | Automatische Preisvergleiche über 30+ Apotheken |
| **Preisänderungen verpassen** | Tägliche automatische Updates |
| **Keine Preis-Historie** | Vollständige Audit-Trail über Monate |
| **Manuelle Dateneingabe** | Vollautomatisches Scraping |
| **Keine Markt-Insights** | Umfassende Analysen und Trends |
| **Technische Komplexität** | Einfache CLI + Web-Interface |

**🌟 WeedDB spart dir Zeit und Geld bei der Cannabis-Beschaffung!**

---

## 📖 Detaillierte Anleitung

### 1. Repository klonen
```bash
git clone https://github.com/laubfrosch-sudo/WeedDB-DE.git
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

**Beispiel-Ausgabe:**
```
=== Scraping Top Pharmacies ===
🔍 Suche nach 'sourdough' (top)
   ✅ Produkt gefunden
   🌐 Lade Produktseite (top)
   ✅ Produktname: Sourdough
   ✅ Genetik gefunden: Indica
   ✅ THC gefunden: 29.0%
   ✅ CBD gefunden: 1.0%
   ✅ Bewertung gefunden: 4.0 (1832 Bewertungen)
   ✅ Hersteller gefunden: Aurora Cannabis
   ✅ Land gefunden: Canada
   🔍 Methode 0: Versuche 'Kaufen bei' Sektion...
   📄 'Kaufen bei' Sektion gefunden
   💰 Sanvivo Cannabis Apotheke (=Senftenauer): €6.77/g

=== Scraping All Pharmacies ===
🔍 Suche nach 'sourdough' (all)
   ✅ Produkt gefunden
   🌐 Lade Produktseite (all)
   💰 Paracelsus Apotheke: €5.69/g

============================================================
📋 Zusammenfassung für: Sourdough
============================================================
   ID: 973
   URL: https://shop.dransay.com/product/sourdough-pedanios-291-srd-ca/973

💰 Günstigste Preise:
   🏆 Top-Apotheken: €6.77/g
       → Sanvivo Cannabis Apotheke (=Senftenauer)
   🌍 Alle Apotheken: €5.69/g
       → Paracelsus Apotheke
============================================================

✅ 'Sourdough' erfolgreich mit günstigsten Preisen zur Datenbank hinzugefügt.
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

**Ausgabe:**
```
Sourdough|5.69|all|Paracelsus Apotheke
Sourdough|6.77|top|Sanvivo Cannabis Apotheke (=Senftenauer)
```

---

## 📖 Dokumentation

- **`docs/ai-assistants/CLAUDE.md`** - Vollständige technische Dokumentation und Architektur (für Claude AI)
- **`docs/ai-assistants/GEMINI.md`** - Technische Dokumentation (für Gemini AI)
- **`docs/ai-assistants/AGENTS.md`** - Umfassende Richtlinien für KI-Assistenten
- **`docs/QUERY_EXAMPLES.md`** - SQL-Abfrage-Beispiele für Preisanalysen (60+ Beispiele)
- **`INSTRUCTIONS.md`** (Englisch) / **`ANLEITUNG.md`** (Deutsch) - Nutzungsanleitung
- **`data/schema.sql`** - Datenbankschema-Definition
- **`docs/generated/SORTEN_ÜBERSICHT.md`** - Automatisch generierte Produktübersicht (führe `generate_overview.py` aus)
- **`scripts/fix_producers.py`** - Auto-Recovery-Skript für fehlende Herstellerdaten

---

## 💡 Verwendungsbeispiele

### Neue Produkte finden
Verwenden Sie das Skript `find_new_products.py`, um Produkte auf shop.dransay.com zu identifizieren, die noch nicht in Ihrer Datenbank sind. Dies hilft, doppelte Einträge zu vermeiden und gezielt neue Sorten hinzuzufügen.

```bash
# Alle neuen Produkte finden
python3 scripts/find_new_products.py

# Neue Produkte von Top-Apotheken mit Suchbegriff "Haze" finden
python3 scripts/find_new_products.py --vendorId top --search "Haze"

# Neue Produkte von bestimmten Herstellern finden
python3 scripts/find_new_products.py --producerId 37,56
```

### Mehrere Produkte hinzufügen
```bash
python3 add_product.py 'gelato'
python3 add_product.py 'wedding cake'
python3 add_product.py 'amnesia haze'
```

### Einzelnes Produkt hinzufügen/aktualisieren
Verwenden Sie das Skript `add_product.py` mit dem Produktnamen als Argument. Das Skript prüft automatisch, ob das Produkt bereits existiert. Wenn ja, werden nur die Preise aktualisiert; andernfalls wird ein neues Produkt hinzugefügt.

```bash
python3 add_product.py 'sourdough'
```

### Einzelnes Produkt hinzufügen/aktualisieren
Verwenden Sie das Skript `add_product.py` mit dem Produktnamen als Argument. Das Skript prüft automatisch, ob das Produkt bereits existiert. Wenn ja, werden nur die Preise aktualisiert; ansonsten wird ein neues Produkt hinzugefügt.

```bash
python3 scripts/add_product.py 'sourdough'
```


### Alle Produkte aktualisieren (Massen-Preisaktualisierung)
```bash
python3 update_prices.py
```
Dieses Skript:
- Lädt alle Produkte aus der Datenbank
- Scrapt Preise für jedes Produkt neu mit verbesserter Zuverlässigkeit
- Zeigt detaillierten Fortschritt mit Batch-Verarbeitung
- Bietet eine umfassende Zusammenfassung erfolgreicher/fehlgeschlagener Updates
- Verbesserte Fehlerbehandlung und Wiederherstellung

### Mehrere Produkte aus Datei hinzufügen (Empfohlene Methode)
Erstelle eine Textdatei mit Produktnamen (einer pro Zeile):
```bash
# products.txt erstellen
cat > products.txt << EOF
gelato
wedding cake
amnesia haze
EOF

# Massen-Hinzufügung ausführen (verarbeitet in kleinen Batches von 2, um Timeouts zu vermeiden)
python3 add_products_batch.py products.txt --yes
```
Siehe `data/example_products.txt` für das Dateiformat.

**Hinweis**: Das Skript verarbeitet Produkte automatisch in Batches von 2 mit Pausen zwischen den Batches, um Timeouts und eine Überlastung der Website zu vermeiden.

### Produktübersicht generieren
### Preisverlauf exportieren
Exportiere aktuelle Preise oder historische Daten im JSON-Format für externe Analysen:
```bash
python3 scripts/export_price_history.py  # Aktueller Snapshot
python3 scripts/export_price_history.py --all  # Kompletter Verlauf
```
Erstellt JSON-Dateien in `data/price_history/` zur einfachen Integration mit anderen Tools.

### Preisverlauf importieren
Importiere Preisdaten aus JSON-Dateien:
```bash
python3 scripts/import_price_history.py data/price_history/2025-11-14.json
```
Unterstützt sowohl aktuelle Snapshots als auch vollständige historische Daten.

### Automatische Archivierung
Richte automatische tägliche Preis-Snapshots und Bereinigung ein:
```bash
python3 scripts/archive_prices.py  # Tägliche Archivierung
python3 scripts/archive_prices.py --cleanup-days=365  # Mit benutzerdefinierter Aufbewahrungszeit
```
Perfekt für Cron-Jobs und automatisierte Backups.

Nach dem Hinzufügen oder Aktualisieren von Produkten, generiere die Übersichts-Markdown-Datei:
```bash
python3 generate_overview.py
```
Dies erstellt/aktualisiert `docs/generated/SORTEN_ÜBERSICHT.md` mit:
- Bestenliste (höchster THC, bester Preis, Community-Liebling, etc.)
- Vollständige Produkttabelle sortiert nach Bewertungsanzahl
- Direkte Links zu allen Produkten auf shop.dransay.com
- Erweiterte Herstellerinformationen und Datenvollständigkeit

### Fehlende Daten korrigieren
Korrigiere fehlende Herstellerinformationen automatisch:
```bash
python3 fix_producers.py
```
Dieses Skript:
- Scannt Produkte mit fehlenden Herstellerdaten
- Scrapt Produktseiten erneut, um Herstellerinformationen zu finden
- Aktualisiert die Datenbank mit korrigierten Daten
- Bietet detaillierte Fortschrittsberichte

### Alle Produkte in der Datenbank anzeigen
```bash
sqlite3 WeedDB.db "SELECT name, id FROM products ORDER BY name"
```

### Günstigste Produkte insgesamt finden
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

## 🛠️ Funktionsweise

1. **Suche**: Skript sucht auf shop.dransay.com nach dem Produktnamen
2. **Top-Apotheken**: Lädt Produktseite mit `vendorId=top` und extrahiert die günstigste Apotheke
3. **Alle Apotheken**: Lädt Produktseite mit `vendorId=all` und extrahiert die günstigste Apotheke
4. **Datenbank**: Speichert 2 Preiseinträge (einen pro Kategorie) mit Apothekennamen, Preis und Zeitstempel

**Wichtiger Vorteil**: Die Website zeigt automatisch die günstigste Apotheke basierend auf dem `vendorId`-Parameter an, sodass wir nicht alle Angebote parsen müssen!

---

## 📊 Datenbankschema

**Vollständiges 3NF-Schema** (definiert in `data/schema.sql`) mit verbesserter Datenintegrität:

```sql
products (
    id INTEGER PRIMARY KEY,        -- Produkt-ID von shop.dransay.com
    name TEXT NOT NULL,            -- Produktname
    variant TEXT,                  -- Vollständige Variantenbeschreibung
    genetics TEXT,                 -- Indica/Sativa/Hybrid
    thc_percent REAL,             -- THC-Prozentsatz
    cbd_percent REAL,             -- CBD-Prozentsatz
    producer_id INTEGER,          -- Fremdschlüssel zu Herstellern
    stock_level INTEGER,          -- Aktueller Lagerbestand
    rating REAL,                  -- Benutzerbewertung (z.B. 4.1)
    review_count INTEGER,         -- Anzahl der Bewertungen
    irradiation TEXT,             -- Ja/Nein
    country TEXT,                 -- Herkunftsland
    effects TEXT,                 -- Gemeldete Effekte
    complaints TEXT,              -- Gemeldete Beschwerden/Anwendungsgebiete
    url TEXT UNIQUE,              -- Produkt-URL
    created_at DATETIME,
    last_updated DATETIME,
    FOREIGN KEY (producer_id) REFERENCES producers(id)
)

producers (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,     -- Herstellername
    origin TEXT                   -- Herkunftsland
)

pharmacies (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,     -- z.B. "Paracelsus Apotheke"
    location TEXT
)

prices (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    pharmacy_id INTEGER NOT NULL,
    price_per_g REAL NOT NULL,
    category TEXT CHECK(category IN ('top', 'all')),  -- Kategorie
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id)
)
```

---

## 🔧 Anforderungen

- **Python 3.9+**
- **SQLite3**
- **Playwright** (für Web-Scraping)
- **Internetverbindung** (für Zugriff auf shop.dransay.com)

---

## 📝 Lizenz

Dies ist ein persönliches Projekt für Bildungszwecke. Bitte respektiere die Nutzungsbedingungen von shop.dransay.com beim Scraping.

---

---


