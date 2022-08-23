from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_select_fee_by_product_name(
        current_user: AuthResponse, product_name: str, trans_amount: int, account_num: str
):
    is_success, fee_info = await service_gw.select_fee_by_product_name(
        current_user=current_user.user_info, product_name=product_name, trans_amount=trans_amount, account_num=account_num
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="select_fee_by_product_name",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(fee_info)
        )

    return ReposReturn(data=fee_info)
