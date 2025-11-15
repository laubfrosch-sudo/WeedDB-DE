# 📋 **Dateien-Überarbeitungsplan für WeedDB-DE**

## 🎯 **Identifizierte Dateien, die Updates benötigen**

### 🗂️ **Zu bereinigende/entfernbare Dateien**

#### **Backup & Test-Dateien (können entfernt werden)**
- [ ] `scripts/add_product.py.backup` - Veraltetes Backup (36KB)
- [ ] `scripts/test_price_extraction.py` - Test-Datei (4.8KB)
- [ ] `scripts/test_single_update.py` - Test-Datei (710B)
- [ ] `scripts/test_small.txt` - Test-Datei (34B)
- [ ] `test_playwright.py` - Debug-Datei (kann entfernt werden)
- [ ] `debug_page.py` - Debug-Datei (kann entfernt werden)
- [ ] `debug_screenshot.png` - Debug-Screenshot (kann entfernt werden)
- [ ] `test_update.txt` - Temporäre Test-Datei

#### **Alternative/Experimentelle Scripts (zu konsolidieren)**
- [ ] `scripts/retry_mechanism.py` - **ERSATZ durch `error_handler.py`**
- [ ] `scripts/improved_price_extraction.py` - **INTEGRIERT in `add_product.py`**
- [ ] `scripts/scrape_product_list.py` - **ERSATZ durch `find_new_products.py`**

### 📚 **README-Dateien (zu aktualisieren)**

#### **data/_README.md**
- [ ] Neue Dateien erwähnen: `cache.db`, `logs/`, `reports/`
- [ ] Datenbank-Größe und Performance-Metriken hinzufügen
- [ ] Backup-Strategien dokumentieren

#### **docs/_README.md**
- [ ] PROCESS_STATUS.md als Live-Dashboard erwähnen
- [ ] Neue Unterordner dokumentieren
- [ ] Obsidian-Integration detaillierter beschreiben

#### **scripts/_README.md**
- [ ] Neue Scripts hinzufügen: `add_products_parallel.py`, `scheduler.py`, etc.
- [ ] Cron-Jobs und Automatisierung dokumentieren
- [ ] Performance-Vergleiche (sequentiell vs. parallel)

### ⚙️ **Konfigurationsdateien (zu aktualisieren)**

#### **requirements.txt**
- [ ] Fehlende Dependencies hinzufügen:
  - `tqdm` (für Fortschrittsbalken)
  - Eventuell `pathlib` (bereits in Python 3.4+)
- [ ] Versions-Pinning für bessere Reproduzierbarkeit

#### **.gitignore**
- [ ] Zusätzliche Muster:
  - `*.pyc` (obwohl `__pycache__/` schon da ist)
  - `data/cache.db*` (Cache-Dateien)
  - `data/reports/` (generierte Reports)
  - `.env` (falls Environment-Variablen verwendet werden)

### 🔧 **Scripts (zu optimieren)**

#### **add_product.py**
- [ ] Debug-Ausgaben entfernen (die print-Statements für Tests)
- [ ] Code-Duplikation reduzieren (mehrere Methoden für Preis-Extraktion)
- [ ] Error-Handling konsolidieren (besser mit error_handler.py integrieren)

#### **update_prices.py**
- [ ] Performance-Optimierung (parallel verarbeiten?)
- [ ] Bessere Fehlerbehandlung für Timeouts
- [ ] Logging integrieren

### 📊 **Dokumentation (zu erweitern)**

#### **CHANGELOG.md**
- [ ] Fehlende Einträge für kleinere Fixes hinzufügen
- [ ] Performance-Verbesserungen dokumentieren
- [ ] Breaking Changes markieren

#### **PROCESS_STATUS.md**
- [ ] Automatische Updates verbessern
- [ ] Mehr Metriken hinzufügen (Cache-Hit-Rate, etc.)
- [ ] DataView-Queries optimieren

### 🗃️ **Datenbank & Schema**

#### **data/schema.sql**
- [ ] Kommentare verbessern
- [ ] Indizes für Performance hinzufügen
- [ ] Constraints überprüfen

#### **Cache-System**
- [ ] `data/cache.db` in .gitignore aufnehmen
- [ ] Cache-Size-Limits definieren
- [ ] Cleanup-Strategien dokumentieren

---

## 🏗️ **Implementierungsplan**

### **Phase 1: Aufräumen (Sofort)**
```bash
# Entferne veraltete Dateien
rm scripts/add_product.py.backup
rm scripts/test_*.py
rm scripts/test_*.txt
rm test_playwright.py
rm debug_page.py
rm debug_screenshot.png

# Konsolidiere alternative Scripts
# (retry_mechanism.py → error_handler.py integrieren)
# (improved_price_extraction.py → add_product.py integrieren)
# (scrape_product_list.py → find_new_products.py integrieren)
```

### **Phase 2: Aktualisieren (1-2 Tage)**
```bash
# READMEs aktualisieren
# requirements.txt erweitern
# .gitignore verbessern
# CHANGELOG.md vervollständigen
```

### **Phase 3: Optimieren (2-3 Tage)**
```bash
# Scripts refactoren
# Performance-Verbesserungen
# Error-Handling konsolidieren
# Dokumentation finalisieren
```

---

## 📊 **Erwartete Verbesserungen**

### **Speicherplatz**
- **Vorher:** ~280KB (mit alten Dateien)
- **Nachher:** ~250KB (gereinigt)
- **Einsparung:** ~30KB

### **Code-Qualität**
- **Redundanz-Reduzierung:** 3 alternative Scripts konsolidiert
- **Test-Dateien:** 4 temporäre Dateien entfernt
- **Dokumentation:** Vollständig aktualisiert

### **Wartbarkeit**
- **READMEs:** Alle aktuell und vollständig
- **Dependencies:** Klar definiert und versioniert
- **Git-Ignore:** Umfassender Datei-Ausschluss

---

## ✅ **Prioritäten**

1. **Sofort entfernen:** Backup & Test-Dateien
2. **Konsolidieren:** Alternative Scripts zusammenführen
3. **Aktualisieren:** READMEs und Konfigurationen
4. **Optimieren:** Performance und Code-Qualität

---

## 🎯 **Status: PLAN ERSTELLT**

**Alle identifizierten Dateien sind katalogisiert. Warte auf Bestätigung für `/cleanup` um mit der Bereinigung zu beginnen.**

**Vorgeschlagene Aktionen:** 15 Dateien entfernen, 8 Dateien aktualisieren, 3 Scripts konsolidieren.