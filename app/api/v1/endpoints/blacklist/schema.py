from datetime import date,datetime

from pydantic import Field

from app.api.base.schema import BaseSchema


class BlacklistRequest(BaseSchema):
    # id :int = Field(..., description="id")
    full_name: str = Field(..., description="Họ và tên", max_length=30)
    date_of_birth: datetime = Field(..., description="ngày sinh")
    identity_id: str = Field(..., description="giấy tờ định danh", max_length=50)
    issued_date: datetime = Field(..., description="ngày cấp")
    place_of_issue_id: str = Field(..., description="nơi cấp", max_length=500)
    cif_num: str = Field(..., description="số cif", max_length=10)
    casa_account_num: str = Field(..., description="Số tài khoản ngân hàng SCB", max_length=20)
    branch_id: str = Field(..., description="mã chi nhánh", max_length=5)
    date_open_account_number: datetime = Field(..., description="ngày mở tài khoản ngân hàng")
    mobile_num: str = Field(..., description="số điện thoại cá nhân", max_length=25)
    place_of_residence: str = Field(..., description="địa chỉ hộ khẩu", max_length=500)
    place_of_origin: str = Field(..., description="nơi sinh", max_length=1000)
    reason: str = Field(..., description="Chuyeen de", max_length=1000)
    job_content: str = Field(..., description="nội dung công việc", max_length=500)
    blacklist_source: str = Field(..., description="nguồn", max_length=500)
    document_no: str = Field(..., description="Số văn bản đến", max_length=20)
    blacklist_area: str = Field(..., description="khu vực", max_length=500)
    created_at: datetime = Field(..., description="Ngày tạo")
    updated_at: datetime = Field(..., description="Ngày cập nhập")


class BlacklistResponse(BlacklistRequest):
    id: int = Field(..., description="id")
