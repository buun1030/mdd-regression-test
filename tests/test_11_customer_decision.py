from helpers import answered_questions

def test_customer_decision(session_id, case_id):
    """
    Tests that the customer_decision  is working correctly.
    """
    answer_payload = [
        {
            "field_name": "_loan.customerDecision",
            "field_value": "ACCEPT",
            "source": "customer"
        },
        {
            "field_name": "loanAmount",
            "field_value": "50000",
            "source": "customer"
        },
        {
            "field_name": "_loan.repaymentType",
            "field_value": "TERM",
            "source": "customer"
        },
        {
            "field_name": "scheduleSettings.repaymentInstallments",
            "field_value": "12",
            "source": "customer"
        }
    ]
    
    answered_questions(session_id, case_id, answer_payload)
