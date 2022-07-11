from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number
)
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_check_casa_account_approved, repos_gw_get_casa_account_by_cif_number,
    repos_gw_get_casa_account_info, repos_gw_get_close_casa_account,
    repos_gw_get_column_chart_casa_account_info,
    repos_gw_get_pie_chart_casa_account_info,
    repos_gw_get_statements_casa_account_info, repos_gw_get_tele_transfer,
    repos_gw_open_casa_account, repos_open_casa_get_casa_account_infos,
    repos_update_casa_account_to_approved
)
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWOpenCasaAccountRequest, GWReportColumnChartHistoryAccountInfoRequest,
    GWReportPieChartHistoryAccountInfoRequest,
    GWReportStatementHistoryAccountInfoRequest
)
from app.api.v1.endpoints.third_parties.gw.payment.controller import (
    CtrGWPayment
)
from app.api.v1.endpoints.third_parties.repository import (
    repos_save_gw_output_data
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.utils.constant.approval import CIF_STAGE_APPROVE_KSV
from app.utils.constant.business_type import BUSINESS_TYPE_CASA_TOP_UP
from app.utils.constant.casa import (
    CASA_ACCOUNT_STATUS_UNAPPROVED, RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD
)
from app.utils.constant.cif import BUSINESS_FORM_CLOSE_CASA
from app.utils.constant.gw import (
    GW_TRANSACTION_TYPE_SEND, GW_TRANSACTION_TYPE_WITHDRAW
)
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_KSV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_KSV
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW, ERROR_PERMISSION
from app.utils.functions import (
    date_to_string, now, orjson_dumps, orjson_loads, string_to_date
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
        account_info_list = account_info['selectCurrentAccountFromCIF_out']['data_output']['customer_info'][
            'account_info_list']
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
        gw_check_exist_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_number,
            current_user=self.current_user.user_info
        ))
        if not gw_check_exist_casa_account_info:
            return self.response(data=dict(is_existed=False))
        account_info = gw_check_exist_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info'][
            'account_info']

        return self.response(data=dict(
            is_existed=True if account_info['account_num'] else False
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
                session=self.oracle_session
            )
            if not is_success:
                gw_errors.append(dict(
                    id=casa_account_id,
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_open_casa_account_info['openCASA_out'])
                ))
            else:
                casa_account_successes.update({casa_account_id: gw_open_casa_account_info['openCASA_out']['data_output']['account_info']['account_num']})

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
            )for casa_account_id, casa_account_number in casa_account_successes.items()],
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
            gw_report_statements_casa_account_info['selectReportStatementCaSaFromAcc_out']['data_output']['report_info']['report_casa_account']
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
        receiving_method = form_data['receiving_method']
        response_data = None
        xref = None

        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            is_success, response_data = await CtrGWPayment(current_user).ctr_gw_pay_in_cash(form_data=form_data)
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(response_data)
                )
            xref = response_data['data']['payInCash_out']['data_output']['xref']['p_xref']

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
            is_success, response_data = await CtrGWPayment(current_user).ctr_gw_pay_in_cash_247_by_acc_num(
                booking_id=booking_id,
                form_data=form_data
            )
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(response_data)
                )

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            is_success, gw_response_data = await CtrGWPayment(current_user).ctr_gw_pay_in_cash_247_by_card_num(
                booking_id=booking_id,
                form_data=form_data
            )
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_response_data)
                )
            response_data = gw_response_data

        if not response_data:
            return self.response_exception(msg="GW return None", loc=f'response_data: {response_data}')

        self.call_repos(await repos_save_gw_output_data(
            booking_id=booking_id,
            business_type_id=BUSINESS_TYPE_CASA_TOP_UP,
            gw_output_data=orjson_dumps(response_data),
            session=self.oracle_session
        ))

        return self.response(data=dict(
            booking_id=booking_id,
            xref=xref
        ))

    async def ctr_gw_get_tele_transfer(self, request_data, place_of_issue):
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
                "staff_name": "HOANT2"  # TODO
            },
            "staff_info_maker": {
                "staff_name": "KHANHLQ"  # TODO
            }
        }
        tele_transfer = self.call_repos(await repos_gw_get_tele_transfer(
            current_user=self.current_user.user_info,
            data_input=data_input
        ))
        tele_transfer_info = tele_transfer['teleTransfer_out']['data_output']
        tele_transfer_info.update(
            data_input=data_input
        )
        return self.response(data=tele_transfer_info)
