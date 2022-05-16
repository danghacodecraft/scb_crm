from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.category.repository import (
    repos_gw_select_category
)
from app.utils.error_messages import INVALID_TRANSACTION_FORM


class CtrSelectCategory(BaseController):
    async def ctr_select_category(
            self,
            transaction_form,
            branch_code
    ):
        select_category = self.call_repos(
            await repos_gw_select_category(
                transaction_form=transaction_form,
                branch_code=branch_code,
                current_user=self.current_user
            )
        )
        TRANSACTION_FORMS = {
            "D": "Trực tiếp",
            "I": "Gián tiếp"
        }
        if transaction_form not in TRANSACTION_FORMS:
            return self.response_exception(
                loc="get_select_category",
                msg=INVALID_TRANSACTION_FORM
            )

        select_category_list = select_category['selectCategory_out']['data_output']

        return self.response(data=[dict(
            id=select_category['MA_NV'],
            code=select_category['MA_NV'],
            name=select_category['TEN_NV']
        ) for select_category in select_category_list]
        )
