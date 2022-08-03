from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.account.repository import (
    repos_get_account_class
)
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.account import AccountType
from app.utils.functions import dropdown


class CtrConfigAccount(BaseController):
    async def ctr_account_type_info(self):
        account_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=AccountType
            )
        )
        return self.response(account_type_info)

    async def ctr_account_class_info(
            self,
            customer_category_id: Optional[str] = None,
            currency_id: Optional[str] = None,
            account_type_id: Optional[str] = None
    ):
        account_class_info = self.call_repos(
            await repos_get_account_class(
                session=self.oracle_session,
                customer_category_id=customer_category_id,
                currency_id=currency_id,
                account_type_id=account_type_id
            )
        )

        return self.response([dropdown(account_class) for account_class in account_class_info])
