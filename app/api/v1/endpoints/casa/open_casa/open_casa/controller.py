from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number, repos_save_casa_casa_account, repos_get_acc_structure_types,
    repos_get_casa_open_casa_info
)
from app.api.v1.endpoints.casa.open_casa.open_casa.schema import CasaOpenCasaRequest
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_get_casa_account_info
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.account import AccountType, AccountClass
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.business_type import BUSINESS_TYPE_OPEN_CASA
from app.utils.constant.cif import ACC_STRUCTURE_TYPE_LEVEL_2, STAFF_TYPE_BUSINESS_CODE, \
    PROFILE_HISTORY_DESCRIPTIONS_INIT_PAYMENT_ACCOUNT, PROFILE_HISTORY_STATUS_INIT
from app.utils.error_messages import (
    ERROR_ACCOUNT_NUMBER_NOT_NULL, ERROR_CASA_ACCOUNT_EXIST,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_FIELD_REQUIRED, ERROR_VALIDATE
)
from app.utils.functions import generate_uuid, now, dropdown, optional_dropdown, orjson_dumps


class CtrCasaOpenCasa(BaseController):
    async def ctr_get_casa_open_casa_info(
            self,
            booking_parent_id: str
    ):
        get_casa_open_casa_infos = self.call_repos(await repos_get_casa_open_casa_info(
            booking_parent_id=booking_parent_id,
            session=self.oracle_session
        ))

        casa_accounts = []

        for _, booking, booking_account, casa_account, acc_structure_type_level_1 in get_casa_open_casa_infos:
            casa_accounts.append(dict(
                self_selected_account_flag=casa_account.self_selected_account_flag,
                currency=dropdown(casa_account.currency),
                account_type=dropdown(casa_account.account_type),
                account_class=dropdown(casa_account.account_class),
                account_structure_type_level_1=optional_dropdown(acc_structure_type_level_1),
                account_structure_type_level_2=optional_dropdown(casa_account.account_structure_type),
                account_structure_type_level_3=optional_dropdown(None),
                casa_account_number=casa_account.casa_account_number,
                account_salary_organization_account=casa_account.acc_salary_org_acc,
                account_salary_organization_name=casa_account.acc_salary_org_name
            ))

        return self.response(data=dict(
            transaction_code=booking_parent_id,
            total_item=len(casa_accounts),
            casa_accounts=casa_accounts
        ))

    async def ctr_save_casa_open_casa_info(
            self,
            booking_parent_id: str,
            open_casa_request: CasaOpenCasaRequest
    ):
        cif_number = open_casa_request.cif_number
        casa_accounts = open_casa_request.casa_accounts
        current_user_info = self.current_user.user_info
        saving_casa_accounts = []
        saving_bookings = []
        saving_booking_accounts = []
        is_errors = []

        ################################################################################################################
        # VALIDATE
        ################################################################################################################
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking(
            booking_id=booking_parent_id,
            business_type_code=BUSINESS_TYPE_OPEN_CASA,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_parent_id}'
        )

        # Kiểm tra số CIF có tồn tại trong CRM không
        customer = self.call_repos(await repos_get_customer_by_cif_number(
            cif_number=cif_number,
            session=self.oracle_session
        ))
        currency_ids = []
        acc_type_ids = []
        acc_class_ids = []
        account_structure_type_level_2_ids = []
        for index, request in enumerate(casa_accounts):
            self_selected_account_flag = request.self_selected_account_flag
            account_salary_organization_account = request.account_salary_organization_account
            account_structure_type_level_2_id = None
            acc_salary_org_name = None

            # Nếu tài khoản số đẹp phải truyền số TKTT
            if self_selected_account_flag:
                casa_account_number = request.casa_account_number
                if not casa_account_number:
                    is_errors.append(dict(msg=ERROR_ACCOUNT_NUMBER_NOT_NULL, loc=f"{index} -> casa_account_number"))
            else:
                casa_account_number = 'DEFAULT'

            # Nếu là TKTT tự chọn
            if self_selected_account_flag:
                # check acc_structure_type_level_3_id exist
                account_structure_type_level_2_id = request.account_structure_type_level_2.id
                if not account_structure_type_level_2_id:
                    is_errors.append(dict(
                        loc=f'{index} -> account_info -> account_structure_type_level_2 -> id',
                        msg=ERROR_FIELD_REQUIRED
                    ))
                account_structure_type_level_2_ids.append(account_structure_type_level_2_id)

                # Kiểm tra STK có tồn tại trong GW chưa
                is_existed = await self.ctr_check_exist_casa_account(account_number=casa_account_number)
                if is_existed:
                    is_errors.append(dict(
                        msg=ERROR_CASA_ACCOUNT_EXIST,
                        loc=f'{index} -> casa_account_number'
                    ))

                if account_salary_organization_account:
                    gw_account_organization_info = self.call_repos(await repos_gw_get_casa_account_info(
                        account_number=account_salary_organization_account,
                        current_user=self.current_user.user_info
                    ))
                    account_organization_info = gw_account_organization_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']
                    if account_organization_info['account_info']['account_num'] == '':
                        return self.response_exception(
                            msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                            loc=f'{index} -> account_salary_organization_account'
                        )
                    acc_salary_org_name = account_organization_info['full_name']

            currency_id = request.currency.id
            currency_ids.append(currency_id)

            acc_type_id = request.account_type.id
            acc_type_ids.append(acc_type_id)

            acc_class_id = request.account_class.id
            acc_class_ids.append(acc_class_id)

            casa_account_id = generate_uuid()

            saving_casa_accounts.append(dict(
                id=casa_account_id,
                customer_id=customer.id,
                casa_account_number=casa_account_number,
                currency_id=currency_id,
                acc_type_id=acc_type_id,
                acc_class_id=acc_class_id,
                acc_structure_type_id=account_structure_type_level_2_id,
                staff_type_id=STAFF_TYPE_BUSINESS_CODE,
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
            ))

            booking_id = generate_uuid()
            current_user_info = self.current_user.user_info

            saving_bookings.append(dict(
                id=booking_id,
                parent_id=booking_parent_id,
                code=None,
                transaction_id=None,
                business_type_id=BUSINESS_TYPE_OPEN_CASA,
                branch_id=current_user_info.hrm_branch_code,
                created_at=now(),
                updated_at=now()
            ))

            saving_booking_accounts.append(dict(
                booking_id=booking_id,
                account_id=casa_account_id,
                created_at=now(),
                updated_at=now()
            ))

        if is_errors:
            return self.response_exception(msg=ERROR_VALIDATE, detail=str(is_errors))

        # Check Currency
        await self.get_model_objects_by_ids(
            model_ids=currency_ids,
            model=Currency
        )

        # Check Account Type
        await self.get_model_objects_by_ids(
            model_ids=acc_type_ids,
            model=AccountType
        )

        # Check Account Class
        await self.get_model_objects_by_ids(
            model_ids=acc_class_ids,
            model=AccountClass
        )

        # Trường hợp đặc biệt, phải check luôn cả loại kiến trúc là cấp 2 nên không dùng get_model_object_by_id
        self.call_repos(
            await repos_get_acc_structure_types(
                acc_structure_type_ids=account_structure_type_level_2_ids,
                level=ACC_STRUCTURE_TYPE_LEVEL_2,
                session=self.oracle_session
            )
        )

        # Tạo data TransactionDaily và các TransactionStage khác cho bước mở CASA
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            business_type_id=BUSINESS_TYPE_OPEN_CASA
        )

        (
            saving_transaction_stage_status, saving_transaction_stage, saving_transaction_stage_phase,
            saving_transaction_stage_lane, saving_transaction_stage_role, saving_transaction_daily,
            saving_transaction_sender
        ) = transaction_datas

        print('saving_transaction_stage_status', saving_transaction_stage_status)
        print('saving_transaction_stage', saving_transaction_stage)
        print('saving_transaction_stage_phase', saving_transaction_stage_phase)
        print('saving_transaction_stage_lane', saving_transaction_stage_lane)
        print('saving_transaction_stage_role', saving_transaction_stage_role)
        print('saving_transaction_daily', saving_transaction_daily)
        print('saving_transaction_sender', saving_transaction_sender)

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_PAYMENT_ACCOUNT,
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

        self.call_repos(await repos_save_casa_casa_account(
            saving_casa_accounts=saving_casa_accounts,
            saving_bookings=saving_bookings,
            saving_booking_accounts=saving_booking_accounts,
            booking_parent_id=booking_parent_id,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            request_json=open_casa_request.json(),
            history_datas=orjson_dumps(history_datas),
            session=self.oracle_session
        ))

        return self.response(data=dict(
            booking_parent_id=booking_parent_id,
            booking_accounts=[dict(
                account_id=booking_account['account_id'],
                booking_id=booking_account['booking_id'],
            ) for index, booking_account in enumerate(saving_booking_accounts)]
        ))

    async def ctr_check_exist_casa_account(self, account_number):
        gw_check_exist_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_number,
            current_user=self.current_user.user_info
        ))
        account_info = gw_check_exist_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']['account_info']
        return True if account_info['account_num'] != '' else False
