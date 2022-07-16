from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.controller import (
    CtrCasaOpenCasa
)
from app.api.v1.endpoints.cif.payment_account.detail.repository import (
    repos_check_casa_account, repos_detail_payment_account,
    repos_gw_check_exist_casa_account_number, repos_save_payment_account
)
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking, repos_get_initializing_customer
)
from app.api.v1.endpoints.config.account.repository import (
    repos_get_account_classes
)
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_get_casa_account_info
)
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.account import AccountType
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.cif import (
    DROPDOWN_NONE_DICT, PROFILE_HISTORY_DESCRIPTIONS_OPEN_CASA_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT, STAFF_TYPE_BUSINESS_CODE
)
from app.utils.error_messages import (
    ERROR_ACCOUNT_NUMBER_NOT_NULL, ERROR_CASA_ACCOUNT_EXIST,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_FIELD_REQUIRED, ERROR_ID_NOT_EXIST,
    ERROR_INVALID_NUMBER
)
from app.utils.functions import dropdown, is_valid_number, now, orjson_dumps


class CtrPaymentAccount(BaseController):

    async def detail(self, cif_id: str):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        detail_payment_account_info = self.call_repos(
            await repos_detail_payment_account(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        account_structure_type_level_1 = detail_payment_account_info.account_structure_type_level_1
        account_structure_type_level_2 = detail_payment_account_info.account_structure_type_level_2
        account_structure_type_level_3 = detail_payment_account_info.AccountStructureType

        return self.response(data=dict(
            self_selected_account_flag=detail_payment_account_info.CasaAccount.self_selected_account_flag,
            currency=dropdown(detail_payment_account_info.Currency),
            country=dropdown(detail_payment_account_info.AddressCountry),
            account_type=dropdown(detail_payment_account_info.AccountType),
            account_class=dropdown(detail_payment_account_info.AccountClass),
            account_structure_type_level_1=dropdown(account_structure_type_level_1)
            if account_structure_type_level_1 else DROPDOWN_NONE_DICT,
            account_structure_type_level_2=dropdown(account_structure_type_level_2)
            if account_structure_type_level_2 else DROPDOWN_NONE_DICT,
            account_structure_type_level_3=dropdown(account_structure_type_level_3)
            if account_structure_type_level_3 else DROPDOWN_NONE_DICT,
            casa_account_number=detail_payment_account_info.CasaAccount.casa_account_number,
            account_salary_organization_account=detail_payment_account_info.CasaAccount.acc_salary_org_acc,
            account_salary_organization_name=detail_payment_account_info.CasaAccount.acc_salary_org_name,
            id=detail_payment_account_info.CasaAccount.id,
            approve_status=detail_payment_account_info.CasaAccount.approve_status,
        ))

    async def save(self,
                   cif_id: str,
                   payment_account_save_request: SavePaymentAccountRequest):

        current_user = self.current_user
        current_user_info = current_user.user_info

        # check cif đang tạo
        customer = self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # check TKTT đã tạo hay chưa
        is_created = True
        # Không cần gọi self.call_repos
        casa_account = await repos_check_casa_account(
            cif_id=cif_id,
            session=self.oracle_session
        )
        if casa_account.data:
            is_created = False

        # Nếu là Tài khoản yêu cầu
        self_selected_account_flag = payment_account_save_request.self_selected_account_flag
        account_salary_organization_account = payment_account_save_request.account_salary_organization_account
        account_structure_type_level_2_id = None
        acc_salary_org_name = None

        # Nếu tài khoản số đẹp phải truyền số TKTT
        casa_account_number = None
        if self_selected_account_flag:
            casa_account_number = payment_account_save_request.casa_account_number
            if not casa_account_number:
                return self.response_exception(msg=ERROR_ACCOUNT_NUMBER_NOT_NULL, loc="casa_account_number")

        # Nếu là TKTT tự chọn
        if self_selected_account_flag:
            # check acc_structure_type_level_2_id exist
            account_structure_type_level_2_id = payment_account_save_request.account_structure_type_level_2.id
            if not account_structure_type_level_2_id:
                return self.response_exception(
                    loc='account_info -> account_structure_type_level_2 -> id',
                    msg=ERROR_FIELD_REQUIRED
                )

            # Kiểm tra STK có tồn tại trong GW chưa
            is_existed = await CtrCasaOpenCasa(current_user=current_user).ctr_check_exist_casa_account(
                account_number=casa_account_number)
            if is_existed:
                return self.response_exception(
                    msg=ERROR_CASA_ACCOUNT_EXIST,
                    loc='casa_account_number'
                )

            if account_salary_organization_account:
                gw_account_organization_info = self.call_repos(await repos_gw_get_casa_account_info(
                    account_number=account_salary_organization_account,
                    current_user=self.current_user.user_info
                ))
                account_organization_info = \
                    gw_account_organization_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']
                if account_organization_info['account_info']['account_num'] == '':
                    return self.response_exception(
                        msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                        loc='account_salary_organization_account'
                    )
                acc_salary_org_name = account_organization_info['full_name']

        # check currency exist
        await self.get_model_object_by_id(
            model=Currency,
            model_id=payment_account_save_request.currency.id,
            loc="currency"
        )

        # check account_type exist
        await self.get_model_object_by_id(
            model=AccountType,
            model_id=payment_account_save_request.account_type.id,
            loc="account_type"
        )

        # check account_class exist
        is_existed = self.call_repos(await repos_get_account_classes(
            customer_category_id=customer.customer_category_id,
            account_class_ids=[payment_account_save_request.account_class.id],
            session=self.oracle_session
        ))
        if not is_existed:
            return self.response_exception(
                msg=ERROR_ID_NOT_EXIST,
                loc="payment_account_save_request -> account_class -> id"
            )

        data_insert = {
            "customer_id": cif_id,
            "casa_account_number": casa_account_number,
            "currency_id": payment_account_save_request.currency.id,
            'acc_type_id': payment_account_save_request.account_type.id,
            'acc_class_id': payment_account_save_request.account_class.id,
            'acc_structure_type_id': account_structure_type_level_2_id,
            "staff_type_id": STAFF_TYPE_BUSINESS_CODE,
            "acc_salary_org_name": acc_salary_org_name,
            "acc_salary_org_acc": account_salary_organization_account,
            "maker_id": current_user_info.code,
            "maker_at": now(),
            "checker_id": None,
            "checker_at": None,
            "approve_status": 0,
            "self_selected_account_flag": self_selected_account_flag,
            "acc_active_flag": 1,
            "created_at": now(),
            "updated_at": now(),
        }

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_OPEN_CASA_ACCOUNT,
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

        save_payment_account_info = self.call_repos(
            await repos_save_payment_account(
                cif_id=cif_id,
                data_insert=data_insert,
                log_data=payment_account_save_request.json(),
                history_datas=orjson_dumps(history_datas),
                created_by=current_user_info.username,
                session=self.oracle_session,
                is_created=is_created
            ))

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        save_payment_account_info.update(booking=dict(
            id=booking.id,
            code=booking.code
        ))

        return self.response(data=save_payment_account_info)

    async def check_exist_casa_account_number(self, casa_account_number):
        # VALIDATE: casa_account_number
        if not is_valid_number(casa_account_number):
            return self.response_exception(
                msg=ERROR_INVALID_NUMBER,
                loc="casa_account_number"
            )

        casa_account_info = await CtrGWCasaAccount().ctr_gw_get_casa_account_info(
            account_number=casa_account_number,
            return_raw_data_flag=True
        )

        return self.response(data=casa_account_info)

    async def ctr_gw_check_exist_casa_account_number(self, cif_id, casa_account_number):
        current_user = self.current_user

        # VALIDATE: casa_account_number
        if not is_valid_number(casa_account_number):
            return self.response_exception(
                msg=ERROR_INVALID_NUMBER,
                loc="casa_account_number"
            )

        data_output = self.call_repos(
            await repos_gw_check_exist_casa_account_number(
                casa_account_number=casa_account_number,
                current_user=current_user
            )
        )
        is_existed = False
        if data_output['retrieveCurrentAccountCASA_out']['data_output']['customer_info']['account_info']['account_num']:
            is_existed = True
        return self.response(data=dict(is_existed=is_existed))
