from datetime import date

from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.statistics.repository import (
    repos_gw_select_data_for_chard_dashboard,
    repos_gw_select_statistic_banking_by_period,
    repos_gw_select_summary_card_by_date
)
from app.utils.constant.date_datetime import START_DATE_OF_YEAR
from app.utils.constant.gw import (
    GW_DASHBOARD_CIF_OPEN_COUNT, GW_DASHBOARD_COMPANY_CUSTOMER_OPEN_COUNT,
    GW_DASHBOARD_COUNT_MORTGAGE_LOAN,
    GW_DASHBOARD_INDIVIDUAL_CUSTOMER_OPEN_COUNT, GW_DASHBOARD_INPUT_PARAMS,
    GW_DASHBOARD_TD_COUNT, GW_DASHBOARD_TKTT_COUNT_CLOSE,
    GW_DASHBOARD_TKTT_COUNT_OPEN, GW_DASHBOARD_TOTAL_TRN_REF_NO
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW
from app.utils.functions import (
    calculate_percentage, first_day_in_year, yesterday
)


class CtrGWStatistic(BaseController):
    async def ctr_gw_select_statistic_banking_by_period(self, request):
        is_success, gw_select_statistic_banking_by_period = self.call_repos(
            await repos_gw_select_statistic_banking_by_period(
                from_date=request.from_date,
                to_date=request.to_date,
                current_user=self.current_user.user_info
            )
        )
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_statistic_banking_by_period))
        return self.response(
            data=gw_select_statistic_banking_by_period['selectStatisticBankingByPeriod_out']['data_output'])

    async def ctr_gw_select_summary_card_by_date(self, request):
        is_success, gw_select_summary_card_by_date = self.call_repos(await repos_gw_select_summary_card_by_date(
            from_date=first_day_in_year(),
            to_date=yesterday() if date.today() != START_DATE_OF_YEAR else START_DATE_OF_YEAR,
            region_id=request.region_id,
            branch_code=request.branch_code,
            current_user=self.current_user.user_info
        ))
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_summary_card_by_date))
        data_output = gw_select_summary_card_by_date['selectSummaryCardsByDate_out']['data_output']

        # Thông tin thẻ TTQT
        debit_open_criterion_amt_week = 0
        debit_open_criterion_amt_month = 0
        debit_open_criterion_accumulated = 0
        for item in data_output['total_debit_card_open_list']:
            item = item['total_debit_card_open_item']
            debit_open_criterion_amt_week += int(item['criterion_amt_week'])
            debit_open_criterion_amt_month += int(item['criterion_amt_month'])
            debit_open_criterion_accumulated += int(item['criterion_amt_day'])

        debit_sales_criterion_amt_week = 0
        debit_sales_criterion_amt_month = 0
        debit_sales_criterion_accumulated = 0
        for item in data_output['total_sales_debit_card_list']:
            item = item['total_sales_debit_card_item']
            debit_sales_criterion_amt_week += int(item['criterion_amt_week'])
            debit_sales_criterion_amt_month += int(item['criterion_amt_month'])
            debit_sales_criterion_accumulated += int(item['criterion_amt_day'])

        # Thông tin thẻ TDQT
        credit_open_criterion_amt_week = 0
        credit_open_criterion_amt_month = 0
        credit_open_criterion_accumulated = 0
        for item in data_output['total_credit_card_open_list']:
            item = item['total_credit_card_open_item']
            credit_open_criterion_amt_week += int(item['criterion_amt_week'])
            credit_open_criterion_amt_month += int(item['criterion_amt_month'])
            credit_open_criterion_accumulated += int(item['criterion_amt_day'])

        credit_sales_criterion_amt_week = 0
        credit_sales_criterion_amt_month = 0
        credit_sales_criterion_accumulated = 0
        for item in data_output['total_sales_credit_card_list']:
            item = item['total_sales_credit_card_item']
            credit_sales_criterion_amt_week += int(item['criterion_amt_week'])
            credit_sales_criterion_amt_month += int(item['criterion_amt_month'])
            credit_sales_criterion_accumulated += int(item['criterion_amt_day'])

        return self.response(data=dict(
            international_debit_card=dict(
                open=dict(
                    criterion_amt_week=debit_open_criterion_amt_week,
                    criterion_amt_month=debit_open_criterion_amt_month,
                    accumulated=debit_open_criterion_accumulated
                ),
                sales=dict(
                    criterion_amt_week=debit_sales_criterion_amt_week,
                    criterion_amt_month=debit_sales_criterion_amt_month,
                    accumulated=debit_sales_criterion_accumulated
                )
            ),
            international_credit_card=dict(
                open=dict(
                    criterion_amt_week=credit_open_criterion_amt_week,
                    criterion_amt_month=credit_open_criterion_amt_month,
                    accumulated=credit_open_criterion_accumulated
                ),
                sales=dict(
                    criterion_amt_week=credit_sales_criterion_amt_week,
                    criterion_amt_month=credit_sales_criterion_amt_month,
                    accumulated=credit_sales_criterion_accumulated
                )
            )
        ))

    async def ctr_gw_select_data_for_chard_dashboard(self, request):
        total_company_customer_open_count = 0
        total_individual_customer_open_count = 0
        total_cif_open_count = 0
        total_tktt_open_count = 0
        total_tktt_count_close_count = 0
        total_tktt_td_count = 0
        total_count_mortgage_loan_count = 0
        total_trn_ref_no_count = 0

        for search_name in GW_DASHBOARD_INPUT_PARAMS.keys():
            is_success, gw_select_data_for_chard_dashboard = self.call_repos(
                await repos_gw_select_data_for_chard_dashboard(
                    from_date=request.from_date,
                    to_date=request.to_date,
                    search_name=search_name,
                    current_user=self.current_user.user_info,
                    region_id=request.region_id,
                    branch_code=request.branch_code
                ))

            if not is_success:
                return self.response_exception(
                    loc=search_name,
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_select_data_for_chard_dashboard)
                )

            gw_select_data_for_chard_dashboard_data_output = \
                gw_select_data_for_chard_dashboard['selectDataForChartDashBoard_out']['data_output']

            if search_name == GW_DASHBOARD_COMPANY_CUSTOMER_OPEN_COUNT:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_company_customer_open_count += int(count_data['total_count_data_item']['total_count'])

            if search_name == GW_DASHBOARD_INDIVIDUAL_CUSTOMER_OPEN_COUNT:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_individual_customer_open_count += int(count_data['total_count_data_item']['total_count'])

            if search_name == GW_DASHBOARD_CIF_OPEN_COUNT:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_cif_open_count += int(count_data['total_count_data_item']['total_count'])

            if search_name == GW_DASHBOARD_TKTT_COUNT_OPEN:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_tktt_open_count += int(count_data['total_count_data_item']['total_count'])

            if search_name == GW_DASHBOARD_TKTT_COUNT_CLOSE:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_tktt_count_close_count += int(count_data['total_count_data_item']['total_count'])

            if search_name == GW_DASHBOARD_TD_COUNT:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_tktt_td_count += int(count_data['total_count_data_item']['total_count'])

            if search_name == GW_DASHBOARD_COUNT_MORTGAGE_LOAN:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_count_mortgage_loan_count += int(count_data['total_count_data_item']['total_count'])

            if search_name == GW_DASHBOARD_TOTAL_TRN_REF_NO:
                for count_data in gw_select_data_for_chard_dashboard_data_output['total_count_data_list']:
                    total_trn_ref_no_count += int(count_data['total_count_data_item']['total_count'])

        total_other = total_trn_ref_no_count - (
            total_cif_open_count
            + total_tktt_open_count
            + total_tktt_count_close_count
            + total_tktt_td_count
            + total_count_mortgage_loan_count
        )

        percent_cif_open_count = calculate_percentage(total_cif_open_count, total_trn_ref_no_count)

        percent_tktt_open_count = calculate_percentage(total_tktt_open_count, total_trn_ref_no_count)

        percent_tktt_count_close_count = calculate_percentage(total_tktt_count_close_count, total_trn_ref_no_count)

        percent_tktt_td_count = calculate_percentage(total_tktt_td_count, total_trn_ref_no_count)

        percent_count_mortgage_loan_count = calculate_percentage(total_count_mortgage_loan_count, total_trn_ref_no_count)

        percent_other = 100 - (percent_cif_open_count
                               + percent_tktt_open_count
                               + percent_tktt_count_close_count
                               + percent_tktt_td_count
                               + percent_count_mortgage_loan_count)

        response_data = dict(
            total=dict(
                company_customer_open_count=total_company_customer_open_count,
                individual_customer_open_count=total_individual_customer_open_count,
                cif_open_count=total_cif_open_count,
                tktt_open_count=total_tktt_open_count,
                tktt_count_close_count=total_tktt_count_close_count,
                tktt_td_count=total_tktt_td_count,
                count_mortgage_loan_count=total_count_mortgage_loan_count,
                total_trn_ref_no_count=total_trn_ref_no_count,
                other=total_other
            ),
            percent=dict(
                cif_open_count=percent_cif_open_count,
                tktt_open_count=percent_tktt_open_count,
                tktt_count_close_count=percent_tktt_count_close_count,
                tktt_td_count=percent_tktt_td_count,
                count_mortgage_loan_count=percent_count_mortgage_loan_count,
                other=percent_other
            )
        )
        return self.response(data=response_data)
