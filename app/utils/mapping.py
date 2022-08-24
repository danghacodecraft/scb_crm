from app.utils.constant.debit_card import (
    IDENTITY_DOCUMENT_TYPE_NEW_IC, IDENTITY_DOCUMENT_TYPE_PASSPORT,
    IDENTITY_DOCUMENT_TYPE_PASSPORT_CODE, MARITAL_STATUS_DISVORSED,
    MARITAL_STATUS_MARRIED, MARITAL_STATUS_OTHERS, MARITAL_STATUS_SINGLE,
    RESIDENT
)
from app.utils.constant.gw import GW_DEFAULT_NO, GW_DEFAULT_YES


########################################################################################################################
# EBANK
########################################################################################################################
def mapping_authentication_code_core_to_crm(core_data: str) -> str:
    if core_data == "XACTHUC_SMS":
        return "SMS"
    elif core_data == "XACTHUC_SOFTTOKEN":
        return "SOFT_TOKEN"


def mapping_authentication_code_crm_to_core(crm_data: str) -> str:
    if crm_data == "SMS":
        return "OTP"
    elif crm_data == "SOFT_TOKEN":
        return "S_TOKEN"
    else:
        return ""


########################################################################################################################
# DEBIT CARD
########################################################################################################################
def mapping_marital_status_crm_to_core(crm_data: str) -> str:
    if crm_data not in [MARITAL_STATUS_SINGLE, MARITAL_STATUS_MARRIED, MARITAL_STATUS_DISVORSED]:
        return MARITAL_STATUS_OTHERS
    else:
        return crm_data


def mapping_identity_code_crm_to_core(crm_data: str) -> str:
    if crm_data == IDENTITY_DOCUMENT_TYPE_PASSPORT_CODE:
        return IDENTITY_DOCUMENT_TYPE_PASSPORT
    else:
        return IDENTITY_DOCUMENT_TYPE_NEW_IC


def mapping_resident_pr_stat_crm_to_core(crm_data: str) -> str:
    if crm_data == RESIDENT:
        return GW_DEFAULT_YES
    else:
        return GW_DEFAULT_NO
