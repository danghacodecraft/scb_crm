from typing import List

from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.category.controller import (
    CtrSelectCategory
)
from app.api.v1.endpoints.third_parties.gw.category.example import (
    GW_CATEGORY_EXAMPLES
)
from app.api.v1.endpoints.third_parties.gw.category.schema import (
    GWCategoryRequest
)
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Select Category",
    description="[GW] Lấy danh mục trên core FCC",
    responses=swagger_response(
        response_model=ResponseData[DropdownResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_select_category(
        request: GWCategoryRequest = Body(..., examples=GW_CATEGORY_EXAMPLES),
        current_user=Depends(get_current_user_from_header())
):
    select_category = await CtrSelectCategory(current_user).ctr_select_category(
        transaction_name=request.transaction_name,
        transaction_value=request.transaction_value
    )
    return ResponseData[List[DropdownResponse]](**select_category)
