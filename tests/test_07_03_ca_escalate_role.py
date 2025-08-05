import pytest
from conftest import edit_task_data, get_task_details

def test_ca_escalate_role(session_id, case_id):
    """
    Tests that the ca escalate_role is working correctly.
    """
    task_details = get_task_details(session_id, case_id)
    for task_id, detail_data in task_details.items():
        # Extract field_name and current_value from required_fields
        required_fields = []
        if "required_fields" in detail_data:
            for field_i in detail_data["required_fields"]:
                field = field_i.get("field")
                required_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})
                
        payload = {
            "task_id": task_id,
            "required_fields": required_fields,
            "editing_fields": [
                {
                    "field_name": "thinker.roleAssignment",
                    "field_value": "SCA"
                }
            ]
        }
        if "verification_method_name" in detail_data and "summary" in detail_data["verification_method_name"]:
            # Call the escalate_role function with the payload
            edit_task_data(session_id, payload)
