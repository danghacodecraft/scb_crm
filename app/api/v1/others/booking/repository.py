from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.functions import count

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, BookingCustomer
)
from app.utils.constant.cif import BUSINESS_FORM_TTCN_GTDD_GTDD
from app.utils.error_messages import ERROR_BOOKING_CODE_EXISTED, MESSAGE_STATUS, ERROR_BOOKING_ID_NOT_EXIST, \
    ERROR_CUSTOMER_NOT_EXIST
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
    booking_code_flag: bool = True
):
    """
    Input:
        booking_code_flag: cần trả ra booking code thì truyền vào
    """
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
    session.add_all([
        Booking(
            id=booking_id,
            transaction_id=transaction_id,
            code=booking_code,
            business_type_id=business_type_code,
            branch_id=current_user_branch_code,
            created_at=now(),
            updated_at=now()
        ),
        BookingBusinessForm(
            booking_id=booking_id,
            business_form_id=BUSINESS_FORM_TTCN_GTDD_GTDD,
            save_flag=False,
            created_at=now()
        )
    ])
    session.commit()
    return ReposReturn(data=(booking_id, booking_code))


async def repos_update_booking(
    booking_id: str,
    transaction_id: Optional[str],
    business_type_code: str,
    session: Session,
    current_user: UserInfoResponse,
    booking_code_flag: bool = False
):
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

    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(
            transaction_id=transaction_id,
            # code=booking_code,
            business_type_id=business_type_code,
            branch_id=current_user_branch_code,
            updated_at=now()
        )
    )
    return ReposReturn(data=(booking_id, booking_code))


async def repos_check_exist_booking(
        booking_id: str,
        session: Session
):

    booking = session.execute(
        select(
            Booking
        )
        .filter(Booking.id == booking_id)
    ).scalar()

    return ReposReturn(data=booking)


async def repos_get_customer_by_booking_id(booking_id: str, cif_number: Optional[str], session: Session):
    booking = session.execute(
        select(
            Booking
        )
        .filter(Booking.id == booking_id)
    ).scalar()
    if not booking:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_ID_NOT_EXIST, loc=f"booking_id: {booking_id}")

    # if booking.business_type.id == BUSINESS_TYPE_CODE_CIF:
    #     customer = session.execute(
    #         select(
    #             Customer,
    #             Booking,
    #             BookingCustomer
    #         )
    #         .join(BookingCustomer, Booking.id == BookingCustomer.booking_id)
    #         .join(Customer, BookingCustomer.customer_id == Customer.id)
    #         .filter(Booking.id == booking_id)
    #     ).scalar()
    #
    # if booking.business_type.id == BUSINESS_TYPE_CODE_OPEN_CASA:
    #     customer = session.execute(
    #         select(
    #             Customer,
    #             Booking,
    #             BookingAccount,
    #             CasaAccount
    #         )
    #         .join(BookingAccount, Booking.id == BookingAccount.booking_id)
    #         .join(CasaAccount, BookingAccount.account_id == CasaAccount.id)
    #         .join(Customer, CasaAccount.customer_id == Customer.id)
    #         .filter(Booking.parent_id == booking_id)
    #     ).scalars().first()

    customer = session.execute(
        select(
            Customer
        )
        .filter(Customer.cif_number == cif_number)
    ).scalar()

    if not customer:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CUSTOMER_NOT_EXIST,
            loc=f"booking_id: {booking_id}, cif_number: {cif_number}"
        )

    return ReposReturn(data=customer)


async def repos_get_business_type(booking_id: str, session: Session):
    booking = session.execute(
        select(
            Booking
        )
        .filter(Booking.id == booking_id)
    ).scalar()
    if not booking:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_ID_NOT_EXIST, loc=f"booking_id: {booking_id}")
    return ReposReturn(data=booking.business_type)


########################################################################################################################
# Not Repos Type
########################################################################################################################
async def repos_is_correct_booking(
        booking_id: str,
        cif_id: str,
        session: Session
):
    booking_customer = session.execute(
        select(
            BookingCustomer
        )
        .filter(and_(
            BookingCustomer.customer_id == cif_id,
            BookingCustomer.booking_id == booking_id
        ))
    ).scalar()

    return True if booking_customer else None


async def repos_is_used_booking(
        booking_id: str,
        session: Session
):
    is_used_booking = session.execute(
        select(
            BookingCustomer
        )
        .filter(BookingCustomer.booking_id == booking_id)
    ).scalar()
    return True if is_used_booking else False
