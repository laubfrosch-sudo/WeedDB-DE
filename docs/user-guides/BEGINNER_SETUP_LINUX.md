---
created: 2025-11-15
updated: 2025-11-15
version: 1.5.0
author: Claude AI
status: stable
platform: Linux (Ubuntu/Debian/Fedora)
target_audience: Absolute Anfänger
description: Schritt-für-Schritt Installationsanleitung für WeedDB auf Linux
---

# WeedDB Einrichtung für absolute Anfänger (Linux)

> **Zielgruppe:** Du hast gerade zum ersten Mal das Terminal geöffnet und möchtest WeedDB nutzen.

Diese Anleitung führt dich Schritt-für-Schritt durch die komplette Installation auf Linux (Ubuntu/Debian/Fedora).

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

**Ubuntu/Debian:**
- Drücke `Ctrl + Alt + T`
- Oder: Suche "Terminal" im Application Launcher

**Fedora:**
- Drücke `Super` (Windows-Taste) und tippe "Terminal"
- Oder: Rechtsklick auf Desktop → "Open Terminal"

**Tipp:** Pinne das Terminal in deine Taskleiste für schnellen Zugriff!

---

## Schritt 2: System aktualisieren

Aktualisiere zuerst dein System, um die neuesten Pakete zu bekommen.

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt upgrade -y
```

**Fedora:**
```bash
sudo dnf update -y
```

Gib dein Passwort ein wenn gefragt (du siehst beim Tippen nichts - das ist normal!).

---

## Schritt 3: Python 3 installieren

Python ist die Programmiersprache, die WeedDB nutzt.

### Prüfen ob Python 3 schon installiert ist:

```bash
python3 --version
```

**Falls du `Python 3.9` oder höher siehst:** ✅ Fertig, weiter zu Schritt 4

**Falls nicht (oder Version unter 3.9):**

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-venv -y
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip -y
```

**Prüfen:**
```bash
python3 --version
```

Du solltest jetzt `Python 3.9` oder höher sehen.

---

## Schritt 4: SQLite3 installieren

SQLite ist die Datenbank.

### Prüfen ob SQLite schon installiert ist:

```bash
sqlite3 --version
```

**Falls du eine Versionsnummer siehst:** ✅ Fertig, weiter zu Schritt 5

**Falls nicht:**

**Ubuntu/Debian:**
```bash
sudo apt install sqlite3 -y
```

**Fedora:**
```bash
sudo dnf install sqlite -y
```

**Prüfen:**
```bash
sqlite3 --version
```

---

## Schritt 5: Git installieren

Git brauchen wir, um WeedDB von GitHub herunterzuladen.

### Prüfen ob Git installiert ist:

```bash
git --version
```

**Falls ja:** ✅ Weiter zu Schritt 6

**Falls nein:**

**Ubuntu/Debian:**
```bash
sudo apt install git -y
```

**Fedora:**
```bash
sudo dnf install git -y
```

---

## Schritt 6: WeedDB Repository herunterladen

Jetzt holen wir uns den WeedDB-Code von GitHub.

### Navigiere zu deinem gewünschten Ordner:

```bash
# Gehe zu deinem Home-Verzeichnis
cd ~

# Erstelle einen "Projects" oder "Cannabis" Ordner (optional)
mkdir -p Projects
cd Projects
```

### Lade WeedDB herunter:

```bash
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB
```

**Prüfen dass du im richtigen Ordner bist:**
```bash
pwd
ls
```

Du solltest Dateien wie `README.md`, `CLAUDE.md`, `scripts/` sehen.

---

## Schritt 7: Python-Abhängigkeiten installieren

Jetzt installieren wir die benötigten Python-Bibliotheken.

```bash
# Stelle sicher, dass du im WeedDB-Ordner bist
pwd
# Sollte zeigen: /home/DEINNAME/Projects/WeedDB (oder ähnlich)

# Installiere Playwright und mypy
pip3 install playwright mypy

# Falls "Permission denied", versuche:
pip3 install --user playwright mypy
```

### Installiere den Chromium-Browser für Playwright:

```bash
python3 -m playwright install chromium

# Falls Fehler wegen fehlender Bibliotheken:
python3 -m playwright install --with-deps chromium
```

**Ubuntu/Debian:** Falls zusätzliche Abhängigkeiten fehlen:
```bash
sudo apt install libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libgbm1 libasound2 -y
```

**Fedora:**
```bash
sudo dnf install nss atk at-spi2-atk libdrm libxkbcommon mesa-libgbm alsa-lib -y
```

Das dauert 2-3 Minuten. Du siehst viel Text durchlaufen - das ist normal!

---

## Schritt 8: Datenbank initialisieren

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

## Schritt 9: Erstes Produkt hinzufügen! 🎉

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

## Schritt 10: Datenbank ansehen

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

## Schritt 11: Weitere Produkte hinzufügen

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

## Schritt 12: Produktübersicht generieren

Erstelle eine schöne Markdown-Übersicht aller Produkte:

```bash
python3 generate_overview.py
```

Die Datei wird hier erstellt: `docs/generated/SORTEN_ÜBERSICHT.md`

**Ansehen im Terminal:**
```bash
cat ../docs/generated/SORTEN_ÜBERSICHT.md | less
```

Drücke `q` zum Beenden.

---

## 🎨 Bonus: Obsidian installieren (optional)

Für eine schöne visuelle Darstellung deiner Cannabis-Datenbank:

### Ubuntu/Debian:

**Option A: AppImage (empfohlen)**
```bash
# Lade Obsidian herunter
cd ~/Downloads
wget https://github.com/obsidianmd/obsidian-releases/releases/download/v1.4.16/Obsidian-1.4.16.AppImage

# Mache es ausführbar
chmod +x Obsidian-1.4.16.AppImage

# Starte Obsidian
./Obsidian-1.4.16.AppImage
```

**Option B: Snap**
```bash
sudo snap install obsidian --classic
```

### Fedora:

**Flatpak (empfohlen):**
```bash
flatpak install flathub md.obsidian.Obsidian
flatpak run md.obsidian.Obsidian
```

### WeedDB in Obsidian öffnen:

1. Obsidian starten
2. "Open folder as vault"
3. Wähle deinen WeedDB-Ordner (z.B. `/home/DEINNAME/Projects/WeedDB`)
4. Öffne `START.md` für einen Überblick

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

### "Permission denied" beim pip3 install

Versuche mit `--user` Flag:
```bash
pip3 install --user playwright mypy
```

Oder erstelle eine virtuelle Umgebung:
```bash
python3 -m venv venv
source venv/bin/activate
pip install playwright mypy
```

### Playwright-Browser kann nicht installiert werden

Installiere System-Abhängigkeiten:

**Ubuntu/Debian:**
```bash
sudo apt install libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 -y
python3 -m playwright install --with-deps chromium
```

**Fedora:**
```bash
sudo dnf install nss atk at-spi2-atk cups libdrm libxkbcommon libXcomposite libXdamage libXrandr mesa-libgbm pango cairo alsa-lib -y
python3 -m playwright install --with-deps chromium
```

### SQLite: "database is locked"

Stelle sicher, dass keine andere Anwendung die Datenbank nutzt:
```bash
pkill -f WeedDB
```

### Scraping schlägt fehl

- Prüfe Internetverbindung
- Stelle sicher, dass shop.dransay.com erreichbar ist
- Manchmal hilft ein Neustart des Terminals

### PATH-Probleme mit pip3/Python

Füge dies zu `~/.bashrc` oder `~/.zshrc` hinzu:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Dann:
```bash
source ~/.bashrc  # oder ~/.zshrc
```

---

## 📞 Hilfe bekommen

- **GitHub Issues:** https://github.com/laubfrosch-sudo/WeedDB/issues
- **Dokumentation:** Siehe `docs/` Ordner
- **README:** Lies die Hauptdatei `README.md`

---

**Viel Erfolg! 🌿**
