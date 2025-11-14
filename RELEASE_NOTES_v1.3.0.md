# Release Notes v1.3.0

## 🚀 Major Features & Improvements

### ✨ **Complete AI Assistant Support**
- **NEW:** `OPENCODE.md` - Dedicated documentation for OpenCode assistant
- **ENHANCED:** Synchronized documentation across all AI assistants (Claude, Gemini, OpenCode)
- **IMPROVED:** Consistent schema definitions and usage instructions

### 🔧 **Enhanced Product Scraping**
- **NEW:** Full product data extraction including:
  - THC% and CBD% percentages
  - Genetics (Indica/Sativa/Hybrid)
  - User ratings and review counts
  - Producer information and variant details
- **IMPROVED:** More robust data parsing from shop.dransay.com
- **FIXED:** Better error handling for missing product information

### 📊 **Improved User Experience**
- **ENHANCED:** `update_prices.py` with auto-confirmation for automated execution
- **UPDATED:** `README.md` with complete database schema and examples
- **IMPROVED:** Better documentation structure and clarity
- **ENHANCED:** Type safety with `mypy --strict` compliance for all scripts

### 📈 **Data Quality Improvements**
- **ENHANCED:** Product overview generation with more accurate data
- **IMPROVED:** Price tracking with complete product attributes
- **UPDATED:** Best-of lists with comprehensive product information

## 🛠️ Technical Improvements

### Type Safety
- ✅ All Python scripts now pass `mypy --strict` type checking
- ✅ Enhanced type annotations throughout codebase
- ✅ Better error handling and validation

### Documentation
- ✅ Complete synchronization between `CLAUDE.md`, `GEMINI.md`, and `OPENCODE.md`
- ✅ Updated README.md with comprehensive schema documentation
- ✅ Clear installation and usage instructions

### Automation
- ✅ Auto-confirmation in `update_prices.py` for CI/CD compatibility
- ✅ Improved batch processing capabilities
- ✅ Better error reporting and progress tracking

## 📋 Database Changes

### Enhanced Product Table
- Now stores complete product information:
  - `thc_percent`, `cbd_percent` - Cannabinoid percentages
  - `genetics` - Strain genetics (Indica/Sativa/Hybrid)
  - `rating`, `review_count` - User ratings and review counts
  - `variant` - Full product variant information
  - `producer_id` - Link to producers table

### Improved Price Tracking
- Historical price data with complete product context
- Better pharmacy name extraction and storage
- Enhanced category-based price comparison

## 🔄 Migration Notes

### For Existing Users
1. **Database:** Existing databases remain compatible
2. **Scripts:** All scripts are backward compatible
3. **Configuration:** No configuration changes required

### For New Users
- Follow updated README.md for complete setup instructions
- All AI assistants now have dedicated documentation
- Enhanced type checking ensures better code quality

## 🐛 Bug Fixes

- Fixed product data extraction for missing attributes
- Improved error handling in scraping operations
- Better handling of special characters in product names
- Enhanced pharmacy name parsing accuracy

## 📚 Documentation Updates

- **NEW:** `OPENCODE.md` for OpenCode assistant users
- **UPDATED:** All AI documentation files are now synchronized
- **ENHANCED:** README.md with complete schema and examples
- **IMPROVED:** Better installation and troubleshooting guides

## 🎯 Performance Improvements

- Faster product data extraction with optimized selectors
- Better memory usage in batch operations
- Improved error recovery in scraping operations
- Enhanced database query performance

## 🔮 Next Steps

### Planned for v1.4.0
- Terpene profile extraction and storage
- Effects and therapeutic use tracking
- Advanced price analytics and trend analysis
- Web dashboard for data visualization

---

## 📦 Installation & Update

### New Installation
```bash
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB
pip3 install playwright mypy
python3 -m playwright install chromium
sqlite3 WeedDB.db < schema.sql
python3 add_product.py 'sourdough'
```

### Update Existing Installation
```bash
git pull origin main
pip3 install --upgrade playwright mypy
python3 update_prices.py
python3 generate_overview.py
```

---

**Total Files Changed:** 6 files, 159 insertions, 23 deletions  
**Type Safety:** 100% compliance with `mypy --strict`  
**AI Support:** Claude, Gemini, OpenCode fully supported  
**Database:** Enhanced with complete product information  

🎉 **WeedDB v1.3.0 - Complete AI Assistant Support & Enhanced Product Data!**