from helpers import submitted_case_id

def test_submit_case(session_id, case_id):
    """
    Tests that the submitted_case_id fixture is working correctly.
    """
    case_id = submitted_case_id(session_id, case_id)
    assert isinstance(case_id, str)
    assert len(case_id) > 0
