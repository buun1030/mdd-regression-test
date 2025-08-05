import pytest
import time
from conftest import verified_tasks, get_case_detail

def test_verify_task_data(session_id, case_id):
    """
    Tests that the verified_tasks fixture is working correctly.
    """
    verified_tasks(session_id, case_id)
    
    # Delay to allow processing
    time.sleep(5)
    
    case_detail = get_case_detail(session_id, case_id)
    
    # Assertions for remaining_verifying_field_list
    remaining_verifying_field_list = case_detail.get("remaining_verifying_field_list", [])
    assert remaining_verifying_field_list == [], "remaining_verifying_field_list should be empty"