CIF_STAGE_BEGIN = "CIF_BEGIN"
CIF_STAGE_INIT = "KHOI_TAO_HO_SO"
CIF_STAGE_APPROVE_KSV = "PHE_DUYET_KSV"
CIF_STAGE_APPROVE_KSS = "PHE_DUYET_KSS"
CIF_STAGE_COMPLETED = "KET_THUC_HO_SO"

CIF_ACTION_PHE_DUYET_KSS = "PHE_DUYET_KSS"
CIF_ACTION_BSTTKXTL_KSS = "BSTTKXTL_KSS"
CIF_ACTION_BSTTXTL_KSS = "BSTTXTL_KSS"
CIF_ACTION_XTL_KSS = "XTL_KSS"

CIF_ACTION_PHE_DUYET_KSV = "PHE_DUYET_KSV"
CIF_ACTION_BSTTKXTL_KSV = "BSTTKXTL_KSV"
CIF_ACTION_BSTTXTL_KSV = "BSTTXTL_KSV"
CIF_ACTION_XTL_KSV = "XTL_KSV"

CIF_ACTIONS = {
    CIF_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    CIF_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    CIF_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    CIF_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    CIF_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    CIF_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    CIF_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    CIF_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

CIF_APPROVE_STAGES = {
    CIF_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    CIF_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}

BUSINESS_JOB_CODE_INIT = "KHOI_TAO"
BUSINESS_JOB_CODE_CIF_INFO = "TT_CIF"
BUSINESS_JOB_CODE_CASA_INFO = "TK_TT"
BUSINESS_JOB_CODE_E_BANKING = "E_BANKING"
BUSINESS_JOB_CODE_DEBIT_CARD = "TGN"

BUSINESS_JOB_CODES = {
    BUSINESS_JOB_CODE_INIT: {'status': None, 'error_code': None, 'error_description': None},
    BUSINESS_JOB_CODE_CIF_INFO: {'status': None, 'error_code': None, 'error_description': None},
    BUSINESS_JOB_CODE_CASA_INFO: {'status': None, 'error_code': None, 'error_description': None},
    BUSINESS_JOB_CODE_E_BANKING: {'status': None, 'error_code': None, 'error_description': None},
    BUSINESS_JOB_CODE_DEBIT_CARD: {'status': None, 'error_code': None, 'error_description': None}
}
