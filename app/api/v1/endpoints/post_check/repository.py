from typing import Optional

from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.others.booking.repository import generate_booking_code
from app.settings.event import service_ekyc
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm
)
from app.utils.constant.ekyc import BUSINESS_FORM_EKYC
from app.utils.error_messages import (
    ERROR_BOOKING_CODE_EXISTED, ERROR_CALL_SERVICE_EKYC, MESSAGE_STATUS
)
from app.utils.functions import generate_uuid, now, orjson_dumps


async def repos_get_list_kss(
        query_data: dict
) -> ReposReturn:
    is_success, response = await service_ekyc.get_list_kss(
        query_data=query_data
    )
    if not is_success:
        return ReposReturn(is_error=True, loc="LIST KSS", detail=response.get('message'))
    for item in response.get('detail'):
        if item['status'] == "Thành công" and not item['kss_status']:
            item['kss_status'] = "Chờ Hậu Kiểm"
            item['date_kss'] = item['trans_date']

    return ReposReturn(data={
        'detail': response.get('detail'),
        'total_page': response.get('total_page'),
        'total_record': response.get('total_record'),
        'page': response.get('page')
    })


async def repos_get_list_branch(query_param: dict) -> ReposReturn:
    is_success, response = await service_ekyc.get_list_branch(
        query_param=query_param
    )

    return ReposReturn(data=response)


async def repos_get_list_zone() -> ReposReturn:
    is_success, response = await service_ekyc.get_list_zone()

    return ReposReturn(data=response)


async def repos_get_statistics_profiles(query_data) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics_profiles(query_data)

    if not is_success:
        return ReposReturn(is_error=True, loc="STATISTICS PROFILES", detail=response.get('message'))

    return ReposReturn(data=response)


async def repos_get_statistics_month(months: int) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics_months(months=months)
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_EKYC, detail=str(response))

    return ReposReturn(data=response)


async def repos_get_history_post_post_check(postcheck_uuid: str) -> ReposReturn:
    is_success, response = await service_ekyc.get_history_post_check(
        postcheck_uuid=postcheck_uuid
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response.get('message'),
            detail=response.get('message')
        )

    return ReposReturn(data=response)


async def repos_update_post_check(request_data: dict) -> ReposReturn:
    is_success, response = await service_ekyc.update_post_check(request_data=request_data)

    if not is_success:
        return ReposReturn(is_error=True, loc="UPDATE_POST_CHECK", detail=response.get('message'))

    return ReposReturn(data=response)


async def repos_get_statistics(query_param: dict) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics(query_param)

    if not is_success and response['detail']:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response['detail'],
            detail=response['detail']
        )

    return ReposReturn(data=response)


async def repos_get_customer_detail(postcheck_uuid: str) -> ReposReturn:
    is_success, response = await service_ekyc.get_customer_detail(postcheck_uuid=postcheck_uuid)

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response['message'],
            detail=response['message']
        )

    return ReposReturn(data=response)


async def repos_create_post_check(payload_data: dict) -> ReposReturn:
    is_success, response = await service_ekyc.create_post_check(payload_data=payload_data)

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc='CREATE_POST_CHECK',
            msg=ERROR_CALL_SERVICE_EKYC,
            detail=str(response.get('post_control'))
        )

    return ReposReturn(data=response)


async def repos_get_post_control(query_params) -> ReposReturn:
    is_success, response = await service_ekyc.get_post_control(
        query_params=query_params
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response['message'],
            detail=response['message']
        )
    return ReposReturn(data=response)


async def repos_save_customer_ekyc(
        body_request: dict,
        booking_id: Optional[str],

):
    is_success, response = await service_ekyc.save_customer_ekyc(
        body_data=body_request,
        booking_id=booking_id
    )

    return ReposReturn(data=response)


@auto_commit
async def repos_create_booking_kss(
    business_type_code: str,
    payload_data: dict,
    current_user,
    session: Session
):
    booking_id = generate_uuid()
    current_user_branch_code = current_user.hrm_branch_code
    is_existed, booking_code = await generate_booking_code(
        branch_code=current_user_branch_code,
        business_type_code=business_type_code,
        session=session
    )
    if is_existed:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_CODE_EXISTED + f", booking_code: {booking_code}",
            detail=MESSAGE_STATUS[ERROR_BOOKING_CODE_EXISTED]
        )

    session.add_all([
        Booking(
            id=booking_id,
            # TODO hard core transaction ekyc kss
            transaction_id=None,
            code=booking_code,
            business_type_id=business_type_code,
            branch_id=current_user_branch_code,
            created_at=now(),
            updated_at=now()
        ),
        BookingBusinessForm(
            booking_id=booking_id,
            business_form_id=BUSINESS_FORM_EKYC,
            save_flag=False,
            form_data=orjson_dumps(payload_data),
            created_at=now()
        )
    ])

    return ReposReturn(data=(booking_id, booking_code))
