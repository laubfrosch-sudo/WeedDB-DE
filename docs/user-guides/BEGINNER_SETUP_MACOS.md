---
created: 2025-11-15
updated: 2025-11-15
version: 1.5.0
author: Claude AI
status: stable
platform: macOS
target_audience: Absolute Anfänger
description: Schritt-für-Schritt Installationsanleitung für WeedDB auf macOS
---

# WeedDB Einrichtung für absolute Anfänger (macOS)

> **Zielgruppe:** Du hast gerade zum ersten Mal das Terminal geöffnet und möchtest WeedDB nutzen.

Diese Anleitung führt dich Schritt-für-Schritt durch die komplette Installation auf macOS.

---

## 🎯 Was du am Ende haben wirst

- ✅ Python 3.9+ installiert
- ✅ SQLite3 einsatzbereit
- ✅ WeedDB-Datenbank eingerichtet
- ✅ Erstes Cannabis-Produkt in der Datenbank
- ✅ Obsidian für schöne Ansichten (optional)

**Geschätzte Zeit:** 15-20 Minuten

---

## Schritt 1: Terminal öffnen

1. Drücke `Cmd + Leertaste` (öffnet Spotlight-Suche)
2. Tippe `Terminal` ein
3. Drücke `Enter`
4. Ein schwarzes/weißes Fenster öffnet sich - das ist das Terminal

**Tipp:** Pinne das Terminal ins Dock (Rechtsklick auf Terminal-Icon → Optionen → Im Dock behalten)

---

## Schritt 2: Homebrew installieren (Paketmanager)

Homebrew ist wie ein "App Store" für Entwickler-Tools. Wir brauchen es, um Software zu installieren.

### Prüfen ob Homebrew schon installiert ist:

```bash
brew --version
```

**Falls du eine Versionsnummer siehst** (z.B. `Homebrew 4.x.x`): ✅ Fertig, weiter zu Schritt 3

**Falls `command not found` erscheint:** Du musst Homebrew installieren:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- Das Passwort eingeben (du siehst beim Tippen nichts - das ist normal!)
- Drücke `Enter` wenn gefragt
- Warte 3-5 Minuten
- **Wichtig:** Am Ende könnten 2 Befehle in grünem Text erscheinen, die du ausführen sollst - kopiere und führe sie aus!

**Prüfen ob's funktioniert:**
```bash
brew --version
```

---

## Schritt 3: Python 3 installieren

Python ist die Programmiersprache, die WeedDB nutzt.

### Prüfen ob Python 3 schon installiert ist:

```bash
python3 --version
```

**Falls du `Python 3.9` oder höher siehst:** ✅ Fertig, weiter zu Schritt 4

**Falls nicht (oder Version unter 3.9):**

```bash
brew install python@3.11
```

Warte 2-3 Minuten.

**Prüfen:**
```bash
python3 --version
```

Du solltest jetzt `Python 3.11.x` sehen.

---

## Schritt 4: SQLite3 prüfen

SQLite ist die Datenbank. Auf macOS ist das normalerweise schon installiert.

```bash
sqlite3 --version
```

**Du solltest etwas wie `3.x.x` sehen:** ✅ Perfekt!

**Falls `command not found`:**
```bash
brew install sqlite
```

---

## Schritt 5: WeedDB Repository herunterladen

Jetzt holen wir uns den WeedDB-Code von GitHub.

### Navigiere zu deinem gewünschten Ordner:

```bash
# Gehe zu Desktop (oder wohin du willst)
cd ~/Desktop

# Erstelle einen "Claude" Ordner (optional)
mkdir -p Claude
cd Claude
```

### Lade WeedDB herunter:

**Option A: Mit Git (empfohlen)**

Prüfe ob Git installiert ist:
```bash
git --version
```

Falls ja:
```bash
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB
```

Falls nein, installiere Git:
```bash
brew install git
# Dann nochmal:
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB
```

**Option B: Als ZIP herunterladen (für Nicht-Entwickler)**

1. Gehe zu: https://github.com/laubfrosch-sudo/WeedDB
2. Klicke auf den grünen "Code" Button
3. Klicke "Download ZIP"
4. Entpacke die ZIP-Datei
5. Im Terminal:
```bash
cd ~/Desktop/WeedDB-main  # oder wo auch immer du es entpackt hast
```

---

## Schritt 6: Python-Abhängigkeiten installieren

Jetzt installieren wir die benötigten Python-Bibliotheken.

```bash
# Stelle sicher, dass du im WeedDB-Ordner bist
pwd
# Sollte zeigen: /Users/DEINNAME/Desktop/Claude/WeedDB (oder ähnlich)

# Installiere Playwright und mypy
pip3 install playwright mypy

# Installiere den Chromium-Browser für Playwright
python3 -m playwright install chromium
```

Das dauert 2-3 Minuten. Du siehst viel Text durchlaufen - das ist normal!

---

## Schritt 7: Datenbank initialisieren

Jetzt erstellen wir die SQLite-Datenbank.

```bash
# Gehe ins scripts-Verzeichnis
cd scripts

# Erstelle die Datenbank mit dem Schema
sqlite3 ../data/WeedDB.db < ../data/schema.sql
```

**Keine Fehlermeldung?** ✅ Perfekt! Die Datenbank wurde erstellt.

**Prüfen ob die Datenbank existiert:**
```bash
ls -lh ../data/WeedDB.db
```

Du solltest eine Datei mit ein paar KB sehen.

---

## Schritt 8: Erstes Produkt hinzufügen! 🎉

Jetzt der spannende Teil - füge deine erste Cannabis-Sorte hinzu!

```bash
# Stelle sicher, dass du im scripts-Ordner bist
cd scripts  # falls noch nicht dort

# Füge "Sourdough" hinzu (ein beliebtes Produkt)
python3 add_product.py 'sourdough'
```

**Was passiert:**
- Das Skript öffnet shop.dransay.com (unsichtbar im Hintergrund)
- Sucht nach "Sourdough"
- Extrahiert Produktdaten, Preise, Apotheken
- Speichert alles in der Datenbank

**Dauer:** 30-60 Sekunden

**Erwartete Ausgabe:**
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

============================================================
✅ Successfully added 'Sourdough' to database with cheapest prices.
```

---

## Schritt 9: Datenbank ansehen

Schaue dir an, was du gerade hinzugefügt hast!

```bash
sqlite3 ../data/WeedDB.db "SELECT name, thc_percent, rating, review_count FROM products;"
```

**Ausgabe:**
```
Sourdough|29.0|4.0|1832
```

🎉 **Glückwunsch! Du hast gerade dein erstes Cannabis-Produkt zur Datenbank hinzugefügt!**

---

## Schritt 10: Weitere Produkte hinzufügen

```bash
# Einzelne Produkte:
python3 add_product.py 'gelato'
python3 add_product.py 'wedding cake'
python3 add_product.py 'amnesia haze'

# Mehrere Produkte aus Datei:
# Erstelle eine Textdatei mit Produktnamen (ein Name pro Zeile)
cat > meine_produkte.txt << EOF
pink kush
grape face
black cherry
EOF

# Füge alle hinzu:
python3 add_products_batch.py meine_produkte.txt --yes
```

---

## Schritt 11: Produktübersicht generieren

Erstelle eine schöne Markdown-Übersicht aller Produkte:

```bash
python3 generate_overview.py
```

Die Datei wird hier erstellt: `docs/generated/SORTEN_ÜBERSICHT.md`

**Ansehen im Terminal:**
```bash
cat ../docs/generated/SORTEN_ÜBERSICHT.md
```

Oder öffne die Datei in einem Texteditor/Obsidian für eine schöne Darstellung!

---

## 🎨 Bonus: Obsidian installieren (optional)

Für eine schöne visuelle Darstellung deiner Cannabis-Datenbank:

1. Lade Obsidian herunter: https://obsidian.md
2. Installiere die App
3. Öffne Obsidian → "Open folder as vault"
4. Wähle deinen WeedDB-Ordner (z.B. `/Users/DEINNAME/Desktop/Claude/WeedDB`)
5. Öffne `START.md` für einen Überblick

**Siehe auch:** [[OBSIDIAN_THEMES|Obsidian Design-Guide]] für schöne Themes und Plugins

---

## 🔧 Nächste Schritte

**Jetzt wo alles läuft:**
- 📖 Lies die [[ANLEITUNG|vollständige Anleitung]] für fortgeschrittene Features
- 📊 Entdecke [[QUERY_EXAMPLES|SQL-Abfrage-Beispiele]] (60+ Queries)
- 🌿 Öffne [[SORTEN_ÜBERSICHT|Sortenübersicht]] um alle Produkte zu sehen
- 🤖 Nutze [[CLAUDE|KI-Assistenten]] für automatisierte Abfragen

---

## ❓ Problemlösungen

### "Permission denied" Fehler

Versuche `pip3` mit `--user` Flag:
```bash
pip3 install --user playwright mypy
```

### "command not found: python3"

Versuche `python` statt `python3`:
```bash
python --version
python -m pip install playwright mypy
```

### Playwright-Browser installiert nicht

Manuell installieren:
```bash
python3 -m playwright install --with-deps chromium
```

### Datenbankfehler "table already exists"

Die Datenbank wurde schon erstellt - das ist OK! Überspringe Schritt 7.

### Scraping schlägt fehl

- Prüfe Internetverbindung
- Stelle sicher, dass shop.dransay.com erreichbar ist: https://shop.dransay.com
- Versuche es nochmal (manchmal temporäre Timeouts)

---

## 📞 Hilfe bekommen

- **GitHub Issues:** https://github.com/laubfrosch-sudo/WeedDB/issues
- **Dokumentation:** Siehe `docs/` Ordner
- **README:** Lies die Hauptdatei `README.md`

---

**Viel Erfolg! 🌿**
