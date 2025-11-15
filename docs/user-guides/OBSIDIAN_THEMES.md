---
created: 2025-11-15
updated: 2025-11-15
version: 1.5.1
author: Claude AI
status: stable
target_audience: Obsidian-User
description: Themes, Plugins, CSS-Snippets und Layout-Optimierungen für WeedDB in Obsidian
---

# Obsidian Design-Guide für WeedDB 🎨

> **Verwandle dein WeedDB-Vault in eine wunderschöne, übersichtliche Cannabis-Wissensdatenbank!**

Dieser Guide zeigt dir, wie du Obsidian für WeedDB optimal einrichtest mit schönen Themes, nützlichen Plugins und praktischen Layouts.

---

## 📖 Inhaltsverzeichnis

1. [Schöne Themes](#schöne-themes)
2. [Empfohlene Plugins](#empfohlene-plugins)
3. [CSS-Snippets für WeedDB](#css-snippets-für-weeddb)
4. [Optimale Layout-Einstellungen](#optimale-layout-einstellungen)
5. [Workspace-Setups](#workspace-setups)

---

## 🎨 Schöne Themes

### Top 5 Themes für WeedDB:

#### 1. **Minimal** (Empfehlung!)
- **Warum:** Clean, modern, fokussiert auf Lesbarkeit
- **Perfekt für:** Produktübersichten und Datenbanken
- **Features:** Anpassbare Farben, mehrere Styles (Atom, Nord, etc.)

**Installation:**
1. Settings → Appearance → Themes → "Manage"
2. Suche "Minimal"
3. Klicke "Install and use"
4. Installiere auch "Minimal Theme Settings" Plugin für mehr Kontrolle

**Empfohlene Einstellungen für WeedDB:**
- Color scheme: "Atom" oder "Gruvbox" (grün passt zu Cannabis! 🌿)
- Text labels: Normal
- Image width: Full line width (für das Logo!)
- Table font size: 90% (kompaktere Produkttabellen)

---

#### 2. **Things**
- **Warum:** macOS-like Design, sehr poliert
- **Perfekt für:** Mac-User die ein natives Look & Feel wollen
- **Features:** Saubere Icons, minimalistische Sidebar

**Installation:** Settings → Appearance → Themes → "Things"

---

#### 3. **Sanctum**
- **Warum:** Warm, gemütlich, perfekt fürs Lesen
- **Perfekt für:** Lange Sessions beim Durchstöbern der Sorten
- **Features:** Warme Farben, gute Kontraste

**Installation:** Settings → Appearance → Themes → "Sanctum"

---

#### 4. **AnuPpuccin**
- **Warum:** Moderne Catppuccin-Farben, super customizable
- **Perfekt für:** User die Pastellfarben mögen
- **Features:** 4 Farbvarianten (Latte, Frappé, Macchiato, Mocha)

**Installation:** Settings → Appearance → Themes → "AnuPpuccin"

---

#### 5. **Border**
- **Warum:** Einzigartige Border-basierte UI
- **Perfekt für:** Experimentierfreudige User
- **Features:** Innovative Layouts, viel Whitespace

**Installation:** Settings → Appearance → Themes → "Border"

---

## 🔌 Empfohlene Plugins

### Essential Plugins für WeedDB:

#### **1. Dataview** (Must-have!)
Erstelle dynamische Produktlisten direkt in Markdown.

```markdown
## Alle Indica-Sorten
```dataview
TABLE thc_percent as "THC%", rating as "★", price as "€/g"
FROM "docs/generated"
WHERE genetics = "Indica"
SORT rating DESC
```

**Installation:** Settings → Community plugins → Browse → "Dataview"

---

#### **2. Advanced Tables**
Macht Tabellen bearbeiten 100x einfacher!

**Features:**
- Auto-formatierung
- Sortieren mit einem Klick
- Zeilen/Spalten einfügen mit Shortcuts

**Installation:** Settings → Community plugins → "Advanced Tables"

---

#### **3. Obsidian Git** (Für Backup!)
Automatisches Backup deiner WeedDB-Daten zu GitHub.

**Installation:** Settings → Community plugins → "Obsidian Git"

**Setup:**
1. Initialisiere Git in deinem WeedDB-Ordner (falls noch nicht geschehen)
2. Plugin-Settings → Backup interval: 10 minutes
3. Automatisches Push/Pull aktivieren

---

#### **4. Excalidraw** (Für Diagramme)
Zeichne Strain-Familienbäume, Terpene-Wheels, etc.!

**Installation:** Settings → Community plugins → "Excalidraw"

---

#### **5. Kanban**
Tracke welche Sorten du probieren willst!

**Installation:** Settings → Community plugins → "Kanban"

**Beispiel-Board:**
```
## Meine Cannabis Wishlist
- [ ] Zu probieren
  - Gelato
  - Wedding Cake
- [ ] Getestet
  - Sourdough ⭐⭐⭐⭐⭐
- [ ] Favoriten
  - Amnesia Haze
```

---

#### **6. Minimal Theme Settings** (wenn du Minimal-Theme nutzt)
Extra Kontrolle über Minimal Theme.

**Installation:** Settings → Community plugins → "Minimal Theme Settings"

---

## 🎨 CSS-Snippets für WeedDB

Custom CSS um dein Vault noch schöner zu machen!

### Wie man CSS-Snippets hinzufügt:

1. Gehe zu Settings → Appearance → CSS snippets
2. Klicke "Open snippets folder"
3. Erstelle eine neue Datei (z.B. `weeddb-custom.css`)
4. Füge CSS-Code ein (siehe unten)
5. Zurück in Obsidian → Aktiviere das Snippet

---

### Snippet 1: Grüner Akzent (Cannabis-Theme)

**Datei:** `cannabis-green.css`

```css
/* Grüne Akzentfarbe für Links und Highlights */
.theme-dark {
  --link-color: #7cb342;
  --link-color-hover: #9ccc65;
  --text-accent: #7cb342;
  --interactive-accent: #7cb342;
}

.theme-light {
  --link-color: #558b2f;
  --link-color-hover: #7cb342;
  --text-accent: #558b2f;
  --interactive-accent: #558b2f;
}

/* Cannabis-Icon für H1 */
h1::before {
  content: "🌿 ";
}
```

---

### Snippet 2: Schönere Tabellen

**Datei:** `better-tables.css`

```css
/* Kompaktere, schönere Tabellen */
.markdown-rendered table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.markdown-rendered th {
  background-color: var(--background-secondary);
  font-weight: 600;
  padding: 8px 12px;
  border-bottom: 2px solid var(--background-modifier-border);
}

.markdown-rendered td {
  padding: 6px 12px;
  border-bottom: 1px solid var(--background-modifier-border);
}

.markdown-rendered tr:hover {
  background-color: var(--background-primary-alt);
}

/* Zebra-Streifen */
.markdown-rendered tbody tr:nth-child(even) {
  background-color: rgba(0, 0, 0, 0.02);
}

.theme-dark .markdown-rendered tbody tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.02);
}
```

---

### Snippet 3: Logo größer darstellen

**Datei:** `bigger-logo.css`

```css
/* Macht das WeedDB-Logo größer und zentrierter */
img[alt*="WeedDB Logo"] {
  max-width: 500px !important;
  width: 100% !important;
  margin: 2em auto;
  display: block;
  border-radius: 50%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
```

---

### Snippet 4: Highlights für Bestenliste

**Datei:** `highlight-trophies.css`

```css
/* Gelber Hintergrund für Trophy-Zeilen */
.markdown-rendered td:has-text("🏆"),
.markdown-rendered tr:has(td:contains("🏆")) {
  background-color: rgba(255, 215, 0, 0.1);
  font-weight: 500;
}

/* Größere Emojis in Tabellen */
.markdown-rendered table td {
  font-size: 1em;
}
```

---

## ⚙️ Optimale Layout-Einstellungen

### Editor-Einstellungen:

**Settings → Editor:**

- ✅ **Spell check:** ON (aber nur für Deutsch/Englisch)
- ✅ **Line numbers:** OFF (cleaner look)
- ✅ **Readable line length:** ON (bessere Lesbarkeit)
- ✅ **Fold heading:** ON (Übersicht bei langen Dokumenten)
- ✅ **Fold indent:** ON
- ✅ **Show frontmatter:** OFF (weniger Clutter)

### Files & Links:

**Settings → Files & Links:**

- **Default location for new notes:** `docs/`
- **Automatically update internal links:** ON
- **Detect all file extensions:** ON
- **Excluded files:** `.git/, node_modules/, .DS_Store`

### Appearance:

**Settings → Appearance:**

- **Base color scheme:** Dark (oder Light nach Geschmack)
- **Accent color:** Grün (z.B. `#7cb342`)
- **Translucent window:** ON (macOS - sieht schick aus!)
- **Native menus:** OFF (konsistente UI)
- **Show inline title:** OFF (weniger Redundanz)
- **Show tab title bar:** ON

---

## 💼 Workspace-Setups

### Setup 1: "Übersicht" (Empfohlen für Anfänger)

**Layout:**
```
┌──────────────────┬────────────────────┐
│  File Explorer   │   START.md         │
│  (Sidebar left)  │   (Main pane)      │
│                  │                    │
│  - START.md      ├────────────────────┤
│  - SORTEN_Ü...   │ SORTEN_ÜBERSICHT   │
│  - QUERY_EX...   │ (Tab 2)            │
│                  │                    │
└──────────────────┴────────────────────┘
```

**So erstellen:**
1. Öffne `START.md`
2. Rechtsklick auf Tab → "Split right"
3. Öffne `SORTEN_ÜBERSICHT.md` im rechten Pane
4. `Cmd/Ctrl + P` → "Workspaces: Save current workspace layout"
5. Name: "Übersicht"

---

### Setup 2: "Research" (Für tiefe Daten-Analysen)

**Layout:**
```
┌──────────────┬──────────────┬────────────┐
│ File Tree    │ Product      │ SQL        │
│              │ Details      │ Queries    │
│              │              │            │
│              ├──────────────┤            │
│              │ Graph View   │            │
└──────────────┴──────────────┴────────────┘
```

**Features:**
- Links: File Explorer
- Mitte oben: Aktuelle Produktseite
- Mitte unten: Graph View (zeigt Verbindungen)
- Rechts: QUERY_EXAMPLES.md

---

### Setup 3: "Minimalist" (Nur Inhalt)

**Layout:**
```
┌────────────────────────────────────────┐
│                                        │
│         SORTEN_ÜBERSICHT.md            │
│         (Fullscreen, no sidebars)      │
│                                        │
│                                        │
└────────────────────────────────────────┘
```

**So erstellen:**
1. Schließe beide Sidebars (`Cmd/Ctrl + \` for left)
2. Öffne nur SORTEN_ÜBERSICHT
3. Reading Mode aktivieren (`Cmd/Ctrl + E`)

---

## 🎯 Quick-Tipps für schöneres WeedDB

### 1. **Custom Icons für Ordner**

Nutze das "Iconize" Plugin:
- Settings → Community Plugins → "Iconize"
- Rechtsklick auf Ordner → "Change Icon"
- Vorschläge:
  - `docs/` → 📚
  - `scripts/` → ⚙️
  - `data/` → 💾
  - `user-guides/` → 📖

### 2. **Sidebar-Reihenfolge optimieren**

Ziehe Dateien in diese Reihenfolge:
1. 🏠 START.md
2. 🌿 SORTEN_ÜBERSICHT.md
3. 📊 QUERY_EXAMPLES.md
4. 📖 ANLEITUNG.md
5. 🤖 CLAUDE.md

### 3. **Hotkeys personalisieren**

**Settings → Hotkeys** - Empfohlene Shortcuts:
- "Open START.md" → `Cmd/Ctrl + H` (H = Home)
- "Toggle left sidebar" → `Cmd/Ctrl + B`
- "Toggle reading mode" → `Cmd/Ctrl + E`
- "Open graph view" → `Cmd/Ctrl + G`

### 4. **Bookmarks nutzen**

Core Plugin "Bookmarks" aktivieren:
- Rechtsklick auf START.md → "Bookmark this file"
- Rechtsklick auf SORTEN_ÜBERSICHT → "Bookmark"
- Sidebar: Quick access zu wichtigen Seiten!

### 5. **Templates für neue Produkte**

Erstelle `docs/templates/product_review.md`:

```markdown
---
product:
genetics:
thc:
cbd:
rating:
tried_date:
---

# {{title}}

## 🌿 Produktinfo
- **Genetik:**
- **THC:**
- **CBD:**
- **Hersteller:**

## 💭 Meine Notizen

### Geschmack & Geruch


### Wirkung


### Preis-Leistung
- Apotheke:
- Preis: €/g

## ⭐ Bewertung

/5 Sterne

**Kaufen wieder?** [ ] Ja [ ] Nein
```

---

## 🌈 Farbschema-Vorschläge

### Cannabis-inspirierte Farbpalette:

**Grüntöne (Hell → Dunkel):**
- `#c5e1a5` - Hellgrün (Highlights)
- `#9ccc65` - Limette (Akzente)
- `#7cb342` - Grasgrün (Links)
- `#558b2f` - Waldgrün (Überschriften)
- `#33691e` - Dunkelgrün (Kontraste)

**Komplementärfarben:**
- `#ab47bc` - Lila (für Hybrid-Sorten)
- `#ffa726` - Orange (für Sativa-Sorten)
- `#5c6bc0` - Blau (für Indica-Sorten)

**In Obsidian anwenden:**
Settings → Appearance → Accent color → Custom → `#7cb342`

---

## 📱 Mobile Ansicht (Obsidian Mobile)

Falls du Obsidian auf dem Handy nutzt:

**Optimale Einstellungen:**
- Settings → Mobile → Quick access toolbar → ON
- Füge hinzu: START, SORTEN_ÜBERSICHT, Search
- Theme: "Minimal" funktioniert auch super auf Mobile!

**Sync:**
- Nutze Obsidian Sync (kostenpflichtig) ODER
- Nutze Syncthing (kostenlos, open source)

---

## 🎓 Weiterführende Ressourcen

- **Obsidian Forum:** https://forum.obsidian.md
- **Theme Gallery:** https://obsidian.md/themes
- **Plugin Directory:** https://obsidian.md/plugins
- **CSS Snippets:** https://github.com/obsidian-community/obsidian-hub

---

## 💡 Pro-Tipp: Vollständiges "Cannabis Knowledge Vault"

Erweitere WeedDB zu einem persönlichen Cannabis-Wiki:

1. **Strain Reviews:** Eigene Bewertungen als Notes
2. **Terpene Guide:** Detaillierte Terpene-Infos
3. **Medical Info:** Therapeutische Anwendungen dokumentieren
4. **Dosage Tracking:** Tagebuch für medizinische Nutzer
5. **Recipe Notes:** Cannabis-Rezepte (Edibles, etc.)

Nutze Tags wie `#review`, `#medical`, `#recipe` für Organisation!

---

**Viel Spaß beim Customizen! 🎨🌿**

> Wenn du ein richtig cooles Setup erstellt hast, teile Screenshots im [GitHub Repository](https://github.com/laubfrosch-sudo/WeedDB)!
