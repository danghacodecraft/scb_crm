from fastapi import APIRouter, Depends, Header, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval_v2.template.controller import (
    CtrTemplateDetail
)
from app.api.v1.endpoints.approval_v2.template.schema import (
    TMSApprovalResponse
)

router = APIRouter()


@router.get(
    path="/fill_data/",
    name="fill_and_return template",
    description="fill_and_return",
    responses=swagger_response(
        response_model=ResponseData[TMSApprovalResponse],
        success_status_code=status.HTTP_200_OK
    )

)
async def fill_data_template(
        booking_id: str = Header(..., description="Mã phiên giao dịch"),
        current_user=Depends(get_current_user_from_header())
):

    template_detail_info = await CtrTemplateDetail().ctr_get_template_after_fill(
        booking_id=booking_id
    )
    return template_detail_info


@router.get(
    path="/data_source/{template_id}/",
    name="API for fill data",
    description="API for fill data",
)
async def view_form(
        booking_id: str = Header(..., description="Mã phiên giao dịch"),
        template_id: str = Path(..., description='id template version 1'),
        current_user=Depends(get_current_user_from_header())
):
    template_detail_info = await CtrTemplateDetail().ctr_get_template_detail(
        template_id=template_id,
        booking_id=booking_id
    )

    return template_detail_info
