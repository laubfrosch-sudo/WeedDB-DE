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

### Open-Source-Modelle (via Ollama)

Mit **Ollama** kannst du leistungsstarke Open-Source-Modelle (wie Llama 3, Code Llama) direkt auf deinem eigenen Computer ausführen. Dies ist eine exzellente Möglichkeit, einen lokalen KI-Assistenten im Terminal zu haben.

1.  **Ollama installieren**:
    *   **macOS**: Lade die App von [ollama.com](https://ollama.com) herunter oder nutze Homebrew: `brew install ollama`.
    *   **Windows**: Lade die `.exe`-Datei von [ollama.com](https://ollama.com) herunter.
    *   **Linux**: Führe das Installations-Skript aus: `curl -fsSL https://ollama.com/install.sh | sh`.

2.  **Ein Modell herunterladen und ausführen**: Nach der Installation kannst du ein Modell deiner Wahl herunterladen. `llama3` ist ein guter Startpunkt.
    ```bash
    # Lädt das Modell herunter (beim ersten Mal) und startet eine Chat-Sitzung
    ollama run llama3
    ```

3.  **Modell nutzen**: Du kannst Ollama nun jederzeit im Terminal für allgemeine Fragen oder zur Code-Analyse verwenden.

---

## Schritt 4: Alles zusammenführen

Nachdem du diese Schritte befolgt hast, ist dein System vollständig eingerichtet. Du kannst nun:
- Die Python-Skripte im Projekt ausführen (`python3 update_all_products.py` etc.).
- Mit dem integrierten KI-Assistenten interagieren, um die Datenbank zu verwalten.
- `Ollama` für lokale KI-Aufgaben nutzen.

Weitere Details zur Interaktion mit dem Assistenten findest du in der `ANLEITUNG.md`.
