from fastapi import APIRouter, Depends, File, Path, UploadFile
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.face.controller import CtrApproveFace
from app.api.v1.endpoints.approval.face.schema import ApprovalFaceSuccess

router = APIRouter()


@router.post(
    path="/face/",
    description="[Thông tin xác thực] Upload khuôn mặt",
    name="Upload khuôn mặt",
    responses=swagger_response(
        response_model=ResponseData[ApprovalFaceSuccess],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_face(
        cif_id: str = Path(..., description='Id CIF ảo'),
        image_file: UploadFile = File(..., description='File hình ảnh giấy tờ định danh'),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrApproveFace(current_user).ctr_upload_face(
        cif_id=cif_id,
        image_file=image_file
    )

    return ResponseData[ApprovalFaceSuccess](**approve_info)
