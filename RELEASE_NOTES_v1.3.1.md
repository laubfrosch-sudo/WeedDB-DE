# Release Notes v1.3.1

**Release Date:** 14.11.2025

## 🐛 Bug Fixes

### Data Extraction Improvements
- **Fixed incomplete product data extraction** - All product attributes are now properly scraped:
  - ✅ Genetics (Indica/Sativa/Hybrid) - was previously missing
  - ✅ Producer information - now correctly extracted and stored
  - ✅ Complete THC/CBD percentages
  - ✅ Rating and review counts
  - ✅ Pharmacy names and prices with improved extraction methods

### Enhanced Scraping Logic
- **Added comprehensive debug output** for better troubleshooting of scraping issues
- **Implemented multiple fallback methods** for pharmacy/price extraction
- **Improved text parsing** to handle various page layouts and content structures
- **Fixed exception handling** to prevent crashes and ensure data completeness

## 📚 Documentation Updates

### Agent Collaboration
- **Renamed `OPENCODE.md` → `AGENTS.md`** for better AI agent collaboration
- **Updated all AI documentation files** with consistent information:
  - `CLAUDE.md` - Claude assistant guidance
  - `GEMINI.md` - Gemini assistant guidance  
  - `AI_INSTALLATION.md` - English installation guide
  - `KI_INSTALLATION.md` - German installation guide
  - `AGENTS.md` - Unified agent documentation

### Critical Process Documentation
- **Added mandatory overview generation notice** to all documentation files
- **Emphasized that `SORTEN_ÜBERSICHT.md` must be updated** after database changes
- **Added warnings about data currency** - overview is only as current as last script execution
- **Documented the complete data collection workflow** for better understanding

## 🔧 Technical Improvements

### Code Quality
- **Enhanced type safety** with better error handling
- **Improved selector robustness** for web scraping
- **Added comprehensive logging** for debugging scraping issues
- **Better data validation** before database insertion

### Database Operations
- **Ensured all required fields are present** before database operations
- **Improved price tracking** with accurate pharmacy name extraction
- **Fixed producer relationship handling** in product records

## 📋 Impact

### Before v1.3.1
- ❌ Genetics data was missing from database
- ❌ Producer information was not consistently stored
- ❌ Debugging scraping issues was difficult
- ❌ Documentation was inconsistent across AI platforms

### After v1.3.1
- ✅ Complete product data extraction (all attributes)
- ✅ Comprehensive debug output for troubleshooting
- ✅ Unified documentation for all AI agents
- ✅ Clear process requirements for overview updates
- ✅ Robust fallback methods for data extraction

## 🚀 Usage

### Add New Product (Now with Complete Data)
```bash
python3 add_product.py 'product_name'
```

### Update Overview (Required After Database Changes)
```bash
python3 generate_overview.py
```

### Verify Data Quality
```sql
SELECT name, genetics, thc_percent, cbd_percent, rating, review_count, producer_id 
FROM products 
WHERE name LIKE '%ProductName%';
```

## 🔄 Migration Notes

This release maintains full backward compatibility:
- Existing database structure unchanged
- All existing scripts work without modification
- No manual intervention required for existing installations

## 📝 Next Steps

Future releases will focus on:
- Enhanced error recovery mechanisms
- Additional data validation rules
- Performance optimizations for bulk operations
- Extended analytics capabilities

---

**Total Files Changed:** 7  
**Lines Added:** 303  
**Lines Removed:** 96  
**Net Improvement:** +207 lines of enhanced functionality and documentation