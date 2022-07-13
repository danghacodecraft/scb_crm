from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.constant.gw import GW_RESPONSE_STATUS_SUCCESS


async def repos_gw_detail_user(current_user, data_input):
    is_success, gw_detail_user = await service_gw.gw_detail_user(
        current_user=current_user.user_info, data_input=data_input
    )
    # check trường hợp lỗi
    detail_user_info = gw_detail_user.get('selectUserInfoByUserID_out')
    if detail_user_info.get('transaction_info').get('transaction_error_code') != GW_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=detail_user_info.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=gw_detail_user)
