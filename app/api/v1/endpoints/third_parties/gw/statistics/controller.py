from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.statistics.repository import (
    repos_gw_select_data_for_chard_dashboard,
    repos_gw_select_statistic_banking_by_period,
    repos_gw_select_summary_card_by_date
)
from app.utils.constant.gw import (
    GW_DASHBOARD_CIF_OPEN_COUNT, GW_DASHBOARD_COMPANY_CUSTOMER_OPEN_COUNT,
    GW_DASHBOARD_COUNT_MORTGAGE_LOAN,
    GW_DASHBOARD_INDIVIDUAL_CUSTOMER_OPEN_COUNT, GW_DASHBOARD_INPUT_PARAMS,
    GW_DASHBOARD_TD_COUNT, GW_DASHBOARD_TKTT_COUNT_CLOSE,
    GW_DASHBOARD_TKTT_COUNT_OPEN, GW_DASHBOARD_TOTAL_TRN_REF_NO
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


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
            from_date=request.from_date,
            to_date=request.to_date,
            region_id=request.region_id,
            branch_code=request.branch_code,
            current_user=self.current_user.user_info
        ))
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_summary_card_by_date))
        data_output = gw_select_summary_card_by_date['selectSummaryCardsByDate_out']['data_output']

        return self.response(data=data_output)

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

        percent_cif_open_count = 0
        try:
            percent_cif_open_count = total_cif_open_count / total_trn_ref_no_count
        except ZeroDivisionError:
            pass

        percent_tktt_open_count = 0
        try:
            percent_tktt_open_count = total_tktt_open_count / total_trn_ref_no_count
        except ZeroDivisionError:
            pass

        percent_tktt_count_close_count = 0
        try:
            percent_tktt_count_close_count = total_tktt_count_close_count / total_trn_ref_no_count
        except ZeroDivisionError:
            pass

        percent_tktt_td_count = 0
        try:
            percent_tktt_td_count = total_tktt_td_count / total_trn_ref_no_count
        except ZeroDivisionError:
            pass

        percent_count_mortgage_loan_count = 0
        try:
            percent_count_mortgage_loan_count = total_count_mortgage_loan_count / total_trn_ref_no_count
        except ZeroDivisionError:
            pass

        percent_trn_ref_no_count = 0
        try:
            percent_trn_ref_no_count = total_trn_ref_no_count / total_trn_ref_no_count
        except ZeroDivisionError:
            pass

        percent_other = 0
        try:
            percent_other = total_other / total_trn_ref_no_count
        except ZeroDivisionError:
            pass

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
                trn_ref_no_count=percent_trn_ref_no_count,
                other=percent_other
            )
        )
        return self.response(data=response_data)
