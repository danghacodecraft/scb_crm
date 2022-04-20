from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.dashboard.account_info.controller import (
    CtrAccountInfo
)
# from app.api.v1.endpoints.third_parties.schema import (
#     GWCasaAccountByCIFNumberRequest, GWCasaAccountByCIFNumberResponse
# )
from app.api.v1.endpoints.dashboard.account_info.schema import (
    AccountInformationRequest
)

router = APIRouter()


@router.post(
    path="/account-info/",
    name="360 - THÔNG TIN TÀI KHOẢN",
    description="360 - THÔNG TIN TÀI KHOẢN",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_account_info(
        request=Body(...),
        current_user=Depends(get_current_user_from_header())
):
    customer_information = await CtrAccountInfo(current_user).ctr_get_account_info(
        cif_number=request.get("cif_number")
    )
    return ResponseData[AccountInformationRequest](**customer_information)
