from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_balance_saving_account_data, repos_check_e_banking,
    repos_get_detail_reset_password, repos_get_detail_reset_password_teller,
    repos_get_e_banking_data, repos_get_payment_accounts, repos_save_e_banking,
    repos_save_sms_casa
)
from app.api.v1.endpoints.cif.e_banking.schema import (
    EBankingRequest, EBankingSMSCasaRequest, GetInitialPasswordMethod
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking, repos_get_initializing_customer
)
from app.api.v1.validator import validate_history_data
from app.utils.constant.cif import (
    EBANKING_ACCOUNT_TYPE_CHECKING,
    PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING,
    PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING_SMS_CASA,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.functions import dropdown, orjson_dumps


class CtrEBanking(BaseController):
    ####################################################################################################################
    # Đăng ký Ebanking
    ####################################################################################################################

    # @ TODO: đăng ký SMS CASA bên GW chỉ cần nhập SĐT, các field khác khi nào bên GW cần sẽ làm sau.
    async def ctr_save_e_banking_and_sms(self, cif_id: str, e_banking_info: EBankingRequest = None,
                                         ebank_sms_casa_info: EBankingSMSCasaRequest = None):

        current_user = self.current_user
        current_user_info = current_user.user_info

        save_e_banking_info = None
        save_sms_casa_info = None

        if not e_banking_info and not ebank_sms_casa_info:
            return self.response_exception(
                msg="Missing data, need at least e_banking_info or ebank_sms_casa_info"
            )

        if e_banking_info:
            ebank_ibmb_username = e_banking_info.username
            ebank_ibmb_receive_password_code = e_banking_info.receive_password_code
            authentication_code_list = e_banking_info.authentication_code_list

            # dữ liệu để tạo ebanking trong DB (CRM_EBANKING_INFO)
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
        """
        1. Kiểm tra tồn tại của cif_id
        2. Kiểm tra cif_id đã có E-banking chưa
        3. Trả data E-banking
        """

        # 1. Kiểm tra tồn tại của cif_id
        _ = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session))

        # 2. Kiểm tra cif_id đã có E-banking chưa
        data_e_banking = await repos_check_e_banking(cif_id=cif_id, session=self.oracle_session)
        if not data_e_banking:
            return self.response_exception(
                msg='ERROR_E-BANKING',
                loc='cif_id not have E-Banking',
                detail=f'E-Banking -> cif_id -> {cif_id}'
            )

        # 3. Trả data E-banking
        data = self.call_repos(
            await repos_get_e_banking_data(
                cif_id=cif_id,
                session=self.oracle_session))

        contact_types = data['contact_types']
        data_e_banking = data['data_e_banking']
        e_bank_info = data['e_bank_info']

        relationship_ids = []
        list_relationships = []

        notification_ids = []
        list_notification = []

        for item in data_e_banking:
            id_notification = item.EBankingNotification.id
            if id_notification not in notification_ids:
                notification_ids.append(id_notification)
                list_notification.append(item.EBankingNotification)

            if not item.EBankingReceiverNotificationRelationship:
                continue

            id_relationship = item.EBankingReceiverNotificationRelationship.id
            if id_relationship not in relationship_ids:
                relationship_ids.append(id_relationship)
                list_relationships.append(
                    (item.EBankingReceiverNotificationRelationship, item.CustomerRelationshipType))

        notification_casa_relationships = [
            {
                "id": relationship[0].id,
                "mobile_number": relationship[0].mobile_number,
                "full_name_vn": relationship[0].full_name,
                "relationship_type": dropdown(relationship[1])
            } for relationship in list_relationships
        ]

        e_banking_notifications = [
            {
                "id": notification.id,
                "code": notification.code,
                "name": notification.name,
                "checked_flag": notification.active_flag
            } for notification in list_notification
        ]

        checking_registration_info, saving_registration_info = {}, {}
        for register in data_e_banking:
            if register.EBankingRegisterBalance.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING:
                if not checking_registration_info.get(register.EBankingRegisterBalance.account_id):
                    checking_registration_info[
                        register.EBankingRegisterBalance.account_id] = register.EBankingRegisterBalance.__dict__
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"] = [
                        register.EBankingNotification]
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"] = [{
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    }]
                else:
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"].append(
                        register.EBankingNotification)
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"].append({
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    })
            else:
                if not saving_registration_info.get(register.EBankingRegisterBalance.account_id):
                    saving_registration_info[
                        register.EBankingRegisterBalance.account_id] = register.EBankingRegisterBalance.__dict__
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"] = [
                        register.EBankingNotification]
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"] = [{
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    }]
                else:
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"].append(
                        register.EBankingNotification)
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"].append({
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    })

        account_info = {}
        for auth_method in e_bank_info:
            if auth_method.EBankingInfo:
                payment_fee = {
                    "flag": auth_method.EBankingInfo.method_payment_fee_flag,
                    "account": auth_method.EBankingInfo.account_payment_fee
                }

                account_info["register_flag"] = auth_method.EBankingInfo.ib_mb_flag
                account_info["account_name"] = auth_method.EBankingInfo.account_name
                account_info["payment_fee"] = payment_fee
                account_info["get_initial_password_method"] = GetInitialPasswordMethod(
                    auth_method.EBankingInfo.method_active_password_id)
                break
        data = {
            "change_of_balance_payment_account": {
                "register_flag": True if checking_registration_info else False,
                "customer_contact_types": [
                    {
                        "id": contact_type.CustomerContactType.id,
                        "name": contact_type.CustomerContactType.name,
                        "group": contact_type.CustomerContactType.group,
                        "description": contact_type.CustomerContactType.description,
                        "checked_flag": True if contact_type.EBankingRegisterBalanceOption else False
                    } for contact_type in contact_types if
                    contact_type.EBankingRegisterBalanceOption.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING
                ],
                "register_balance_casas": [
                    {
                        "account_id": registration_info['account_id'],
                        "checking_account_name": registration_info['name'],
                        "primary_phone_number": registration_info.get('mobile_number'),
                        "full_name_vn": registration_info['full_name'],
                        "notification_casa_relationships": notification_casa_relationships,
                        "e_banking_notifications": e_banking_notifications

                    } for registration_info in checking_registration_info.values()
                ]
            },
            "e_banking_information": {
                "account_information": {
                    **account_info,
                    "method_authentication": [
                        {
                            **dropdown(method.MethodAuthentication),
                            "checked_flag": True if method.EBankingInfo else False
                        } for method in e_bank_info
                    ],
                },
            }
        }

        return self.response(data=data)

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
