import json
from typing import List

import loguru
from sqlalchemy import select
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
from app.utils.constant.cif import BUSINESS_FORM_TGN, CIF_ID_TEST
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_CIF_NUMBER_NOT_EXIST
)
from app.utils.functions import dropdown, now


async def repos_debit_card(cif_id: str, session: Session) -> ReposReturn:
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
            DebitCard.customer_id == cif_id,
            DebitCard.active_flag == 1,
        )
    ).all()

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
        list_debit_card_type: List,
        data_card_delivery_address,
        data_debit_card,
        list_sub_delivery_address,
        list_sub_debit_card,
        list_sub_debit_card_type,
        log_data: json,
        session: Session) -> ReposReturn:
    session.add(CardDeliveryAddress(**data_card_delivery_address))
    session.flush()
    session.add(DebitCard(**data_debit_card))
    session.flush()
    session.bulk_save_objects([DebitCardType(**data_type) for data_type in list_debit_card_type])

    session.bulk_save_objects(
        [CardDeliveryAddress(**list_sub_delivery_address) for list_sub_delivery_address in list_sub_delivery_address])
    session.bulk_save_objects([DebitCard(**list_sub_debit_card) for list_sub_debit_card in list_sub_debit_card])
    session.bulk_save_objects([DebitCardType(**data_sub_type) for data_sub_type in list_sub_debit_card_type])

    await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TGN
    )
    return ReposReturn(data={
        "cif_id": cif_id,
        'created_at': now(),
        'created_by': 'system',
        'updated_at': now(),
        'updated_by': 'system'
    })


async def repos_get_list_debit_card(
        cif_id: str,
        branch_of_card_id: str,  # noqa
        issuance_fee_id: str,  # noqa
        annual_fee_id: str  # noqa
) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
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
    else:
        ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")


async def get_customer_by_cif_number(cif_num: str, session: Session) -> ReposReturn:

    try:
        data = session.execute(
            select(Customer).filter(
                Customer.cif_number == cif_num
            )
        ).one()
    except Exception as ex:
        loguru.logger.error(ex)
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_NOT_EXIST, loc="cif_num")
    if not data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_NOT_EXIST, loc="cif_num")

    return ReposReturn(data={
        "last_name": data[0].last_name,
        "first_name": data[0].first_name,
        "cus_id": data[0].id
    })
