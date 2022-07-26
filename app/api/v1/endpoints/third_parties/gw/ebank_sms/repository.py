from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_select_mobile_number_sms_by_account_casa(
        ebank_sms_indentify_num,
        current_user
):
    current_user = current_user.user_info
    is_success, select_mobile_number_sms_by_account_casa = await service_gw.select_mobile_number_sms_by_account_casa(
        current_user=current_user, ebank_sms_indentify_num=ebank_sms_indentify_num
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_select_mobile_number_sms_by_account_casa",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(select_mobile_number_sms_by_account_casa)
        )

    return ReposReturn(data=select_mobile_number_sms_by_account_casa)


async def repos_gw_get_select_account_td_by_mobile_num(
        ebank_sms_indentify_num,
        current_user
):
    current_user = current_user.user_info
    is_success, select_account_td_by_mobile_num = await service_gw.select_account_td_by_mobile_num(
        current_user=current_user, ebank_sms_indentify_num=ebank_sms_indentify_num
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_select_account_td_by_mobile_num",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(select_account_td_by_mobile_num)
        )

    return ReposReturn(data=select_account_td_by_mobile_num)


async def repos_gw_register_sms_service_by_account_casa(
        account_info,
        ebank_sms_info_list,
        staff_info_checker,
        staff_info_maker,
        current_user
):
    current_user = current_user.user_info
    is_success, register_sms_service_by_account_casa = await service_gw.register_sms_service_by_account_casa(
        current_user=current_user,
        account_info=account_info,
        ebank_sms_info_list=ebank_sms_info_list,
        staff_info_checker=staff_info_checker,
        staff_info_maker=staff_info_maker
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="register_sms_service_by_account_casa",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(register_sms_service_by_account_casa)
        )

    return ReposReturn(data=register_sms_service_by_account_casa)
