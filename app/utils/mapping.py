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
