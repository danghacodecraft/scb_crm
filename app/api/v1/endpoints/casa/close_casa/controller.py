from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.close_casa.repository import (
    repos_save_close_casa_account
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_account_id_by_account_number
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import BUSINESS_TYPE_CLOSE_CASA
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_CLOSE_CASA_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.functions import now, orjson_dumps


class CtrCloseCasa(BaseController):
    async def ctr_close_casa(
            self,
            close_casa_request: List,
            BOOKING_ID: str,
    ):
        current_user = self.current_user
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_CLOSE_CASA,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )
        close_account_list = []
        account_numbers = []
        blk_closure = {
            "CLOSE_MODE": "CASH",
            "ACCOUNT_NO": ""
        }

        for account in close_casa_request:
            if account.account_info.account_num in account_numbers:
                return self.response_exception(msg="Duplicate account_number")

            account_numbers.append(account.account_info.account_num)
            for item in account.p_blk_closure:
                if item.close_mode == "CASA":
                    if not item.account_number:
                        return self.response_exception(msg="CLOSE_MODE is not data")

                    blk_closure = {
                        "CLOSE_MODE": item.close_mode,
                        "ACCOUNT_NO": item.account_number
                    }
            close_account_list.append({
                "account_info": {
                    "account_number": account.account_info.account_num
                },
                "p_blk_closure": blk_closure,
                # TODO chưa được mô tả
                "p_blk_charge_main": "",
                "p_blk_charge_details": "",
                "p_blk_udf": "",
                # TODO hard core
                "staff_info_checker": {
                    "staff_name": "HOANT2"
                },
                "staff_info_maker": {
                    "staff_name": "KHANHLQ"
                }
            })
        saving_booking_account = []
        saving_booking_customer = []  # noqa

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
            business_type_id=BUSINESS_TYPE_CLOSE_CASA
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender
        ) = transaction_data

        history_data = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_CLOSE_CASA_ACCOUNT,
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

        booking_id = self.call_repos(await repos_save_close_casa_account(
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
            request_json=orjson_dumps(close_account_list),
            history_data=orjson_dumps(history_data),
            session=self.oracle_session
        ))
        response_data = {
            "booking_id": booking_id
        }
        return self.response(data=response_data)
