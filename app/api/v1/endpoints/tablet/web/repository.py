from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.tablet.model import Tablet
from app.utils.constant.tablet import (
    MAX_RETRY_GENERATE_NEW_OTP, OTP_EXPIRED_AFTER_IN_SECONDS
)
from app.utils.functions import now
from app.utils.tablet_functions import generate_otp


@auto_commit
async def repos_create_tablet_otp(teller_username: str, session: Session):
    session.execute(
        delete(
            Tablet
        ).filter(
            Tablet.teller_username == teller_username
        )
    )
    session.flush()

    otp = None
    is_exist_otp = False
    for _ in range(MAX_RETRY_GENERATE_NEW_OTP):
        otp = generate_otp()

        if not session.execute(
            select(
                Tablet.id
            ).filter(
                Tablet.otp == otp
            )
        ).scalar():
            is_exist_otp = False
            break
        else:
            is_exist_otp = True

    if is_exist_otp:
        return ReposReturn(is_error=True, msg='ERROR_GENERATE_OTP', detail='Can not generate new OTP', loc='otp')

    created_at = now()
    expired_at = created_at + timedelta(seconds=OTP_EXPIRED_AFTER_IN_SECONDS)

    tablet = Tablet(
        teller_username=teller_username,
        otp=otp,
        created_at=created_at,
        expired_at=expired_at,
        device_information='',
        is_paired=0
    )
    session.add(tablet)
    session.flush()

    return ReposReturn(data={
        'tablet_id': tablet.id,
        'otp': otp,
        'expired_after_in_seconds': OTP_EXPIRED_AFTER_IN_SECONDS,
        'expired_at': expired_at,
    })


async def repos_retrieve_tablet(teller_username: str, session: Session):
    tablet = session.execute(
        select(
            Tablet
        ).filter(
            Tablet.teller_username == teller_username
        )
    ).scalar()
    return ReposReturn(data={
        'tablet_id': tablet.id if tablet else None,
        'otp': tablet.otp if tablet else None,
        'is_paired': tablet.is_paired if tablet else None
    })


async def repos_delete_tablet_if_exists(teller_username: str, session: Session):
    session.execute(
        delete(
            Tablet
        ).filter(
            Tablet.teller_username == teller_username
        )
    )
    session.commit()

    return ReposReturn(data=True)
