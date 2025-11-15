---
created: 2025-11-15
updated: 2025-11-15
version: 0.1.0
author: laubfrosch-sudo
status: alpha
description: Version history and changelog for WeedDB project
---

# Changelog

All notable changes to WeedDB-DE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2025-11-15

### 🎉 Initial Alpha Release

This is the foundational release of WeedDB-DE, marking the re-entry into Alpha development phase. The project has been reset to focus on core functionality for German medical cannabis product tracking.

### Added

#### Core Functionality
- **SQLite Database**: 3NF normalized schema for product, price, and pharmacy data
- **Web Scraping**: Playwright-based extraction from shop.dransay.com
- **Price Tracking**: Dual-category pricing (top/all pharmacies) with historical data
- **Product Management**: Comprehensive strain data including THC/CBD, genetics, effects, and therapeutic uses

#### Scripts & Automation
- `add_product.py`: Individual product scraping and database insertion
- `update_prices.py`: Bulk price updates for all products
- `add_products_batch.py`: Batch processing with enhanced reliability
- `generate_overview.py`: Automated markdown generation for SORTEN_ÜBERSICHT.md

#### Documentation
- **Alpha Release Notes**: `CHANGELOG/RELEASE_NOTES_V0.1.0.md`
- **Project Plan**: `docs/development/PROJEKTPLAN.md`
- **Kanban Board**: `docs/development/KANBAN.md`
- **AI Assistant Guidelines**: Updated for Alpha phase
- **Repository Setup**: Git and GitHub integration for WeedDB-DE

#### New Features & Improvements
- **`find_new_products.py`**: New script to identify products not yet in DB.
- **Path Handling**: All Python scripts updated to use dynamic absolute paths for improved portability.
- **Type Safety**: All Python scripts are now strictly type-checked with `mypy --strict`.
- **`add_product.py`**: Implemented existence check before adding/updating products.
- **`find_new_products.py`**: Improved product name extraction from URLs.
- **`README.md`**: Consolidated and translated to German.
- **`SORTEN_ÜBERSICHT.md`**: Generation fixed and updated.

#### Bug Fixes
- Numerous `mypy --strict` type errors across all Python scripts.
- Database connection and file path issues in various scripts.
- `generate_overview.py` output path.

### Changed
- **Repository Reset**: All previous version references removed
- **Alpha Phase**: Project status set to Alpha development
- **Documentation**: Streamlined to reflect current state

### Technical Details
- **Database**: SQLite with normalized schema
- **Scraping**: Playwright for JavaScript-rendered pages
- **Dependencies**: Python 3.9+, Playwright, MyPy
- **Platform**: Cross-platform (macOS, Linux, Windows)

---

### v2.0.0 (Future)
- REST API for programmatic access
- Web interface for database browsing
- Advanced analytics and visualizations

---

**For detailed validation reports, see:**


**For documentation maintenance guidelines, see:**
- [docs/DOCUMENTATION_MAINTENANCE.md](docs/DOCUMENTATION_MAINTENANCE.md)

---

*Maintained by [laubfrosch-sudo](https://github.com/laubfrosch-sudo)*
