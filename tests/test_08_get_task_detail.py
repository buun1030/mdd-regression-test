import pytest
from conftest import get_task_details

def test_get_task_detail(session_id, case_id):
    """
    Tests that the task_details fixture is working correctly.
    """
    task_details = get_task_details(session_id, case_id)
    assert len(task_details) > 0, "task_details should not be empty"
    for task_id, detail_data in task_details.items():
        assert "verifying_fields" in detail_data
        assert "required_fields" in detail_data
