from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_balance_saving_account_data, repos_get_detail_reset_password,
    repos_get_detail_reset_password_teller, repos_get_e_banking,
    repos_get_payment_accounts, repos_get_sms_data, repos_save_e_banking,
    repos_save_sms_casa
)
from app.api.v1.endpoints.cif.e_banking.schema import (
    EBankingRequest, EBankingSMSCasaRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_booking
from app.api.v1.validator import validate_history_data
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING,
    PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING_SMS_CASA,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.functions import orjson_dumps


class CtrEBanking(BaseController):
    ####################################################################################################################
    # Đăng ký Ebanking
    ####################################################################################################################

    # @ TODO: đăng ký SMS CASA bên GW chỉ cần nhập SĐT, các field khác khi nào bên GW cần sẽ làm sau.
    async def ctr_save_e_banking_and_sms(self, cif_id: str, e_banking_info: EBankingRequest,
                                         ebank_sms_casa_info: EBankingSMSCasaRequest = None):

        current_user = self.current_user
        current_user_info = current_user.user_info

        save_e_banking_info = None
        save_sms_casa_info = None

        if e_banking_info:
            ebank_ibmb_username = e_banking_info.username
            ebank_ibmb_receive_password_code = e_banking_info.receive_password_code
            authentication_code_list = e_banking_info.authentication_code_list

            # dữ liệu để tạo ebanking trong DB
            data_insert = {
                "ebank_info": {
                    "customer_id": cif_id,
                    "account_name": ebank_ibmb_username,
                    "method_active_password_id": ebank_ibmb_receive_password_code,
                },
                "ebank_info_authen_list": [{
                    "method_authentication_id": authentication_code
                } for authentication_code in authentication_code_list]
            }

            history_datas = self.make_history_log_data(
                description=PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING,
                history_status=PROFILE_HISTORY_STATUS_INIT,
                current_user=current_user_info
            )
            # Validate history data
            is_success, history_response = validate_history_data(history_datas)
            if not is_success:
                return self.response_exception(
                    msg=history_response['msg'],
                    loc=history_response['loc'],
                    detail=history_response['detail']
                )

            save_e_banking_info = self.call_repos(
                await repos_save_e_banking(
                    cif_id=cif_id,
                    data_insert=data_insert,
                    log_data=e_banking_info.json(),
                    history_datas=orjson_dumps(history_datas),
                    created_by=current_user_info.username,
                    session=self.oracle_session
                ))

            # Lấy Booking Code
            booking = self.call_repos(await repos_get_booking(
                cif_id=cif_id, session=self.oracle_session
            ))
            save_e_banking_info.update(booking=dict(
                id=booking.id,
                code=booking.code
            ))

        if ebank_sms_casa_info:
            data_insert = {
                "casa_account_id": ebank_sms_casa_info.casa_account_id,
                "identity_phone_num_list": ebank_sms_casa_info.indentify_phone_num_list
            }

            history_datas = self.make_history_log_data(
                description=PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING_SMS_CASA,
                history_status=PROFILE_HISTORY_STATUS_INIT,
                current_user=current_user_info
            )
            # Validate history data
            is_success, history_response = validate_history_data(history_datas)
            if not is_success:
                return self.response_exception(
                    msg=history_response['msg'],
                    loc=history_response['loc'],
                    detail=history_response['detail']
                )

            save_sms_casa_info = self.call_repos(
                await repos_save_sms_casa(
                    cif_id=cif_id,
                    data_insert=data_insert,
                    log_data=ebank_sms_casa_info.json(),
                    history_datas=orjson_dumps(history_datas),
                    created_by=current_user_info.username,
                    session=self.oracle_session,
                ))
            # Lấy Booking Code
            booking = self.call_repos(await repos_get_booking(
                cif_id=cif_id, session=self.oracle_session
            ))
            save_sms_casa_info.update(booking=dict(
                id=booking.id,
                code=booking.code
            ))

        response_data = save_e_banking_info if save_e_banking_info else save_sms_casa_info

        return self.response(data=response_data)

    ####################################################################################################################
    # End: Đăng ký Ebanking
    ####################################################################################################################
    async def ctr_get_e_banking(self, cif_id: str):
        # 1. lấy data E-banking
        e_banking_result = await repos_get_e_banking(cif_id=cif_id, session=self.oracle_session)

        # 2. lấy data sms casa
        sms_casa_result = await repos_get_sms_data(cif_id=cif_id, session=self.oracle_session)

        response = dict(
            e_banking=e_banking_result.data if e_banking_result.data else None,
            sms_casa=sms_casa_result.data if sms_casa_result.data else None,
        )

        return self.response(data=response)

    async def ctr_balance_payment_account(self, cif_id: str):

        # Luồng tạo mới chỉ lấy tài khoản thanh toán trong DB
        # Lấy danh sách tài khoản thanh toán trong DB
        payment_accounts = self.call_repos(
            await repos_get_payment_accounts(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        payment_account_infos = []
        for casa_account, account_type in payment_accounts:
            payment_account_infos.append({
                "id": casa_account.id,
                "account_number": casa_account.casa_account_number,
                "product_name": account_type.name,
            })

        return self.response(data=payment_account_infos)

    async def get_detail_reset_password(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password(cif_id))

        return self.response(data=detail_reset_password_data)

    async def ctr_balance_saving_account(self, cif_id: str):
        balance_saving_account = self.call_repos(
            await repos_balance_saving_account_data(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        # response_data = []
        # if balance_saving_account:
        #     balance_saving_accounts = balance_saving_account['selectDepositAccountFromCIF_out']['accountInfo']
        #     for account in balance_saving_accounts:
        #         response_data.append({
        #             "id": account['customerInfo']['rowOrder'],
        #             "account_number": account['accountNum'],
        #             "name": account['customerInfo']['fullname'],
        #         })

        return self.response_paging(
            data=balance_saving_account,
            total_items=len(balance_saving_account)
        )

    async def get_detail_reset_password_teller(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password_teller(cif_id))

        return self.response(data=detail_reset_password_data)
