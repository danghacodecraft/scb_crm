from fastapi import APIRouter, Depends, Header, Path

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval_v2.template.controller import (
    CtrTemplateDetail
)

router = APIRouter()


@router.get(
    path="/{template_id}/",
    name="Thông tin Biểu Mẫu",
    description="Thông tin Biểu Mẫu",
    # responses=swagger_response(
    #     # response_model=ResponseData[List[CifApprovalProcessResponse]],
    #     success_status_code=status.HTTP_200_OK
    # )

)
async def view_form(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        template_id: str = Path(..., description='id template version 1'),
        current_user=Depends(get_current_user_from_header())
):
    template_detail_info = await CtrTemplateDetail(current_user).ctr_get_template_detail(
        template_id=template_id,
        booking_id=BOOKING_ID
    )
    return ResponseData(**template_detail_info)
