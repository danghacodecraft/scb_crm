import json

from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm
from app.utils.constant.cif import BUSINESS_FORM_PAY_IN_CASH
from app.utils.functions import now


@auto_commit
async def repos_save_pay_in_cash_info(booking_id: str, form_data: json, session: Session):
    session.add(BookingBusinessForm(
        booking_id=booking_id,
        form_data=form_data,
        business_form_id=BUSINESS_FORM_PAY_IN_CASH,
        created_at=now(),
        save_flag=True
    ))
    session.flush()
    return ReposReturn(data=form_data)
