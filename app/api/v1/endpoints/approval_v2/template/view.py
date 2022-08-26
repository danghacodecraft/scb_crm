from fastapi import APIRouter, Depends, Header, Path

from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval_v2.template.controller import (
    CtrTemplateDetail
)

router = APIRouter()


@router.get(
    path="/{template_id}/",
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


@router.get(
    path="/{template_id}/fill_data/",
    name="fill_and_return template",
    description="fill_and_return",
)
async def fill_data_template(
        booking_id: str = Header(..., description="Mã phiên giao dịch"),
        template_id: str = Path(..., description='id template version 1'),
        current_user=Depends(get_current_user_from_header())
):
    template_detail_info = await CtrTemplateDetail().ctr_get_template_after_fill(
        template_id=template_id,
        booking_id=booking_id
    )
    return template_detail_info
