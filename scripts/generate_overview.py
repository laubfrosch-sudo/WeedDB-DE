#!/usr/bin/env python3
"""
Generate ../docs/SORTEN_ÜBERSICHT.md from WeedDB database.

This script creates a comprehensive overview of all cannabis products in the database,
including a "best of" list and a detailed table sorted by review count.

Usage:
    python3 generate_overview.py
"""

import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime


def get_all_products_with_prices() -> List[Dict[str, Any]]:
    """Fetch all products with their cheapest prices and details"""
    conn = sqlite3.connect('../data/WeedDB.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.genetics,
            p.thc_percent,
            p.cbd_percent,
            p.rating,
            p.review_count,
            p.url,
            COALESCE(pr.name, 'N/A') as producer_name,
            MIN(prices.price_per_g) as min_price
        FROM products p
        LEFT JOIN producers pr ON p.producer_id = pr.id
        LEFT JOIN prices ON p.id = prices.product_id
        GROUP BY p.id
        ORDER BY p.review_count DESC, p.rating DESC
    """)

    products = []
    for row in cursor.fetchall():
        products.append({
            'id': row[0],
            'name': row[1],
            'genetics': row[2] if row[2] else 'N/A',
            'thc_percent': row[3] if row[3] is not None else None,
            'cbd_percent': row[4] if row[4] is not None else None,
            'rating': row[5] if row[5] is not None else None,
            'review_count': row[6] if row[6] is not None else None,
            'url': row[7],
            'producer_name': row[8] if row[8] else 'N/A',
            'min_price': row[9] if row[9] is not None else None
        })

    conn.close()
    return products


def calculate_best_products(products: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Calculate best products in various categories"""
    best: Dict[str, Dict[str, Any]] = {}

    # Filter products with sufficient data
    products_with_reviews = [p for p in products if p['review_count'] and p['review_count'] > 50]
    products_with_price = [p for p in products if p['min_price']]
    products_with_thc = [p for p in products if p['thc_percent']]

    # Highest THC
    if products_with_thc:
        best['highest_thc'] = max(products_with_thc, key=lambda p: p['thc_percent'] or 0)

    # Best rating (with >50 reviews)
    if products_with_reviews:
        best['best_rating'] = max(products_with_reviews, key=lambda p: p['rating'] or 0)

    # Most reviews
    products_with_count = [p for p in products if p['review_count']]
    if products_with_count:
        best['most_reviews'] = max(products_with_count, key=lambda p: p['review_count'] or 0)

    # Cheapest price
    if products_with_price:
        best['cheapest'] = min(products_with_price, key=lambda p: p['min_price'] or 999)

    # Best price/performance (THC per Euro)
    products_value = [p for p in products if p['thc_percent'] and p['min_price'] and p['min_price'] > 0]
    if products_value:
        best['best_value'] = max(products_value, key=lambda p: (p['thc_percent'] or 0) / (p['min_price'] or 1))

    return best


def generate_product_url(product_id: int) -> str:
    """Generate product URL for shop.dransay.com"""
    return f"https://shop.dransay.com/product/p/{product_id}"


def format_float(value: Optional[float]) -> str:
    """Format float value or return N/A"""
    return str(value) if value is not None else 'N/A'


def generate_overview_markdown(products: List[Dict[str, Any]], best: Dict[str, Dict[str, Any]]) -> str:
    """Generate the markdown content for ../docs/SORTEN_ÜBERSICHT.md"""

    now = datetime.now().strftime('%d.%m.%Y %H:%M')

    md = f"""# Sortenübersicht (Sortiert nach Anzahl der Bewertungen)

Diese Übersicht wird automatisch aus der `../data/WeedDB.db` Datenbank generiert.
**Letzte Aktualisierung:** {now}

Um diese Datei zu aktualisieren, führe aus: `python3 generate_overview.py`

## 🏆 Bestenliste

Hier ist eine Zusammenfassung der Top-Sorten in verschiedenen Kategorien, inklusive Direktlinks zur Produktseite.

| Kategorie | Sorte | Link |
| :--- | :--- | :--- |
"""

    # Add best products
    if 'highest_thc' in best:
        p = best['highest_thc']
        md += f"| **Höchster THC-Gehalt** | {p['name']} | [Link]({generate_product_url(p['id'])}) |\n"

    if 'best_value' in best:
        p = best['best_value']
        md += f"| **Bestes Preis-Leistungs-Verhältnis** | {p['name']} | [Link]({generate_product_url(p['id'])}) |\n"

    if 'cheapest' in best:
        p = best['cheapest']
        md += f"| **Günstigster Preis** | {p['name']} | [Link]({generate_product_url(p['id'])}) |\n"

    if 'best_rating' in best:
        p = best['best_rating']
        md += f"| **Community-Liebling (Beste Bewertung)** | {p['name']} | [Link]({generate_product_url(p['id'])}) |\n"

    if 'most_reviews' in best:
        p = best['most_reviews']
        md += f"| **Am populärsten (Meiste Reviews)** | {p['name']} | [Link]({generate_product_url(p['id'])}) |\n"

    md += """
---

### ⭐ Highlights in der Gesamtliste

Sorten, die in einer der Top-Kategorien die besten sind, sind in der folgenden Tabelle mit einer Trophäe markiert:
- **Am populärsten**: Die Sorte mit den meisten Bewertungen.
- **Community-Liebling**: Die Sorte mit der höchsten Bewertung (bei >50 Reviews).
- **Höchster THC-Gehalt**: Die Sorte mit dem absolut höchsten THC-Prozentsatz.
- **Bestes Preis-Leistungs-Verhältnis**: Das meiste THC pro Euro.
- **Günstigster Preis**: Der absolut niedrigste Preis pro Gramm.

---

| Name | Hersteller | THC (%) | Genetik | Bewertung | Reviews | Günstigster Preis (€/g) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

    # Create lookup for best products
    best_ids = {category: p['id'] for category, p in best.items()}

    # Add all products
    for p in products:
        name_with_link = f"[{p['name']}]({generate_product_url(p['id'])})"

        # Add trophy if product is in a best category
        trophies = []
        if p['id'] == best_ids.get('most_reviews'):
            trophies.append('🏆 **Am populärsten**')
        if p['id'] == best_ids.get('best_rating'):
            trophies.append('🏆 **Community-Liebling**')
        if p['id'] == best_ids.get('highest_thc'):
            trophies.append('🏆 **Höchster THC-Gehalt**')
        if p['id'] == best_ids.get('best_value'):
            trophies.append('🏆 **Bestes Preis-Leistungs-Verhältnis**')
        if p['id'] == best_ids.get('cheapest'):
            trophies.append('🏆 **Günstigster Preis**')

        if trophies:
            name_with_link += ' ' + ' '.join(trophies)

        md += f"| {name_with_link} | {p['producer_name']} | {format_float(p['thc_percent'])} | {p['genetics']} | "
        md += f"{format_float(p['rating'])} | {p['review_count'] or 'N/A'} | {format_float(p['min_price'])} |\n"

    return md


def main() -> None:
    """Main function to generate overview"""
    print("📊 Generiere ../docs/SORTEN_ÜBERSICHT.md...")

    # Get data
    products = get_all_products_with_prices()

    if not products:
        print("❌ Keine Produkte in der Datenbank gefunden!")
        return

    print(f"✅ {len(products)} Produkte gefunden")

    # Calculate best products
    best = calculate_best_products(products)
    print(f"✅ {len(best)} Kategorien für Bestenliste berechnet")

    # Generate markdown
    markdown_content = generate_overview_markdown(products, best)

    # Write to file
    with open('../docs/SORTEN_ÜBERSICHT.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✅ ../docs/SORTEN_ÜBERSICHT.md erfolgreich generiert!")
    print(f"   {len(products)} Produkte")
    print(f"   {len(best)} Top-Kategorien")


if __name__ == '__main__':
    main()
