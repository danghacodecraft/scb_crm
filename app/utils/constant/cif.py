CIF_ID_TEST = '7654321'  # cif_id dùng tạm để test
CIF_ID_NEW_TEST = 'NEW123'  # cif_id dùng tạm để test khi tạo

IDENTITY_TYPE_CODE_NON_RESIDENT = 'VANG_LAI'
ADDRESS_TYPE_CODE_UNDEFINDED = 'KHONG_XAC_DINH'

CIF_METHOD_SIGN_ALL = 1
CIF_METHOD_SIGN_ONE = 2
CIF_METHOD_SIGN_PARTLY = 3
CIF_AGREEMENT_AUTHORIZATION_1 = 'NOIDUNG1'
CIF_AGREEMENT_AUTHORIZATION_2 = 'NOIDUNG2'
CIF_NUMBER_MIN_LENGTH = 7
CIF_NUMBER_MAX_LENGTH = 7
UUID_MIN_LENGTH = 32
UUID_MAX_LENGTH = 32
CIF_NUMBER_REGEX = r"^\d{7}$"

BUSINESS_TYPE_CODE_CIF = "CIF"
BUSINESS_TYPE_CODE_OPEN_CASA = "OPEN_CASA"
BUSINESS_TYPE_CODE_CLOSE_CASA = "CLOSE_CASA"
BUSINESS_TYPE_CODE_WITHDRAW = "WITHDRAW"
BUSINESS_TYPE_CODE_TOP_UP_CASA = "CASA_TOP_UP"
BUSINESS_TYPE_CODE_OPEN_TD_ACCOUNT = "OPEN_TD_ACCOUNT"
BUSINESS_TYPE_CODE_REDEEM_OPEN_TD = "REDEEM_ACCOUNT"
BUSINESS_TYPE_CODE_AMOUNT_BLOCK = "AMOUNT_BLOCK"
BUSINESS_TYPE_CODE_AMOUNT_UNBLOCK = "AMOUNT_UNBLOCK"
BUSINESS_TYPE_CODE_TRANSFER = "TRANSFER"

BUSINESS_TYPE_CODE_OPEN_SEC = "OPEN_SEC"


IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD = 'CMND'
IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD = 'CCCD'
IDENTITY_DOCUMENT_TYPE_PASSPORT = 'HO_CHIEU'

IDENTITY_DOCUMENT_TYPE = {
    IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD: 'Chứng minh nhân dân',
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD: 'Căn cước công dân',
    IDENTITY_DOCUMENT_TYPE_PASSPORT: 'Hộ chiếu'
}

HAND_SIDE_LEFT_CODE = '1'
HAND_SIDE_RIGHT_CODE = '2'

ACTIVE_FLAG_CREATE_FINGERPRINT = 1
FRONT_FLAG_CREATE_FINGERPRINT = 0
ACTIVE_FLAG_CREATE_SIGNATURE = 1

IMAGE_TYPE_FINGERPRINT = 'VT'
IMAGE_TYPE_SIGNATURE = 'CK'
IMAGE_TYPE_FACE = 'KM'

STAFF_TYPE_BUSINESS_CODE = "NV_KD"
STAFF_TYPE_REFER_INDIRECT_CODE = "NV_GT_GT"

RESIDENT_ADDRESS_CODE = "THUONG_TRU"
CONTACT_ADDRESS_CODE = "TAM_TRU"

IMAGE_TYPE_CODE_IDENTITY = "GT_DD"
IMAGE_TYPE_CODE_SUB_IDENTITY = "GT_DD_P"
IMAGE_TYPE_CODE_FINGERPRINT = "VT"
IMAGE_TYPE_CODE_SIGNATURE = "CK"
IMAGE_TYPE_CODE_FACE = "KM"
IDENTITY_IMAGE_FLAG_BACKSIDE = 0
IDENTITY_IMAGE_FLAG_FRONT_SIDE = 1
IDENTITY_PASSPORT_TYPE_ID_DEFAULT = "P"

CUSTOMER_COMPLETED_FLAG = 1
CUSTOMER_UNCOMPLETED_FLAG = 0

CUSTOMER_TYPE_ORGANIZE = "TO_CHUC"

CUSTOMER_CONTACT_TYPE_EMAIL = 'TTCN_EMAIL'
CUSTOMER_CONTACT_TYPE_MOBILE = 'TTCN_MOBILE'

CUSTOMER_CONTACT_TYPE_GROUP_E_BANKING = "E_BANKING"
CUSTOMER_CONTACT_TYPE_GROUP_TTCN = "THONG_TIN_CA_NHAN"
CUSTOMER_CONTACT_TYPE_GROUP = {
    CUSTOMER_CONTACT_TYPE_GROUP_E_BANKING: "Hình thức kích hoạt mật khẩu lần đầu",
    CUSTOMER_CONTACT_TYPE_GROUP_TTCN: "Hình thức liên hệ"
}

LANGUAGE_TYPE_VN = 'VN'
LANGUAGE_TYPE_EN = 'EN'

LANGUAGE_ID_VN = "1"
LANGUAGE_ID_EN = "2"

# Dùng trong table CRM_CUST_PERSONAL_RELATIONSHIP
CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN = 0
CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP = 1
CUSTOMER_ADDRESS_DOMESTIC_FLAG = 1
CUSTOMER_ADDRESS_SAME_PERMANENT_FLAG = 0
CUSTOMER_RELATIONSHIP_TYPE = {
    CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN: "Thông tin người giám hộ",
    CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP: "Mối quan hệ khách hàng"
}

EKYC_IDENTITY_TYPE_PASSPORT = 0
EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD = 1
EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD = 2
EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD = 3
EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD = 4

EKYC_IDENTITY_TYPE = {
    EKYC_IDENTITY_TYPE_PASSPORT: "Hộ chiếu",
    EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD: "CMND mặt trước",
    EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD: "CMND mặt sau",
    EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD: "CCCD mặt trước",
    EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD: "CCCD mặt sau",
}

ADDRESS_COUNTRY_CODE_VN = 'VN'
CRM_GENDER_TYPE_MALE = 'M'
CRM_GENDER_TYPE_FEMALE = 'F'

CRM_TITLE_TYPE_MALE = 'ONG'
CRM_TITLE_TYPE_FEMALE = 'BA'

EKYC_GENDER_TYPE_FEMALE = 'F'
EKYC_GENDER_TYPE_MALE = "M"

EKYC_DOCUMENT_TYPE_PASSPORT = 0
EKYC_DOCUMENT_TYPE_OLD_IDENTITY = 1
EKYC_DOCUMENT_TYPE_NEW_IDENTITY = 2
EKYC_DOCUMENT_TYPE_OLD_CITIZEN = 3
EKYC_DOCUMENT_TYPE_NEW_CITIZEN = 4

EKYC_DOCUMENT_TYPE = {
    EKYC_DOCUMENT_TYPE_PASSPORT: 'Hộ chiếu',
    EKYC_DOCUMENT_TYPE_OLD_IDENTITY: 'CMND Cũ',
    EKYC_DOCUMENT_TYPE_NEW_IDENTITY: 'CMND Mới',
    EKYC_DOCUMENT_TYPE_OLD_CITIZEN: 'CCCD Cũ',
    EKYC_DOCUMENT_TYPE_NEW_CITIZEN: 'CCCD Mới'
}

IDENTITY_DOCUMENT_TYPE_TYPE = {
    IDENTITY_DOCUMENT_TYPE_PASSPORT: [
        EKYC_DOCUMENT_TYPE_PASSPORT
    ],
    IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD: [
        EKYC_DOCUMENT_TYPE_OLD_IDENTITY,
        EKYC_DOCUMENT_TYPE_NEW_IDENTITY
    ],
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD: [
        EKYC_DOCUMENT_TYPE_OLD_CITIZEN,
        EKYC_DOCUMENT_TYPE_NEW_CITIZEN
    ]
}

# Dùng trong cho field e_banking_register_account_type(col_name=eb_reg_account_type)
EBANKING_ACCOUNT_TYPE_CHECKING = 'DD'
EBANKING_ACCOUNT_TYPE_SAVING = 'FD'

EBANKING_ACCOUNT_TYPE = {
    EBANKING_ACCOUNT_TYPE_CHECKING: "Tài khoản thanh toán",
    EBANKING_ACCOUNT_TYPE_SAVING: "Tài khoản tiết kiệm"
}

EBANKING_ACTIVE_PASSWORD_EMAIL = "Email"
EBANKING_ACTIVE_PASSWORD_SMS = "SMS"

EBANKING_PAYMENT_FEE = 1
EBANKING_NOT_PAYMENT_FEE = 0
METHOD_TYPE_HARD_TOKEN = "HARD_TOKEN"

CHANNEL_AT_THE_COUNTER = "TAI_QUAY"
CHANNEL_AT_THE_MOBILE = "ONLINE"
ACC_STRUCTURE_TYPE_LEVEL_1 = 1
ACC_STRUCTURE_TYPE_LEVEL_2 = 2
ACC_STRUCTURE_TYPE_LEVEL_3 = 3

ACTIVE_FLAG_ACTIVED = 1
ACTIVE_FLAG_DISACTIVED = 0

SOA_GENDER_TYPE_MALE = "M"
SOA_GENDER_TYPE_FEMALE = "F"
AGREEMENT_AUTHOR_TYPE_DD = "DD"
DROPDOWN_NONE_DICT = {
    "id": None,
    "code": None,
    "name": None
}

BUSINESS_FORM_TTCN_GTDD_GTDD = "TTCN_GTDD_GTDD"
BUSINESS_FORM_TTCN_GTDD_KM = "TTCN_GTDD_KM"
BUSINESS_FORM_TTCN_GTDD_VT = "TTCN_GTDD_VT"
BUSINESS_FORM_TTCN_GTDD_CK = "TTCN_GTDD_CK"
BUSINESS_FORM_TTCN_GTDD_GTDDP = "TTCN_GTDD_GTDDP"
BUSINESS_FORM_OPEN_CIF_PD = "PD"

BUSINESS_FORM_TTCN_TTCN = "TTCN_TTCN"
BUSINESS_FORM_TTCN_TTLL = "TTCN_TTLL"
BUSINESS_FORM_TTCN_FATCA = "TTCN_FATCA"
BUSINESS_FORM_TTCN_NGH = "TTCN_NGH"
BUSINESS_FORM_TTCN_MQHKH = "TTCN_MQHKH"

BUSINESS_FORM_TTK = "TTK"

BUSINESS_FORM_TKTT_CTTKTT = "TKTT_CTTKTT"
BUSINESS_FORM_TKTT_DSH = "TKTT_DSH"

BUSINESS_FORM_EB = "EB"

BUSINESS_FORM_DEBIT_CARD = "DEBIT_CARD"

BUSINESS_FORM_AMOUNT_BLOCK = "AMOUNT_BLOCK_KHOI_TAO"
BUSINESS_FORM_AMOUNT_BLOCK_PD = "AMOUNT_BLOCK_PD"

BUSINESS_FORM_AMOUNT_UNBLOCK = "AMOUNT_UNBLOCK_KHOI_TAO"
BUSINESS_FORM_AMOUNT_UNBLOCK_PD = "AMOUNT_UNBLOCK_PD"

BUSINESS_FORM_CLOSE_CASA = "CLOSE_CASA_KHOI_TAO"
BUSINESS_FORM_CLOSE_CASA_PD = "CLOSE_CASA_PD"

BUSINESS_FORM_WITHDRAW = "WITHDRAW_KHOI_TAO"
BUSINESS_FORM_WITHDRAW_PD = "WITHDRAW_UNBLOCK_PD"

BUSINESS_FORM_OPEN_CASA_PD = 'OPEN_CASA_PD'
BUSINESS_FORM_REDEEM_ACCOUNT = 'REDEEM_ACCOUNT_KHOI_TAO'
BUSINESS_FORM_OPEN_CASA_OPEN_CASA = 'OPEN_CASA_KHOI_TAO'
BUSINESS_FORM_OPEN_TD_OPEN_TD_ACCOUNT = 'OPEN_TD_ACCOUNT_KHOI_TAO'
BUSINESS_FORM_OPEN_TD_ACCOUNT_PAY = 'OPEN_TD_ACCOUNT_PAY'
BUSINESS_FORM_OPEN_TD_OPEN_TD_ACCOUNT_PD = 'OPEN_TD_ACCOUNT_PD'

BUSINESS_FORM_CASA_TOP_UP = 'CASA_TOP_UP_KHOI_TAO'
BUSINESS_FORM_CASA_TRANSFER = 'TRANSFER_KHOI_TAO'
BUSINESS_FORM_CASA_TRANSFER_PD = "TRANSFER_PD"

TRANSACTION_STATUS_ALL = "1"
TRANSACTION_STATUS_PROCESSING = "2"
TRANSACTION_STATUS_SUCCESS = "3"
TRANSACTION_STATUS_REJECTED = "4"
TRANSACTION_STATUS_FAILED = "5"
TRANSACTION_STATUS_CANCELED = "6"

CHECK_CONDITION_WITHDRAW = 50000
CHECK_CONDITION_VAT = 10

APPROVE_STATUS_PENDING = "0"
APPROVE_STATUS_APPROVED = "1"
APPROVE_STATUS_REFUSE = "2"

TRANSACTION_STATUS_TYPE = {
    TRANSACTION_STATUS_ALL: 'Tất cả',
    TRANSACTION_STATUS_PROCESSING: 'Đang xử lí',
    TRANSACTION_STATUS_SUCCESS: 'Thành công',
    TRANSACTION_STATUS_REJECTED: 'Từ chối',
    TRANSACTION_STATUS_FAILED: 'Thất bại',
    TRANSACTION_STATUS_CANCELED: 'Hủy',
}
POST_CHECK_TYPE = {
    APPROVE_STATUS_PENDING: "Chờ duyệt",
    APPROVE_STATUS_APPROVED: "Đã duyệt",
    APPROVE_STATUS_REFUSE: "Từ chối",
}
TRANSACTION_eKYC = '1'
TRANSACTION_VTM = '2'
TRANSACTION_LiveBank = '3'
TRANSACTIONS_TYPE = {
    TRANSACTION_eKYC: 'eKYC',
    TRANSACTION_VTM: 'VTM',
    TRANSACTION_LiveBank: 'LiveBank'
}

PROFILE_HISTORY_STATUS_INIT = 0
PROFILE_HISTORY_STATUS_APPROVED = 1
PROFILE_HISTORY_STATUS_WAITING = 2
PROFILE_HISTORY_STATUS_RETURN = 3
PROFILE_HISTORY_STATUS_CANCEL = 4

PROFILE_HISTORY_STATUS = {
    0: "Khởi tạo",
    1: "Đã duyệt",
    2: "Chờ duyệt",
    3: "Hoàn trả",
    4: "Hủy"
}

PROFILE_HISTORY_DESCRIPTIONS_INIT_CIF = "Khởi tạo CIF"
PROFILE_HISTORY_DESCRIPTIONS_EDIT_CIF = "Tu chỉnh CIF"
PROFILE_HISTORY_DESCRIPTIONS_OPEN_CASA_ACCOUNT = "Mở tài khoản thanh toán"
PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT = "Nộp tiền vào tài khoản thanh toán"
PROFILE_HISTORY_DESCRIPTIONS_CLOSE_CASA_ACCOUNT = "Đóng tài khoản thanh toán"
PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW = "Rút tiền từ Tài khoản thanh toán"
PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT = "Mở tài khoản tiết kiệm"
PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT_PAY_IN = "Mở tài khoản tiết kiệm - Nguồn tiền"
PROFILE_HISTORY_DESCRIPTIONS_INIT_REDEEM_ACCOUNT = "Tất toán tài khoản tiết kiệm"
PROFILE_HISTORY_DESCRIPTIONS_INIT_DEBIT_CARD = "Tạo thẻ ghi nợ"
PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING = "Tạo E-Banking"

PROFILE_HISTORY_DESCRIPTIONS_INIT_OPEN_SEC = "Phát hành SEC"

PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK = "Phong tỏa tài khoản"
PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK = "Giải tỏa tài khoản"
PROFILE_HISTORY_DESCRIPTIONS_OPEN_TD_ACCOUNT = "Mở tài khoản tiết kiệm"
PROFILE_HISTORY_DESCRIPTIONS_TRANSFER_CASA_ACCOUNT = "Chuyển khoản tài khoản thanh toán"


PROFILE_HISTORY_DESCRIPTIONS = {
    BUSINESS_TYPE_CODE_CIF: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_INIT_CIF,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên [Thông tin cá nhân]"
    },
    # PROFILE_HISTORY_DESCRIPTIONS_EDIT_CIF: "Tu chỉnh CIF",
    BUSINESS_TYPE_CODE_OPEN_CASA: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_OPEN_CASA_ACCOUNT,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên "
                   f"[{PROFILE_HISTORY_DESCRIPTIONS_OPEN_CASA_ACCOUNT}]"
    },
    BUSINESS_TYPE_CODE_CLOSE_CASA: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_CLOSE_CASA_ACCOUNT,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên "
                   f"[{PROFILE_HISTORY_DESCRIPTIONS_CLOSE_CASA_ACCOUNT}]"
    },
    BUSINESS_TYPE_CODE_TOP_UP_CASA: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên "
                   f"[{PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT}]"
    },
    BUSINESS_TYPE_CODE_REDEEM_OPEN_TD: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_INIT_REDEEM_ACCOUNT,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên "
                   f"[{PROFILE_HISTORY_DESCRIPTIONS_INIT_REDEEM_ACCOUNT}]"
    },
    BUSINESS_TYPE_CODE_OPEN_TD_ACCOUNT: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên "
                   f"[{PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT}]"
    },
    # PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT: "Mở tài khoản tiết kiệm",
    # PROFILE_HISTORY_DESCRIPTIONS_INIT_DEBIT_CARD: "Tạo thẻ ghi nợ",
    # PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING: "Tạo E-Banking"

    BUSINESS_TYPE_CODE_AMOUNT_BLOCK: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên [Phong tỏa tài khoản]"
    },
    BUSINESS_TYPE_CODE_AMOUNT_UNBLOCK: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên [Giải tỏa tài khoản]"
    },
    BUSINESS_TYPE_CODE_WITHDRAW: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   f"Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên [{PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW}]"
    },
    BUSINESS_TYPE_CODE_TRANSFER: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_TRANSFER_CASA_ACCOUNT,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên [Giải tỏa tài khoản]"
    },
    BUSINESS_TYPE_CODE_OPEN_SEC: {
        'description': PROFILE_HISTORY_DESCRIPTIONS_INIT_OPEN_SEC,
        'content': "Giao dịch viên đang chuẩn bị hồ sơ. "
                   "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên "
                   f"[{PROFILE_HISTORY_DESCRIPTIONS_INIT_OPEN_SEC}]"
    }
}

EB_QUESTION_TYPE_BASIC_01 = 'BASIC_01'
EB_QUESTION_TYPE_BASIC_02 = 'BASIC_02'
EB_QUESTION_TYPE_ADVANCE = 'ADVANCE'

EB_QUESTION_TYPE = {
    EB_QUESTION_TYPE_BASIC_01: 'Câu hỏi cơ bản 1',
    EB_QUESTION_TYPE_BASIC_02: 'Câu hỏi cơ bản 2',
    EB_QUESTION_TYPE_ADVANCE: 'Câu hỏi nâng cao'
}

CLASSIFICATION_PERSONAL = 'I_11'
TRANSACTION_JOB_OPEN_CIF = 'OPEN_CIF'
NEWS_COMMENT_FILTER_BY_INTERESTED = "interested"
NEWS_COMMENT_FILTER_BY_TIME = "time"

NEWS_COMMENT_FILTER_PARAMS = {NEWS_COMMENT_FILTER_BY_INTERESTED, NEWS_COMMENT_FILTER_BY_TIME}

CIF_STAGE_ROLE_CODE_TELLER = "GDV"
CIF_STAGE_ROLE_CODE_SUPERVISOR = "KSV"
CIF_STAGE_ROLE_CODE_AUDIT = "KSS"

CIF_STAGE_ROLE_CODES = {
    CIF_STAGE_ROLE_CODE_TELLER: "GDV",
    CIF_STAGE_ROLE_CODE_SUPERVISOR: "KSV",
    CIF_STAGE_ROLE_CODE_AUDIT: "KSS"
}

TRANSACTION_STATUS_CODE_INIT = 0
TRANSACTION_STATUS_CODE_APPROVED = 1
TRANSACTION_STATUS_CODE_WAITING = 2
TRANSACTION_STATUS_CODE_REJECTED = 3
TRANSACTION_STATUS_CODE_CANCEL = 4
TRANSACTION_STATUS_LIST = {
    TRANSACTION_STATUS_CODE_INIT: "Khởi tạo",
    TRANSACTION_STATUS_CODE_APPROVED: "Đã duyệt",
    TRANSACTION_STATUS_CODE_WAITING: "Chờ duyệt",
    TRANSACTION_STATUS_CODE_REJECTED: "Hoàn trả",
    TRANSACTION_STATUS_CODE_CANCEL: "Hủy"
}
