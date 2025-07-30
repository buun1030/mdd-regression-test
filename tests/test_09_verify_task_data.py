import pytest

def test_verify_task_data(verified_tasks):
    """
    Tests that the verified_tasks fixture is working correctly.
    """
    assert verified_tasks is None # The fixture asserts success internally
