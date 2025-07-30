def test_login(session_id):
    """
    Tests that the session_id fixture is working correctly.
    """
    assert isinstance(session_id, str)
    assert len(session_id) > 0