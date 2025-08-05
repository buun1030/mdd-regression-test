from conftest import get_booking_detail

def test_get_booking_detail(session_id, case_id):
    """
    Tests the get-booking-detail endpoint.
    """
    booking_detail = get_booking_detail(session_id, case_id)
    
    assert "latest_status" in booking_detail
    assert booking_detail["latest_status"] == "COMPLETED"
