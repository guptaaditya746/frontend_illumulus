# Project Title (Replace with your project's actual title)

(Add a brief description of your project here)

## Installation

Follow these steps to set up the project environment and install the necessary dependencies.

### Prerequisites

*   **Python:** Ensure you have Python installed on your system. This project was developed with Python (you can specify the version if you know it, e.g., Python 3.9+). You can download Python from [python.org](https://www.python.org/).
*   **pip:** Python's package installer, which usually comes with Python.
*   **Git:** For cloning the repository (if the user doesn't have the code yet).

### Setup Steps

1.  **Clone the Repository (Optional):**
    If you haven't downloaded the code yet, clone the repository to your local machine:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    It's highly recommended to use a virtual environment to manage project-specific dependencies. This keeps your global Python installation clean.

    *   **Create the virtual environment (e.g., named `venv`):**
        ```bash
        python -m venv ai_story_exhibit_venv
        ```
        (On some systems, you might need to use `python3` instead of `python`)

    *   **Activate the virtual environment:**
        *   On macOS and Linux:
            ```bash
            source venv/bin/activate
            ```
        *   On Windows (Command Prompt):
            ```bash
            .\ai_story_exhibit_venv\Scripts\activate
            ```
        *   On Windows (PowerShell):
            ```bash
            .\ai_story_exhibit_venv\Scripts\Activate.ps1
            ```
        You should see the virtual environment's name (e.g., `(venv)`) prefixed to your command prompt.

3.  **Install Dependencies:**
    With your virtual environment activated, install all the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
    This command will read the `/home/prims/frontend_illumulus/ai-story-exhibit/requirements.txt` file and install all the listed packages and their specified versions.

4.  **Potential System-Level Dependencies (Note for Users):**
    Some Python packages, especially those for computer vision (like OpenCV) or deep learning, might have underlying system-level dependencies.
    *   For example, if you encounter errors related to missing shared libraries like `libGL.so.1` (common for OpenCV on headless systems), you might need to install them via your system's package manager.
        *   On Debian/Ubuntu: `sudo apt-get update && sudo apt-get install libgl1-mesa-glx`
        *   On Fedora/RHEL/CentOS: `sudo yum install mesa-libGL` or `sudo dnf install mesa-libGL`
    *   If running in a specific environment (like a Slurm cluster), you might need to load environment modules provided by the cluster administrators.

    (You can adjust this section based on common issues you or your users have faced.)

### Running the Application
```cmd
streamlit run app.py
```
---

