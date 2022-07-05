from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.bank import Bank, BankBranch


class CtrConfigBank(BaseController):
    async def ctr_get_bank_branch(self):
        bank_branch_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=BankBranch
            )
        )
        return self.response(bank_branch_info)

    async def ctr_get_bank(self, napas_flag: bool, citad_flag: bool):
        bank_branch_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Bank,
                napas_flag=napas_flag,
                citad_flag=citad_flag
            )
        )
        return self.response(bank_branch_info)
