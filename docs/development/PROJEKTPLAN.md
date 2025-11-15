---
created: 2025-11-15
updated: 2025-11-15
version: 0.1.0
author: laubfrosch-sudo
status: alpha
description: Projektplan für die Entwicklung von WeedDB-DE
---

# Projektplan WeedDB-DE

**Version:** 0.1.0 (Alpha)  
**Datum:** 2025-11-15  
**Status:** Aktiv - Alpha Phase  
**Projektleiter:** laubfrosch-sudo  

## Projektübersicht

WeedDB-DE ist eine Datenbank für medizinisches Cannabis in Deutschland, die Produkte von verschiedenen Versandapotheken trackt. Die Daten stammen primär von shop.dransay.com und werden in einer SQLite-Datenbank gespeichert.

**Ziel:** Eine zuverlässige, automatisierte Plattform für Cannabis-Produkt-Tracking mit Fokus auf Preisverfolgung, Produktinformationen und therapeutische Anwendungen.

## Aktueller Stand (v0.1.0 Alpha)

### ✅ Abgeschlossen
- **Datenbankschema:** 3NF normalisierte SQLite-Datenbank implementiert
- **Kernfunktionalität:** Web-Scraping mit Playwright für shop.dransay.com
- **Preisverfolgung:** Dual-Kategorie-System (Top/All-Apotheken) mit historischen Daten
- **Automatisierung:** Grundlegende Scripts für Produkt-Hinzufügung und Preis-Updates
- **Dokumentation:** Umfassende Obsidian-optimierte Dokumentation
- **Repository:** Git-Setup mit GitHub-Integration

### 🔄 In Arbeit
- **Datenvalidierung:** Grundlegende Validierung implementiert, aber erweiterte Prüfungen fehlen
- **Fehlerbehandlung:** Basis-Retry-Mechanismen vorhanden, aber nicht vollständig
- **Testing:** Manuelle Tests durchgeführt, automatisierte Tests fehlen

### ❌ Ausstehend
- **Automatisierte Tests:** Unit-Tests, Integrationstests
- **Monitoring & Logging:** Zentrales Logging-System
- **Web-Interface:** Benutzeroberfläche für Datenbrowsing
- **API:** REST-API für externe Zugriffe
- **Performance-Optimierung:** Skalierbarkeit für große Datensätze
- **Sicherheit:** Input-Validation, Rate-Limiting für Scraping

## Meilensteine

### v0.1.0 (Aktuell - Alpha)
- Grundfunktionalität implementiert
- Basis-Dokumentation erstellt
- Repository-Struktur etabliert

### v0.2.0 (Beta - Q1 2026)
- Vollständige Testabdeckung
- Erweiterte Fehlerbehandlung
- Verbesserte Scraping-Reliabilität
- Logging und Monitoring

### v0.3.0 (Release Candidate - Q2 2026)
- Web-Interface (Grundversion)
- API-Endpoints
- Performance-Optimierungen

### v1.0.0 (Stable Release - Q3 2026)
- Produktionsreife Features
- Vollständige Dokumentation
- Community-Feedback integriert

## Risiken & Herausforderungen

### Hohes Risiko
- **Website-Änderungen:** shop.dransay.com könnte Layout ändern → Scraping bricht
- **Rechtliche Änderungen:** Cannabis-Regulierung in DE könnte sich ändern
- **Abhängigkeit:** Starke Abhängigkeit von einer Datenquelle

### Mittleres Risiko
- **Performance:** Bei vielen Produkten könnte Scraping langsam werden
- **Datenqualität:** Validierung der gescrapten Daten
- **Skalierbarkeit:** Datenbank-Performance bei Wachstum

### Geringes Risiko
- **Technologie-Stack:** Python/SQLite sind stabil
- **Community:** Kleines Projekt, geringe externe Abhängigkeiten

## Ressourcen

### Technisch
- **Sprachen:** Python 3.9+, SQL
- **Frameworks:** Playwright, SQLite3
- **Tools:** MyPy, Git, Obsidian.md

### Human
- **Entwickler:** 1 (laubfrosch-sudo)
- **Tester:** Manuell, zukünftig automatisiert
- **Dokumentation:** Selbstverwaltung

## Kommunikation

- **Repository:** https://github.com/laubfrosch-sudo/WeedDB-DE
- **Issues:** GitHub Issues für Bug-Reports und Feature-Requests
- **Dokumentation:** Obsidian-Vault in `docs/`

## Nächste Schritte

1. **Sofort (Diese Woche):**
   - Test-Suite implementieren
   - Erweiterte Validierung hinzufügen

2. **Kurzfristig (1-2 Wochen):**
   - Logging-System integrieren
   - Performance-Messungen durchführen

3. **Mittelfristig (1-3 Monate):**
   - Web-Interface planen
   - API-Design entwickeln

---

*Dieser Projektplan wird regelmäßig aktualisiert. Letzte Aktualisierung: 2025-11-15*

**Verwandte Dokumente:**
- [[AGENTS.md|AI-Assistenten Guidelines]]
- [[CHANGELOG/RELEASE_NOTES_V0.1.0.md|Release Notes v0.1.0]]
- [[docs/development/KANBAN.md|Kanban-Board]]