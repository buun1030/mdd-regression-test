import pytest

def test_apply_for_product(case_id):
    """
    Tests that the case_id fixture is working correctly.
    """
    assert isinstance(case_id, str)
    assert len(case_id) > 0
