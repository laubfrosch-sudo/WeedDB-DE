---
created: 2024-02-01
updated: 2025-11-15
version: 0.1.0
author: laubfrosch-sudo
status: alpha
language: de
target_audience: Alle User
description: Anleitung zur Interaktion mit KI-Assistenten (Claude/Gemini) für WeedDB-Verwaltung
sync_with: INSTRUCTIONS.md
---

# Anleitung zur Interaktion mit dem KI-Assistenten (v0.1.0 Alpha)

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

Dieses Dokument erklärt, wie du mit einem KI-Assistenten (wie Gemini oder Claude) in diesem Verzeichnis interagieren kannst, um die `WeedDB`-Datenbank zu nutzen, abzufragen und zu verwalten. Der Assistent kennt die Projektstruktur, die verfügbaren Skripte und das Datenbankschema.

**Neuerungen:**
- Verbesserte Batch-Verarbeitung mit Timeout-Schutz
- Automatische Datenkorrektur für fehlende Hersteller
- Erweiterte Producer-Erkennung (24+ bekannte Hersteller)
- Robuste Preis-Extraktion mit mehreren Fallback-Methoden

## 1. Datenbank abfragen

Du kannst Fragen in natürlicher Sprache stellen, um Informationen aus der Datenbank zu erhalten. Der Assistent wird die passenden Abfragen ausführen und dir die Ergebnisse präsentieren.

**Beispiele für Abfragen:**

*   `Welche Sorte hat das beste Preis-Leistungs-Verhältnis, um high zu werden?`
*   `Zeig mir die Top 5 Sorten mit dem höchsten THC-Gehalt.`
*   `Was ist die URL für "Grape Face"?`
*   `Welche Sorten haben einen erdigen Geschmack und wirken entspannend?`
*   **NEU:** `Vergleiche die Preise für "Gelato" über alle Apotheken.`
*   **NEU:** `Welche Apotheke hat insgesamt die günstigsten Preise?`
*   **NEU:** `Zeig mir Produkte mit den größten Preisunterschieden zwischen Apotheken.`

**Erweiterte Abfragen:**

Für umfassende SQL-Abfrage-Beispiele (60+ Beispiele), siehe `QUERY_EXAMPLES.md`. Dies umfasst:
- Multi-Apotheken-Preisvergleiche
- Produktsuche nach Terpenen, Effekten und therapeutischen Anwendungen
- Statistiken und Analysen
- Best-Value-Berechnungen (THC-zu-Preis-Verhältnis)

## 2. Daten aktualisieren und verwalten

Der Assistent kann die Datenbank für dich pflegen, indem er die vorhandenen Skripte ausführt.

### Alle Produkte aktualisieren

Wenn die Preise oder andere Daten in der Datenbank veraltet sind, kannst du eine vollständige Aktualisierung anstoßen.

**Beispiel-Anweisung:**

*   `Passe jetzt alle Datensätze nochmal richtig an gemäß der richtigen Websites.`
*   `Aktualisiere die komplette Datenbank.`
*   `Führe eine vollständige Datenbank-Aktualisierung durch.`

Der Assistent wird daraufhin das Skript `update_prices.py` ausführen, das alle Produkte in kleinen Batches verarbeitet, um Timeouts zu vermeiden.

**Neue Option:**
*   `Korrigiere fehlende Hersteller-Daten automatisch.`

Führt das neue `fix_producers.py` Script aus, das automatisch fehlende Producer-Informationen korrigiert.

### Einzelne Produkte hinzufügen

Du kannst neue Sorten von `shop.dransay.com` hinzufügen, indem du dem Assistenten einfach die URL gibst.

**Beispiel-Anweisung:**

*   `Füge dieses Produkt hinzu: <URL des Produkts>`

### Daten korrigieren

Wenn du einen Fehler in den Daten findest (z.B. einen falschen THC-Wert), kannst du den Assistenten bitten, diesen zu korrigieren.

**Beispiel-Anweisung:**

*   `Der THC-Wert für "Big Purple Dragon" von Remexian ist 22%, nicht 30%. Bitte korrigiere das.`

## 3. Übersichtsdatei (`docs/generated/SORTEN_ÜBERSICHT.md`)

Die Datei `docs/generated/SORTEN_ÜBERSICHT.md` ist eine dynamisch generierte Übersicht aller Produkte in der Datenbank. Du kannst den Assistenten bitten, diese Datei zu aktualisieren oder anzupassen.

### Übersicht neu generieren

Nach einer größeren Datenaktualisierung sollte die Übersicht neu erstellt werden, um die Änderungen widerzuspiegeln.

**Beispiel-Anweisung:**

*   `Generiere die Übersichtsdatei neu.`
*   `Aktualisiere die Markdown-Übersicht.`

### Übersicht anpassen

Du kannst auch Wünsche zur Gestaltung der Übersicht äußern.

**Beispiel-Anweisung:**

*   `Erstelle eine separate Übersicht nur für Indica-Sorten, sortiert nach THC-Gehalt.`
*   `Füge eine Spalte für die Top-3 Terpene zu jeder Sorte hinzu.`
*   `Zeige in der Übersicht auch die Hersteller-Information an.`
*   `Erstelle eine Preisvergleichs-Tabelle mit den günstigsten 3 Apotheken pro Produkt.`
*   `Gruppiere die Sorten nach Genetik (Indica/Sativa/Hybrid) in separaten Tabellen.`
*   `Füge eine Spalte mit therapeutischen Anwendungen hinzu.`
