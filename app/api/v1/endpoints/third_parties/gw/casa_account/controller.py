from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_get_casa_account_by_cif_number, repos_gw_get_casa_account_info
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
            balance = int(account['account_info_item']['account_balance'])
            total_balances += balance
            account_infos.append(account['account_info_item'])

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
            number=cif_info['cif_num'],
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
                branch_code=branch_info['branch_code'],
                branch_name=branch_info['branch_name']
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
