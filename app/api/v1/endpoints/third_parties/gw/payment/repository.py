from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.constant.gw import GW_CASA_REPONSE_STATUS_SUCCESS


async def repos_gw_payment_amount_block(current_user, data_input):

    is_success, gw_payment_amount_block = await service_gw.gw_payment_amount_block(
        current_user=current_user.user_info, data_input=data_input
    )
    amount_block_out = gw_payment_amount_block.get('amountBlock_out', {})

    # check trường hợp lỗi
    if gw_payment_amount_block.get('transaction_info').get('transaction_error_code') != GW_CASA_REPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=amount_block_out.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=gw_payment_amount_block)


async def repos_gw_payment_amount_unblock(current_user, data_input):

    is_success, gw_payment_amount_unblock = await service_gw.gw_payment_amount_unblock(
        data_input=data_input,
        current_user=current_user.user_info
    )
    amount_unblock_out = gw_payment_amount_unblock.get('amountUnBlock_out', {})

    # check trường hợp lỗi
    if amount_unblock_out.get('transaction_info').get('transaction_error_code') != GW_CASA_REPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=amount_unblock_out.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=gw_payment_amount_unblock)
