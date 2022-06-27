import json
from typing import List

from sqlalchemy import select, and_, delete, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import BookingAccount, Booking, BookingBusinessForm, \
    TransactionDaily, TransactionSender
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import AccountStructureType
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.others import TransactionStageStatus, TransactionStage, \
    TransactionStageLane, TransactionStagePhase, TransactionStageRole, TransactionJob, SlaTransaction, Currency
from app.utils.constant.approval import BUSINESS_JOB_CODE_START_CASA
from app.utils.constant.casa import CASA_ACCOUNT_STATUS_APPROVED
from app.utils.constant.cif import ACTIVE_FLAG_ACTIVED, BUSINESS_FORM_OPEN_CASA_OPEN_CASA
from app.utils.error_messages import ERROR_CIF_NUMBER_NOT_EXIST, ERROR_IDS_NOT_EXIST
from app.utils.functions import get_index_positions, now, generate_uuid


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
        request_json: json,
        history_datas: json,
        session: Session
):
    # Lấy Những Account có thể xóa được
    deletable_datas = session.execute(
        select(
            CasaAccount,
            Booking,
            BookingAccount
        )
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(CasaAccount, and_(
            BookingAccount.account_id == CasaAccount.id,
            CasaAccount.approve_status != CASA_ACCOUNT_STATUS_APPROVED
        ))
        .filter(Booking.parent_id == booking_parent_id)
    ).all()

    deletable_casa_account_ids = []
    deletable_booking_ids = []
    for casa_account, booking, _ in deletable_datas:
        deletable_casa_account_ids.append(casa_account.id)
        deletable_booking_ids.append(booking.id)

    deletable_casa_account_ids = tuple(deletable_casa_account_ids)
    deletable_booking_ids = tuple(deletable_booking_ids)
    # Xóa dữ liệu cũ, những tài khoản phê duyệt rồi thì giữ lại
    session.execute(delete(BookingAccount).filter(BookingAccount.booking_id.in_(deletable_booking_ids)))
    session.execute(delete(Booking).filter(Booking.id.in_(deletable_booking_ids)))
    session.execute(delete(CasaAccount).filter(CasaAccount.id.in_(deletable_casa_account_ids)))

    # Cập nhật lại bằng dữ liệu mới
    session.bulk_save_objects([CasaAccount(**saving_casa_account) for saving_casa_account in saving_casa_accounts])
    session.bulk_save_objects([Booking(**saving_booking) for saving_booking in saving_bookings])
    session.bulk_save_objects([BookingAccount(**saving_booking_account) for saving_booking_account in saving_booking_accounts])

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
        BookingBusinessForm(**dict(
            booking_id=booking_parent_id,
            form_data=request_json,
            business_form_id=BUSINESS_FORM_OPEN_CASA_OPEN_CASA,
            save_flag=True,
            created_at=now(),
            log_data=history_datas
        )),
        TransactionJob(**dict(
            transaction_id=generate_uuid(),
            booking_id=booking_parent_id,
            business_job_id=BUSINESS_JOB_CODE_START_CASA,
            complete_flag=True,
            error_code=None,
            error_desc=None,
            created_at=now()
        ))
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
            AccountStructureType,  # Level 1
            Currency,
            AddressCountry
        )
        .join(Booking, booking_parent.id == Booking.parent_id)
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(CasaAccount, BookingAccount.account_id == CasaAccount.id)
        .join(Currency, CasaAccount.currency_id == Currency.id)
        .outerjoin(AccountStructureType, CasaAccount.acc_structure_type_id == AccountStructureType.parent_id)
        .outerjoin(AddressCountry, Currency.country_code == AddressCountry.id)
        .filter(booking_parent.id == booking_parent_id)
    ).all()
    return ReposReturn(data=get_casa_open_casa_info)
