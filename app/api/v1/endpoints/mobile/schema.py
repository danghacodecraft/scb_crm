from datetime import date

from fastapi import File, UploadFile
from pydantic import Field

from app.api.base.schema import BaseSchema


class IdentityMobileRequest(BaseSchema):
    @staticmethod
    def upload_identity_mobile(
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
            avatar_image: UploadFile = File(..., description='hình ảnh khuôn mặt')

    ):
        return (full_name_vn, date_of_birth, gender_id, nationality_id, identity_number, issued_date, expired_date,
                place_of_issue_id, identity_type, front_side_image, back_side_image, avatar_image)


class CustomerMobileRequest(BaseSchema):
    code: str = Field(None, description='Mã giao dịch')
    full_name: str = Field(None, description='Họ và tên')
    identity_number: str = Field(None, description='Số GTDD')
