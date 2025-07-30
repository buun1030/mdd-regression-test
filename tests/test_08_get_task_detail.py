import pytest

def test_get_task_detail(task_details):
    """
    Tests that the task_details fixture is working correctly.
    """
    assert len(task_details) > 0, "task_details should not be empty"
    for task_id, detail_data in task_details.items():
        assert "verifying_fields" in detail_data
        assert "required_fields" in detail_data
