from app.api.base.repository import ReposReturn
from app.settings.event import service_gw


async def repos_gw_payment_amount_block(current_user, data_input):

    is_success, gw_payment_amount_block = await service_gw.gw_payment_amount_block(
        current_user=current_user.user_info, data_input=data_input
    )
    return ReposReturn(data=gw_payment_amount_block)
