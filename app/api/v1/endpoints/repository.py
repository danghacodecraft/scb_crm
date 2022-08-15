import json
from typing import List, Optional, Tuple

import inflection as inflection
from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm, BookingCustomer
)
from app.third_parties.oracle.models.denomination.denomination import (
    CurrencyDenomination
)
from app.third_parties.oracle.models.master_data.account import (
    AccountStructureType
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.cif import ACTIVE_FLAG_ACTIVED
from app.utils.error_messages import ERROR_ID_NOT_EXIST, ERROR_INVALID_NUMBER
from app.utils.functions import (
    dropdown, generate_uuid, is_valid_number, now, special_dropdown
)


async def repos_get_model_object_by_id_or_code(model_id: Optional[str], model_code: Optional[str], model: Base,
                                               loc: str, session: Session) -> ReposReturn:
    statement = None

    if model_id:
        statement = select(model).filter(model.id == model_id)

    if model_code:
        statement = select(model).filter(model.code == model_code)

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == ACTIVE_FLAG_ACTIVED)

    obj = session.execute(statement).scalar()
    if not obj:
        if not loc:
            loc = f'{str(model.tablename)}_{"id" if model_id else "code"}'

        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=loc
        )

    return ReposReturn(data=obj)


async def repos_get_model_objects_by_ids(model_ids: List[str], model: Base, session: Session,
                                         loc: Optional[str] = None) -> ReposReturn:
    """
    Get model objects by ids
    Chỉ cần truyền vào list id -> hàm sẽ tự chuyển về set(model_ids)
    :param model_ids: danh sách các id cần lấy ra model object
    :param model: model trong DB
    :param loc: vị trí lỗi
    :param session: phiên làm việc với DB bên controller
    :return:
    """
    model_ids = set(model_ids)

    statement = select(model).filter(model.id.in_(model_ids))

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    objs = session.execute(statement).scalars().all()
    if len(objs) != len(model_ids):
        obj_ids = [obj.id for obj in objs]
        return ReposReturn(
            is_error=True,
            msg=ERROR_ID_NOT_EXIST,
            loc=f'{inflection.tableize(str(model.id))}, {model_ids - model_ids.intersection(set(obj_ids))}' if not loc else loc
        )

    return ReposReturn(data=objs)


async def get_optional_model_object_by_code_or_name(
        model: Base, session: Session, model_id: Optional[str] = None,
        model_code: Optional[str] = None, model_name: Optional[str] = None
) -> Optional[object]:
    statement = None

    if model_id:
        statement = select(model).filter(model.id == model_id)

    if model_name:
        statement = select(model).filter(func.lower(model.name) == func.lower(model_name))  # TODO: check it

    if model_code:
        statement = select(model).filter(model.code == model_code)

    if statement is None:
        return None

    if hasattr(model, 'active_flag'):
        statement = statement.filter(model.active_flag == 1)

    return session.execute(statement).scalar()


async def repos_get_data_currency_config(session):
    response_data = session.execute(
        select(
            Currency,
            AddressCountry
        ).join(
            AddressCountry, Currency.country_code == AddressCountry.code
        )
    ).all()
    return ReposReturn(data=response_data)


async def repos_get_data_currency_denominations_config(session, currency_id: str):
    response_data = session.execute(
        select(
            CurrencyDenomination
        )
        .filter(CurrencyDenomination.currency_id == currency_id)
        .order_by(desc(CurrencyDenomination.denominations))
    ).scalars().all()

    return ReposReturn(data=response_data)


async def repos_get_data_model_config(
        session: Session, model: Base, country_id: Optional[str] = None, province_id: Optional[str] = None,
        district_id: Optional[str] = None, region_id: Optional[str] = None, ward_id: Optional[str] = None,
        level: Optional[str] = None, parent_id: Optional[str] = None, is_special_dropdown: bool = False,
        type_id: Optional[str] = None, napas_flag: bool = False, citad_flag: bool = False,
        bank_id: Optional[str] = None, category_id: Optional[str] = None
):
    list_data_engine = select(model)
    if hasattr(model, "country_id"):
        list_data_engine = list_data_engine.filter(model.country_id == country_id)

    if hasattr(model, "region_id") and region_id:
        list_data_engine = list_data_engine.filter(model.region_id == region_id)

    if hasattr(model, "district_id") and district_id:
        list_data_engine = list_data_engine.filter(model.district_id == district_id)

    if hasattr(model, "province_id") and province_id:
        list_data_engine = list_data_engine.filter(model.province_id == province_id)

    if hasattr(model, "ward_id") and ward_id:
        list_data_engine = list_data_engine.filter(model.ward_id == ward_id)

    if hasattr(model, "level") and level:
        list_data_engine = list_data_engine.filter(model.level == level)

    if hasattr(model, "parent_id") and parent_id:
        list_data_engine = list_data_engine.filter(model.parent_id == parent_id)

    if hasattr(model, 'active_flag'):
        list_data_engine = list_data_engine.filter(model.active_flag == 1)

    if hasattr(model, 'type'):
        list_data_engine = list_data_engine.filter(model.type == type_id)

    if hasattr(model, 'category_id'):
        list_data_engine = list_data_engine.filter(model.category_id == category_id)

    # Bank
    if hasattr(model, 'napas_flag') and napas_flag:
        list_data_engine = list_data_engine.filter(model.napas_flag == napas_flag)

    if hasattr(model, 'citad_flag') and citad_flag:
        list_data_engine = list_data_engine.filter(model.citad_flag == citad_flag)

    # Bank Branch
    if hasattr(model, 'bank_id') and bank_id:
        list_data_engine = list_data_engine.filter(model.bank_id == bank_id)

    if hasattr(model, 'order_no'):
        list_data_engine = list_data_engine.order_by(model.order_no)

    list_data = session.execute(list_data_engine).scalars().all()

    if not list_data:
        return ReposReturn(is_error=True, msg="model doesn't have data", loc='config')

    # Nếu là dropdown có content và type
    if is_special_dropdown:
        return ReposReturn(data=[
            special_dropdown(data) for data in list_data
        ])

    return ReposReturn(data=[
        dropdown(data) for data in list_data
    ])


async def write_transaction_log_and_update_booking(
        log_data: json,
        session: Session,
        business_form_id: str,
        history_datas: Optional[List] = None,
        customer_id: Optional[str] = None,
        account_id: Optional[str] = None,
        booking_id: Optional[str] = None
) -> Tuple[bool, Optional[dict]]:
    if customer_id:
        booking = session.execute(
            select(
                Booking
            )
            .join(
                BookingCustomer, and_(
                    Booking.id == BookingCustomer.booking_id,
                    BookingCustomer.customer_id == customer_id
                )
            )
        ).scalar()
    elif account_id:
        booking = session.execute(
            select(
                Booking
            )
            .join(
                BookingAccount, and_(
                    Booking.id == BookingAccount.booking_id,
                    BookingAccount.account_id == account_id
                )
            )
        ).scalar()
    else:
        booking = None

    if booking_id:
        booking = session.execute(
            select(
                Booking
            ).filter(Booking.id == booking_id)
        ).scalar()

    if not booking:
        return False, dict(msg='Can not found booking')

    booking_business_form = session.execute(
        select(BookingBusinessForm).filter(and_(
            BookingBusinessForm.booking_id == booking.id,
            BookingBusinessForm.business_form_id == business_form_id
        ))
    ).scalar()

    # Nếu chưa có thì tạo mới
    if not booking_business_form:
        session.add(BookingBusinessForm(**dict(
            booking_business_form_id=generate_uuid(),
            booking_id=booking.id,
            business_form_id=business_form_id,
            save_flag=True,
            created_at=now(),
            updated_at=now(),
            form_data=log_data,
            log_data=history_datas
        )))
        response = dict(
            booking_id=booking.id,
            booking_code=booking.code,
            created_at=now(),
            updated_at=now()
        )

    # Nếu có thì cập nhật
    else:
        booking_business_form = session.execute(
            select(
                BookingBusinessForm
            ).filter(and_(
                BookingBusinessForm.business_form_id == business_form_id,
                BookingBusinessForm.booking_id == booking.id
            ))
        ).scalar()
        # Cập nhật đã hoàn thành Tab này
        booking_business_form.form_data = log_data
        booking_business_form.log_data = history_datas
        booking_business_form.update_at = now()
        response = dict(
            booking_id=booking.id,
            booking_code=booking.code,
            created_at=booking_business_form.created_at,
            updated_at=now()
        )
        session.commit()

    return True, response


async def repos_get_acc_structure_type(acc_structure_type_id: str, level: int, loc: str, session: Session):
    acc_structure_type = session.execute(
        select(
            AccountStructureType
        ).filter(and_(
            AccountStructureType.level == level,
            AccountStructureType.id == acc_structure_type_id,
            AccountStructureType.active_flag == ACTIVE_FLAG_ACTIVED
        ))
    ).scalar()
    if not acc_structure_type:
        return ReposReturn(is_error=True, msg=ERROR_ID_NOT_EXIST, loc=loc)

    return ReposReturn(data=acc_structure_type)


async def repos_is_valid_number(string: str, loc: str):
    if is_valid_number(string):
        return ReposReturn(data=None)

    return ReposReturn(is_error=True, msg=ERROR_INVALID_NUMBER, loc=loc)
