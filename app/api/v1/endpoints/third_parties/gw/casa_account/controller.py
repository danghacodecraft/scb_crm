from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_get_casa_account_by_cif_number, repos_gw_get_casa_account_info,
    repos_gw_get_column_chart_casa_account_info,
    repos_gw_get_pie_chart_casa_account_info
)
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWReportPieChartHistoryAccountInfoRequest
)
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.utils.functions import string_to_date


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
            balance = int(account['account_info_item']['account_balance'])
            total_balances += balance
            branch_info = account['account_info_item']["branch_info"]
            account_infos.append(dict(
                number=account['account_info_item']["account_num"],
                type=account['account_info_item']["account_type"],
                type_name=account['account_info_item']["account_type_name"],
                currency=account['account_info_item']["account_currency"],
                balance=account['account_info_item']["account_balance"],
                balance_available=account['account_info_item']["account_balance_available"],
                balance_lock=account['account_info_item']["account_balance_lock"],
                over_draft_limit=account['account_info_item']["account_over_draft_limit"],
                over_draft_expired_date=account['account_info_item']["account_over_draft_expired_date"],
                latest_trans_date=account['account_info_item']["account_latest_trans_date"],
                open_date=account['account_info_item']["account_open_date"],
                maturity_date=account['account_info_item']["account_maturity_date"],
                lock_status=account['account_info_item']["account_lock_status"],
                class_name=account['account_info_item']["account_class_name"],
                class_code=account['account_info_item']["account_class_code"],
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
        gw_casa_account_info_response = dict(
            number=account_info['account_num'],
            type=account_info['account_type'],
            type_name=account_info['account_type_name'],
            currency=account_info['account_currency'],
            balance=account_info['account_balance'],
            balance_available=account_info['account_balance_available'],
            balance_lock=account_info['account_balance_lock'],
            over_draft_limit=account_info['account_over_draft_limit'],
            over_draft_expired_date=account_info['account_over_draft_expired_date'],
            latest_transaction_date=account_info['account_latest_trans_date'],
            open_date=account_info['account_open_date'],
            maturity_date=account_info['account_maturity_date'],
            status=account_info['account_status'],
            lock_status=account_info['account_lock_status'],
            class_name=account_info['account_class_name'],
            class_code=account_info['account_class_code'],
            saving_serials=account_info['account_saving_serials'],
            pre_open_date=account_info['account_pre_open_date'],
            service=account_info['account_service'],
            service_date=account_info['account_service_date'],
            company_salary=account_info['account_company_salary'],
            company_salary_num=account_info['account_company_salary_num'],
            service_escrow=account_info['account_service_escrow'],
            service_escrow_ex_date=account_info['account_service_escrow_ex_date'],
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
            current_user=self.current_user.user_info,
            # from_date=request.from_date,
            # to_date=request.to_date,
        ))
        report_casa_accounts = \
            gw_report_history_account_info['selectReportHisCaSaFromAcc_out']['data_output']['report_info'][
                'report_casa_account']

        pie_chart = []
        total = 0
        for report_casa_account in report_casa_accounts:
            pie_chart.append(dict(
                transaction_type=report_casa_account['tran_type'],
                transaction_date=string_to_date(report_casa_account['tran_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT),
                transaction_value=report_casa_account['tran_value']
            ))
            total += int(report_casa_account['tran_value'])

        percents = 0
        if total > 0:
            for index, pie in enumerate(pie_chart):
                if index != -1:
                    percent = float(int(pie['transaction_value']) * 100 / total)
                    percents += percent
                    pie.update(transaction_percent=percent)
                else:
                    pie.update(transaction_percent=100 - percents)

        return self.response(data=pie_chart)

    async def ctr_gw_get_column_chart_casa_account_info(self, request: GWReportPieChartHistoryAccountInfoRequest):
        gw_report_column_chart_casa_account_info = self.call_repos(await repos_gw_get_column_chart_casa_account_info(
            account_number=request.account_number,
            current_user=self.current_user.user_info,
            # from_date=request.from_date,
            # to_date=request.to_date,
        ))
        report_casa_accounts = \
            gw_report_column_chart_casa_account_info['selectReportHisCaSaFromAcc_out']['data_output']['report_info'][
                'report_casa_account']
        column_chart = []
        for report_casa_account in report_casa_accounts:
            column_chart.append(dict(
                transaction_type=report_casa_account['tran_type'],
                transaction_date=string_to_date(report_casa_account['tran_date'], _format=DATETIME_INPUT_OUTPUT_FORMAT),
                transaction_value=report_casa_account['tran_value']
            ))

        return self.response(data=column_chart)
