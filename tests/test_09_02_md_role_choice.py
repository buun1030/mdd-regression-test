import pytest
from helpers import get_task_details

def test_md_role_choice(session_id, case_id):
    """
    Tests role choice that list correctly.
    """
    task_details = get_task_details(session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "verifying_fields" in detail_data and "summary" in detail_data.get("verification_method_name", ""):
            for field_i in detail_data["verifying_fields"]:
                field = field_i.get("field")
                if field.get("field_name") == "thinker.roleAssignment":
                    # Check if the role choice is present: CA, SCA, CM, MD, CC, EC
                    choices = field.get("choices", [])
                    expected_roles = ["CA", "SCA", "CM", "MD", "CC", "EC"]
                    for role in expected_roles:
                        assert any(choice.get("value") == role for choice in choices), \
                            f"Expected role '{role}' not found in choices for field 'thinker.roleAssignment'"
                    break