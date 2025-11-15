#!/usr/bin/env python3
"""
Generate charts and visualizations from WeedDB database.

This script creates various charts for price trends, product distributions,
and analytics that can be embedded in Obsidian notes.

Usage:
    python3 generate_charts.py
"""

import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import os
from pathlib import Path

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'WeedDB.db')
CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'assets', 'charts')

def setup_matplotlib_style() -> None:
    """Configure matplotlib for better-looking charts"""
    plt.style.use('seaborn-v0_8')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10


def get_price_history_data() -> List[Dict[str, Any]]:
    """Get price history data for top products"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.name,
            pr.price_per_g,
            pr.timestamp,
            pr.category
        FROM products p
        JOIN prices pr ON p.id = pr.product_id
        WHERE p.review_count > 100
        ORDER BY p.name, pr.timestamp
    """)

    data = []
    for row in cursor.fetchall():
        data.append({
            'name': row[0],
            'price': row[1],
            'timestamp': datetime.fromisoformat(row[2]),
            'category': row[3]
        })

    conn.close()
    return data


def get_product_distribution_data() -> Dict[str, Any]:
    """Get data for product distribution charts"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Genetics distribution
    cursor.execute("""
        SELECT genetics, COUNT(*) as count
        FROM products
        WHERE genetics IS NOT NULL AND genetics != 'N/A'
        GROUP BY genetics
        ORDER BY count DESC
    """)
    genetics_data = dict(cursor.fetchall())

    # THC distribution
    cursor.execute("""
        SELECT
            CASE
                WHEN thc_percent < 20 THEN '< 20%'
                WHEN thc_percent BETWEEN 20 AND 24.9 THEN '20-24%'
                WHEN thc_percent BETWEEN 25 AND 29.9 THEN '25-29%'
                WHEN thc_percent >= 30 THEN '30%+'
                ELSE 'Unknown'
            END as thc_range,
            COUNT(*) as count
        FROM products
        WHERE thc_percent IS NOT NULL
        GROUP BY thc_range
        ORDER BY count DESC
    """)
    thc_data = dict(cursor.fetchall())

    # Rating distribution
    cursor.execute("""
        SELECT
            ROUND(rating, 1) as rating_rounded,
            COUNT(*) as count
        FROM products
        WHERE rating IS NOT NULL
        GROUP BY rating_rounded
        ORDER BY rating_rounded
    """)
    rating_data = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return {
        'genetics': genetics_data,
        'thc': thc_data,
        'rating': rating_data
    }


def create_price_trend_chart(data: List[Dict[str, Any]], output_path: str) -> None:
    """Create price trend chart for top products"""
    # Group data by product and category
    product_data: Dict[str, List[Tuple[datetime, float]]] = {}
    for item in data:
        key = f"{item['name']} ({item['category']})"
        if key not in product_data:
            product_data[key] = []
        product_data[key].append((item['timestamp'], item['price']))

    # Sort by number of data points and take top 5
    top_products = sorted(product_data.items(),
                         key=lambda x: len(x[1]),
                         reverse=True)[:5]

    plt.figure(figsize=(14, 8))

    for product_name, points in top_products:
        if len(points) > 1:  # Only plot if we have multiple data points
            timestamps, prices = zip(*sorted(points))
            plt.plot(timestamps, prices, marker='o', linewidth=2, markersize=4,
                    label=product_name[:30] + '...' if len(product_name) > 30 else product_name)

    plt.title('Preisverlauf Top-Produkte (letzte 30 Tage)', fontsize=16, pad=20)
    plt.xlabel('Datum', fontsize=12)
    plt.ylabel('Preis (€/g)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def create_genetics_pie_chart(genetics_data: Dict[str, float], output_path: str) -> None:
    """Create genetics distribution pie chart"""
    # Filter out small categories
    total = sum(genetics_data.values())
    filtered_data = {k: v for k, v in genetics_data.items() if v/total > 0.05}
    other_count = sum(v for k, v in genetics_data.items() if k not in filtered_data)
    if other_count > 0:
        filtered_data['Andere'] = other_count

    plt.figure(figsize=(10, 8))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

    wedges, texts, autotexts = plt.pie(list(filtered_data.values()),
                                      labels=list(filtered_data.keys()),
                                      autopct='%1.1f%%',
                                      colors=colors[:len(filtered_data)],
                                      startangle=90,
                                      textprops={'fontsize': 11})

    plt.title('Genetik-Verteilung der Produkte', fontsize=16, pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def create_thc_distribution_chart(thc_data: Dict[str, int], output_path: str) -> None:
    """Create THC percentage distribution bar chart"""
    plt.figure(figsize=(12, 6))

    ranges = list(thc_data.keys())
    counts = list(thc_data.values())

    bars = plt.bar(ranges, counts, color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels on bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{count}', ha='center', va='bottom', fontweight='bold')

    plt.title('THC-Gehalt-Verteilung', fontsize=16, pad=20)
    plt.xlabel('THC-Bereich', fontsize=12)
    plt.ylabel('Anzahl Produkte', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def create_rating_distribution_chart(rating_data: Dict[float, int], output_path: str) -> None:
    """Create rating distribution histogram"""
    plt.figure(figsize=(12, 6))

    ratings = list(rating_data.keys())
    counts = list(rating_data.values())

    bars = plt.bar(ratings, counts, width=0.1, color='#FF6B6B', alpha=0.8,
                   edgecolor='black', linewidth=1, align='center')

    # Add value labels
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{count}', ha='center', va='bottom', fontweight='bold')

    plt.title('Bewertungsverteilung der Produkte', fontsize=16, pad=20)
    plt.xlabel('Bewertung (Sterne)', fontsize=12)
    plt.ylabel('Anzahl Produkte', fontsize=12)
    plt.xticks([i/10 for i in range(25, 46, 5)])  # 2.5 to 4.5 stars
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def create_visualization_markdown(distribution_data: Dict[str, Any], output_path: str) -> None:
    """Create markdown file with embedded charts"""
    total_products = sum(distribution_data['genetics'].values())
    avg_rating = sum(k*v for k,v in distribution_data['rating'].items()) / sum(distribution_data['rating'].values())

    markdown_content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
version: 0.1.0
author: Claude AI
status: alpha
description: Datenvisualisierungen und Diagramme für WeedDB
---

# 📊 WeedDB Datenvisualisierungen

Diese Seite enthält automatisch generierte Diagramme und Visualisierungen der WeedDB-Daten.
**Letzte Aktualisierung:** {datetime.now().strftime('%d.%m.%Y %H:%M')}

## 📈 Preisverläufe

### Top-Produkte Preisverlauf
![Preisverlauf Top-Produkte](assets/charts/price_trends.png)
*Preisverlauf der 5 meistbewerteten Produkte über die letzten 30 Tage*

## 🧬 Produktverteilungen

### Genetik-Verteilung
![Genetik-Verteilung](assets/charts/genetics_distribution.png)
*Verteilung der Genetik-Typen (Indica, Sativa, Hybrid) in der Datenbank*

### THC-Gehalt-Verteilung
![THC-Verteilung](assets/charts/thc_distribution.png)
*Verteilung der THC-Prozentsätze in verschiedenen Bereichen*

### Bewertungsverteilung
![Bewertungsverteilung](assets/charts/rating_distribution.png)
*Verteilung der Kundenbewertungen (1-5 Sterne)*

## 📋 Statistiken Übersicht

| Metrik | Wert |
|--------|------|
| Gesamtprodukte | {total_products} |
| Durchschnittliche Bewertung | {avg_rating:.2f} ⭐ |
| Höchster THC-Gehalt | 30%+ |
| Niedrigster THC-Gehalt | < 20% |

## 🔄 Automatische Generierung

Diese Diagramme werden automatisch mit dem Skript `generate_charts.py` erstellt:

```bash
python3 scripts/generate_charts.py
```

Das Skript sollte nach jeder größeren Datenbank-Aktualisierung ausgeführt werden, um die Visualisierungen aktuell zu halten.
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)


def main() -> None:
    """Main function to generate all charts"""
    print("📊 Generiere WeedDB-Diagramme...")

    # Setup
    setup_matplotlib_style()
    charts_dir = Path(CHARTS_DIR)
    charts_dir.mkdir(parents=True, exist_ok=True) # Use parents=True to create parent directories if they don't exist

    # Get data
    print("📥 Lade Daten aus Datenbank...")
    price_data = get_price_history_data()
    distribution_data = get_product_distribution_data()

    print(f"✅ {len(price_data)} Preisdatensätze gefunden")
    print(f"✅ {sum(distribution_data['genetics'].values())} Produkte für Verteilungen")

    # Generate charts
    print("📈 Erstelle Preisverlauf-Diagramm...")
    create_price_trend_chart(price_data, str(charts_dir / 'price_trends.png'))

    print("🥧 Erstelle Genetik-Verteilungsdiagramm...")
    create_genetics_pie_chart(distribution_data['genetics'], str(charts_dir / 'genetics_distribution.png'))

    print("📊 Erstelle THC-Verteilungsdiagramm...")
    create_thc_distribution_chart(distribution_data['thc'], str(charts_dir / 'thc_distribution.png'))

    print("⭐ Erstelle Bewertungsverteilungsdiagramm...")
    create_rating_distribution_chart(distribution_data['rating'], str(charts_dir / 'rating_distribution.png'))

    print("📝 Erstelle Visualisierungs-Seite...")
    markdown_output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'DATEN_VISUALISIERUNGEN.md')
    create_visualization_markdown(distribution_data, markdown_output_path)

    print("✅ Alle Diagramme erfolgreich generiert!")
    print(f"   📁 Gespeichert in: {charts_dir}")
    print("   📄 Markdown-Seite: docs/DATEN_VISUALISIERUNGEN.md")


if __name__ == '__main__':
    main()