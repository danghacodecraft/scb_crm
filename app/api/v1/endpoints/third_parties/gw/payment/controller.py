from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_gw_pay_in_cash, repos_gw_payment_amount_block,
    repos_gw_payment_amount_unblock
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    AccountAmountBlockRequest, AccountAmountUnblock, PayInCashRequest
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
            "account_ref_no":
                gw_payment_amount_block['amountBlock_out']['data_output']['account_info']['blance_lock_info'][
                    'account_ref_no']
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

    async def ctr_gw_pay_in_cash(self, pay_in_cash: PayInCashRequest):
        current_user = self.current_user

        data_input = {
            "account_info": {
                "account_num": pay_in_cash.account_number,
                "account_currency": pay_in_cash.account_currency,
                "account_opening_amount": pay_in_cash.account_opening_amount
            },
            "p_blk_denomination": "",
            "p_blk_charge": pay_in_cash.p_blk_charge,
            "p_blk_project": "",
            "p_blk_mis": "",
            # TODO hard core
            "p_blk_udf": [
                {
                    "UDF_NAME": "NGUOI_GIAO_DICH",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "CMND_PASSPORT",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "NGAY_CAP",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "NOI_CAP",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "DIA_CHI",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "THU_PHI_DICH_VU",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "TEN_KHACH_HANG",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "TY_GIA_GD_DOI_UNG_HO",
                    "UDF_VALUE": "1"
                },
                {
                    "UDF_NAME": "MUC_DICH_GIAO_DICH",
                    "UDF_VALUE": "MUC_DICH_KHAC"
                },
                {
                    "UDF_NAME": "NGHIEP_VU_GDQT",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "NGAY_CHOT_TY_GIA",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "GIO_PHUT_CHOT_TY_GIA",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_1",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_2",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_3",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_4",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_5",
                    "UDF_VALUE": ""
                }
            ],
            # TODO hard core
            "staff_info_checker": {
                "staff_name": "HOANT2"
            },
            # TODO hard core
            "staff_info_maker": {
                "staff_name": "KHANHLQ"
            }
        }
        gw_pay_in_cash = self.call_repos(await repos_gw_pay_in_cash(
            data_input=data_input,
            current_user=current_user
        ))
        return self.response(data=gw_pay_in_cash)
