import pytest
import requests
import configparser
import os
import time
import json
import uuid

# Get the absolute path of the project's root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.ini file
config_path = os.path.join(ROOT_DIR, '..', 'config.ini')

# Read the config file
config = configparser.ConfigParser()
config.read(config_path)

# Get the base URL, email, and password from the config file
BASE_URL = config['settings']['base_url']
EMAIL = config['settings']['email']
PASSWORD = config['settings']['password']
THINKER_WORKSPACE = config['settings']['thinker_workspace']

@pytest.fixture(scope="session")
def session_id():
    """
    Logs in to the API and returns the session ID.
    This fixture has a "session" scope, so it will only run once per test session.
    """
    login_url = f"{BASE_URL}/authentication/api/v1/login"
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(login_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    response_data = response.json()
    return response_data["data"]["session_id"]

@pytest.fixture(scope="session")
def case_id(session_id):
    """
    Applies for a product and returns the case ID.
    This fixture has a "session" scope, so it will only run once per test session.
    """
    apply_url = f"{BASE_URL}/question-taskpool/api/v1/apply-for-product"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "product_name": config['settings']['product_name']
    }
    response = requests.post(apply_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    response_data = response.json()
    generated_case_id = response_data["data"]["case_id"]
    print(f"Generated Case ID: {generated_case_id}")
    return generated_case_id

@pytest.fixture(scope="session")
def answered_questions(session_id, case_id):
    """
    Answers questions for the case.
    """
    answer_url = "https://moneydd-dev.thinkerfint.com/question-taskpool/api/v1/answer-question"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }

    # Correctly escaped JSON string for base64 content
    valid_base64_content = "[\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEAAQMAAABmvDolAAAABlBMVEX///8AAABVwtN+AAABmklEQVR4nOyYMdKrMAyE10ORkiNwFB8NH81HyREoKTzeN5LsxDC89p+gQVXwfCmQxGplPPHEEz8bMyV2RAaS7/HIFSBn0z6TVR/WsLcjZ0BkVSCU17YI1458AqnixZYHtwBi0q6O/8vD7YHewnViL/dF298dMEGa86pdnaXcVyJ2c6BzebVXXysu4+ZAl2LNg3S1fcIstwKwkMCLGVJNACpB6du0PgAZlXUimYK8uijRtjAdEuUBYLYfWm59kDx8W9cHIK+uA4WD0spYcQaIuBbMTJi4SToo2RiU1gcA/VLF005q3asq1aBRLgAdkgW93NnMXqpHe3B/4B2T2oHEYp62PcAbwJaOoi0OLXfwBoj62oYyqXXnLrM2DG7QBSDlLubyhokDwBlgu4mezcytq4+L2M8Dn6I2vWXYRY9CgSvgc6OV2kCxy4Hxry6AtiJHXSrFGJzz4ATodyBayJE2XQ4S5AiwdXnJqGdv7woQjZJ9c+WFPfAAtOurVTC1BxtOa7UHoN9ooXlaW1rGhdQD8MQTT/x5/AsAAP//oCbiyX1d9MUAAAAASUVORK5CYII=\"]"

    answers_payload = [
        {
            "field_name": "emailAddress",
            "field_value": "test-email@gmail.com",
            "source": "customer"
        },
        {
            "field_name": "mobilePhone",
            "field_value": "0899999988",
            "source": "customer"
        },
        {
            "field_name": "_loan.loanApplicationNumber",
            "field_value": "TESTLOANTYPE111114",
            "source": "customer"
        },
        {
            "field_name": "_loan.requestDate",
            "field_value": "1730104992",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.nationalIdNumber",
            "field_value": "1200100436663",
            "source": "customer"
        },
        {
            "field_name": "_occupation.businessAddressPropertyRight",
            "field_value": "2",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.mailingAddressIndex",
            "field_value": "1",
            "source": "customer"
        },
        {
            "field_name": "_occupation.businessType",
            "field_value": "0",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.titleName",
            "field_value": "2101",
            "source": "customer"
        },
        {
            "field_name": "firstName",
            "field_value": "สมมุติแก้ไข",
            "source": "customer"
        },
        {
            "field_name": "middleName",
            "field_value": "",
            "source": "customer"
        },
        {
            "field_name": "lastName",
            "field_value": "ทดสอบแก้ไข",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.enFirstName",
            "field_value": "Testmambu",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.enLastName",
            "field_value": "Demoeditmambu",
            "source": "customer"
        },
        {
            "field_name": "birthDate",
            "field_value": "962557200",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.idExpireDate",
            "field_value": "0",
            "source": "customer"
        },
        {
            "field_name": "_addresses.1.line1",
            "field_value": "220/30",
            "source": "customer"
        },
        {
            "field_name": "_addresses.1.line2",
            "field_value": "หมู่ที่ 9",
            "source": "customer"
        },
        {
            "field_name": "_addresses.1.city",
            "field_value": "20",
            "source": "customer"
        },
        {
            "field_name": "_addresses.1.district",
            "field_value": "2011",
            "source": "customer"
        },
        {
            "field_name": "_addresses.1.subDistrict",
            "field_value": "201101",
            "source": "customer"
        },
        {
            "field_name": "_addresses.1.postcode",
            "field_value": "12346",
            "source": "customer"
        },
        {
            "field_name": "_loan.typePreSelect",
            "field_value": "P_LOAN",
            "source": "customer"
        },
        {
            "field_name": "_occupation.employType",
            "field_value": "EMPLOYEE",
            "source": "customer"
        },
        {
            "field_name": "_occupation.type",
            "field_value": "01",
            "source": "customer"
        },
        {
            "field_name": "_occupation.previousType",
            "field_value": "01",
            "source": "customer"
        },
        {
            "field_name": "_occupation.subType",
            "field_value": "01",
            "source": "customer"
        },
        {
            "field_name": "_occupation.previousSubType",
            "field_value": "01",
            "source": "customer"
        },
        {
            "field_name": "_occupation.typeOther",
            "field_value": "0891548123",
            "source": "customer"
        },
        {
            "field_name": "_loan.repaymentType",
            "field_value": "TERM",
            "source": "customer"
        },
        {
            "field_name": "_loan.loanRequest",
            "field_value": "100000",
            "source": "customer"
        },
        {
            "field_name": "scheduleSettings.repaymentInstallments",
            "field_value": "24",
            "source": "customer"
        },
        {
            "field_name": "scheduleSettings.fixedDaysOfMonth",
            "field_value": "2",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.educationLevel",
            "field_value": "6",
            "source": "customer"
        },
        {
            "field_name": "gender",
            "field_value": "F",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.maritalStatus",
            "field_value": "M",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.childWorkedAmount",
            "field_value": "1",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.childNotWorkedAmount",
            "field_value": "1",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.childAmount",
            "field_value": "2",
            "source": "customer"
        },
        {
            "field_name": "_occupation.incomeAmount",
            "field_value": "700000",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.residencePeriodYear",
            "field_value": "5",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.residencePeriodMonth",
            "field_value": "2",
            "source": "customer"
        },
        {
            "field_name": "_occupation.companyName",
            "field_value": "บริษัท เงินดีดี จำกัด (มหาชน)",
            "source": "customer"
        },
        {
            "field_name": "_occupation.previousCompanyName",
            "field_value": "บริษัท เงินมั่งมี จำกัด (มหาชน)",
            "source": "customer"
        },
        {
            "field_name": "_credit.expenseAmount",
            "field_value": "5000",
            "source": "customer"
        },
        {
            "field_name": "_occupation.periodYear",
            "field_value": "0",
            "source": "customer"
        },
        {
            "field_name": "_occupation.totalPeriodYear",
            "field_value": "1",
            "source": "customer"
        },
        {
            "field_name": "_occupation.totalPeriodMonth",
            "field_value": "10",
            "source": "customer"
        },
        {
            "field_name": "_occupation.previousPeriodYear",
            "field_value": "1",
            "source": "customer"
        },
        {
            "field_name": "_occupation.periodMonth",
            "field_value": "5",
            "source": "customer"
        },
        {
            "field_name": "_occupation.previousPeriodMonth",
            "field_value": "2",
            "source": "customer"
        },
        {
            "field_name": "_occupation.shareholdingPorpotion",
            "field_value": "0",
            "source": "customer"
        },
        {
            "field_name": "_addresses.3.line1",
            "field_value": "199 รัชดา 17",
            "source": "customer"
        },
        {
            "field_name": "_addresses.3.line2",
            "field_value": "ถนนรัชดา",
            "source": "customer"
        },
        {
            "field_name": "_addresses.3.city",
            "field_value": "10",
            "source": "customer"
        },
        {
            "field_name": "_addresses.3.district",
            "field_value": "1001",
            "source": "customer"
        },
        {
            "field_name": "_addresses.3.subDistrict",
            "field_value": "100110",
            "source": "customer"
        },
        {
            "field_name": "_addresses.3.postcode",
            "field_value": "10110",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.residenceType",
            "field_value": "01",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.residenceStatus",
            "field_value": "01",
            "source": "customer"
        },
        {
            "field_name": "_addresses.2.city",
            "field_value": "10",
            "source": "customer"
        },
        {
            "field_name": "_refPersons.1.relationship",
            "field_value": "01",
            "source": "customer"
        },
        {
            "field_name": "_addresses.2.line1",
            "field_value": "asasas",
            "source": "customer"
        },
        {
            "field_name": "_addresses.2.line2",
            "field_value": "asasas",
            "source": "customer"
        },
        {
            "field_name": "_addresses.2.district",
            "field_value": "1001",
            "source": "customer"
        },
        {
            "field_name": "_addresses.2.subDistrict",
            "field_value": "100103",
            "source": "customer"
        },
        {
            "field_name": "_addresses.2.postcode",
            "field_value": "10110",
            "source": "customer"
        },
        {
            "field_name": "_bankAccount.1.accountNumber",
            "field_value": "1231456454",
            "source": "customer"
        },
        {
            "field_name": "_bankAccount.1.accountName",
            "field_value": "ศศิภัคณ์",
            "source": "customer"
        },
        {
            "field_name": "_bankAccount.1.bankName",
            "field_value": "GSB",
            "source": "customer"
        },
        {
            "field_name": "_bankAccount.1.bankId",
            "field_value": "30",
            "source": "customer"
        },
        {
            "field_name": "_bankAccount.1.isValid",
            "field_value": "true",
            "source": "customer"
        },
        {
            "field_name": "_bankAccount.1.isDefault",
            "field_value": "true",
            "source": "customer"
        },
        {
            "field_name": "_documents.16.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.16.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.16.password",
            "field_value": "[\"12334\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.16.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.1.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.1.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.1.password",
            "field_value": "[\"-\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.1.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.2.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.2.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.2.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.2.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.3.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.3.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.3.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.3.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.4.name",
            "field_value": "[\"AcctSt_Jul23.pdf\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.4.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.4.password",
            "field_value": "[\"14021995\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.4.docType",
            "field_value": "[\"file/pdf\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.5.name",
            "field_value": "[\"AcctSt_Aug23.pdf\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.5.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.5.password",
            "field_value": "[\"14021995\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.5.docType",
            "field_value": "[\"file/pdf\"]",
            "source": "customer"
        },
        
        {
            "field_name": "_documents.8.name",
            "field_value": "[\"AcctSt_Nov23.pdf\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.8.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.8.password",
            "field_value": "[\"14021995\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.8.docType",
            "field_value": "[\"file/pdf\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.9.name",
            "field_value": "[\"AcctSt_Dec23.pdf\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.9.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.9.password",
            "field_value": "[\"14021995\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.9.docType",
            "field_value": "[\"file/pdf\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.10.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.10.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.10.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.10.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.11.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.11.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.11.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.11.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.12.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.12.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.12.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.12.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.13.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.13.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.13.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.13.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.14.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.14.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.14.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.14.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.15.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        
        {
            "field_name": "_documents.17.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.17.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.17.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.17.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.18.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.18.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.18.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.18.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.19.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.19.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.19.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.19.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.20.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.20.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.20.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.20.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.21.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.21.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.21.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.21.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.22.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.22.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.22.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.22.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.23.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.23.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.23.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.23.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.24.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.24.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.24.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.24.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.25.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.25.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.25.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.25.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.26.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.26.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.26.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.26.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.27.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.27.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.27.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.27.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.28.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.28.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.28.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.28.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.29.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.29.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.29.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.29.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.30.name",
            "field_value": "[\"test.png\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.30.content",
            "field_value": valid_base64_content,
            "source": "customer"
        },
        {
            "field_name": "_documents.30.password",
            "field_value": "[\"1234\"]",
            "source": "customer"
        },
        {
            "field_name": "_documents.30.docType",
            "field_value": "[\"image/png\"]",
            "source": "customer"
        },
        {
            "field_name": "_credit.isNcbTrustSource",
            "field_value": "TRUST",
            "source": "customer"
        },
        {
            "field_name": "_credit.isNcbConsentAccept",
            "field_value": "true",
            "source": "customer"
        },
        {
            "field_name": "_customerInfo.authenticationType",
            "field_value": "NDID",
            "source": "customer"
        }
    ]

    payload = {
        "case_id": case_id,
        "answers": answers_payload
    }

    response = requests.post(answer_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0

@pytest.fixture(scope="session")
def submitted_case_id(session_id, case_id, answered_questions):
    """
    Submits the case and returns the case_id.
    Depends on answered_questions to ensure questions are answered before submission.
    """
    submit_url = f"{BASE_URL}/case-datasources/api/v1/cases/submit"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    response = requests.post(submit_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes
    response_data = response.json()
    assert "case_id" in response_data
    assert "case_submission_id" in response_data
    assert "message" in response_data
    assert response_data["message"] == "processing"
    return case_id

@pytest.fixture(scope="session")
def completed_batch_process(session_id, submitted_case_id):
    """
    Performs the batch-process-complete API call with retry logic.
    This fixture ensures the batch process is completed before dependent fixtures/tests run.
    """
    batch_process_url = f"{BASE_URL}/case-datasources/api/v1/callback/batch-process-complete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": submitted_case_id
    }

    # Initial delay after submit case
    time.sleep(5)

    max_retries = 3
    retry_delay = 3  # seconds
    response = None

    for attempt in range(max_retries + 1):
        response = requests.post(batch_process_url, json=payload, headers=headers)
        if response.status_code == 200:
            break  # Success, exit loop
        elif response.status_code == 500 and attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Received 500. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            # Other status code or last retry failed with 500
            break

    # Final assertions after all attempts
    assert response.status_code == 200, \
        f"Expected 200, but got {response.status_code}. Response: {response.text}"
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == "0"

@pytest.fixture(scope="session")
def case_detail_data(session_id, case_id, completed_batch_process):
    """
    Fetches case details and returns the 'data' portion of the response.
    Includes retry logic for eventual consistency.
    Depends on completed_batch_process to ensure batch process is complete.
    """
    get_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-case-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    # Delay after batch process complete, as requested
    time.sleep(10)

    max_retries = 3
    retry_delay = 5  # seconds
    found_condition = False
    response_data = None

    for attempt in range(max_retries + 1):
        response = requests.post(get_detail_url, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes (e.g., 4xx or 5xx)
        response_data = response.json()

        if "data" in response_data and \
           "traversal_path" in response_data["data"] and \
           any(item.get("field_name") == "thinker.caDecision" and item.get("value") == "__UNKNOWN__" for item in response_data["data"]["traversal_path"]):
            found_condition = True
            break  # Condition met, exit retry loop
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            # Last attempt failed, print the traversal path for debugging
            print(f"Final attempt failed. Traversal Path: {response_data.get("data", {}).get("traversal_path")}")
            pytest.fail("Expected 'thinker.caDecision' with '__UNKNOWN__' value not found in traversal_path after retries")

    return response_data["data"]

@pytest.fixture(scope="session")
def claimed_tasks_data(session_id, case_id):
    """
    Claims the case and returns the 'data' portion of the response.
    """
    claim_url = f"{BASE_URL}/question-taskpool/api/v1/claim-case"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    response = requests.post(claim_url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0
    assert "data" in response_data
    assert isinstance(response_data["data"], list)
    return response_data["data"]

@pytest.fixture(scope="session")
def task_ids(claimed_tasks_data):
    """
    Extracts task_id values from the claimed_tasks_data.
    """
    return [task.get("id") for task in claimed_tasks_data if task.get("id")]

@pytest.fixture(scope="session")
def task_details(session_id, task_ids):
    """
    Fetches details for each task_id and returns a dictionary of task_id to its detail data.
    """
    task_detail_map = {}
    for task_id in task_ids:
        get_task_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-task-detail"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_id}"
        }
        payload = {
            "task_id": task_id,
            "all_task_mode": False
        }
        response = requests.post(get_task_detail_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        assert "code" in response_data
        assert response_data["code"] == 0
        assert "data" in response_data
        task_detail_map[task_id] = response_data["data"]
    return task_detail_map

@pytest.fixture(scope="session")
def verified_tasks(session_id, task_details):
    """
    Verifies task data for each task.
    """
    for task_id, detail_data in task_details.items():
        verify_task_url = f"{BASE_URL}/question-taskpool/api/v1/verify-task-data"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_id}"
        }
        # Extract field_name and current_value from verifying_fields and required_fields
        verifying_fields = []
        if "verifying_fields" in detail_data:
            for field_i in detail_data["verifying_fields"]:
                field = field_i.get("field")
                verifying_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})

        required_fields = []
        if "required_fields" in detail_data:
            for field_i in detail_data["required_fields"]:
                field = field_i.get("field")
                required_fields.append({"field_name": field.get("field_name"), "field_value": field.get("current_value")})

        payload = {
            "task_id": task_id,
            "verifying_fields": verifying_fields,
            "required_fields": required_fields
        }
        response = requests.post(verify_task_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        assert "code" in response_data
        assert response_data["code"] == 0

@pytest.fixture(scope="session")
def first_additional_answer_success(session_id, case_id, verified_tasks):
    """
    Sends the first set of additional answers (thinker.caDecision).
    """
    answer_url = "https://moneydd-dev.thinkerfint.com/question-taskpool/api/v1/answer-question"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "answers": [
            {
                "field_name": "thinker.caDecision",
                "field_value": "A02",
                "source": "customer"
            }
        ],
        "case_id": case_id,
        "module_name": "",
        "is_question_mode": False,
        "save_valid_answers": False,
        "not_skip_to_latest_question": False
    }
    response = requests.post(answer_url, json=payload, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0

@pytest.fixture(scope="session")
def approved_case_detail_data(session_id, case_id, first_additional_answer_success):
    """
    Fetches case details after the first additional answer and checks for APPROVED status.
    """
    get_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-case-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    # Delay to allow processing
    time.sleep(5) # Reduced delay as it's after a specific answer

    max_retries = 3
    retry_delay = 3  # seconds
    found_condition = False
    response_data = None

    for attempt in range(max_retries + 1):
        response = requests.post(get_detail_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if "data" in response_data and \
           "customer_data" in response_data["data"] and \
           any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == "APPROVED" for item in response_data["data"]["customer_data"]) and \
           response_data["data"].get("remaining_verifying_field_list") == []:
            found_condition = True
            break
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Final attempt failed. Customer Data: {response_data.get("data", {}).get("customer_data")}")
            print(f"Remaining Verifying Field List: {response_data.get("data", {}).get("remaining_verifying_field_list")}")
            pytest.fail("Expected 'thinker.loanStatus' to be APPROVED and remaining_verifying_field_list to be empty after retries")

    return response_data["data"]

@pytest.fixture(scope="session")
def second_additional_answer_success(session_id, case_id, approved_case_detail_data):
    """
    Sends the second set of additional answers (loan details).
    """
    answer_url = "https://moneydd-dev.thinkerfint.com/question-taskpool/api/v1/answer-question"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "answers": [
            {
                "field_name": "_loan.customerDecision",
                "field_value": "ACCEPT",
                "source": "customer"
            },
            {
                "field_name": "loanAmount",
                "field_value": "20000",
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
        ],
        "case_id": case_id,
        "module_name": "",
        "is_question_mode": False,
        "save_valid_answers": False,
        "not_skip_to_latest_question": False
    }
    response = requests.post(answer_url, json=payload, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == 0

@pytest.fixture(scope="session")
def completed_case_detail_data(session_id, case_id, second_additional_answer_success):
    """
    Fetches case details after the second additional answer and checks for COMPLETED status.
    """
    get_detail_url = f"{BASE_URL}/question-taskpool/api/v1/get-case-detail"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}"
    }
    payload = {
        "case_id": case_id
    }

    # Delay to allow processing
    time.sleep(10)

    max_retries = 3
    retry_delay = 5  # seconds
    found_condition = False
    response_data = None

    for attempt in range(max_retries + 1):
        response = requests.post(get_detail_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if "data" in response_data and \
           "customer_data" in response_data["data"] and \
           any(item.get("field_name") == "thinker.loanStatus" and item.get("value") == "COMPLETED" for item in response_data["data"]["customer_data"]) and \
           any(item.get("field_name") == "thinker.loanResult" and item.get("value") == "A02" for item in response_data["data"]["customer_data"]) and \
           response_data["data"].get("status") == "completed":
            found_condition = True
            break
        elif attempt < max_retries:
            print(f"Attempt {attempt + 1}/{max_retries + 1}: Condition not met. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Final attempt failed. Customer Data: {response_data.get("data", {}).get("customer_data")}")
            print(f"Status: {response_data.get("data", {}).get("status")}")
            pytest.fail("Expected 'thinker.loanStatus' to be COMPLETED, 'thinker.loanResult' to be A02, and status to be completed after retries")

    return response_data["data"]
