from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_customer_info_list(
        cif_number: str,
        identity_number: str,
        mobile_number: str,
        full_name: str,
        current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, customer_infos = await service_gw.get_customer_info_list(
        cif_number=cif_number,
        identity_number=identity_number,
        mobile_number=mobile_number,
        full_name=full_name,
        current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_customer_info_list",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(customer_infos)
        )

    return ReposReturn(data=customer_infos)


async def repos_get_customer_ids_from_cif_numbers(cif_numbers: List, session: Session):
    customer_ids = session.execute(
        select(
            Customer.id,
            Customer.cif_number
        ).filter(
            Customer.cif_number.in_(cif_numbers)
        )
    ).all()

    return ReposReturn(data=customer_ids)


async def repos_gw_get_customer_info_detail(
        cif_number: str, current_user: AuthResponse,
        loc: str = "get_customer_info_detail"
):
    is_success, customer_info = await service_gw.get_customer_info_detail(
        customer_cif_number=cif_number, current_user=current_user.user_info
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=loc,
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(customer_info)
        )

    return ReposReturn(data=customer_info)


async def repos_gw_get_co_owner(
        account_number: str, current_user
):
    current_user = current_user.user_info
    is_success, co_owner = await service_gw.get_co_owner(
        account_number=account_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_co_owner_list",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(co_owner)
        )

    return ReposReturn(data=co_owner)


async def repos_gw_get_authorized(
        account_number: str, current_user
):
    current_user = current_user.user_info
    is_success, authorized = await service_gw.get_authorized(
        account_number=account_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_authorized_list",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(authorized)
        )

    return ReposReturn(data=authorized)
