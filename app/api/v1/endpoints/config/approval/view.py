from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.approval.controller import CtrStageAction
from app.api.v1.schemas.utils import DropdownResponse
from app.utils.constant.approval import CIF_APPROVE_STAGES
from app.utils.functions import make_description_from_dict

router = APIRouter()


@router.get(
    path="/action/",
    name="Stage Action",
    description="Hành động",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_province_info(
    stage_code: str = Query(..., description="Mã bước phê duyệt" + make_description_from_dict(CIF_APPROVE_STAGES)),
    stage_action=Depends(get_current_user_from_header())
):
    stage_action_info = await CtrStageAction(stage_action).ctr_stage_action(stage_code=stage_code)
    return ResponseData[List[DropdownResponse]](**stage_action_info)
