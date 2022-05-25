from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.category.repository import (
    repos_gw_select_category
)


class CtrSelectCategory(BaseController):
    async def ctr_select_category(
            self,
            transaction_name,
            transaction_value
    ):
        select_category = self.call_repos(
            await repos_gw_select_category(
                transaction_name=transaction_name,
                transaction_value=transaction_value,
                current_user=self.current_user
            )
        )

        select_category_list = select_category['selectCategory_out']['data_output']

        response_datas = []
        for category in select_category_list:
            for key, value in category.items():
                response_datas.append(dict(
                    id=key,
                    code=key,
                    name=value
                ))

        return self.response(data=response_datas)
