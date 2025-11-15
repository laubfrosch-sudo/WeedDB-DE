---
created: 2024-02-01
updated: 2025-11-15
version: 0.1.0
author: laubfrosch-sudo
status: alpha
language: en
target_audience: All Users
description: Guide for interacting with AI assistants (Claude/Gemini) to manage WeedDB
sync_with: ANLEITUNG.md
---

# How to Interact with the AI Assistant (v0.1.0 Alpha)

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This document explains how to interact with an AI assistant (like Gemini or Claude) within this directory to use, query, and manage the `WeedDB` database. The assistant is aware of the project structure, the available scripts, and the database schema.

**New:**
- Enhanced batch processing with timeout protection
- Automatic data correction for missing producers
- Extended producer recognition (24+ known manufacturers)
- Robust price extraction with multiple fallback methods

## 1. Querying the Database

You can ask questions in natural language to get information from the database. The assistant will execute the appropriate queries and present the results.

**Example Prompts:**

*   `Which strain has the best price-to-performance ratio for getting high?`
*   `Show me the top 5 strains with the highest THC content.`
*   `What is the URL for "Grape Face"?`
*   `Which strains have an earthy taste and a relaxing effect?`
*   **NEW:** `Compare prices for "Gelato" across all pharmacies.`
*   **NEW:** `Which pharmacy has the cheapest prices overall?`
*   **NEW:** `Show me products with the biggest price differences between pharmacies.`

**Advanced Queries:**

For comprehensive SQL query examples (60+ examples), see `QUERY_EXAMPLES.md`. This includes:
- Multi-pharmacy price comparisons
- Product search by terpenes, effects, and therapeutic uses
- Statistics and analytics
- Best value calculations (THC-to-price ratio)

## 2. Updating and Managing Data

The assistant can maintain the database for you by executing the project's scripts.

### Updating All Products

If prices or other data points in the database are outdated, you can trigger a full refresh.

**Example Prompts:**

*   `Now, please adjust all data records correctly according to the actual websites.`
*   `Update the entire database.`
*   `Perform a complete database update.`

The assistant will then run the `update_prices.py` script, which processes all products in small batches to avoid timeouts.

**New Option:**
*   `Automatically correct missing manufacturer data.`

Runs the new `fix_producers.py` script, which automatically corrects missing producer information.

### Finding and Adding New Products

To find new products from `shop.dransay.com` that are not yet in the database, and then add them:

**1. Identify New Products (`find_new_products.py`)
Ask the assistant to find new products. You can use filters like `vendorId`, `producerId`, or `search`.

**Example Prompt:**
*   `Find new products on shop.dransay.com.`
*   `Find new Haze strains from top pharmacies.`

The assistant will run the `find_new_products.py` script and present you with a list of newly found products.

**2. Add Products to the Database (`add_product.py`)
Once you have identified new products, you can add them individually. The `add_product.py` script automatically checks if the product already exists. If it exists, it updates the product details and prices; otherwise, it adds a new product.

**Example Prompt:**
*   `Add the product "Pink Diesel".`
*   `Add the product with ID 12345.`
### Correcting Data

If you find an error in the data (e.g., an incorrect THC value), you can ask the assistant to correct it.

**Example Prompt:**

*   `The THC for "Big Purple Dragon" from Remexian is actually 22%, not 30%. Please correct it.`

## 3. Using the Overview File (`docs/generated/SORTEN_ÜBERSICHT.md`)

The `docs/generated/SORTEN_ÜBERSICHT.md` file is a dynamically generated overview of all products in the database. You can ask the assistant to update or modify this file.

### Regenerating the Overview

After a major data update, the overview should be regenerated to reflect the changes.

**Example Prompts:**

*   `Regenerate the overview file.`
*   `Update the Markdown overview.`

### Customizing the Overview

You can also request changes to the structure and content of the overview file.

**Example Prompts:**

*   `Create a separate overview for Indica strains only, sorted by THC content.`
*   `Add a column showing the top-3 terpenes for each strain.`
*   `Show producer/manufacturer information in the overview.`
*   `Create a price comparison table with the 3 cheapest pharmacies per product.`
*   `Group strains by genetics (Indica/Sativa/Hybrid) in separate tables.`
*   `Add a column for therapeutic uses/medical applications.`
