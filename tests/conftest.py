import pytest
import requests
import configparser
import os

# Get the absolute path of the project's root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.ini file
config_path = os.path.join(ROOT_DIR, '..', 'config.ini')

# Read the config file
config = configparser.ConfigParser()
config.read(config_path)

# Get the base URL from the config file
BASE_URL = config['settings']['base_url']

@pytest.fixture(scope="session")
def email():
    return config['settings']['email']

@pytest.fixture(scope="session")
def password():
    return config['settings']['password']

@pytest.fixture(scope="function")
def session():
    """
    Provides a requests.Session object for making HTTP requests.
    This fixture has a "function" scope, so a new session is created for each test function.
    """
    with requests.Session() as s:
        yield s