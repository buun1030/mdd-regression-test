def test_submit_case(submitted_case_id):
    """
    Tests that the submitted_case_id fixture is working correctly.
    """
    assert isinstance(submitted_case_id, str)
    assert len(submitted_case_id) > 0
