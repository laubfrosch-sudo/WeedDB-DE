---
created: 2025-11-15
updated: 2025-11-15
version: 1.5.1
author: Claude AI
status: stable
description: Datenvisualisierungen und Diagramme für WeedDB
---

# 📊 WeedDB Datenvisualisierungen

Diese Seite enthält automatisch generierte Diagramme und Visualisierungen der WeedDB-Daten.
**Letzte Aktualisierung:** 15.11.2025 01:31

## 📈 Preisverläufe

### Top-Produkte Preisverlauf
![Preisverlauf Top-Produkte](assets/charts/price_trends.png)
*Preisverlauf der 5 meistbewerteten Produkte über die letzten 30 Tage*

## 🧬 Produktverteilungen

### Genetik-Verteilung
![Genetik-Verteilung](assets/charts/genetics_distribution.png)
*Verteilung der Genetik-Typen (Indica, Sativa, Hybrid) in der Datenbank*

### THC-Gehalt-Verteilung
![THC-Verteilung](assets/charts/thc_distribution.png)
*Verteilung der THC-Prozentsätze in verschiedenen Bereichen*

### Bewertungsverteilung
![Bewertungsverteilung](assets/charts/rating_distribution.png)
*Verteilung der Kundenbewertungen (1-5 Sterne)*

## 📋 Statistiken Übersicht

| Metrik | Wert |
|--------|------|
| Gesamtprodukte | 32 |
| Durchschnittliche Bewertung | 3.98 ⭐ |
| Höchster THC-Gehalt | 30%+ |
| Niedrigster THC-Gehalt | < 20% |

## 🔄 Automatische Generierung

Diese Diagramme werden automatisch mit dem Skript `generate_charts.py` erstellt:

```bash
python3 scripts/generate_charts.py
```

Das Skript sollte nach jeder größeren Datenbank-Aktualisierung ausgeführt werden, um die Visualisierungen aktuell zu halten.
