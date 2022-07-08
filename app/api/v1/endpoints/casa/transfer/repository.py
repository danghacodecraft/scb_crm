from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.others import (
    SlaTransaction, TransactionJob, TransactionStage, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.approval import BUSINESS_JOB_CODE_CASA_TRANSFER
from app.utils.constant.casa import (
    RECEIVING_METHOD_SCB_BY_IDENTITY, RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT
)
from app.utils.constant.cif import BUSINESS_FORM_CASA_TRANSFER_PD
from app.utils.constant.gw import GW_CASA_RESPONSE_STATUS_SUCCESS
from app.utils.functions import generate_uuid, now, orjson_dumps


@auto_commit
async def repos_save_casa_transfer_info(
        booking_id: str,
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
        saving_customer: dict,
        saving_customer_identity: dict,
        saving_customer_address: dict,
        session: Session
):
    # Lưu log vào DB
    insert_list = [
        # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSINESS_FORM
        TransactionStageStatus(**saving_transaction_stage_status),
        SlaTransaction(**saving_sla_transaction),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        TransactionJob(**saving_transaction_job),
        BookingBusinessForm(**saving_booking_business_form)
    ]
    if saving_customer and saving_customer_identity and saving_customer_address:
        insert_list.extend([
            Customer(**saving_customer),
            CustomerIdentity(**saving_customer_identity)
        ])

    # Lưu log vào DB
    session.add_all(insert_list)

    # Update Booking
    session.execute(
        update(
            Booking
        )
        .filter(Booking.id == booking_id)
        .values(
            transaction_id=saving_transaction_daily['transaction_id']
        )
    )
    session.flush()
    return ReposReturn(data=booking_id)


# @auto_commit
async def repos_gw_save_casa_transfer_info(
        current_user,
        receiving_method: str,
        request_data,
        booking_id,
        session
):
    gw_casa_transfer, function_out, is_success = None, None, False
    if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
        is_success, gw_casa_transfer = await service_gw.gw_payment_internal_transfer(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        function_out = 'internal_transfer_out'

    if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
        is_success, gw_casa_transfer = await service_gw.gw_payment_tt_liquidation(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        function_out = 'tt_liquidation_out'

    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
        is_success, gw_casa_transfer = await service_gw.gw_payment_interbank_transfer(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        function_out = 'interbankTransfer_out'
    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY and \
            receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
        is_success, gw_casa_transfer = await service_gw.gw_payment_tt_liquidation(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        function_out = 'tt_liquidation_out'
    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT:
        is_success, gw_casa_transfer = await service_gw.gw_payment_interbank_transfer_247_by_account_number(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        function_out = 'interbankTransfer247ByAccNum_out'
    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD:
        is_success, gw_casa_transfer = await service_gw.gw_payment_interbank_transfer_247_by_card_number(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        function_out = 'interbankTransfer247ByCardNum_out'

    if not gw_casa_transfer:
        return ReposReturn(is_error=True, msg="No GW Casa Transfer")

    casa_transfer = gw_casa_transfer.get(function_out, {})

    # check trường hợp lỗi
    if casa_transfer.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=casa_transfer.get('transaction_info').get('transaction_error_msg'))

    # lưu form data request GW
    session.add(
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            form_data=orjson_dumps(request_data),
            business_form_id=BUSINESS_FORM_CASA_TRANSFER_PD,
            save_flag=True,
            created_at=now(),
            log_data=orjson_dumps(gw_casa_transfer)
        ))
    )

    session.add(TransactionJob(**dict(
        transaction_id=generate_uuid(),
        booking_id=booking_id,
        business_job_id=BUSINESS_JOB_CODE_CASA_TRANSFER,
        complete_flag=is_success,
        error_code=gw_casa_transfer.get(function_out).get('transaction_info').get(
            'transaction_error_code'),
        error_desc=gw_casa_transfer.get(function_out).get('transaction_info').get(
            'transaction_error_msg'),
        created_at=now()
    )))

    return ReposReturn(data=casa_transfer)


async def repos_get_casa_transfer_info(booking_id: str, session: Session):
    get_casa_transfer_info = session.execute(
        select(
            BookingBusinessForm
        )
        .filter(BookingBusinessForm.booking_id == booking_id)
        .order_by(desc(BookingBusinessForm.created_at))
    ).scalars().first()
    return ReposReturn(data=get_casa_transfer_info)


async def repos_get_acc_types(numbers: list, session: Session):
    get_acc_types = session.execute(
        select(
            CasaAccount.casa_account_number,
            CasaAccount.acc_type_id
        ).filter(CasaAccount.casa_account_number.in_(numbers))
    ).all()

    return ReposReturn(data=get_acc_types)
