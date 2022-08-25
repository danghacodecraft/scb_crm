from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm
)
from app.third_parties.oracle.models.template.model import Template
from app.utils.error_messages import (
    ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST, ERROR_BOOKING_ID_NOT_EXIST,
    ERROR_TEMPLATE_NOT_EXIST
)


async def repos_get_template_data(template_id: str, booking_id: str, session: Session):
    booking = session.execute(
        select(Booking).filter(
            Booking.id == booking_id
        )
    ).scalar()

    if not booking:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_ID_NOT_EXIST,
            detail='Can not found booking'
        )

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

    booking_business_forms = session.execute(select(
        BookingBusinessForm
    ).filter(
        BookingBusinessForm.booking_id == booking_id
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

    data_return['booking'] = {"created_at": booking.created_at, "updated_at": booking.updated_at,
                              'created_by': booking.created_by, 'updated_by': booking.updated_by}

    return ReposReturn(data=data_return)
