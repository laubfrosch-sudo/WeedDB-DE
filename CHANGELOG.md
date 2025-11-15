---
created: 2025-11-15
updated: 2025-11-15
version: 1.5.1
author: laubfrosch-sudo
status: stable
description: Version history and changelog for WeedDB project
---

# Changelog

All notable changes to WeedDB will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.5.0] - 2025-11-15

### 🎉 Major Release: Documentation & Onboarding Overhaul

This release focuses on making WeedDB accessible to absolute beginners and providing comprehensive customization options for Obsidian users.

### Added

#### Documentation
- **Beginner Setup Guides** - Complete step-by-step installation guides for all operating systems
  - `docs/user-guides/BEGINNER_SETUP_MACOS.md` - macOS setup with Homebrew installation
  - `docs/user-guides/BEGINNER_SETUP_LINUX.md` - Ubuntu/Debian/Fedora setup with package managers
  - `docs/user-guides/BEGINNER_SETUP_WINDOWS.md` - Windows 10/11 setup with PowerShell/CMD
  - Includes troubleshooting sections for common issues on each platform
  - Realistic time estimates (15-25 minutes)

- **Obsidian Customization Guide** - `docs/user-guides/OBSIDIAN_THEMES.md`
  - 5 recommended themes (Minimal, Things, Sanctum, AnuPpuccin, Border)
  - 6 essential plugins (Dataview, Advanced Tables, Obsidian Git, Excalidraw, Kanban, Minimal Theme Settings)
  - 4 ready-to-use CSS snippets (Cannabis-green accent, better tables, bigger logo, trophy highlights)
  - 3 workspace setups (Übersicht, Research, Minimalist)
  - Cannabis-inspired color palette for theming
  - Dataview queries for metadata tracking

- **Documentation Maintenance Guide** - `docs/DOCUMENTATION_MAINTENANCE.md`
  - YAML frontmatter standards and policies
  - Update rules for version changes
  - Metadata maintenance workflows
  - Planned validation tools documentation
  - Obsidian Dataview queries for finding outdated docs

- **Enhanced START.md** - Obsidian vault homepage
  - New "Beginner" section with OS-specific guide links
  - Obsidian setup instructions with theme guide reference
  - Updated project statistics for v1.5.0
  - Improved navigation structure

- **Validation Report** - `VALIDATION_REPORT_V1.5.0.md`
  - Comprehensive release readiness report
  - Quality metrics and validation results
  - Link integrity verification
  - Metadata compliance check

#### Metadata System
- **YAML Frontmatter** added to all major documentation files
  - Fields: `created`, `updated`, `version`, `author`, `status`, `description`
  - Additional fields: `platform`, `target_audience`, `language`, `sync_with`
  - 13 files now with complete metadata
  - 100% metadata coverage for required files

- **AI Assistant Metadata Policy** - Added to `CLAUDE.md`
  - Critical guidelines for AI assistants when editing docs
  - Automatic `updated` field update requirements
  - Version consistency checks
  - Sync file management rules

#### Branding
- **WeedDB Logo Integration** - Logo added to all major documentation
  - `docs/assets/icons/WeedDB.jpeg` - Created with Google Gemini
  - Integrated in: README.md, START.md, CLAUDE.md, GEMINI.md, SORTEN_ÜBERSICHT.md
  - Proper crediting in all files
  - Automatic integration in generated overview

### Changed

#### Version Updates
- **All documentation updated to v1.5.0**
  - README.md title updated
  - All frontmatter `version` fields updated
  - Code examples and references updated
  - Consistency across all documentation

- **Enhanced User Guides**
  - `ANLEITUNG.md` (v1.5.0) - Now with frontmatter
  - `INSTRUCTIONS.md` (v1.5.0) - Now with frontmatter
  - Updated example prompts with v1.5.0 features

- **Improved AI Assistant Guidelines**
  - `CLAUDE.md` - Added Documentation Metadata Policy section
  - `GEMINI.md` - Updated to v1.5.0 with frontmatter
  - `AGENTS.md` - Added frontmatter and updated references

- **START.md Enhancements**
  - New features list for v1.5.0
  - Separated v1.5.0 features from v1.4.0 features
  - Better database query examples (4 practical examples instead of generic one)
  - Improved Obsidian setup instructions

### Fixed

- **Standardized version references** across all documents
- **Corrected internal link inconsistencies** (0 broken links)
- **Improved documentation structure** for better Obsidian integration
- **Fixed relative paths** for logo in subdirectory docs

### Documentation Structure

```
docs/
├── user-guides/
│   ├── ANLEITUNG.md (v1.5.0)
│   ├── INSTRUCTIONS.md (v1.5.0)
│   ├── BEGINNER_SETUP_MACOS.md (NEW)
│   ├── BEGINNER_SETUP_LINUX.md (NEW)
│   ├── BEGINNER_SETUP_WINDOWS.md (NEW)
│   └── OBSIDIAN_THEMES.md (NEW)
├── ai-assistants/
│   ├── CLAUDE.md (v1.5.0)
│   ├── GEMINI.md (v1.5.0)
│   └── AGENTS.md (v1.5.0)
├── QUERY_EXAMPLES.md (v1.5.0)
├── DOCUMENTATION_MAINTENANCE.md (NEW)
└── assets/
    └── icons/
        └── WeedDB.jpeg (NEW)
```

### Quality Metrics

- **Documentation Coverage:** 100% (13/13 required files)
- **Metadata Compliance:** 100% (all 6 required fields in all files)
- **Link Integrity:** 100% (0 broken links)
- **Version Consistency:** 100% (all files on v1.5.0)
- **Content Quality:** Excellent (comprehensive, beginner-friendly)

### Migration Notes

- **No breaking changes** - All existing functionality preserved
- **No database schema changes** - Database remains compatible with v1.4.0
- **Documentation-only release** - No Python code changes
- **Obsidian users**: Re-generate overview with `python3 scripts/generate_overview.py` to get logo

### Upgrade Path from v1.4.0

1. Pull latest changes: `git pull origin main`
2. No Python dependencies changed - no reinstallation needed
3. (Optional) Re-generate overview to get new logo: `cd scripts && python3 generate_overview.py`
4. (Optional) Open in Obsidian and enjoy new START.md and theme guide!

---

## [1.4.0] - 2024-11-10

### Added

- Enhanced batch processing with timeout protection
- Automatic data correction for missing producers (`fix_producers.py`)
- Extended producer recognition (24+ known manufacturers)
- Robust price extraction with multiple fallback methods
- Export/Import functionality for price history data
- Multi-pharmacy price comparison views
- Improved error handling and recovery mechanisms

### Changed

- Optimized scraping reliability
- Enhanced database views for analytics
- Improved batch processing scripts

### Fixed

- Timeout issues in batch operations
- Missing producer data handling
- Price extraction edge cases

---

## [1.3.0] - 2024-09-15

### Added

- Multi-pharmacy price tracking system
- Price history functionality
- Enhanced product metadata (country, effects, complaints)
- Improved terpene and therapeutic uses tracking

### Changed

- Database schema enhancements for price categories
- Updated documentation structure

---

## [1.2.0] - 2024-06-20

### Added

- Basic price tracking functionality
- Product scraping from shop.dransay.com
- SQLite database schema (3NF)
- Initial documentation

---

## [1.1.0] - 2024-04-15

### Added

- Initial project structure
- Basic scraping capabilities
- README documentation

---

## [1.0.0] - 2024-01-15

### Added

- Initial release
- Basic database structure
- Core scraping functionality

---

## Version Numbering

WeedDB follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.5.0)
- **MAJOR**: Breaking changes (database schema, API changes)
- **MINOR**: New features, significant improvements (backward compatible)
- **PATCH**: Bug fixes, minor improvements (backward compatible)

---

## Planned Features (Upcoming Versions)

### v1.6.0 (Planned)
- Automated frontmatter validation script (`check_frontmatter.py`)
- GitHub Actions CI for documentation validation
- Automated version bump script (`update_docs_version.py`)
- CLAUDE.md ↔ GEMINI.md sync script (`sync_ai_docs.py`)

### v1.7.0 (Planned)
- Multi-language support for documentation
- Enhanced price analytics dashboard
- Community contribution guidelines (CONTRIBUTING.md)

### v2.0.0 (Future)
- REST API for programmatic access
- Web interface for database browsing
- Advanced analytics and visualizations

---

**For detailed validation reports, see:**
- [VALIDATION_REPORT_V1.5.0.md](VALIDATION_REPORT_V1.5.0.md)

**For documentation maintenance guidelines, see:**
- [docs/DOCUMENTATION_MAINTENANCE.md](docs/DOCUMENTATION_MAINTENANCE.md)

---

*Maintained by [laubfrosch-sudo](https://github.com/laubfrosch-sudo)*
