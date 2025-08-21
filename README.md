# API Regression Tests

This project contains automated regression tests for a sample API, written in Python using `pytest`.

## Setup

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running Tests

*   **Run all tests:**
    ```bash
    pytest
    ```

*   **Run tests in parallel:**
    ```bash
    pytest -n auto
    ```

*   **Run tests in parallel with report:**
    ```bash
    pytest -n auto --tb=short --html=report.html
    ```

## Project Structure

```
.
├── requirements.txt
├── tests/
└── config.ini
```