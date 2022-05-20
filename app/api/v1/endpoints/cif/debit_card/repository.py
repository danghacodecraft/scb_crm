import json
from typing import List

from sqlalchemy import and_, delete, or_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.debit_card.model import (
    CardDeliveryAddress, DebitCard, DebitCardType
)
from app.third_parties.oracle.models.master_data.address import (
    AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.card import (
    BrandOfCard, CardIssuanceFee, CardIssuanceType, CardType
)
from app.third_parties.oracle.models.master_data.customer import CustomerType
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.cif import BUSINESS_FORM_TGN
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST, ERROR_NO_DATA
from app.utils.functions import dropdown, now


async def repos_debit_card(cif_id: str, session: Session) -> ReposReturn:
    parent_id = session.execute(select(DebitCard.id).filter(DebitCard.customer_id == cif_id)).scalar()
    if not parent_id:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA,
                           loc="cif_id")
    list_debit_card_info_engine = session.execute(
        select(
            DebitCard.customer_id,
            DebitCard.customer_type_id,
            DebitCard.brand_of_card_id,
            DebitCard.card_issuance_fee_id,
            DebitCard.parent_card_id,
            DebitCard.card_registration_flag,
            DebitCard.payment_online_flag,
            DebitCard.first_name_on_card,
            DebitCard.middle_name_on_card,
            DebitCard.last_name_on_card,
            DebitCard.card_delivery_address_flag,
            DebitCardType.card_id,
            DebitCardType.card_type_id,
            CardType,
            CardIssuanceType,
            CustomerType,
            BrandOfCard,
            CardIssuanceFee,
            CardDeliveryAddress,
            AddressWard,
            AddressDistrict,
            AddressProvince,
            Customer,
            DebitCard,
            Branch
        ).join(
            DebitCardType, DebitCardType.card_id == DebitCard.id
        ).join(
            CardType, CardType.id == DebitCardType.card_type_id
        ).join(
            CardIssuanceType, CardIssuanceType.id == DebitCard.card_issuance_type_id
        ).join(
            CustomerType, CustomerType.id == DebitCard.customer_type_id
        ).join(
            BrandOfCard, BrandOfCard.id == DebitCard.brand_of_card_id
        ).join(
            CardIssuanceFee, CardIssuanceFee.id == DebitCard.card_issuance_fee_id
        ).join(
            CardDeliveryAddress, CardDeliveryAddress.id == DebitCard.card_delivery_address_id
        ).outerjoin(
            Branch, CardDeliveryAddress.branch_id == Branch.id
        ).join(
            Customer, Customer.id == DebitCard.customer_id
        ).outerjoin(
            AddressWard, CardDeliveryAddress.ward_id == AddressWard.id,
        ).outerjoin(
            AddressDistrict, CardDeliveryAddress.district_id == AddressDistrict.id
        ).outerjoin(
            AddressProvince, CardDeliveryAddress.province_id == AddressProvince.id
        ).filter(
            and_(
                DebitCard.active_flag == 1,
                or_(
                    DebitCard.customer_id == cif_id,
                    DebitCard.parent_card_id == parent_id
                )
            )
        )).all()

    if not list_debit_card_info_engine:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
    issue_debit_card = None
    information_debit_card = None
    card_delivery_address = None
    physical_card_type = []
    sub_debit_card = {}
    for item in list_debit_card_info_engine:
        if item.parent_card_id is None:
            physical_card_type.append(dropdown(item.CardType))
            issue_debit_card = {
                "register_flag": item.card_registration_flag,
                "physical_card_type": physical_card_type,
                "physical_issuance_type": dropdown(item.CardIssuanceType),
                "customer_type": dropdown(item.CustomerType),
                "payment_online_flag": item.payment_online_flag,
                "branch_of_card": dropdown(item.BrandOfCard),
                "issuance_fee": dropdown(item.CardIssuanceFee),
                "annual_fee": dropdown(item.CardIssuanceFee),  # TODO
                "debit_card_types": [  # TODO
                    {
                        "id": "1",
                        "code": "MDTC1",
                        "name": "VISA",
                        "source_code": "DM407",
                        "promo_code": "P311",
                        "active_flag": True
                    }
                ]
            }
            information_debit_card = {
                "name_on_card": {
                    "last_name_on_card": item.last_name_on_card,
                    "middle_name_on_card": item.middle_name_on_card,
                    "first_name_on_card": item.first_name_on_card,

                },
                "main_card_number": {  # TODO
                    "number_part_1": "1234",
                    "number_part_2": "5678",
                    "number_part_3": "9875",
                    "number_part_4": "5781"
                },
                "card_image_url": "https://vi.wikipedia.org/wiki/Trang_Ch%C3%ADn"
            }
            card_delivery_address = {
                "delivery_address_flag": item.DebitCard.card_delivery_address_flag,
                "scb_branch": dropdown(item.Branch) if item.Branch else None,
                "delivery_address": {
                    "province": dropdown(item.AddressProvince) if item.AddressProvince else None,
                    "district": dropdown(item.AddressDistrict) if item.AddressDistrict else None,
                    "ward": dropdown(item.AddressWard) if item.AddressWard else None,
                    "number_and_street": item.CardDeliveryAddress.card_delivery_address_address,
                },
                "note": item.CardDeliveryAddress.card_delivery_address_note
            }
        else:
            if not item.Customer.cif_number or len(item.Customer.cif_number) != 7:
                return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc=item.Customer.cif_number)
            sub_debit_card_data = {
                "id": item.DebitCard.id,
                "cif_number": item.Customer.cif_number,
                "name_on_card": {
                    "last_name_on_card": item.DebitCard.last_name_on_card,
                    "middle_name_on_card": item.DebitCard.middle_name_on_card,
                    "first_name_on_card": item.DebitCard.first_name_on_card,
                },
                "physical_card_type": [dropdown(item.CardType)],
                "card_issuance_type": dropdown(item.CardIssuanceType),
                "payment_online_flag": item.DebitCard.payment_online_flag,
                "card_delivery_address": {
                    "delivery_address_flag": item.DebitCard.card_delivery_address_flag,
                    "scb_branch": dropdown(item.Branch) if item.Branch else None,
                    "delivery_address": {
                        "province": dropdown(item.AddressProvince) if item.AddressProvince else None,
                        "district": dropdown(item.AddressDistrict) if item.AddressDistrict else None,
                        "ward": dropdown(item.AddressWard) if item.AddressWard else None,
                        "number_and_street": item.CardDeliveryAddress.card_delivery_address_address,
                    },
                    "note": item.CardDeliveryAddress.card_delivery_address_note
                },
                "main_card_number": {  # TODO
                    "number_part_1": "1234",
                    "number_part_2": "5678",
                    "number_part_3": "9875",
                    "number_part_4": "5781"
                },
                "card_image_url": "https://vi.wikipedia.org/wiki/Trang_Ch%C3%ADn"  # TODO

            }
            if not sub_debit_card.get(item.DebitCard.id):
                sub_debit_card[item.DebitCard.id] = sub_debit_card_data
            else:
                sub_debit_card[item.DebitCard.id]["physical_card_type"].append(dropdown(item.CardType))

    return ReposReturn(data={
        "issue_debit_card": issue_debit_card,
        "information_debit_card": information_debit_card,
        "card_delivery_address": card_delivery_address,
        "information_sub_debit_card": {
            "sub_debit_cards": list(sub_debit_card.values()),
            "total_sub_debit_card": len(sub_debit_card)
        }

    })


@auto_commit
async def repos_add_debit_card(
        cif_id: str,
        list_card_type: List,
        list_sub_card_ids: List,
        list_delivery_address_ids: List,
        main_card_id,
        list_debit_card_type: List,
        data_card_delivery_address,
        data_debit_card,
        list_sub_delivery_address,
        list_sub_debit_card,
        list_sub_debit_card_type,
        log_data: json,
        history_datas: json,
        session: Session) -> ReposReturn:
    # Xóa dữ liệu cũ
    if main_card_id:

        session.execute(delete(DebitCardType).filter(DebitCardType.card_id.in_(list_card_type)))
        if len(list_sub_card_ids) > 0:
            session.execute(delete(DebitCard).filter(DebitCard.id.in_(list_sub_card_ids)))

        session.execute(delete(DebitCard).filter(DebitCard.id == main_card_id))
        session.execute(delete(CardDeliveryAddress).filter(CardDeliveryAddress.id.in_(list_delivery_address_ids)))

    session.add(CardDeliveryAddress(**data_card_delivery_address))
    session.flush()
    session.add(DebitCard(**data_debit_card))
    session.flush()
    session.bulk_save_objects([DebitCardType(**data_type) for data_type in list_debit_card_type])

    session.bulk_save_objects(
        [CardDeliveryAddress(**list_sub_delivery_address) for list_sub_delivery_address in list_sub_delivery_address])
    session.bulk_save_objects([DebitCard(**list_sub_debit_card) for list_sub_debit_card in list_sub_debit_card])
    session.bulk_save_objects([DebitCardType(**data_sub_type) for data_sub_type in list_sub_debit_card_type])

    is_success, booking_responses = await write_transaction_log_and_update_booking(
        log_data=log_data,
        history_datas=history_datas,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TGN
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_responses['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        'created_at': now(),
        'created_by': 'system',
        'updated_at': now(),
        'updated_by': 'system'
    })


async def repos_get_list_debit_card(
        cif_id: str,  # noqa #  TODO
        branch_of_card_id: str,  # noqa
        issuance_fee_id: str,  # noqa
        annual_fee_id: str  # noqa
) -> ReposReturn:
    return ReposReturn(data=[
        {
            "id": "1",
            "code": "MDTC1",
            "name": "VISA",
            "source_code": "DM407",
            "promo_code": "P311",
        },
        {
            "id": "2",
            "code": "VSDB",
            "name": "MASTER CARD",
            "source_code": "DM407",
            "promo_code": "P311",
        }
    ]
    )


async def get_data_debit_card_by_cif_num(session: Session, cif_id: str) -> ReposReturn:
    parent_id = session.execute(select(DebitCard.id).filter(DebitCard.customer_id == cif_id)).scalar()
    if not parent_id:
        return ReposReturn(data=[])
    obj = session.execute(
        select(DebitCard).filter(
            and_(
                DebitCard.active_flag == 1,
                or_(
                    DebitCard.customer_id == cif_id,
                    DebitCard.parent_card_id == parent_id)
            )
        )
    ).scalars().all()

    return ReposReturn(data=obj)


async def get_data_customer_id(session: Session, cif_id: str) -> ReposReturn:
    objs = session.execute(select(Customer.id).filter(Customer.cif_number == cif_id)).scalars().all()
    if not objs:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST,
                           loc="information_sub_debit_card -> sub_debit_cards -> cif_number")

    return ReposReturn(data=objs)
