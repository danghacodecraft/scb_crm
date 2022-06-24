from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_account_id_by_account_number
)
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_create_booking_payment, repos_gw_pay_in_cash,
    repos_gw_payment_amount_block, repos_gw_payment_amount_unblock,
    repos_gw_redeem_account, repos_payment_amount_block,
    repos_payment_amount_unblock
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    PayInCashRequest, RedeemAccountRequest
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_REDEEM_ACCOUNT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_AMOUNT_BLOCK, BUSINESS_FORM_AMOUNT_UNBLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.constant.gw import GW_CASA_RESPONSE_STATUS_SUCCESS
from app.utils.functions import now, orjson_dumps, orjson_loads


class CtrGWPayment(BaseController):

    async def ctr_payment_amount_block(
            self,
            BOOKING_ID: str,
            account_amount_blocks: list
    ):
        current_user = self.current_user # noqa

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_AMOUNT_BLOCK,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )
        request_datas = []
        account_numbers = []
        for item in account_amount_blocks:
            account_numbers.append(item.account_number)
            request_datas.append({
                "account_info": {
                    "account_num": item.account_number
                },
                "p_blk_detail": {
                    "AMOUNT": item.amount,
                    "AMOUNT_BLOCK_TYPE": item.amount_block_type,
                    "HOLD_CODE": item.hold_code,
                    "EFFECTIVE_DATE": item.effective_date,
                    "EXPIRY_DATE": item.expiry_date if item.expiry_date else "",
                    "REMARKS": item.remarks,
                    "VERIFY_AVAILABLE_BALANCE": item.verify_available_balance,
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
            })

        if len(set(account_numbers)) != len(account_amount_blocks):
            return self.response_exception(msg="account_number duplicate")

        saving_booking_account = []
        saving_booking_customer = [] # noqa

        for account_number in account_numbers:
            # TODO check account_number in db crm
            response_data = self.call_repos(
                await repos_get_account_id_by_account_number(
                    account_number=account_number,
                    session=self.oracle_session
                ))

            saving_booking_account.append({
                "booking_id": BOOKING_ID,
                "account_id": response_data.get('account_id'),
                "created_at": now()
            })

            saving_booking_customer.append({
                "booking_id": BOOKING_ID,
                "customer_id": response_data.get('customer_id')
            })
        # Tạo data TransactionDaily và các TransactionStage
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            business_type_id=BUSINESS_TYPE_AMOUNT_BLOCK
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender
        ) = transaction_datas

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user.user_info
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_datas)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        booking_id = self.call_repos(await repos_payment_amount_block(
            booking_id=BOOKING_ID,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_booking_account=saving_booking_account,
            saving_booking_customer=saving_booking_customer,
            request_json=orjson_dumps(request_datas),
            history_datas=orjson_dumps(history_datas),
            session=self.oracle_session
        ))
        response_data = {
            "booking_id": booking_id
        }

        return self.response(data=response_data)

    async def ctr_gw_payment_amount_block(self, BOOKING_ID: str):
        current_user = self.current_user

        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=BOOKING_ID,
                business_form_id=BUSINESS_FORM_AMOUNT_BLOCK,
                session=self.oracle_session

            ))

        request_data_gw = orjson_loads(booking_business_form.form_data)

        gw_payment_amount_block = self.call_repos(await repos_gw_payment_amount_block(
            current_user=current_user,
            booking_id=BOOKING_ID,
            request_data_gw=request_data_gw,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": BOOKING_ID,
            "account_list": gw_payment_amount_block
        }

        return self.response(data=response_data)

    async def ctr_payment_amount_unblock(
            self,
            BOOKING_ID: str,
            account_amount_unblocks: list
    ):
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_AMOUNT_UNBLOCK,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )

        current_user = self.current_user
        request_data = []
        account_ref = []
        account_numbers = []
        for account_number in account_amount_unblocks:
            if account_number.account_number in account_numbers:
                return self.response_exception(msg="Duplicate Account_number", detail=f"Account_number {account_number.account_number}")

            account_numbers.append(account_number.account_number)
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
            for account_amount in account_number.account_amount_block:
                if account_amount.account_ref_no in account_ref:
                    return self.response_exception(msg="Duplicate Account_ref", detail=f"Account_ref {account_amount.account_ref_no}")
                account_ref.append(account_amount.account_ref_no)
                if account_amount.p_type_unblock == "P":
                    if not account_amount.p_blk_detail:
                        return self.response_exception(msg="type_unblock is not data")

                    p_blk_detail = {
                        "AMOUNT": account_amount.p_blk_detail.amount,
                        "HOLD_CODE": account_amount.p_blk_detail.hold_code,
                        "EXPIRY_DATE": account_amount.p_blk_detail.expiry_date,
                        "REMARKS": account_amount.p_blk_detail.remarks,
                        "CHARGE_DETAIL": {
                            "TYPE_CHARGE": "",
                            "ACCOUNT_CHARGE": ""
                        }
                    }

                request_data.append({
                    "account_info": {
                        "balance_lock_info": {
                            "account_ref_no": account_amount.account_ref_no
                        }
                    },
                    "p_type_unblock": account_amount.p_type_unblock,
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
                })

        saving_booking_account = []
        saving_booking_customer = []

        for account_number in account_numbers:
            # TODO check account_number in db crm
            response_data = self.call_repos(
                await repos_get_account_id_by_account_number(
                    account_number=account_number,
                    session=self.oracle_session
                ))
            saving_booking_account.append({
                "booking_id": BOOKING_ID,
                "account_id": response_data.get('account_id'),
                "created_at": now()
            })

            saving_booking_customer.append({
                "booking_id": BOOKING_ID,
                "customer_id": response_data.get('customer_id')
            })
        # Tạo data TransactionDaily và các TransactionStage
        transaction_data = await self.ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            business_type_id=BUSINESS_TYPE_AMOUNT_UNBLOCK
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender
        ) = transaction_data

        history_data = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user.user_info
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_data)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        booking_id = self.call_repos(await repos_payment_amount_unblock(
            booking_id=BOOKING_ID,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_booking_account=saving_booking_account,
            saving_booking_customer=saving_booking_customer,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            request_json=orjson_dumps(request_data),
            history_data=orjson_dumps(history_data),
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": booking_id,
        }
        return self.response(data=response_data)

    async def ctr_gw_payment_amount_unblock(
            self,
            BOOKING_ID: str,
    ):
        current_user = self.current_user
        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=BOOKING_ID,
                business_form_id=BUSINESS_FORM_AMOUNT_UNBLOCK,
                session=self.oracle_session

            ))
        request_data = orjson_loads(booking_business_form.form_data)

        gw_payment_amount_unblock = self.call_repos(await repos_gw_payment_amount_unblock(
            current_user=current_user,
            booking_id=BOOKING_ID,
            request_data_gw=request_data,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": BOOKING_ID,
            "account_list": gw_payment_amount_unblock
        }
        return self.response(data=response_data)

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

    async def ctr_gw_redeem_account(self, redeem_account: RedeemAccountRequest):
        current_user = self.current_user
        payout_details = [{
            "payout_component": item.payout_component,
            "payout_mode": item.payout_mode,
            "payout_amount": item.payout_amount,
            "offset_account": item.offset_account
        } for item in redeem_account.p_payout_detail.payout_details]
        data_input = {
            "account_info": {
                "account_num": redeem_account.account_info.account_number,
            },
            "p_payout_detail": {
                "redemption_details": {
                    "redemption_mode": redeem_account.p_payout_detail.redemption_details.redemption_mode,
                    "redemption_amount": redeem_account.p_payout_detail.redemption_details.redemption_amount,
                    "waive_penalty": redeem_account.p_payout_detail.redemption_details.waive_penalty,
                    "waive_interest": redeem_account.p_payout_detail.redemption_details.waive_interest
                },
                "payout_details": payout_details
            },
            # TODO hard core
            "p_denominated_deposit": "",
            "p_addl_payout_detail": "",
            "p_charges": "",
            "p_denomination": "",
            "p_mis": "",
            "p_udf": [
                {
                    "UDF_NAME": "",
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
        request_data, gw_payment_redeem_account = self.call_repos(
            await repos_gw_redeem_account(
                current_user=current_user,
                data_input=data_input,
            )
        )

        booking_id, booking_code = self.call_repos(await repos_create_booking_payment(
            business_type_code=BUSINESS_TYPE_REDEEM_ACCOUNT,
            current_user=current_user.user_info,
            form_data=request_data,
            log_data=gw_payment_redeem_account,
            session=self.oracle_session
        ))

        redeem_account = gw_payment_redeem_account.get('redeemAccount_out', {})
        # check trường hợp lỗi
        if redeem_account.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
            return self.response_exception(msg=redeem_account.get('transaction_info').get('transaction_error_msg'))
        response_data = {
            "booking_id": booking_id,
        }
        return self.response(data=response_data)
