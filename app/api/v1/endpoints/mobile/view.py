from datetime import date

from fastapi import APIRouter, Depends, File, UploadFile
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.file.schema import FileServiceResponse
from app.api.v1.endpoints.mobile.controller import CtrIdentityMobile

router = APIRouter()


@router.post(
    path="/cif/identity/",
    name="Thu thập DTDD",
    description="Thu thập DTDD",
    responses=swagger_response(
        response_model=ResponseData[FileServiceResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def save_identity_mobile(
        full_name_vn: str = File(..., description='Họ và tên'),
        date_of_birth: date = File(..., description='ngày sinh'),
        gender_id: str = File(..., description='gioi tinh'),
        nationality_id: str = File(..., description='quoc tich'),
        identity_number: str = File(..., description='so GTDD'),
        issued_date: date = File(..., description='ngày cấp'),
        expired_date: date = File(..., description='ngày hết hạn'),
        place_of_issue_id: str = File(..., description='nơi cấp'),
        identity_type: str = File(..., description='loại giấy tờ dịnh danh'),
        front_side_image: UploadFile = File(..., description='hộ chiếu hoặc mặt trước DTDD'),
        back_side_image: UploadFile = File(None, description='Mặt sau DTDD'),
        avatar_image: UploadFile = File(..., description='hình ảnh khuôn mặt'),
        signature_image: UploadFile = File(None, description='hình ảnh chữ ký'),
        current_user=Depends(get_current_user_from_header()),
):
    response_data = await CtrIdentityMobile(current_user).save_identity_mobile(
        full_name_vn=full_name_vn,
        date_of_birth=date_of_birth,
        gender_id=gender_id,
        nationality_id=nationality_id,
        identity_number=identity_number,
        issued_date=issued_date,
        expired_date=expired_date,
        place_of_issue_id=place_of_issue_id,
        identity_type=identity_type,
        front_side_image=front_side_image,
        back_side_image=back_side_image,
        avatar_image=avatar_image,
        signature_image=signature_image,
    )
    return ResponseData(**response_data)
