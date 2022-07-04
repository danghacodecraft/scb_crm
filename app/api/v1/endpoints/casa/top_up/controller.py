from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.top_up.repository import (
    repos_get_casa_top_up_info, repos_save_casa_top_up_info
)
from app.api.v1.endpoints.casa.top_up.schema import (
    CasaTopUpSCBByIdentityRequest, CasaTopUpSCBToAccountRequest,
    CasaTopUpThirdParty247ToAccountRequest,
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
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.approval import CASA_TOP_UP_STAGE_BEGIN
from app.utils.constant.business_type import BUSINESS_TYPE_CASA_TOP_UP
from app.utils.constant.casa import (
    DENOMINATIONS__AMOUNTS, RECEIVING_METHOD__METHOD_TYPES,
    RECEIVING_METHOD_IDENTITY_CASES, RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_SCB_TO_ACCOUNT, RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT,
    RECEIVING_METHODS, RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY, RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD, RECEIVING_METHOD_ACCOUNT_CASES
)
from app.utils.constant.cif import PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT, PROFILE_HISTORY_STATUS_INIT
from app.utils.constant.gw import GW_REQUEST_DIRECT_INDIRECT
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_GDV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_GDV
)
from app.utils.error_messages import (
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_CIF_NUMBER_NOT_EXIST,
    ERROR_DENOMINATIONS_NOT_EXIST, ERROR_MAPPING_MODEL, ERROR_NOT_NULL,
    ERROR_RECEIVING_METHOD_NOT_EXIST, USER_CODE_NOT_EXIST
)
from app.utils.functions import dropdown, orjson_loads, orjson_dumps


class CtrCasaTopUp(BaseController):
    async def ctr_get_casa_top_up_info(self, booking_id: str):
        current_user = self.current_user
        get_casa_top_up_info = self.call_repos(await repos_get_casa_top_up_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))
        form_data = orjson_loads(get_casa_top_up_info.form_data)
        receiving_method = form_data['receiving_method']

        ################################################################################################################
        # Thông tin người thụ hưởng
        ################################################################################################################
        receiver_response = {}

        if receiving_method in RECEIVING_METHOD_ACCOUNT_CASES:
            receiver_account_number = form_data['receiver_account_number']

            if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
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

                if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
                    branch_id = form_data['receiver_branch']['id']
                    receiver_response = dict(
                        # bank=form_data['bank'],
                        bank=dict(
                            code=branch_id,
                            name=branch_id
                        ),  # TODO: đợi e-bank
                        # province=dropdown(branch_info.address_province),
                        province=dict(
                            code=branch_id,
                            name=branch_id
                        ),
                        branch_info=dict(
                            code=branch_id,
                            name=branch_id
                        ),  # TODO: đợi e-bank
                        account_number=form_data['receiver_account_number'],
                        fullname_vn=form_data['receiver_full_name_vn'],
                        address_full=form_data['receiver_address_full']
                    )

                if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT:
                    receiver_response = dict(
                        # bank=form_data['bank'],
                        bank=dict(
                            code="branch_id",
                            name="branch_id"
                        ),  # TODO: đợi e-bank
                        receiver_account_number=receiver_account_number,
                        # fullname_vn=gw_casa_account_info_customer_info['full_name'],
                        address_full=form_data['address_full']
                    )
            if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD:
                receiver_response = dict(
                    bank=dict(
                        code="branch_id",
                        name="branch_id"
                    ),  # TODO: đợi e-bank
                    account_number=form_data['card_number'],  # TODO: đợi e-bank
                    # fullname_vn=gw_casa_account_info_customer_info['full_name'],
                    address_full=form_data['address_full']
                )
        else:
            place_of_issue = await self.get_model_object_by_id(
                model_id=form_data['sender_place_of_issue'], model=PlaceOfIssue, loc='place_of_issue_id'
            )

            if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
                branch_info = await self.get_model_object_by_id(
                    model_id=form_data['branch']['id'], model=Branch, loc='branch_id'
                )

                receiver_response = dict(
                    province=dropdown(branch_info.address_province),
                    branch_info=dropdown(branch_info),
                    fullname_vn=form_data['full_name_vn'],
                    identity_number=form_data['identity_number'],
                    issued_date=form_data['issued_date'],
                    place_of_issue=dropdown(place_of_issue),
                    mobile_number=form_data['mobile_number'],
                    address_full=form_data['address_full']
                )

            if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
                branch_id = form_data['branch']['id']
                receiver_response = dict(
                    # bank=form_data['bank'],
                    bank=dict(
                        code=branch_id,
                        name=branch_id
                    ),  # TODO: đợi e-bank
                    # province=dropdown(branch_info.address_province),
                    province=dict(
                        code=branch_id,
                        name=branch_id
                    ),  # TODO: đợi e-bank
                    branch_info=dict(
                        code=branch_id,
                        name=branch_id
                    ),  # TODO: đợi e-bank
                    fullname_vn=form_data['full_name_vn'],
                    identity_number=form_data['identity_number'],
                    issued_date=form_data['issued_date'],
                    place_of_issue=dropdown(place_of_issue),
                    mobile_number=form_data['mobile_number'],
                    address_full=form_data['address_full']
                )

        ################################################################################################################

        transfer_amount = form_data['amount']

        ################################################################################################################
        # Thông tin phí
        ################################################################################################################
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

        fee_info.update(dict(
            vat_tax=vat_tax,
            total=total,
            actual_total=actual_total,
            is_transfer_payer=is_transfer_payer,
            payer=payer
        ))
        ################################################################################################################

        ################################################################################################################
        # Bảng kê
        ################################################################################################################
        statement = DENOMINATIONS__AMOUNTS
        for row in form_data['statement']:
            statement.update({row['denominations']: row['amount']})

        statements = []
        total_amount = 0
        for denominations, amount in statement.items():
            into_money = int(denominations) * amount
            statements.append(dict(
                denominations=denominations,
                amount=amount,
                into_money=into_money
            ))
            total_amount += into_money
        statement_response = dict(
            statements=statements,
            total=total_amount,
            odd_difference=abs(actual_total - total_amount)
        )
        ################################################################################################################

        ################################################################################################################
        # Thông tin khách hàng giao dịch
        ################################################################################################################
        sender_cif_number = form_data['sender_cif_number']
        gw_customer_info = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_detail(
            cif_number="",
            return_raw_data_flag=True
        )
        gw_customer_info_identity_info = gw_customer_info['id_info']
        sender_response = dict(
            cif_number=sender_cif_number,
            fullname_vn=gw_customer_info['full_name'],
            address_full=gw_customer_info['t_address_info']['contact_address_full'],
            identity_info=dict(
                number=gw_customer_info_identity_info['id_num'],
                issued_date=gw_customer_info_identity_info['id_issued_date'],
                place_of_issue=gw_customer_info_identity_info['id_issued_location']
            ),
            mobile_phone=gw_customer_info['mobile_phone'],
            telephone=gw_customer_info['telephone'],
            otherphone=gw_customer_info['otherphone']
        )
        if not sender_cif_number:
            sender_response.update(
                fullname_vn=form_data['sender_full_name_vn'],
                address_full=form_data['sender_address_full'],
                identity_info=dict(
                    number=form_data['sender_identity_number'],
                    issued_date=form_data['sender_place_of_issue'],
                    place_of_issue=form_data['sender_place_of_issue']
                ),
                mobile_phone=form_data['sender_mobile_number']
            )
        controller_gw_employee = CtrGWEmployee(current_user)
        gw_direct_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=form_data['direct_staff_code'],
            return_raw_data_flag=True
        )
        direct_staff = dict(
            code=gw_direct_staff['staff_code'],
            name=gw_direct_staff['staff_name']
        )
        gw_indirect_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=form_data['indirect_staff_code'],
            return_raw_data_flag=True
        )
        indirect_staff = dict(
            code=gw_indirect_staff['staff_code'],
            name=gw_indirect_staff['staff_name']
        )
        ################################################################################################################

        response_data = dict(
            transfer_type=dict(
                receiving_method_type=RECEIVING_METHOD__METHOD_TYPES[receiving_method],
                receiving_method=receiving_method
            ),
            receiver=receiver_response,
            transfer=dict(
                amount=transfer_amount,
                content=form_data['content'],
                entry_number=None,  # TODO: Số bút toán
            ),
            fee_info=fee_info,
            statement=statement_response,
            sender=sender_response,
            direct_staff=direct_staff,
            indirect_staff=indirect_staff,
        )

        return self.response(response_data)

    async def ctr_save_casa_top_up_scb_to_account(
            self,
            current_user: AuthResponse,
            request: CasaTopUpSCBToAccountRequest
    ):
        if not isinstance(request, CasaTopUpSCBToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpSCBToAccountRequest, request: {type(request)}'
            )

        sender_cif_number = request.sender_cif_number
        if not sender_cif_number:
            return self.response_exception(msg=ERROR_CIF_NUMBER_NOT_EXIST, loc=f"cif_number: {sender_cif_number}")

        receiver_account_number = request.receiver_account_number

        # Kiểm tra số tài khoản có tồn tại hay không
        casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=receiver_account_number
        )
        if not casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"account_number: {receiver_account_number}"
            )

        return request

    async def ctr_save_casa_top_up_scb_by_identity(
            self,
            request: CasaTopUpSCBByIdentityRequest
    ):
        if not isinstance(request, CasaTopUpSCBByIdentityRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpSCBByIdentityRequest, request: {type(request)}'
            )

        # validate branch
        await self.get_model_object_by_id(model_id=request.receiver_branch.id, model=Branch, loc='branch -> id')

        # validate issued_date
        await self.validate_issued_date(issued_date=request.receiver_issued_date, loc='issued_date')

        # validate place_of_issue
        await self.get_model_object_by_id(
            model_id=request.receiver_place_of_issue.id, model=PlaceOfIssue, loc='place_of_issue -> id'
        )

        return request

    async def ctr_save_casa_top_up_third_party_to_account(
            self,
            request: CasaTopUpThirdPartyToAccountRequest
    ):
        if not isinstance(request, CasaTopUpThirdPartyToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdPartyToAccountRequest, request: {type(request)}'
            )
        # validate branch of bank
        # TODO:
        # await self.get_model_object_by_id(model_id=request.branch.id, model=Branch, loc='branch -> id')
        return request

    async def ctr_save_casa_top_up_third_party_by_identity(
            self,
            request: CasaTopUpThirdPartyByIdentityRequest
    ):
        if not isinstance(request, CasaTopUpThirdPartyByIdentityRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdPartyByIdentityRequest, request: {type(request)}'
            )
        # validate branch of bank
        # TODO:
        # await self.get_model_object_by_id(model_id=request.branch.id, model=Branch, loc='branch -> id')
        return request

    async def ctr_save_casa_top_up_third_party_247_to_account(
            self,
            request: CasaTopUpThirdParty247ToAccountRequest
    ):
        if not isinstance(request, CasaTopUpThirdParty247ToAccountRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdPartyByIdentityRequest, request: {type(request)}'
            )
        # validate branch of bank
        # TODO:
        # await self.get_model_object_by_id(model_id=request.branch.id, model=Branch, loc='branch -> id')
        return request

    async def ctr_save_casa_top_up_third_party_247_to_card(
            self,
            request: CasaTopUpThirdParty247ToCardRequest
    ):
        if not isinstance(request, CasaTopUpThirdParty247ToCardRequest):
            return self.response_exception(
                msg=ERROR_MAPPING_MODEL,
                loc=f'expect: CasaTopUpThirdParty247ToCardRequest, request: {type(request)}'
            )
        # TODO: validate branch of bank
        # await self.get_model_object_by_id(model_id=request.branch.id, model=Branch, loc='branch -> id')

        # TODO: validate card number

        return request

    async def ctr_save_casa_top_up_info(
            self,
            booking_id: str,
            request: Union[
                CasaTopUpSCBToAccountRequest,
                CasaTopUpSCBByIdentityRequest,
                CasaTopUpThirdPartyToAccountRequest,
                CasaTopUpThirdPartyByIdentityRequest,
                CasaTopUpThirdParty247ToAccountRequest,
                CasaTopUpThirdParty247ToCardRequest
            ]
    ):
        sender_cif_number = request.sender_cif_number
        receiving_method = request.receiving_method
        is_fee = request.is_fee
        fee_info = request.fee_info
        statement = request.statement
        direct_staff_code = request.direct_staff_code
        indirect_staff_code = request.indirect_staff_code
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

        if is_fee is not None and not fee_info:
            return self.response_exception(msg=ERROR_NOT_NULL, loc="fee_info")
            # TODO: Case cho bên chuyển/ Bên nhận

        denominations__amounts = DENOMINATIONS__AMOUNTS
        denominations_errors = []
        for index, row in enumerate(statement):
            denominations = row.denominations
            if denominations not in DENOMINATIONS__AMOUNTS:
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

        # Kiểm tra số CIF có tồn tại trong CRM không
        if sender_cif_number:
            # self.call_repos(await repos_get_customer_by_cif_number(
            #     cif_number=cif_number,
            #     session=self.oracle_session
            # ))
            is_existed = await CtrGWCustomer(current_user).ctr_gw_check_exist_customer_detail_info(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            if not is_existed:
                return self.response_exception(msg=ERROR_CIF_NUMBER_NOT_EXIST, loc="cif_number")

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
                request=request
            )

        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
            casa_top_up_info = await self.ctr_save_casa_top_up_scb_by_identity(request=request)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_to_account(request=request)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_by_identity(request=request)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_247_to_account(request=request)

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD:
            casa_top_up_info = await self.ctr_save_casa_top_up_third_party_247_to_card(request=request)

        if not casa_top_up_info:
            return self.response_exception(msg="No Casa Top Up")

        # Tạo data TransactionDaily và các TransactionStage khác cho bước mở CASA
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            business_type_id=BUSINESS_TYPE_CASA_TOP_UP)

        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender
        ) = transaction_datas

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
            request_json=casa_top_up_info.json(),
            history_datas=orjson_dumps(history_datas),
            session=self.oracle_session
        ))

        return self.response(data=dict(
            booking_id=booking_id
        ))
