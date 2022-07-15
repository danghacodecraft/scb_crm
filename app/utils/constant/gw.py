######################################################################################################
#                                           Endpoints                                                #
######################################################################################################
GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM = "/customer/v1.0/rest/selectCustomerRefDataMgmtCIFNum"
GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT = "/customer/v1.0/rest/retrieveCustomerRefDataMgmt"
GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA = "/currentaccount/v1.0/rest/retrieveCurrentAccountCASA"
GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF = '/currentaccount/v1.0/rest/selectCurrentAccountFromCIF'
GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT = '/report/v1.0/rest/selectReportHisCaSaFromAcc'
GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT = '/report/v1.0/rest/selectReportStatementCaSaFromAcc'
GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT = '/report/v1.0/rest/selectReportStatementTDFromAcc'
GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT = '/report/v1.0/rest/selectReportCaSaFromAcc'
GW_ENDPOINT_URL_RETRIEVE_OPEN_CASA_ACCOUNT = '/currentaccount/v1.0/rest/openCASA'
GW_ENDPOINT_URL_RETRIEVE_CLOSE_CASA_ACCOUNT = '/currentaccount/v1.0/rest/closeCASA'
GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF = '/depositaccount/v1.0/rest/selectDepositAccountFromCIF'
GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD = "/depositaccount/v1.0/rest/retrieveDepositAccountTD"
GW_ENDPOINT_URL_DEPOSIT_OPEN_ACCOUNT_TD = "/depositaccount/v1.0/rest/openTD"
GW_ENDPOINT_URL_RETRIEVE_REPORT_TD_FROM_CIF = "/report/v1.0/rest/selectReportTDFromCif"
GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM = "/customer/v1.0/rest/selectAuthorizedRefDataMgmtAccNum"
GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM = "/customer/v1.0/rest/selectCoownerRefDataMgmtAccNum"
GW_ENDPOINT_URL_SELECT_EMPLOYEE_INFO_FROM_CODE = "/employee/v1.0/rest/selectEmployeeInfoFromCode"
GW_ENDPOINT_URL_CHECK_EXITS_ACCOUNT_CASA = "/currentaccount/v1.0/rest/retrieveCurrentAccountCASA"
GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME = "/employee/v1.0/rest/selectEmployeeInfoFromUserName"
GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_LIST_FROM_ORG_ID = "/employee/v1.0/rest/selectEmployeeListFromOrgId"
GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE = "/employee/v1.0/rest/retrieveEmployeeInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_WORKING_PROCESS_INFO_FROM_CODE = "/employee/v1.0/rest/selectWorkingProcessInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_REWARD_INFO_FROM_CODE = "/employee/v1.0/rest/selectRewardInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_DISCIPLINE_INFO_FROM_CODE = "/employee/v1.0/rest/selectDisciplineInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_TOPIC_INFO_FROM_CODE = "/employee/v1.0/rest/selectTopicInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_KPIS_INFO_FROM_CODE = "/employee/v1.0/rest/selectKpisInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_STAFF_OTHER_INFO_FROM_CODE = "/employee/v1.0/rest/selectStaffOtherInfoFromCode"
GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO = "/organization/v1.0/rest/selectOrgInfo"
GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_PARENT = "/organization/v1.0/rest/selectOrgInfoFromParent"
GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_CHILD = "/organization/v1.0/rest/selectOrgInfoFromChild"
GW_ENDPOINT_URL_SELECT_CATEGORY = "/category/v1.0/rest/selectCategory"
GW_ENDPOINT_URL_HISTORY_CHANGE_FIELD = "/history/v1.0/rest/historyChangeFieldAccount"
GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF = '/customer/v1.0/rest/openCIFAuthorise'
GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_ID_FCC = '/users/v1.0/rest/selectUserInfoByUserID'
GW_ENDPOINT_URL_RETRIEVE_TELE_TRANSFER_INFO = '/payment/v1.0/rest/teleTransfer'
GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_ACCOUNT_NUMBER = '/payment/v1.0/rest/retrieveBenNameByAccNum'
GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_CARD_NUMBER = '/payment/v1.0/rest/retrieveBenNameByCardNum'
GW_ENDPOINT_URL_RETRIEVE_CHANGE_STATUS_ACCOUNT_NUMBER = '/currentaccount/v1.0/rest/accountChangeStatus'

# ---------------------------------------------- PAYMENT ---------------------------------------------- #

GW_ENDPOINT_URL_PAYMENT_AMOUNT_BLOCK = "/payment/v1.0/rest/amountBlock"
GW_ENDPOINT_URL_PAYMENT_AMOUNT_UNBLOCK = "/payment/v1.0/rest/amountUnBlock"
GW_ENDPOINT_URL_PAY_IN_CASH = "/payment/v1.0/rest/payInCash"
GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_ACCOUNT_NUMBER = "/payment/v1.0/rest/payInCash247byAccNum"
GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_CARD_NUMBER = "/payment/v1.0/rest/payInCash247byCardNum"
GW_ENDPOINT_URL_REDEEM_ACCOUNT = "/payment/v1.0/rest/redeemAccount"
GW_ENDPOINT_URL_INTERNAL_TRANSFER = "/payment/v1.0/rest/internalTransfer"
GW_ENDPOINT_URL_TT_LIQUIDATION = "/payment/v1.0/rest/ttLiquidation"
GW_ENDPOINT_URL_TELE_TRANSFER = "/payment/v1.0/rest/teleTransfer"
GW_ENDPOINT_URL_INTERBANK_TRANSFER = "/payment/v1.0/rest/interbankTransfer"
GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_ACCOUNT_NUMBER = "/payment/v1.0/rest/interbankTransfer247ByAccNum"
GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_CARD_NUMBER = "/payment/v1.0/rest/interbankTransfer247ByCardNum"
GW_ENDPOINT_URL_WITHDRAW = "/payment/v1.0/rest/cashWithdrawals"
# ---------------------------------------------- USER ---------------------------------------------- #
GW_ENDPOINT_URL_SELECT_USER_INFO = "/users/v1.0/rest/selectUserInfoByUserID"

# ---------------------------------------------- SERIAL ---------------------------------------------- #
GW_ENDPOINT_URL_SELECT_SERIAL_NUMBER = "/serial/v1.0/rest/retrieveSerialNumber"

# ---------------------------------------------- BRANCH LOCATION ---------------------------------------------- #
GW_ENDPOINT_URL_SELECT_BRANCH_BY_REGION_ID = "/branchlocation/v1.0/rest/selectBranchByRegionID"
GW_ENDPOINT_URL_SELECT_BRANCH_BY_BRANCH_ID = "/branchlocation/v1.0/rest/selectBranchByBranchID"

# ---------------------------------------------- STATISTIC ---------------------------------------------- #
GW_ENDPOINT_URL_SELECT_STATISTIC_BANKING_BY_PERIOD = "/statistics/v1.0/rest/selectStatisticBankingByPeriod"

######################################################################################################
#                                           Constant                                                #
######################################################################################################

GW_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
GW_DATE_FORMAT = '%Y-%m-%d'
GW_CORE_DATE_FORMAT = '%m/%d/%Y'

GW_RESPONSE_STATUS_SUCCESS = '00'
GW_FUNCTION_OPEN_CASA = "openCASA_in"

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

GW_RETRIEVE_CASA_ACCOUNT_DETAIL = "CurrentAccountCASA"
GW_EMPLOYEE_FROM_CODE = "EmployeeFromCode"
GW_EMPLOYEE_FROM_NAME = "EmployeeFromName"
GW_EMPLOYEES = "Employees"

GW_ORGANIZATION_INFO_FROM_PARENT_NAME = "selectOrgInfoFromParent_in"
GW_ORGANIZATION_INFO_FROM_CHILD_NAME = "selectOrgInfoFromChild_in"
GW_ORGANIZATION_INFO_NAME = "selectOrgInfo_in"
GW_ORGANIZATION_FROM_CHILD_ID = "4"
GW_ORGANIZATION_ID = ""

GW_LOC_CHECK_CIF_EXIST = "check_exist_cif"

GW_GENDER_MALE = 'M'
GW_GENDER_FEMALE = 'F'

GW_PASSPORT_TYPE_ID = "P"
GW_CMND_TYPE_ID = "C"

GW_AUTO = "N"
GW_SELECT = "Y"

GW_HISTORY_ACCOUNT_NUM = "00576400195"
GW_HISTORY_CHANGE_FIELD_ACCOUNT = "TD"

GW_SELF_SELECTED_ACCOUNT_FLAG = 'Y'
GW_SELF_UNSELECTED_ACCOUNT_FLAG = 'N'

GW_YES = "DONG_Y"
GW_NO_AGREEMENT_FLAG = "KHONG"
GW_YES_AGREEMENT_FLAG = "CO"
GW_NO_MARKETING_FLAG = "KHONG_DONG_Y"

GW_UDF_NAME = "CN_00_CUNG_CAP_TT_FATCA~THU_NHAP_BQ_03_THANG~NGHE_NGHIEP~NHAN_SMS_EMAIL_TIEP_THI_QUANG_CAO~CUNG_CAP_DOANH_THU_THUAN~THOA_THUAN_PHAP_LY~KHTC_DOI_TUONG"

GW_ACCOUNT_CLASS_CODE = "CAI025"

GW_ACCOUNT_AUTO_CREATE_CIF_Y = "Y"
GW_ACCOUNT_AUTO_CREATE_CIF_N = "N"

GW_ACCOUNT_CHARGE_ON_ORDERING = "Y"
GW_ACCOUNT_CHARGE_ON_RECEIVER = "N"

GW_MARTIAL_STATUS_SINGLE = "S"
GW_MARTIAL_STATUS_MARRIED = "M"
GW_DEFAULT_KHTC_DOI_TUONG = "THONG THUONG"
GW_DEFAULT_TYPE_ID = "ID CARD/PASSPORT"
GW_DEFAULT_CUSTOMER_CATEGORY = "I_11"

GW_CUSTOMER_TYPE_I = "I"
GW_CUSTOMER_TYPE_B = "B"

GW_LANGUAGE = "ENG"

GW_LOCAL_CODE = "101"

GW_DEFAULT_VALUE = ""

GW_TRANSACTION_NAME = "DM_DONVI"
GW_TRANSACTION_VALUE = []

GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP = "GUARDIAN_OR_CUSTOMER_RELATIONSHIP"
GW_REQUEST_PARAMETER_DEBIT_CARD = "DEBIT_CARD"
GW_REQUEST_PARAMETER_CO_OWNER = "CO_OWNER"
GW_REQUEST_PARAMETER_DEFAULT = "DEFAULT"

GW_GL_BRANCH_CODE = '101101001'

GW_REQUEST_DIRECT_INDIRECT = "DS_NV_DIRECT_INDIRECT"
TRANSACTION_FORMS = {
    "D": "Trực tiếp",
    "I": "Gián tiếp"
}

GW_REQUEST_PARAMETER = {
    GW_REQUEST_PARAMETER_DEFAULT: "Giá trị theo GW trả về",
    GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP: "Người giám hộ/Mối quan hệ khách hàng",
    GW_REQUEST_PARAMETER_DEBIT_CARD: "Thẻ ghi nợ",
    GW_REQUEST_PARAMETER_CO_OWNER: "Đồng sở hữu"
}

GW_TYPE_DEFAULT = "CN Đa năng"
GW_LONGITUDE_DEFAULT = 106.70564814326777
GW_LONGITUDE_MIN = 100
GW_LONGITUDE_MAX = 120

GW_LATITUDE_DEFAULT = 10.771912559303502
GW_LATITUDE_MIN = 10
GW_LATITUDE_MAX = 30
