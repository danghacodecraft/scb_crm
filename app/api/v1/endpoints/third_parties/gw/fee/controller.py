from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.fee.repository import (
    repos_gw_select_fee_by_product_name
)
from app.utils.constant.gw import GW_FUNC_SELECT_FEE_INFO_OUT


class CtrGWFeeInfo(BaseController):
    async def ctr_gw_select_fee_from_product_name(
            self, product_name: str, trans_amount: int, account_num: str
    ):
        gw_fee_info = self.call_repos(await repos_gw_select_fee_by_product_name(
            product_name=product_name, trans_amount=trans_amount, account_num=account_num, current_user=self.current_user
        ))

        fee_info = gw_fee_info[GW_FUNC_SELECT_FEE_INFO_OUT]["data_output"]

        return self.response(
            data=dict(
                charge_1=fee_info['charge_1'],
                charge_2=fee_info['charge_2'],
                charge_3=fee_info['charge_3'],
                charge_4=fee_info['charge_4']
            ))
