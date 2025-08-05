import requests
import configparser
import os

# Get the absolute path of the project's root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the path to the config.ini file
config_path = os.path.join(ROOT_DIR, 'config.ini')

# Read the config file
config = configparser.ConfigParser()
config.read(config_path)

# Get the base URL from the config file
BASE_URL = config['settings']['base_url']

def test_get_booking_report_detail(session_id, case_id):
    """
    Tests the get-booking-report-detail endpoint.
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
    assert "latest_status" in response_data["data"]
    assert response_data["data"]["latest_status"] == "COMPLETED"
