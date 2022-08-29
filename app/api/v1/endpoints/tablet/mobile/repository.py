from sqlalchemy import desc, select, update
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


async def repos_init_booking_authentication(
        tablet_id: str, teller_username: str, identity_number: str, cif_number: str,
        session: Session,
        identity_front_document_file_uuid: str = None, identity_front_document_file_uuid_ekyc: str = None,
        face_file_uuid: str = None, face_file_uuid_ekyc: str = None, booking_id: str = None
) -> ReposReturn:
    session.add(
        BookingAuthentication(
            tablet_id=tablet_id,
            teller_username=teller_username,
            identity_number=identity_number,
            created_at=now(),
            cif_number=cif_number,
            identity_front_document_file_uuid=identity_front_document_file_uuid,
            identity_front_document_file_uuid_ekyc=identity_front_document_file_uuid_ekyc,
            face_file_uuid=face_file_uuid,
            face_file_uuid_ekyc=face_file_uuid_ekyc,
            booking_id=booking_id,
        )
    )
    session.commit()

    return ReposReturn(data=True)


async def repos_retrieve_current_booking_authentication_by_tablet_id(tablet_id: str, session: Session) -> ReposReturn:
    booking_authentication = session.execute(
        select(
            BookingAuthentication
        ).filter(
            BookingAuthentication.tablet_id == tablet_id
        ).order_by(desc(BookingAuthentication.created_at))
    ).scalars().first()
    if not booking_authentication:
        return ReposReturn(is_error=True, msg='INVALID_TABLET_ID', detail='Can not found booking authentication',
                           loc='token', error_status_code=status.HTTP_401_UNAUTHORIZED)

    return ReposReturn(data=booking_authentication)


async def repos_update_current_booking_authentication_by_tablet_id(
        need_to_update_booking_authentication: BookingAuthentication,
        session: Session
) -> ReposReturn:
    session.execute(
        update(
            BookingAuthentication
        ).filter(
            BookingAuthentication.id == need_to_update_booking_authentication.id
        ).values(
            identity_front_document_file_uuid=need_to_update_booking_authentication.identity_front_document_file_uuid,
            identity_front_document_file_uuid_ekyc=need_to_update_booking_authentication.identity_front_document_file_uuid_ekyc,
            face_file_uuid=need_to_update_booking_authentication.face_file_uuid,
            face_file_uuid_ekyc=need_to_update_booking_authentication.face_file_uuid_ekyc,
            booking_id=need_to_update_booking_authentication.booking_id
        )
    )
    session.commit()

    return ReposReturn(data=True)
