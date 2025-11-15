# Release Notes - WeedDB-DE v0.1.0 (Alpha)

**Release Date:** 2025-11-15  
**Status:** Alpha Phase  
**Previous Version:** N/A (Initial Alpha Release)  
**Next Planned:** v0.2.0 (Beta Features)  

## Overview

WeedDB-DE v0.1.0 marks the re-entry into the Alpha development phase. This version represents a foundational rebuild and consolidation of the cannabis product database system, optimized for German medical cannabis tracking and Obsidian.md integration.

## Key Features

### Core Functionality
- **SQLite Database**: 3NF normalized schema for product, price, and pharmacy data
- **Web Scraping**: Playwright-based extraction from shop.dransay.com
- **Price Tracking**: Dual-category pricing (top/all pharmacies) with historical data
- **Product Management**: Comprehensive strain data including THC/CBD, genetics, effects, and therapeutic uses

### Scripts & Automation
- `add_product.py`: Individual product scraping and database insertion
- `update_prices.py`: Bulk price updates for all products
- `add_products_batch.py`: Batch processing with enhanced reliability
- `generate_overview.py`: Automated markdown generation for SORTEN_ÜBERSICHT.md

### Obsidian Integration
- Full Obsidian.md optimization with cross-linked documentation
- Template-based documentation structure
- Knowledge management friendly folder organization

## Alpha Phase Status

This release represents the **Alpha phase** of WeedDB-DE development:

- **Stability**: Core functionality implemented but may contain bugs
- **Features**: Basic scraping and database operations functional
- **Testing**: Limited automated testing; manual verification required
- **Documentation**: Comprehensive but evolving
- **Performance**: Basic optimization; may require tuning for large datasets

## Known Issues & Limitations

### Critical
- Web scraping reliability depends on shop.dransay.com page structure
- No automated error recovery for failed scrapes
- Limited validation of scraped data accuracy

### Minor
- .DS_Store files may appear in commits (now properly ignored)
- Type checking requires manual execution
- No CI/CD pipeline implemented

## Installation & Setup

```bash
# Prerequisites
pip3 install playwright mypy
python3 -m playwright install chromium

# Database setup
sqlite3 WeedDB.db < data/schema.sql

# Initial data population
python3 scripts/add_products_batch.py data/example_products.txt --yes
```

## Usage Examples

```bash
# Add single product
python3 scripts/add_product.py "Blue Dream"

# Update all prices
python3 scripts/update_prices.py

# Generate overview
python3 scripts/generate_overview.py
```

## Development Roadmap

### Immediate Next Steps (v0.2.0)
- Implement automated testing suite
- Add data validation and error handling
- Enhance scraping reliability with retry mechanisms
- Add logging and monitoring

### Future Releases
- Web interface for data browsing
- Advanced analytics and reporting
- Multi-source data integration
- API endpoints for external access

## Dependencies

- **Python**: 3.9+
- **SQLite3**: 3.x
- **Playwright**: Latest stable
- **MyPy**: For type checking

## Changelog

### Added
- Initial Alpha release structure
- Core scraping and database functionality
- Obsidian-optimized documentation
- Basic automation scripts

### Changed
- Re-entered Alpha development phase
- Consolidated repository structure

### Fixed
- Proper .gitignore handling for macOS files
- Remote repository setup for WeedDB-DE

## Contributing

This is an Alpha release. Please report issues via GitHub Issues with detailed reproduction steps.

## License

See LICENSE file for details (to be added in future release).

---

*This release marks the beginning of structured development for WeedDB-DE. Feedback and contributions welcome!*