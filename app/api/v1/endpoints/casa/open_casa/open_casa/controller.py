from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_acc_structure_types, repos_get_casa_open_casa_info_from_booking,
    repos_save_casa_casa_account
)
from app.api.v1.endpoints.casa.open_casa.open_casa.schema import (
    CasaOpenCasaRequest
)
from app.api.v1.endpoints.config.account.repository import (
    repos_get_account_classes
)
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_get_casa_account_info
)
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_gw_get_customer_info_detail
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountStructureType, AccountType
)
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.business_type import BUSINESS_TYPE_OPEN_CASA
from app.utils.constant.casa import CASA_ACCOUNT_STATUS_UNAPPROVED
from app.utils.constant.cif import (
    ACC_STRUCTURE_TYPE_LEVEL_2, DROPDOWN_NONE_DICT,
    PROFILE_HISTORY_DESCRIPTIONS_OPEN_CASA_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT, STAFF_TYPE_BUSINESS_CODE
)
from app.utils.error_messages import (
    ERROR_ACCOUNT_NUMBER_NOT_NULL, ERROR_CASA_ACCOUNT_EXIST,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_FIELD_REQUIRED, ERROR_VALIDATE
)
from app.utils.functions import (
    dropdown, generate_uuid, now, optional_dropdown, orjson_dumps, orjson_loads
)


class CtrCasaOpenCasa(BaseController):
    async def ctr_get_casa_open_casa_info(
            self,
            booking_parent_id: str
    ):
        get_casa_open_casa_infos = self.call_repos(await repos_get_casa_open_casa_info_from_booking(
            booking_id=booking_parent_id,
            session=self.oracle_session
        ))

        casa_accounts = []

        mark_created_at = None
        # Lấy thông tin Lưu tài khoản cập nhật mới nhất
        for booking, booking_account, booking_business_form in get_casa_open_casa_infos:
            form_data = orjson_loads(booking_business_form.form_data)
            form_data['account_info']['approval_status'] = booking_business_form.is_success
            if not mark_created_at:
                mark_created_at = booking_business_form.created_at
                casa_accounts.append(form_data)
            elif mark_created_at == booking_business_form.created_at:
                casa_accounts.append(form_data)

        booking = await CtrBooking(current_user=self.current_user).ctr_get_booking(
            booking_id=booking_parent_id,
            business_type_code=BUSINESS_TYPE_OPEN_CASA
        )

        return self.response(data=dict(
            booking_parent_id=booking_parent_id,
            transaction_code=booking.code,
            total_item=len(casa_accounts),
            casa_accounts=casa_accounts,
            read_only=booking.completed_flag
        ))

    async def ctr_save_casa_open_casa_info(
            self,
            booking_parent_id: str,
            open_casa_request: CasaOpenCasaRequest
    ):
        cif_number = open_casa_request.cif_number
        casa_accounts = open_casa_request.casa_accounts
        current_user = self.current_user
        current_user_info = current_user.user_info
        saving_casa_accounts = []
        saving_bookings = []
        saving_booking_accounts = []
        saving_booking_child_business_forms = []
        is_errors = []

        ################################################################################################################
        # VALIDATE
        ################################################################################################################
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_parent_id,
            business_type_code=BUSINESS_TYPE_OPEN_CASA,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_parent_id}',
            check_completed_booking=True
        )

        currency_ids = []
        acc_type_ids = []
        acc_class_ids = []
        account_structure_type_level_2_ids = []

        gw_customer_detail = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number,
            current_user=current_user
        ))

        for index, request in enumerate(casa_accounts):
            self_selected_account_flag = request.self_selected_account_flag
            account_salary_organization_account = request.account_salary_organization_account
            account_structure_type_level_2_id = None
            acc_salary_org_name = None

            # Nếu tài khoản số đẹp phải truyền số TKTT
            casa_account_number = None
            if self_selected_account_flag:
                casa_account_number = request.casa_account_number
                if not casa_account_number:
                    is_errors.append(dict(msg=ERROR_ACCOUNT_NUMBER_NOT_NULL, loc=f"{index} -> casa_account_number"))

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
                    acc_salary_org_name = "account_organization_info['full_name']"

            currency_id = request.currency.id
            currency_ids.append(currency_id)

            acc_type_id = request.account_type.id
            acc_type_ids.append(acc_type_id)

            acc_class_id = request.account_class.id
            acc_class_ids.append(acc_class_id)

            casa_account_id = generate_uuid()

            saving_casa_accounts.append(dict(
                id=casa_account_id,
                casa_account_number=casa_account_number,
                currency_id=currency_id,
                acc_type_id=acc_type_id,
                acc_class_id=acc_class_id,
                acc_structure_type_id=account_structure_type_level_2_id,
                staff_type_id=STAFF_TYPE_BUSINESS_CODE,
                acc_salary_org_name=acc_salary_org_name,
                acc_salary_org_acc=request.account_salary_organization_account,
                maker_id=self.current_user.user_info.username,
                maker_at=now(),
                checker_id=None,
                checker_at=None,
                approve_status=CASA_ACCOUNT_STATUS_UNAPPROVED,
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
                account_number=request.casa_account_number,
                created_at=now(),
                updated_at=now()
            ))

            # Check Currency
            dropdown_currency = await self.get_model_object_by_id(
                model_id=currency_id,
                model=Currency,
                loc="currency_id"
            )
            # Check Account Type
            dropdown_account_type = await self.get_model_object_by_id(
                model_id=acc_type_id,
                model=AccountType,
                loc="acc_type_id"
            )

            # Check Account Class
            dropdown_account_class = await self.get_model_object_by_id(
                model_id=acc_class_id,
                model=AccountClass,
                loc="acc_class_id"
            )

            # Check Acc Struct type
            account_structure_type_level_2_id = request.account_structure_type_level_2.id
            dropdown_account_structure_type_level_2 = None
            dropdown_account_structure_type_level_1 = None
            if account_structure_type_level_2_id:
                dropdown_account_structure_type_level_2 = self.call_repos(await repos_get_acc_structure_types(
                    acc_structure_type_ids=[account_structure_type_level_2_id],
                    level=2,
                    session=self.oracle_session
                ))
                if not dropdown_account_structure_type_level_2:
                    return self.response_exception(msg=ERROR_VALIDATE, loc=f"{index} -> account_structure_type_level_2_id")

                dropdown_account_structure_type_level_1 = await self.get_model_object_by_id(
                    model_id=account_structure_type_level_2_id,
                    model=AccountStructureType,
                    loc=f"{index} -> account_structure_type_level_1_id"
                )

            saving_booking_child_business_forms.append(dict(
                booking_business_form_id=generate_uuid(),
                booking_id=booking_id,
                form_data=orjson_dumps(dict(
                    cif_number=cif_number,
                    account_info=dict(
                        self_selected_account_flag=request.self_selected_account_flag,
                        currency=dropdown(dropdown_currency),
                        account_type=dropdown(dropdown_account_type),
                        account_class=dropdown(dropdown_account_class),
                        account_structure_type_level_2=optional_dropdown(
                            dropdown_account_structure_type_level_2[0]
                        ) if dropdown_account_structure_type_level_2 else DROPDOWN_NONE_DICT,
                        account_structure_type_level_1=optional_dropdown(
                            dropdown_account_structure_type_level_1
                        ) if dropdown_account_structure_type_level_1 else DROPDOWN_NONE_DICT,
                        account_structure_type_level_3=DROPDOWN_NONE_DICT,
                        casa_account_number=request.casa_account_number,
                        approve_status=None,
                        account_salary_organization_account=request.account_salary_organization_account,
                        account_salary_organization_name=acc_salary_org_name
                    )
                )),
                business_form_id=BUSINESS_TYPE_OPEN_CASA,
                created_at=now(),
                save_flag=True,
                log_data=None
            ))
            print(saving_booking_child_business_forms)

        if is_errors:
            return self.response_exception(msg=ERROR_VALIDATE, detail=str(is_errors))

        # Check Account Class
        account_class_ids = self.call_repos(await repos_get_account_classes(
            customer_category_id=gw_customer_detail['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info']['customer_category'],
            account_class_ids=acc_class_ids,
            session=self.oracle_session
        ))
        unique_account_class_ids = set(account_class_ids)
        unique_unique_account_class_ids = set(unique_account_class_ids)
        if len(unique_account_class_ids) != len(unique_unique_account_class_ids):
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_EXIST,
                detail=f'{unique_unique_account_class_ids.intersection(unique_account_class_ids)} is not exist'
            )

        # Trường hợp đặc biệt, phải check luôn cả loại kiến trúc là cấp 2 nên không dùng get_model_object_by_id
        self.call_repos(
            await repos_get_acc_structure_types(
                acc_structure_type_ids=account_structure_type_level_2_ids,
                level=ACC_STRUCTURE_TYPE_LEVEL_2,
                session=self.oracle_session
            )
        )

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
        request_json = open_casa_request.json()
        history_datas = orjson_dumps(history_datas)

        # Tạo data TransactionDaily và các TransactionStage khác cho bước mở CASA
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_OPEN_CASA,
            booking_id=booking_parent_id,
            request_json=request_json,
            history_datas=history_datas
        )

        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        self.call_repos(await repos_save_casa_casa_account(
            saving_casa_accounts=saving_casa_accounts,
            saving_bookings=saving_bookings,
            saving_booking_accounts=saving_booking_accounts,
            booking_parent_id=booking_parent_id,
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
            saving_booking_child_business_forms=saving_booking_child_business_forms,
            session=self.oracle_session
        ))

        return self.response(data=dict(
            booking_parent_id=booking_parent_id,
            booking_ids=[saving_booking_account['booking_id'] for saving_booking_account in saving_booking_accounts]
        ))

    async def ctr_check_exist_casa_account(self, account_number):
        gw_check_exist_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_number,
            current_user=self.current_user.user_info
        ))
        account_info = gw_check_exist_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']['account_info']
        return True if account_info['account_num'] != '' else False
