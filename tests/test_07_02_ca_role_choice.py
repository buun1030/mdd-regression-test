import pytest
from helpers import get_task_details

def test_sca_role_choice(session_id, case_id):
    """
    Tests role choice that list correctly.
    """
    task_details = get_task_details(session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "verifying_fields" in detail_data and "summary" in detail_data.get("verification_method_name", ""):
            for field_i in detail_data["verifying_fields"]:
                field = field_i.get("field")
                if field.get("field_name") == "thinker.roleAssignment":
                    # Check if the role choice is present: CA, SCA
                    choices = field.get("choices", [])
                    expected_must_have_roles = ["CA", "SCA"]
                    for role in expected_must_have_roles:
                        assert any(choice.get("value") == role for choice in choices), \
                            f"Expected role '{role}' not found in choices for field 'thinker.roleAssignment'"
                    # Check that roles not expected are not present
                    expected_must_not_have_roles = ["CM", "MD", "CC", "EC"]
                    for role in expected_must_not_have_roles:
                        assert not any(choice.get("value") == role for choice in choices), \
                            f"Unexpected role '{role}' found in choices for field 'thinker.roleAssignment'"
                    break