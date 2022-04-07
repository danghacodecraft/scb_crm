from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.detail.repository import (
    repos_check_casa_account, repos_check_exist_casa_account_number,
    repos_detail_payment_account, repos_get_casa_account_from_soa,
    repos_save_payment_account
)
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.repository import repos_get_acc_structure_type
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountType
)
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.cif import (
    ACC_STRUCTURE_TYPE_LEVEL_3,
    PROFILE_HISTORY_DESCRIPTIONS_INIT_PAYMENT_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT, STAFF_TYPE_BUSINESS_CODE
)
from app.utils.error_messages import (
    ERROR_CASA_ACCOUNT_EXIST, ERROR_CASA_ACCOUNT_NOT_EXIST,
    ERROR_INVALID_NUMBER, ERROR_NOT_NULL, MESSAGE_STATUS
)
from app.utils.functions import (
    datetime_to_string, is_valid_number, now, orjson_dumps
)


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

        return self.response(detail_payment_account_info)

    async def save(self,
                   cif_id: str,
                   payment_account_save_request: SavePaymentAccountRequest):

        current_user = self.current_user

        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # check TKTT đã tạo hay chưa
        is_created = True
        # Không cần gọi self.call_repos
        casa_account = await repos_check_casa_account(
            cif_id=cif_id,
            session=self.oracle_session
        )
        if casa_account.data:
            is_created = False

        casa_account_number = cif_id[:12] + "0001"  # TODO: đợi rule cho CIF thông thường
        account_structure_type_level_3_id = None
        account_salary_organization_account_name = None

        # Nếu là Tài khoản yêu cầu
        self_selected_account_flag = payment_account_save_request.self_selected_account_flag
        if self_selected_account_flag:
            # TODO: Số tài khoản có thể có yêu cầu nghiệp vụ về độ dài tùy theo kiểu kiến trúc, VALIDATE
            casa_account_number = payment_account_save_request.casa_account_number
            if not casa_account_number:
                return self.response_exception(
                    msg=f"casa_account_number {MESSAGE_STATUS[ERROR_NOT_NULL]}",
                    loc="casa_account_number"
                )

            # Kiểm tra tài khoản thanh toán đã tồn tại chưa
            account_salary_organization = self.call_repos(await repos_get_casa_account_from_soa(
                casa_account_number=casa_account_number,
                loc="casa_account_number"
            ))
            if account_salary_organization['is_existed']:
                return self.response_exception(
                    msg=ERROR_CASA_ACCOUNT_EXIST,
                    detail=MESSAGE_STATUS[ERROR_CASA_ACCOUNT_EXIST],
                    loc="casa_account_number"
                )

            if payment_account_save_request.account_structure_type_level_3.id:
                # check acc_structure_type_level_3_id exist
                # Trường hợp đặc biệt, phải check luôn cả loại kiến trúc là cấp 3 nên không dùng get_model_object_by_id
                account_structure_type_level_3_id = payment_account_save_request.account_structure_type_level_3.id
                self.call_repos(
                    await repos_get_acc_structure_type(
                        acc_structure_type_id=account_structure_type_level_3_id,
                        level=ACC_STRUCTURE_TYPE_LEVEL_3,
                        loc="account_structure_type_level_3",
                        session=self.oracle_session
                    )
                )

        # Lấy thông tin Tài khoản của tổ chức chi lương
        account_salary_organization_account_number = payment_account_save_request.account_salary_organization_account
        if account_salary_organization_account_number:
            account_salary_organization = self.call_repos(await repos_get_casa_account_from_soa(
                casa_account_number=account_salary_organization_account_number,
                loc="account_salary_organization_account"
            ))

            if not account_salary_organization['is_existed']:
                return self.response_exception(
                    msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                    detail=MESSAGE_STATUS[ERROR_CASA_ACCOUNT_NOT_EXIST],
                    loc="account_salary_organization_account"
                )

            account_salary_organization_account_name = account_salary_organization['retrieveCurrentAccountCASA_out']['accountInfo']['customerInfo']['fullname']

        # Mở tài khoản thông thường, hiện tại không gửi data để lưu kiểu kiến trúc cấp 3

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
        await self.get_model_object_by_id(
            model=AccountClass,
            model_id=payment_account_save_request.account_class.id,
            loc="account_class"
        )

        data_insert = {
            "customer_id": cif_id,
            "casa_account_number": casa_account_number,
            "currency_id": payment_account_save_request.currency.id,
            'acc_type_id': payment_account_save_request.account_type.id,
            'acc_class_id': payment_account_save_request.account_class.id,
            'acc_structure_type_id': account_structure_type_level_3_id,
            "staff_type_id": STAFF_TYPE_BUSINESS_CODE,
            "acc_salary_org_name": account_salary_organization_account_name,
            "acc_salary_org_acc": account_salary_organization_account_number,
            "maker_id": self.current_user.code,
            "maker_at": now(),
            "checker_id": 1,
            "checker_at": None,
            "approve_status": None,
            "self_selected_account_flag": self_selected_account_flag,
            "acc_active_flag": 1,
            "created_at": now(),
            "updated_at": now(),
        }

        history_datas = [dict(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_PAYMENT_ACCOUNT,
            completed_at=datetime_to_string(now()),
            created_at=datetime_to_string(now()),
            status=PROFILE_HISTORY_STATUS_INIT,
            branch_id=current_user.hrm_branch_id,
            branch_code=current_user.hrm_branch_code,
            branch_name=current_user.hrm_branch_name,
            user_id=current_user.code,
            user_name=current_user.name,
            position_id=current_user.hrm_position_id,
            position_code=current_user.hrm_position_code,
            position_name=current_user.hrm_position_name
        )]
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
                created_by=current_user.username,
                session=self.oracle_session,
                is_created=is_created
            ))

        return self.response(data=save_payment_account_info)

    async def check_exist_casa_account_number(self, casa_account_number):
        # VALIDATE: casa_account_number
        if not is_valid_number(casa_account_number):
            return self.response_exception(
                msg=ERROR_INVALID_NUMBER,
                loc="casa_account_number"
            )

        casa_account_info = self.call_repos(
            await repos_check_exist_casa_account_number(
                casa_account_number=casa_account_number,
                session=self.oracle_session
            )
        )
        return self.response(data=casa_account_info)
