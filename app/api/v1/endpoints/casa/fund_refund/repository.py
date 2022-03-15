from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.casa.fund_refund.schema import FundRefundResponse
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)


async def repos_fund_info(
    cif_id: str,
    session: Session
) -> ReposReturn:
    data_response = {
        "transaction_code": "CRM2115200100001",
        "transaction_type": {
            "is_fund_flag": True,
            "is_main_fund_flag": True,
            "till_or_vault": {
                "id": "1",
                "code": "TILL",
                "name": "TILL"
            },
            "full_name_vn": "Nguyễn Văn A",
            "position": {
                "id": "BAC_SI",
                "code": "BAC_SI",
                "name": "BAC_SI"
            },
            "currency": {
                "id": "01",
                "code": "VND",
                "name": "VND"
            },
            "amount": 1000000,
            "content": "Ứng quỹ",
            "sealed_bags": [
                {
                    "id": "001_VND_THIPTM_14587125_4152_LANH",
                    "code": "001_VND_THIPTM_14587125_4152_LANH",
                    "name": "BAO_NIEM_PHONG_TIEN_LANH_THIPTM",
                    "amount": 100000000,
                    "status": {
                        "id": "2",
                        "code": "DA_NIEM_PHONG",
                        "name": "Đã niêm phong"
                    }
                },
                {
                    "id": "001_VND_THIPTM_14587125_4152_LANH",
                    "code": "001_VND_THIPTM_14587125_4152_LANH",
                    "name": "BAO_NIEM_PHONG_TIEN_LANH_THIPTM",
                    "amount": 100000000,
                    "status": {
                        "id": "2",
                        "code": "DA_NIEM_PHONG",
                        "name": "Đã niêm phong"
                    }
                }
            ]
        },
        "invoice_list_detail": {
            "invoice_list": [
                {
                    "denomination": 500000,
                    "quantity": 0,
                    "into_money": 0
                },
                {
                    "denomination": 200000,
                    "quantity": 0,
                    "into_money": 0
                },
                {
                    "denomination": 100000,
                    "quantity": 0,
                    "into_money": 0
                },
                {
                    "denomination": 50000,
                    "quantity": 0,
                    "into_money": 0
                },
                {
                    "denomination": 20000,
                    "quantity": 0,
                    "into_money": 0
                },
                {
                    "denomination": 10000,
                    "quantity": 0,
                    "into_money": 0
                }
            ],
            "total_list": 1200000,
            "total_sealed_bags": 1000000,
            "total_money": 2200000
        }
    }

    return ReposReturn(data=data_response)


async def repos_save_fund_info(
    cif_id: str,
    request: FundRefundResponse,
    session: Session

) -> ReposReturn:
    customer = session.execute(
        select(
            Customer
        ).filter(Customer.id == cif_id)
    ).all()

    data_response = {}
    if customer:
        sealed_bags = [{
            "id": item.id,
            "amount": item.amount,
            "status": item.status
        } for item in request.transaction_type.sealed_bags]
        transaction_type = {
            "is_fund_flag": request.transaction_type.is_fund_flag,
            "is_main_fund_flag": request.transaction_type.is_main_fund_flag,
            "till_or_vault": request.transaction_type.till_or_vault,
            "full_name_vn": request.transaction_type.full_name_vn,
            "position": request.transaction_type.position,
            "currency": request.transaction_type.currency,
            "amount": request.transaction_type.amount,
            "content": request.transaction_type.content,
            "sealed_bags": sealed_bags
        }
        invoice_list = [{
            "denomination": item.denomination,
            "quantity": item.quantity,
            "total": item.denomination * item.quantity,
        } for item in request.invoice_list_detail.invoice_list]

        invoice_list_detail = {
            "invoice_list": invoice_list,
        }

        data_response = {
            "transaction_code": request.transaction_code,
            "transaction_type": transaction_type,
            "invoice_list_detail": invoice_list_detail,
        }
    return ReposReturn(data=data_response)
