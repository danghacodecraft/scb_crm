from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.sec.controller import CtrSecInfo
from app.api.v1.endpoints.casa.sec.schema import SecRequest

router = APIRouter()


@router.post(
    path="/sec/{account_num}/",
    name="Phát hành SEC",
    description="Phát hành SEC",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_sec_info(
        account_num: str = Path(..., description='Số tài khoản'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: SecRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    sec_info = await CtrSecInfo(current_user).ctr_sec_info(
        booking_id=BOOKING_ID,
        account_num=account_num,
        request=request
    )
    return ResponseData(**sec_info)
