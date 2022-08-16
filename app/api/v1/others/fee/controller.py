from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.others.fee.repository import repos_get_fee_detail
from app.api.v1.others.fee.schema import (
    MultipleFeeInfoRequest, OneFeeInfoRequest
)
from app.utils.constant.casa import (
    CASA_FEE_METHOD_CASA, CASA_FEE_METHODS, PAYMENT_PAYERS
)
from app.utils.error_messages import (
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_CASA_FEE_METHOD_NOT_EXIST,
    ERROR_FEE_ID_NOT_EXIST, ERROR_PAYER_NOT_EXIST, ERROR_VALIDATE
)
from app.utils.functions import dropdown


class CtrAccountFee(BaseController):
    """
    Thông tin phí dành cho TKTT/TKTK
    """
    async def calculate_fees(
            self,
            fee_info_request: MultipleFeeInfoRequest,
            business_type_id: str
    ):
        """
        Tính phí dành cho NHIỀU loại phí
        """
        method_type = fee_info_request.method_type
        if method_type not in CASA_FEE_METHODS:
            return self.response_exception(msg=ERROR_CASA_FEE_METHOD_NOT_EXIST)

        fee_details = []
        total_fee = 0
        response_account_number = None
        account_owner = None
        request_account_number = fee_info_request.account_number
        if method_type == CASA_FEE_METHOD_CASA:
            if not request_account_number:
                return self.response_exception(msg=ERROR_VALIDATE)
            else:
                gw_casa_response = await CtrGWCasaAccount(
                    current_user=self.current_user
                ).ctr_gw_check_exist_casa_account_info(
                    account_number=request_account_number
                )
                gw_casa_response_data = gw_casa_response['data']
                if not gw_casa_response_data['is_existed']:
                    return self.response_exception(
                        msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                        loc=f'fee_info -> account_number: {request_account_number}'
                    )
                account_owner = gw_casa_response_data['account_owner']
                response_account_number = request_account_number

        for index, fee_detail_request in enumerate(fee_info_request.fee_details):
            fee_id = fee_detail_request.fee_id
            fee_detail = self.call_repos(await repos_get_fee_detail(
                fee_id=fee_id,
                business_type_id=business_type_id,
                session=self.oracle_session
            ))
            if fee_id and not fee_detail:
                return self.response_exception(msg=ERROR_FEE_ID_NOT_EXIST, loc=f"fee_id: {fee_id}")

            amount = fee_detail_request.amount
            vat = amount / 10
            total = amount + vat
            total_fee += total

            fee_detail_request = fee_detail_request.dict()

            fee_detail_request.update(
                fee=dropdown(fee_detail),
                fee_category=dropdown(fee_detail.category),
                vat=vat,
                total=total,
                ref_num="ABCDEF",    # TODO: Số bút toán
            )

            fee_details.append(fee_detail_request)

        return dict(
            account_number=response_account_number,
            account_owner=account_owner,
            method_type=fee_info_request.method_type,
            fee_details=fee_details,
            total_fee=total_fee
        )

    async def calculate_fee(
            self,
            one_fee_info_request: OneFeeInfoRequest,
            fee_note: Optional[str] = None
    ):
        """
        Tính phí dành cho MỘT loại phí
        """

        fee_info_response = dict(
            is_fee=False,
            payer=None,
            fee_amount=None,
            vat_tax=None,
            total=None,
            actual_total=None,
            note=fee_note
        )

        if one_fee_info_request:
            if one_fee_info_request.payer not in PAYMENT_PAYERS:
                return self.response_exception(msg=ERROR_PAYER_NOT_EXIST)

            amount = one_fee_info_request.amount
            vat = amount / 10
            total = amount + vat
            actual_total = amount + total

            fee_info_response.update(
                is_fee=True,
                payer=PAYMENT_PAYERS[one_fee_info_request.payer],
                amount=amount,
                vat=vat,
                total=total,
                actual_total=actual_total,
                note=fee_note
            )

        return fee_info_response
