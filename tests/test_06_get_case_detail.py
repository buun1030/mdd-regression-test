import pytest
import time
from conftest import get_case_detail

def test_get_case_detail(session_id, case_id):
    """
    Tests the get-case-detail endpoint and checks for specific conditions.
    """
    # Delay after batch process complete, as requested
    time.sleep(10)

    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries + 1):
        case_detail = get_case_detail(session_id, case_id)
        if any(item.get("field_name") == "thinker.caDecision" and item.get("value") == "__UNKNOWN__" for item in case_detail["traversal_path"]):
            break
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            # Last attempt failed, print the traversal path for debugging
            traversal_path = case_detail.get("traversal_path")
            print(f"Final attempt failed. Traversal Path: {traversal_path}")
            pytest.fail("Expected 'thinker.caDecision' with '__UNKNOWN__' value not found in traversal_path after retries")
            
    # Assertions for customer_data
    customer_data_list = case_detail.get("customer_data", [])
    loan_status_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "VERIFYING":
            loan_status_found = True
            break
    assert loan_status_found, "Expected 'thinker.loanStatus' with 'VERIFYING' value not found in customer_data"

    # Assertions for verifying_field_list
    verifying_field_list = case_detail.get("verifying_field_list", [])
    assert len(verifying_field_list) > 0, "verifying_field_list should not be empty"

    # Assertions for all_tasks
    all_tasks = case_detail.get("all_tasks", [])
    assert len(all_tasks) > 0, "all_tasks should not be empty"
