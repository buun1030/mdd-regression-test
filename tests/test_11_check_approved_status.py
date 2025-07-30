import pytest

def test_check_approved_status(approved_case_detail_data):
    """
    Tests that the approved_case_detail_data fixture is working correctly and checks for APPROVED status.
    """
    assert approved_case_detail_data is not None

    customer_data_list = approved_case_detail_data.get("customer_data", [])
    loan_status_approved_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "APPROVED":
            loan_status_approved_found = True
            break
    assert loan_status_approved_found, "Expected 'thinker.loanStatus' with 'APPROVED' value not found in customer_data"

    remaining_verifying_field_list = approved_case_detail_data.get("remaining_verifying_field_list", [])
    assert remaining_verifying_field_list == [], "remaining_verifying_field_list should be empty"