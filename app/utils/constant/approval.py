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

BUSINESS_JOB_CODE_INIT = "OPEN_CIF"
BUSINESS_JOB_CODE_CIF_INFO = "TT_CIF"
BUSINESS_JOB_CODE_CASA_INFO = "TK_TT"
BUSINESS_JOB_CODE_E_BANKING = "E_BANKING"
BUSINESS_JOB_CODE_DEBIT_CARD = "TGN"

BUSINESS_JOB_CODE_START_CASA = "BAT_DAU_CASA"
BUSINESS_JOB_CODE_OPEN_CASA = "MO_TAI_KHOAN"

INIT_RESPONSE = {'status': None, 'error_code': None, 'error_description': None}

OPEN_CASA_STAGE_BEGIN = 'OPEN_CASA_BEGIN'
OPEN_CASA_STAGE_INIT = "OPEN_CASA_KHOI_TAO_HO_SO"
OPEN_CASA_STAGE_APPROVE_KSV = "OPEN_CASA_PHE_DUYET_KSV"
OPEN_CASA_STAGE_APPROVE_KSS = "OPEN_CASA_PHE_DUYET_KSS"
OPEN_CASA_STAGE_COMPLETED = "OPEN_CASA_KET_THUC_HO_SO"

OPEN_CASA_ACTION_PHE_DUYET_KSS = "OPEN_CASA_PHE_DUYET_KSS"
OPEN_CASA_ACTION_BSTTKXTL_KSS = "OPEN_CASA_BSTTKXTL_KSS"
OPEN_CASA_ACTION_BSTTXTL_KSS = "OPEN_CASA_BSTTXTL_KSS"
OPEN_CASA_ACTION_XTL_KSS = "OPEN_CASA_XTL_KSS"

OPEN_CASA_ACTION_PHE_DUYET_KSV = "OPEN_CASA_PHE_DUYET_KSV"
OPEN_CASA_ACTION_BSTTKXTL_KSV = "OPEN_CASA_BSTTKXTL_KSV"
OPEN_CASA_ACTION_BSTTXTL_KSV = "OPEN_CASA_BSTTXTL_KSV"
OPEN_CASA_ACTION_XTL_KSV = "OPEN_CASA_XTL_KSV"

OPEN_CASA_ACTIONS = {
    OPEN_CASA_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    OPEN_CASA_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    OPEN_CASA_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    OPEN_CASA_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    OPEN_CASA_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    OPEN_CASA_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    OPEN_CASA_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    OPEN_CASA_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

OPEN_CASA_APPROVE_STAGES = {
    OPEN_CASA_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    OPEN_CASA_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}

STAGE_BEGINS = [
    CIF_STAGE_BEGIN,
    OPEN_CASA_STAGE_BEGIN
]

STAGE_INITS = [
    CIF_STAGE_INIT,
    OPEN_CASA_STAGE_INIT
]

STAGE_APPROVE_SUPERVISORS = [
    CIF_STAGE_APPROVE_KSV,
    OPEN_CASA_STAGE_APPROVE_KSV
]

STAGE_APPROVE_AUDITS = [
    CIF_STAGE_APPROVE_KSS,
    OPEN_CASA_STAGE_APPROVE_KSS
]

