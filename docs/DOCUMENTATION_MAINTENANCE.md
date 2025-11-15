---
created: 2025-11-15
updated: 2025-11-15
version: 0.1.0
author: Claude AI
status: alpha
description: Richtlinien für die Pflege und Aktualisierung der WeedDB-Dokumentation
---

# Dokumentations-Wartung & Metadata-Richtlinien

> **Wichtig:** Diese Richtlinien gelten für ALLE Markdown-Dateien im WeedDB-Repository.

## 📋 Übersicht

Jede Dokumentationsdatei im WeedDB-Repository **MUSS** YAML-Frontmatter mit Metadaten enthalten. Diese Metadaten helfen bei:

- ✅ Versionskontrolle und Changelog-Tracking
- ✅ Erkennung veralteter Dokumentation
- ✅ Nachverfolgung von Änderungen
- ✅ Obsidian-Integration (Dataview-Queries)
- ✅ Automatischen Wartungs-Checks

---

## 📝 YAML-Frontmatter Standard

### Pflichtfelder (für alle Dokumentations-Dateien):

```yaml
---
created: YYYY-MM-DD        # Datum der Erstellung
updated: YYYY-MM-DD        # Datum der letzten Änderung
version: X.X.X             # WeedDB-Version (z.B. 1.5.0)
author: Name               # Ersteller (GitHub Username oder "Claude AI")
status: stable|draft|deprecated  # Dokumentations-Status
description: Kurzbeschreibung     # 1-Satz Beschreibung des Inhalts
---
```

### Optionale Felder (je nach Dokumenttyp):

```yaml
platform: macOS|Linux|Windows     # Für OS-spezifische Guides
target_audience: Anfänger|Fortgeschritten|Entwickler
language: de|en                    # Sprache der Dokumentation
related_docs: [file1.md, file2.md]  # Verwandte Dokumente
changelog_url: link                # Link zu detailliertem Changelog
repository: GitHub-URL             # Nur für README.md
```

---

## 🔄 Wann müssen Metadaten aktualisiert werden?

### 1. **Bei JEDER inhaltlichen Änderung:**

**Regel:** Sobald du eine Datei bearbeitest, **MUSST** du das `updated`-Feld aktualisieren!

```yaml
# VORHER:
updated: 2025-11-10

# NACHHER (nach Bearbeitung am 15.11.):
updated: 2025-11-15
```

**Beispiele für inhaltliche Änderungen:**
- ✅ Text hinzufügen/entfernen
- ✅ Code-Beispiele aktualisieren
- ✅ Links korrigieren
- ✅ Formatierung verbessern
- ✅ Fehler beheben

**NICHT als inhaltliche Änderung zählt:**
- ❌ Reine Whitespace-Änderungen
- ❌ Kommentare in HTML/CSS
- ❌ Automatische Formatierung durch Linter

---

### 2. **Bei Version-Updates:**

Wenn eine neue WeedDB-Version released wird (z.B. 1.5.0 → 1.6.0):

1. Prüfe **ALLE** Dokumentationsdateien auf Relevanz
2. Aktualisiere betroffene Dateien inhaltlich
3. Setze `version: 1.6.0` in den bearbeiteten Dateien
4. Aktualisiere `updated`-Datum

**Automatisierung (in Arbeit):**
```bash
# Zukünftiges Skript (TODO):
python scripts/update_docs_version.py --new-version 1.6.0
```

---

### 3. **Bei Status-Änderungen:**

#### Status-Definitionen:

| Status | Bedeutung | Aktion erforderlich |
|--------|-----------|---------------------|
| `draft` | In Arbeit, nicht final | Review vor Veröffentlichung |
| `stable` | Geprüft, aktuell, produktionsbereit | Regelmäßige Updates bei Änderungen |
| `deprecated` | Veraltet, ersetzt durch neue Datei | Entfernen oder archivieren |
| `review` | Wartet auf Review | Manuelles Review erforderlich |

**Beispiel:**
```yaml
# Alte Anleitung für v1.3.0:
status: deprecated
deprecated_by: docs/user-guides/BEGINNER_SETUP_MACOS.md
deprecated_date: 2025-11-15
```

---

## 📂 Welche Dateien brauchen Frontmatter?

### ✅ Frontmatter PFLICHT für:

- `README.md` (Root)
- `START.md`
- `CLAUDE.md`, `GEMINI.md` (und Versionen in docs/)
- Alle Dateien in `docs/user-guides/`
- Alle Dateien in `docs/ai-assistants/`
- Alle Dateien in `docs/development/`
- `docs/QUERY_EXAMPLES.md`
- `ANLEITUNG.md`, `INSTRUCTIONS.md`

### ❌ Frontmatter NICHT nötig für:

- Automatisch generierte Dateien (`docs/generated/SORTEN_ÜBERSICHT.md`)
- Template-Dateien (`docs/templates/*.md`)
- Git-Dateien (`.gitignore`, `.github/*`)
- Python-Skripte (`*.py`)
- Datenbank-Schema (`data/schema.sql`)

**Ausnahme:** Generierte Dateien können ein spezielles "generated"-Frontmatter haben:

```yaml
---
generated: true
generated_by: scripts/generate_overview.py
generated_at: 2025-11-15 14:30:00
source_db: data/WeedDB.db
---
```

---

## 🤖 Richtlinien für AI-Assistenten

### Wenn du eine Datei bearbeitest:

1. **IMMER zuerst Frontmatter prüfen:**
   ```bash
   # Lies die ersten 15 Zeilen:
   head -n 15 docs/user-guides/ANLEITUNG.md
   ```

2. **Updated-Datum aktualisieren:**
   ```yaml
   updated: 2025-11-15  # Heutiges Datum
   ```

3. **Version prüfen:**
   - Stimmt `version: 1.4.0` mit aktueller WeedDB-Version überein?
   - Falls nicht: Inhalt auf Aktualität prüfen!

4. **Status prüfen:**
   - `deprecated` → Warnung an User, dass Datei veraltet ist
   - `draft` → Darauf hinweisen, dass Datei noch in Arbeit ist

### Wenn du eine NEUE Datei erstellst:

```yaml
---
created: 2025-11-15      # Heutiges Datum
updated: 2025-11-15      # Gleich wie 'created' bei neuen Dateien
version: 1.4.0           # Aktuelle WeedDB-Version
author: Claude AI        # Oder GitHub Username
status: stable           # Oder 'draft' wenn noch nicht final
description: Kurze Beschreibung was die Datei enthält
---
```

### Syncing zwischen CLAUDE.md und GEMINI.md:

**Wichtig:** CLAUDE.md und GEMINI.md sollten **synchron** bleiben (siehe Hinweis in den Dateien selbst).

**Bei Änderung an CLAUDE.md:**
1. Aktualisiere auch GEMINI.md
2. Setze `updated`-Datum in **BEIDEN** Dateien auf dasselbe Datum
3. Prüfe dass beide denselben `version`-Wert haben

**Automatisierung (TODO):**
```bash
# Zukünftiges Skript:
python scripts/sync_ai_docs.py
```

---

## 🔍 Wartungs-Checks

### Monatlicher Check (Empfohlen):

```bash
# 1. Finde Dateien die älter als 90 Tage sind:
find docs -name "*.md" -type f -exec grep -l "updated:" {} \; | \
  xargs grep "updated:" | \
  awk -F: '{if ($3 < "'$(date -d '90 days ago' +%Y-%m-%d)'") print $1}'

# 2. Finde Dateien mit falscher Version:
grep -r "version: 1.3.0" docs/

# 3. Finde Dateien im Draft-Status:
grep -r "status: draft" docs/
```

### Automatischer CI-Check (TODO):

```yaml
# .github/workflows/docs-check.yml
name: Documentation Metadata Check

on: [push, pull_request]

jobs:
  check-metadata:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check frontmatter
        run: python scripts/check_frontmatter.py
```

---

## 📊 Obsidian Dataview-Queries

### Alle Dokumente nach Update-Datum sortiert:

```dataview
TABLE
  updated as "Letztes Update",
  version as "Version",
  status as "Status"
FROM "docs"
WHERE file.frontmatter.updated
SORT updated DESC
```

### Veraltete Dokumente finden (> 90 Tage):

```dataview
TABLE
  updated as "Letztes Update",
  date(now) - date(updated) as "Tage alt"
FROM "docs"
WHERE file.frontmatter.updated
WHERE date(now) - date(updated) > dur(90 days)
SORT updated ASC
```

### Dokumente im Draft-Status:

```dataview
LIST description
FROM "docs"
WHERE status = "draft"
SORT created DESC
```

### Deprecated Dokumente:

```dataview
TABLE
  deprecated_by as "Ersetzt durch",
  deprecated_date as "Seit"
FROM "docs"
WHERE status = "deprecated"
```

---

## 🛠️ Tools & Skripte (Geplant)

### 1. `scripts/check_frontmatter.py`

Prüft alle Markdown-Dateien auf:
- Vorhandensein von Frontmatter
- Pflichtfelder (created, updated, version, author, status, description)
- Gültiges Datumsformat (YYYY-MM-DD)
- Version entspricht aktueller WeedDB-Version

**Usage:**
```bash
python scripts/check_frontmatter.py
# Output: Liste aller Dateien mit fehlenden/ungültigen Metadaten
```

---

### 2. `scripts/update_docs_version.py`

Massenupdate der Version in allen Dokumenten:

```bash
python scripts/update_docs_version.py --new-version 1.5.0 --dry-run
# Zeigt Vorschau was geändert würde

python scripts/update_docs_version.py --new-version 1.5.0
# Führt Update durch
```

---

### 3. `scripts/sync_ai_docs.py`

Synchronisiert CLAUDE.md und GEMINI.md:

```bash
python scripts/sync_ai_docs.py --check
# Prüft ob Dateien synchron sind

python scripts/sync_ai_docs.py --sync
# Synchronisiert Metadaten zwischen beiden Dateien
```

---

## 📜 Changelog-Format (für größere Updates)

Bei größeren Dokumentations-Änderungen, füge einen Changelog-Eintrag am Ende der Datei hinzu:

```markdown
---

## 📝 Changelog

### 2025-11-15 (v1.4.0)
- Added: Obsidian theme recommendations
- Updated: Installation instructions for Python 3.11
- Fixed: Broken links to QUERY_EXAMPLES.md

### 2025-10-20 (v1.3.0)
- Added: Multi-pharmacy price comparison section
- Updated: Database schema documentation

### 2025-09-15 (v1.2.0)
- Initial documentation created
```

---

## ⚠️ Wichtige Hinweise

### 1. **Niemals `created`-Datum ändern!**
Das `created`-Datum ist **unveränderlich** und zeigt die ursprüngliche Erstellung.

### 2. **`updated` bei jedem Edit!**
Auch bei kleinsten Änderungen muss `updated` aktualisiert werden!

### 3. **Version-Synchronität**
Alle Docs sollten auf der aktuellen WeedDB-Version sein. Bei Major-Updates (1.x.0 → 2.0.0) alle Docs reviewen!

### 4. **Status sorgfältig setzen**
- `draft` → Nur für unfertige Docs
- `stable` → Standard für produktionsbereite Docs
- `deprecated` → Immer mit `deprecated_by` angeben!

---

## 📞 Fragen?

Bei Unklarheiten zur Dokumentations-Wartung:
- **GitHub Issues:** https://github.com/laubfrosch-sudo/WeedDB/issues
- **Maintainer:** @laubfrosch-sudo

---

**Letzte Aktualisierung dieser Richtlinien:** 2025-11-15
