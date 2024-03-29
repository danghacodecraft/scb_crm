from datetime import date
from typing import List, Optional

from sqlalchemy import and_, desc, distinct, func, or_, select
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.e_banking.model import TdAccount
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm, BookingCustomer,
    TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    Branch, SlaTransaction, TransactionStage, TransactionStageRole,
    TransactionStageStatus
)
from app.utils.constant.cif import (
    BUSINESS_FORM_OPEN_CASA_OPEN_CASA, BUSINESS_FORM_WITHDRAW,
    CONTACT_ADDRESS_CODE
)
from app.utils.functions import date_to_datetime, end_time_of_day
from app.utils.vietnamese_converter import convert_to_unsigned_vietnamese


async def repos_count_total_item(region_id: Optional[str], branch_id: Optional[str], business_type_id: Optional[str],
                                 status_code: Optional[str], search_box: Optional[str], from_date: Optional[date],
                                 to_date: Optional[date], session: Session) -> ReposReturn:
    transaction_list = select(
        func.count(distinct(Booking.code))
    ) \
        .join(Branch, Booking.branch_id == Branch.id) \
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id) \
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id) \
        .outerjoin(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id) \
        .outerjoin(BookingCustomer, Booking.id == BookingCustomer.booking_id) \
        .outerjoin(Customer, BookingCustomer.customer_id == Customer.id) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .distinct()

    if region_id:
        transaction_list = transaction_list.filter(Branch.region_id == region_id)

    if branch_id:
        transaction_list = transaction_list.filter(Branch.id == branch_id)

    if business_type_id:
        transaction_list = transaction_list.filter(Booking.business_type_id == business_type_id)

    if status_code:
        transaction_list = transaction_list.filter(TransactionStageStatus.code == status_code)

    if search_box:
        search_box = f'%{search_box}%'
        transaction_list = transaction_list.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    Customer.cif_number.ilike(search_box),
                    or_(
                        CustomerIdentity.identity_num.ilike(search_box)),
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                )
            )
        )

    if from_date:
        transaction_list = transaction_list.filter(
            Booking.created_at >= date_to_datetime(from_date)
        )

    if to_date:
        transaction_list = transaction_list.filter(
            Booking.created_at <= end_time_of_day(date_to_datetime(to_date))
        )

    total_item = session.execute(transaction_list).scalar()
    return ReposReturn(data=total_item)


async def repos_get_customers_by_cif_number(
        cif_numbers: list,
        session: Session
) -> ReposReturn:
    customers = session.execute(
        select(
            Customer
        ).filter(
            Customer.cif_number.in_(cif_numbers),
            Customer.complete_flag == 1
        )
    ).scalars().all()

    return ReposReturn(data=customers)


async def repos_get_transaction_list(region_id: Optional[str], branch_id: Optional[str],
                                     business_type_id: Optional[str], status_code: Optional[str],
                                     search_box: Optional[str], from_date: Optional[date], to_date: Optional[date],
                                     limit: int, page: int, session: Session):
    sql = select(
        Booking,
        Branch,
        TransactionStageStatus.name.label('status'),
        TransactionStageRole
    ) \
        .join(Branch, Booking.branch_id == Branch.id) \
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id) \
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id) \
        .join(TransactionStageRole, TransactionStage.id == TransactionStageRole.transaction_stage_id) \
        .outerjoin(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id) \
        .outerjoin(BookingCustomer, Booking.id == BookingCustomer.booking_id) \
        .outerjoin(Customer, BookingCustomer.customer_id == Customer.id) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .distinct()

    if region_id:
        sql = sql.filter(Branch.region_id == region_id)

    if branch_id:
        sql = sql.filter(Branch.id == branch_id)

    if business_type_id:
        sql = sql.filter(Booking.business_type_id == business_type_id)

    if status_code:
        sql = sql.filter(TransactionStageStatus.code == status_code)

    if search_box:
        search_box = f'%{search_box}%'
        sql = sql.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    Customer.cif_number.ilike(search_box),
                    or_(
                        CustomerIdentity.identity_num.ilike(search_box)),
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                )
            )
        )

    if from_date:
        sql = sql.filter(
            Booking.created_at >= date_to_datetime(from_date)
        )

    if to_date:
        sql = sql.filter(
            Booking.created_at <= end_time_of_day(date_to_datetime(to_date))
        )

    sql = sql.limit(limit).offset(limit * (page - 1)).order_by(desc(Booking.created_at))

    transaction_list = session.execute(sql).all()
    return ReposReturn(data=transaction_list)


async def repos_get_senders(
        booking_ids: tuple,
        region_id: Optional[str], branch_id: Optional[str], status_code: Optional[str],
        search_box: Optional[str], from_date: Optional[date], to_date: Optional[date], business_type_id: Optional[str],
        session: Session
):
    # Lấy tất cả các transaction
    sql = select(
        TransactionDaily.transaction_root_id,
        Booking
    ) \
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id) \
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id) \
        .join(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id) \
        .join(Branch, Booking.branch_id == Branch.id) \
        .outerjoin(BookingCustomer, Booking.id == BookingCustomer.booking_id) \
        .outerjoin(Customer, BookingCustomer.customer_id == Customer.id) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .filter(Booking.id.in_(booking_ids))

    if region_id:
        sql = sql.filter(Branch.region_id == region_id)

    if branch_id:
        sql = sql.filter(Booking.branch_id == branch_id)

    if business_type_id:
        sql = sql.filter(Booking.business_type_id == business_type_id)

    if status_code:
        sql = sql.filter(TransactionStageStatus.code == status_code)

    if search_box:
        search_box = f'%{search_box}%'
        sql = sql.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    Customer.cif_number.ilike(search_box),
                    or_(
                        CustomerIdentity.identity_num.ilike(search_box)),
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                )
            )
        )

    if from_date and to_date:
        sql = sql.filter(
            and_(
                Booking.created_at >= date_to_datetime(from_date),
                Booking.created_at <= end_time_of_day(date_to_datetime(to_date))
            ))

    transaction_root_dailies = session.execute(
        sql
    ).scalars().all()

    if not transaction_root_dailies:
        return ReposReturn(is_error=True, msg="No Transaction Root Daily")

    transaction_daily_ids = session.execute(
        select(
            TransactionDaily.transaction_id
        )
        .filter(TransactionDaily.transaction_root_id.in_(transaction_root_dailies))
    ).scalars().all()

    sql = select(
        TransactionDaily,
        TransactionStage,
        TransactionStageRole,
        TransactionSender,
        Booking,
        SlaTransaction
    ) \
        .outerjoin(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id) \
        .join(Booking, TransactionDaily.transaction_id == Booking.transaction_id) \
        .outerjoin(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id) \
        .outerjoin(TransactionStageRole, TransactionStage.id == TransactionStageRole.transaction_stage_id) \
        .outerjoin(SlaTransaction, TransactionStage.sla_transaction_id == SlaTransaction.id) \
        .outerjoin(BookingCustomer, Booking.id == BookingCustomer.booking_id) \
        .outerjoin(Customer, BookingCustomer.customer_id == Customer.id) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .filter(TransactionDaily.transaction_id.in_(transaction_daily_ids))

    if region_id:
        sql = sql.filter(Branch.region_id == region_id)

    if branch_id:
        sql = sql.filter(Booking.branch_id == branch_id)

    if business_type_id:
        sql = sql.filter(Booking.business_type_id == business_type_id)

    if status_code:
        sql = sql.filter(TransactionStageStatus.code == status_code)

    if search_box:
        search_box = f'%{search_box}%'
        sql = sql.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    Customer.cif_number.ilike(search_box),
                    or_(
                        CustomerIdentity.identity_num.ilike(search_box)),
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                )
            )
        )

    if from_date and to_date:
        sql = sql.filter(
            and_(
                Booking.created_at >= date_to_datetime(from_date),
                Booking.created_at <= end_time_of_day(date_to_datetime(to_date))
            ))
    stage_infos = session.execute(
        sql
    ).all()
    return ReposReturn(data=stage_infos)


async def repos_get_sla_transaction_infos(booking_ids: tuple, session: Session):
    sla_transaction_parent = aliased(SlaTransaction, name="SlaTransParent")
    sla_trans_daily_parent = aliased(TransactionDaily, name="SlaTransDailyParent")
    sla_trans_stage_parent = aliased(TransactionStage, name="SlaTransStageParent")
    sender_sla_trans_parent = aliased(TransactionSender, name="SenderSlaTransParent")

    sla_transaction_grandparent = aliased(SlaTransaction, name="SlaTransGrandparent")
    sla_trans_daily_grandparent = aliased(TransactionDaily, name="SlaTransDailyGrandparent")
    sla_trans_stage_grandparent = aliased(TransactionStage, name="SlaTransStageGrandparent")
    sender_sla_trans_grandparent = aliased(TransactionSender, name="SenderSlaTransGrandparent")

    sla_transaction_infos = session.execute(
        select(
            Booking,
            SlaTransaction,
            TransactionSender,
            sla_transaction_parent,
            sender_sla_trans_parent,
            sla_transaction_grandparent,
            sender_sla_trans_grandparent,
            BookingBusinessForm
        )
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id)
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id)
        .join(SlaTransaction, TransactionStage.sla_transaction_id == SlaTransaction.id)
        .outerjoin(sla_transaction_parent, SlaTransaction.parent_id == sla_transaction_parent.id)
        .outerjoin(sla_trans_stage_parent, sla_transaction_parent.id == sla_trans_stage_parent.sla_transaction_id)
        .outerjoin(sla_trans_daily_parent,
                   sla_trans_stage_parent.id == sla_trans_daily_parent.transaction_stage_id)
        .outerjoin(sender_sla_trans_parent,
                   sla_trans_daily_parent.transaction_id == sender_sla_trans_parent.transaction_id)
        .outerjoin(sla_transaction_grandparent,
                   sla_transaction_parent.parent_id == sla_transaction_grandparent.id)
        .outerjoin(sla_trans_stage_grandparent,
                   sla_transaction_grandparent.id == sla_trans_stage_grandparent.sla_transaction_id)
        .outerjoin(sla_trans_daily_grandparent,
                   sla_trans_stage_grandparent.id == sla_trans_daily_grandparent.transaction_stage_id)
        .outerjoin(sender_sla_trans_grandparent,
                   sla_trans_daily_grandparent.transaction_id == sender_sla_trans_grandparent.transaction_id)
        .outerjoin(BookingBusinessForm, Booking.id == BookingBusinessForm.booking_id)
        .filter(Booking.id.in_(booking_ids))
    ).all()

    return ReposReturn(data=sla_transaction_infos)


async def repos_get_total_item(
        cif_number: str,
        identity_number: str,
        phone_number: str,
        full_name: str,
        session: Session
):
    customers = select(
        func.count(Customer.id)
    ) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .outerjoin(CustomerAddress,
                   and_(
                       Customer.id == CustomerAddress.customer_id,
                       CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE
                   )) \
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id) \
        .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id) \
        .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id) \
        .outerjoin(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id) \
        .outerjoin(Branch, Customer.open_branch_id == Branch.id)

    customers = customers.filter(Customer.complete_flag == True)  # noqa
    if cif_number:
        customers = customers.filter(Customer.cif_number.ilike(f'%{cif_number}%'))
    if identity_number:
        customers = customers.filter(CustomerIdentity.identity_num.ilike(f'%{identity_number}%'))
    if phone_number:
        customers = customers.filter(Customer.mobile_number.ilike(f'%{phone_number}%'))
    if full_name:
        customers = customers.filter(Customer.full_name.ilike(f'%{full_name}%'))

    total_item = session.execute(
        customers
    ).scalar()

    return ReposReturn(data=total_item)


async def repos_get_customer(
        cif_number: str,
        identity_number: str,
        phone_number: str,
        full_name: str,
        limit: int,
        page: int,
        session: Session
):
    customers = select(
        Customer,
        CustomerIdentity,
        CustomerAddress,
        AddressWard,
        AddressDistrict,
        AddressProvince,
        AddressCountry,
        Branch
    ) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .outerjoin(CustomerAddress, and_(
            Customer.id == CustomerAddress.customer_id,
            CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE
        )) \
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id) \
        .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id) \
        .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id) \
        .outerjoin(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id) \
        .outerjoin(Branch, Customer.open_branch_id == Branch.id)

    customers = customers.filter(Customer.complete_flag == True)  # noqa
    if cif_number:
        customers = customers.filter(Customer.cif_number.ilike(f'%{cif_number}%'))
    if identity_number:
        customers = customers.filter(CustomerIdentity.identity_num.ilike(f'%{identity_number}%'))
    if phone_number:
        customers = customers.filter(Customer.mobile_number.ilike(f'%{phone_number}%'))
    if full_name:
        customers = customers.filter(Customer.full_name.ilike(f'%{full_name}%'))

    customers = customers.limit(limit)
    customers = customers.offset(limit * (page - 1))

    customers = session.execute(
        customers.order_by(desc('open_cif_at')),
    ).all()

    return ReposReturn(data=customers)

#
# async def repos_accounting_entry(
#         branch_code: str,
# ) -> ReposReturn:
#     data_response = await service_dwh.accounting_entry(branch_code=branch_code, module=NAME_ACCOUNTING_ENTRY)
#
#     return ReposReturn(data=data_response)
#
#
# async def repos_region(
# ) -> ReposReturn:
#     data_response = await service_dwh.get_region()
#
#     return ReposReturn(data=data_response)


async def repos_get_open_casa_info_from_booking(
    booking_ids: List,
    session: Session
) -> ReposReturn:
    open_casa_infos = session.execute(
        select(
            Booking,
            BookingAccount,
            CasaAccount,
            Customer
        )
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(CasaAccount, BookingAccount.account_id == CasaAccount.id)
        .join(Customer, CasaAccount.customer_id == Customer.id)
        .filter(Booking.parent_id.in_(booking_ids))
    ).all()

    booking_business_form_infos = session.execute(
        select(
            Booking.id,
            BookingBusinessForm
        )
        .join(BookingBusinessForm, Booking.id == BookingBusinessForm.booking_id,
              BookingBusinessForm.business_form_id == BUSINESS_FORM_OPEN_CASA_OPEN_CASA)
        .filter(Booking.id.in_(booking_ids))
        .order_by(BookingBusinessForm.created_at)
    )

    return ReposReturn(data=(open_casa_infos, booking_business_form_infos))


async def repos_get_open_cif_info_from_booking(
    booking_ids: List,
    session: Session
) -> ReposReturn:
    open_cif_infos = session.execute(
        select(
            Booking,
            BookingCustomer,
            Customer
        )
        .outerjoin(BookingCustomer, Booking.id == BookingCustomer.booking_id)
        .outerjoin(Customer, BookingCustomer.customer_id == Customer.id)
        .filter(Booking.id.in_(booking_ids))
    ).all()
    return ReposReturn(data=open_cif_infos)


async def repos_get_withdraw_info_from_booking(
    booking_ids: List,
    session: Session
) -> ReposReturn:
    withdraw_infos = session.execute(
        select(
            Booking,
            BookingBusinessForm
        )
        .join(
            BookingBusinessForm, and_(
                Booking.id == BookingBusinessForm.booking_id,
                BookingBusinessForm.business_form_id == BUSINESS_FORM_WITHDRAW
            )
        )
        .filter(Booking.id.in_(booking_ids))
        .order_by(BookingBusinessForm.created_at)
    ).all()
    return ReposReturn(data=withdraw_infos)


async def repos_get_amount_block_from_booking(
        booking_ids: List,
        session: Session
):
    response_data = session.execute(
        select(
            Booking.id,
            BookingAccount,
            CasaAccount,
            Customer
        )
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(CasaAccount, BookingAccount.account_id == CasaAccount.id)
        .join(Customer, CasaAccount.customer_id == Customer.id)
        .filter(Booking.id.in_(booking_ids))
    ).all()

    booking_business_form = session.execute(
        select(
            Booking.id,
            BookingBusinessForm
        )
        .join(BookingBusinessForm, Booking.id == BookingBusinessForm.booking_id)
        .filter(Booking.id.in_(booking_ids))
        .order_by(BookingBusinessForm.created_at)
    ).all()

    return ReposReturn(data=(response_data, booking_business_form))


async def repos_get_td_account_from_booking(
        booking_ids: List,
        session: Session
):

    response_data = session.execute(
        select(
            Booking,
            BookingAccount,
            TdAccount,
            Customer
        )
        .join(BookingAccount, Booking.id == BookingAccount.booking_id)
        .join(TdAccount, BookingAccount.td_account_id == TdAccount.id)
        .join(Customer, TdAccount.customer_id == Customer.id)
        .filter(Booking.id.in_(booking_ids))
    ).all()
    return ReposReturn(data=response_data)
