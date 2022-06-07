from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_gw_payment_amount_block
)


class CtrGWPayment(BaseController):

    async def ctr_gw_payment_amount_block(self):
        current_user = self.current_user

        data_input = {
            "account_info": {
                "account_num": "0010108370590001"
            },
            "p_blk_detail": {
                "AMOUNT": 1,
                "AMOUNT_BLOCK_TYPE": "F",
                "HOLD_CODE": "PTKHAC",
                "EFFECTIVE_DATE": "30/11/2019",
                "EXPIRY_DATE": "",
                "REMARKS": "",
                "VERIFY_AVAILABLE_BALANCE": "N",
                "CHARGE_DETAIL": {
                    "TYPE_CHARGE": "",
                    "ACCOUNT_CHARGE": ""
                }
            },
            "p_blk_charge": [
                {
                    "CHARGE_NAME": "",
                    "CHARGE_AMOUNT": 0,
                    "WAIVED": "N"
                }
            ],
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
