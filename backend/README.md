# Backend

This directory contains the Python backend for the application.

## Setup and Running

1. **Install uv**

    It is recommended to use `uv` for package management. Follow the instructions at [astral.sh](https://docs.astral.sh/uv/getting-started/installation/) to install `uv`. For macOS and Linux, you can use:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. **Create virtual environment and install dependencies**

    Navigate to the `backend` directory and sync the dependencies. This will create a virtual environment (`.venv`) and install the packages listed in `pyproject.toml`.

    ```bash
    cd backend
    uv sync
    ```

3. **Activate virtual environment**

    ```bash
    source .venv/bin/activate
    ```

4. **Run the servers**

    You need to run two services in separate terminals from the `backend` directory (with the virtual environment activated).

    * **Terminal 1: Flask App**

        ```bash
        python api/flask-app.py
        ```

    * **Terminal 2: Uvicorn App**

        ```bash
        uvicorn main:app --reload
        ```
