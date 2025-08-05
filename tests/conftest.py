import pytest
import requests
import configparser
import os
import time
import json

# Get the absolute path of the project's root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.ini file
config_path = os.path.join(ROOT_DIR, '..', 'config.ini')

# Read the config file
config = configparser.ConfigParser()
config.read(config_path)

# Get the base URL, email, and password from the config file
BASE_URL = config['settings']['base_url']
EMAIL = config['settings']['email']
PASSWORD = config['settings']['password']

@pytest.fixture(scope="session")
def session_id():
    """
    Logs in to the API and returns the session ID.
    This fixture has a "session" scope, so it will only run once per test session.
    """
    login_url = f"{BASE_URL}/authentication/api/v1/login"
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(login_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    response_data = response.json()
    return response_data["data"]["session_id"]

@pytest.fixture(scope="session")
def case_id(session_id):
    """
    Applies for a product and returns the case ID.
    This fixture has a "session" scope, so it will only run once per test session.
    """
    apply_url = f"{BASE_URL}/question-taskpool/api/v1/apply-for-product"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "product_name": config['settings']['product_name']
    }
    response = requests.post(apply_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    response_data = response.json()
    generated_case_id = response_data["data"]["case_id"]
    print(f"Generated Case ID: {generated_case_id}")
    return generated_case_id

def submitted_case_id(session_id, case_id):
    """
    Submits the case and returns the case_id.
    Depends on answered_questions to ensure questions are answered before submission.
    """
    submit_url = f"{BASE_URL}/case-datasources/api/v1/cases/submit"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    response = requests.post(submit_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes
    response_data = response.json()
    assert "case_id" in response_data
    assert "case_submission_id" in response_data
    assert "message" in response_data
    assert response_data["message"] == "processing"
    return case_id

def completed_batch_process(session_id, case_id):
    """
    Performs the batch-process-complete API call with retry logic.
    This fixture ensures the batch process is completed before dependent fixtures/tests run.
    """
    batch_process_url = f"{BASE_URL}/case-datasources/api/v1/callback/batch-process-complete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    # Initial delay after submit case
    time.sleep(5)

    max_retries = 3
    retry_delay = 3  # seconds
    response = None

    for attempt in range(max_retries + 1):
        response = requests.post(batch_process_url, json=payload, headers=headers)
        if response.status_code == 200:
            break  # Success, exit loop
        elif response.status_code == 500 and attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Received 500. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            # Other status code or last retry failed with 500
            break

    # Final assertions after all attempts
    assert response.status_code == 200, \
        f"Expected 200, but got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == "0"

def answered_questions(session_id, case_id, answers_payload):
    """
    Answers questions for the case.
    """
    answer_url = f"{BASE_URL}/question-taskpool/api/v1/answer-question"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }

    payload = {
        "case_id": case_id,
        "answers": answers_payload
    }

    response = requests.post(answer_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0

def get_case_detail(session_id, case_id):
    """
    Fetches case details and returns the 'data' portion of the response.
    Includes retry logic for eventual consistency.
    """
    get_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-case-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    response = requests.post(get_detail_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes (e.g., 4xx or 5xx)
    response_data = response.json()
    
    assert "data" in response_data
    return response_data["data"]

def claim_case(session_id, case_id):
    """
    Claims the case and returns the 'data' portion of the response.
    This is a helper function, not a fixture.
    """
    # Add a delay to allow the case to become claimable
    time.sleep(5)
    
    claim_url = f"{BASE_URL}/question-taskpool/api/v1/claim-case"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    response = requests.post(claim_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0
    assert "data" in response_data
    assert isinstance(response_data["data"], list)
    return response_data["data"]

def release_case(session_id, case_id):
    """
    Releases the case to make it available for other users.
    This is a helper function, not a fixture.
    """
    release_url = f"{BASE_URL}/question-taskpool/api/v1/release-case"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }
    response = requests.post(release_url, json=payload, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0

def get_task_ids(session_id, case_id):
    """
    Claims tasks and extracts the task_id values.
    This is a helper function, not a fixture.
    """
    
    # Add a delay to all data are updated
    time.sleep(5)
    
    get_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-case-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }
    
    response = requests.post(get_detail_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes (e.g., 4xx or 5xx)
    response_data = response.json()
    
    task_ids = []
    if "data" in response_data and "all_tasks" in response_data["data"] and isinstance(response_data["data"]["all_tasks"], list):
        for task in response_data["data"]["all_tasks"]:
            if "task_id" in task and task.get("status") == "claimed":
                task_ids.append(task["task_id"])
    
    return task_ids 

def get_task_details(session_id, case_id):
    """
    Fetches details for each task_id and returns a dictionary of task_id to its detail data.
    This is a helper function, not a fixture, so it can be called multiple times for fresh data.
    """
    time.sleep(5)
    
    task_ids = get_task_ids(session_id, case_id)
    task_detail_map = {}
    for task_id in task_ids:
        get_task_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-task-detail"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_id}"
        }
        payload = {
            "task_id": task_id,
            "all_task_mode": False
        }
        try:
            response = requests.post(get_task_detail_url, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            assert "code" in response_data
            assert response_data["code"] == 0
            assert "data" in response_data
            task_detail_map[task_id] = response_data["data"]
        except requests.exceptions.HTTPError as e:
            print(f"\nError fetching task detail for task_id: {task_id}")
            print(f"\n{e}\nResponse Text: {e.response.text}")
            raise
    task_detail_map_path = os.path.join(ROOT_DIR, '..', 'task_detail_map.json')
    with open(task_detail_map_path, "w") as f:
        f.write(json.dumps(task_detail_map, indent=4))
    return task_detail_map

def edit_task_data(session_id, payload):
    """
    Edit field value via tasks and submit.
    """ 
    edit_task_url = f"{BASE_URL}/question-taskpool/api/v1/edit-task-data"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    
    response = requests.post(edit_task_url, json=payload, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0

def verified_tasks(session_id, case_id):
    """
    Verifies task data for each task after an edit has been made.
    """
    task_details = get_task_details(session_id, case_id)
    for task_id, detail_data in task_details.items():
        verify_task_url = f"{BASE_URL}/question-taskpool/api/v1/verify-task-data"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_id}"
        }
        # Extract field_name and current_value from verifying_fields and required_fields
        verifying_fields = []
        if "verifying_fields" in detail_data:
            for field_i in detail_data["verifying_fields"]:
                field = field_i.get("field")
                verifying_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})

        required_fields = []
        if "required_fields" in detail_data:
            for field_i in detail_data["required_fields"]:
                field = field_i.get("field")
                required_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})

        payload = {
            "task_id": task_id,
            "verifying_fields": verifying_fields,
            "required_fields": required_fields
        }
        task = detail_data.get("task")
        if task.get("status") == "claimed":
            try:
                response = requests.post(verify_task_url, json=payload, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                assert "code" in response_data
                assert response_data["code"] == 0
            except requests.exceptions.HTTPError as e:
                print(f"\nError verifying task: {task_id} with verification method: {detail_data.get('verification_method_name')}")
                print(f"\n{e}\nResponse Text: {e.response.text}")
                raise
            
def get_booking_detail(session_id, case_id):
    """
    Edit field value via tasks and submit.
    """ 
    get_report_url = f"{BASE_URL}/question-taskpool/api/v1/get-booking-report-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    response = requests.post(get_report_url, json=payload, headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    
    assert "data" in response_data
    return response_data["data"]
