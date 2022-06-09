from typing import List

from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import BookingAccount, Booking
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import AccountStructureType
from app.utils.constant.cif import ACTIVE_FLAG_ACTIVED
from app.utils.error_messages import ERROR_CIF_NUMBER_NOT_EXIST, ERROR_IDS_NOT_EXIST
from app.utils.functions import get_index_positions


@auto_commit
async def repos_save_casa_casa_account(
        saving_casa_accounts: List[dict],
        saving_bookings: List[dict],
        saving_booking_accounts: List[dict],
        booking_parent_id: str,
        session: Session
):
    account_ids = session.execute(
        select(
            BookingAccount.account_id
        )
        .filter(BookingAccount.booking_id == booking_parent_id)
    ).scalars().all()

    booking_ids = session.execute(
        select(
            BookingAccount.booking_id
        )
        .filter(BookingAccount.booking_id == booking_parent_id)
    ).scalars().all()

    session.execute(delete(Booking).filter(Booking.id.in_(booking_ids)))
    session.execute(delete(CasaAccount).filter(CasaAccount.id.in_(account_ids)))
    session.execute(delete(BookingAccount).filter(BookingAccount.account_id.in_(booking_ids)))

    session.bulk_save_objects([CasaAccount(**saving_casa_account) for saving_casa_account in saving_casa_accounts])
    session.bulk_save_objects([Booking(**saving_booking) for saving_booking in saving_bookings])
    session.bulk_save_objects([BookingAccount(**saving_booking_account) for saving_booking_account in saving_booking_accounts])

    return ReposReturn(data=(saving_casa_accounts, saving_booking_accounts))


########################################################################################################################
# Others
########################################################################################################################
async def repos_get_customer_by_cif_number(
        cif_number: str, session: Session
) -> ReposReturn:
    """
    Lấy dữ liệu customer theo số cif_number
    """
    customers = session.execute(
        select(
            Customer
        )
        # .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        # .join(AddressCountry, Customer.nationality_id == AddressCountry.id)
        # .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        # .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        # .join(
        #     CustomerIdentityType,
        #     CustomerIdentity.identity_type_id == CustomerIdentityType.id,
        # )
        # .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        # .join(
        #     CustomerPersonalRelationship,
        #     Customer.id == CustomerPersonalRelationship.customer_id,
        # )
        # .join(
        #     CustomerRelationshipType,
        #     CustomerRelationshipType.id
        #     == CustomerPersonalRelationship.customer_relationship_type_id,
        # )
        # .join(
        #     CustomerIdentityImage,
        #     and_(
        #         CustomerIdentity.id == CustomerIdentityImage.identity_id,
        #         CustomerIdentityImage.image_type_id == IMAGE_TYPE_SIGNATURE,
        #     ),
        # )
        .filter(Customer.cif_number == cif_number)
    ).scalar()

    if not customers:
        return ReposReturn(
            is_error=True, msg=ERROR_CIF_NUMBER_NOT_EXIST, loc="cif_number"
        )

    return ReposReturn(data=customers)


async def repos_get_acc_structure_types(acc_structure_type_ids: List[str], level: int, session: Session):
    unique_acc_structure_type_ids = set(acc_structure_type_ids)

    acc_structure_types = session.execute(
        select(
            AccountStructureType
        ).filter(and_(
            AccountStructureType.level == level,
            AccountStructureType.id.in_(unique_acc_structure_type_ids),
            AccountStructureType.active_flag == ACTIVE_FLAG_ACTIVED
        ))
    ).scalars().all()

    if len(acc_structure_types) != len(unique_acc_structure_type_ids):
        acc_structure_types = {acc_structure_type.id for acc_structure_type in acc_structure_types}

        remaining_elements = unique_acc_structure_type_ids - unique_acc_structure_type_ids.intersection(set(acc_structure_types))

        loc_errors = [dict(
            item_value=element,
            indexs=get_index_positions(acc_structure_type_ids, element),
        ) for element in remaining_elements]

        return ReposReturn(
            is_error=True, msg=ERROR_IDS_NOT_EXIST,
            loc=f'acc_structure_type_ids: {loc_errors}'
        )

    return ReposReturn(data=acc_structure_types)


async def repos_get_casa_open_casa_info(booking_parent_id: str, session: Session):
    booking_parent = aliased(Booking, name="BookingParent")
    get_casa_open_casa_info = session.execute(
        select(
            booking_parent,
            Booking,
            BookingAccount,
            CasaAccount,
            AccountStructureType  # Level 1
        )
        .join(Booking, booking_parent.id == Booking.parent_id)
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(CasaAccount, BookingAccount.account_id == CasaAccount.id)
        .join(AccountStructureType, CasaAccount.acc_structure_type_id == AccountStructureType.parent_id)
        .filter(booking_parent.id == booking_parent_id)
        .distinct()
    ).all()
    return ReposReturn(data=get_casa_open_casa_info)
