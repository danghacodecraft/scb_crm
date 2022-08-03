EKYC_DATE_FORMAT = '%d/%m/%Y'
EKYC_DEFAULT_VALUE = ""
BUSINESS_FORM_EKYC = "CREATE_CUSTOMER_SERVICE"
MENU_CODE = 'EKYC_VIEW'
MENU_CODE_VIEW = "EKYC_VIEW"
GROUP_ROLE_CODE_VIEW = 'EKYC_VIEW'
GROUP_ROLE_CODE_AP = 'EKYC_AP'
GROUP_ROLE_CODE_IN = 'EKYC_IN'
is_success = 'Success'

STATUS_SUCCESS = "SUCCESSED"
STATUS_FAILED = "FAILED"
STATUS_OPEN = "Mở"
STATUS_CLOSE = "Đóng"
EKYC_FLAG = 1

ERROR_CREATE_USER = "CREATE_USER"
ERROR_CREATE_CIF = "CREATE_CIF"
ERROR_CREATE_CARD_VIRTUAL = "CREATE_CARD_VIRTUAL"
ERROR_UPLOAD_ATTACHMENT_PORTRAIT = "UPLOAD_ATTACHMENT_PORTRAIT"
ERROR_UPLOAD_ATTACHMENT_ID_BACK = "UPLOAD_ATTACHMENT_ID_BACK"
ERROR_UPLOAD_ATTACHMENT_ID_FRONT = "UPLOAD_ATTACHMENT_ID_FRONT"
ERROR_VERIFIED = "VERIFIED"
ERROR_CHECK_ALM = "CHECK_ALM"
ERROR_CREATE_E_BANKING = "ERROR_CREATE_E_BANKING"

ERROR_CODE_FAILED_EKYC = {
    ERROR_CREATE_CIF: "TC01: Tạo CIF thất bại (GTDD, SĐT, Email)",
    ERROR_VERIFIED: "TC02: Trùng họ tên và ngày tháng năm sinh với KH hiện hữu",
    ERROR_CHECK_ALM: "TC03: Check AML"
}

ERROR_CODE_PROCESSING_EKYC = {
    ERROR_CREATE_E_BANKING: "XL01: Tạo user Ebanking thất bại",
    ERROR_UPLOAD_ATTACHMENT_PORTRAIT: "XL02: Lỗi tải lên ảnh chân dung",
    ERROR_UPLOAD_ATTACHMENT_ID_BACK: "XL03: Lỗi tải lên ảnh mặt sau",
    ERROR_UPLOAD_ATTACHMENT_ID_FRONT: "XL04: Lỗi tải lên ảnh mặt trước",
}

ERROR_CODE_EKYC = {
    ERROR_CREATE_USER: "User tồn tại",
    ERROR_CREATE_CIF: "Tạo CIF thất bại",
    ERROR_CREATE_CARD_VIRTUAL: "Thẻ ảo tồn tại",
    ERROR_VERIFIED: "Trùng họ tên và ngày tháng năm sinh với KH hiện hữu",
    ERROR_UPLOAD_ATTACHMENT_PORTRAIT: "Lỗi tải lên ảnh chân dung",
    ERROR_UPLOAD_ATTACHMENT_ID_BACK: "Lỗi tải lên ảnh mặt sau",
    ERROR_UPLOAD_ATTACHMENT_ID_FRONT: "Lỗi tải lên ảnh mặt trước",
    ERROR_CREATE_E_BANKING: "Tạo DV Ebank thất bại",
    ERROR_CHECK_ALM: "CHECK_ALM",
}

EKYC_REGION_ZONE_MAPPING = [
    {
        "region_code": "V01",
        "zone_id": 1
    },
    {
        "region_code": "V02",
        "zone_id": 2
    },
    {
        "region_code": "V03",
        "zone_id": 3
    },
    {
        "region_code": "V05",
        "zone_id": 4
    },
    {
        "region_code": "V06",
        "zone_id": 5
    },
    {
        "region_code": "V07",
        "zone_id": 6
    },
    {
        "region_code": "V08",
        "zone_id": 7
    },
    {
        "region_code": "V09",
        "zone_id": 8
    },
    {
        "region_code": "V10",
        "zone_id": 9
    },
    {
        "region_code": "V11",
        "zone_id": 10
    },
    {
        "region_code": "V12",
        "zone_id": 11
    },
    {
        "region_code": "V14",
        "zone_id": 12
    },
    {
        "region_code": "V15",
        "zone_id": 13
    },
    {
        "region_code": "V97",
        "zone_id": 14
    },
    {
        "region_code": "V98",
        "zone_id": 15
    },
    {
        "region_code": "V00",
        "zone_id": 16
    },
    {
        "region_code": "V99",
        "zone_id": 1
    }
]

EKYC_STATUS_DEFAULT = 1
EKYC_CUSTOMER_STATUS = {
    EKYC_STATUS_DEFAULT: "Mặc định"
}

EKYC_APPROVE_STATUS_DEFAULT = 1
EKYC_CUSTOMER_APPROVE_STATUS = {
    EKYC_APPROVE_STATUS_DEFAULT: "Mặc định"
}

EKYC_KSS_STATUS_DEFAULT = 1
EKYC_CUSTOMER_KSS_STATUS = {
    EKYC_KSS_STATUS_DEFAULT: "Mặc định"
}
