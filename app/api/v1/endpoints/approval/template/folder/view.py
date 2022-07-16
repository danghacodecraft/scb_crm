from typing import List

from fastapi import APIRouter, Depends, Header, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.template.folder.controller import (
    CtrTemplateFolder
)
from app.api.v1.endpoints.approval.template.folder.schema import (
    ApprovalTemplateFolderResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="Danh sách Biểu Mẫu",
    description="Lấy danh sách các biểu mẫu",
    responses=swagger_response(
        response_model=ResponseData[List[ApprovalTemplateFolderResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_approval_template_folder_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    template_folder_info = await CtrTemplateFolder(current_user).ctr_get_approval_template_folder_info(
        booking_id=BOOKING_ID
    )
    return ResponseData[List[ApprovalTemplateFolderResponse]](**template_folder_info)
