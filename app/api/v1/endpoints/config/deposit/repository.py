from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.e_banking.model import TdInterestType
from app.utils.constant.gw import GW_CASA_RESPONSE_STATUS_SUCCESS


async def repos_get_interest_type_by_id(
        interest_type_id: str,
        session: Session
):
    response_data = session.execute(
        select(
            TdInterestType.name
        ).filter(TdInterestType.id == interest_type_id)
    ).scalar()

    return ReposReturn(data=response_data)


async def repos_get_acc_type(
        current_user
):
    transaction_value = [
        {
            "param1": "Có kỳ hạn",
            "param2": "Tiết kiệm CKH"
        }
    ]

    is_success, acc_type = await service_gw.get_select_category(
        current_user=current_user,
        transaction_name="DM_SP03",
        transaction_value=transaction_value
    )

    if acc_type['selectCategory_out']['transaction_info']['transaction_error_code'] == GW_CASA_RESPONSE_STATUS_SUCCESS:
        response_data = acc_type['selectCategory_out']['data_output']
    else:
        return ReposReturn(is_error=True, msg=acc_type['selectCategory_out']['transaction_info']['transaction_error_msg'])
    return ReposReturn(data=response_data)


async def repos_get_acc_class(
        current_user,
        interest,
        acc_type,
        currency_id
):
    transaction_value = [
        {
            "param1": "Có kỳ hạn",
            "param2": "Tiết kiệm CKH",
            "param3": acc_type,
            "param4": interest,
            "param5": currency_id
        }
    ]

    is_success, acc_class = await service_gw.get_select_category(
        current_user=current_user,
        transaction_name="DM_SP04_LS",
        transaction_value=transaction_value
    )

    if acc_class['selectCategory_out']['transaction_info']['transaction_error_code'] == GW_CASA_RESPONSE_STATUS_SUCCESS:
        response_data = acc_class['selectCategory_out']['data_output']
    else:
        return ReposReturn(is_error=True, msg=acc_type['selectCategory_out']['transaction_info']['transaction_error_msg'])

    return ReposReturn(data=response_data)
