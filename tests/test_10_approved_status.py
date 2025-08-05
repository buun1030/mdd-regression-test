
import pytest
import time
from conftest import get_case_detail

def test_approved_status(session_id, case_id):
    """
    Tests that the approved_status is working correctly and checks for APPROVED status.
    """

    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries + 1):
        case_detail = get_case_detail(session_id, case_id)
        if any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == "APPROVED" for item in case_detail["customer_data"]) and \
           case_detail.get("remaining_verifying_field_list") == []:
            break
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            # Last attempt failed, print the customer_data and remaining_verifying_field_list for debugging
            customer_data = case_detail.get("customer_data", [])
            remaining_verifying_field_list = case_detail.get("remaining_verifying_field_list", [])
            print(f"Final attempt failed. Customer Data: {customer_data}")
            print(f"Remaining Verifying Field List: {remaining_verifying_field_list}")
            pytest.fail("Expected 'thinker.loanStatus' to be APPROVED and remaining_verifying_field_list to be empty after retries")
    
    # Assertions for customer_data
    customer_data_list = case_detail.get("customer_data", [])
    loan_status_approved_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "APPROVED":
            loan_status_approved_found = True
            break
    assert loan_status_approved_found, "Expected 'thinker.loanStatus' with 'APPROVED' value not found in customer_data"
    
    # Assertions for all_tasks
    all_tasks = case_detail.get("all_tasks", [])
    assert len(all_tasks) > 0, "all_tasks should not be empty"

    # Assertions for verifying_field_list
    verifying_field_list = case_detail.get("verifying_field_list", [])
    assert len(verifying_field_list) > 0, "verifying_field_list should not be empty"
    
    # Assertions for remaining_verifying_field_list
    remaining_verifying_field_list = case_detail.get("remaining_verifying_field_list", [])
    assert remaining_verifying_field_list == [], "remaining_verifying_field_list should be empty"