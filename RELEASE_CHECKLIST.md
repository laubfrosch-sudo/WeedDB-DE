---
created: 2025-11-15
updated: 2025-11-15
version: 1.0.0
author: laubfrosch-sudo
status: active
description: Comprehensive release and push checklist for WeedDB-DE
related_docs: [AGENTS.md, CHANGELOG.md]
---

# Release & Push Checklist - WeedDB-DE

**WICHTIG:** Diese Checkliste MUSS vor jedem `git push` und jedem Release durchgeführt werden. Sie stellt sicher, dass Code-Qualität, Sicherheit, Anonymität und Funktionalität gewährleistet sind.

**Letzte Aktualisierung:** 2025-11-15
**Version:** 1.0.0

---

## 🔒 SICHERHEIT & ANONYMITÄT (HÖCHSTE PRIORITÄT)

### Persönliche Daten & Anonymität
- [ ] **KEINE persönlichen Informationen** in Commits, Code oder Dokumentation
- [ ] **KEINE echten Namen, Adressen oder Kontaktdaten** in Beispieldaten
- [ ] **KEINE API-Schlüssel oder Credentials** in Code oder Config-Dateien
- [ ] **KEINE sensiblen URLs** oder Server-Informationen
- [ ] **Git-Konfiguration geprüft**: `git config --list` - keine persönlichen Daten
- [ ] **.gitignore überprüft**: Alle sensiblen Dateien ausgeschlossen

### Code-Sicherheit
- [ ] **Keine hartcodierten Secrets** in Python-Skripten
- [ ] **Keine Debug-Ausgaben** mit sensiblen Daten
- [ ] **SQL-Injection Schutz**: Alle Queries verwenden Parameterized Statements
- [ ] **Input-Validation**: Alle User-Inputs werden validiert
- [ ] **Error-Handling**: Keine sensitiven Informationen in Error-Messages

---

## 💻 CODE-QUALITÄT

### Type Safety & Linting
- [ ] **MyPy Type-Checking**: `python3 -m mypy scripts/*.py --strict` - 0 Fehler
- [ ] **Syntax-Prüfung**: Alle Python-Dateien syntaxfehlerfrei
- [ ] **Import-Prüfung**: Alle Imports funktionieren korrekt

### Funktionalität
- [ ] **Datenbank-Integrität**: `sqlite3 data/WeedDB.db "PRAGMA integrity_check;"` → "ok"
- [ ] **Kernskripte testen**:
  - [ ] `python3 scripts/generate_overview.py` → erfolgreich
  - [ ] `python3 scripts/add_product.py --help` → funktioniert
  - [ ] `python3 scripts/update_prices.py --help` → funktioniert
- [ ] **Dependencies**: `pip3 install -r requirements.txt` → erfolgreich

---

## 📚 DOKUMENTATION

### Pflichtdokumentation
- [ ] **README.md**: Aktuell, korrekte Version, vollständige Setup-Anleitung
- [ ] **CHANGELOG.md**: Alle Änderungen dokumentiert, korrektes Format
- [ ] **AGENTS.md**: AI-Assistenten Guidelines aktuell
- [ ] **Schema-Dokumentation**: `data/schema.sql` kommentiert und verständlich

### Release-spezifische Dokumentation
- [ ] **Release Notes**: `CHANGELOG/RELEASE_NOTES_Vx.x.x.md` vorhanden und vollständig
- [ ] **Versionsnummern**: Konsistent in allen Dateien (README, CHANGELOG, etc.)
- [ ] **Dependencies**: `requirements.txt` aktuell und vollständig

---

## 🗄️ DATEN & DATENBANK

### Datenintegrität
- [ ] **Datenbank-Schema**: Entspricht `data/schema.sql`
- [ ] **Testdaten**: Nur anonyme, fiktive Beispieldaten
- [ ] **Keine echten Preise/Personen**: Alle Daten sind generisch oder anonymisiert
- [ ] **Foreign Key Constraints**: Alle Beziehungen intakt

### Backup & Recovery
- [ ] **Datenbank-Backup**: Wichtige Daten gesichert vor Tests
- [ ] **Recovery-Skripte**: Funktionieren korrekt bei Datenverlust

---

## 🔧 SETUP & DEPENDENCIES

### Systemanforderungen
- [ ] **Python-Version**: 3.9+ kompatibel
- [ ] **SQLite-Version**: 3.x verfügbar
- [ ] **Playwright**: Chromium installierbar
- [ ] **Platform-Kompatibilität**: macOS, Linux, Windows berücksichtigt

### Installation
- [ ] **Clean Install Test**: Repository klonen und von Grund auf installieren
- [ ] **Setup-Skripte**: Alle Anleitungen funktionieren
- [ ] **Fehlerbehandlung**: Klare Fehlermeldungen bei Setup-Problemen

---

## 🏷️ GIT & GITHUB

### Commit-Qualität
- [ ] **Commit-Message**: Klar, beschreibend, auf Englisch
- [ ] **Atomic Commits**: Jeder Commit eine logische Änderung
- [ ] **Keine großen Binärdateien**: Assets < 10MB pro Datei
- [ ] **Branch-Name**: Beschreibend (feature/*, bugfix/*, etc.)

### Repository-Status
- [ ] **Git-Status**: `git status` - sauber, keine uncommitted changes
- [ ] **Branch**: Korrekter Branch für Push/Release
- [ ] **Remote**: `git remote -v` - korrekte URLs
- [ ] **Tags**: Bei Release - korrekter Tag-Name (vx.x.x)

---

## 🚀 RELEASE-SPEZIFISCHE CHECKS

### Vor Release
- [ ] **Version-Nummer**: Semantic Versioning (MAJOR.MINOR.PATCH)
- [ ] **Breaking Changes**: In CHANGELOG dokumentiert
- [ ] **Deprecation Warnings**: Für entfernte Features
- [ ] **Migration Guide**: Bei Datenbank-Änderungen

### Nach Release
- [ ] **Tag erstellt**: `git tag vx.x.x && git push origin vx.x.x`
- [ ] **GitHub Release**: Mit CHANGELOG-Inhalt erstellt
- [ ] **Branch Protection**: Main-Branch geschützt
- [ ] **CI/CD**: Automatisierte Checks aktiv

---

## 🧪 TESTING & VALIDATION

### Automatisierte Tests
- [ ] **Unit Tests**: Kritische Funktionen getestet (falls vorhanden)
- [ ] **Integration Tests**: Datenbank-Operationen funktionieren
- [ ] **End-to-End Tests**: Vollständige Workflows getestet

### Manuelle Tests
- [ ] **Happy Path**: Normale Nutzung funktioniert
- [ ] **Error Cases**: Fehler werden graceful behandelt
- [ ] **Edge Cases**: Grenzfälle berücksichtigt
- [ ] **Performance**: Grundlegende Performance akzeptabel

---

## 📋 CHECKLIST-VERWENDUNG

### Bei jedem Push
1. Diese Checkliste vollständig durchgehen
2. Alle Checks mit [x] markieren
3. Bei Fehlern: Probleme beheben, nicht ignorieren
4. Erst dann: `git push`

### Bei Releases
1. Zusätzlich zu Push-Checks
2. Release-spezifische Abschnitte durchführen
3. CHANGELOG und Release Notes finalisieren
4. Tag erstellen und pushen

### Verantwortlichkeit
- **Entwickler**: Führt Checkliste durch vor jedem Push
- **Reviewer**: Überprüft Checkliste bei Pull Requests
- **Release Manager**: Finale Validierung vor Release

---

## 🚨 NOTFALL-PROTOKOLL

Bei kritischen Sicherheitsproblemen:
1. **SOFORT stoppen** - keinen Code pushen
2. **Sicherheitsaudit** durchführen
3. **Betroffene Commits** reverten falls nötig
4. **Sicherheitsupdate** planen und kommunizieren

---

## 📞 SUPPORT & FEEDBACK

**Bei Fragen zur Checkliste:**
- AGENTS.md konsultieren
- GitHub Issues für Verbesserungsvorschläge
- Sicherheitsbedenken: Sofort melden

**Checklisten-Updates:**
- Bei Änderungen: Version erhöhen
- Alle Teammitglieder informieren
- In CHANGELOG dokumentieren

---

*Letzte Checkliste-Ausführung: _______________*
*Ausgeführt von: ___________________________*
*Ergebnis: _______________________________*