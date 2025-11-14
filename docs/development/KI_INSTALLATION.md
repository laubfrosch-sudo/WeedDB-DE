# KI-Installation: Eine Anleitung für das KI-gestützte Terminal

Dieses Dokument dient als erste Hilfestellung, um deinen Computer für die Interaktion mit KI-Assistenten (wie Gemini, Claude oder Open-Source-Modellen) direkt im Terminal vorzubereiten. Ziel ist es, dir zu ermöglichen, die `WeedDB`-Datenbank mithilfe von KI zu verwalten und abzufragen.

## Übersicht der Komponenten

1.  **Modernes Terminal**: Eine leistungsstarke Kommandozeile ist die Basis.
2.  **System-Abhängigkeiten**: Software, die das Projekt benötigt (z.B. Python, SQLite).
3.  **Projekteinrichtung**: Das lokale Einrichten der `WeedDB`.
4.  **KI-Tools**: Die Einrichtung von Werkzeugen für den Zugriff auf KI-Modelle.

---

## Schritt 1: Betriebssystem-spezifische Einrichtung

Wähle die Anleitung für dein Betriebssystem.

### macOS

1.  **Package Manager (Homebrew) installieren**: Homebrew ist unerlässlich für die einfache Installation von Software auf macOS. Öffne die vorinstallierte `Terminal.app` und führe folgenden Befehl aus:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Modernes Terminal (iTerm2) installieren**: iTerm2 ist eine beliebte Alternative zum Standard-Terminal.
    ```bash
    brew install --cask iterm2
    ```
    *Öffne ab jetzt immer iTerm2 anstelle des Standard-Terminals.*

3.  **Python & SQLite installieren**:
    ```bash
    brew install python sqlite
    ```

### Windows

Für Windows ist die empfohlene Methode das **Windows Subsystem for Linux (WSL)**, da es eine nahtlose Linux-Umgebung bereitstellt, die von Entwicklern bevorzugt wird.

1.  **Windows Terminal installieren**: Lade das "Windows Terminal" aus dem Microsoft Store. Es ist eine moderne Oberfläche für alle deine Kommandozeilen.

2.  **WSL installieren**: Öffne das Windows Terminal (als Administrator) und installiere WSL mit dem Standard-Linux (Ubuntu).
    ```powershell
    wsl --install
    ```
    Nach einem Neustart wirst du aufgefordert, einen Benutzernamen und ein Passwort für deine neue Linux-Umgebung zu erstellen.

3.  **Abhängigkeiten in WSL installieren**: Öffne das Windows Terminal mit einem Ubuntu/WSL-Tab und fahre mit der Linux-Anleitung fort.

### Linux (Debian / Ubuntu)

1.  **System aktualisieren**:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2.  **Python & SQLite installieren**:
    ```bash
    sudo apt install python3 python3-pip sqlite3 git -y
    ```

---

## Schritt 2: Projekteinrichtung

Diese Schritte sind für alle Betriebssysteme gleich (auf Windows werden sie innerhalb von WSL/Ubuntu ausgeführt).

1.  **Projekt-Verzeichnis klonen** (falls noch nicht geschehen):
    ```bash
    # Ersetze <repository_url> mit der tatsächlichen URL
    git clone https://github.com/laubfrosch-sudo/WeedDB.git
    cd WeedDB
    ```

2.  **Python-Abhängigkeiten installieren**: Das Projekt nutzt `playwright` für das Web-Scraping.
    ```bash
    pip3 install playwright
    ```

3.  **Playwright-Browser installieren**:
    ```bash
    python3 -m playwright install
    ```

4.  **Datenbank initialisieren**: Erstellt die `WeedDB.db`-Datei und die Tabellenstruktur.
    ```bash
    sqlite3 WeedDB.db < schema.sql
    ```

---

## Schritt 3: Einrichtung der KI-Assistenten

### Proprietäre Modelle (Gemini, Claude)

Die Interaktion mit kommerziellen Modellen wie Gemini und Claude, die du vielleicht gerade nutzt, ist oft in eine spezielle Entwicklungsumgebung oder ein Tool integriert. Es gibt in der Regel keine einfache, öffentliche "Gemini CLI" oder "Claude CLI" zum Herunterladen.

Für die eigene Nutzung in Skripten würdest du:
1.  Einen **API-Schlüssel** vom jeweiligen Anbieter (Google, Anthropic) erhalten.
2.  Diesen Schlüssel als Umgebungsvariable setzen (z.B. `export GOOGLE_API_KEY="DEIN_SCHLÜSSEL"`).
3.  Die entsprechende Client-Bibliothek in Python verwenden, um Anfragen an die KI zu senden.

**Für dieses Projekt ist die Interaktion bereits durch das verwendete Terminal-Tool gegeben.**

### OpenCode - Dein KI-Coding-Assistent

**OpenCode** ist das primäre KI-Tool für die Interaktion mit diesem Projekt. Es bietet spezialisierte Unterstützung für Softwareentwicklung und Datenbank-Management.

#### Warum OpenCode?
- **Spezialisiert auf Code**: Optimiert für Programmierung und technische Aufgaben
- **Projekt-Kontext**: Kennt die WeedDB-Struktur und verfügbare Scripts
- **Direkte Terminal-Integration**: Arbeitet nahtlos mit deinen lokalen Dateien
- **Sicherheit**: Lokale Verarbeitung ohne Cloud-Abhängigkeiten

#### OpenCode verwenden:
1. **Starte OpenCode** in deinem Terminal
2. **Navigiere zum Projekt**: `cd /path/to/WeedDB`
3. **Frage nach Hilfe**: "Wie füge ich ein neues Produkt hinzu?" oder "Aktualisiere alle Preise"

#### Beispiel-Interaktionen:
```bash
# Produkt hinzufügen
opencode: "Füge das Produkt 'Blue Dream' zur Datenbank hinzu"

# Datenbank abfragen
opencode: "Zeige mir die 5 teuersten Produkte"

# Code-Analyse
opencode: "Optimiere das add_product.py Script"
```

### Grok Code - Alternative KI-Unterstützung

**Grok Code** bietet eine alternative KI-Unterstützung mit Fokus auf erklärendem und hilfreichem Coding.

#### Grok Code Features:
- **Erklärende Antworten**: Detaillierte Erklärungen von Code und Konzepten
- **Breites Wissen**: Umfassende Kenntnisse in verschiedenen Programmiersprachen
- **Interaktive Hilfe**: Schritt-für-Schritt Anleitungen
- **Code-Generierung**: Automatische Erstellung von Code-Snippets

#### Grok Code für WeedDB:
- **Datenbank-Abfragen**: "Wie erstelle ich eine SQL-Abfrage für alle Indica-Sorten?"
- **Script-Optimierung**: "Verbessere die Performance von update_prices.py"
- **Fehlerbehebung**: "Warum funktioniert das Scraping nicht?"

---

## Schritt 4: Alles zusammenführen

Nachdem du diese Schritte befolgt hast, ist dein System vollständig eingerichtet. Du kannst nun:
- Die Python-Skripte im Projekt ausführen (`python3 scripts/update_prices.py` etc.).
- Mit **OpenCode** interagieren, um die Datenbank zu verwalten und Code zu entwickeln.
- **Grok Code** als alternative KI-Unterstützung für komplexe Fragen nutzen.

Weitere Details zur Interaktion mit dem Assistenten findest du in der `ANLEITUNG.md`.

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
