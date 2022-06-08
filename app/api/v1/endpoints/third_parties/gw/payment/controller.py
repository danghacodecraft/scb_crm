from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_gw_payment_amount_block
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    AccountAmountBlock
)


class CtrGWPayment(BaseController):

    async def ctr_gw_payment_amount_block(
        self,
        account_number: str,
        account_amount_block: AccountAmountBlock
    ):
        current_user = self.current_user

        data_input = {
            "account_info": {
                "account_num": account_number
            },
            "p_blk_detail": {
                "AMOUNT": account_amount_block.amount,
                "AMOUNT_BLOCK_TYPE": account_amount_block.amount_block_type,
                "HOLD_CODE": account_amount_block.hold_code,
                "EFFECTIVE_DATE": account_amount_block.effective_date,
                "EXPIRY_DATE": account_amount_block.expiry_date if account_amount_block.expiry_date else "",
                "REMARKS": account_amount_block.remarks,
                "VERIFY_AVAILABLE_BALANCE": account_amount_block.verify_available_balance,
                "CHARGE_DETAIL": {
                    "TYPE_CHARGE": "",
                    "ACCOUNT_CHARGE": ""
                }
            },
            # TODO chưa được mô tả
            "p_blk_charge": [
                {
                    "CHARGE_NAME": "",
                    "CHARGE_AMOUNT": 0,
                    "WAIVED": "N"
                }
            ],
            # TODO chưa được mô tả
            "p_blk_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": "",
                    "AMOUNT_BLOCK": {
                        "UDF_NAME": "",
                        "UDF_VALUE": ""
                    }
                }
            ],
            "staff_info_checker": {
                # TODO hard core
                "staff_name": "HOANT2"
            },
            "staff_info_maker": {
                # TODO hard core
                "staff_name": "KHANHLQ"
            }
        }

        gw_payment_amount_block = self.call_repos(await repos_gw_payment_amount_block(
            current_user=current_user,
            data_input=data_input
        ))

        return self.response(data=gw_payment_amount_block)
