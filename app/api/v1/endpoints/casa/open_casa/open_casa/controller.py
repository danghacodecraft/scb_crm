from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number, repos_save_casa_casa_account
)
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)
from app.api.v1.endpoints.repository import repos_get_acc_structure_type
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_get_casa_account_info
)
from app.third_parties.oracle.models.master_data.account import AccountType
from app.utils.constant.cif import ACC_STRUCTURE_TYPE_LEVEL_2
from app.utils.error_messages import (
    ERROR_ACCOUNT_NUMBER_NOT_NULL, ERROR_CASA_ACCOUNT_EXIST,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_FIELD_REQUIRED
)
from app.utils.functions import generate_uuid, now


class CtrCasaOpenCasa(BaseController):
    async def ctr_save_casa_open_casa_info(
            self,
            cif_number: str,
            request: SavePaymentAccountRequest
    ):
        self_selected_account_flag = request.self_selected_account_flag
        account_structure_type_level_2_id = None
        acc_type_id = request.account_type.id
        acc_class_id = request.account_class.id
        account_salary_organization_account = request.account_salary_organization_account

        # Nếu tài khoản số đẹp phải truyền số TKTT
        if self_selected_account_flag:
            casa_account_number = request.casa_account_number
            if not casa_account_number:
                return self.response_exception(msg=ERROR_ACCOUNT_NUMBER_NOT_NULL, loc="body -> casa_account_number")
        else:
            casa_account_number = 'DEFAULT'

        # Kiểm tra số CIF có tồn tại trong CRM không
        customer = self.call_repos(await repos_get_customer_by_cif_number(
            cif_number=cif_number,
            session=self.oracle_session
        ))

        # Check Account Type
        await self.get_model_object_by_id(
            model_id=acc_type_id,
            model=AccountType,
            loc="body -> account_type -> id"
        )

        # Nếu là TKTT tự chọn
        if self_selected_account_flag:
            # check acc_structure_type_level_3_id exist
            account_structure_type_level_2_id = request.account_structure_type_level_2.id
            if not account_structure_type_level_2_id:
                return self.response_exception(
                    loc='body -> account_info -> account_structure_type_level_2 -> id',
                    msg=ERROR_FIELD_REQUIRED
                )
            # Trường hợp đặc biệt, phải check luôn cả loại kiến trúc là cấp 2 nên không dùng get_model_object_by_id
            self.call_repos(
                await repos_get_acc_structure_type(
                    acc_structure_type_id=account_structure_type_level_2_id,
                    level=ACC_STRUCTURE_TYPE_LEVEL_2,
                    loc="body -> account_info -> account_structure_type_level_2 -> id",
                    session=self.oracle_session
                )
            )

            # Kiểm tra STK có tồn tại trong GW chưa
            is_existed = await self.ctr_check_exist_casa_account(account_number=casa_account_number)
            if is_existed:
                return self.response_exception(
                    msg=ERROR_CASA_ACCOUNT_EXIST,
                    loc='body -> casa_account_number'
                )

        gw_account_organization_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_salary_organization_account,
            current_user=self.current_user.user_info
        ))
        account_organization_info = gw_account_organization_info['retrieveCurrentAccountCASA_out']['data_output'][
            'customer_info']
        if account_organization_info['account_info']['account_num'] == '':
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc='body -> account_salary_organization_account'
            )
        acc_salary_org_name = account_organization_info['full_name']
        casa_account_id = generate_uuid()
        saving_casa_account = dict(
            id=casa_account_id,
            customer_id=customer.id,
            casa_account_number=casa_account_number,
            currency_id=request.currency.id,
            acc_type_id=acc_type_id,
            acc_class_id=acc_class_id,
            acc_structure_type_id=account_structure_type_level_2_id,
            staff_type_id=None,
            acc_salary_org_name=acc_salary_org_name,
            acc_salary_org_acc=request.account_salary_organization_account,
            maker_id=self.current_user.user_info.code,
            maker_at=now(),
            checker_id=None,
            checker_at=None,
            approve_status=None,
            self_selected_account_flag=self_selected_account_flag,
            acc_active_flag=1,
            created_at=now(),
            updated_at=now()
        )

        self.call_repos(
            await repos_save_casa_casa_account(
                saving_casa_account=saving_casa_account,
                session=self.oracle_session
            )
        )

        return self.response(data=dict(
            account_id=casa_account_id
        ))

    async def ctr_check_exist_casa_account(self, account_number):
        gw_check_exist_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_number,
            current_user=self.current_user.user_info
        ))
        account_info = gw_check_exist_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']['account_info']
        return True if account_info['account_num'] != '' else False
