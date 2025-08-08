import pytest
import time
from .scenarios import NORMAL_HAPPY_PATH_SCENARIOS, GSB_LEAD_HAPPY_PATH_SCENARIOS
from . import workflow_helpers as wf

@pytest.mark.parametrize("scenario", NORMAL_HAPPY_PATH_SCENARIOS, ids=lambda s: s["test_id"])
def test_normal_workflow(session, email, password, scenario):
    """
    Tests the entire end-to-end user workflow from login to booking.
    Each run is independent and driven by its scenario data.
    """
    print(f"--- Starting Test: {scenario["test_id"]} ---")

    print("Step 1: Logging in...")
    # Step 1: Login
    session_id = wf.login(session, email, password)
    assert session_id
    print("Step 1: Login successful.")

    print("Step 2: Applying for Product...")
    # Step 2: Apply for Product
    case_id = wf.apply_for_product(session, session_id, scenario["product_name"])
    assert case_id
    print(f"Step 2: Product applied. Case ID: {case_id}")

    print("Step 3: Answering Initial Questions...")
    # Step 3: Answer Initial Questions
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["initial_questions"])
    print("Step 3: Initial Questions answered.")

    print("Step 4: Submitting Case...")
    # Step 4: Submit Case
    wf.submit_case(session, session_id, case_id)
    print("Step 4: Case submitted.")

    print("Step 5: Completing Batch Process...")
    # Step 5: Complete Batch Process
    wf.complete_batch_process(session, session_id, case_id)
    print("Step 5: Batch Process completed.")

    print("Step 6: Verifying Case Details (CA Decision Unknown, Loan Status VERIFYING, etc.)...")
    # Step 6.1: Verify CA Decision is Unknown
    time.sleep(10)
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries + 1):
        case_detail = wf.get_case_detail(session, session_id, case_id)
        if any(item.get("field_name") == "thinker.caDecision" and item.get("value") == "__UNKNOWN__" for item in case_detail["traversal_path"]):
            break
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            pytest.fail("Expected 'thinker.caDecision' with '__UNKNOWN__' value not found after retries")

    # Step 6.2: Verify Loan Status is VERIFYING
    customer_data_list = case_detail.get("customer_data", [])
    loan_status_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "VERIFYING":
            loan_status_found = True
            break
    assert loan_status_found, "Expected 'thinker.loanStatus' with 'VERIFYING' value not found in customer_data"

    # Step 6.3: Verify Verifying Field List is Not Empty
    verifying_field_list = case_detail.get("verifying_field_list", [])
    assert len(verifying_field_list) > 0, "verifying_field_list should not be empty"

    # Step 6.4: Verify All Tasks are Not Empty
    all_tasks = case_detail.get("all_tasks", [])
    assert len(all_tasks) > 0, "all_tasks should not be empty"
    print("Step 6: Case Details verified.")
    
    print("Step 7: CA Role...")
    # Step 7.1: CA Claim Case
    print("  7.1: Claiming CA case...")
    claimed_tasks_data = wf.claim_case(session, session_id, case_id)
    assert len(claimed_tasks_data) > 0, "claimed_tasks_data should not be empty"
    print("  7.1: CA case claimed.")

    expected_task_substrings = scenario["expected"]["task_name_substrings"]["ca"]

    found_task_substrings = []
    for expected_substring in expected_task_substrings:
        found = False
        for task in claimed_tasks_data:
            if expected_substring in task.get("task_method_name", ""):
                found = True
                found_task_substrings.append(expected_substring)
                break
        assert found, f"Expected task substring '{expected_substring}' not found in claimed_tasks_data"

    assert len(found_task_substrings) == len(expected_task_substrings), \
        f"Missing some expected task substrings. Found: {found_task_substrings}, Expected: {expected_task_substrings}"
    print("  7.1: CA tasks verified.")
        
    # Step 7.2: Verify available escalation roles in CA tasks
    print("  7.2: Verifying available escalation roles for CA...")
    task_details = wf.get_task_details(session, session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "verifying_fields" in detail_data and "summary" in detail_data.get("verification_method_name", ""):
            for field_i in detail_data["verifying_fields"]:
                field = field_i.get("field")
                if field.get("field_name") == "thinker.roleAssignment":
                    # Check if the role choice is present
                    choices = field.get("choices", [])
                    expected_must_have_roles = scenario["expected"]["available_escalation_roles"]["ca"]
                    for role in expected_must_have_roles:
                        assert any(choice.get("value") == role for choice in choices), \
                            f"Expected role '{role}' not found in choices for field 'thinker.roleAssignment'"
                    # Check that roles not expected are not present
                    expected_must_not_have_roles = scenario["expected"]["unavailable_escalation_roles"]["ca"]
                    for role in expected_must_not_have_roles:
                        assert not any(choice.get("value") == role for choice in choices), \
                            f"Unexpected role '{role}' found in choices for field 'thinker.roleAssignment'"
                    break
    print("  7.2: Escalation roles for CA verified.")

    # Step 7.3: Escalate CA Role to SCA
    print("  7.3: Escalating CA Role to SCA...")
    for task_id, detail_data in task_details.items():
        if "verification_method_name" in detail_data and "summary" in detail_data["verification_method_name"]:
            required_fields = []
            if "required_fields" in detail_data:
                for field_i in detail_data["required_fields"]:
                    field = field_i.get("field")
                    required_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})
            payload = {
                "task_id": task_id,
                "required_fields": required_fields,
                "editing_fields": [
                    {"field_name": "thinker.roleAssignment", "field_value": scenario["escalations"]["ca_to_sca"]}
                ]
            }
            wf.edit_task_data(session, session_id, payload)
    print("  7.3: CA Role escalated to SCA.")
    print("Step 7: CA Role completed.")

    print("Step 8: SCA Role...")
    # Step 8.1: SCA Claim Case
    print("  8.1: Claiming SCA case...")
    claimed_tasks_data = wf.claim_case(session, session_id, case_id)
    assert len(claimed_tasks_data) > 0, "claimed_tasks_data should not be empty"
    print("  8.1: SCA case claimed.")
    
    expected_task_substrings = scenario["expected"]["task_name_substrings"]["sca"]
    
    found_task_substrings = []
    for expected_substring in expected_task_substrings:
        found = False
        for task in claimed_tasks_data:
            if expected_substring in task.get("task_method_name", ""):
                found = True
                found_task_substrings.append(expected_substring)
                break
        assert found, f"Expected task substring '{expected_substring}' not found in claimed_tasks_data"
        
    assert len(found_task_substrings) == len(expected_task_substrings), \
        f"Missing some expected task substrings. Found: {found_task_substrings}, Expected: {expected_task_substrings}"
    print("  8.1: SCA tasks verified.")
    
    # Step 8.2: Verify available escalation roles in SCA tasks
    print("  8.2: Verifying available escalation roles for SCA...")
    task_details = wf.get_task_details(session, session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "verifying_fields" in detail_data and "summary" in detail_data.get("verification_method_name", ""):
            for field_i in detail_data["verifying_fields"]:
                field = field_i.get("field")
                if field.get("field_name") == "thinker.roleAssignment":
                    # Check if the role choice is present
                    choices = field.get("choices", [])
                    expected_roles = scenario["expected"]["available_escalation_roles"]["sca"]
                    for role in expected_roles:
                        assert any(choice.get("value") == role for choice in choices), \
                            f"Expected role '{role}' not found in choices for field 'thinker.roleAssignment'"
                    # Check that roles not expected are not present
                    expected_must_not_have_roles = scenario["expected"]["unavailable_escalation_roles"]["sca"]
                    for role in expected_must_not_have_roles:
                        assert not any(choice.get("value") == role for choice in choices), \
                            f"Unexpected role '{role}' found in choices for field 'thinker.roleAssignment'"
                    break
    print("  8.2: Available escalation roles verified.")

    # Step 8.3: Verify SCA tasks
    print("  8.3: Verifying SCA tasks...")
    wf.verify_tasks(session, session_id, case_id)
    time.sleep(5) 
    case_detail = wf.get_case_detail(session, session_id, case_id)
    remaining_verifying_field_list = case_detail.get("remaining_verifying_field_list", [])
    assert remaining_verifying_field_list == [], "remaining_verifying_field_list should be empty"
    print("  8.3: SCA tasks verified.")

    # Step 8.4: Escalate SCA Role to MD
    print("  8.4: Escalating SCA Role to MD...")
    for task_id, detail_data in task_details.items():
        if "verification_method_name" in detail_data and "summary" in detail_data["verification_method_name"]:
            required_fields = []
            if "required_fields" in detail_data:
                for field_i in detail_data["required_fields"]:
                    field = field_i.get("field")
                    required_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})
            payload = {
                "task_id": task_id,
                "required_fields": required_fields,
                "editing_fields": [
                    {"field_name": "thinker.roleAssignment", "field_value": scenario["escalations"]["sca_to_md"]}
                ]
            }
            wf.edit_task_data(session, session_id, payload)
    print("  8.4: SCA Role escalated to MD.")
    print("Step 8: SCA Role completed.")

    print("Step 9: MD Role...")
    # Step 9.1: MD Claim Case
    claimed_tasks_data = wf.claim_case(session, session_id, case_id)
    assert len(claimed_tasks_data) > 0, "claimed_tasks_data should not be empty"

    expected_task_substrings = scenario["expected"]["task_name_substrings"]["md"]
    
    found_task_substrings = []
    for expected_substring in expected_task_substrings:
        found = False
        for task in claimed_tasks_data:
            if expected_substring in task.get("task_method_name", ""):
                found = True
                found_task_substrings.append(expected_substring)
                break
        assert found, f"Expected task substring '{expected_substring}' not found in claimed_tasks_data"

    assert len(found_task_substrings) == len(expected_task_substrings), \
        f"Missing some expected task substrings. Found: {found_task_substrings}, Expected: {expected_task_substrings}"
    
    # Step 9.2: Verify available escalation roles in MD tasks
    task_details = wf.get_task_details(session, session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "verifying_fields" in detail_data and "summary" in detail_data.get("verification_method_name", ""):
            for field_i in detail_data["verifying_fields"]:
                field = field_i.get("field")
                if field.get("field_name") == "thinker.roleAssignment":
                    # Check if the role choice is present
                    choices = field.get("choices", [])
                    expected_roles = scenario["expected"]["available_escalation_roles"]["md"]
                    for role in expected_roles:
                        assert any(choice.get("value") == role for choice in choices), \
                            f"Expected role '{role}' not found in choices for field 'thinker.roleAssignment'"
                    # Check that roles not expected are not present
                    expected_must_not_have_roles = scenario["expected"]["unavailable_escalation_roles"]["md"]
                    for role in expected_must_not_have_roles:
                        assert not any(choice.get("value") == role for choice in choices), \
                            f"Unexpected role '{role}' found in choices for field 'thinker.roleAssignment'"
                    break
    
    # Step 9.3: MD Decision
    wf.release_case(session, session_id, case_id)
    wf.claim_case(session, session_id, case_id)
    task_details = wf.get_task_details(session, session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "verification_method_name" in detail_data and "summary" in detail_data["verification_method_name"]:
            required_fields = []
            if "required_fields" in detail_data:
                for field_i in detail_data["required_fields"]:
                    field = field_i.get("field")
                    required_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})
            payload = {
                "task_id": task_id,
                "required_fields": required_fields,
                "editing_fields": [
                    {"field_name": "thinker.caDecision", "field_value": scenario["md_decision"]}
                ]
            }
            wf.edit_task_data(session, session_id, payload)
    print("Step 9: MD Role completed.")

    print("Step 10: Approved Status...")
    # Step 10.1: Verify Approved Status
    time.sleep(10)
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries + 1):
        case_detail = wf.get_case_detail(session, session_id, case_id)
        print(f"Attempt {attempt + 1}: Case Detail for Approved Status: {case_detail}") # Added logging
        loan_status_approved_found = any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == "APPROVED" for item in case_detail["customer_data"])
        remaining_verifying_field_list_empty = case_detail.get("remaining_verifying_field_list") == []
        
        if loan_status_approved_found and remaining_verifying_field_list_empty:
            break
        elif attempt < max_retries:
            print(f"Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            customer_data = case_detail.get("customer_data", [])
            remaining_verifying_field_list = case_detail.get("remaining_verifying_field_list", [])
            pytest.fail(f"Expected 'thinker.loanStatus' to be APPROVED and remaining_verifying_field_list to be empty after retries. Current loanStatus: {[item['value'] for item in customer_data if item['field_name'] == 'thinker.loanStatus']}, Remaining verifying fields: {remaining_verifying_field_list}")
            
    # Step 10.2: Verify Loan Status is APPROVED
    customer_data_list = case_detail.get("customer_data", [])
    loan_status_approved_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "APPROVED":
            loan_status_approved_found = True
            break
    assert loan_status_approved_found, "Expected 'thinker.loanStatus' with 'APPROVED' value not found in customer_data"

    # Step 10.3: Verify Verifying Field List is Not Empty
    verifying_field_list = case_detail.get("verifying_field_list", [])
    assert len(verifying_field_list) > 0, "verifying_field_list should not be empty"
    
    # Step 10.4: Verify Remaining Verifying Field List is Empty
    remaining_verifying_field_list = case_detail.get("remaining_verifying_field_list", [])
    assert remaining_verifying_field_list == [], "remaining_verifying_field_list should be empty"

    # Step 10.5: Verify All Tasks are Not Empty
    all_tasks = case_detail.get("all_tasks", [])
    assert len(all_tasks) > 0, "all_tasks should not be empty"
    print("Step 10: Approved Status verified.")
    
    print("Step 11: Customer Decision...")
    # Step 11: Customer Decision
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["customer_decision"])
    print("Step 11: Customer Decision answered.")

    print("Step 12: Completed Status...")
    # Step 12: Verify Completed Status
    time.sleep(10)
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries + 1):
        case_detail = wf.get_case_detail(session, session_id, case_id)
        print(f"Attempt {attempt + 1}: Case Detail for Completed Status: {case_detail}") # Added logging
        loan_status_completed_found = any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == scenario["expected"]["final_status"] for item in case_detail["customer_data"])
        loan_result_a02_found = any(item.get("field_name") == "thinker.loanResult" and item.get("value") == scenario["expected"]["loan_result"] for item in case_detail["customer_data"])
        status_completed = case_detail.get("status") == "completed"

        if loan_status_completed_found and loan_result_a02_found and status_completed:
            break
        elif attempt < max_retries:
            print(f"Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            customer_data = case_detail.get("customer_data", [])
            status = case_detail.get("status")
            pytest.fail(f"Expected final status conditions not met after retries. Current loanStatus: {[item['value'] for item in customer_data if item['field_name'] == 'thinker.loanStatus']}, loanResult: {[item['value'] for item in customer_data if item['field_name'] == 'thinker.loanResult']}, status: {status}")

    customer_data_list = case_detail.get("customer_data", [])
    loan_status_completed_found = False
    loan_result_a02_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "COMPLETED":
            loan_status_completed_found = True
        if item.get("field_name") == "thinker.loanResult" and item.get("value") == "A02":
            loan_result_a02_found = True
    assert loan_status_completed_found, "Expected 'thinker.loanStatus' with 'COMPLETED' value not found in customer_data"
    assert loan_result_a02_found, "Expected 'thinker.loanResult' with 'A02' value not found in customer_data"

    status_field = case_detail.get("status")
    assert status_field == "completed", f"Expected status to be 'completed', but got '{status_field}'"
    print("Step 12: Completed Status verified.")

    print("Step 13: Booking Detail...")
    # Step 13: Get Booking Detail
    booking_detail = wf.get_booking_detail(session, session_id, case_id)
    assert "latest_status" in booking_detail
    assert booking_detail["latest_status"] == "COMPLETED"
    print("Step 13: Booking Detail retrieved.")
    
@pytest.mark.parametrize("scenario", GSB_LEAD_HAPPY_PATH_SCENARIOS, ids=lambda s: s["test_id"])
def test_gsb_lead_workflow(session, email, password, scenario):
    """
    Tests the entire end-to-end user workflow from login to booking.
    Each run is independent and driven by its scenario data.
    """
    print(f"--- Starting Test: {scenario["test_id"]} ---")

    print("Step 1: Logging in...")
    # Step 1: Login
    session_id = wf.login(session, email, password)
    assert session_id
    print("Step 1: Login successful.")

    print("Step 2: Applying for Product...")
    # Step 2: Apply for Product
    case_id = wf.apply_for_product(session, session_id, scenario["product_name"])
    assert case_id
    print(f"Step 2: Product applied. Case ID: {case_id}")

    print("Step 3: Answering Initial Questions...")
    # Step 3: Answer Initial & Campaign Select Questions
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["initial_questions"])
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["campaign_select_questions"])
    print("Step 3: Initial Questions answered.")
    
    print("Step 4: Submitting Case...")
    # Step 4: Submit Case
    wf.submit_case(session, session_id, case_id)
    print("Step 4: Case submitted.")
    
    print("Step 5: Verifying Case Details (Customer Decision Unknown, Loan Status PRE-APPROVED, etc.)...")
    # Step 5.1: Verify Customer Decision is Unknown
    time.sleep(5)
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries + 1):
        case_detail = wf.get_case_detail(session, session_id, case_id)
        if any(item.get("field_name") == "_loan.customerDecision" and item.get("value") == "__UNKNOWN__" for item in case_detail["traversal_path"]):
            break
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            pytest.fail("Expected '_loan.customerDecision' with '__UNKNOWN__' value not found after retries")

    # Step 5.2: Verify Loan Status is PRE-APPROVED
    time.sleep(5)
    customer_data_list = case_detail.get("customer_data", [])
    loan_status_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "PRE-APPROVED":
            loan_status_found = True
            break
    assert loan_status_found, "Expected 'thinker.loanStatus' with 'PRE-APPROVED' value not found in customer_data"

    # Step 5.3: Verify Verifying Field List is Not Empty
    verifying_field_list = case_detail.get("verifying_field_list", [])
    assert len(verifying_field_list) > 0, "verifying_field_list should not be empty"
    
    print("Step 6: Answering Secondary Questions...")
    # Step 6: Answer Secondary Questions
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["secondary_questions"])
    print("Step 6: Secondary Questions answered.")
    
    print("Step 7: Verifying Case Details (Loan Status APPROVED, etc.)...")
    # Step 7: Verify Loan Status is APPROVED
    time.sleep(10)
    case_detail = wf.get_case_detail(session, session_id, case_id)
    customer_data_list = case_detail.get("customer_data", [])
    loan_status_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "APPROVED":
            loan_status_found = True
            break
    assert loan_status_found, "Expected 'thinker.loanStatus' with 'APPROVED' value not found in customer_data"
    print("Step 7: Loan Status is APPROVED verified.")
    
    print("Step 8: Customer Decision...")
    # Step 8: Answer Customer Decision
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["customer_decision"])
    print("Step 8: Customer Decision answered.")
    
    print("Step 9: Completed Status...")
    # Step 9.1: Verify Loan Status is COMPLETED
    time.sleep(10)
    case_detail = wf.get_case_detail(session, session_id, case_id)
    customer_data_list = case_detail.get("customer_data", [])
    loan_status_found = False
    for item in customer_data_list:
        if item.get("field_name") == "thinker.loanStatus" and item.get("value") == "COMPLETED":
            loan_status_found = True
            break
    assert loan_status_found, "Expected 'thinker.loanStatus' with 'COMPLETED' value not found in customer_data"
    
    # Step 9.2: Verify Case Status is COMPLETED
    assert case_detail.get("status") == "completed", "Expected status to be 'completed' but got a different value"
    
    # Step 9.3: Verify Verifying Field List is Not Empty
    verifying_field_list = case_detail.get("verifying_field_list", [])
    assert len(verifying_field_list) > 0, "verifying_field_list should not be empty"
    
    # Step 9.4: Verify Remaining Verifying Field List is Empty
    remaining_verifying_field_list = case_detail.get("remaining_verifying_field_list", [])
    assert remaining_verifying_field_list == [], "remaining_verifying_field_list should be empty"
    print("Step 9: Completed Status verified.")
    
    print("Step 10: Booking Detail...")
    # Step 10: Get Booking Detail
    time.sleep(5)
    booking_detail = wf.get_booking_detail(session, session_id, case_id)
    assert "latest_status" in booking_detail
    assert booking_detail["latest_status"] == "COMPLETED"
    print("Step 10: Booking Detail retrieved.")