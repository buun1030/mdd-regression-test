from conftest import completed_batch_process

def test_batch_process_complete(session_id, case_id):
    """
    Tests that the completed_batch_process fixture is working correctly.
    """
    case_id = completed_batch_process(session_id, case_id)
