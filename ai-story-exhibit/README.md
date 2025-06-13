# Project Title (Replace with your project's actual title)

This repo serve the frontend for illumulus 2025 using streamlit
## Setup Steps

Follow these steps to set up and run the project:

1.  **Navigate to the project directory:**
    Open your terminal (Linux/macOS) or Command Prompt/PowerShell (Windows).
    The original instructions were `cd frontend_illumulus/ai-story-exhibit`. Ensure you navigate into the main `ai-story-exhibit` directory where the `requirements.txt` and `main.py` files are located.
    For example, if you cloned a repository named `ai-story-exhibit`, you would typically do:
    ```bash
    cd ai-story-exhibit
    ```

2.  **Create a Python virtual environment:**
    In the project directory, it's highly recommended to create a virtual environment. Run:
    ```bash
    python -m venv ai_story_venv
    ```
    *(Note: If `python` on your system points to an older Python 2 version, or if you prefer to be explicit, you can use `python3 -m venv ai_story_venv`)*

3.  **Activate the virtual environment:**
    *   **On macOS and Linux (bash, zsh, etc.):**
        ```bash
        source ai_story_venv/bin/activate
        ```
    *   **On Windows (Command Prompt):**
        ```cmd
        ai_story_venv\Scripts\activate.bat
        ```
    *   **On Windows (PowerShell):**
        ```powershell
        .\ai_story_venv\Scripts\Activate.ps1
        ```
        *(If you encounter an error in PowerShell regarding script execution being disabled, you might need to adjust your execution policy. For example, you could run PowerShell as an administrator and execute `Set-ExecutionPolicy RemoteSigned -Scope Process` or `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` and then try activating again.)*

4.  **Install dependencies:**
    Once the virtual environment is active (you should see `(ai_story_venv)` in your prompt), install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    streamlit run main.py
    ```
---
