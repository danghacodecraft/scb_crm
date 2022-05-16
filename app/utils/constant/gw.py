GW_REPONSE_STATUS_SUCCESS = 1
GW_CASA_REPONSE_STATUS_SUCCESS = '00'

GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM = "/customer/v1.0/rest/selectCustomerRefDataMgmtCIFNum"
GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT = "/customer/v1.0/rest/retrieveCustomerRefDataMgmt"
GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA = "/currentaccount/v1.0/rest/retrieveCurrentAccountCASA"
GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF = '/currentaccount/v1.0/rest/selectCurrentAccountFromCIF'
GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT = '/report/v1.0/rest/selectReportHisCaSaFromAcc'
GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT = '/report/v1.0/rest/selectReportStatementCaSaFromAcc'
GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT = '/report/v1.0/rest/selectReportStatementTDFromAcc'
GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT = '/report/v1.0/rest/selectReportCaSaFromAcc'
GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF = '/depositaccount/v1.0/rest/selectDepositAccountFromCIF'
GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD = "/depositaccount/v1.0/rest/retrieveDepositAccountTD"
GW_ENDPOINT_URL_RETRIEVE_REPORT_TD_FROM_CIF = "/report/v1.0/rest/selectReportTDFromCif"
GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM = "/customer/v1.0/rest/selectAuthorizedRefDataMgmtAccNum"
GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM = "/customer/v1.0/rest/selectCoownerRefDataMgmtAccNum"
GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE = "/employee/v1.0/rest/selectEmployeeInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME = "/employee/v1.0/rest/selectEmployeeInfoFromUserName"
GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO = "/organization/v1.0/rest/selectOrgInfo"
GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_PARENT = "/organization/v1.0/rest/selectOrgInfoFromParent"
GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_CHILD = "/organization/v1.0/rest/selectOrgInfoFromChild"
GW_SELECT_CATEGORY = "/category/v1.0/rest/selectCategory"

GW_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
GW_DATE_FORMAT = '%Y-%m-%d'

GW_CURRENT_ACCOUNT_FROM_CIF = "CurrentAccountFromCIF"
GW_CURRENT_ACCOUNT_CASA = "CurrentAccountCASA"
GW_SELECT_CATEGORY_TYPE = "DS_NV_DIRECT_INDIRECT"

GW_DEPOSIT_ACCOUNT_FROM_CIF = "DepositAccountFromCIF"
GW_DEPOSIT_ACCOUNT_TD = "DepositAccountTD"

GW_CUSTOMER_REF_DATA_MGMT_CIF_NUM = "CustomerRefDataMgmtCifNum"
GW_CUST_FROM_CIF = "CustFromCIF"

GW_TRANSACTION_NAME_COLUMN_CHART = "TRAN_SUMARY"
GW_TRANSACTION_NAME_PIE_CHART = "3M_LATEST"
GW_TRANSACTION_NAME_STATEMENT = "TRAN_DETAILS"
GW_TRANSACTION_NAME_ALL = "ALL"
GW_TRANSACTION_NAME_PARENT = "PARENT"
GW_TRANSACTION_NAME_CHILD = "CHILD"
GW_TRANSACTION_NAME_COLUMN_CHART_TD = "6M_BAL"

GW_TRANSACTION_TYPE_SEND = "GUI"
GW_TRANSACTION_TYPE_WITHDRAW = "RUT"

GW_AUTHORIZED_REF_DATA_MGM_ACC_NUM = "AuthorizedRefDataMgmAccNum"

GW_CO_OWNER_REF_DATA_MGM_ACC_NUM = "CoownerRefDataMgmAccNum"

GW_EMPLOYEE_FROM_CODE = "EmployeeFromCode"
GW_EMPLOYEE_FROM_NAME = "EmployeeFromName"

GW_ORGANIZATION_INFO_FROM_PARENT_NAME = "selectOrgInfoFromParent_in"
GW_ORGANIZATION_INFO_FROM_CHILD_NAME = "selectOrgInfoFromChild_in"
GW_ORGANIZATION_INFO_NAME = "selectOrgInfo_in"
GW_ORGANIZATION_FROM_CHILD_ID = "4"
GW_ORGANIZATION_ID = ""

GW_LOC_CHECK_CIF_EXIST = "check_exist_cif"

GW_GENDER_MALE = 'M'
GW_GENDER_FEMALE = 'F'

GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP = "GUARDIAN_OR_CUSTOMER_RELATIONSHIP"
GW_REQUEST_PARAMETER_DEBIT_CARD = "DEBIT_CARD"
GW_REQUEST_PARAMETER_DEFAULT = "DEFAULT"

TRANSACTION_FORMS = {
    "D": "Trực tiếp",
    "I": "Gián tiếp"
}

GW_REQUEST_PARAMETER = {
    GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP: "Người giám hộ/Mối quan hệ khách hàng",
    GW_REQUEST_PARAMETER_DEBIT_CARD: "Thẻ ghi nợ"
}
