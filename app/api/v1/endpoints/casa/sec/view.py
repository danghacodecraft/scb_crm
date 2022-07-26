from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.sec.controller import CtrSecInfo
from app.api.v1.endpoints.casa.sec.schema import SaveSecRequest

router = APIRouter()


@router.post(
    path="/sec/",
    name="Phát hành SEC",
    description="Phát hành SEC",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_open_sec_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: SaveSecRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    save_open_sec_info = await CtrSecInfo(current_user).ctr_save_open_sec_info(
        booking_id=BOOKING_ID,
        request=request
    )
    return ResponseData(**save_open_sec_info)


@router.get(
    path="/sec/",
    name="Phát hành SEC",
    description="Phát hành SEC",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_open_sec_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    get_open_sec_info = await CtrSecInfo(current_user).ctr_get_open_sec_info(
        booking_id=BOOKING_ID
    )
    return ResponseData(**get_open_sec_info)
