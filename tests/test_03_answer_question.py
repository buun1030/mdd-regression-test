from conftest import answered_questions

def test_answer_question(session_id, case_id):
    """
    Tests that the answered_questions is working correctly.
    """
     # Correctly escaped JSON string for base64 content
    valid_base64_content = "[\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEAAQMAAABmvDolAAAABlBMVEX///8AAABVwtN+AAABmklEQVR4nOyYMdKrMAyE10ORkiNwFB8NH81HyREoKTzeN5LsxDC89p+gQVXwfCmQxGplPPHEEz8bMyV2RAaS7/HIFSBn0z6TVR/WsLcjZ0BkVSCU17YI1458AqnixZYHtwBi0q6O/8vD7YHewnViL/dF298dMEGa86pdnaXcVyJ2c6BzebVXXysu4+ZAl2LNg3S1fcIstwKwkMCLGVJNACpB6du0PgAZlXUimYK8uijRtjAdEuUBYLYfWm59kDx8W9cHIK+uA4WD0spYcQaIuBbMTJi4SToo2RiU1gcA/VLF005q3asq1aBRLgAdkgW93NnMXqpHe3B/4B2T2oHEYp62PcAbwJaOoi0OLXfwBoj62oYyqXXnLrM2DG7QBSDlLubyhokDwBlgu4mezcytq4+L2M8Dn6I2vWXYRY9CgSvgc6OV2kCxy4Hxry6AtiJHXSrFGJzz4ATodyBayJE2XQ4S5AiwdXnJqGdv7woQjZJ9c+WFPfAAtOurVTC1BxtOa7UHoN9ooXlaW1rGhdQD8MQTT/x5/AsAAP//oCbiyX1d9MUAAAAASUVORK5CYII=\"]"

    answer_payload = [
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

    answered_questions(session_id, case_id, answer_payload)
    
