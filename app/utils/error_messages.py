# status error
PAGING_ERROR = "PAGING_ERROR"
VALIDATE_ERROR = "VALIDATE_ERROR"

USER_ID_NOT_EXIST = "USER_ID_NOT_EXIST"
USERNAME_OR_PASSWORD_INVALID = "USERNAME_OR_PASSWORD_INVALID"
ERROR_INVALID_TOKEN = "INVALID_TOKEN"

ERROR_CALL_SERVICE_FILE = "ERROR_CALL_SERVICE_FILE"
ERROR_CALL_SERVICE_EKYC = "ERROR_CALL_SERVICE_EKYC"
ERROR_CALL_SERVICE_TEMPLATE = "ERROR_CALL_SERVICE_TEMPLATE"
ERROR_CALL_SERVICE_SOA = "ERROR_CALL_SERVICE_SOA"
ERROR_CUSTOMER_DETAIL_CALL_SERVICE_SOA = "ERROR_CUSTOMER_DETAIL_CALL_SERVICE_SOA"

ERROR_FILE_IS_NULL = "ERROR_FILE_IS_NULL"
ERROR_FILE_TOO_LARGE = "ERROR_FILE_TOO_LARGE"
ERROR_TOO_MANY_FILE = "ERROR_TOO_MANY_FILE"

ERROR_ID_NOT_EXIST = "ID_NOT_EXIST"

ERROR_COMMIT = "ERROR_COMMIT"

ERROR_CIF_ID_NOT_EXIST = "CIF_ID_NOT_EXIST"
ERROR_CIF_ID_NOT_CUSTOMER_ADDRESS_EXIST = "CIF_ID_NOT_CUSTOMER_ADDRESS_EXIST"
ERROR_CIF_NUMBER_DUPLICATED = "CIF_NUMBER_DUPLICATED"
ERROR_CIF_NUMBER_EXIST = "CIF_NUMBER_EXIST"
ERROR_CIF_NUMBER_NOT_EXIST = "CIF_NUMBER_NOT_EXIST"
ERROR_CIF_NUMBER_INVALID = "ERROR_CIF_NUMBER_INVALID"
ERROR_CIF_NUMBER_NOT_COMPLETED = "CIF_NUMBER_NOT_COMPLETED"
ERROR_IDENTITY_DOCUMENT_NOT_EXIST = "ERROR_IDENTITY_DOCUMENT_NOT_EXIST"
ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST = "ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST"
ERROR_CASA_ACCOUNT_NOT_EXIST = "CASA_ACCOUNT_NOT_EXIST"
ERROR_CUSTOMER_INDIVIDUAL_INFO = "CUSTOMER_INDIVIDUAL_INFO_NOT_EXIST"
ERROR_CUSTOMER_IDENTITY = "CUSTOMER_IDENTITY_NOT_EXIST"
ERROR_CUSTOMER_IDENTITY_IMAGE = "CUSTOMER_IDENTITY_IMAGE_NOT_EXIST"
ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST = "AGREEMENT_AUTHORIZATIONS_NOT_EXIST"
ERROR_CAN_NOT_CREATE = "CAN_NOT_CREATE"

ERROR_IMAGE_TYPE_NOT_EXIST = 'IMAGE_TYPE_NOT_EXIST'
ERROR_SIGNATURE_IS_NULL = "ERROR_SIGNATURE_IS_NULL"
ERROR_PHONE_NUMBER = "ERROR_PHONE_NUMBER"

ERROR_RELATION_CUSTOMER_SELF_RELATED = "ERROR_CUSTOMER_SELF_RELATED"
ERROR_RELATIONSHIP_EXIST = "ERROR_RELATION_EXIST"
ERROR_RELATIONSHIP_TYPE_ID_NOT_EXIST = "ERROR_RELATIONSHIP_TYPE_ID_NOT_EXIST"
ERROR_RELATIONSHIP_NOT_GUARDIAN = "ERROR_RELATIONSHIP_NOT_GUARDIAN"

ERROR_INVALID_URL = "ERROR_INVALID_URL"
ERROR_INVALID_NUMBER = "ERROR_INVALID_NUMBER"

ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST = "ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST"
ERROR_WRONG_TYPE_IDENTITY = "ERROR_WRONG_TYPE_IDENTITY"

ERROR_NOT_NULL = "ERROR_NOT_NULL"

ERROR_NO_DATA = "ERROR_NO_DATA"

MESSAGE_STATUS = {
    # general error
    PAGING_ERROR: "Can not found page!",
    VALIDATE_ERROR: "Validate error!",

    USER_ID_NOT_EXIST: "User id is not exist",
    USERNAME_OR_PASSWORD_INVALID: "Username or password is invalid",
    ERROR_INVALID_TOKEN: "Token is invalid",

    ERROR_CALL_SERVICE_FILE: "Call service file error",
    ERROR_CALL_SERVICE_EKYC: "Call service eKYC error",
    ERROR_CALL_SERVICE_TEMPLATE: "Call service template error",
    ERROR_CALL_SERVICE_SOA: "Call service SOA error",
    ERROR_CUSTOMER_DETAIL_CALL_SERVICE_SOA: "Customer detail call service SOA error",
    ERROR_FILE_IS_NULL: "File can not be empty",
    ERROR_FILE_TOO_LARGE: "File size is too large",
    ERROR_TOO_MANY_FILE: "Upload too many file",

    ERROR_COMMIT: "Commit to database error",

    ERROR_ID_NOT_EXIST: "Id is not exist",
    ERROR_CIF_NUMBER_EXIST: "CIF number is exist",
    ERROR_CIF_NUMBER_NOT_EXIST: "CIF number does not exist",
    ERROR_CIF_NUMBER_DUPLICATED: "CIF numbers are duplicated",
    ERROR_CIF_NUMBER_INVALID: "CIF number must be number",
    ERROR_CIF_NUMBER_NOT_COMPLETED: "CIF number have not completed",

    ERROR_CIF_ID_NOT_EXIST: "CIF id is not exist",
    ERROR_IDENTITY_DOCUMENT_NOT_EXIST: "Identity Document is not exist",
    ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST: 'Sub Identity is not exist',
    ERROR_CAN_NOT_CREATE: 'Can not create',
    ERROR_IMAGE_TYPE_NOT_EXIST: 'Image type is not exist',
    ERROR_SIGNATURE_IS_NULL: "Signature can not be empty",
    ERROR_PHONE_NUMBER: "Phone number only 9 to 10 numbers and start with 0",

    ERROR_RELATIONSHIP_TYPE_ID_NOT_EXIST: "Relationship type does not exist",
    ERROR_RELATION_CUSTOMER_SELF_RELATED: "Customer can not relate to himself/herself",
    ERROR_RELATIONSHIP_EXIST: "guardian/customer relationship existed",
    ERROR_RELATIONSHIP_NOT_GUARDIAN: "Can not be guardian, because cif_number has guardian(s)",
    ERROR_CASA_ACCOUNT_NOT_EXIST: "casa_account not exist",
    ERROR_CUSTOMER_INDIVIDUAL_INFO: "customer_individual_info is not exist",
    ERROR_CUSTOMER_IDENTITY: "customer_identity is not exist",
    ERROR_CUSTOMER_IDENTITY_IMAGE: "customer_identity_image is not exist",
    ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST: "agreement_authorizations is not exist",

    ERROR_INVALID_URL: "url is invalid",
    ERROR_INVALID_NUMBER: "number is invalid",

    ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST: "Identity Document Type Type is not exist",
    ERROR_WRONG_TYPE_IDENTITY: "Identity Document Type Type is wrong",

    ERROR_NOT_NULL: " is not null",
    ERROR_CIF_ID_NOT_CUSTOMER_ADDRESS_EXIST: "CIF_ID is not address",

    ERROR_NO_DATA: "No data"
}
