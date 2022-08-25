from typing import List

from sqlalchemy import and_, select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm, TransactionDaily,
    TransactionSender
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import (
    AccountStructureType
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.others import (
    Currency, SlaTransaction, TransactionJob, TransactionStage,
    TransactionStageLane, TransactionStagePhase, TransactionStageRole,
    TransactionStageStatus
)
from app.utils.constant.cif import ACTIVE_FLAG_ACTIVED
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_IDS_NOT_EXIST
)
from app.utils.functions import get_index_positions


@auto_commit
async def repos_save_casa_casa_account(
        saving_casa_accounts: List[dict],
        saving_bookings: List[dict],
        saving_booking_accounts: List[dict],
        booking_parent_id: str,
        saving_transaction_stage_status: dict,
        saving_sla_transaction: dict,
        saving_transaction_stage: dict,
        saving_transaction_stage_phase: dict,
        saving_transaction_stage_lane: dict,
        saving_transaction_stage_role: dict,
        saving_transaction_daily: dict,
        saving_transaction_sender: dict,
        saving_transaction_job: dict,
        saving_booking_business_form: dict,
        saving_booking_child_business_forms: List[dict],
        session: Session
):
    # Cập nhật lại bằng dữ liệu mới
    session.bulk_save_objects([Booking(**saving_booking) for saving_booking in saving_bookings])
    session.bulk_save_objects([BookingAccount(**saving_booking_account) for saving_booking_account in saving_booking_accounts])
    session.bulk_save_objects([BookingBusinessForm(
        **saving_booking_child_business_form
    ) for saving_booking_child_business_form in saving_booking_child_business_forms
    ])

    # Lưu log vào DB
    session.add_all([
        # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSINESS_FORM
        TransactionStageStatus(**saving_transaction_stage_status),
        SlaTransaction(**saving_sla_transaction),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        BookingBusinessForm(**saving_booking_business_form),
        TransactionJob(**saving_transaction_job)
    ])

    # Update Booking
    session.execute(
        update(
            Booking
        )
        .filter(Booking.id == booking_parent_id)
        .values(
            transaction_id=saving_transaction_daily['transaction_id']
        )
    )

    return ReposReturn(data=(saving_casa_accounts, saving_booking_accounts))


########################################################################################################################
# Others
########################################################################################################################
async def repos_get_customer_by_cif_number(
        cif_number: str, session: Session
) -> ReposReturn:
    customers = session.execute(
        select(
            Customer
        )
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
            AccountStructureType,  # Level 1
            Currency,
            AddressCountry.code,
            AddressCountry.name
        )
        .join(Booking, booking_parent.id == Booking.parent_id)
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(CasaAccount, BookingAccount.account_id == CasaAccount.id)
        .join(Currency, CasaAccount.currency_id == Currency.id)
        .outerjoin(AccountStructureType, CasaAccount.acc_structure_type_id == AccountStructureType.parent_id)
        .outerjoin(AddressCountry, Currency.country_code == AddressCountry.id)
        .filter(booking_parent.id == booking_parent_id)
        .distinct()
    ).all()
    return ReposReturn(data=get_casa_open_casa_info)


async def repos_get_casa_open_casa_info_from_booking(booking_id: str, session: Session):
    get_casa_open_casa_info = session.execute(
        select(
            Booking,
            BookingAccount,
            BookingBusinessForm
        )
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(BookingBusinessForm, and_(
            BookingAccount.booking_id == BookingBusinessForm.booking_id,
            BookingBusinessForm.is_success is not True
        ))
        .filter(Booking.parent_id == booking_id)
        .order_by(BookingBusinessForm.created_at.desc())
    ).all()
    return ReposReturn(data=get_casa_open_casa_info)


async def repos_get_acc_structure_type_by_parent(acc_structure_type_id: str, session: Session):
    """
    Tìm kiến trúc cấp trước đó của tài khoản
    VD: input Cấp 2 -> truyền vào cấp 1
    """
    acc_structure_type_parent = aliased(AccountStructureType, name='AccountStructureTypeParent')
    acc_structure_type = session.execute(
        select(
            acc_structure_type_parent,
            AccountStructureType
        )
        .join(acc_structure_type_parent, AccountStructureType.parent_id == acc_structure_type_parent.id)
        .filter(AccountStructureType.id == acc_structure_type_id)
    ).scalar()
    return ReposReturn(data=acc_structure_type)
