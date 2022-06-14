from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.deposit_account.repository import (
    ctr_gw_get_statement_deposit_account_td, repos_gw_deposit_open_account_td,
    repos_gw_get_column_chart_deposit_account_info,
    repos_gw_get_deposit_account_by_cif_number, repos_gw_get_deposit_account_td
)
from app.api.v1.endpoints.third_parties.gw.deposit_account.schema import (
    GWColumnChartDepositAccountRequest, GWDepositOpenAccountTD,
    GWReportStatementHistoryTDAccountInfoRequest
)
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.utils.functions import string_to_date


class CtrGWDepositAccount(BaseController):
    async def ctr_gw_get_deposit_account_by_cif_number(
            self,
            cif_number: str
    ):
        current_user = self.current_user
        account_info = self.call_repos(await repos_gw_get_deposit_account_by_cif_number(
            cif_number=cif_number, current_user=current_user))
        response_data = {}
        total_balances = 0
        account_info_list = account_info['selectDepositAccountFromCIF_out']['data_output']['customer_info'][
            'account_info_list']
        account_infos = []
        for account in account_info_list:
            account_info_item = account['account_info_item']
            balance = int(account_info_item['account_balance'])
            total_balances += balance

            account_infos.append(dict(
                number=account_info_item["account_num"],
                term=account_info_item["account_term"],
                type=account_info_item["account_type"],
                type_name=account_info_item["account_type_name"],
                currency=account_info_item["account_currency"],
                balance=account_info_item["account_balance"],
                balance_available=account_info_item["account_balance_available"],
                balance_available_vnd=account_info_item["account_balance_available_vnd"],
                balance_lock=account_info_item["account_balance_lock"],
                open_date=string_to_date(account_info_item["account_open_date"], _format=DATETIME_INPUT_OUTPUT_FORMAT),
                maturity_date=string_to_date(account_info_item["account_maturity_date"],
                                             _format=DATETIME_INPUT_OUTPUT_FORMAT),
                saving_serials=account_info_item["account_saving_serials"],
                class_name=account_info_item["account_class_name"],
                class_code=account_info_item["account_class_code"],
                interest_rate=account_info_item["account_interest_rate"],
                lock_status=account_info_item["account_lock_status"],
                branch_info=dict(
                    code=account_info_item["branch_info"]["branch_code"],
                    name=account_info_item["branch_info"]["branch_name"]
                ),
                payin_account=dict(number=account_info_item['payin_acc']['payin_account']),
                payout_account=dict(number=account_info_item['payout_acc']['payout_account'])
            ))

        response_data.update(dict(
            total_balances=total_balances,
            total_items=len(account_infos),
            account_info_list=account_infos
        ))

        return self.response(data=response_data)

    async def ctr_gw_get_deposit_account_td(
            self,
            account_number: str
    ):
        current_user = self.current_user
        response_data = {}
        deposit_account_td = self.call_repos(await repos_gw_get_deposit_account_td(
            account_number=account_number, current_user=current_user))

        customer_info = deposit_account_td['retrieveDepositAccountTD_out']['data_output']['customer_info']

        account_info = customer_info['account_info']

        cif_info = customer_info['cif_info']

        gw_deposit_cif_info_response = dict(
            cif_number=cif_info["cif_num"],
            issued_date=cif_info["cif_issued_date"]
        )

        branch_info = account_info["branch_info"]
        payin_account = account_info["payin_acc"]
        payout_account = account_info["payout_acc"]
        staff_info_direct = account_info["staff_info_direct"]
        staff_info_indirect = account_info["staff_info_indirect"]
        gw_deposit_account_info_response = ({
            "number": account_info["account_num"],
            "term": account_info["account_term"],
            "type": account_info["account_type"],
            "type_name": account_info["account_type_name"],
            "saving_serials": account_info["account_saving_serials"],
            "currency": account_info["account_currency"],
            "balance": account_info["account_balance"],
            "balance_available": account_info["account_balance_available"],
            "balance_available_vnd": account_info["account_balance_available_vnd"],
            "balance_lock": account_info["account_balance_lock"],
            "interest_receivable_type": account_info["account_interest_receivable_type"],
            "open_date": string_to_date(account_info["account_open_date"], _format=DATETIME_INPUT_OUTPUT_FORMAT),
            "maturity_date": string_to_date(account_info["account_maturity_date"],
                                            _format=DATETIME_INPUT_OUTPUT_FORMAT),
            "lock_status": account_info["account_lock_status"],
            "class_name": account_info["account_class_name"],
            "class_code": account_info["account_class_code"],
            "interest_rate": account_info["account_interest_rate"],
            "branch_info": dict(
                code=branch_info["branch_code"],
                name=branch_info["branch_name"]
            ),
            "payin_account": dict(
                number=payin_account["payin_account"]
            ),
            "payout_account": dict(
                number=payout_account["payout_account"]
            ),
            "staff_info_direct": dict(
                code=staff_info_direct["staff_code"],
                name=staff_info_direct["staff_name"]
            ),
            "staff_info_indirect": dict(
                code=staff_info_indirect["staff_code"],
                name=staff_info_indirect["staff_name"]
            )
        })

        gw_deposit_customer_info_response = dict(
            fullname_vn=customer_info["full_name"],
            date_of_birth=customer_info["birthday"],
            gender=customer_info["gender"],
            email=customer_info["email"],
            mobile_phone=customer_info["mobile_phone"],
            type=customer_info["customer_type"]
        )

        response_data.update(
            account_info=gw_deposit_account_info_response,
            customer_info=gw_deposit_customer_info_response,
            cif_info=gw_deposit_cif_info_response
        )

        return self.response(data=response_data)

    async def ctr_gw_get_statement_deposit_account_td(self, request: GWReportStatementHistoryTDAccountInfoRequest):
        gw_report_statements_casa_td_account_info = self.call_repos(await ctr_gw_get_statement_deposit_account_td(
            account_number=request.account_number,
            current_user=self.current_user.user_info,
            from_date=request.from_date,
            to_date=request.to_date
        ))
        report_td_accounts = \
            gw_report_statements_casa_td_account_info['selectReportStatementTDFromAcc_out']['data_output']['report_info']['report_td_account']

        statements = []

        for report_td_account in report_td_accounts:
            code = report_td_account['tran_ref_no']
            transaction_date = report_td_account['tran_date']
            description = report_td_account['tran_description']
            amount = report_td_account['tran_amount']
            rate = report_td_account['tran_rate']
            balance = report_td_account['tran_balance']
            expire_date = report_td_account['tran_expire_date']

            statements.append(dict(
                code=code if code else None,
                transaction_date=string_to_date(
                    transaction_date, _format=DATETIME_INPUT_OUTPUT_FORMAT
                ),
                description=description,
                amount=amount,
                rate=rate,
                balance=balance,
                expire_date=string_to_date(
                    expire_date, _format=DATETIME_INPUT_OUTPUT_FORMAT
                )
            ))

        return self.response(data=statements)

    async def ctr_gw_get_column_chart_deposit_account_info(
        self,
        request: GWColumnChartDepositAccountRequest
    ):
        current_user = self.current_user

        account_number = request.account_number
        from_date = request.from_date
        to_date = request.to_date

        gw_column_chart_deposit_account_infos = self.call_repos(await repos_gw_get_column_chart_deposit_account_info(
            account_number=account_number, current_user=current_user, from_date=from_date, to_date=to_date
        ))
        data_output = gw_column_chart_deposit_account_infos['selectReportTDFromCif_out']['data_output']
        report_td_accounts = data_output['report_info']['report_td_account']
        columns = []
        for column in report_td_accounts:
            columns.append(dict(
                year=column['tran_year'],
                month=column['tran_month'],
                value=column['tran_value']
            ))

        return self.response(data=columns)

    async def ctr_gw_deposit_open_account_td(
            self,
            request: GWDepositOpenAccountTD
    ):
        current_user = self.current_user
        # TODO hard core data_input open_account_td
        data_input = {
            "customer_info": {
                "cif_info": {
                    "cif_num": request.cif_number
                },
                "account_info": {
                    "account_currency": "VND",
                    "account_class_code": "CAI025",
                    "account_saving_serials": "",
                    "p_blk_cust_account": [
                        {
                            "ACCOUNT_TYPE": "S",
                            "MODE_OF_OPERATION": "S"
                        }
                    ],
                    "p_blk_provision_main": "",
                    "p_blk_provdetails": "",
                    "p_blk_report_gentime1": "",
                    "p_blk_accmaintinstr": "",
                    "p_blk_report_gentime2": "",
                    "p_blk_multi_account_generation": "",
                    "p_blk_account_generation": "",
                    "p_blk_interim_details": "",
                    "p_blk_accprdres": "",
                    "p_blk_acctxnres": "",
                    "p_blk_authbicdetails": "",
                    "p_blk_acstatuslines": "",
                    "p_blk_jointholders": [
                        {
                            "JOINT_HOLDER_CODE": "",
                            "JOINT_HOLDER": "",
                            "START_DATE": "",
                            "END_DATE": ""
                        }
                    ],
                    "p_blk_acccrdrlmts": "",
                    "p_blk_intdetails": "",
                    "p_blk_intprodmap": "",
                    "p_blk_inteffdtmap": "",
                    "p_blk_intsde": "",
                    "p_blk_tddetails": "",
                    "p_blk_amount_dates": "",
                    "p_blk_turnovers": "",
                    "p_blk_noticepref": "",
                    "p_blk_acc_nominees": "",
                    "p_blk_dcdmaster": "",
                    "p_blk_tdpayindetails": [
                        {
                            "TD_AMOUNT": "100000000",
                            "ROLLOVER_TYPE": "I"
                        }
                    ],
                    "p_blk_tdpayoutdetails": [
                        {
                            "PAYOUT_TYPE": "",
                            "PAYOUT_BRN": "",
                            "PAYOUT_ACC": ""
                        }
                    ],
                    "p_blk_tod_renew": "",
                    "p_blk_od_limit": "",
                    "p_blk_doctype_checklist": "",
                    "p_blk_doctype_remarks": "",
                    "p_blk_sttms_od_coll_linkages": "",
                    "p_blk_cust_acc_check": "",
                    "p_blk_cust_acc_card": "",
                    "p_blk_intermediary": "",
                    "p_blk_summary": "",
                    "p_blk_interest_payout": "",
                    "p_blk_addpayin_dtls": "",
                    "p_blk_accls_rollover": "",
                    "p_blk_promotions": "",
                    "p_blk_link_pricing": "",
                    "p_blk_linkedentities": [
                        {
                            "CUSTOMER": "",
                            "RELATIONSHIP": "",
                            "INCLUDE_RELATIONSHIP": ""
                        }
                    ],
                    "p_blk_custacc_icccspcn": "",
                    "p_blk_custacc_icchspcn": "",
                    "p_blk_custacc_iccinstr": "",
                    "p_blk_custaccdet": "",
                    "p_blk_custacc_sicdiary": "",
                    "p_blk_custacc_stccusbl": "",
                    "p_blk_accclose": "",
                    "p_blk_acc_svcacsig": "",
                    "p_blk_sttms_debit": "",
                    "p_blk_tddetailsprn": "",
                    "p_blk_extsys_ws_master": "",
                    "p_blk_custacc_iccintpo": "",
                    "p_blk_sttms_cust_account": "",
                    "p_blk_customer_acc": "",
                    "p_blk_customer_accis": "",
                    "p_blk_master": "",
                    "p_blk_sttms_cust_acc_swp": "",
                    "p_blk_acc_chnl": "",
                    "p_blk_acc": ""
                },
                "staff_info_checker": {
                    "staff_name": "HOANT2"
                },
                "staff_info_maker": {
                    "staff_name": "KHANHLQ"
                },
                "udf_info": {
                    "udf_json_array": [
                        {
                            "UDF_NAME": "01_MANV_KINH_DOANH",
                            "UDF_VALUE": "00563"
                        }
                    ]
                }
            }
        }
        gw_deposit_open_account_td = self.call_repos(await repos_gw_deposit_open_account_td(
            current_user=current_user,
            data_input=data_input
        ))
        return self.response(data=gw_deposit_open_account_td)
