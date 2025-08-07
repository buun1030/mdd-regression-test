# API Regression Tests

This project contains automated regression tests for a sample API. The tests are written in Python using the `pytest` framework and the `requests` library.

## Prerequisites

Before you can run the tests, you need to have the following installed on your system:

*   **Python 3.6+**: You can download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   **pip**: `pip` is the package installer for Python. It usually comes with Python. You can check if you have it installed by running `pip --version` in your terminal.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Create a virtual environment:**
    It's a good practice to create a virtual environment to isolate the project's dependencies.
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**
    Install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure the API key:**
    The tests require an API key to access the API. Create a file named `config.ini` in the root directory of the project and add the following content:
    ```ini
    [settings]
    base_url = https://moneydd-dev.thinkerfint.com
    email = moneydd-dev@thinkerfint.com
    password = moneydd-dev
    product_name = moneydd.pLoan
    thinker_workspace = Develop
    ```
    Replace `moneydd-dev@thinkerfint.com` and `moneydd-dev` with your actual login credentials.

## Running the Tests

To run the tests, simply execute the following command in your terminal (make sure your virtual environment is activated):

```bash
pytest
```

If you encounter a `command not found` error, you can also run the tests using this more explicit command:

```bash
python3 -m pytest
```

## Project Structure

```
.
├── requirements.txt
├── tests
│   ├── conftest.py
│   ├── test_01_login.py
│   ├── test_02_apply_for_product.py
│   ├── test_03_answer_question.py
│   ├── test_04_submit_case.py
│   ├── test_05_batch_process_complete.py
│   ├── test_06_get_case_detail.py
│   ├── test_07_claim_case.py
│   ├── test_08_get_task_detail.py
│   ├── test_09_verify_task_data.py
│   ├── test_10_first_additional_answer.py
│   ├── test_11_check_approved_status.py
│   ├── test_12_second_additional_answer.py
│   ├── test_13_check_completed_status.py
│   ├── test_14_get_booking_detail.py
│   └── test_other_features.py
└── config.ini
```

*   `requirements.txt`: Lists the Python dependencies required for the project.
*   `tests/`: Contains all the test files.
*   `tests/conftest.py`: Contains `pytest` fixtures, including the `session_id` fixture for login, `case_id` fixture for applying for a product, `answered_questions` for answering questions, `submitted_case_id` for submitting a case, `completed_batch_process` for batch process completion, `get_case_detail` for getting case details, `claimed_tasks_data` for claiming tasks, `task_ids` for extracting task IDs, `task_details` for getting task details, `verified_tasks` for verifying task data, `first_additional_answer_success` for sending the first additional answer, `approved_status` for checking approved status, `customer_decision` for sending the second additional answer, and `completed_get_case_detail` for checking completed status.
*   `tests/test_01_login.py`: Test file for the login functionality.
*   `tests/test_02_apply_for_product.py`: Test file for the apply for product functionality.
*   `tests/test_03_answer_question.py`: Test file for answering questions.
*   `tests/test_04_submit_case.py`: Test file for submitting a case.
*   `tests/test_05_batch_process_complete.py`: Test file for the batch process complete callback.
*   `tests/test_06_get_case_detail.py`: Test file for getting case details.
*   `tests/test_07_claim_case.py`: Test file for claiming a case.
*   `tests/test_08_get_task_detail.py`: Test file for getting task details.
*   `tests/test_09_verify_task_data.py`: Test file for verifying task data.
*   `tests/test_10_first_additional_answer.py`: Test file for sending the first additional answer.
*   `tests/test_11_check_approved_status.py`: Test file for checking approved status.
*   `tests/test_12_second_additional_answer.py`: Test file for sending the second additional answer.
*   `tests/test_13_check_completed_status.py`: Test file for checking completed status.
*   `tests/test_14_get_booking_detail.py`: Test file for getting booking report details.
*   `tests/test_other_features.py`: Example test file demonstrating the use of the `session_id` fixture.
*   `config.ini`: Configuration file for the API base URL, login credentials, product name, and Thinker-Workspace.

## Adding New Tests

To add a new test case, simply create a new function in any test file (e.g., `tests/test_other_features.py`) that starts with `test_`. If your test requires authentication, you can simply add `session_id` as an argument to your test function, and `pytest` will automatically provide the session ID from the fixture. If your test requires a `case_id`, you can add `case_id` as an argument. If your test requires `task_ids`, you can add `task_ids` as an argument.

For example:

```python
def test_get_user_by_id(session_id):
    user_id = 1
    headers = {
        'Authorization': f'Bearer {session_id}'
    }
    # Assuming your API has a /users/{id} endpoint
    response = requests.get(f'{BASE_URL}/users/{user_id}', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['id'] == user_id
```

This test will check if the API returns a single user when a valid user ID is provided, using the authenticated session.
