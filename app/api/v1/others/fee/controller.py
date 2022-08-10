from app.api.base.controller import BaseController
from app.api.v1.others.fee.repository import repos_get_fee_detail
from app.api.v1.others.fee.schema import FeeInfoRequest
from app.utils.constant.casa import CASA_FEE_METHODS
from app.utils.error_messages import (
    CASA_FEE_METHOD_NOT_EXIST, ERROR_FEE_ID_NOT_EXIST
)


class BaseAccountFee(BaseController):
    """
    Thông tin phí dành cho TKTT/TKTK
    """
    async def calculate_fee(self, fee_info_request: FeeInfoRequest, business_type_id: str):
        """
        Tính phí
        """
        method_type = fee_info_request.method_type
        if method_type not in CASA_FEE_METHODS:
            return self.response_exception(msg=CASA_FEE_METHOD_NOT_EXIST)

        fee_id = fee_info_request.fee_id
        fee_detail = await repos_get_fee_detail(
            fee_id=fee_id,
            business_type_id=business_type_id,
            session=self.oracle_session
        )
        if fee_id and not fee_detail:
            return self.response_exception(msg=ERROR_FEE_ID_NOT_EXIST, loc=f"fee_id: {fee_id}")

        amount = fee_info_request.amount
        vat = amount / 10
        total = amount + vat

        saving_fee_info = fee_info_request.dict()
        saving_fee_info.update(
            vat=vat,
            total=total,
            ref_num="ABCDEF"    # TODO: Số bút toán
        )
        return saving_fee_info
