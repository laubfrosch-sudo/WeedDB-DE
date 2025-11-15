---
created: 2024-03-10
updated: 2025-11-15
version: 0.1.0
author: laubfrosch-sudo
status: alpha
description: 60+ comprehensive SQL query examples for WeedDB price analysis and product search
---

# WeedDB Query Examples

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This document provides comprehensive SQL query examples for analyzing the WeedDB cannabis product database.

## Quick Reference

Open the database in SQLite CLI:
```bash
sqlite3 WeedDB.db
```

Enable better formatting:
```sql
.mode column
.headers on
.width 30 10 10 10
```

---

## 📊 Multi-Pharmacy Price Analysis

### Find Products with Largest Price Differences

Shows which products have the most price variation across pharmacies:

```sql
SELECT
    product_name,
    pharmacy_count as pharmacies,
    min_price || '€' as cheapest,
    max_price || '€' as most_expensive,
    price_spread || '€' as difference,
    ROUND((price_spread / min_price) * 100, 1) || '%' as percent_diff
FROM product_price_stats
WHERE pharmacy_count > 1
ORDER BY price_spread DESC
LIMIT 20;
```

**Use case:** Find products where shopping around saves the most money.

---

### Compare All Prices for a Specific Product

View all available pharmacies and prices for one product:

```sql
SELECT
    pharmacy_name,
    ROUND(price_per_g, 2) || '€/g' as price,
    price_rank as rank,
    datetime(timestamp, 'localtime') as last_updated
FROM product_pharmacy_prices
WHERE product_name LIKE '%Gelato%'
ORDER BY price_per_g ASC;
```

**Use case:** Find the best deal for a specific strain.

---

### Top 10 Cheapest Pharmacies Overall

Ranks pharmacies by average price and how often they're the cheapest:

```sql
SELECT
    pharmacy_name,
    products_offered as products,
    avg_price_per_g || '€' as avg_price,
    times_cheapest as '# times cheapest'
FROM pharmacy_price_ranking
LIMIT 10;
```

**Use case:** Identify which pharmacies consistently offer the best prices.

---

### Price History for a Product

Track how a product's price has changed over time:

```sql
SELECT
    ph.name as pharmacy,
    ROUND(pr.price_per_g, 2) || '€/g' as price,
    datetime(pr.timestamp, 'localtime') as timestamp
FROM prices pr
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
JOIN products p ON pr.product_id = p.id
WHERE p.name LIKE '%Black Cherry%'
ORDER BY pr.timestamp DESC
LIMIT 20;
```

**Use case:** See if prices are going up or down.

---

## 🔍 Product Search & Filter

### Find High-THC Indica Strains Under €7/g

```sql
SELECT
    p.name,
    p.genetics,
    p.thc_percent || '%' as THC,
    p.rating || '★' as rating,
    s.min_price || '€' as cheapest_price,
    s.pharmacy_count as pharmacies
FROM products p
JOIN product_price_stats s ON p.id = s.product_id
WHERE p.genetics = 'Indica'
  AND p.thc_percent >= 20
  AND s.min_price <= 7.0
ORDER BY p.rating DESC;
```

**Use case:** Find potent Indica strains within budget.

---

### Search by Terpene Profile

Find all products containing Myrcen (sedative terpene):

```sql
SELECT
    p.name,
    p.genetics,
    p.thc_percent || '%' as THC,
    GROUP_CONCAT(DISTINCT t.name, ', ') as terpenes,
    s.min_price || '€' as cheapest_price
FROM products p
JOIN product_terpenes pt ON p.id = pt.product_id
JOIN terpenes t ON pt.terpene_id = t.id
JOIN product_price_stats s ON p.id = s.product_id
WHERE t.name = 'Myrcen'
GROUP BY p.id
ORDER BY p.rating DESC
LIMIT 10;
```

**Use case:** Find strains with specific terpene profiles for desired effects.

---

### Find Products by Therapeutic Use

Search for products recommended for chronic pain:

```sql
SELECT
    p.name,
    p.genetics,
    p.thc_percent || '%' as THC,
    p.cbd_percent || '%' as CBD,
    p.rating || '★' as rating,
    s.min_price || '€' as price,
    GROUP_CONCAT(DISTINCT tu.name, ', ') as therapeutic_uses
FROM products p
JOIN product_therapeutic_uses ptu ON p.id = ptu.product_id
JOIN therapeutic_uses tu ON ptu.therapeutic_use_id = tu.id
JOIN product_price_stats s ON p.id = s.product_id
WHERE tu.name = 'chronic pain'
GROUP BY p.id
ORDER BY p.rating DESC
LIMIT 10;
```

**Use case:** Find medically appropriate strains for specific conditions.

---

### Find Products by Effects

Search for relaxing strains:

```sql
SELECT
    p.name,
    p.genetics,
    p.thc_percent || '%' as THC,
    GROUP_CONCAT(DISTINCT e.name, ', ') as effects,
    s.min_price || '€' as price
FROM products p
JOIN product_effects pe ON p.id = pe.product_id
JOIN effects e ON pe.effect_id = e.id
JOIN product_price_stats s ON p.id = s.product_id
WHERE e.name IN ('relaxing', 'sedative')
GROUP BY p.id
ORDER BY p.rating DESC
LIMIT 10;
```

**Use case:** Find strains with desired effects.

---

## 📈 Statistics & Analytics

### Database Overview

```sql
SELECT
    'Products' as category, COUNT(*) as count FROM products
UNION ALL
SELECT 'Producers', COUNT(*) FROM producers
UNION ALL
SELECT 'Pharmacies', COUNT(*) FROM pharmacies
UNION ALL
SELECT 'Price Entries', COUNT(*) FROM prices
UNION ALL
SELECT 'Terpenes', COUNT(*) FROM terpenes
UNION ALL
SELECT 'Effects', COUNT(*) FROM effects
UNION ALL
SELECT 'Therapeutic Uses', COUNT(*) FROM therapeutic_uses;
```

---

### Genetics Distribution

```sql
SELECT
    genetics,
    COUNT(*) as count,
    ROUND(AVG(thc_percent), 1) || '%' as avg_THC,
    ROUND(AVG(rating), 2) || '★' as avg_rating
FROM products
WHERE genetics IS NOT NULL
GROUP BY genetics
ORDER BY count DESC;
```

---

### Top Rated Products by Genetics

```sql
SELECT
    genetics,
    name,
    rating || '★' as rating,
    review_count as reviews,
    thc_percent || '%' as THC,
    s.min_price || '€' as price
FROM products p
JOIN product_price_stats s ON p.id = s.product_id
WHERE rating IS NOT NULL
ORDER BY genetics, rating DESC;
```

---

### Producer Market Share

```sql
SELECT
    pr.name as producer,
    pr.origin,
    COUNT(p.id) as products,
    ROUND(AVG(p.rating), 2) || '★' as avg_rating,
    ROUND(AVG(p.thc_percent), 1) || '%' as avg_THC
FROM producers pr
JOIN products p ON pr.id = p.producer_id
GROUP BY pr.id
ORDER BY products DESC
LIMIT 15;
```

---

### Price Distribution by Genetics

```sql
SELECT
    p.genetics,
    COUNT(DISTINCT p.id) as products,
    ROUND(MIN(s.min_price), 2) || '€' as cheapest,
    ROUND(AVG(s.avg_price), 2) || '€' as average,
    ROUND(MAX(s.max_price), 2) || '€' as most_expensive
FROM products p
JOIN product_price_stats s ON p.id = s.product_id
WHERE p.genetics IS NOT NULL
GROUP BY p.genetics
ORDER BY AVG(s.avg_price);
```

---

## 🏆 Best Value Products

### Best THC-to-Price Ratio

Find the most potent products for your money:

```sql
SELECT
    p.name,
    p.genetics,
    p.thc_percent || '%' as THC,
    s.min_price || '€' as price,
    ROUND(p.thc_percent / s.min_price, 2) as 'THC per €',
    p.rating || '★' as rating
FROM products p
JOIN product_price_stats s ON p.id = s.product_id
WHERE p.thc_percent IS NOT NULL
  AND s.min_price > 0
ORDER BY (p.thc_percent / s.min_price) DESC
LIMIT 20;
```

---

### Best Rated Products Under €6/g

```sql
SELECT
    p.name,
    p.genetics,
    p.rating || '★' as rating,
    p.review_count as reviews,
    p.thc_percent || '%' as THC,
    s.min_price || '€' as price,
    s.pharmacy_count as pharmacies
FROM products p
JOIN product_price_stats s ON p.id = s.product_id
WHERE p.rating >= 4.0
  AND s.min_price <= 6.0
ORDER BY p.rating DESC, p.review_count DESC
LIMIT 20;
```

---

## 🔬 Advanced Queries

### Complete Product Profile

Get all information about a specific product:

```sql
WITH product_info AS (
    SELECT
        p.id,
        p.name,
        p.variant,
        p.genetics,
        p.thc_percent,
        p.cbd_percent,
        p.rating,
        p.review_count,
        pr.name as producer,
        pr.origin
    FROM products p
    LEFT JOIN producers pr ON p.producer_id = pr.id
    WHERE p.name LIKE '%Gelato%'
    LIMIT 1
),
product_terpenes_list AS (
    SELECT
        GROUP_CONCAT(t.name, ', ') as terpenes
    FROM product_info pi
    JOIN product_terpenes pt ON pi.id = pt.product_id
    JOIN terpenes t ON pt.terpene_id = t.id
),
product_effects_list AS (
    SELECT
        GROUP_CONCAT(e.name, ', ') as effects
    FROM product_info pi
    JOIN product_effects pe ON pi.id = pe.product_id
    JOIN effects e ON pe.effect_id = e.id
),
product_prices_list AS (
    SELECT
        GROUP_CONCAT(ph.name || ': €' || ROUND(pr.price_per_g, 2), ' | ') as prices
    FROM product_info pi
    JOIN prices pr ON pi.id = pr.product_id
    JOIN pharmacies ph ON pr.pharmacy_id = ph.id
    WHERE pr.timestamp >= datetime('now', '-7 days')
)
SELECT * FROM product_info, product_terpenes_list, product_effects_list, product_prices_list;
```

---

### Pharmacy Competition Analysis

Find products with the most competing pharmacies:

```sql
SELECT
    product_name,
    genetics,
    pharmacy_count as competing_pharmacies,
    min_price || '€' as cheapest,
    max_price || '€' as expensive,
    price_spread || '€' as savings_potential,
    avg_price || '€' as market_avg
FROM product_price_stats
WHERE pharmacy_count >= 3
ORDER BY pharmacy_count DESC, price_spread DESC
LIMIT 20;
```

---

## 💡 Tips

### Enable CSV Export

```bash
sqlite3 WeedDB.db <<EOF
.mode csv
.headers on
.output results.csv
SELECT * FROM product_price_stats;
.output stdout
EOF
```

### Create Custom View

```sql
CREATE VIEW my_indica_picks AS
SELECT
    p.name,
    p.thc_percent,
    p.rating,
    s.min_price,
    s.pharmacy_count
FROM products p
JOIN product_price_stats s ON p.id = s.product_id
WHERE p.genetics = 'Indica'
  AND p.rating >= 4.0
ORDER BY p.rating DESC;

-- Use it:
SELECT * FROM my_indica_picks LIMIT 10;
```

---

## 📝 Notes

- **Price Data Freshness:** Views filter prices from the last 7 days by default
- **NULL Values:** Some products may have incomplete data (no rating, terpenes, etc.)
- **LIKE Operator:** Use `%` as wildcard when searching product names
- **Case Sensitivity:** SQLite is case-insensitive for LIKE by default

For more information, see `CLAUDE.md` or `INSTRUCTIONS.md`.
# Price History Queries

## Current Price Queries

SELECT p.name, pr.price_per_g, pr.category, ph.name as pharmacy
FROM products p
JOIN prices pr ON p.id = pr.product_id
LEFT JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE pr.timestamp = (
    SELECT MAX(timestamp) FROM prices
    WHERE product_id = p.id AND category = pr.category
);

## Historical Price Queries

SELECT DATE(ph.recorded_at) as date, p.name, ph.price_per_g, ph.category
FROM price_history ph
JOIN products p ON ph.product_id = p.id
ORDER BY ph.recorded_at DESC;
