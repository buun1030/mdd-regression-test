import pytest

def test_get_case_detail(case_detail_data):
    """
    Tests the get-case-detail endpoint and checks for specific conditions.
    """
    # Assertions for customer_data
    customer_data_list = case_detail_data.get("customer_data", [])
    loan_status_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "VERIFYING":
            loan_status_found = True
            break
    assert loan_status_found, "Expected 'thinker.loanStatus' with 'VERIFYING' value not found in customer_data"

    # Assertions for verifying_field_list
    verifying_field_list = case_detail_data.get("verifying_field_list", [])
    assert len(verifying_field_list) > 0, "verifying_field_list should not be empty"

    # Assertions for all_tasks
    all_tasks = case_detail_data.get("all_tasks", [])
    assert len(all_tasks) > 0, "all_tasks should not be empty"
