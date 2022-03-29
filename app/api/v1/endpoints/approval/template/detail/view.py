from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.template.detail.controller import (
    CtrTemplateDetail
)
from app.api.v1.endpoints.approval.template.detail.schema import (
    CifApprovalProcessResponse
)

router = APIRouter()


@router.get(
    path="/{template_id}/",
    name="Thông tin Biểu Mẫu",
    description="Thông tin Biểu Mẫu",
    responses=swagger_response(
        response_model=ResponseData[List[CifApprovalProcessResponse]],
        success_status_code=status.HTTP_200_OK
    )

)
async def view_form(
        cif_id: str = Path(..., description='Cif_id'),
        template_id: str = Path(..., description='template_id'),
        current_user=Depends(get_current_user_from_header())
):
    if template_id == "1":
        template = await CtrTemplateDetail(current_user).ctr_form_1(cif_id)
        return ResponseData(**template)

    if template_id == "2":
        template = await CtrTemplateDetail(current_user).ctr_form_2(cif_id)
        return ResponseData(**template)

    if template_id == "3":
        template = await CtrTemplateDetail(current_user).ctr_form_3(cif_id)
        return ResponseData(**template)

    if template_id == "4":
        template = await CtrTemplateDetail(current_user).ctr_form_4(cif_id)
        return ResponseData(**template)

    if template_id == "5":
        template = await CtrTemplateDetail(current_user).ctr_form_5(cif_id)
        return ResponseData(**template)

    if template_id == "6":
        template = await CtrTemplateDetail(current_user).ctr_form_6(cif_id)
        return ResponseData(**template)
