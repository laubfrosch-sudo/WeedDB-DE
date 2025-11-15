---
created: 2025-11-15
updated: 2025-11-15
version: 1.5.1
author: Claude AI
status: stable
description: WeedDB Obsidian Vault Startseite mit Navigation und Setup-Anleitungen
---

<div align="center">
  <img src="docs/assets/icons/WeedDB.jpeg" alt="WeedDB Logo" width="400"/>
</div>

# WeedDB - Cannabis Preis-Tracking Datenbank

> **Willkommen im WeedDB Obsidian Vault!**
>
> Diese Wissensdatenbank enthält alle Informationen zu WeedDB - einem Cannabis-Produkt-Preisvergleich für den deutschen medizinischen Markt.

---

## 🆕 Kompletter Anfänger? Start hier!

**Erstes Mal Terminal geöffnet?** Kein Problem! Wähle dein Betriebssystem und folge der Schritt-für-Schritt-Anleitung:

### 📱 Betriebssystem-spezifische Anleitungen:

- 🍎 **[[BEGINNER_SETUP_MACOS|macOS Setup-Guide]]** - Für Mac-User (inkl. Homebrew-Installation)
- 🐧 **[[BEGINNER_SETUP_LINUX|Linux Setup-Guide]]** - Für Ubuntu/Debian/Fedora-User
- 🪟 **[[BEGINNER_SETUP_WINDOWS|Windows Setup-Guide]]** - Für Windows 10/11-User

**Was du lernst:**
- ✅ Python, Git, SQLite installieren
- ✅ WeedDB-Repository herunterladen
- ✅ Datenbank initialisieren
- ✅ Erstes Produkt hinzufügen
- ✅ Obsidian optional einrichten

**Geschätzte Zeit:** 15-25 Minuten (je nach OS)

---

## 📖 Obsidian Setup

### So öffnest du dieses Vault in Obsidian:

1. **Obsidian installieren** (falls noch nicht vorhanden)
   - Download: [obsidian.md](https://obsidian.md)
   - Kostenlos für persönliche Nutzung

2. **WeedDB als Vault öffnen**
   - Obsidian starten → "Open folder as vault"
   - Navigiere zu deinem WeedDB-Ordner (z.B. `~/Desktop/WeedDB` oder `~/Projects/WeedDB`)
   - Oder: Klicke auf "Open another vault" → "Open folder as vault"

3. **START.md als Standard-Seite festlegen**
   - Settings (⚙️) → Core plugins → "Daily notes" deaktivieren
   - Settings → Core plugins → "Workspaces" aktivieren
   - Diese Datei (`START.md`) öffnen
   - Rechtsklick auf Tab → "Pin"
   - Layout speichern: Command Palette (`Cmd/Ctrl+P`) → "Workspaces: Save current workspace layout as..."

4. **Empfohlene Einstellungen**
   - Settings → Editor → "Readable line length" aktivieren
   - Settings → Files & Links → "Default location for new notes" → "In the folder specified below" → `docs/`
   - Settings → Appearance → Theme nach Wahl (z.B. "Minimal" für Clean Look)

5. **Nützliche Hotkeys**
   - `Cmd/Ctrl + O` - Schnellsuche für Dateien
   - `Cmd/Ctrl + P` - Command Palette
   - `Cmd/Ctrl + E` - Edit/Preview Mode wechseln
   - `Cmd/Ctrl + Click` - Link in neuem Tab öffnen

### 🎨 Schöne Obsidian-Ansicht gewünscht?

Mach dein WeedDB-Vault richtig schick mit Themes, Plugins und Custom CSS!

👉 **[[OBSIDIAN_THEMES|Obsidian Design-Guide]]** - Kompletter Guide für:
- 🎨 Top 5 empfohlene Themes (inkl. Cannabis-grünes Theme!)
- 🔌 Must-have Plugins (Dataview, Advanced Tables, etc.)
- 💅 CSS-Snippets für schönere Produkttabellen
- ⚙️ Optimale Layout-Einstellungen
- 💼 Fertige Workspace-Setups

---

## 🚀 Schnellstart

### Für Einsteiger
- 📖 [[INSTRUCTIONS|Englische Anleitung]] - Complete setup and usage guide
- 📖 [[ANLEITUNG|Deutsche Anleitung]] - Vollständige Installations- und Nutzungsanleitung
- 🌿 [[SORTEN_ÜBERSICHT|Sortenübersicht]] - Automatisch generierte Produktliste
- 📊 [[DATEN_VISUALISIERUNGEN|Datenvisualisierungen]] - Diagramme und Charts der Produktdaten

### Für Entwickler
- 🤖 [[CLAUDE|Claude AI Dokumentation]] - Technische Dokumentation für Claude Code
- 🤖 [[GEMINI|Gemini AI Dokumentation]] - Technische Dokumentation für Google Gemini
- 🔧 [[AGENTS|AI Agents Guidelines]] - Richtlinien für AI-Assistenten
- 💾 [[data/schema|Datenbankschema]] - SQLite 3NF Schema-Definition

---

## 📁 Vault-Struktur

```
WeedDB/
├── 📂 docs/
│   ├── 📂 user-guides/          # Benutzeranleitungen (DE/EN)
│   ├── 📂 ai-assistants/        # AI-Dokumentation
│   ├── 📂 development/          # Entwicklungs-Reports & Tests
│   ├── 📂 generated/            # Automatisch generierte Dateien
│   ├── 📂 templates/            # Vorlagen
│   └── 📄 QUERY_EXAMPLES.md     # 60+ SQL-Abfrage-Beispiele
├── 📂 scripts/                  # Python-Skripte
├── 📂 data/                     # Datenbank & Schema
└── 📄 README.md                 # Projekt-Übersicht
```

---

## 🔗 Wichtige Links

### Produktdaten & Analysen
- [[SORTEN_ÜBERSICHT|🌿 Sortenübersicht]] - Alle Produkte sortiert nach Bewertungen
- [[QUERY_EXAMPLES|📊 SQL-Abfragen]] - Preisvergleiche, Terpene, Therapeutische Anwendungen

### Anleitungen & Dokumentation
- [[INSTRUCTIONS|📖 English Guide]] - Setup, usage, troubleshooting
- [[ANLEITUNG|📖 Deutsche Anleitung]] - Installation, Nutzung, Fehlerbehandlung
- [[AI_INSTALLATION|🤖 AI Installation Guide]] - For AI assistants
- [[KI_INSTALLATION|🤖 KI Installations-Anleitung]] - Für KI-Assistenten

### AI-Assistenten
- [[CLAUDE|Claude AI]] - Technische Dokumentation & Arbeitsanweisungen
- [[GEMINI|Gemini AI]] - Projektübersicht & Schema-Definitionen
- [[AGENTS|AI Agents]] - Allgemeine Richtlinien für alle AI-Assistenten

### Entwicklung & Testing
- [[DEVELOPMENT_REPORT|📝 Development Report]] - Projektfortschritt & Features
- [[TESTING_REPORT|🧪 Testing Report]] - Test-Ergebnisse & Validierung

---

## 🎯 Häufige Aufgaben

### Neue Produkte hinzufügen
```bash
# Einzelnes Produkt
python3 add_product.py 'sourdough'

# Mehrere Produkte aus Datei
python3 add_products_batch.py products.txt --yes
```

### Preise aktualisieren
```bash
# Alle Produkte aktualisieren
python3 update_prices.py

# Sortenübersicht neu generieren
python3 scripts/generate_overview.py
```

### Datenbank abfragen
```bash
# SQLite CLI öffnen
sqlite3 data/WeedDB.db

# Produkte mit größten Preisunterschieden finden
sqlite3 data/WeedDB.db "SELECT product_name, min_price || '€' as billigster_preis,
max_price || '€' as teuerster_preis, price_spread || '€' as differenz
FROM product_price_stats WHERE pharmacy_count > 1 ORDER BY price_spread DESC LIMIT 10;"

# Beste Apotheke für eine bestimmte Sorte finden
sqlite3 data/WeedDB.db "SELECT pharmacy_name, price_per_g || '€/g' as preis
FROM product_pharmacy_prices WHERE product_name LIKE '%Gelato%' ORDER BY price_per_g ASC LIMIT 5;"

# Top 10 Indica-Sorten nach Bewertung
sqlite3 data/WeedDB.db "SELECT name, thc_percent || '%' as THC, rating || '★' as bewertung,
review_count as reviews FROM products WHERE genetics = 'Indica' ORDER BY rating DESC LIMIT 10;"

# Preisverlauf einer Sorte ansehen
sqlite3 data/WeedDB.db "SELECT ph.name as apotheke, pr.price_per_g || '€/g' as preis,
datetime(pr.timestamp, 'localtime') as zeitstempel FROM prices pr
JOIN pharmacies ph ON pr.pharmacy_id = ph.id JOIN products p ON pr.product_id = p.id
WHERE p.name LIKE '%Sourdough%' ORDER BY pr.timestamp DESC LIMIT 10;"
```

Siehe [[QUERY_EXAMPLES|SQL-Abfrage-Beispiele]] für 60+ vorkonfigurierte Queries.

---

## 📊 Projekt-Statistiken

**Version:** 1.5.0
**Datenquelle:** [shop.dransay.com](https://shop.dransay.com)
**GitHub:** [laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

### Neueste Features (v1.5.0)
- ✅ Komplette Beginner-Guides für alle Betriebssysteme (macOS/Linux/Windows)
- ✅ Obsidian Design-Guide mit Themes, Plugins & CSS-Snippets
- ✅ YAML-Frontmatter-System für alle Dokumentationen
- ✅ Dokumentations-Wartungs-Richtlinien
- ✅ Verbesserte Logo-Integration in allen Docs

### Features aus v1.4.0:
- ✅ Verbesserte Batch-Verarbeitung
- ✅ Automatische Datenkorrektur (`fix_producers.py`)
- ✅ Export/Import von Preisverlaufsdaten
- ✅ Erweiterte Fehlerbehandlung
- ✅ Multi-Pharmacy Preisvergleich

---

## 🛠️ Technologie-Stack

- **Datenbank:** SQLite (3NF-Schema)
- **Web Scraping:** Playwright (Headless Chromium)
- **Sprache:** Python 3.9+
- **Type Checking:** mypy (strict mode)
- **Knowledge Base:** Obsidian.md

---

## 📝 Hinweise

> **Logo:** Das WeedDB-Logo wurde mit Google Gemini erstellt.

> **Automatische Dateien:** Die Datei `docs/generated/SORTEN_ÜBERSICHT.md` wird automatisch generiert. Änderungen manuell vornehmen hat keinen Effekt - nutze stattdessen `python3 scripts/generate_overview.py`.

> **Obsidian-Optimierung:** Dieses Repository ist für Obsidian.md optimiert mit strukturierten Ordnern, Cross-Links und Navigations-Guides.

---

## 🔄 Zuletzt aktualisiert

Diese Datei wurde automatisch generiert. Für die aktuellste Version siehe:
- [[README|Projekt README]]
- [[SORTEN_ÜBERSICHT|Sortenübersicht]] (mit Zeitstempel)

---

<div align="center">

**[GitHub Repository](https://github.com/laubfrosch-sudo/WeedDB)** | **[[README|Projekt-Übersicht]]** | **[[QUERY_EXAMPLES|SQL-Beispiele]]**

</div>
