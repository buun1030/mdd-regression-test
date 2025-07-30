import pytest

def test_check_completed_status(completed_case_detail_data):
    """
    Tests that the completed_case_detail_data fixture is working correctly and checks for COMPLETED status.
    """
    assert completed_case_detail_data is not None

    customer_data_list = completed_case_detail_data.get("customer_data", [])
    loan_status_completed_found = False
    loan_result_a02_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "COMPLETED":
            loan_status_completed_found = True
        if item.get("field_name") == "thinker.loanResult" and item.get("value") == "A02":
            loan_result_a02_found = True
    assert loan_status_completed_found, "Expected 'thinker.loanStatus' with 'COMPLETED' value not found in customer_data"
    assert loan_result_a02_found, "Expected 'thinker.loanResult' with 'A02' value not found in customer_data"

    status_field = completed_case_detail_data.get("status")
    assert status_field == "completed", f"Expected status to be 'completed', but got '{status_field}'"