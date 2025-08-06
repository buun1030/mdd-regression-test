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
