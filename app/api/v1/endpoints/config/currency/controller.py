from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_currency_config


class CtrConfigCurrency(BaseController):
    async def ctr_currency_info(self):
        currency_info = self.call_repos(
            await repos_get_data_currency_config(
                session=self.oracle_session
            )
        )
        response_data = [{
            'currency_id': item.Currency.id,
            'currency_code': item.Currency.code,
            'currency_name': item.Currency.name,
            'country_id': item.AddressCountry.id,
            'country_code': item.AddressCountry.code,
            'country_name': item.AddressCountry.name,
        } for item in currency_info]

        return self.response(response_data)
