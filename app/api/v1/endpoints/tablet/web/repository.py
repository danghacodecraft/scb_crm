from datetime import timedelta

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.booking.model import BookingAuthentication
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.tablet.model import Tablet
from app.utils.constant.cif import IMAGE_TYPE_FACE
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


async def repos_get_customer_avatar_url_and_full_name_if_exist_by_booking_authentication_id(
        booking_authentication_id: str, session: Session
):
    customer_id_and_full_name = session.execute(
        select(
            Customer.id,
            Customer.full_name_vn
        ).join(
            BookingAuthentication, and_(BookingAuthentication.cif_number == Customer.cif_number, BookingAuthentication.id == booking_authentication_id)
        )
    ).first()
    if not customer_id_and_full_name:
        return ReposReturn(data={
            "avatar_uuid": None,
            "full_name": None
        })

    avatar_url = session.execute(
        select(
            CustomerIdentityImage.image_url
        )
        .join(CustomerIdentity, CustomerIdentityImage.identity_id == CustomerIdentity.id)
        .join(Customer, CustomerIdentity.customer_id == Customer.id, )
        .filter(
            Customer.id == customer_id_and_full_name[0],
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FACE
        )
    ).scalar()

    return ReposReturn(data={
        "avatar_uuid": avatar_url,
        "full_name": customer_id_and_full_name[1]
    })
