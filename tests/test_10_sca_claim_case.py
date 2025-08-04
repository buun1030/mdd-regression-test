import pytest

def test_sca_claim_case(sca_claimed_tasks_data):
    """
    Tests the claim-case endpoint and verifies the returned tasks.
    """
    assert len(sca_claimed_tasks_data) > 0, "sca_claimed_tasks_data should not be empty"

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
        "summary"
    ]

    found_task_substrings = []
    for expected_substring in expected_task_substrings:
        found = False
        for task in sca_claimed_tasks_data:
            if expected_substring in task.get("task_method_name", ""):
                found = True
                found_task_substrings.append(expected_substring)
                break
        assert found, f"Expected task substring '{expected_substring}' not found in claimed_tasks_data"

    # Optionally, you can assert that all expected substrings were found
    assert len(found_task_substrings) == len(expected_task_substrings), \
        f"Missing some expected task substrings. Found: {found_task_substrings}, Expected: {expected_task_substrings}"

