import requests
import time
import json
import os
import configparser

# Get the absolute path of the project's root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.ini file
config_path = os.path.join(ROOT_DIR, '..', 'config.ini')

# Read the config file
config = configparser.ConfigParser()
config.read(config_path)

# Get the base URL from the config file
BASE_URL = config['settings']['base_url']

def login(session, email, password):
    """
    Logs in to the API and returns the session ID.
    """
    login_url = f"{BASE_URL}/authentication/api/v1/login"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    with session.post(login_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        return response_data["data"]["session_id"]

def apply_for_product(session, session_id, product_name):
    """
    Applies for a product and returns the case ID.
    """
    apply_url = f"{BASE_URL}/question-taskpool/api/v1/apply-for-product"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "product_name": product_name
    }
    with session.post(apply_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        generated_case_id = response_data["data"]["case_id"]
        print(f"Generated Case ID: {generated_case_id}")
        return generated_case_id

def answer_questions(session, session_id, case_id, answers_payload):
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

    with session.post(answer_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        assert "code" in response_data
        assert response_data["code"] == 0

def submit_case(session, session_id, case_id):
    """
    Submits the case and returns the case_id.
    """
    submit_url = f"{BASE_URL}/case-datasources/api/v1/cases/submit"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    with session.post(submit_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        print(f"Submit Case Response: {response_data}")
        assert "case_id" in response_data
        assert "case_submission_id" in response_data
        assert "message" in response_data
        assert response_data["message"] == "processing"
        return case_id

def complete_batch_process(session, session_id, case_id):
    """
    Performs the batch-process-complete API call with retry logic.
    """
    batch_process_url = f"{BASE_URL}/case-datasources/api/v1/callback/batch-process-complete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    time.sleep(10)

    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries + 1):
        with session.post(batch_process_url, json=payload, headers=headers) as response:
            if response.status_code == 200:
                break
            elif response.status_code == 500 and attempt < max_retries:
                print(f"Attempt {attempt + 1}/{max_retries + 1}: Received {response.status_code}. Response: {response.text}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Final attempt for complete_batch_process failed. Status: {response.status_code}. Response: {response.text}")
                break

    assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == "0"

def get_case_detail(session, session_id, case_id):
    """
    Fetches case details and returns the 'data' portion of the response.
    """
    get_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-case-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    with session.post(get_detail_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        assert "data" in response_data
        return response_data["data"]

def claim_case(session, session_id, case_id):
    """
    Claims the case and returns the 'data' portion of the response.
    """
    time.sleep(5)
    
    claim_url = f"{BASE_URL}/question-taskpool/api/v1/claim-case"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    with session.post(claim_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        assert "code" in response_data
        assert response_data["code"] == 0
        assert "data" in response_data
        assert isinstance(response_data["data"], list)
        return response_data["data"]

def release_case(session, session_id, case_id):
    """
    Releases the case to make it available for other users.
    """
    release_url = f"{BASE_URL}/question-taskpool/api/v1/release-case"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }
    with session.post(release_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        assert "code" in response_data
        assert response_data["code"] == 0

def get_task_ids(session, session_id, case_id):
    """
    Claims tasks and extracts the task_id values.
    """
    time.sleep(5)
    
    get_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-case-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }
    
    with session.post(get_detail_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        
        task_ids = []
        if "data" in response_data and "all_tasks" in response_data["data"] and isinstance(response_data["data"]["all_tasks"], list):
            for task in response_data["data"]["all_tasks"]:
                if "task_id" in task and task.get("status") == "claimed":
                    task_ids.append(task["task_id"])
        
        return task_ids

def get_task_details(session, session_id, case_id):
    """
    Fetches details for each task_id and returns a dictionary of task_id to its detail data.
    """
    time.sleep(10)
    
    task_ids = get_task_ids(session, session_id, case_id)
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
            with session.post(get_task_detail_url, json=payload, headers=headers) as response:
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
    # task_detail_map_path = os.path.join(ROOT_DIR, '..', 'task_detail_map.json')
    # with open(task_detail_map_path, "w") as f:
    #     f.write(json.dumps(task_detail_map, indent=4))
    return task_detail_map

def edit_task_data(session, session_id, payload):
    """
    Edit field value via tasks and submit.
    """
    edit_task_url = f"{BASE_URL}/question-taskpool/api/v1/edit-task-data"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    
    with session.post(edit_task_url, json=payload, headers=headers) as response:
        response.raise_for_status()
        response_data = response.json()
        assert "code" in response_data
        assert response_data["code"] == 0

def verify_tasks(session, session_id, case_id):
    """
    Verifies task data for each task after an edit has been made.
    """
    task_details = get_task_details(session, session_id, case_id)
    for task_id, detail_data in task_details.items():
        verify_task_url = f"{BASE_URL}/question-taskpool/api/v1/verify-task-data"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_id}"
        }
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
                with session.post(verify_task_url, json=payload, headers=headers) as response:
                    response.raise_for_status()
                    response_data = response.json()
                    assert "code" in response_data
                    assert response_data["code"] == 0
            except requests.exceptions.HTTPError as e:
                print(f"\nError verifying task: {task_id} with verification method: {detail_data.get('verification_method_name')}")
                print(f"\n{e}\nResponse Text: {e.response.text}")
                raise

def get_booking_detail(session, session_id, case_id):
    """
    Gets the booking report detail.
    """
    get_report_url = f"{BASE_URL}/question-taskpool/api/v1/get-booking-report-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    with session.post(get_report_url, json=payload, headers=headers) as response:
        assert response.status_code == 200
        response_data = response.json()
        assert "data" in response_data
        return response_data["data"]