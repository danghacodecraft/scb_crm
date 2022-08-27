from typing import Any, Union

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_tms
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm
)
from app.third_parties.oracle.models.master_data.others import BusinessType
from app.third_parties.oracle.models.template.model import Template
from app.utils.error_messages import (
    ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST, ERROR_BOOKING_ID_NOT_EXIST,
    ERROR_CALL_SERVICE_TEMPLATE, ERROR_TEMPLATE_NOT_EXIST
)


async def repos_check_exist_and_get_info_template_booking(
        template_id: Union[str, None],
        booking_id: str,
        session: Session,

) -> Union[dict, Any]:

    print("da vaa ", template_id, booking_id)
    booking = session.execute(
        select(Booking).filter(
            Booking.id == booking_id
        )
    ).scalar()
    print("da vaa 2222")
    if not booking:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_ID_NOT_EXIST,
            detail='Can not found booking'
        )
    print(template_id)
    if not template_id:
        print("hahahah")
        template_info = None
    else:
        print("voooooooooooo")
        template_info = session.execute(
            select(Template).filter(
                Template.template_id == template_id,
                Template.business_type_id == booking.business_type_id
            )
        ).scalar()

        if not template_info:
            return ReposReturn(
                is_error=True,
                msg=ERROR_TEMPLATE_NOT_EXIST,
                detail='Can not found template'
            )
    print({'template_info': template_info, "booking_info": booking})
    return ReposReturn(data={'template_info': template_info, "booking_info": booking})


async def repos_get_template_data(booking, session: Session):
    booking_business_forms = session.execute(select(
        BookingBusinessForm
    ).filter(
        BookingBusinessForm.booking_id == booking.id
    ).order_by(
        desc(BookingBusinessForm.business_form_id),
        desc(BookingBusinessForm.created_at)

    )).scalars().all()

    if not booking_business_forms:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST,
            detail='Can not found booking business form'
        )
    data_return = {}
    for booking_business_form in booking_business_forms:
        if booking_business_form.business_form_id not in data_return:
            data_return[booking_business_form.business_form_id] = booking_business_form.form_data

    data_return['booking'] = {
        "business_type_id": booking.business_type_id,
        "created_at_datetime": booking.created_at,
        "updated_at_datetime": booking.updated_at,
        "created_at_date": booking.created_at,
        "updated_at_date": booking.updated_at,
        # "created_at_time": booking.created_at,
        # "updated_at_time": booking.updated_at,
        'created_by': booking.created_by,
        'updated_by': booking.updated_by if booking.updated_by else booking.created_by,
    }

    return ReposReturn(data=data_return)


async def repo_form(template_id: str, booking_id: str, path: str) -> ReposReturn:
    body = {
        "parameter_values": {
            "str_id": template_id,
            "str_booking_id": booking_id
        },
        "data_fill": {}
    }

    is_success, response = await service_tms.fill_form(body=body, path=path)

    if not is_success:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_TEMPLATE,
            detail=str(response['message'])
        )

    return ReposReturn(data=response)


async def repos_get_all_template_of_booking(business_type_id: str, session: Session) -> ReposReturn:
    templates = session.execute(
        select(
            Template,
            BusinessType
        ).join(
            BusinessType, Template.business_type_id == BusinessType.code
        ).filter(
            Template.business_type_id == business_type_id
        )
    ).all()
    print(templates)
    return ReposReturn(data=templates)
