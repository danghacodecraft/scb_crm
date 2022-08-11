from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.top_up.repository import (
    repos_get_casa_top_up_info, repos_save_casa_top_up_info
)
from app.api.v1.endpoints.casa.top_up.schema import (
    CasaTopUpRequest, CasaTopUpSCBByIdentityRequest,
    CasaTopUpSCBToAccountRequest, CasaTopUpThirdParty247ToAccountRequest,
    CasaTopUpThirdParty247ToCardRequest, CasaTopUpThirdPartyByIdentityRequest,
    CasaTopUpThirdPartyToAccountRequest
)
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.category.controller import (
    CtrSelectCategory
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.api.v1.others.statement.controller import CtrStatement
from app.api.v1.others.statement.repository import repos_get_denominations
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.address import AddressProvince
from app.third_parties.oracle.models.master_data.bank import Bank
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.approval import CASA_TOP_UP_STAGE_BEGIN
from app.utils.constant.business_type import BUSINESS_TYPE_CASA_TOP_UP
from app.utils.constant.casa import (
    RECEIVING_METHOD__METHOD_TYPES, RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT, RECEIVING_METHODS
)
from app.utils.constant.cif import (
    ADDRESS_TYPE_CODE_UNDEFINDED, DROPDOWN_NONE_DICT,
    IDENTITY_TYPE_CODE_NON_RESIDENT,
    PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.constant.gw import (
    GW_DATETIME_FORMAT, GW_REQUEST_DIRECT_INDIRECT
)
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_GDV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_GDV
)
from app.utils.error_messages import (
    ERROR_BANK_NOT_IN_CITAD, ERROR_BANK_NOT_IN_NAPAS, ERROR_BOOKING_INCORRECT,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_CIF_NUMBER_NOT_EXIST,
    ERROR_DENOMINATIONS_NOT_EXIST, ERROR_FIELD_REQUIRED,
    ERROR_INTERBANK_ACCOUNT_NUMBER_NOT_EXIST,
    ERROR_INTERBANK_CARD_NUMBER_NOT_EXIST, ERROR_MAPPING_MODEL,
    ERROR_RECEIVING_METHOD_NOT_EXIST, USER_CODE_NOT_EXIST
)
from app.utils.functions import (
    dropdown, generate_uuid, now, orjson_dumps, orjson_loads, string_to_date
)
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, make_short_name, split_name
)


class CtrCasaTopUp(BaseController):
    async def ctr_get_casa_top_up_info(self, booking_id: str):
        booking = await CtrBooking().ctr_get_booking(booking_id=booking_id, business_type_code=BUSINESS_TYPE_CASA_TOP_UP)
        if booking.business_type.id != BUSINESS_TYPE_CASA_TOP_UP:
            return self.response_exception(
                msg=ERROR_BOOKING_INCORRECT, loc=f"business_type: {booking.business_type.id}"
            )

        get_casa_top_up_info = self.call_repos(await repos_get_casa_top_up_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))
        form_data = orjson_loads(get_casa_top_up_info.form_data)
        return self.response(data=form_data)

    async def ctr_save_casa_top_up_scb_to_account(
            self,
            receiving_method: str,
            current_user: AuthResponse,
            data: CasaTopUpSCBToAccountRequest
    ):
        if not isinstance(data, CasaTopUpSCBToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpSCBToAccountRequest, request: {type(data)}'
            )

        receiver_account_number = data.receiver_account_number

        # Kiểm tra số tài khoản có tồn tại hay không
        casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=receiver_account_number
        )
        if not casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"account_number: {receiver_account_number}"
            )

        gw_casa_account_info = await CtrGWCasaAccount(
            current_user=current_user).ctr_gw_get_casa_account_info(
            account_number=receiver_account_number,
            return_raw_data_flag=True
        )
        gw_casa_account_info_customer_info = gw_casa_account_info['customer_info']
        account_info = gw_casa_account_info_customer_info['account_info']

        receiver = dict(
            account_number=data.receiver_account_number,
            fullname_vn=gw_casa_account_info_customer_info['full_name'],
            currency=account_info['account_currency']
        )

        return dict(
            receiver=receiver,
        )

    async def ctr_save_casa_top_up_scb_by_identity(
            self,
            receiving_method: str,
            data: CasaTopUpSCBByIdentityRequest
    ):
        if not isinstance(data, CasaTopUpSCBByIdentityRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpSCBByIdentityRequest, request: {type(data)}'
            )

        # validate province
        receiver_province_id = data.receiver_province.id
        province = await self.get_model_object_by_id(
            model_id=receiver_province_id,
            model=AddressProvince,
            loc=f'receiver_province -> id: {receiver_province_id}'
        )

        # validate branch
        branch = await self.get_model_object_by_id(model_id=data.receiver_branch.id, model=Branch, loc='branch -> id')

        # validate issued_date
        issued_date = await self.validate_issued_date(issued_date=data.receiver_issued_date, loc='receiver_issued_date')

        # validate receiver_place_of_issue
        place_of_issue = await self.get_model_object_by_id(
            model_id=data.receiver_place_of_issue.id, model=PlaceOfIssue, loc='receiver_place_of_issue -> id'
        )

        # validate sender_place_of_issue
        if data.sender_place_of_issue:
            await self.get_model_object_by_id(
                model_id=data.sender_place_of_issue.id, model=PlaceOfIssue, loc='sender_place_of_issue -> id'
            )

        data.receiving_method = receiving_method

        receiver = dict(
            province=dropdown(province),
            branch=dropdown(branch),
            issued_date=issued_date,
            place_of_issue=dropdown(place_of_issue)
        )

        return dict(
            receiver=receiver
        )

    async def ctr_save_casa_top_up_third_party_to_account(
            self,
            receiving_method: str,
            data: CasaTopUpThirdPartyToAccountRequest
    ):
        if not isinstance(data, CasaTopUpThirdPartyToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdPartyToAccountRequest, request: {type(data)}'
            )
        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(
            model_id=data.receiver_bank.id,
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

        data.receiving_method = receiving_method

        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(
            model_id=receiver_bank_id, model=Bank, loc=f"receiver_bank_id: {receiver_bank_id}"
        )
        receiver_province_id = data.receiver_province.id
        receiver_province = await self.get_model_object_by_id(
            model_id=receiver_province_id, model=AddressProvince, loc=f"receiver_province_id: {receiver_province_id}"
        )

        receiver = dict(
            bank=dropdown(receiver_bank),
            province=dropdown(receiver_province),
            account_number=data.receiver_account_number,
            fullname_vn=data.receiver_full_name_vn,
            address_full=data.receiver_address_full
        )

        return dict(
            receiver=receiver,
        )

    async def ctr_save_casa_top_up_third_party_by_identity(
            self,
            receiving_method: str,
            data: CasaTopUpThirdPartyByIdentityRequest
    ):
        if not isinstance(data, CasaTopUpThirdPartyByIdentityRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdPartyByIdentityRequest, request: {type(data)}'
            )
        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(
            model_id=data.receiver_bank.id,
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

        # validate receiver_place_of_issue
        await self.get_model_object_by_id(
            model_id=data.receiver_place_of_issue.id, model=PlaceOfIssue, loc='receiver_place_of_issue -> id'
        )

        data.receiving_method = receiving_method

        return data

    async def ctr_save_casa_top_up_third_party_247_to_account(
            self,
            receiving_method: str,
            data: CasaTopUpThirdParty247ToAccountRequest
    ):
        if not isinstance(data, CasaTopUpThirdParty247ToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdPartyByIdentityRequest, request: {type(data)}'
            )
        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(
            model_id=data.receiver_bank.id,
            model=Bank,
            loc=f'receiver_bank -> id: {receiver_bank_id}'
        )
        if not receiver_bank.napas_flag:
            return self.response_exception(
                loc=f'receiver_bank -> id: {receiver_bank_id}',
                msg=ERROR_BANK_NOT_IN_NAPAS
            )

        # validate account_number
        account_number = data.receiver_account_number
        is_existed = await CtrGWCasaAccount(self.current_user).ctr_check_exist_account_number_from_other_bank(
            account_number=account_number
        )
        if not is_existed:
            self.response_exception(msg=ERROR_INTERBANK_ACCOUNT_NUMBER_NOT_EXIST, loc=f'account_number: {account_number}')

        data.receiving_method = receiving_method
        return data

    async def ctr_save_casa_top_up_third_party_247_to_card(
            self,
            receiving_method: str,
            data: CasaTopUpThirdParty247ToCardRequest
    ):
        if not isinstance(data, CasaTopUpThirdParty247ToCardRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdParty247ToCardRequest, request: {type(data)}'
            )

        # validate bank
        receiver_bank_id = data.receiver_bank.id
        receiver_bank = await self.get_model_object_by_id(
            model_id=data.receiver_bank.id,
            model=Bank,
            loc=f'receiver_bank -> id: {receiver_bank_id}'
        )
        if not receiver_bank.napas_flag:
            return self.response_exception(
                loc=f'receiver_bank -> id: {receiver_bank_id}',
                msg=ERROR_BANK_NOT_IN_NAPAS
            )
        # validate card number
        card_number = data.receiver_card_number
        is_existed = await CtrGWCasaAccount(self.current_user).ctr_check_exist_card_number_from_other_bank(
            card_number=card_number
        )
        if not is_existed:
            self.response_exception(msg=ERROR_INTERBANK_CARD_NUMBER_NOT_EXIST,
                                    loc=f'card_number: {card_number}')

        data.receiving_method = receiving_method
        return data

    async def ctr_save_casa_top_up_info(
            self,
            booking_id: str,
            request: CasaTopUpRequest
    ):
        data = request.data
        receiving_method = request.receiving_method
        sender_cif_number = data.sender_cif_number
        statement = data.statement
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
            stage_code=CASA_TOP_UP_STAGE_BEGIN
        ))

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_CASA_TOP_UP,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        denominations__amounts = {}
        statement_info = self.call_repos(await repos_get_denominations(currency_id="VND", session=self.oracle_session))

        for item in statement_info:
            denominations__amounts.update({
                str(int(item.denominations)): 0
            })
        denominations_errors = []
        for index, row in enumerate(statement):
            denominations = row.denominations
            if denominations not in denominations__amounts:
                denominations_errors.append(dict(
                    index=index,
                    value=denominations
                ))

            denominations__amounts[denominations] = row.amount

        if denominations_errors:
            return self.response_exception(
                msg=ERROR_DENOMINATIONS_NOT_EXIST,
                loc=str(denominations_errors)
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

        # TH1: có nhập cif -> Kiểm tra số CIF có tồn tại trong CRM không
        if sender_cif_number:
            # self.call_repos(await repos_get_customer_by_cif_number(
            #     cif_number=cif_number,
            #     session=self.oracle_session
            # ))
            customer_detail = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_detail(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            if not customer_detail['full_name']:
                return self.response_exception(
                    msg=ERROR_CIF_NUMBER_NOT_EXIST,
                    loc=f"sender_cif_number {sender_cif_number}"
                )

            data.sender_full_name_vn = customer_detail['full_name']
            customer_identity_detail = customer_detail['id_info']
            data.sender_identity_number = customer_identity_detail['id_num']
            data.sender_issued_date = string_to_date(customer_identity_detail['id_issued_date'], _format=GW_DATETIME_FORMAT)
            data.sender_address_full = customer_detail['t_address_info']['contact_address_full']
            data.sender_mobile_number = customer_detail['mobile_phone']
        # TH2: Không nhập CIF
        else:
            sender_full_name_vn = data.sender_full_name_vn
            sender_identity_number = data.sender_identity_number
            sender_issued_date = data.sender_issued_date
            sender_address_full = data.sender_address_full
            sender_mobile_number = data.sender_mobile_number

            sender_place_of_issue_id = data.sender_place_of_issue.id
            await self.get_model_object_by_id(
                model_id=sender_place_of_issue_id,
                model=PlaceOfIssue,
                loc=f'sender_place_of_issue_id: {sender_place_of_issue_id}'
            )

            errors = []
            if not sender_full_name_vn:
                errors.append(f'sender_full_name_vn: {sender_full_name_vn}')
            if not sender_identity_number:
                errors.append(f'sender_identity_number: {sender_identity_number}')
            if not sender_issued_date:
                errors.append(f'sender_issued_date: {sender_issued_date}')
            if not sender_address_full:
                errors.append(f'sender_address_full: {sender_address_full}')
            if not sender_mobile_number:
                errors.append(f'sender_mobile_number: {sender_mobile_number}')

            if errors:
                return self.response_exception(msg=ERROR_FIELD_REQUIRED, loc=', '.join(errors))

        if receiving_method not in RECEIVING_METHODS:
            return self.response_exception(
                msg=ERROR_RECEIVING_METHOD_NOT_EXIST,
                loc=f'receiving_method: {receiving_method}'
            )
        ################################################################################################################

        casa_top_up_info = None
        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            casa_top_up_info = await self.ctr_save_casa_top_up_scb_to_account(
                current_user=current_user,
                receiving_method=receiving_method,
                data=data
            )

        # saving_customer = {}
        # saving_customer_identity = {}
        # saving_customer_address = {}
        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
            casa_top_up_info = await self.ctr_save_casa_top_up_scb_by_identity(
                receiving_method=receiving_method,
                data=data
            )
            # (
            #     saving_customer, saving_customer_identity, saving_customer_address
            # ) = await CtrCustomer(current_user).ctr_create_non_resident_customer(request=request)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_to_account(
                receiving_method=receiving_method,
                data=data
            )

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_by_identity(
                receiving_method=receiving_method,
                data=data
            )
            # (
            #     saving_customer, saving_customer_identity, saving_customer_address
            # ) = await CtrCustomer(current_user).ctr_create_non_resident_customer(request=request)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_247_to_account(
                receiving_method=receiving_method,
                data=data
            )

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_247_to_card(
                receiving_method=receiving_method,
                data=data
            )

        if not casa_top_up_info:
            return self.response_exception(msg="No Casa Top Up")

        ################################################################################################################
        # Thông tin giao dịch
        ################################################################################################################
        transfer_response = dict(
            amount=data.amount,
            content=data.content,
            entry_number=data.p_instrument_number
        )

        transfer_type_response = dict(
            receiving_method_type=RECEIVING_METHOD__METHOD_TYPES[receiving_method],
            receiving_method=receiving_method
        )

        fee_info_request = data.fee_info
        fee_info_response = dict(
            is_fee=False,
            payer=None,
            fee_amount=None,
            vat_tax=None,
            total=None,
            actual_total=None,
            note=None
        )
        if fee_info_request:
            amount = fee_info_request.amount
            vat = amount / 10
            total = amount + vat
            actual_total = amount + total

            fee_info_response.update(
                is_fee=True,
                payer=fee_info_request.payer,
                amount=amount,
                vat=vat,
                total=total,
                actual_total=actual_total,
                note=fee_info_request.note
            )

        statement_response = await CtrStatement().ctr_get_statement_info(statement_requests=data.statement)

        ################################################################################################################
        # Thông tin khách hàng giao dịch
        ################################################################################################################
        sender_cif_number = data.sender_cif_number
        if sender_cif_number:
            gw_customer_info = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_detail(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            gw_customer_info_identity_info = gw_customer_info['id_info']
            sender_response = dict(
                cif_number=sender_cif_number,
                fullname_vn=gw_customer_info['full_name'],
                address_full=gw_customer_info['t_address_info']['contact_address_full'],
                identity_info=dict(
                    number=gw_customer_info_identity_info['id_num'],
                    issued_date=data.sender_issued_date,
                    place_of_issue=await self.dropdown_mapping_crm_model_or_dropdown_name(
                        model=PlaceOfIssue,
                        code=gw_customer_info_identity_info['id_issued_location'],
                        name=gw_customer_info_identity_info['id_issued_location']
                    )
                ),
                mobile_phone=gw_customer_info['mobile_phone'],
                telephone=gw_customer_info['telephone'],
                otherphone=gw_customer_info['otherphone']
            )
        else:
            identity_place_of_issue = DROPDOWN_NONE_DICT
            if data.sender_place_of_issue:
                identity_place_of_issue = await self.get_model_object_by_id(
                    model_id=data.sender_place_of_issue.id,
                    model=PlaceOfIssue,
                    loc='sender_place_of_issue -> id'
                )
            sender_response = dict(
                cif_number=sender_cif_number,
                fullname_vn=data.sender_full_name_vn,
                address_full=data.sender_address_full,
                identity_info=dict(
                    number=data.sender_identity_number,
                    issued_date=data.sender_issued_date,
                    place_of_issue=dropdown(identity_place_of_issue)
                ),
                mobile_phone=data.sender_mobile_number,
                telephone=None,
                otherphone=None
            )

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

        casa_top_up_info.update(
            transfer=transfer_response,
            fee_info=fee_info_response,
            transfer_type=transfer_type_response,
            statement=statement_response,
            sender=sender_response,
            direct_staff=direct_staff,
            indirect_staff=indirect_staff
        )

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT,
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
            business_type_id=BUSINESS_TYPE_CASA_TOP_UP,
            booking_id=booking_id,
            request_json=orjson_dumps(casa_top_up_info),
            history_datas=orjson_dumps(history_datas),
        )

        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        self.call_repos(await repos_save_casa_top_up_info(
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
            # saving_customer=saving_customer,
            # saving_customer_identity=saving_customer_identity,
            # saving_customer_address=saving_customer_address,
            session=self.oracle_session
        ))

        return self.response(data=dict(
            booking_id=booking_id
        ))


class CtrCustomer(BaseController):
    async def ctr_create_non_resident_customer(
            self,
            request: Union[CasaTopUpSCBByIdentityRequest, CasaTopUpThirdPartyByIdentityRequest],
    ):
        current_user_info = self.current_user.user_info
        full_name_vn = request.sender_full_name_vn
        sender_place_of_issue_id = request.sender_place_of_issue.id
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
            mobile_number=request.sender_mobile_number,
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
            identity_num=request.sender_identity_number,
            issued_date=request.sender_issued_date,
            place_of_issue_id=sender_place_of_issue_id,
            maker_id=current_user_info.code,
            maker_at=now()
        )
        saving_customer_address = dict(
            id=generate_uuid(),
            customer_id=customer_id,
            address=request.sender_address_full,
            address_type_id=ADDRESS_TYPE_CODE_UNDEFINDED
        )
        return saving_customer, saving_customer_identity, saving_customer_address
