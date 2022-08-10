from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import (
    repos_get_data_currency_denominations_config
)


class CtrConfigCurrencyDenomination(BaseController):
    async def ctr_currency_denominations_info(self, currency_id: str):
        currency_denominations_info = self.call_repos(
            await repos_get_data_currency_denominations_config(
                session=self.oracle_session, currency_id=currency_id
            )
        )
        response_data = [{
            'denominations_name': item.denominations_name,
            'denominations': int(item.denominations)
        } for item in currency_denominations_info]

        return self.response(response_data)
