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
