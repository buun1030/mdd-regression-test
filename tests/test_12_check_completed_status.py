import pytest
import time
from conftest import get_case_detail

def test_completed_status(session_id, case_id):
    """
    Tests that the completed_status is working correctly and checks for COMPLETED status.
    """
    # Delay to allow processing
    time.sleep(10)
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries + 1):
        case_detail = get_case_detail(session_id, case_id)
        if any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == "COMPLETED" for item in case_detail["customer_data"]) and \
           any(item.get("field_name") == "thinker.loanResult" and item.get("value") == "A02" for item in case_detail["customer_data"]) and \
           case_detail.get("status") == "completed":
            break
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            # Last attempt failed, print the customer_data and status for debugging
            customer_data = case_detail.get("customer_data")
            status = case_detail.get("status")
            print(f"Final attempt failed. Customer Data: {customer_data}")
            print(f"Status: {status}")
            pytest.fail("Expected 'thinker.loanStatus' to be COMPLETED, 'thinker.loanResult' to be A02, and status to be completed after retries")

    customer_data_list = case_detail.get("customer_data", [])
    loan_status_completed_found = False
    loan_result_a02_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "COMPLETED":
            loan_status_completed_found = True
        if item.get("field_name") == "thinker.loanResult" and item.get("value") == "A02":
            loan_result_a02_found = True
    assert loan_status_completed_found, "Expected 'thinker.loanStatus' with 'COMPLETED' value not found in customer_data"
    assert loan_result_a02_found, "Expected 'thinker.loanResult' with 'A02' value not found in customer_data"

    status_field = case_detail.get("status")
    assert status_field == "completed", f"Expected status to be 'completed', but got '{status_field}'"