from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.deposit.controller import CtrConfigDeposit
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/rollover-type/",
    name="Chỉ định khi đến hạn",
    description="Chỉ định khi đến hạn",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_business_type(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    rollover_type = await CtrConfigDeposit().ctr_get_rollover_type()

    return ResponseData[List[DropdownResponse]](**rollover_type)
