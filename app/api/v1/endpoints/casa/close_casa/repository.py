import json

from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_CLOSE_CASA_ACCOUNT
)
from app.utils.functions import now


async def repos_save_casa_account(
        booking_id,
        request_json: json,
        session: Session
) -> ReposReturn:
    session.add(BookingBusinessForm(**dict(
        booking_id=booking_id,
        form_data=request_json,
        business_form_id=PROFILE_HISTORY_DESCRIPTIONS_CLOSE_CASA_ACCOUNT,
        save_flag=True,
        created_at=now()
    )))
    session.flush()

    return ReposReturn(data=None)
