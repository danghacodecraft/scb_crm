from sqlalchemy import select, update
from sqlalchemy.orm import Session
from starlette import status

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.booking.model import BookingAuthentication
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


async def repos_retrieve_table_by_tablet_token(tablet_id: str, otp: str, session: Session) -> ReposReturn:
    tablet = session.execute(
        select(
            Tablet
        ).filter(
            Tablet.id == tablet_id,
            Tablet.otp == otp,
            Tablet.is_paired == 1
        )
    ).scalar()
    if not tablet:
        return ReposReturn(is_error=True, msg=ERROR_TABLET_OTP_INVALID, loc='token',
                           error_status_code=status.HTTP_401_UNAUTHORIZED)

    return ReposReturn(data={
        'tablet_id': tablet.id,
        'teller_username': tablet.teller_username,
        'otp': tablet.otp
    })


async def repos_init_booking_authentication(tablet_id: str, teller_username: str, identity_number: str, cif_number: str,
                                            session: Session) -> ReposReturn:
    session.add(
        BookingAuthentication(
            tablet_id=tablet_id,
            teller_username=teller_username,
            identity_number=identity_number,
            created_at=now(),
            cif_number=cif_number
        )
    )
    session.commit()

    return ReposReturn(data=True)
