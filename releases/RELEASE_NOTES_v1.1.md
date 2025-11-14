# WeedDB Release v1.1.0 - Multi-Pharmacy Price Tracking

**Release Date:** 2025-11-14
**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

---

## 🎉 Major New Features

### 1. **Multi-Pharmacy Price Tracking** 🆕

WeedDB now tracks prices from **ALL pharmacies** displayed on shop.dransay.com, not just the cheapest one!

**Benefits:**
- 💰 Compare prices across up to 50+ German pharmacies
- 📊 Identify which pharmacies consistently offer the best deals
- 🏆 Find products with the biggest price differences (save up to €0.80/g)
- 📈 Track historical pricing across all pharmacies

**Example Output:**
```
💰 Pharmacy Prices (3 pharmacies found):
   🏆 Apotheke A: €5.99/g
     2. Apotheke B: €6.44/g
     3. Apotheke C: €7.12/g
```

### 2. **Advanced Database Views** 🆕

Three new powerful SQL views for comprehensive price analysis:

#### `product_pharmacy_prices`
View all prices per product with automatic ranking:
```sql
SELECT * FROM product_pharmacy_prices WHERE product_name LIKE '%Gelato%';
```

#### `product_price_stats`
Get price statistics (min, max, avg, spread, pharmacy count):
```sql
SELECT * FROM product_price_stats WHERE pharmacy_count > 1;
```

#### `pharmacy_price_ranking`
Rank pharmacies by how often they're the cheapest:
```sql
SELECT * FROM pharmacy_price_ranking LIMIT 10;
```

### 3. **Comprehensive Query Examples** 🆕

**New File:** `QUERY_EXAMPLES.md` (60+ SQL examples)

Categories include:
- 📊 Multi-pharmacy price analysis
- 🔍 Product search by terpenes, effects, therapeutic uses
- 📈 Statistics & analytics
- 🏆 Best value products (THC-to-price ratio)
- 🔬 Advanced queries (price trends, pharmacy competition)
- 💾 CSV export examples

### 4. **Testing & Documentation** 🆕

**New Files:**
- `TESTING_REPORT.md` - Complete testing report with validation results
- `QUERY_EXAMPLES.md` - 60+ ready-to-use SQL queries

**Updated Documentation:**
- `CLAUDE.md` - Multi-pharmacy sections, new views
- `GEMINI.md` - Architecture updates
- `README.md` - Query examples step added
- `INSTRUCTIONS.md` / `ANLEITUNG.md` - Multi-pharmacy query examples
- `schema.sql` - Fully documented with new views

---

## 📊 Technical Improvements

### Code Enhancements

**`add_product.py` (v1.1.0):**
- ✅ Multi-strategy scraping for all pharmacy prices
- ✅ Vendor card element detection
- ✅ XPath ancestor context search
- ✅ Fallback to featured pharmacy (backward compatible)
- ✅ Top 5 cheapest pharmacies output
- ✅ 100% type-safe (mypy --strict)

**Database Enhancements:**
- ✅ 3 new views: `product_pharmacy_prices`, `product_price_stats`, `pharmacy_price_ranking`
- ✅ Window functions for price ranking
- ✅ 7-day data freshness filtering
- ✅ All foreign keys validated
- ✅ Database integrity confirmed (PRAGMA checks)

### Quality Metrics

```
Type Safety:       100% (mypy --strict ✓)
Database Integrity: ✓ PRAGMA integrity_check: ok
Foreign Keys:       ✓ PRAGMA foreign_key_check: no errors
Normal Form:        ✓ 3NF
Documentation:      62 KB across 10 files
Total Code Lines:   2,909 lines
```

---

## 📈 Database Statistics

**Current Dataset:**
- **100 Products** tracked
- **53 Pharmacies** monitored
- **370 Price Entries** (historical data)
- **5 SQL Views** for analysis
- **7 Terpenes** cataloged
- **9 Effects** tracked
- **14 Therapeutic Uses** documented

**Multi-Pharmacy Coverage:**
- 9 products currently have prices from 2+ pharmacies
- Largest price spread: €0.80/g (Ghost Train Haze)
- Average savings: 7-10% by comparing pharmacies

---

## 🚀 Usage Examples

### Add Product with Multi-Pharmacy Prices

```bash
python3 add_product.py "https://shop.dransay.com/product/gelato/123?vendorId=all"
```

### Compare Prices Across Pharmacies

```sql
sqlite3 WeedDB.db
SELECT product_name, pharmacy_count, min_price, price_spread
FROM product_price_stats
WHERE pharmacy_count > 1
ORDER BY price_spread DESC;
```

### Find Cheapest Pharmacy Overall

```sql
SELECT pharmacy_name, times_cheapest, avg_price_per_g
FROM pharmacy_price_ranking
LIMIT 5;
```

---

## 🔄 Migration Guide

### For Existing Databases

**No migration required!** This release is fully backward compatible.

**To populate multi-pharmacy data:**
```bash
python3 update_all_products.py
```

This will refresh all 100 products with prices from all available pharmacies.

### For New Installations

```bash
# 1. Clone repository
git clone https://github.com/laubfrosch-sudo/WeedDB.git
cd WeedDB

# 2. Install dependencies
pip3 install playwright mypy
python3 -m playwright install chromium

# 3. Create database
sqlite3 WeedDB.db < schema.sql

# 4. Add products
python3 add_product.py "<product_url>"
```

---

## 📝 Files Changed

### New Files
- `QUERY_EXAMPLES.md` - 60+ SQL query examples
- `TESTING_REPORT.md` - Comprehensive testing report
- `RELEASE_NOTES_v1.1.md` - This file

### Modified Files
- `add_product.py` - Multi-pharmacy scraping logic (+80 lines)
- `schema.sql` - 3 new views (+67 lines)
- `CLAUDE.md` - Multi-pharmacy documentation
- `GEMINI.md` - Architecture updates
- `README.md` - Query examples reference
- `INSTRUCTIONS.md` - Multi-pharmacy examples (EN)
- `ANLEITUNG.md` - Multi-pharmacy examples (DE)

### Unchanged Files
- `update_all_products.py` - No changes needed
- `add_batch_products.py` - No changes needed
- `debug_scrape.py` - No changes needed
- Database schema structure - Fully backward compatible

---

## 🐛 Bug Fixes

- ✅ Fixed type annotation issue in pharmacy name extraction
- ✅ Improved error handling for missing pharmacy data
- ✅ Enhanced scraping fallback logic for edge cases

---

## 🔜 Future Enhancements

### Planned for v1.2.0
- [ ] Price trend visualization
- [ ] Email alerts for price drops
- [ ] Web dashboard for visual comparison
- [ ] Automated daily updates (cron job)
- [ ] Export functionality to CSV/JSON

### Under Consideration
- [ ] Price prediction using historical data
- [ ] Pharmacy availability heatmap
- [ ] Mobile-friendly query interface
- [ ] REST API for external integrations

---

## 📖 Documentation

### Quick Links
- **Getting Started:** `README.md`
- **Query Examples:** `QUERY_EXAMPLES.md` (60+ examples)
- **AI Assistant Guide:** `INSTRUCTIONS.md` (EN) / `ANLEITUNG.md` (DE)
- **Technical Docs:** `CLAUDE.md` / `GEMINI.md`
- **Testing Report:** `TESTING_REPORT.md`

### Documentation Stats
```
Total Documentation:  62 KB
Files:                10 markdown files
SQL Examples:         60+ queries
Code Comments:        Comprehensive inline documentation
```

---

## 🙏 Acknowledgments

This release was developed with the assistance of Claude Code (claude.ai/code) and represents a major milestone in WeedDB's evolution from a simple price tracker to a comprehensive multi-pharmacy comparison platform.

---

## 📊 Version Comparison

| Feature | v1.0.0 | v1.1.0 |
|---------|--------|--------|
| Single pharmacy tracking | ✅ | ✅ |
| Multi-pharmacy tracking | ❌ | ✅ |
| Price comparison views | ❌ | ✅ (3 views) |
| Query examples | Basic | ✅ 60+ examples |
| Type safety | ✅ | ✅ 100% |
| Documentation | 8 files | 10 files (+2) |
| Testing report | ❌ | ✅ |

---

## 💬 Feedback & Contributions

Found a bug? Have a feature request?

Please open an issue at: [https://github.com/laubfrosch-sudo/WeedDB/issues](https://github.com/laubfrosch-sudo/WeedDB/issues)

---

**Thank you for using WeedDB!** 🌿

This release represents hundreds of lines of code improvements and comprehensive testing to bring you the most accurate cannabis price comparison tool for the German market.

**Version:** 1.1.0
**Release Date:** 2025-11-14
**Codename:** "Multi-Pharmacy Milestone"
