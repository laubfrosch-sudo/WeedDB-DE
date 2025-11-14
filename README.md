# WeedDB Project

This project scrapes and manages cannabis product data from `shop.dransay.com`.

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

---

## Quick Start

1.  **Clone Repository**
    ```bash
    git clone https://github.com/laubfrosch-sudo/WeedDB.git
    cd WeedDB
    ```

2.  **Install Dependencies**
    ```bash
    pip3 install playwright
    python3 -m playwright install
    ```

3.  **Initialize Database**
    ```bash
    sqlite3 WeedDB.db < schema.sql
    ```

4.  **Run a Script**
    ```bash
    # Add a single new product
    python3 add_product.py "<product_url_from_shop.dransay.com>"

    # Update all existing products
    python3 update_all_products.py
    ```

For more detailed information, please see `INSTRUCTIONS.md` (English) or `ANLEITUNG.md` (Deutsch).

---
---

# WeedDB Projekt

Dieses Projekt dient dem Scrapen und Verwalten von Cannabis-Produktdaten von `shop.dransay.com`.

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

---

## Schnellstart

1.  **Repository klonen**
    ```bash
    git clone https://github.com/laubfrosch-sudo/WeedDB.git
    cd WeedDB
    ```

2.  **Abhängigkeiten installieren**
    ```bash
    pip3 install playwright
    python3 -m playwright install
    ```

3.  **Datenbank initialisieren**
    ```bash
    sqlite3 WeedDB.db < schema.sql
    ```

4.  **Skript ausführen**
    ```bash
    # Einzelnes neues Produkt hinzufügen
    python3 add_product.py "<produkt_url_von_shop.dransay.com>"

    # Alle bestehenden Produkte aktualisieren
    python3 update_all_products.py
    ```

Für detailliertere Informationen siehe `INSTRUCTIONS.md` (Englisch) oder `ANLEITUNG.md` (Deutsch).
