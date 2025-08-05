import pytest
import time
from conftest import claim_case, release_case

def test_md_claim_case(session_id, case_id):
    """
    Tests the claim-case endpoint and verifies the returned tasks.
    """
    time.sleep(5)
    
    release_case(session_id, case_id) # avoid the case is already claimed by previous role
    claimed_tasks_data = claim_case(session_id, case_id)
    assert len(claimed_tasks_data) > 0, "claimed_tasks_data should not be empty"

    expected_task_substrings = [
        "summary.md"
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

