import pytest
from helpers import claim_case

def test_ca_claim_case(session_id, case_id):
    """
    Tests the claim-case endpoint and verifies the returned tasks.
    """
    claimed_tasks_data = claim_case(session_id, case_id)
    assert len(claimed_tasks_data) > 0, "claimed_tasks_data should not be empty"

    expected_task_substrings = [
        "customer.information",
        "occupation.informationPresent",
        "bank.1.information",
        "occupation.informationPrevious",
        "informationNewCustomer",
        "document.other",
        "ncb.direct",
        "document.main",
        "informationInterest",
        "informationRevolving",
        "informationTerm",
        "summary.ca"
    ]

    found_task_substrings = []
    for expected_substring in expected_task_substrings:
        found = False
        for task in claimed_tasks_data:
            if expected_substring in task.get("task_method_name", ""):
                found = True
                found_task_substrings.append(expected_substring)
                break
        assert found, f"Expected task substring '{expected_substring}' not found in claimed_tasks_data"

    # Optionally, you can assert that all expected substrings were found
    assert len(found_task_substrings) == len(expected_task_substrings), \
        f"Missing some expected task substrings. Found: {found_task_substrings}, Expected: {expected_task_substrings}"

