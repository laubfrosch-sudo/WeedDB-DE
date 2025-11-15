---
created: 2025-11-15
updated: 2025-11-15
version: 0.1.0
author: laubfrosch-sudo
status: alpha
description: Guide for setting up AI tools for terminal interaction with WeedDB
---

# AI Installation: A Guide for the AI-Powered Terminal

This document serves as a first-time setup guide to prepare your computer for interacting with AI assistants (like Gemini, Claude, or open-source models) directly in the terminal. The goal is to enable you to use and manage the `WeedDB` database with the help of AI.

## Overview of Components

1.  **Modern Terminal**: A powerful command-line interface is the foundation.
2.  **System Dependencies**: Software required by the project (e.g., Python, SQLite).
3.  **Project Setup**: Setting up the `WeedDB` project locally.
4.  **AI Tools**: Configuring tools to access AI models.

---

## Step 1: OS-Specific Setup

Choose the guide for your operating system.

### macOS

1.  **Install Package Manager (Homebrew)**: Homebrew is essential for easily installing software on macOS. Open the pre-installed `Terminal.app` and run the following command:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Install a Modern Terminal (iTerm2)**: iTerm2 is a popular replacement for the default terminal.
    ```bash
    brew install --cask iterm2
    ```
    *From now on, always open iTerm2 instead of the default Terminal app.*

3.  **Install Python & SQLite**:
    ```bash
    brew install python sqlite
    ```

### Windows

For Windows, the recommended approach is the **Windows Subsystem for Linux (WSL)**, as it provides a seamless Linux environment preferred by developers.

1.  **Install Windows Terminal**: Download "Windows Terminal" from the Microsoft Store. It's a modern interface for all your command-line tools.

2.  **Install WSL**: Open Windows Terminal (as Administrator) and install WSL with its default Linux distribution (Ubuntu).
    ```powershell
    wsl --install
    ```
    After a restart, you will be prompted to create a username and password for your new Linux environment.

3.  **Install Dependencies in WSL**: Open Windows Terminal with an Ubuntu/WSL tab and proceed with the Linux instructions.

### Linux (Debian / Ubuntu)

1.  **Update Your System**:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2.  **Install Python & SQLite**:
    ```bash
    sudo apt install python3 python3-pip sqlite3 git -y
    ```

---

## Step 2: Project Setup

These steps are the same for all operating systems (on Windows, they are performed inside WSL/Ubuntu).

1.  **Clone the Project Directory** (if you haven't already):
    ```bash
    # Replace <repository_url> with the actual URL
    git clone https://github.com/laubfrosch-sudo/WeedDB.git
    cd WeedDB
    ```

2.  **Install Python Dependencies**: The project uses `playwright` for web scraping.
    ```bash
    pip3 install playwright
    ```

3.  **Install Playwright Browsers**:
    ```bash
    python3 -m playwright install
    ```

4.  **Initialize the Database**: This creates the `WeedDB.db` file and its table structure.
    ```bash
    sqlite3 WeedDB.db < schema.sql
    ```

---

## Step 3: AI Assistant Setup

### Proprietary Models (Gemini, Claude)

The interaction with commercial models like Gemini and Claude, which you might be using right now, is often integrated into a specific development environment or tool. There is typically no simple, public "Gemini CLI" or "Claude CLI" to download.

For custom use in your own scripts, you would generally:
1.  Obtain an **API Key** from the respective provider (Google, Anthropic).
2.  Set this key as an environment variable (e.g., `export GOOGLE_API_KEY="YOUR_KEY"`).
3.  Use the corresponding client library in Python to send requests to the AI.

**For this project, the interaction is already provided by the terminal tool you are using.**

### OpenCode - Your AI Coding Assistant

**OpenCode** is the primary AI tool for interacting with this project. It provides specialized support for software development and database management.

#### Why OpenCode?
- **Code Specialized**: Optimized for programming and technical tasks
- **Project Context**: Knows the WeedDB structure and available scripts
- **Direct Terminal Integration**: Works seamlessly with your local files
- **Security**: Local processing without cloud dependencies

#### Using OpenCode:
1. **Launch OpenCode** in your terminal
2. **Navigate to project**: `cd /path/to/WeedDB`
3. **Ask for help**: "How do I add a new product?" or "Update all prices"

#### Example Interactions:
```bash
# Add product
opencode: "Add the product 'Blue Dream' to the database"

# Query database
opencode: "Show me the 5 most expensive products"

# Code analysis
opencode: "Optimize the add_product.py script"
```

### Grok Code - Alternative AI Support

**Grok Code** provides alternative AI support with a focus on explanatory and helpful coding.

#### Grok Code Features:
- **Explanatory Answers**: Detailed explanations of code and concepts
- **Broad Knowledge**: Comprehensive knowledge across programming languages
- **Interactive Help**: Step-by-step guidance
- **Code Generation**: Automatic creation of code snippets

#### Grok Code for WeedDB:
- **Database Queries**: "How do I create a SQL query for all Indica strains?"
- **Script Optimization**: "Improve the performance of update_prices.py"
- **Troubleshooting**: "Why isn't the scraping working?"

---

## Step 4: Putting It All Together

After following these steps, your system is fully configured. You can now:
- Run the project's Python scripts (e.g., `python3 scripts/update_prices.py`).
- Interact with **OpenCode** to manage the database and develop code.
- Use **Grok Code** as alternative AI support for complex questions.

For more details on how to interact with the assistant for this specific project, see the `INSTRUCTIONS.md` file.

---

## Dynamische Übersichtsdateien

**Wichtiger Hinweis:** Die Datei `docs/generated/SORTEN_ÜBERSICHT.md` wird mit dem Skript `generate_overview.py` aus der `WeedDB.db` Datenbank generiert. 

**Nach dem Hinzufügen oder Aktualisieren von Produkten MUSS das Skript ausgeführt werden:**

```bash
python3 generate_overview.py
```

Das Skript erstellt eine sortierte Übersicht aller Produkte mit:
- Bestenliste (höchster THC, bester Preis, Community-Liebling, etc.)
- Vollständige Produkttabelle sortiert nach Bewertungsanzahl
- Direkte Links zu allen Produktseiten auf shop.dransay.com
- Automatischen Timestamp der letzten Aktualisierung

**WICHTIG:** Die Übersicht ist nur so aktuell wie die Daten in der Datenbank und die letzte Ausführung des Skripts!
