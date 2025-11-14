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

### Open-Source Models (via Ollama)

With **Ollama**, you can run powerful open-source models (like Llama 3, Code Llama) directly on your own machine. This is an excellent way to have a local AI assistant in your terminal.

1.  **Install Ollama**:
    *   **macOS**: Download the app from [ollama.com](https://ollama.com) or use Homebrew: `brew install ollama`.
    *   **Windows**: Download the `.exe` installer from [ollama.com](https://ollama.com).
    *   **Linux**: Run the installation script: `curl -fsSL https://ollama.com/install.sh | sh`.

2.  **Download and Run a Model**: After installation, you can pull a model of your choice. `llama3` is a great starting point.
    ```bash
    # Downloads the model (on first run) and starts a chat session
    ollama run llama3
    ```

3.  **Use the Model**: You can now use Ollama in your terminal at any time for general questions or code analysis.

---

## Step 4: Putting It All Together

After following these steps, your system is fully configured. You can now:
- Run the project's Python scripts (e.g., `python3 update_all_products.py`).
- Interact with the integrated AI assistant to manage the database.
- Use `Ollama` for local AI tasks.

For more details on how to interact with the assistant for this specific project, see the `INSTRUCTIONS.md` file.
