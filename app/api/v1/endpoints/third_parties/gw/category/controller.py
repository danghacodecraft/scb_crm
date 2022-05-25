from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.category.repository import (
    repos_gw_select_category
)
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.gw import GW_REQUEST_DIRECT_INDIRECT
from app.utils.functions import optional_dropdown


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
            if transaction_name == GW_REQUEST_DIRECT_INDIRECT:
                response_datas.append(dict(
                    employee_code=category['MA_NV'],
                    employee_name=category['TEN_NV'],
                    department=optional_dropdown(obj=None, obj_name=category['PHONG_BAN']),
                    branch=await self.dropdown_mapping_crm_model_or_dropdown_name(
                        model=Branch,
                        name=None,
                        code=category['MA_DON_VI'],
                    )
                ))
            else:
                for key, value in category.items():
                    response_datas.append(dict(
                        id=key,
                        code=key,
                        name=value
                    ))

        return self.response(data=response_datas)
