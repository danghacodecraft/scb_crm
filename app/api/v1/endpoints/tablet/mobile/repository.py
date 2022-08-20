from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.tablet.model import Tablet
from app.utils.error_messages import ERROR_TABLET_OTP_INVALID
from app.utils.functions import now


@auto_commit
async def repos_pair_by_otp(otp: str, device_information: str, session: Session):
    tablet = session.execute(
        select(
            Tablet
        ).filter(
            Tablet.otp == otp,
            Tablet.expired_at >= now(),
            Tablet.is_paired == 0
        )
    ).scalar()
    if not tablet:
        return ReposReturn(is_error=True, msg=ERROR_TABLET_OTP_INVALID, loc='otp')

    session.execute(
        update(
            Tablet
        ).filter(
            Tablet.id == tablet.id
        ).values(
            is_paired=1,
            device_information=device_information
        )
    )
    session.commit()

    return ReposReturn(data={
        'tablet_id': tablet.id,
        'teller_username': tablet.teller_username,
    })