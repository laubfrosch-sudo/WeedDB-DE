# Anleitung zur Interaktion mit dem KI-Assistenten

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

Dieses Dokument erklärt, wie du mit einem KI-Assistenten (wie Gemini oder Claude) in diesem Verzeichnis interagieren kannst, um die `WeedDB`-Datenbank zu nutzen, abzufragen und zu verwalten. Der Assistent kennt die Projektstruktur, die verfügbaren Skripte und das Datenbankschema.

## 1. Datenbank abfragen

Du kannst Fragen in natürlicher Sprache stellen, um Informationen aus der Datenbank zu erhalten. Der Assistent wird die passenden Abfragen ausführen und dir die Ergebnisse präsentieren.

**Beispiele für Abfragen:**

*   `Welche Sorte hat das beste Preis-Leistungs-Verhältnis, um high zu werden?`
*   `Zeig mir die Top 5 Sorten mit dem höchsten THC-Gehalt.`
*   `Was ist die URL für "Grape Face"?`
*   `Welche Sorten haben einen erdigen Geschmack und wirken entspannend?`

## 2. Daten aktualisieren und verwalten

Der Assistent kann die Datenbank für dich pflegen, indem er die vorhandenen Skripte ausführt.

### Alle Produkte aktualisieren

Wenn die Preise oder andere Daten in der Datenbank veraltet sind, kannst du eine vollständige Aktualisierung anstoßen.

**Beispiel-Anweisung:**

*   `Passe jetzt alle Datensätze nochmal richtig an gemäß der richtigen Websites.`
*   `Aktualisiere die komplette Datenbank.`

Der Assistent wird daraufhin das Skript `update_all_products.py` ausführen.

### Einzelne Produkte hinzufügen

Du kannst neue Sorten von `shop.dransay.com` hinzufügen, indem du dem Assistenten einfach die URL gibst.

**Beispiel-Anweisung:**

*   `Füge dieses Produkt hinzu: <URL des Produkts>`

### Daten korrigieren

Wenn du einen Fehler in den Daten findest (z.B. einen falschen THC-Wert), kannst du den Assistenten bitten, diesen zu korrigieren.

**Beispiel-Anweisung:**

*   `Der THC-Wert für "Big Purple Dragon" von Remexian ist 22%, nicht 30%. Bitte korrigiere das.`

## 3. Übersichtsdatei (`SORTEN_ÜBERSICHT.md`)

Die Datei `SORTEN_ÜBERSICHT.md` ist eine dynamisch generierte Übersicht aller Produkte in der Datenbank. Du kannst den Assistenten bitten, diese Datei zu aktualisieren oder anzupassen.

### Übersicht neu generieren

Nach einer größeren Datenaktualisierung sollte die Übersicht neu erstellt werden, um die Änderungen widerzuspiegeln.

**Beispiel-Anweisung:**

*   `Generiere die Übersichtsdatei neu.`
*   `Aktualisiere die Markdown-Übersicht.`

### Übersicht anpassen

Du kannst auch Wünsche zur Gestaltung der Übersicht äußern.

**Beispiel-Anweisung:**

*   `Kannst du in der Übersicht die Sorten highlighten, die in irgendeiner Kategorie am besten sind?`
*   `Füge der Bestenliste auch Links zu den jeweiligen Produktseiten hinzu.`
*   `Die restlichen Sorten in der großen Tabelle sollten auch alle Links haben.`
