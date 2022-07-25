from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.casa.transfer.repository import (
    repos_get_casa_transfer_info
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_account_id_by_account_number
)
from app.api.v1.endpoints.config.bank.controller import CtrConfigBank
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_create_booking_payment, repos_gw_interbank_transfer,
    repos_gw_pay_in_cash, repos_gw_payment_amount_block,
    repos_gw_payment_amount_unblock, repos_gw_redeem_account,
    repos_gw_save_casa_transfer_info, repos_gw_tele_transfer,
    repos_gw_tt_liquidation, repos_pay_in_cash_247_by_acc_num,
    repos_pay_in_cash_247_by_card_num, repos_payment_amount_block,
    repos_payment_amount_unblock
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    RedeemAccountRequest
)
from app.api.v1.endpoints.third_parties.repository import (
    repos_save_gw_output_data
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.address import AddressProvince
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_CASA_TRANSFER, BUSINESS_TYPE_REDEEM_ACCOUNT
)
from app.utils.constant.casa import (
    RECEIVING_METHOD_SCB_BY_IDENTITY, RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_AMOUNT_BLOCK, BUSINESS_FORM_AMOUNT_UNBLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.constant.gw import (
    GW_ACCOUNT_CHARGE_ON_ORDERING, GW_ACCOUNT_CHARGE_ON_RECEIVER,
    GW_CORE_DATE_FORMAT, GW_DATE_FORMAT, GW_DATETIME_FORMAT,
    GW_FUNC_INTERNAL_TRANSFER_OUT, GW_GL_BRANCH_CODE,
    GW_RESPONSE_STATUS_SUCCESS
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_NO_INSTRUMENT_NUMBER
)
from app.utils.functions import (
    date_string_to_other_date_string_format, datetime_to_string, now,
    orjson_dumps, orjson_loads
)


class CtrGWPayment(BaseController):

    async def get_sender_info(self, form_data):
        sender_cif_number = form_data['sender_cif_number']
        if sender_cif_number:
            gw_customer_info = await CtrGWCustomer(self.current_user).ctr_gw_get_customer_info_detail(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            gw_customer_info_id_info = gw_customer_info['id_info']
            sender_full_name_vn = gw_customer_info['full_name']
            sender_address_full = gw_customer_info['t_address_info']['contact_address_full']
            sender_identity_number = gw_customer_info_id_info['id_num']
            sender_issued_date = date_string_to_other_date_string_format(
                date_input=gw_customer_info_id_info['id_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_CORE_DATE_FORMAT
            )

            sender_place_of_issue_id = gw_customer_info_id_info['id_issued_location']
        else:
            sender_full_name_vn = form_data['sender_full_name_vn']
            sender_address_full = form_data['sender_address_full']
            sender_identity_number = form_data['sender_identity_number']
            sender_issued_date = form_data['sender_issued_date']
            sender_place_of_issue_id = form_data['sender_place_of_issue']['id']
        sender_place_of_issue = await self.get_model_object_by_id(
            model_id=sender_place_of_issue_id,
            model=PlaceOfIssue,
            loc='sender_place_of_issue_id'
        )
        sender_place_of_issue = sender_place_of_issue.name

        return (
            sender_cif_number, sender_full_name_vn, sender_address_full, sender_identity_number, sender_issued_date,
            sender_place_of_issue
        )

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
                "p_blk_charge": "",
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

        # Tạo data TransactionDaily và các TransactionStage
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_AMOUNT_BLOCK,
            booking_id=BOOKING_ID,
            request_json=orjson_dumps(request_datas),
            history_datas=orjson_dumps(history_datas),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        booking_id = self.call_repos(await repos_payment_amount_block(
            booking_id=BOOKING_ID,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_transaction_job=saving_transaction_job,
            saving_booking_business_form=saving_booking_business_form,
            saving_booking_account=saving_booking_account,
            saving_booking_customer=saving_booking_customer,
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

        # Tạo data TransactionDaily và các TransactionStage
        transaction_data = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_AMOUNT_UNBLOCK,
            booking_id=BOOKING_ID,
            request_json=orjson_dumps(request_data),
            history_datas=orjson_dumps(history_data),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_data

        booking_id = self.call_repos(await repos_payment_amount_unblock(
            booking_id=BOOKING_ID,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_transaction_job=saving_transaction_job,
            saving_booking_business_form=saving_booking_business_form,
            saving_booking_account=saving_booking_account,
            saving_booking_customer=saving_booking_customer,
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
        if redeem_account.get('transaction_info').get('transaction_error_code') != GW_RESPONSE_STATUS_SUCCESS:
            return self.response_exception(msg=redeem_account.get('transaction_info').get('transaction_error_msg'))
        response_data = {
            "booking_id": booking_id,
        }
        return self.response(data=response_data)

    ####################################################################################################################
    # Nộp tiền
    ####################################################################################################################
    async def ctr_gw_pay_in_cash(
            self,
            form_data
    ):
        current_user = self.current_user
        sender_place_of_issue_id = form_data['sender_place_of_issue']['id']
        sender_place_of_issue = await self.get_model_object_by_id(
            model_id=sender_place_of_issue_id,
            model=PlaceOfIssue,
            loc=f"sender_place_of_issue_id: {sender_place_of_issue_id}"
        )

        data_input = {
            "account_info": {
                # "account_num": form_data['receiver_account_number'],
                "account_num": form_data['receiver_account_number'],
                "account_currency": "VND",  # TODO: hiện tại chuyển tiền chỉ dùng tiền tệ VN
                "account_opening_amount": form_data['amount']
            },
            "p_blk_denomination": "",
            "p_blk_charge": [
                {
                    "CHARGE_TYPE": "CASH",
                    "CHARGE_ACCOUNT": "",
                    "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                    "CHARGE_AMOUNT": 100000,
                    "WAIVED": "N"
                }
            ],
            "p_blk_project": "",
            "p_blk_mis": "",
            "p_blk_udf": [
                {
                    "UDF_NAME": "NGUOI_GIAO_DICH",
                    "UDF_VALUE": self.current_user.user_info.name
                },
                {
                    "UDF_NAME": "CMND_PASSPORT",
                    "UDF_VALUE": form_data['sender_identity_number'] if form_data['sender_identity_number'] else ''
                },
                {
                    "UDF_NAME": "NGAY_CAP",
                    "UDF_VALUE": form_data['sender_issued_date'] if form_data['sender_issued_date'] else ''
                },
                {
                    "UDF_NAME": "NOI_CAP",
                    "UDF_VALUE": sender_place_of_issue.name
                },
                {
                    "UDF_NAME": "DIA_CHI",
                    "UDF_VALUE": form_data['sender_address_full']
                },
                {
                    "UDF_NAME": "THU_PHI_DICH_VU",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "TEN_KHACH_HANG",
                    "UDF_VALUE": form_data['sender_full_name_vn']
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
            "staff_info_checker": {
                "staff_name": "HOANT2"
            },
            "staff_info_maker": {
                "staff_name": "KHANHLQ"
            }
        }
        print(data_input)
        gw_pay_in_cash = self.call_repos(await repos_gw_pay_in_cash(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_pay_in_cash

    async def ctr_tele_transfer(self, form_data, pay_in_cash_flag: bool = True):
        current_user = self.current_user
        receiver_place_of_issue_id = form_data['receiver_place_of_issue']['id']
        receiver_place_of_issue = await self.get_model_object_by_id(
            model_id=receiver_place_of_issue_id,
            model=PlaceOfIssue,
            loc='receiver_place_of_issue_id'
        )
        (
            sender_cif_number, sender_full_name_vn, sender_address_full, sender_identity_number, sender_issued_date,
            sender_place_of_issue
        ) = await self.get_sender_info(form_data=form_data)

        data_input = {
            "p_tt_type": "C" if pay_in_cash_flag else "A",
            "p_details": {
                "TT_DETAILS": {
                    "TT_CURRENCY": "VND",
                    "TT_AMOUNT": form_data['amount'],
                    "TRANSACTION_CURRENCY": "VND"
                },
                "BENEFICIARY_DETAILS": {
                    "BENEFICIARY_NAME": form_data['receiver_full_name_vn'],
                    "BENEFICIARY_PHONE_NO": form_data['receiver_mobile_number'],
                    "BENEFICIARY_ID_NO": form_data['receiver_identity_number'],
                    # "ID_ISSUE_DATE": date_string_to_other_date_string_format(
                    #     date_input=form_data['receiver_issued_date'],
                    #     from_format=GW_DATE_FORMAT,
                    #     to_format=GW_CORE_DATE_FORMAT
                    # ),
                    "ID_ISSUE_DATE": form_data['receiver_issued_date'],
                    "ID_ISSUER": receiver_place_of_issue.name,
                    "ADDRESS": form_data['receiver_address_full']
                },
                "REMITTER_DETAILS": {
                    "REMITTER_NAME": sender_full_name_vn,
                    "REMITTER_PHONE_NO": form_data['sender_mobile_number'],
                    "REMITTER_ID_NO": sender_identity_number,
                    "ID_ISSUE_DATE": date_string_to_other_date_string_format(
                        date_input=sender_issued_date,
                        from_format=GW_CORE_DATE_FORMAT,
                        to_format=GW_DATE_FORMAT
                    ),
                    "ID_ISSUER": sender_place_of_issue,
                    "ADDRESS": sender_address_full
                },
                "ADDITIONAL_DETAILS": {
                    "NARRATIVE": form_data['content']
                }
            },
            "p_denomination": "",
            "p_charges": [
                {
                    "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                    "CHARGE_AMOUNT": 100000,
                    "WAIVED": "N"
                }
            ],
            "p_mis": "",
            "p_udf": "",
            "staff_info_checker": {
                "staff_name": "HOANT2"
            },
            "staff_info_maker": {
                "staff_name": "KHANHLQ"
            }
        }
        if not pay_in_cash_flag:
            data_input["p_details"]["ACCOUNT_DETAILS"] = {
                "ACCOUNT_NUMBER": form_data['sender_account_number'],
                "CHARGE_BY_CASH": "N"
            }

        gw_tele_transfer = self.call_repos(await repos_gw_tele_transfer(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_tele_transfer

    async def ctr_tt_liquidation(self, p_instrument_number, form_data):
        current_user = self.current_user
        data_input = {
            "account_info": {
                "account_num": "123456787912",
                "account_currency": "VND"
            },
            "branch_info": {
                "branch_code": "000"
            },
            "p_liquidation_type": "C",
            "p_liquidation_details": "",
            "p_instrument_number": p_instrument_number,
            "p_instrument_status": "LIQD",
            "p_charges": [
                {
                    "CHARGE_NAME": "",
                    "CHARGE_AMOUNT": 0,
                    "WAIVED": "N"
                }
            ],
            "p_mis": "",
            "p_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": ""
                }
            ],
            "staff_info_checker": {
                "staff_name": "HOANT2"
            },
            "staff_info_maker": {
                "staff_name": "KHANHLQ"
            }
        }
        gw_tt_liquidation = self.call_repos(await repos_gw_tt_liquidation(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_tt_liquidation

    async def ctr_gw_interbank_transfer(
            self,
            booking_id: str,
            form_data: dict,
            receiving_method: str
    ):
        current_user = self.current_user

        ben = await CtrConfigBank(current_user).ctr_get_bank_branch(bank_id=form_data['receiver_bank']['id'])

        fee_info = form_data['fee_info']
        details_of_charge = ''
        if fee_info:
            if fee_info['is_transfer_payer'] is True:
                details_of_charge = GW_ACCOUNT_CHARGE_ON_ORDERING
            if fee_info['is_transfer_payer'] is False:
                details_of_charge = GW_ACCOUNT_CHARGE_ON_RECEIVER

        (
            sender_cif_number, sender_full_name_vn, sender_address_full, sender_identity_number, sender_issued_date,
            sender_place_of_issue
        ) = await self.get_sender_info(form_data=form_data)

        data_input = {}
        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            data_input.update({
                "account_info": {
                    "account_bank_code": ben['data'][0]['id'],
                    "account_product_package": "NC01"
                },
                "staff_info_checker": {
                    "staff_name": "DIEMNTK"     # TODO
                },
                "staff_info_maker": {
                    "staff_name": "DIEPTTN1"    # TODO
                },
                "p_blk_mis": "",
                "p_blk_udf": "",
                "p_blk_refinance_rates": "",
                "p_blk_amendment_rate": "",
                "p_blk_main": {
                    "PRODUCT": {
                        "DETAILS_OF_CHARGE": details_of_charge,
                        "PAYMENT_FACILITY": "O"
                    },
                    "TRANSACTION_LEG": {
                        "ACCOUNT": "101101001",
                        "AMOUNT": form_data['amount']
                    },
                    "RATE": {
                        "EXCHANGE_RATE": 0,
                        "LCY_EXCHANGE_RATE": 0,
                        "LCY_AMOUNT": 0
                    },
                    "ADDITIONAL_INFO": {
                        "RELATED_CUSTOMER": form_data['sender_cif_number'],
                        "NARRATIVE": form_data['content']
                    }
                },
                "p_blk_charge": [
                    {
                        "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                        "CHARGE_AMOUNT": 10000,
                        "WAIVED": "N"
                    },
                    {
                        "CHARGE_NAME": "THUE VAT",
                        "CHARGE_AMOUNT": 0,
                        "WAIVED": "N"
                    }
                ],
                "p_blk_settlement_detail": {
                    "SETTLEMENTS": {
                        "TRANSFER_DETAIL": {
                            "BENEFICIARY_ACCOUNT_NUMBER": form_data['receiver_account_number'],
                            "BENEFICIARY_NAME": form_data['receiver_full_name_vn'],
                            "BENEFICIARY_ADRESS": form_data['receiver_address_full'],
                            "ID_NO": '',
                            "ISSUE_DATE": "",
                            "ISSUER": ""
                        },
                        "ORDERING_CUSTOMER": {
                            "ORDERING_ACC_NO": "",
                            "ORDERING_NAME": sender_full_name_vn,
                            "ORDERING_ADDRESS": sender_address_full,
                            "ID_NO": sender_identity_number,
                            "ISSUE_DATE": sender_issued_date,
                            "ISSUER": sender_place_of_issue
                        }
                    }
                }
            })

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            receiver_place_of_issue_id = form_data['receiver_place_of_issue']['id']
            receiver_place_of_issue = await self.get_model_object_by_id(
                model_id=receiver_place_of_issue_id,
                model=PlaceOfIssue,
                loc='receiver_place_of_issue_id'
            )
            data_input.update({
                "account_info": {
                    "account_bank_code": ben['data'][0]['id'],
                    "account_product_package": "NC01"
                },
                "staff_info_checker": {
                    "staff_name": "DIEMNTK"     # TODO
                },
                "staff_info_maker": {
                    "staff_name": "DIEPTTN1"    # TODO
                },
                "p_blk_mis": "",
                "p_blk_udf": "",
                "p_blk_refinance_rates": "",
                "p_blk_amendment_rate": "",
                "p_blk_main": {
                    "PRODUCT": {
                        "DETAILS_OF_CHARGE": details_of_charge,
                        "PAYMENT_FACILITY": "O"
                    },
                    "TRANSACTION_LEG": {
                        "ACCOUNT": "101101001",
                        "AMOUNT": form_data['amount']
                    },
                    "RATE": {
                        "EXCHANGE_RATE": 0,
                        "LCY_EXCHANGE_RATE": 0,
                        "LCY_AMOUNT": 0
                    },
                    "ADDITIONAL_INFO": {
                        "RELATED_CUSTOMER": form_data['sender_cif_number'],
                        "NARRATIVE": form_data['content']
                    }
                },
                "p_blk_charge": [
                    {
                        "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                        "CHARGE_AMOUNT": 10000,
                        "WAIVED": "N"
                    },
                    {
                        "CHARGE_NAME": "THUE VAT",
                        "CHARGE_AMOUNT": 0,
                        "WAIVED": "N"
                    }
                ],
                "p_blk_settlement_detail": {
                    "SETTLEMENTS": {
                        "TRANSFER_DETAIL": {
                            "BENEFICIARY_ACCOUNT_NUMBER": '.',  # TODO
                            "BENEFICIARY_NAME": form_data['receiver_full_name_vn'],
                            "BENEFICIARY_ADRESS": form_data['receiver_address_full'],
                            "ID_NO": form_data['receiver_identity_number'],
                            "ISSUE_DATE": date_string_to_other_date_string_format(
                                date_input=form_data['receiver_issued_date'],
                                from_format=GW_DATE_FORMAT,
                                to_format=GW_CORE_DATE_FORMAT
                            ),
                            "ISSUER": receiver_place_of_issue.name
                        },
                        "ORDERING_CUSTOMER": {
                            "ORDERING_ACC_NO": "",
                            "ORDERING_NAME": sender_full_name_vn,
                            "ORDERING_ADDRESS": sender_address_full,
                            "ID_NO": sender_identity_number,
                            "ISSUE_DATE": sender_issued_date,
                            "ISSUER": sender_place_of_issue
                        }
                    }
                }
            })

        gw_interbank_transfer = self.call_repos(await repos_gw_interbank_transfer(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_interbank_transfer

    async def ctr_gw_pay_in_cash_247_by_acc_num(
            self,
            booking_id: str,
            form_data: dict
    ):
        current_user = self.current_user
        current_user_info = current_user.user_info

        ben = await CtrConfigBank(current_user).ctr_get_bank_branch(bank_id=form_data['receiver_bank']['id'])

        data_input = {
            "customer_info": {
                "full_name": form_data['sender_full_name_vn'],
                "birthday": date_string_to_other_date_string_format(
                    date_input=form_data['sender_issued_date'],
                    from_format=GW_DATETIME_FORMAT,
                    to_format=GW_DATE_FORMAT
                )
            },
            "id_info": {
                "id_num": form_data['sender_identity_number']
            },
            "address_info": {
                "address_full": form_data['sender_address_full']
            },
            "trans_date": datetime_to_string(now()),
            "time_stamp": datetime_to_string(now()),
            "trans_id": booking_id,
            "amount": form_data['amount'],
            "description": form_data['content'],
            "account_to_info": {
                "account_num": form_data['receiver_account_number']
            },
            "ben_id": ben['data'][0]['id'],
            "account_from_info": {
                "account_num": GW_GL_BRANCH_CODE
            },
            "staff_maker": {
                "staff_code": "annvh"   # TODO
            },
            "staff_checker": {
                "staff_code": "THUYTP"  # TODO
            },
            "branch_info": {
                "branch_code": current_user_info.hrm_branch_code
            }
        }
        gw_pay_in_cash_247_by_acc_num = self.call_repos(await repos_pay_in_cash_247_by_acc_num(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_pay_in_cash_247_by_acc_num

    async def ctr_gw_pay_in_cash_247_by_card_num(
            self,
            booking_id: str,
            form_data: dict
    ):
        current_user = self.current_user
        current_user_info = current_user.user_info

        ben = await CtrConfigBank(current_user).ctr_get_bank_branch(bank_id=form_data['receiver_bank']['id'])

        data_input = {
            "customer_info": {
                "full_name": form_data['sender_full_name_vn'],
                "birthday": date_string_to_other_date_string_format(
                    date_input=form_data['sender_issued_date'],
                    from_format=GW_DATETIME_FORMAT,
                    to_format=GW_DATE_FORMAT
                )
            },
            "id_info": {
                "id_num": form_data['sender_identity_number']
            },
            "address_info": {
                "address_full": form_data['sender_address_full']
            },
            "trans_date": datetime_to_string(now()),
            "time_stamp": datetime_to_string(now()),
            "trans_id": booking_id,
            "amount": form_data['amount'],
            "description": form_data['content'],
            "card_to_info": {
                "card_num": form_data['receiver_card_number']
            },
            "ben_id": ben['data'][0]['id'],
            "account_from_info": {
                "account_num": "101101001"
            },
            "staff_maker": {
                "staff_code": "annvh"   # TODO
            },
            "staff_checker": {
                "staff_code": "THUYTP"  # TODO
            },
            "branch_info": {
                "branch_code": current_user_info.hrm_branch_code
            }
        }
        gw_pay_in_cash_247_by_card_num = self.call_repos(await repos_pay_in_cash_247_by_card_num(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_pay_in_cash_247_by_card_num

    async def ctr_gw_save_casa_transfer_info(self, BOOKING_ID: str):
        current_user = self.current_user
        get_casa_transfer_info = self.call_repos(await repos_get_casa_transfer_info(
            booking_id=BOOKING_ID,
            session=self.oracle_session
        ))
        form_data = orjson_loads(get_casa_transfer_info.form_data)
        receiving_method = form_data['receiving_method']
        transfer_amount = form_data['amount']

        # Thông tin phí
        ################################################################################################################
        fee_info = {}
        if form_data['is_fee']:
            fee_info = form_data['fee_info']
            fee_amount = fee_info['fee_amount']
            vat_tax = fee_amount / 10
            total = fee_amount + vat_tax
            actual_total = total + transfer_amount
            is_transfer_payer = False
            payer = None
            if fee_info['is_transfer_payer'] is not None:
                payer = "RECEIVER"
                if fee_info['is_transfer_payer'] is True:
                    is_transfer_payer = True
                    payer = "SENDER"
        else:
            fee_amount = None
            vat_tax = None
            total = None
            actual_total = transfer_amount
            is_transfer_payer = None
            payer = None

        fee_info.update(dict(
            fee_amount=fee_amount,
            vat_tax=vat_tax,
            total=total,
            actual_total=actual_total,
            is_transfer_payer=is_transfer_payer,
            payer=payer,
            note=form_data['fee_info']['note']
        ))

        request_data = {}

        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            request_data = {
                "data_input": {
                    "p_blk_detail": {
                        "FROM_ACCOUNT_NUMBER": form_data['sender_account_number'],
                        "FROM_ACCOUNT_AMOUNT": actual_total,
                        "TO_ACCOUNT_NUMBER": form_data['receiver_account_number']
                    },
                    "p_blk_charge": [],  # TODO thông tin phí
                    "p_blk_mis": "",
                    "p_blk_udf": [
                        {
                            "UDF_NAME": "",
                            "UDF_VALUE": ""
                        }
                    ],
                    "p_blk_project": "",
                    # TODO
                    "staff_info_checker": {
                        "staff_name": "HOANT2"
                    },
                    # TODO
                    "staff_info_maker": {
                        "staff_name": "KHANHLQ"
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
            is_success, tele_transfer_response_data = await self.ctr_tele_transfer(
                form_data=form_data, pay_in_cash_flag=False
            )
            if not is_success:
                return self.response_exception(
                    loc='tele_transfer',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(tele_transfer_response_data)
                )
            p_instrument_number = tele_transfer_response_data[GW_FUNC_INTERNAL_TRANSFER_OUT]['data_output']['p_instrument_number']

            if p_instrument_number == '':
                return self.response_exception(
                    loc='tele_transfer',
                    msg=ERROR_NO_INSTRUMENT_NUMBER,
                    detail=str(tele_transfer_response_data)
                )

            request_data = {
                "data_input": {
                    "p_liquidation_type": "A",
                    "p_liquidation_details": "",
                    "branch_info": {
                        "branch_code": "000"  # TODO
                    },
                    "p_instrument_number": p_instrument_number,
                    "p_instrument_status": "LIQD",
                    "account_info": {
                        "account_num": form_data['sender_account_number'],
                        "account_currency": "VND"
                    },
                    "p_charges": [
                        {
                            "CHARGE_NAME": "",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_mis": "",
                    "p_udf": [
                        {
                            "UDF_NAME": "",
                            "UDF_VALUE": ""
                        }
                    ],
                    "staff_info_checker": {
                        "staff_name": "HOANT2"  # TODO
                    },
                    "staff_info_maker": {
                        "staff_name": "KHANHLQ"  # TODO
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            details_of_charge = ''
            if fee_info:
                if fee_info['is_transfer_payer'] is True:
                    details_of_charge = GW_ACCOUNT_CHARGE_ON_ORDERING
                if fee_info['is_transfer_payer'] is False:
                    details_of_charge = GW_ACCOUNT_CHARGE_ON_RECEIVER

            (
                sender_cif_number, sender_full_name_vn, sender_address_full, sender_identity_number, sender_issued_date,
                sender_place_of_issue
            ) = await self.get_sender_info(form_data=form_data)
            receiver_place_of_issue_id = form_data['receiver_place_of_issue']['id']
            receiver_place_of_issue = await self.get_model_object_by_id(
                model_id=receiver_place_of_issue_id,
                model=PlaceOfIssue,
                loc='receiver_place_of_issue_id'
            )
            ben = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
                bank_id=form_data['receiver_bank']['id'])
            request_data = {
                "data_input": {
                    "account_info": {
                        "account_bank_code": ben['data'][0]['id'],
                        "account_product_package": "FT01"
                    },
                    "staff_info_checker": {
                        "staff_name": "DIEMNTK"  # TODO
                    },
                    "staff_info_maker": {
                        "staff_name": "DIEPTTN1"  # TODO
                    },
                    "p_blk_mis": "",
                    "p_blk_udf": "",
                    "p_blk_refinance_rates": "",
                    "p_blk_amendment_rate": "",
                    "p_blk_main": {
                        "PRODUCT": {
                            "DETAILS_OF_CHARGE": details_of_charge,
                            "PAYMENT_FACILITY": "O"
                        },
                        "TRANSACTION_LEG": {
                            "ACCOUNT": form_data['sender_account_number'],
                            "AMOUNT": form_data['amount']
                        },
                        "RATE": {
                            "EXCHANGE_RATE": 0,
                            "LCY_EXCHANGE_RATE": 0,
                            "LCY_AMOUNT": 0
                        },
                        "ADDITIONAL_INFO": {
                            "RELATED_CUSTOMER": form_data['sender_cif_number'],
                            "NARRATIVE": form_data['content']
                        }
                    },
                    "p_blk_charge": [
                        {
                            "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        },
                        {
                            "CHARGE_NAME": "THUE VAT",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_blk_settlement_detail": {
                        "SETTLEMENTS": {
                            "TRANSFER_DETAIL": {
                                "BENEFICIARY_ACCOUNT_NUMBER": ".",
                                "BENEFICIARY_NAME": form_data['receiver_full_name_vn'],
                                "BENEFICIARY_ADRESS": form_data['receiver_address_full'],
                                "ID_NO": form_data['receiver_identity_number'],
                                "ISSUE_DATE": date_string_to_other_date_string_format(
                                    date_input=form_data['receiver_issued_date'],
                                    from_format=GW_DATE_FORMAT,
                                    to_format=GW_CORE_DATE_FORMAT
                                ),
                                "ISSUER": receiver_place_of_issue.name
                            },
                            "ORDERING_CUSTOMER": {
                                "ORDERING_ACC_NO": "",
                                "ORDERING_NAME": sender_full_name_vn,
                                "ORDERING_ADDRESS": sender_address_full,
                                "ID_NO": sender_identity_number,
                                "ISSUE_DATE": date_string_to_other_date_string_format(
                                    date_input=sender_issued_date,
                                    from_format=GW_DATE_FORMAT,
                                    to_format=GW_CORE_DATE_FORMAT
                                ),
                                "ISSUER": sender_place_of_issue
                            }
                        }
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            bank_info = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
                bank_id=form_data['receiver_bank']['id'])

            receiver_province_id = form_data['receiver_province']['id']
            province = await self.get_model_object_by_id(
                model_id=receiver_province_id,
                model=AddressProvince,
                loc=f'receiver_province_id: {receiver_province_id}'
            )
            request_data = {
                "data_input": {
                    "account_info": {
                        "account_bank_code": bank_info['data'][0]['code'],
                        "account_product_package": "FT01"
                    },
                    "staff_info_checker": {
                        "staff_name": "HOANT2"
                    },
                    "staff_info_maker": {
                        "staff_name": "KHANHLQ"
                    },
                    "p_blk_mis": "",
                    "p_blk_udf": "",
                    "p_blk_refinance_rates": "",
                    "p_blk_amendment_rate": "",
                    "p_blk_main": {
                        "PRODUCT": {
                            "DETAILS_OF_CHARGE": "Y" if is_transfer_payer else "O",
                            "PAYMENT_FACILITY": "O"
                        },
                        "TRANSACTION_LEG": {
                            "ACCOUNT": form_data['sender_account_number'],
                            "AMOUNT": actual_total
                        },
                        "RATE": {
                            "EXCHANGE_RATE": 0,
                            "LCY_EXCHANGE_RATE": 0,
                            "LCY_AMOUNT": 0
                        },
                        "ADDITIONAL_INFO": {
                            "RELATED_CUSTOMER": form_data["sender_cif_number"],
                            "NARRATIVE": form_data["content"]
                        }
                    },
                    "p_blk_charge": [
                        {
                            "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        },
                        {
                            "CHARGE_NAME": "THUE VAT",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_blk_settlement_detail": {
                        "SETTLEMENTS": {
                            "TRANSFER_DETAIL": {
                                "BENEFICIARY_ACCOUNT_NUMBER": form_data['receiver_account_number'],
                                "BENEFICIARY_NAME": form_data['receiver_full_name_vn'],
                                "BENEFICIARY_ADRESS": province.code,
                                "ID_NO": "",
                                "ISSUE_DATE": "",
                                "ISSUER": ""
                            },
                            "ORDERING_CUSTOMER": {
                                "ORDERING_ACC_NO": form_data['receiver_account_number'],
                                "ORDERING_NAME": form_data['receiver_full_name_vn'],
                                "ORDERING_ADDRESS": province.code,
                                "ID_NO": "",
                                "ISSUE_DATE": "",
                                "ISSUER": ""
                            }
                        }
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
            # ben = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
            #     bank_id=form_data['receiver_bank']['id'])

            request_data = {
                "data_input": {
                    # "ben_id": ben['data'][0]['id'],
                    "ben_id": "970436",  # TODO
                    "trans_date": datetime_to_string(now()),
                    "time_stamp": datetime_to_string(now()),
                    "trans_id": "20220629160002159368",
                    "amount": actual_total,
                    "description": form_data["content"],
                    "account_to_info": {
                        "account_num": form_data["receiver_account_number"]
                    },
                    "account_from_info": {
                        "account_num": form_data["sender_account_number"]
                    },
                    "customer_info": {
                        "full_name": form_data["sender_full_name_vn"]
                    },
                    # TODO
                    "staff_maker": {
                        "staff_code": "annvh"
                    },
                    # TODO
                    "staff_checker": {
                        "staff_code": "THUYTP"
                    },
                    # TODO
                    "branch_info": {
                        "branch_code": "001"
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            # ben = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
            #     bank_id=form_data['receiver_bank']['id'])

            request_data = {
                "data_input": {
                    # "ben_id": ben['data'][0]['id'],
                    "ben_id": "970436",  # TODO hard core chưa thông tin ngân hàng khác
                    "trans_date": datetime_to_string(now()),
                    "time_stamp": datetime_to_string(now()),
                    "trans_id": "20220629160002159368",
                    "amount": actual_total,
                    "description": form_data["content"],
                    "account_from_info": {
                        "account_num": form_data["sender_account_number"]
                    },
                    "customer_info": {
                        "full_name": form_data["sender_full_name_vn"]
                    },
                    # TODO
                    "staff_maker": {
                        "staff_code": "annvh"
                    },
                    # TODO
                    "staff_checker": {
                        "staff_code": "THUYTP"
                    },
                    # TODO
                    "branch_info": {
                        "branch_code": "001"
                    },
                    "card_to_info": {
                        "card_num": form_data["receiver_card_number"]
                    }
                }
            }
        response_data, gw_casa_transfer = self.call_repos(await repos_gw_save_casa_transfer_info(
            current_user=self.current_user,
            receiving_method=receiving_method,
            booking_id=BOOKING_ID,
            request_data=request_data,
            session=self.oracle_session
        ))

        self.call_repos(await repos_save_gw_output_data(
            booking_id=BOOKING_ID,
            business_type_id=BUSINESS_TYPE_CASA_TRANSFER,
            gw_output_data=orjson_dumps(gw_casa_transfer),
            session=self.oracle_session
        ))

        return self.response(data=response_data)
    ####################################################################################################################
