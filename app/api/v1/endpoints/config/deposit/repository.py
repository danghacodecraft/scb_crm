from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.e_banking.model import TdInterestType
from app.utils.constant.gw import (
    GW_FUNC_RETRIEVE_SERIAL_NUMBER_OUT, GW_RESPONSE_STATUS_SUCCESS
)


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

    if acc_type['selectCategory_out']['transaction_info']['transaction_error_code'] == GW_RESPONSE_STATUS_SUCCESS:
        response_data = acc_type['selectCategory_out']['data_output']
    else:
        return ReposReturn(is_error=True,
                           msg=acc_type['selectCategory_out']['transaction_info']['transaction_error_msg'])
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

    if acc_class['selectCategory_out']['transaction_info']['transaction_error_code'] == GW_RESPONSE_STATUS_SUCCESS:
        response_data = acc_class['selectCategory_out']['data_output']
    else:
        return ReposReturn(is_error=True,
                           msg=acc_type['selectCategory_out']['transaction_info']['transaction_error_msg'])

    return ReposReturn(data=response_data)


async def repos_get_account_detail(account_class, current_user):
    transaction_value = [
        {
            "param1": account_class
        }
    ]
    is_success, account_detail = await service_gw.get_select_category(
        current_user=current_user,
        transaction_name="DM_ACCLASS_DETAIL",
        transaction_value=transaction_value
    )
    response_data = account_detail['selectCategory_out']['data_output'][0]
    return ReposReturn(data=response_data)


async def repos_get_serial(serial_prefix, serial_key, current_user):
    data_input = {
        "serial_info": {
            "serial_prefix": serial_prefix,
            "serial_key": serial_key
        },
        "maker_info": {
            "staff_name": current_user.username
        },
        "branch_info": {
            "branch_code": current_user.hrm_branch_code
        }
    }
    is_success, serial = await service_gw.get_select_serial(
        data_input=data_input,
        current_user=current_user,
    )
    serial_out = serial[GW_FUNC_RETRIEVE_SERIAL_NUMBER_OUT]['transaction_info']
    if serial_out['transaction_error_code'] != GW_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=serial_out['transaction_error_msg'], loc="SERIAL")

    response_data = serial[GW_FUNC_RETRIEVE_SERIAL_NUMBER_OUT]['data_output']['serial_info']

    return ReposReturn(data=response_data)
