from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_gw_payment_amount_block, repos_gw_payment_amount_unblock
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    AccountAmountBlockRequest, AccountAmountUnblock
)


class CtrGWPayment(BaseController):

    async def ctr_gw_payment_amount_block(
            self,
            account_number: str,
            account_amount_block: AccountAmountBlockRequest
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
        response_data = {
            "account_ref_no": gw_payment_amount_block['amountBlock_out']['data_output']['account_info']['blance_lock_info']['account_ref_no']
        }

        return self.response(data=response_data)

    async def ctr_gw_payment_amount_unblock(
            self,
            account_amount_unblock: AccountAmountUnblock
    ):
        current_user = self.current_user

        p_blk_detail = {
            "AMOUNT": "",
            "HOLD_CODE": "",
            "EXPIRY_DATE": "",
            "REMARKS": "",
            "CHARGE_DETAIL": {
                "TYPE_CHARGE": "",
                "ACCOUNT_CHARGE": ""
            }
        }

        if account_amount_unblock.p_type_unblock == "P":
            if not account_amount_unblock.p_blk_detail:
                return self.response_exception(msg="type_unblock is not data")

            p_blk_detail = {
                "AMOUNT": account_amount_unblock.p_blk_detail.amount,
                "HOLD_CODE": account_amount_unblock.p_blk_detail.hold_code,
                "EXPIRY_DATE": account_amount_unblock.p_blk_detail.expiry_date,
                "REMARKS": account_amount_unblock.p_blk_detail.remarks,
                "CHARGE_DETAIL": {
                    "TYPE_CHARGE": "",
                    "ACCOUNT_CHARGE": ""
                }
            }

        data_input = {
            "account_info": {
                "balance_lock_info": {
                    "account_ref_no": account_amount_unblock.account_ref_no
                }
            },
            "p_type_unblock": account_amount_unblock.p_type_unblock,
            "p_blk_detail": p_blk_detail,
            # TODO hard core
            "p_blk_charge": [
                {
                    "CHARGE_NAME": "",
                    "CHARGE_AMOUNT": 0,
                    "WAIVED": "N"
                }
            ],
            # TODO hard core
            "p_blk_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": "",
                    "AMOUNT_UNBLOCK": {
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
        gw_payment_amount_unblock = self.call_repos(await repos_gw_payment_amount_unblock(
            data_input=data_input,
            current_user=current_user
        ))
        return self.response(data=gw_payment_amount_unblock)
