---
created: 2025-11-15
updated: 2025-11-15
version: 0.1.0
author: Claude AI
status: alpha
platform: Windows 10/11
target_audience: Absolute Anfänger
description: Schritt-für-Schritt Installationsanleitung für WeedDB auf Windows
---

# WeedDB Einrichtung für absolute Anfänger (Windows)

> **Zielgruppe:** Du hast gerade zum ersten Mal das Terminal/CMD geöffnet und möchtest WeedDB nutzen.

Diese Anleitung führt dich Schritt-für-Schritt durch die komplette Installation auf Windows 10/11.

---

## 🎯 Was du am Ende haben wirst

- ✅ Python 3.9+ installiert
- ✅ SQLite3 einsatzbereit
- ✅ WeedDB-Datenbank eingerichtet
- ✅ Erstes Cannabis-Produkt in der Datenbank
- ✅ Obsidian für schöne Ansichten (optional)

**Geschätzte Zeit:** 20-25 Minuten

---

## Schritt 1: PowerShell oder CMD öffnen

**PowerShell (empfohlen):**
1. Drücke `Windows + X`
2. Klicke auf "Windows PowerShell" oder "Terminal"

**Oder CMD:**
1. Drücke `Windows + R`
2. Tippe `cmd` ein
3. Drücke `Enter`

**Tipp:** Pinne PowerShell an die Taskleiste für schnellen Zugriff!

---

## Schritt 2: Python 3 installieren

Python ist die Programmiersprache, die WeedDB nutzt.

### Prüfen ob Python 3 schon installiert ist:

```powershell
python --version
```

**Falls du `Python 3.9` oder höher siehst:** ✅ Fertig, weiter zu Schritt 3

**Falls nicht (oder `command not found`):**

### Python von python.org installieren:

1. Gehe zu: https://www.python.org/downloads/
2. Klicke auf den gelben "Download Python 3.11.x" Button
3. **WICHTIG:** Starte den Installer
4. **WICHTIG:** ✅ Hake "Add Python to PATH" an (ganz unten!)
5. Klicke "Install Now"
6. Warte 2-3 Minuten
7. **Schließe PowerShell/CMD und öffne es NEU!** (wichtig damit PATH aktualisiert wird)

### Prüfen:

```powershell
python --version
pip --version
```

Du solltest jetzt `Python 3.11.x` und `pip xx.x.x` sehen.

---

## Schritt 3: Git installieren

Git brauchen wir, um WeedDB von GitHub herunterzuladen.

### Prüfen ob Git installiert ist:

```powershell
git --version
```

**Falls ja:** ✅ Weiter zu Schritt 4

**Falls nein:**

1. Gehe zu: https://git-scm.com/download/win
2. Lade "64-bit Git for Windows Setup" herunter
3. Starte den Installer
4. Klicke durch den Installer (Standard-Einstellungen sind OK)
5. **Wichtig:** Bei "Adjusting your PATH environment" → Wähle "Git from the command line and also from 3rd-party software"
6. Installiere
7. **Schließe PowerShell/CMD und öffne es NEU!**

### Prüfen:

```powershell
git --version
```

---

## Schritt 4: SQLite3 installieren

SQLite ist die Datenbank.

### Option A: SQLite kommt mit Python (empfohlen)

Python auf Windows bringt normalerweise SQLite mit. Prüfe:

```powershell
python -c "import sqlite3; print(sqlite3.version)"
```

**Falls du eine Versionsnummer siehst:** ✅ Fertig, weiter zu Schritt 5

### Option B: Manuelle Installation (falls Option A nicht funktioniert)

1. Gehe zu: https://www.sqlite.org/download.html
2. Lade "sqlite-tools-win32-x86-xxxxxxx.zip" herunter
3. Entpacke die ZIP-Datei nach `C:\sqlite`
4. Füge `C:\sqlite` zum PATH hinzu:
   - Drücke `Windows + Pause` (öffnet System)
   - Klicke "Erweiterte Systemeinstellungen"
   - Klicke "Umgebungsvariablen"
   - Unter "Systemvariablen" → Wähle "Path" → Klicke "Bearbeiten"
   - Klicke "Neu" → Füge `C:\sqlite` hinzu
   - OK → OK → OK
5. **Schließe PowerShell/CMD und öffne es NEU!**

### Prüfen:

```powershell
sqlite3 --version
```

---

## Schritt 5: WeedDB Repository herunterladen

Jetzt holen wir uns den WeedDB-Code von GitHub.

### Navigiere zu deinem gewünschten Ordner:

```powershell
# Gehe zu deinem Dokumente-Ordner
cd $HOME\Documents

# Oder wähle einen anderen Ort, z.B. Desktop:
# cd $HOME\Desktop

# Erstelle einen "Projects" Ordner (optional)
mkdir Projects
cd Projects
```

### Lade WeedDB herunter:

```powershell
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB
```

**Prüfen dass du im richtigen Ordner bist:**
```powershell
pwd
dir
```

Du solltest Dateien wie `README.md`, `CLAUDE.md`, `scripts\` sehen.

---

## Schritt 6: Python-Abhängigkeiten installieren

Jetzt installieren wir die benötigten Python-Bibliotheken.

```powershell
# Stelle sicher, dass du im WeedDB-Ordner bist
pwd
# Sollte zeigen: C:\Users\DEINNAME\Documents\Projects\WeedDB (oder ähnlich)

# Installiere Playwright und mypy
pip install playwright mypy

# Installiere den Chromium-Browser für Playwright
python -m playwright install chromium
```

Das dauert 2-3 Minuten. Du siehst viel Text durchlaufen - das ist normal!

---

## Schritt 7: Datenbank initialisieren

Jetzt erstellen wir die SQLite-Datenbank.

```powershell
# Gehe ins scripts-Verzeichnis
cd scripts

# Erstelle die Datenbank mit dem Schema
# PowerShell:
Get-Content ..\data\schema.sql | sqlite3 ..\data\WeedDB.db

# Falls das nicht funktioniert, versuche CMD-Stil:
# type ..\data\schema.sql | sqlite3 ..\data\WeedDB.db
```

**Keine Fehlermeldung?** ✅ Perfekt! Die Datenbank wurde erstellt.

**Prüfen ob die Datenbank existiert:**
```powershell
dir ..\data\WeedDB.db
```

Du solltest eine Datei mit ein paar KB sehen.

---

## Schritt 8: Erstes Produkt hinzufügen! 🎉

Jetzt der spannende Teil - füge deine erste Cannabis-Sorte hinzu!

```powershell
# Stelle sicher, dass du im scripts-Ordner bist
cd scripts  # falls noch nicht dort

# Füge "Sourdough" hinzu (ein beliebtes Produkt)
python add_product.py "sourdough"
```

**Wichtig:** Auf Windows nutze `"` (doppelte Anführungszeichen) statt `'` (einfache)!

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

```powershell
sqlite3 ..\data\WeedDB.db "SELECT name, thc_percent, rating, review_count FROM products;"
```

**Ausgabe:**
```
Sourdough|29.0|4.0|1832
```

🎉 **Glückwunsch! Du hast gerade dein erstes Cannabis-Produkt zur Datenbank hinzugefügt!**

---

## Schritt 10: Weitere Produkte hinzufügen

```powershell
# Einzelne Produkte:
python add_product.py "gelato"
python add_product.py "wedding cake"
python add_product.py "amnesia haze"

# Mehrere Produkte aus Datei:
# Erstelle eine Textdatei mit Produktnamen (ein Name pro Zeile)
@"
pink kush
grape face
black cherry
"@ | Out-File -Encoding UTF8 meine_produkte.txt

# Füge alle hinzu:
python add_products_batch.py meine_produkte.txt --yes
```

---

## Schritt 11: Produktübersicht generieren

Erstelle eine schöne Markdown-Übersicht aller Produkte:

```powershell
python generate_overview.py
```

Die Datei wird hier erstellt: `docs\generated\SORTEN_ÜBERSICHT.md`

**Ansehen im Editor:**
```powershell
notepad ..\docs\generated\SORTEN_ÜBERSICHT.md
```

---

## 🎨 Bonus: Obsidian installieren (optional)

Für eine schöne visuelle Darstellung deiner Cannabis-Datenbank:

1. Gehe zu: https://obsidian.md
2. Klicke "Get Obsidian for Windows"
3. Lade den Installer herunter
4. Installiere Obsidian
5. Starte Obsidian
6. Klicke "Open folder as vault"
7. Wähle deinen WeedDB-Ordner (z.B. `C:\Users\DEINNAME\Documents\Projects\WeedDB`)
8. Öffne `START.md` für einen Überblick

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

### "python" wird nicht erkannt

Du hast vergessen, "Add Python to PATH" beim Installieren anzuhaken. Optionen:

**Option A:** Python neu installieren mit PATH-Option
**Option B:** Manuell zum PATH hinzufügen:
1. Finde Python-Installation (normalerweise `C:\Users\DEINNAME\AppData\Local\Programs\Python\Python311`)
2. Füge zum PATH hinzu (siehe Schritt 4 → SQLite → Option B für Anleitung)
3. Füge auch `...\Python311\Scripts` zum PATH hinzu

### PowerShell Execution Policy Fehler

Wenn du `cannot be loaded because running scripts is disabled` siehst:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### SQLite: "Get-Content" funktioniert nicht

Versuche CMD statt PowerShell:

```cmd
cd scripts
type ..\data\schema.sql | sqlite3 ..\data\WeedDB.db
```

### Playwright-Installation schlägt fehl

Stelle sicher, dass Visual C++ Redistributables installiert sind:
1. Gehe zu: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Lade herunter und installiere
3. Versuche nochmal: `python -m playwright install chromium`

### Windows Defender blockiert Playwright

Manchmal blockiert Windows Defender den Chromium-Download:
1. Windows Defender öffnen
2. Virus & Bedrohungsschutz → Schutzeinstellungen verwalten
3. Echtzeitschutz kurz deaktivieren
4. Playwright installieren
5. Echtzeitschutz wieder aktivieren

### Scraping schlägt fehl

- Prüfe Internetverbindung
- Stelle sicher, dass shop.dransay.com erreichbar ist
- Deaktiviere temporär Firewall/Antivirus
- Versuche es nochmal (manchmal temporäre Timeouts)

### Pfad-Probleme (Backslash vs Forward Slash)

Windows nutzt `\` (Backslash), aber Python akzeptiert auch `/`:

```powershell
# Beide funktionieren:
python add_product.py "gelato"
python .\add_product.py "gelato"
```

---

## 💡 Windows-spezifische Tipps

### Terminal als Administrator öffnen (falls nötig)

1. Suche "PowerShell" im Startmenü
2. Rechtsklick → "Als Administrator ausführen"

### Zeichen-Encoding-Probleme

Falls du komische Zeichen siehst:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Schneller navigieren

```powershell
# Tab-Completion nutzen:
cd Doc<TAB>  # vervollständigt zu "Documents"
cd Pr<TAB>   # vervollständigt zu "Projects"
```

---

## 📞 Hilfe bekommen

- **GitHub Issues:** https://github.com/laubfrosch-sudo/WeedDB/issues
- **Dokumentation:** Siehe `docs\` Ordner
- **README:** Lies die Hauptdatei `README.md`

---

**Viel Erfolg! 🌿**
