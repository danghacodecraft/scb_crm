CIF_ID_TEST = '123'  # cif_id dùng tạm để test
CIF_ID_NEW_TEST = 'NEW123'  # cif_id dùng tạm để test khi tạo

CIF_NUMBER_MIN_LENGTH = 7
CIF_NUMBER_MAX_LENGTH = 7

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

STAFF_TYPE_BUSINESS_CODE = "NV_KD"
STAFF_TYPE_REFER_INDIRECT_CODE = "NV_GT_GT"

RESIDENT_ADDRESS_CODE = "THUONG_TRU"
CONTACT_ADDRESS_CODE = "TAM_TRU"

IMAGE_TYPE_CODE_IDENTITY = "GT_DD"
IMAGE_TYPE_CODE_SUB_IDENTITY = "GT_DD_P"
IMAGE_TYPE_CODE_FINGERPRINT = "VT"
IMAGE_TYPE_CODE_SIGNATURE = "CK"

IDENTITY_IMAGE_FLAG_BACKSIDE = 0
IDENTITY_IMAGE_FLAG_FRONT_SIDE = 1

CUSTOMER_COMPLETED_FLAG = 1
CUSTOMER_UNCOMPLETED_FLAG = 0

CUSTOMER_CONTACT_TYPE_EMAIL = 'EMAIL'
CUSTOMER_CONTACT_TYPE_MOBILE = 'MOBILE'

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
CRM_GENDER_TYPE_MALE = 'NAM'
CRM_GENDER_TYPE_FEMALE = 'NU'
EKYC_GENDER_TYPE_FEMALE = 'F'
EKYC_GENDER_TYPE_MALE = "M"

EKYC_DOCUMENT_TYPE_PASSPORT = 0
EKYC_DOCUMENT_TYPE_OLD_IDENTITY = 1
EKYC_DOCUMENT_TYPE_NEW_IDENTITY = 2
EKYC_DOCUMENT_TYPE_OLD_CITIZEN = 3
EKYC_DOCUMENT_TYPE_NEW_CITIZEN = 4


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

EBANKING_HAS_FEE = 0
EBANKING_HAS_NO_FEE = 1

CHANNEL_AT_THE_COUNTER = "TAI_QUAY"

ACC_STRUCTURE_TYPE_LEVEL_1 = 1
ACC_STRUCTURE_TYPE_LEVEL_2 = 2
ACC_STRUCTURE_TYPE_LEVEL_3 = 3

ACTIVE_FLAG_ACTIVED = 1
ACTIVE_FLAG_DISACTIVED = 0


SOA_GENDER_TYPE_MALE = "M"
SOA_GENDER_TYPE_FEMALE = "F"

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

BUSINESS_FORM_TTCN_TTCN = "TTCN_TTCN"
BUSINESS_FORM_TTCN_TTLL = "TTCN_TTLL"
BUSINESS_FORM_TTCN_FATCA = "TTCN_FATCA"
BUSINESS_FORM_TTCN_NGH = "TTCN_NGH"
BUSINESS_FORM_TTCN_MQHKH = "TTCN_MQHKH"

BUSINESS_FORM_TTK = "TTK"

BUSINESS_FORM_TKTT_CTTKTT = "TKTT_CTTKTT"
BUSINESS_FORM_TKTT_DSH = "TKTT_DSH"
