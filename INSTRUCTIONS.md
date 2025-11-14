# How to Interact with the AI Assistant

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB](https://github.com/laubfrosch-sudo/WeedDB)

This document explains how to interact with an AI assistant (like Gemini or Claude) within this directory to use, query, and manage the `WeedDB` database. The assistant is aware of the project structure, the available scripts, and the database schema.

## 1. Querying the Database

You can ask questions in natural language to get information from the database. The assistant will execute the appropriate queries and present the results.

**Example Prompts:**

*   `Which strain has the best price-to-performance ratio for getting high?`
*   `Show me the top 5 strains with the highest THC content.`
*   `What is the URL for "Grape Face"?`
*   `Which strains have an earthy taste and a relaxing effect?`

## 2. Updating and Managing Data

The assistant can maintain the database for you by executing the project's scripts.

### Updating All Products

If prices or other data points in the database are outdated, you can trigger a full refresh.

**Example Prompts:**

*   `Now, please adjust all data records correctly according to the actual websites.`
*   `Update the entire database.`

The assistant will then run the `update_all_products.py` script.

### Adding a Single Product

You can add new strains from `shop.dransay.com` by simply providing the URL to the assistant.

**Example Prompt:**

*   `Add this product: <product_url>`

### Correcting Data

If you find an error in the data (e.g., an incorrect THC value), you can ask the assistant to correct it.

**Example Prompt:**

*   `The THC for "Big Purple Dragon" from Remexian is actually 22%, not 30%. Please correct it.`

## 3. Using the Overview File (`SORTEN_ÜBERSICHT.md`)

The `SORTEN_ÜBERSICHT.md` file is a dynamically generated overview of all products in the database. You can ask the assistant to update or modify this file.

### Regenerating the Overview

After a major data update, the overview should be regenerated to reflect the changes.

**Example Prompts:**

*   `Regenerate the overview file.`
*   `Update the Markdown overview.`

### Customizing the Overview

You can also request changes to the structure and content of the overview file.

**Example Prompts:**

*   `Can you somehow highlight the strains in the overview that are the best in any category?`
*   `Also, add a link to the correct page for the strain in the "Best of" list.`
*   `The remaining strains in the main table should also have links.`
