import json

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm
from app.utils.constant.cif import BUSINESS_FORM_CASA_TOP_UP
from app.utils.functions import now


# @auto_commit
async def repos_save_casa_top_up_info(booking_id: str, form_data: json, session: Session):
    session.add(BookingBusinessForm(
        booking_id=booking_id,
        form_data=form_data,
        business_form_id=BUSINESS_FORM_CASA_TOP_UP,
        created_at=now(),
        save_flag=True
    ))
    return ReposReturn(data=form_data)


async def repos_get_casa_top_up_info(booking_id: str, session: Session):
    get_casa_top_up_info = session.execute(
        select(
            BookingBusinessForm
        )
        .filter(BookingBusinessForm.booking_id == booking_id)
        .order_by(desc(BookingBusinessForm.created_at))
    ).scalars().first()
    return ReposReturn(data=get_casa_top_up_info)
