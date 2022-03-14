from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawResponse
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)


async def repos_withdraw_info(
        cif_id: str,
        session: Session
) -> ReposReturn:
    data_response = {
        "transaction_code": {
            "id": "1",
            "code": "CRM211",
            "name": "CRM2115200100001"
        },
        "transaction_information": {
            "total_account": "5",
            "source_accounts": [
                {
                    "user_id": "1",
                    "full_name": "Nguyễn Ngọc Phương Anh",
                    "card_type": {
                        "id": "1",
                        "code": "SFREE",
                        "name": "S-FREE"
                    },
                    "payment_account": "555789490189018",
                    "available_balances": "123456789000",
                    "currency": {
                        "id": "1",
                        "code": "VND",
                        "name": "VND"
                    }
                }
            ],
            "beneficiary_information": {
                "withdraw_account_flag": True,
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "VND"
                },
                "number_money": "1000000",
                "seri_cheque": {
                    "id": "1",
                    "code": "Code",
                    "name": "Abc123"
                },
                "date_of_issue": "2021-02-18",
                "exchange_VND_flag": True,
                "exchange_rate": "23000",
                "exchanged_money_VND": {
                    "id": "1",
                    "code": "KHONG",
                    "name": "Không"
                },
                "reciprocal_rate_headquarters": "23000",
                "withdrawal_content": "Rút tiền mặt",
                "journal_entry_number": "Số bút toán"
            },
            "fee_information": {
                "fees_same_transaction_flag": {
                    "id": "1",
                    "code": "CO",
                    "name": "Có"
                },
                "fee_payer": {
                    "id": "1",
                    "code": "BENCHUYEN",
                    "name": "Bên chuyển"
                },
                "fee_amount": "100000",
                "tax_VAT": "100000",
                "total_fee_amount": "110000",
                "actual_amount_transferred": "101100000",
                "note": "Chuyển tiền bên chuyển chịu phí"
            },
        },
        "transactional_customer_information": {
            "CIF_flag": True,
            "customer_code": "1234567",
            "trades": "Tran Minh Huyen",
            "identity_document": "89142127412",
            "issued_date": "20/12/1986",
            "place_of_issue": {
                "id": "1",
                "code": "HOCHIMINH",
                "name": "Hồ Chí Minh"
            },
            "address": "17/25 Phường 5, QUận 8, TP HCM",
            "mobile_number": "0714529632",
            "note": "Ghi chú"
        }
    }
    return ReposReturn(data=data_response)


async def repos_save_withdraw_info(
        cif_id: str,
        request: WithdrawResponse,
        session: Session
) -> ReposReturn:
    customer = session.execute(
        select(
            Customer
        ).filter(Customer.id == cif_id)
    ).all()

    data_response = {}
    if customer:
        source_accounts = [{
            "user_id": source_account.user_id,
            "full_name": source_account.full_name,
            "card_type": {
                "id": source_account.card_type.id,
                "code": source_account.card_type.id,
                "name": source_account.card_type.id
            },
            "payment_account": source_account.payment_account,
            "available_balances": source_account.available_balances,
            "currency": {
                "id": source_account.currency.id,
                "code": source_account.currency.id,
                "name": source_account.currency.id
            }
        } for source_account in request.transaction_information.source_account]
        beneficiary_information = request.transaction_information.beneficiary_information
        fee_information = request.transaction_information.fee_information
        transactional_customer_information = request.transactional_customer_information

        data_response = {
            "transaction_code": {
                "id": request.transaction_code.id,
                "code": request.transaction_code.id,
                "name": request.transaction_code.id
            },
            "transaction_information": {
                "total_account": len(source_accounts),
                "source_accounts": source_accounts,
                "beneficiary_information": {
                    "withdraw_account_flag": beneficiary_information.withdraw_account_flag,
                    "currency": {
                        "id": beneficiary_information.currency.id,
                        "code": beneficiary_information.currency.id,
                        "name": beneficiary_information.currency.id
                    },
                    "number_money": beneficiary_information.number_money,
                    "seri_cheque": {
                        "id": beneficiary_information.seri_cheque.id,
                        "code": beneficiary_information.seri_cheque.id,
                        "name": beneficiary_information.seri_cheque.id
                    },
                    "date_of_issue": beneficiary_information.date_of_issue,
                    "exchange_VND_flag": beneficiary_information.exchange_VND_flag,
                    "exchange_rate": beneficiary_information.exchange_rate,
                    "exchanged_money_VND": {
                        "id": beneficiary_information.exchanged_money_VND.id,
                        "code": beneficiary_information.exchanged_money_VND.id,
                        "name": beneficiary_information.exchanged_money_VND.id
                    },
                    "reciprocal_rate_headquarters": beneficiary_information.reciprocal_rate_headquarters,
                    "withdrawal_content": beneficiary_information.withdrawal_content,
                    "journal_entry_number": beneficiary_information.journal_entry_number
                },
                "fee_information": {
                    "fees_same_transaction_flag": {
                        "id": fee_information.fees_same_transaction_flag.id,
                        "code": fee_information.fees_same_transaction_flag.id,
                        "name": fee_information.fees_same_transaction_flag.id
                    },
                    "fee_payer": {
                        "id": fee_information.fee_payer.id,
                        "code": fee_information.fee_payer.id,
                        "name": fee_information.fee_payer.id
                    },
                    "fee_amount": fee_information.fee_amount,
                    "tax_VAT": fee_information.tax_VAT,
                    "total_fee_amount": fee_information.total_fee_amount,
                    "actual_amount_transferred": fee_information.actual_amount_transferred,
                    "note": fee_information.note
                }
            },
            "transactional_customer_information": {
                "CIF_flag": transactional_customer_information.CIF_flag,
                "customer_code": transactional_customer_information.customer_code,
                "trades": transactional_customer_information.trades,
                "identity_document": transactional_customer_information.identity_document,
                "issued_date": transactional_customer_information.issued_date,
                "place_of_issue": {
                    "id": transactional_customer_information.place_of_issue.id,
                    "code": transactional_customer_information.place_of_issue.id,
                    "name": transactional_customer_information.place_of_issue.id
                },
                "address": transactional_customer_information.address,
                "mobile_number": transactional_customer_information.mobile_number,
                "note": transactional_customer_information.note
            }
        }
    return ReposReturn(data=data_response)
