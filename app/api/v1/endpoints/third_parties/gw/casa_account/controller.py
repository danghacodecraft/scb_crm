from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_get_casa_account_by_cif_number, repos_gw_get_casa_account_info,
    repos_gw_get_column_chart_casa_account_info,
    repos_gw_get_pie_chart_casa_account_info,
    repos_gw_get_statements_casa_account_info
)
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWReportColumnChartHistoryAccountInfoRequest,
    GWReportPieChartHistoryAccountInfoRequest,
    GWReportStatementHistoryAccountInfoRequest
)
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.utils.constant.gw import (
    GW_TRANSACTION_TYPE_SEND, GW_TRANSACTION_TYPE_WITHDRAW
)
from app.utils.functions import orjson_loads, string_to_date


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
            account_number: str
    ):
        gw_casa_account_info = self.call_repos(await repos_gw_get_casa_account_info(
            account_number=account_number,
            current_user=self.current_user.user_info
        ))

        customer_info = gw_casa_account_info['retrieveCurrentAccountCASA_out']['data_output']['customer_info']
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
        branch_info = account_info['branch_info']
        status_info = []
        if account_info['account_status']:
            list_account_status = orjson_loads(account_info['account_status'])[0]
            for key, value in list_account_status.items():
                status_info.append(dict(
                    id=key,
                    code=key,
                    name=value
                ))
        gw_casa_account_info_response = dict(
            number=account_info['account_num'],
            type=account_info['account_type'],
            type_name=account_info['account_type_name'],
            currency=account_info['account_currency'],
            balance=account_info['account_balance'],
            balance_available=account_info['account_balance_available'],
            balance_available_vnd=account_info['account_balance_available_vnd'],
            balance_lock=account_info['account_balance_lock'],
            over_draft_limit=account_info['account_over_draft_limit'],
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
            service_escrow_ex_date=string_to_date(account_info['account_service_escrow_ex_date'],
                                                  _format=DATETIME_INPUT_OUTPUT_FORMAT),
            product_package=account_info["account_product_package"],
            branch_info=dict(
                code=branch_info['branch_code'],
                name=branch_info['branch_name']
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
