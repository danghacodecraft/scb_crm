from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number
)
from app.api.v1.endpoints.casa.transfer.repository import (
    repos_get_casa_transfer_info
)
from app.api.v1.endpoints.config.bank.controller import CtrConfigBank
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_check_casa_account_approved, repos_gw_change_status_account,
    repos_gw_get_casa_account_by_cif_number, repos_gw_get_casa_account_info,
    repos_gw_get_close_casa_account,
    repos_gw_get_column_chart_casa_account_info,
    repos_gw_get_pie_chart_casa_account_info,
    repos_gw_get_retrieve_ben_name_by_account_number,
    repos_gw_get_retrieve_ben_name_by_card_number,
    repos_gw_get_statements_casa_account_info, repos_gw_get_tele_transfer,
    repos_gw_open_casa_account, repos_gw_withdraw,
    repos_open_casa_get_casa_account_infos,
    repos_update_casa_account_to_approved
)
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWOpenCasaAccountRequest, GWReportColumnChartHistoryAccountInfoRequest,
    GWReportPieChartHistoryAccountInfoRequest,
    GWReportStatementHistoryAccountInfoRequest
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_gw_interbank_transfer, repos_gw_pay_in_cash,
    repos_gw_save_casa_transfer_info, repos_gw_tele_transfer,
    repos_gw_tt_liquidation, repos_pay_in_cash_247_by_acc_num,
    repos_pay_in_cash_247_by_card_num
)
from app.api.v1.endpoints.third_parties.repository import (
    repos_save_gw_output_data
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.approval import CIF_STAGE_APPROVE_KSV
from app.utils.constant.business_type import (
    BUSINESS_TYPE_CASA_TOP_UP, BUSINESS_TYPE_CASA_TRANSFER,
    BUSINESS_TYPE_OPEN_CASA
)
from app.utils.constant.casa import (
    CASA_ACCOUNT_STATUS_UNAPPROVED, PAYER_RECEIVER, PAYER_TRANSFER,
    PAYMENT_PAYERS, RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_CLOSE_CASA, BUSINESS_FORM_WITHDRAW
)
from app.utils.constant.gw import (
    GW_ACCOUNT_CHARGE_ON_ORDERING, GW_ACCOUNT_CHARGE_ON_RECEIVER,
    GW_CORE_DATE_FORMAT, GW_DATE_FORMAT, GW_DATETIME_FORMAT, GW_DEFAULT_VALUE,
    GW_FUNC_TELE_TRANSFER_OUT, GW_FUNC_TT_LIQUIDATION_OUT, GW_GL_BRANCH_CODE,
    GW_TRANSACTION_TYPE_SEND, GW_TRANSACTION_TYPE_WITHDRAW
)
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_KSV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_KSV
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_NO_INSTRUMENT_NUMBER, ERROR_PERMISSION
)
from app.utils.functions import (
    date_string_to_other_date_string_format, date_to_string,
    datetime_to_string, now, orjson_dumps, orjson_loads, string_to_date
)


class CtrGWCasaAccount(BaseController):
    async def ctr_gw_get_casa_account_by_cif_number(
            self,
            cif_number: str
    ):
        account_info = self.call_repos(await repos_gw_get_casa_account_by_cif_number(
            cif_number=cif_number,
            current_user=self.current_user
        ))
        response_data = {}
        total_balances = 0
        customer_info = account_info['selectCurrentAccountFromCIF_out']['data_output']['customer_info']
        account_info_list = customer_info['account_info_list']
        full_name_vn = customer_info['full_name']
        account_infos = []
        for account in account_info_list:
            account_info_item = account['account_info_item']
            balance = int(account_info_item['account_balance'])
            total_balances += balance
            branch_info = account_info_item["branch_info"]
            account_infos.append(dict(
                number=account_info_item["account_num"],
                type=account_info_item["account_type"],
                type_name=account_info_item["account_type_name"],
                currency=account_info_item["account_currency"],
                balance=account_info_item["account_balance"],
                balance_available=account_info_item["account_balance_available"],
                balance_available_vnd=account_info_item["account_balance_available_vnd"],
                balance_lock=account_info_item["account_balance_lock"],
                over_draft_limit=account_info_item["account_over_draft_limit"],
                over_draft_expired_date=string_to_date(account['account_info_item']["account_over_draft_expired_date"],
                                                       _format=DATETIME_INPUT_OUTPUT_FORMAT),
                latest_trans_date=string_to_date(account['account_info_item']["account_latest_trans_date"],
                                                 _format=DATETIME_INPUT_OUTPUT_FORMAT),
                open_date=string_to_date(account['account_info_item']["account_open_date"],
                                         _format=DATETIME_INPUT_OUTPUT_FORMAT),
                maturity_date=string_to_date(account['account_info_item']["account_maturity_date"],
                                             _format=DATETIME_INPUT_OUTPUT_FORMAT),
                lock_status=account_info_item["account_lock_status"],
                class_name=account_info_item["account_class_name"],
                class_code=account_info_item["account_class_code"],
                branch_info=dict(
                    code=branch_info["branch_code"],
                    name=branch_info["branch_name"]
                )
            ))

        response_data.update(dict(
            total_balances=total_balances,
            full_name_vn=full_name_vn,
            total_items=len(account_infos),
            account_info_list=account_infos
        ))
        return self.response(data=response_data)

    async def ctr_gw_get_casa_account_info(
            self,
            account_number: str,
            return_raw_data_flag: bool = False
    ):
        gw_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_number,
            current_user=self.current_user.user_info
        ))
        gw_casa_account_info_output = gw_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']
        if return_raw_data_flag:
            return gw_casa_account_info_output

        customer_info = gw_casa_account_info_output['customer_info']
        gw_casa_customer_info_response = dict(
            fullname_vn=customer_info['full_name'],
            date_of_birth=customer_info['birthday'],
            gender=customer_info['gender'],
            email=customer_info['email'],
            mobile_phone=customer_info['mobile_phone'],
            type=customer_info['customer_type']
        )

        cif_info = customer_info['cif_info']
        gw_casa_cif_info_response = dict(
            cif_number=cif_info['cif_num'],
            issued_date=cif_info['cif_issued_date']
        )

        account_info = customer_info['account_info']

        lock_infos = account_info['account_lock_info']

        branch_info = account_info['branch_info']
        status_info = []
        if account_info['account_status']:
            for key, value in account_info['account_status'][0].items():
                status_info.append(dict(
                    id=key,
                    code=key,
                    name=value
                ))

        staff_info_direct = account_info['staff_info_direct']
        staff_info_indirect = account_info['staff_info_indirect']

        lock_none = {
            "balance_lock": "",
            "date_lock": "",
            "expire_date_lock": "",
            "type_code_lock": "",
            "type_name_lock": "",
            "reason_lock": "",
            "ref_no": ""
        }

        lock_info_response = []

        for lock_info in lock_infos:
            lock_dict = dict(
                balance_lock=lock_info['account_balance_lock'],
                date_lock=lock_info['account_date_lock'],
                expire_date_lock=lock_info['account_expire_date_lock'],
                type_code_lock=lock_info['account_type_code_lock'],
                type_name_lock=lock_info['account_type_name_lock'],
                reason_lock=lock_info['account_reason_lock'],
                ref_no=lock_info['account_ref_no'])
            if lock_dict != lock_none:
                lock_info_response.append(lock_dict)

        gw_casa_account_info_response = dict(
            number=account_info['account_num'],
            type=account_info['account_type'],
            type_name=account_info['account_type_name'],
            currency=account_info['account_currency'],
            product_package=account_info["account_product_package"],
            balance=account_info['account_balance'],
            balance_available=account_info['account_balance_available'],
            balance_available_vnd=account_info['account_balance_available_vnd'],
            balance_lock=account_info['account_balance_lock'],
            over_draft_limit=account_info['account_over_draft_limit'],
            over_draft_used=account_info['account_over_draft_used'],
            over_draft_remain=account_info['account_over_draft_remain'],
            over_draft_expired_date=string_to_date(account_info['account_over_draft_expired_date'],
                                                   _format=DATETIME_INPUT_OUTPUT_FORMAT),
            latest_transaction_date=string_to_date(account_info['account_latest_trans_date'],
                                                   _format=DATETIME_INPUT_OUTPUT_FORMAT),
            open_date=string_to_date(account_info['account_open_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT),
            maturity_date=string_to_date(account_info['account_maturity_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT),
            status=status_info,
            lock_status=account_info['account_lock_status'],
            class_name=account_info['account_class_name'],
            class_code=account_info['account_class_code'],
            saving_serials=account_info['account_saving_serials'],
            pre_open_date=string_to_date(account_info['account_pre_open_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT),
            service=account_info['account_service'],
            service_date=string_to_date(account_info['account_service_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT),
            company_salary=account_info['account_company_salary'],
            company_salary_num=account_info['account_company_salary_num'],
            service_escrow=account_info['account_service_escrow'],
            amount_rate_close=account_info['account_amount_rate_close'],
            fee_close=account_info['account_fee_close'],
            total=int(account_info['account_balance']) + int(account_info['account_amount_rate_close'])
            if account_info['account_amount_rate_close'] and account_info['account_balance'] else None,
            service_escrow_ex_date=string_to_date(account_info['account_service_escrow_ex_date'],
                                                  _format=DATETIME_INPUT_OUTPUT_FORMAT),
            lock_info=lock_info_response,
            branch_info=dict(
                code=branch_info['branch_code'],
                name=branch_info['branch_name']
            ),
            staff_info_direct=dict(
                code=staff_info_direct['staff_code'],
                name=staff_info_direct['staff_name']
            ),
            staff_info_indirect=dict(
                code=staff_info_indirect['staff_code'],
                name=staff_info_indirect['staff_name']
            )
        )

        return self.response(data=dict(
            account_info=gw_casa_account_info_response,
            customer_info=gw_casa_customer_info_response,
            cif_info=gw_casa_cif_info_response
        ))

    async def ctr_gw_check_exist_casa_account_info(
            self,
            account_number: str
    ):
        current_user_info = self.current_user.user_info
        gw_check_exist_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_number,
            current_user=current_user_info
        ))
        if not gw_check_exist_casa_account_info:
            return self.response(data=dict(is_existed=False))
        customer_info = gw_check_exist_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']
        account_info = customer_info['account_info']
        is_lower_core_fcc_date = False
        account_open_date = string_to_date(account_info['account_open_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT)
        if account_open_date and current_user_info.fcc_current_date and account_open_date <= current_user_info.fcc_current_date:
            is_lower_core_fcc_date = True

        return self.response(data=dict(
            is_existed=True if account_info['account_num'] else False,
            account_owner=customer_info['full_name'],
            is_lower_core_fcc_date=is_lower_core_fcc_date
        ))

    async def ctr_gw_get_pie_chart_casa_account_info(self, request: GWReportPieChartHistoryAccountInfoRequest):
        gw_report_history_account_info = self.call_repos(await repos_gw_get_pie_chart_casa_account_info(
            account_number=request.account_number,
            current_user=self.current_user.user_info
        ))
        report_casa_accounts = \
            gw_report_history_account_info['selectReportCaSaFromAcc_out']['data_output']['report_info'][
                'report_casa_account']

        pie_chart = []
        total_value = 0
        total_count = 0
        for report_casa_account in report_casa_accounts:
            pie_chart.append(dict(
                transaction_type=report_casa_account['tran_type'],
                transaction_count=report_casa_account['tran_count'],
                transaction_value=report_casa_account['tran_value']
            ))
            total_value += int(report_casa_account['tran_value'])
            total_count += int(report_casa_account['tran_count'])

        if not (total_value == 0 or total_count == 0):
            value_percents = 0
            count_percents = 0
            for index, pie in enumerate(pie_chart):
                if index != -1:
                    value_percent = float(int(pie['transaction_value']) * 100 / total_value)
                    value_percents += value_percent

                    count_percent = float(int(pie['transaction_count']) * 100 / total_count)
                    count_percents += value_percent

                    pie.update(
                        value_percent=value_percent,
                        count_percent=count_percent
                    )
                else:
                    pie.update(
                        value_percent=100 - value_percents,
                        count_percent=100 - count_percents
                    )

        return self.response(data=pie_chart)

    async def ctr_gw_get_column_chart_casa_account_info(self, request: GWReportColumnChartHistoryAccountInfoRequest):
        gw_report_column_chart_casa_account_info = self.call_repos(await repos_gw_get_column_chart_casa_account_info(
            account_number=request.account_number,
            current_user=self.current_user.user_info,
            from_date=request.from_date,
            to_date=request.to_date
        ))
        report_casa_accounts = \
            gw_report_column_chart_casa_account_info['selectReportHisCaSaFromAcc_out']['data_output']['report_info'][
                'report_casa_account']

        column_chart = []
        report_casa_accounts = sorted(report_casa_accounts, key=lambda i: i['tran_date'])
        previous_date = None
        for report_casa_account in report_casa_accounts:
            transaction_date = string_to_date(report_casa_account['tran_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT)
            transaction_type = report_casa_account['tran_type']
            transaction_value = report_casa_account['tran_value']
            send_withdraw_response = dict(
                transaction_type=transaction_type,
                transaction_value=transaction_value
            )
            # TH1: chưa có data
            if not column_chart:
                if transaction_type == GW_TRANSACTION_TYPE_SEND:
                    column_chart.append(dict(
                        transaction_date=transaction_date,
                        send=send_withdraw_response
                    ))
                if transaction_type == GW_TRANSACTION_TYPE_WITHDRAW:
                    column_chart.append(dict(
                        transaction_date=transaction_date,
                        withdraw=send_withdraw_response
                    ))
                previous_date = transaction_date
            # TH2: data cùng 1 ngày
            elif transaction_date == previous_date:
                if transaction_type == GW_TRANSACTION_TYPE_SEND:
                    column_chart[-1].update(dict(
                        send=send_withdraw_response
                    ))
                if transaction_type == GW_TRANSACTION_TYPE_WITHDRAW:
                    column_chart[-1].update(dict(
                        withdraw=send_withdraw_response
                    ))
            # TH2: data khác ngày
            else:
                if transaction_type == GW_TRANSACTION_TYPE_SEND:
                    column_chart.append(dict(
                        transaction_date=transaction_date,
                        send=send_withdraw_response
                    ))
                if transaction_type == GW_TRANSACTION_TYPE_WITHDRAW:
                    column_chart.append(dict(
                        transaction_date=transaction_date,
                        withdraw=send_withdraw_response
                    ))
                previous_date = transaction_date

        gw_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=request.account_number,
            current_user=self.current_user.user_info
        ))

        customer_info = gw_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']
        account_info = customer_info['account_info']
        balance_available_vnd = account_info['account_balance_available_vnd']
        return self.response(data=dict(
            fullname_vn=customer_info['full_name'],
            type=account_info['account_type'],
            type_name=account_info['account_type_name'],
            number=account_info['account_num'],
            currency=account_info['account_currency'],
            balance_available_vnd=balance_available_vnd if balance_available_vnd else None,
            report_casa_account=column_chart))

    async def ctr_gw_open_casa_account(self, request: GWOpenCasaAccountRequest, booking_id: str):
        current_user = self.current_user
        current_user_info = current_user.user_info
        is_role_supervisor = self.call_repos(await PermissionController.ctr_approval_check_permission_stage(
            auth_response=current_user,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_KSV,
            permission_code=IDM_PERMISSION_CODE_KSV,
            stage_code=CIF_STAGE_APPROVE_KSV
        ))
        if not is_role_supervisor:
            self.response_exception(
                loc=f"user: {current_user_info.code} - {current_user_info.username}",
                msg=ERROR_PERMISSION,
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        cif_number = request.cif_number
        # Kiểm tra số CIF có tồn tại trong CRM không
        self.call_repos(await repos_get_customer_by_cif_number(
            cif_number=cif_number,
            session=self.oracle_session
        ))

        # Kiểm tra Booking Account, Account lấy ra là những account chưa được phê duyệt
        casa_accounts = await CtrBooking().ctr_get_casa_account_from_booking(
            booking_id=booking_id, session=self.oracle_session
        )

        casa_account_ids = []
        booking = await CtrBooking().ctr_get_booking(booking_id=booking_id, business_type_code=BUSINESS_TYPE_OPEN_CASA)
        maker_staff_name = booking.created_by

        for casa_account in casa_accounts:
            if casa_account.approve_status == CASA_ACCOUNT_STATUS_UNAPPROVED:
                casa_account_ids.append(casa_account.id)

        # RULE: tài khoản đã được phê duyệt thì không cho phép phê duyệt
        self.call_repos(await repos_check_casa_account_approved(
            casa_account_ids=casa_account_ids,
            session=self.oracle_session
        ))

        casa_account_infos = self.call_repos(await repos_open_casa_get_casa_account_infos(
            casa_account_ids=casa_account_ids,
            session=self.oracle_session
        ))

        casa_account_successes = {}
        gw_errors = []
        for casa_account_info in casa_account_infos:
            self_selected_account_flag = casa_account_info.self_selected_account_flag

            casa_account_id = casa_account_info.id

            is_success, gw_open_casa_account_info = await repos_gw_open_casa_account(
                cif_number=cif_number,
                self_selected_account_flag=self_selected_account_flag,
                casa_account_info=casa_account_info,
                current_user=self.current_user,
                booking_parent_id=booking_id,
                session=self.oracle_session,
                maker_staff_name=maker_staff_name
            )
            if not is_success:
                gw_errors.append(dict(
                    id=casa_account_id,
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_open_casa_account_info['openCASA_out'])
                ))
            else:
                casa_account_successes.update({casa_account_id:
                                               gw_open_casa_account_info['openCASA_out']['data_output']['account_info']['account_num']})

        update_casa_accounts = []
        for casa_account_id, casa_account_number in casa_account_successes.items():
            update_casa_accounts.append(dict(
                id=casa_account_id,
                casa_account_number=casa_account_number,
                approve_status=1,
                checker_id=current_user_info.code,
                checker_at=now()
            ))

        self.call_repos(await repos_update_casa_account_to_approved(
            update_casa_accounts=update_casa_accounts,
            session=self.oracle_session
        ))

        return self.response(data=dict(
            successes=[dict(
                id=casa_account_id,
                number=casa_account_number
            ) for casa_account_id, casa_account_number in casa_account_successes.items()],
            errors=gw_errors
        ))

    async def ctr_gw_get_close_casa_account(self, booking_id):
        booking_business_form = self.call_repos(await repos_get_booking_business_form_by_booking_id(
            booking_id=booking_id,
            business_form_id=BUSINESS_FORM_CLOSE_CASA,
            session=self.oracle_session
        ))
        request_data = orjson_loads(booking_business_form.form_data)
        gw_close_casa_account = self.call_repos(await repos_gw_get_close_casa_account(
            current_user=self.current_user,
            booking_id=booking_id,
            request_data_gw=request_data,
            session=self.oracle_session
        ))
        response_data = {
            "booking_id": booking_id,
            "account_list": gw_close_casa_account
        }

        return self.response(data=response_data)

    async def ctr_gw_get_statement_casa_account_info(self, request: GWReportStatementHistoryAccountInfoRequest):
        gw_report_statements_casa_account_info = self.call_repos(await repos_gw_get_statements_casa_account_info(
            account_number=request.account_number,
            current_user=self.current_user.user_info,
            from_date=request.from_date,
            to_date=request.to_date
        ))
        report_casa_accounts = \
            gw_report_statements_casa_account_info['selectReportStatementCaSaFromAcc_out']['data_output'][
                'report_info']['report_casa_account']
        statements = []

        for report_casa_account in report_casa_accounts:
            code = report_casa_account['tran_ref_no']
            transaction_date = report_casa_account['tran_date']
            description = report_casa_account['tran_description']
            channel = report_casa_account['tran_channel']
            transaction_type = report_casa_account['tran_type']
            credit = report_casa_account['tran_credit']
            debit = report_casa_account['tran_debit']
            balance = report_casa_account['tran_balance']

            statements.append(dict(
                code=code if code else None,
                transaction_date=string_to_date(
                    transaction_date, _format=DATETIME_INPUT_OUTPUT_FORMAT
                ) if transaction_date else None,
                description=description if description else None,
                channel=channel if channel else None,
                transaction_type=transaction_type if transaction_type else None,
                credit=credit if credit else None,
                debit=debit if debit else None,
                balance=balance if balance else None
            ))

        return self.response(data=statements)

    async def ctr_gw_top_up_casa_account(self, booking_id: str):
        current_user = self.current_user
        booking_business_form = await CtrBooking(
            current_user=current_user
        ).ctr_get_booking_business_form(
            booking_id=booking_id, session=self.oracle_session
        )
        form_data = orjson_loads(booking_business_form.form_data)
        receiving_method = form_data['transfer_type']['receiving_method']
        response_data = None
        xref = None
        p_contract_ref = None

        maker = booking_business_form.booking.created_by

        is_completed = False

        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            is_success, response_data = await self.ctr_gw_pay_in_cash(
                form_data=form_data,
                maker=maker
            )
            if not is_success:
                return self.response_exception(
                    loc='pay_in_cash',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(response_data)
                )
            is_completed = True
            xref = response_data['payInCash_out']['data_output']['xref']['p_xref']

        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:

            is_success, tele_transfer_response_data = await self.ctr_tele_transfer(
                form_data=form_data,
                maker=maker
            )
            if not is_success:
                return self.response_exception(
                    loc='tele_transfer',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(tele_transfer_response_data)
                )
            p_instrument_number = tele_transfer_response_data[GW_FUNC_TELE_TRANSFER_OUT]['data_output']['p_instrument_number']

            if p_instrument_number == '':
                return self.response_exception(
                    loc='tele_transfer',
                    msg=ERROR_NO_INSTRUMENT_NUMBER,
                    detail=str(tele_transfer_response_data)
                )

            is_success, tt_liquidation_response_data = await self.ctr_tt_liquidation(
                maker=maker,
                p_instrument_number=p_instrument_number
            )
            if not is_success:
                return self.response_exception(
                    loc='tt_liquidation',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(tt_liquidation_response_data)
                )
            p_contract_ref = tt_liquidation_response_data[GW_FUNC_TT_LIQUIDATION_OUT]['data_output']['p_contract_ref']
            response_data = tt_liquidation_response_data
            is_completed = True

        if receiving_method in [RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT, RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY]:
            is_success, gw_response_data = await self.ctr_gw_interbank_transfer(
                form_data=form_data,
                maker=maker,
                receiving_method=receiving_method
            )
            if not is_success:
                return self.response_exception(
                    loc='interbank_transfer',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_response_data)
                )
            response_data = gw_response_data
            is_completed = True

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
            is_success, gw_response_data = await self.ctr_gw_pay_in_cash_247_by_acc_num(
                fcc_booking_code=booking_business_form.booking.fcc_booking_code,
                maker=maker,
                form_data=form_data
            )
            if not is_success:
                return self.response_exception(
                    loc='pay_in_cash_247_by_acc_num',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_response_data)
                )
            response_data = gw_response_data
            is_completed = True

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            is_success, gw_response_data = await self.ctr_gw_pay_in_cash_247_by_card_num(
                fcc_booking_code=booking_business_form.booking.fcc_booking_code,
                maker=maker,
                form_data=form_data
            )
            if not is_success:
                return self.response_exception(
                    loc='pay_in_cash_247_by_card_num',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_response_data)
                )
            response_data = gw_response_data
            is_completed = True

        if not response_data:
            return self.response_exception(msg="GW return None", loc=f'response_data: {response_data}')

        self.call_repos(await repos_save_gw_output_data(
            booking_id=booking_id,
            business_type_id=BUSINESS_TYPE_CASA_TOP_UP,
            gw_output_data=orjson_dumps(response_data),
            is_completed=is_completed,
            session=self.oracle_session
        ))

        return self.response(data=dict(
            booking_id=booking_id,
            xref=xref,
            p_contract_ref=p_contract_ref
        ))

    async def ctr_gw_get_tele_transfer(self, maker: str, request_data, place_of_issue):
        data_input = {
            "p_tt_type": "C",
            "p_details": {
                "TT_DETAILS": {
                    "TT_CURRENCY": "VND",  # TODO
                    "TT_AMOUNT": request_data.amount,
                    "TRANSACTION_CURRENCY": "VND"  # TODO
                },
                "BENEFICIARY_DETAILS": {
                    "BENEFICIARY_NAME": request_data.receiver_full_name_vn,
                    "BENEFICIARY_PHONE_NO": request_data.receiver_mobile_number,
                    "BENEFICIARY_ID_NO": request_data.receiver_identity_number,
                    "ID_ISSUE_DATE": date_to_string(request_data.receiver_issued_date),
                    "ID_ISSUER": place_of_issue.name,
                    "ADDRESS": request_data.receiver_address_full
                },
                "REMITTER_DETAILS": {
                    "REMITTER_NAME": request_data.sender_full_name_vn,
                    "REMITTER_PHONE_NO": request_data.sender_mobile_number,
                    "REMITTER_ID_NO": request_data.sender_identity_number,
                    "ID_ISSUE_DATE": date_to_string(request_data.sender_issued_date),
                    "ID_ISSUER": request_data.sender_place_of_issue.id,
                    "ADDRESS": request_data.sender_address_full
                },
                "ADDITIONAL_DETAILS": {
                    "NARRATIVE": "NARRATIVE"
                }
            },
            "p_denomination": "",
            "p_charges": [],
            "p_mis": "",
            "p_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": ""
                }
            ],
            "staff_info_checker": {
                "staff_name": self.current_user.user_info.username
            },
            "staff_info_maker": {
                "staff_name": maker
            }
        }
        tele_transfer = self.call_repos(await repos_gw_get_tele_transfer(
            current_user=self.current_user.user_info,
            data_input=data_input
        ))
        tele_transfer_info = tele_transfer[GW_FUNC_TELE_TRANSFER_OUT]['data_output']
        tele_transfer_info.update(
            data_input=data_input
        )
        return self.response(data=tele_transfer_info)

    async def ctr_gw_withdraw(self, booking_id: str):

        current_user = self.current_user
        current_user_info = current_user.user_info
        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=booking_id,
                business_form_id=BUSINESS_FORM_WITHDRAW,
                session=self.oracle_session

            ))

        maker = booking_business_form.booking.created_by
        request_data_gw = orjson_loads(booking_business_form.form_data)
        p_blk_udf = []
        p_blk_udf.append(dict(
            UDF_NAME='MUC_DICH_GIAO_DICH',
            UDF_VALUE='MUC_DICH_KHAC'
        ))

        data_input = {
            "account_info": {
                "account_num": request_data_gw['transaction_info']['source_accounts']['account_num'],
                "account_currency": 'VND',
                "account_withdrawals_amount": request_data_gw['transaction_info']['receiver_info']['amount']
            },
            "staff_info_checker": {
                "staff_name": current_user_info.username
            },
            "staff_info_maker": {
                "staff_name": maker
            },
            "p_blk_detail": "",
            "p_blk_mis": "",
            "p_blk_udf": p_blk_udf,
            "p_blk_charge": ""
        }

        _, gw_payment_amount_block = self.call_repos(await repos_gw_withdraw(
            current_user=current_user,
            booking_id=booking_id,
            request_data_gw=data_input,
            session=self.oracle_session
        ))
        if not gw_payment_amount_block:
            return self.response_exception(
                msg=ERROR_CALL_SERVICE_GW,
                loc=f'gw_payment_amount_block: {gw_payment_amount_block}'
            )

        response_data = {
            "booking_id": booking_id,
            "account": gw_payment_amount_block
        }

        response_data.update({
            'account_number': request_data_gw['transaction_info']['source_accounts']['account_num'],
            'account_withdrawals_amount': request_data_gw['transaction_info']['receiver_info']['amount']
        })

        return self.response(data=response_data)

    async def ctr_gw_get_retrieve_ben_name_by_account_number(self, account_number: str):
        current_user = self.current_user
        data_input = {
            "account_to_info": {
                "account_num": account_number
            },
            # TODO
            "account_from_info": {
                "account_num": "20625700001"
            },
            # TODO
            "ben_id": "970436",
            "trans_date": datetime_to_string(now()),
            "time_stamp": datetime_to_string(now()),
            "trans_id": "20220629160002159368",
            # TODO
            "staff_maker": {
                "staff_code": "annvh"
            },
            # TODO
            "staff_checker": {
                "staff_code": "THUYTP"
            },
            # TODO
            "branch_info": {
                "branch_code": "001",
                "branch_name": "CN CONG QUYNH"
            }
        }

        gw_ben_name = self.call_repos(await repos_gw_get_retrieve_ben_name_by_account_number(
            current_user=current_user.user_info, data_input=data_input))

        ben_name = gw_ben_name['retrieveBenNameByAccNum_out']['data_output']['customer_info']

        return self.response(data=ben_name)

    async def ctr_check_exist_account_number_from_other_bank(self, account_number) -> bool:
        account_info = await self.ctr_gw_get_retrieve_ben_name_by_account_number(account_number=account_number)
        return True if account_info['data']['full_name'] else False

    async def ctr_gw_get_retrieve_ben_name_by_card_number(self, card_number: str):
        current_user = self.current_user.user_info
        data_input = {
            "card_to_info": {
                "card_num": card_number
            },
            # TODO
            "account_from_info": {
                "account_num": "20625700001"
            },
            # TODO
            "ben_id": "970436",
            "trans_date": datetime_to_string(now()),
            "time_stamp": datetime_to_string(now()),
            "trans_id": "20220629160002159368",
            # TODO
            "staff_maker": {
                "staff_code": "annvh"
            },
            # TODO
            "staff_checker": {
                "staff_code": "THUYTP"
            },
            # TODO
            "branch_info": {
                "branch_code": "001",
                "branch_name": "CN CONG QUYNH"
            }
        }

        gw_ben_name = self.call_repos(await repos_gw_get_retrieve_ben_name_by_card_number(
            current_user=current_user, data_input=data_input))

        ben_name = gw_ben_name['retrieveBenNameByCardNum_out']['data_output']['customer_info']

        return self.response(data=ben_name)

    async def ctr_check_exist_card_number_from_other_bank(self, card_number) -> bool:
        card_info = await self.ctr_gw_get_retrieve_ben_name_by_card_number(card_number=card_number)
        return True if card_info['data']['full_name'] else False

    async def ctr_gw_change_status_account(self, account_number):
        current_user = self.current_user

        gw_change_status = self.call_repos(await repos_gw_change_status_account(
            current_user=current_user.user_info,
            account_number=account_number
        ))

        account_changes = gw_change_status.get('accountChangeStatus_out').get('transaction_info')

        if account_changes['transaction_error_code'] == "00":
            response_data = {
                "account": account_number,
                "transaction": {
                    "code": None,
                    "msg": account_changes.get('transaction_error_msg')
                }
            }
        else:
            response_data = {
                "account": account_number,
                "transaction": {
                    "code": account_changes.get('transaction_error_code'),
                    "msg": account_changes.get('transaction_error_msg')
                }
            }

        return self.response(data=response_data)

    ####################################################################################################################
    # Nộp tiền
    ####################################################################################################################
    async def ctr_gw_pay_in_cash(
            self,
            maker: str,
            form_data
    ):
        current_user = self.current_user
        sender = form_data['sender']
        receiver = form_data['receiver']
        fee_info = form_data['fee_info']
        identity_info = sender['identity_info']
        current_user_info = current_user.user_info

        sender_place_of_issue_id = identity_info['place_of_issue']['id']
        # sender_place_of_issue = await self.get_model_object_by_id(
        #     model_id=sender_place_of_issue_id,
        #     model=PlaceOfIssue,
        #     loc=f"sender_place_of_issue_id: {sender_place_of_issue_id}"
        # )

        data_input = {
            "account_info": {
                "account_num": receiver['account_number'],
                "account_currency": "VND",  # TODO: hiện tại chuyển tiền chỉ dùng tiền tệ VN
                "account_opening_amount": fee_info['actual_total']
            },
            "p_blk_denomination": "",
            "p_blk_charge": [
                {
                    "CHARGE_TYPE": "CASH",
                    "CHARGE_ACCOUNT": "",
                    "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                    "CHARGE_AMOUNT": 100000,
                    "WAIVED": "N"
                }
            ],
            "p_blk_project": "",
            "p_blk_mis": "",
            "p_blk_udf": [
                {
                    "UDF_NAME": "NGUOI_GIAO_DICH",
                    "UDF_VALUE": self.current_user.user_info.name
                },
                {
                    "UDF_NAME": "CMND_PASSPORT",
                    "UDF_VALUE": identity_info['number'] if identity_info['number'] else ''
                },
                {
                    "UDF_NAME": "NGAY_CAP",
                    "UDF_VALUE": identity_info['issued_date'] if identity_info['issued_date'] else ''
                },
                {
                    "UDF_NAME": "NOI_CAP",
                    "UDF_VALUE": sender_place_of_issue_id if sender_place_of_issue_id else ''  # TODO
                },
                {
                    "UDF_NAME": "DIA_CHI",
                    "UDF_VALUE": sender['address_full']
                },
                {
                    "UDF_NAME": "THU_PHI_DICH_VU",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "TEN_KHACH_HANG",
                    "UDF_VALUE": sender['fullname_vn']
                },
                {
                    "UDF_NAME": "TY_GIA_GD_DOI_UNG_HO",
                    "UDF_VALUE": "1"
                },
                {
                    "UDF_NAME": "MUC_DICH_GIAO_DICH",
                    "UDF_VALUE": "MUC_DICH_KHAC"
                },
                {
                    "UDF_NAME": "NGHIEP_VU_GDQT",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "NGAY_CHOT_TY_GIA",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "GIO_PHUT_CHOT_TY_GIA",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_1",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_2",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_3",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_4",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_5",
                    "UDF_VALUE": ""
                }
            ],
            "staff_info_checker": {
                "staff_name": current_user_info.username
            },
            "staff_info_maker": {
                "staff_name": maker
            }
        }

        gw_pay_in_cash = self.call_repos(await repos_gw_pay_in_cash(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_pay_in_cash

    async def ctr_tele_transfer(self, form_data, maker: str, pay_in_cash_flag: bool = True):
        current_user = self.current_user
        receiver = form_data['receiver']
        sender = form_data['sender']
        sender_identity_info = sender['identity_info']
        transfer = form_data['transfer']
        data_input = {
            "p_tt_type": "C" if pay_in_cash_flag else "A",
            "p_details": {
                "TT_DETAILS": {
                    "TT_CURRENCY": "VND",
                    "TT_AMOUNT": form_data['fee_info']['actual_total'],
                    "TRANSACTION_CURRENCY": "VND"
                },
                "BENEFICIARY_DETAILS": {
                    "BENEFICIARY_NAME": receiver['fullname_vn'] if 'fullname_vn' in receiver else GW_DEFAULT_VALUE,
                    "BENEFICIARY_PHONE_NO": receiver['mobile_number'] if 'mobile_number' in receiver else GW_DEFAULT_VALUE,
                    "BENEFICIARY_ID_NO": receiver['identity_number']
                    if 'identity_number' in receiver.keys() else GW_DEFAULT_VALUE,
                    "ID_ISSUE_DATE": receiver['issued_date'],
                    "ID_ISSUER": receiver['place_of_issue']['name'] if 'identity_number' in receiver else GW_DEFAULT_VALUE,
                    "ADDRESS": receiver['address_full'] if 'identity_number' in receiver else GW_DEFAULT_VALUE
                },
                "REMITTER_DETAILS": {
                    "REMITTER_NAME": sender['fullname_vn'],
                    "REMITTER_PHONE_NO": sender['mobile_phone'],
                    "REMITTER_ID_NO": sender_identity_info['number'],
                    "ID_ISSUE_DATE": sender_identity_info['issued_date'],
                    "ID_ISSUER": sender_identity_info['place_of_issue']['name'],
                    "ADDRESS": sender['address_full']
                },
                "ADDITIONAL_DETAILS": {
                    "NARRATIVE": transfer['content']
                }
            },
            "p_denomination": "",
            "p_charges": [
                {
                    "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                    "CHARGE_AMOUNT": 100000,
                    "WAIVED": "N"
                }
            ],
            "p_mis": "",
            "p_udf": "",
            "staff_info_checker": {
                "staff_name": self.current_user.user_info.username
            },
            "staff_info_maker": {
                "staff_name": maker
            }
        }
        if not pay_in_cash_flag:
            data_input["p_details"]["ACCOUNT_DETAILS"] = {
                "ACCOUNT_NUMBER": sender['account_number'],
                "CHARGE_BY_CASH": "N"
            }

        gw_tele_transfer = self.call_repos(await repos_gw_tele_transfer(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_tele_transfer

    async def ctr_tt_liquidation(self, p_instrument_number, maker: str):
        current_user = self.current_user
        data_input = {
            "account_info": {
                "account_num": "123456787912",
                "account_currency": "VND"
            },
            "branch_info": {
                "branch_code": current_user.user_info.hrm_branch_code
            },
            "p_liquidation_type": "C",
            "p_liquidation_details": "",
            "p_instrument_number": p_instrument_number,
            "p_instrument_status": "LIQD",
            "p_charges": [
                {
                    "CHARGE_NAME": "",
                    "CHARGE_AMOUNT": 0,
                    "WAIVED": "N"
                }
            ],
            "p_mis": "",
            "p_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": ""
                }
            ],
            "staff_info_checker": {
                "staff_name": self.current_user.user_info.username
            },
            "staff_info_maker": {
                "staff_name": maker
            }
        }
        gw_tt_liquidation = self.call_repos(await repos_gw_tt_liquidation(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_tt_liquidation

    async def ctr_gw_interbank_transfer(
            self,
            maker: str,
            form_data: dict,
            receiving_method: str
    ):
        current_user = self.current_user
        username = current_user.user_info.username

        sender = form_data['sender']
        receiver = form_data['receiver']
        transfer = form_data['transfer']
        identity_info = sender['identity_info']

        ben = await CtrConfigBank(current_user).ctr_get_bank_branch(bank_id=receiver['bank']['id'])

        fee_info = form_data['fee_info']
        details_of_charge = GW_DEFAULT_VALUE
        if fee_info:
            if fee_info['payer'] == PAYER_TRANSFER:
                details_of_charge = GW_ACCOUNT_CHARGE_ON_ORDERING
            if fee_info['payer'] == PAYER_RECEIVER:
                details_of_charge = GW_ACCOUNT_CHARGE_ON_RECEIVER

        data_input = {}
        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            data_input.update({
                "account_info": {
                    "account_bank_code": ben['data'][0]['id'],
                    "account_product_package": "NC01"
                },
                "staff_info_checker": {
                    "staff_name": username
                },
                "staff_info_maker": {
                    "staff_name": maker
                },
                "p_blk_mis": "",
                "p_blk_udf": "",
                "p_blk_refinance_rates": "",
                "p_blk_amendment_rate": "",
                "p_blk_main": {
                    "PRODUCT": {
                        "DETAILS_OF_CHARGE": details_of_charge,
                        "PAYMENT_FACILITY": "O"
                    },
                    "TRANSACTION_LEG": {
                        "ACCOUNT": "101101001",
                        "AMOUNT": fee_info['actual_total']
                    },
                    "RATE": {
                        "EXCHANGE_RATE": 0,
                        "LCY_EXCHANGE_RATE": 0,
                        "LCY_AMOUNT": 0
                    },
                    "ADDITIONAL_INFO": {
                        "RELATED_CUSTOMER": sender['cif_number'],
                        "NARRATIVE": fee_info['note']
                    }
                },
                "p_blk_charge": [
                    {
                        "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                        "CHARGE_AMOUNT": 10000,
                        "WAIVED": "N"
                    },
                    {
                        "CHARGE_NAME": "THUE VAT",
                        "CHARGE_AMOUNT": 0,
                        "WAIVED": "N"
                    }
                ],
                "p_blk_settlement_detail": {
                    "SETTLEMENTS": {
                        "TRANSFER_DETAIL": {
                            "BENEFICIARY_ACCOUNT_NUMBER": receiver['account_number'],
                            "BENEFICIARY_NAME": receiver['fullname_vn'],
                            "BENEFICIARY_ADRESS": receiver['address_full'],
                            "ID_NO": '',
                            "ISSUE_DATE": "",
                            "ISSUER": ""
                        },
                        "ORDERING_CUSTOMER": {
                            "ORDERING_ACC_NO": "",
                            "ORDERING_NAME": sender['fullname_vn'],
                            "ORDERING_ADDRESS": sender['address_full'],
                            "ID_NO": identity_info['number'],
                            "ISSUE_DATE": date_string_to_other_date_string_format(
                                identity_info['issued_date'], from_format=GW_CORE_DATE_FORMAT
                            ),
                            "ISSUER": identity_info['place_of_issue']
                        }
                    }
                }
            })

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            data_input.update({
                "account_info": {
                    "account_bank_code": ben['data'][0]['id'],
                    "account_product_package": "NC01"
                },
                "staff_info_checker": {
                    "staff_name": username
                },
                "staff_info_maker": {
                    "staff_name": maker
                },
                "p_blk_mis": "",
                "p_blk_udf": "",
                "p_blk_refinance_rates": "",
                "p_blk_amendment_rate": "",
                "p_blk_main": {
                    "PRODUCT": {
                        "DETAILS_OF_CHARGE": details_of_charge,
                        "PAYMENT_FACILITY": "O"
                    },
                    "TRANSACTION_LEG": {
                        "ACCOUNT": "101101001",
                        "AMOUNT": fee_info['actual_total']
                    },
                    "RATE": {
                        "EXCHANGE_RATE": 0,
                        "LCY_EXCHANGE_RATE": 0,
                        "LCY_AMOUNT": 0
                    },
                    "ADDITIONAL_INFO": {
                        "RELATED_CUSTOMER": sender['cif_number'],
                        "NARRATIVE": transfer['content']
                    }
                },
                "p_blk_charge": [
                    {
                        "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                        "CHARGE_AMOUNT": 10000,
                        "WAIVED": "N"
                    },
                    {
                        "CHARGE_NAME": "THUE VAT",
                        "CHARGE_AMOUNT": 0,
                        "WAIVED": "N"
                    }
                ],
                "p_blk_settlement_detail": {
                    "SETTLEMENTS": {
                        "TRANSFER_DETAIL": {
                            "BENEFICIARY_ACCOUNT_NUMBER": '.',  # TODO
                            "BENEFICIARY_NAME": receiver['fullname_vn'],
                            "BENEFICIARY_ADRESS": receiver['address_full'],
                            "ID_NO": receiver['identity_number'] if 'identity_number' in receiver else GW_DEFAULT_VALUE,
                            "ISSUE_DATE": date_string_to_other_date_string_format(
                                date_input=receiver['issued_date'],
                                from_format=GW_DATE_FORMAT,
                                to_format=GW_CORE_DATE_FORMAT
                            ) if 'issued_date' in receiver else GW_DEFAULT_VALUE,
                            "ISSUER": receiver['place_of_issue'] if 'place_of_issue' in receiver else GW_DEFAULT_VALUE
                        },
                        "ORDERING_CUSTOMER": {
                            "ORDERING_ACC_NO": "",
                            "ORDERING_NAME": sender['fullname_vn'],
                            "ORDERING_ADDRESS": sender['address_full'],
                            "ID_NO": sender['identity_number'] if 'identity_number' in sender else GW_DEFAULT_VALUE,
                            "ISSUE_DATE": sender['issued_date'] if 'issued_date' in sender else GW_DEFAULT_VALUE,
                            "ISSUER": sender['place_of_issue'] if 'place_of_issue' in sender else GW_DEFAULT_VALUE
                        }
                    }
                }
            })

        gw_interbank_transfer = self.call_repos(await repos_gw_interbank_transfer(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_interbank_transfer

    async def ctr_gw_pay_in_cash_247_by_acc_num(
            self,
            maker: str,
            fcc_booking_code: str,
            form_data: dict
    ):
        current_user = self.current_user
        current_user_info = current_user.user_info

        sender = form_data['sender']
        sender_identity = sender['identity_info']
        receiver = form_data['receiver']
        transfer = form_data['transfer']

        data_input = {
            "customer_info": {
                "full_name": sender['fullname_vn'],
                "birthday": sender_identity['issued_date']
            },
            "id_info": {
                "id_num": sender_identity['number']
            },
            "address_info": {
                "address_full": sender['address_full'] if 'address_full' in sender else GW_DEFAULT_VALUE
            },
            "trans_date": datetime_to_string(now()),
            "time_stamp": datetime_to_string(now()),
            "trans_id": fcc_booking_code,  # TODO hard code ffc_booking_code
            "amount": form_data['fee_info']['actual_total'],
            "description": transfer['content'],
            "account_to_info": {
                "account_num": receiver['account_number']
            },
            # "ben_id": ben['data'][0]['id'],
            "ben_id": '970436',  # TODO: hiện tại chỉ có mã ngân hàng này dùng được
            "account_from_info": {
                "account_num": GW_GL_BRANCH_CODE
            },
            "staff_maker": {
                "staff_code": maker
            },
            "staff_checker": {
                "staff_code": current_user_info.username
            },
            "branch_info": {
                "branch_code": current_user_info.hrm_branch_code
            }
        }
        gw_pay_in_cash_247_by_acc_num = self.call_repos(await repos_pay_in_cash_247_by_acc_num(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_pay_in_cash_247_by_acc_num

    async def ctr_gw_pay_in_cash_247_by_card_num(
            self,
            maker: str,
            fcc_booking_code: str,
            form_data: dict
    ):
        current_user = self.current_user
        current_user_info = current_user.user_info
        sender = form_data['sender']
        sender_identity = sender['identity_info']
        sender_identity_issued_date = sender_identity['issued_date']
        receiver = form_data['receiver']
        transfer = form_data['transfer']
        # ben = await CtrConfigBank(current_user).ctr_get_bank_branch(bank_id=receiver['bank']['id'])

        data_input = {
            "customer_info": {
                "full_name": sender['fullname_vn'],
                "birthday": sender_identity_issued_date if sender_identity_issued_date else GW_DEFAULT_VALUE
            },
            "id_info": {
                "id_num": sender_identity['number']
            },
            "address_info": {
                "address_full": sender['address_full']
            },
            "trans_date": datetime_to_string(now()),
            "time_stamp": datetime_to_string(now()),
            "trans_id": fcc_booking_code,  # TODO hard code ffc_booking_code
            "amount": form_data['fee_info']['actual_total'],
            "description": transfer['content'],
            "card_to_info": {
                "card_num": receiver['card_number']
            },
            # "ben_id": ben['data'][0]['id'],
            "ben_id": '970436',  # TODO: hiện tại chỉ có mã ngân hàng này dùng được
            "account_from_info": {
                "account_num": "101101001"
            },
            "staff_maker": {
                "staff_code": maker,
            },
            "staff_checker": {
                "staff_code": current_user_info.username
            },
            "branch_info": {
                "branch_code": current_user_info.hrm_branch_code
            }
        }
        gw_pay_in_cash_247_by_card_num = self.call_repos(await repos_pay_in_cash_247_by_card_num(
            data_input=data_input,
            current_user=current_user
        ))
        return gw_pay_in_cash_247_by_card_num

    async def ctr_gw_save_casa_transfer_info(self, BOOKING_ID: str):
        current_user = self.current_user
        current_user_info = current_user.user_info
        get_casa_transfer_info, booking = self.call_repos(await repos_get_casa_transfer_info(
            booking_id=BOOKING_ID,
            session=self.oracle_session
        ))
        maker = booking.created_by

        form_data = orjson_loads(get_casa_transfer_info.form_data)
        receiving_method = form_data['transfer_type']['receiving_method']

        fee_info = form_data['fee_info']

        sender = form_data['sender']
        receiver = form_data['receiver']

        transfer = form_data['transfer']

        request_data = {}

        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            request_data = {
                "data_input": {
                    "p_blk_detail": {
                        "FROM_ACCOUNT_DETAILS": {
                            "FROM_ACCOUNT_NUMBER": sender['account_number'],
                            "FROM_ACCOUNT_AMOUNT": fee_info['actual_total']
                        },
                        "TO_ACCOUNT_DETAILS": {
                            "TO_ACCOUNT_NUMBER": receiver['account_number']
                        }
                    },
                    "p_blk_charge": [],  # TODO thông tin phí
                    "p_blk_mis": "",
                    "p_blk_udf": [
                        {
                            "UDF_NAME": "",
                            "UDF_VALUE": ""
                        }
                    ],
                    "p_blk_project": "",
                    "staff_info_checker": {
                        "staff_name": current_user_info.username
                    },
                    "staff_info_maker": {
                        "staff_name": maker
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
            is_success, tele_transfer_response_data = await self.ctr_tele_transfer(
                form_data=form_data, maker=maker, pay_in_cash_flag=False
            )
            if not is_success:
                return self.response_exception(
                    loc='tele_transfer',
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(tele_transfer_response_data)
                )
            p_instrument_number = tele_transfer_response_data[GW_FUNC_TELE_TRANSFER_OUT]['data_output'][
                'p_instrument_number']

            if p_instrument_number == '':
                return self.response_exception(
                    loc='tele_transfer',
                    msg=ERROR_NO_INSTRUMENT_NUMBER,
                    detail=str(tele_transfer_response_data)
                )

            request_data = {
                "data_input": {
                    "p_liquidation_type": "A",
                    "p_liquidation_details": "",
                    "branch_info": {
                        "branch_code": current_user.user_info.hrm_branch_code
                    },
                    "p_instrument_number": p_instrument_number,
                    "p_instrument_status": "LIQD",
                    "account_info": {
                        "account_num": "123456787912",  # TODO
                        "account_currency": "VND"
                    },
                    "p_charges": [
                        {
                            "CHARGE_NAME": "",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_mis": "",
                    "p_udf": [
                        {
                            "UDF_NAME": "",
                            "UDF_VALUE": ""
                        }
                    ],
                    "staff_info_checker": {
                        "staff_name": current_user_info.username
                    },
                    "staff_info_maker": {
                        "staff_name": maker
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            details_of_charge = ''
            if fee_info:
                if fee_info['payer'] == PAYMENT_PAYERS[PAYER_TRANSFER]:
                    details_of_charge = GW_ACCOUNT_CHARGE_ON_ORDERING
                if fee_info['payer'] == PAYMENT_PAYERS[PAYER_RECEIVER]:
                    details_of_charge = GW_ACCOUNT_CHARGE_ON_RECEIVER

            identity_info = sender['identity_info']

            ben = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
                bank_id=receiver['bank']['id'])
            request_data = {
                "data_input": {
                    "account_info": {
                        "account_bank_code": ben['data'][0]['id'],
                        "account_product_package": "FT01"
                    },
                    "staff_info_checker": {
                        "staff_name": current_user_info.username
                    },
                    "staff_info_maker": {
                        "staff_name": maker
                    },
                    "p_blk_mis": "",
                    "p_blk_udf": "",
                    "p_blk_refinance_rates": "",
                    "p_blk_amendment_rate": "",
                    "p_blk_main": {
                        "PRODUCT": {
                            "DETAILS_OF_CHARGE": details_of_charge,
                            "PAYMENT_FACILITY": "O"
                        },
                        "TRANSACTION_LEG": {
                            "ACCOUNT": sender['account_number'],
                            "AMOUNT": fee_info['actual_total']
                        },
                        "RATE": {
                            "EXCHANGE_RATE": 0,
                            "LCY_EXCHANGE_RATE": 0,
                            "LCY_AMOUNT": 0
                        },
                        "ADDITIONAL_INFO": {
                            "RELATED_CUSTOMER": sender['cif_number'],
                            "NARRATIVE": transfer['content']
                        }
                    },
                    "p_blk_charge": [
                        {
                            "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        },
                        {
                            "CHARGE_NAME": "THUE VAT",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_blk_settlement_detail": {
                        "SETTLEMENTS": {
                            "TRANSFER_DETAIL": {
                                "BENEFICIARY_ACCOUNT_NUMBER": ".",
                                "BENEFICIARY_NAME": receiver['fullname_vn'],
                                "BENEFICIARY_ADRESS": receiver['address_full'],
                                "ID_NO": receiver['identity_number'],
                                "ISSUE_DATE": date_string_to_other_date_string_format(
                                    date_input=receiver['issued_date'],
                                    from_format=GW_DATE_FORMAT,
                                    to_format=GW_CORE_DATE_FORMAT
                                ),
                                "ISSUER": receiver['place_of_issue']['name']
                            },
                            "ORDERING_CUSTOMER": {
                                "ORDERING_ACC_NO": "",
                                "ORDERING_NAME": sender['fullname_vn'],
                                "ORDERING_ADDRESS": sender['address_full'],
                                "ID_NO": identity_info['number'],
                                "ISSUE_DATE": date_string_to_other_date_string_format(
                                    date_input=identity_info['issued_date'],
                                    from_format=GW_DATE_FORMAT,
                                    to_format=GW_CORE_DATE_FORMAT
                                ),
                                "ISSUER": identity_info['place_of_issue']['name']
                            }
                        }
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            bank_info = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
                bank_id=receiver['bank']['id'])

            request_data = {
                "data_input": {
                    "account_info": {
                        "account_bank_code": bank_info['data'][0]['code'],
                        "account_product_package": "FT01"
                    },
                    "staff_info_checker": {
                        "staff_name": current_user_info.username
                    },
                    "staff_info_maker": {
                        "staff_name": maker
                    },
                    "p_blk_mis": "",
                    "p_blk_udf": "",
                    "p_blk_refinance_rates": "",
                    "p_blk_amendment_rate": "",
                    "p_blk_main": {
                        "PRODUCT": {
                            "DETAILS_OF_CHARGE": "Y" if fee_info['payer'] == PAYMENT_PAYERS[PAYER_TRANSFER] else "O",
                            "PAYMENT_FACILITY": "O"
                        },
                        "TRANSACTION_LEG": {
                            "ACCOUNT": sender['account_number'],
                            "AMOUNT": fee_info['actual_total']
                        },
                        "RATE": {
                            "EXCHANGE_RATE": 0,
                            "LCY_EXCHANGE_RATE": 0,
                            "LCY_AMOUNT": 0
                        },
                        "ADDITIONAL_INFO": {
                            "RELATED_CUSTOMER": sender['cif_number'],
                            "NARRATIVE": transfer["content"]
                        }
                    },
                    "p_blk_charge": [
                        {
                            "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        },
                        {
                            "CHARGE_NAME": "THUE VAT",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_blk_settlement_detail": {
                        "SETTLEMENTS": {
                            "TRANSFER_DETAIL": {
                                "BENEFICIARY_ACCOUNT_NUMBER": receiver['account_number'],
                                "BENEFICIARY_NAME": receiver['fullname_vn'],
                                "BENEFICIARY_ADRESS": receiver['province']['name'],
                                "ID_NO": "",
                                "ISSUE_DATE": "",
                                "ISSUER": ""
                            },
                            "ORDERING_CUSTOMER": {
                                "ORDERING_ACC_NO": receiver['account_number'],
                                "ORDERING_NAME": receiver['fullname_vn'],
                                "ORDERING_ADDRESS": receiver['province']['name'],
                                "ID_NO": "",
                                "ISSUE_DATE": "",
                                "ISSUER": ""
                            }
                        }
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
            # ben = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
            #     bank_id=form_data['receiver_bank']['id'])

            request_data = {
                "data_input": {
                    # "ben_id": ben['data'][0]['id'],
                    "ben_id": "970436",  # TODO
                    "trans_date": datetime_to_string(now()),
                    "time_stamp": datetime_to_string(now()),
                    "trans_id": "20220629160002159368",
                    "amount": fee_info['actual_total'],
                    "description": transfer["content"],
                    "account_to_info": {
                        "account_num": receiver["account_number"]
                    },
                    "account_from_info": {
                        "account_num": sender["account_number"]
                    },
                    "customer_info": {
                        "full_name": sender["fullname_vn"]
                    },
                    "staff_maker": {
                        "staff_code": maker
                    },
                    "staff_checker": {
                        "staff_code": current_user_info.username
                    },
                    "branch_info": {
                        "branch_code": current_user_info.hrm_branch_code
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            # ben = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch(
            #     bank_id=form_data['receiver_bank']['id'])

            request_data = {
                "data_input": {
                    # "ben_id": ben['data'][0]['id'],
                    "ben_id": "970436",  # TODO hard core chưa thông tin ngân hàng khác
                    "trans_date": datetime_to_string(now()),
                    "time_stamp": datetime_to_string(now()),
                    "trans_id": "20220629160002159368",
                    "amount": fee_info['actual_total'],
                    "description": transfer["content"],
                    "account_from_info": {
                        "account_num": sender["account_number"]
                    },
                    "customer_info": {
                        "full_name": sender["fullname_vn"]
                    },
                    "staff_maker": {
                        "staff_code": maker
                    },
                    "staff_checker": {
                        "staff_code": current_user_info.username
                    },
                    "branch_info": {
                        "branch_code": current_user_info.hrm_branch_code
                    },
                    "card_to_info": {
                        "card_num": receiver["card_number"]
                    }
                }
            }
        response_data, gw_casa_transfer, is_completed = self.call_repos(await repos_gw_save_casa_transfer_info(
            current_user=self.current_user,
            receiving_method=receiving_method,
            booking_id=BOOKING_ID,
            request_data=request_data
        ))

        self.call_repos(await repos_save_gw_output_data(
            booking_id=BOOKING_ID,
            business_type_id=BUSINESS_TYPE_CASA_TRANSFER,
            is_completed=is_completed,
            gw_output_data=orjson_dumps(gw_casa_transfer),
            session=self.oracle_session
        ))

        return self.response(data=response_data)
    ####################################################################################################################

    async def get_sender_info(self, form_data):
        sender_cif_number = form_data['sender_cif_number']
        if sender_cif_number:
            gw_customer_info = await CtrGWCustomer(self.current_user).ctr_gw_get_customer_info_detail(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            gw_customer_info_id_info = gw_customer_info['id_info']
            sender_full_name_vn = gw_customer_info['full_name']
            sender_address_full = gw_customer_info['t_address_info']['contact_address_full']
            sender_identity_number = gw_customer_info_id_info['id_num']
            sender_issued_date = date_string_to_other_date_string_format(
                date_input=gw_customer_info_id_info['id_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_CORE_DATE_FORMAT
            )

            sender_place_of_issue = gw_customer_info_id_info['id_issued_location']
        else:
            sender_full_name_vn = form_data['sender_full_name_vn']
            sender_address_full = form_data['sender_address_full']
            sender_identity_number = form_data['sender_identity_number']
            sender_issued_date = form_data['sender_issued_date']
            sender_place_of_issue_id = form_data['sender_place_of_issue']['id']
            sender_place_of_issue = await self.get_model_object_by_id(
                model_id=sender_place_of_issue_id,
                model=PlaceOfIssue,
                loc='sender_place_of_issue_id'
            )
            sender_place_of_issue = sender_place_of_issue.name

        return (
            sender_cif_number, sender_full_name_vn, sender_address_full, sender_identity_number, sender_issued_date,
            sender_place_of_issue
        )
