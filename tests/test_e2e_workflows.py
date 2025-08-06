import pytest
import time
from .scenarios import HAPPY_PATH_SCENARIOS
from . import workflow_helpers as wf

@pytest.mark.parametrize("scenario", HAPPY_PATH_SCENARIOS, ids=lambda s: s["test_id"])
def test_full_workflow(session, email, password, scenario):
    """
    Tests the entire end-to-end user workflow from login to booking.
    Each run is independent and driven by its scenario data.
    """
    # Step 1: Login
    session_id = wf.login(session, email, password)
    assert session_id

    # Step 2: Apply for Product
    case_id = wf.apply_for_product(session, session_id, scenario["product_name"])
    assert case_id

    # Step 3: Answer Initial Questions
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["initial_questions"])

    # Step 4: Submit Case
    wf.submit_case(session, session_id, case_id)
    time.sleep(5) # Add a delay after submitting the case

    # Step 5: Complete Batch Process
    wf.complete_batch_process(session, session_id, case_id)

    # Step 6.1: Verify CA Decision is Unknown
    case_detail = wf.get_case_detail(session, session_id, case_id)
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
    
    # Step 7.1: CA Claim Case
    claimed_tasks_data = wf.claim_case(session, session_id, case_id)
    assert len(claimed_tasks_data) > 0, "claimed_tasks_data should not be empty"
    
    expected_task_substrings = [
        "customer.information",
        "occupation.informationPresent",
        "bank.1.information",
        "occupation.informationPrevious",
        "informationNewCustomer",
        "document.other",
        "ncb.direct",
        "document.main",
        "informationInterest",
        "informationRevolving",
        "informationTerm",
        "summary.ca"
    ]

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
        
    # Step 7.2: Verify available escalation roles in CA tasks
    task_details = wf.get_task_details(session, session_id, case_id)
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

    # Step 7.3: CA Claim and Escalate
    for task_id, detail_data in task_details.items():
        if "summary" in detail_data.get("verification_method_name", ""):
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
            if "verification_method_name" in detail_data and "summary" in detail_data["verification_method_name"]:
                wf.edit_task_data(session, session_id, payload)

    # Step 8: SCA Claim and Escalate
    wf.claim_case(session, session_id, case_id)
    task_details = wf.get_task_details(session, session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "summary" in detail_data.get("verification_method_name", ""):
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

    # Step 9: MD Claim and Decide
    wf.release_case(session, session_id, case_id)
    wf.claim_case(session, session_id, case_id)
    task_details = wf.get_task_details(session, session_id, case_id)
    for task_id, detail_data in task_details.items():
        if "summary" in detail_data.get("verification_method_name", ""):
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

    # Step 10: Verify Approved Status
    time.sleep(15) # Increased delay
    max_retries = 10 # Increased retries
    retry_delay = 10 # Increased retry delay
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

    # Step 12: Verify Completed Status
    time.sleep(15) # Increased delay
    max_retries = 10 # Increased retries
    retry_delay = 10 # Increased retry delay
    for attempt in range(max_retries + 1):
        case_detail = wf.get_case_detail(session, session_id, case_id)
        print(f"Attempt {attempt + 1}: Case Detail for Completed Status: {case_detail}") # Added logging
        loan_status_completed_found = any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == scenario["expected_final_status"] for item in case_detail["customer_data"])
        loan_result_a02_found = any(item.get("field_name") == "thinker.loanResult" and item.get("value") == scenario["expected_loan_result"] for item in case_detail["customer_data"])
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

    # Step 11: Customer Decision
    wf.answer_questions(session, session_id, case_id, scenario["answers"]["customer_decision"])

    # Step 12: Verify Completed Status
    time.sleep(10)
    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries + 1):
        case_detail = wf.get_case_detail(session, session_id, case_id)
        if any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == scenario["expected_final_status"] for item in case_detail["customer_data"]) and \
           any(item.get("field_name") == "thinker.loanResult" and item.get("value") == scenario["expected_loan_result"] for item in case_detail["customer_data"]) and \
           case_detail.get("status") == "completed":
            break
        elif attempt < max_retries:
            time.sleep(retry_delay)
        else:
            pytest.fail("Expected final status conditions not met after retries")

    # Step 13: Get Booking Report Detail
    booking_report = wf.get_booking_report_detail(session, session_id, case_id)
    assert booking_report
    assert "booking_report_url" in booking_report
