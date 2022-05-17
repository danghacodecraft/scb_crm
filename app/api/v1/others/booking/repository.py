from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.functions import count

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.third_parties.oracle.models.cif.form.model import Booking
from app.utils.error_messages import ERROR_BOOKING_CODE_EXISTED, MESSAGE_STATUS
from app.utils.functions import (
    date_to_datetime, datetime_to_string, end_time_of_day, generate_uuid, now,
    today
)


async def generate_booking_code(
    branch_code: str,
    business_type_code: str,
    session: Session
):
    datetime_today = date_to_datetime(today())
    sequence = session.execute(
        select(
            count(Booking.id)
        )
        .filter(and_(
            Booking.created_at >= datetime_today,
            Booking.created_at < end_time_of_day(datetime_today)
        ))
    ).scalar()

    date_code = datetime_to_string(datetime_today, _format='%Y%m%d')
    sequence_code = '{:07d}'.format(sequence + 1)
    booking_code = f'{branch_code}_CRM_{business_type_code}_{date_code}_{sequence_code}'
    is_existed = session.execute(select(Booking).filter(Booking.code == booking_code)).scalar() is not None
    return is_existed, booking_code


async def repos_create_booking(
    transaction_id: Optional[str],
    business_type_code: str,
    session: Session,
    current_user: UserInfoResponse,
    booking_code_flag: bool = False
):
    booking_id = generate_uuid()
    current_user_branch_code = current_user.hrm_branch_code
    booking_code = None
    if booking_code_flag:
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
    session.add(
        Booking(
            id=booking_id,
            transaction_id=transaction_id,
            code=booking_code,
            business_type_id=business_type_code,
            branch_id=current_user_branch_code,
            created_at=now(),
            updated_at=now()
        )
    )
    session.commit()
    return ReposReturn(data=(booking_id, booking_code))
