import json
from datetime import date
from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.transfer.repository import (
    repos_get_acc_types, repos_get_casa_transfer_info,
    repos_save_casa_transfer_info
)
from app.api.v1.endpoints.casa.transfer.schema import (
    CasaTransferRequest, CasaTransferSCBByIdentityRequest,
    CasaTransferSCBToAccountRequest, CasaTransferThirdParty247ToAccountRequest,
    CasaTransferThirdParty247ToCardRequest,
    CasaTransferThirdPartyByIdentityRequest,
    CasaTransferThirdPartyToAccountRequest
)
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.category.controller import (
    CtrSelectCategory
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.fee.controller import CtrAccountFee
from app.api.v1.others.permission.controller import PermissionController
from app.api.v1.others.sender.controller import CtrPaymentSender
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.address import AddressProvince
from app.third_parties.oracle.models.master_data.bank import Bank, BankBranch
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.approval import CASA_TRANSFER_STAGE_BEGIN
from app.utils.constant.business_type import BUSINESS_TYPE_CASA_TRANSFER
from app.utils.constant.casa import (
    RECEIVING_METHOD__METHOD_TYPES, RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT, RECEIVING_METHODS
)
from app.utils.constant.cif import (
    ADDRESS_TYPE_CODE_UNDEFINDED, IDENTITY_TYPE_CODE_NON_RESIDENT,
    PROFILE_HISTORY_DESCRIPTIONS_TRANSFER_CASA_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.constant.gw import GW_REQUEST_DIRECT_INDIRECT
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_GDV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_GDV
)
from app.utils.error_messages import (
    ERROR_BANK_NOT_IN_CITAD, ERROR_BANK_NOT_IN_NAPAS,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_MAPPING_MODEL,
    ERROR_RECEIVING_METHOD_NOT_EXIST, USER_CODE_NOT_EXIST
)
from app.utils.functions import (
    date_to_string, dropdown, generate_uuid, now, orjson_dumps, orjson_loads
)
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, make_short_name, split_name
)


class CtrCasaTransfer(BaseController):
    async def ctr_get_casa_transfer_info(self, booking_id: str):
        get_casa_transfer_info, _ = self.call_repos(await repos_get_casa_transfer_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))

        form_data = orjson_loads(get_casa_transfer_info.form_data)

        return self.response(form_data)

    async def ctr_save_casa_transfer_scb_to_account(
            self,
            current_user: AuthResponse,
            data: CasaTransferSCBToAccountRequest
    ):
        if not isinstance(data, CasaTransferSCBToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTransferSCBToAccountRequest, request: {type(data)}'
            )

        receiver_account_number = data.receiver_account_number
        sender_account_number = data.sender_account_number

        # Kiểm tra số tài khoản chuyển khoản tồn tại hay không
        sender_casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=sender_account_number
        )
        if not sender_casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"sender_account_number: {sender_account_number}"
            )

        # Kiểm tra số tài khoản thụ hưởng có tồn tại hay không
        receiver_casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=receiver_account_number
        )
        if not receiver_casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"receiver_account_number: {receiver_account_number}"
            )

        receiver_account_number = data.receiver_account_number

        gw_casa_account_info = await CtrGWCasaAccount(
            current_user=current_user).ctr_gw_get_casa_account_info(
            account_number=receiver_account_number,
            return_raw_data_flag=True
        )

        gw_casa_account_info_customer_info = gw_casa_account_info['customer_info']
        account_info = gw_casa_account_info_customer_info['account_info']

        receiver_response = dict(
            account_number=receiver_account_number,
            fullname_vn=gw_casa_account_info_customer_info['full_name'],
            currency=account_info['account_currency'],
            branch_info=dict(
                id=account_info['branch_info']['branch_code'],
                code=account_info['branch_info']['branch_code'],
                name=account_info['branch_info']['branch_name']
            )
        )

        return receiver_response

    async def ctr_save_casa_transfer_scb_by_identity(
            self,
            current_user: AuthResponse,
            data: CasaTransferSCBByIdentityRequest
    ):
        if not isinstance(data, CasaTransferSCBByIdentityRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTransferSCBByIdentityRequest, request: {type(data)}'
            )

        sender_account_number = data.sender_account_number

        # Kiểm tra số tài khoản chuyển khoản tồn tại hay không
        sender_casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=sender_account_number
        )
        if not sender_casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"sender_account_number: {sender_account_number}"
            )

        # validate branch
        await self.get_model_object_by_id(model_id=data.receiver_branch.id, model=Branch, loc='branch -> id')

        # validate issued_date
        await self.validate_issued_date(issued_date=data.receiver_issued_date, loc='issued_date')

        # validate place_of_issue
        await self.get_model_object_by_id(
            model_id=data.receiver_place_of_issue.id, model=PlaceOfIssue, loc='place_of_issue -> id'
        )

        receiver_place_of_issue = await self.get_model_object_by_id(
            model_id=data.receiver_place_of_issue.id, model=PlaceOfIssue,
            loc='receiver_place_of_issue_id')

        receiver_branch_info = await self.get_model_object_by_id(
            model_id=data.receiver_branch.id, model=Branch, loc='receiver_branch_id'
        )

        receiver_response = dict(
            province=dropdown(receiver_branch_info.address_province),
            branch_info=dropdown(receiver_branch_info),
            fullname_vn=data.receiver_full_name_vn,
            identity_number=data.receiver_identity_number,
            issued_date=date_to_string(data.receiver_issued_date),
            place_of_issue=dropdown(receiver_place_of_issue),
            mobile_phone=data.receiver_mobile_number if data.receiver_mobile_number in data else None,
            address_full=data.receiver_address_full
        )

        return receiver_response

    async def ctr_save_casa_transfer_third_party_to_account(
            self,
            current_user: AuthResponse,
            data: CasaTransferThirdPartyToAccountRequest
    ):
        if not isinstance(data, CasaTransferThirdPartyToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTransferThirdPartyToAccountRequest, request: {type(data)}'
            )
        sender_account_number = data.sender_account_number

        # Kiểm tra số tài khoản chuyển khoản tồn tại hay không
        sender_casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=sender_account_number
        )
        if not sender_casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"sender_account_number: {sender_account_number}"
            )

        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(
            model_id=receiver_bank_id,
            model=Bank,
            loc=f'receiver_bank -> id: {receiver_bank_id}'
        )
        if not receiver_bank.citad_flag:
            return self.response_exception(
                loc=f'receiver_bank -> id: {receiver_bank_id}',
                msg=ERROR_BANK_NOT_IN_CITAD
            )

        # validate province
        receiver_province_id = data.receiver_province.id
        await self.get_model_object_by_id(
            model_id=receiver_province_id,
            model=AddressProvince,
            loc=f'receiver_province -> id: {receiver_province_id}'
        )
        receiver_account_number = data.receiver_account_number
        bank_id = data.receiver_bank.id
        bank_info = await self.get_model_object_by_id(model_id=bank_id, model=Bank, loc='receiver_bank_id')
        province_id = data.receiver_province.id
        province_info = await self.get_model_object_by_id(model_id=province_id, model=AddressProvince,
                                                          loc='receiver_province_id')
        receiver_response = dict(
            bank=dropdown(bank_info),
            province=dropdown(province_info),
            account_number=receiver_account_number,
            fullname_vn=data.receiver_full_name_vn,
            address_full=data.receiver_address_full,
        )

        return receiver_response

    async def ctr_save_casa_transfer_third_party_by_identity(
            self,
            current_user: AuthResponse,
            data: CasaTransferThirdPartyByIdentityRequest
    ):
        if not isinstance(data, CasaTransferThirdPartyByIdentityRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTransferThirdPartyByIdentityRequest, request: {type(data)}'
            )
        sender_account_number = data.sender_account_number

        # Kiểm tra số tài khoản chuyển khoản tồn tại hay không
        sender_casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=sender_account_number
        )
        if not sender_casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"sender_account_number: {sender_account_number}"
            )

        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(
            model_id=receiver_bank_id,
            model=Bank,
            loc=f'receiver_bank -> id: {receiver_bank_id}'
        )
        if not receiver_bank.citad_flag:
            return self.response_exception(
                loc=f'receiver_bank -> id: {receiver_bank_id}',
                msg=ERROR_BANK_NOT_IN_CITAD
            )

        # validate bank branch
        receiver_branch_id = data.receiver_branch.id
        await self.get_model_object_by_id(
            model_id=receiver_branch_id,
            model=BankBranch,
            loc=f'receiver_branch -> id: {receiver_branch_id}'
        )

        # validate province
        receiver_province_id = data.receiver_province.id
        await self.get_model_object_by_id(
            model_id=receiver_province_id,
            model=AddressProvince,
            loc=f'receiver_province -> id: {receiver_province_id}'
        )

        # validate receiver_place_of_issue
        await self.get_model_object_by_id(
            model_id=data.receiver_place_of_issue.id, model=PlaceOfIssue, loc='receiver_place_of_issue -> id'
        )

        receiver_place_of_issue = await self.get_model_object_by_id(
            model_id=data.receiver_place_of_issue.id, model=PlaceOfIssue,
            loc='receiver_place_of_issue_id')

        bank_id = data.receiver_bank.id
        branch_id = data.receiver_branch.id
        province_id = data.receiver_province.id

        province_info = await self.get_model_object_by_id(
            model_id=province_id, model=AddressProvince, loc='receiver_province'
        )
        bank_info = await self.get_model_object_by_id(
            model_id=bank_id, model=Bank, loc='receiver_bank'
        )
        branch_info = await self.get_model_object_by_id(
            model_id=branch_id, model=BankBranch, loc='receiver_branch'
        )

        receiver_response = dict(
            bank=dropdown(bank_info),
            province=dropdown(province_info),
            branch_info=dropdown(branch_info),
            fullname_vn=data.receiver_full_name_vn,
            identity_number=data.receiver_identity_number,
            issued_date=date_to_string(data.receiver_issued_date),
            place_of_issue=dropdown(receiver_place_of_issue),
            mobile_phone=data.receiver_mobile_number if data.receiver_mobile_number else None,
            address_full=data.receiver_address_full
        )

        return receiver_response

    async def ctr_save_casa_transfer_third_party_247_to_account(
            self,
            current_user: AuthResponse,
            data: CasaTransferThirdParty247ToAccountRequest
    ):
        if not isinstance(data, CasaTransferThirdParty247ToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTransferThirdParty247ToAccountRequest, request: {type(data)}'
            )
        sender_account_number = data.sender_account_number
        receiver_account_number = data.receiver_account_number

        ben_name = await CtrGWCasaAccount(current_user).ctr_gw_get_retrieve_ben_name_by_account_number(
            account_number=receiver_account_number)
        receiver_full_name = ben_name['data']['full_name']

        if not receiver_full_name:
            return self.response_exception(
                msg="receiver_account_number not exist",
                loc=f"receiver_account_number: {receiver_account_number}"
            )

        data.receiver_full_name = receiver_full_name

        # Kiểm tra số tài khoản chuyển khoản tồn tại hay không
        sender_casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=sender_account_number
        )

        if not sender_casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"sender_account_number: {sender_account_number}"
            )

        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(model_id=receiver_bank_id, model=Bank, loc='bank -> id')
        if not receiver_bank.napas_flag:
            return self.response_exception(
                loc=f'receiver_bank -> id: {receiver_bank_id}',
                msg=ERROR_BANK_NOT_IN_NAPAS
            )

        receiver_account_number = data.receiver_account_number
        bank_id = data.receiver_bank.id
        bank_info = await self.get_model_object_by_id(
            model_id=bank_id, model=Bank, loc='receiver_bank'
        )
        receiver_response = dict(
            bank=dropdown(bank_info),
            account_number=receiver_account_number,
            fullname_vn=data.receiver_full_name,
            address_full=data.receiver_address_full
        )

        return receiver_response

    async def ctr_save_casa_transfer_third_party_247_to_card(
            self,
            current_user: AuthResponse,
            data: CasaTransferThirdParty247ToCardRequest
    ):
        if not isinstance(data, CasaTransferThirdParty247ToCardRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTransferThirdParty247ToCardRequest, request: {type(data)}'
            )
        receiver_card_number = data.receiver_card_number

        ben_name = await CtrGWCasaAccount(current_user).ctr_gw_get_retrieve_ben_name_by_card_number(
            card_number=receiver_card_number)
        receiver_full_name = ben_name['data']['full_name']

        if not receiver_full_name:
            return self.response_exception(
                msg="receiver_card_number not exist",
                loc=f"receiver_card_number: {receiver_card_number}"
            )

        data.receiver_full_name = receiver_full_name

        sender_account_number = data.sender_account_number

        # Kiểm tra số tài khoản chuyển khoản tồn tại hay không
        sender_casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=sender_account_number
        )
        if not sender_casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"sender_account_number: {sender_account_number}"
            )

        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(model_id=receiver_bank_id, model=Bank, loc='bank -> id')
        if not receiver_bank.napas_flag:
            return self.response_exception(
                loc=f'receiver_bank -> id: {receiver_bank_id}',
                msg=ERROR_BANK_NOT_IN_NAPAS
            )

        receiver_card_number = data.receiver_card_number
        bank_id = data.receiver_bank.id
        bank_info = await self.get_model_object_by_id(
            model_id=bank_id, model=Bank, loc='receiver_bank'
        )
        receiver_response = dict(
            bank=dropdown(bank_info),
            card_number=receiver_card_number,
            fullname_vn=data.receiver_full_name,
            address_full=data.receiver_address_full
        )

        return receiver_response

    async def ctr_save_casa_transfer_info(
            self,
            booking_id: str,
            request: CasaTransferRequest
    ):
        data = request.data
        receiving_method = request.receiving_method
        direct_staff_code = data.direct_staff_code
        indirect_staff_code = data.indirect_staff_code
        current_user = self.current_user
        current_user_info = current_user.user_info
        ################################################################################################################
        # VALIDATE
        ################################################################################################################
        # check quyền user
        self.call_repos(await PermissionController().ctr_approval_check_permission(
            auth_response=current_user,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_GDV,
            permission_code=IDM_PERMISSION_CODE_GDV,
            stage_code=CASA_TRANSFER_STAGE_BEGIN
        ))

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_CASA_TRANSFER,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        if direct_staff_code:
            gw_direct_staffs = await CtrSelectCategory(current_user).ctr_select_category(
                transaction_name=GW_REQUEST_DIRECT_INDIRECT,
                transaction_value=[
                    {
                        "param1": "D",
                        "param2": current_user_info.hrm_branch_code
                    }
                ]
            )
            is_direct_staff = False
            for gw_direct_staff in gw_direct_staffs['data']:
                if direct_staff_code == gw_direct_staff['employee_code']:
                    is_direct_staff = True
                    break
            if not is_direct_staff:
                return self.response_exception(msg=USER_CODE_NOT_EXIST, loc=f'direct_staff_code: {direct_staff_code}')

        if indirect_staff_code:
            gw_indirect_staffs = await CtrSelectCategory(current_user).ctr_select_category(
                transaction_name=GW_REQUEST_DIRECT_INDIRECT,
                transaction_value=[
                    {
                        "param1": "I",
                        "param2": current_user_info.hrm_branch_code
                    }
                ]
            )
            is_indirect_staff = False
            for gw_indirect_staff in gw_indirect_staffs['data']:
                if indirect_staff_code == gw_indirect_staff['employee_code']:
                    is_indirect_staff = True
                    break
            if not is_indirect_staff:
                return self.response_exception(
                    msg=USER_CODE_NOT_EXIST, loc=f'indirect_staff_code: {indirect_staff_code}'
                )

        if receiving_method not in RECEIVING_METHODS:
            return self.response_exception(
                msg=ERROR_RECEIVING_METHOD_NOT_EXIST,
                loc=f'receiving_method: {receiving_method}'
            )
        ################################################################################################################

        casa_transfer_info = None

        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            casa_transfer_info = await self.ctr_save_casa_transfer_scb_to_account(
                current_user=current_user, data=data
            )

        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
            casa_transfer_info = await self.ctr_save_casa_transfer_scb_by_identity(
                current_user=current_user, data=data)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            casa_transfer_info = await self.ctr_save_casa_transfer_third_party_to_account(
                current_user=current_user, data=data)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            casa_transfer_info = await self.ctr_save_casa_transfer_third_party_by_identity(
                current_user=current_user, data=data)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
            casa_transfer_info = await self.ctr_save_casa_transfer_third_party_247_to_account(
                current_user=current_user, data=data)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            casa_transfer_info = await self.ctr_save_casa_transfer_third_party_247_to_card(
                current_user=current_user, data=data)

        if not casa_transfer_info:
            return self.response_exception(msg="No Casa Transfer")

        # Thông tin giao dịch
        transfer_response = dict(
            amount=data.amount,
            content=data.content,
            entry_number=data.p_instrument_number
        )

        # Thông tin loại giao dịch
        transfer_type_response = dict(
            receiving_method_type=RECEIVING_METHOD__METHOD_TYPES[receiving_method],
            receiving_method=receiving_method
        )

        # Thông tin phí
        fee_info_response = await CtrAccountFee().calculate_fee(
            one_fee_info_request=data.fee_info, fee_note=data.fee_note
        )

        # Thông tin khách hàng giao dịch
        sender_response = await CtrPaymentSender(self.current_user).get_payment_sender(
            sender_cif_number=data.sender_cif_number,
            sender_full_name_vn=data.sender_full_name_vn,
            sender_address_full=data.sender_address_full,
            sender_identity_number=data.sender_identity_number,
            sender_issued_date=data.sender_issued_date,
            sender_mobile_number=data.sender_mobile_number,
            sender_place_of_issue=data.sender_place_of_issue
        )

        if isinstance(sender_response['identity_info']['issued_date'], date):
            sender_response['identity_info']['issued_date'] = date_to_string(sender_response['identity_info']['issued_date'])

        sender_response['account_number'] = data.sender_account_number

        controller_gw_employee = CtrGWEmployee(current_user)
        gw_direct_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=data.direct_staff_code,
            return_raw_data_flag=True
        )
        direct_staff = dict(
            code=gw_direct_staff['staff_code'],
            name=gw_direct_staff['staff_name']
        )
        gw_indirect_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=data.indirect_staff_code,
            return_raw_data_flag=True
        )
        indirect_staff = dict(
            code=gw_indirect_staff['staff_code'],
            name=gw_indirect_staff['staff_name']
        )
        ################################################################################################################

        response_data = dict(
            transfer_type=transfer_type_response,
            receiver=casa_transfer_info,
            transfer=transfer_response,
            fee_info=fee_info_response,
            fee_note=data.fee_note,
            sender=sender_response,
            direct_staff=direct_staff,
            indirect_staff=indirect_staff,
        )

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_TRANSFER_CASA_ACCOUNT,
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

        # Tạo data TransactionDaily và các TransactionStage khác cho bước mở CASA
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_CASA_TRANSFER,
            booking_id=booking_id,
            request_json=json.dumps(response_data),
            history_datas=orjson_dumps(history_datas)
        )

        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        self.call_repos(await repos_save_casa_transfer_info(
            booking_id=booking_id,
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
            session=self.oracle_session
        ))

        return self.response(data=dict(
            booking_id=booking_id
        ))

    async def ctr_source_account_info(self, cif_number: str):
        current_user = self.current_user

        gw_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_by_cif_number(
            cif_number=cif_number
        )
        account_list = gw_account_info['data']
        account_info_list = account_list['account_info_list']
        full_name_vn = account_list['full_name_vn']

        total_items = account_list['total_items']

        casa_accounts = []
        numbers = []

        for account in account_info_list:
            casa_accounts.append(dict(
                number=account["number"],
                fullname_vn=full_name_vn,
                balance_available=account['balance_available'],
                currency=account['currency']
            ))
            numbers.append(account["number"])

        acc_types = self.call_repos(await repos_get_acc_types(
            numbers=numbers,
            session=self.oracle_session
        ))

        for account in casa_accounts:
            number = account["number"]
            for casa_account_number, acc_type in acc_types:
                if number == casa_account_number:
                    account.update(
                        account_type=acc_type
                    )
                    break

        source_accounts = dict(
            total_items=total_items,
            casa_accounts=casa_accounts
        )

        return self.response(source_accounts)


class CtrCustomer(BaseController):
    async def ctr_create_non_resident_customer(
            self,
            data: Union[CasaTransferSCBByIdentityRequest, CasaTransferThirdPartyByIdentityRequest]
    ):
        current_user_info = self.current_user.user_info
        full_name_vn = data.sender_full_name_vn
        sender_place_of_issue_id = data.sender_place_of_issue.id
        customer_id = generate_uuid()
        first_name, middle_name, last_name = split_name(full_name_vn)
        if not last_name:
            return self.response_exception(msg="Full name at least 2 words")

        short_name = make_short_name(first_name, middle_name, last_name)
        saving_customer = dict(
            id=customer_id,
            full_name=convert_to_unsigned_vietnamese(full_name_vn),
            full_name_vn=full_name_vn,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            short_name=short_name,
            mobile_number=data.sender_mobile_number,
            open_branch_id=current_user_info.hrm_branch_code,
            non_resident_flag=True,
            active_flag=True,
            open_cif_at=now(),
            self_selected_cif_flag=False,
            kyc_level_id='EKYC_1',
            nationality_id="VN",
            customer_classification_id='I_11',
            customer_status_id='1',
            channel_id='TAI_QUAY',
            complete_flag=False
        )
        saving_customer_identity = dict(
            id=generate_uuid(),
            identity_type_id=IDENTITY_TYPE_CODE_NON_RESIDENT,
            customer_id=customer_id,
            identity_num=data.sender_identity_number,
            issued_date=data.sender_issued_date,
            place_of_issue_id=sender_place_of_issue_id,
            maker_id=current_user_info.code,
            maker_at=now()
        )
        saving_customer_address = dict(
            id=generate_uuid(),
            customer_id=customer_id,
            address=data.sender_address_full,
            address_type_id=ADDRESS_TYPE_CODE_UNDEFINDED
        )
        return saving_customer, saving_customer_identity, saving_customer_address
