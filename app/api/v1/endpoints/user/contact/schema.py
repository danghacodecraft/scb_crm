from pydantic import Field

from app.api.base.schema import BaseSchema


class ContactResponse(BaseSchema):
    emp_name: str = Field(None, description="Dương Đỗ Nguyên")
    emp_code: str = Field(None, description="17487")
    username: str = Field(None, description="NGUYENDD1")
    working_location: str = Field(None, description="Số 927 Trần Hưng Đạo, Phường 12, Quận 5, TP.Hồ Chí Minh")
    email_scb: str = Field(None, description="nguyendd1@scb.com.vn")
    contact_mobile: str = Field(None, description="mb_00965")
    internal_mobile: str = Field(None, description="imb_00965")
    emp_id: str = Field(None, description="6036")
    title_name: str = Field(None, description="Nhân Viên PTUDNB")
    unit: str = Field(None,
                      description="Ngân hàng TMCP Sài Gòn;Ban Điều hành;Khối Vận hành và Công nghệ;Trung tâm Vận hành và Phát triển Giải pháp;Phòng Phát triển Giải pháp;Mảng Phát triển Hệ thống [Back-end]")
    avatar_link: str = Field(None, description="/cdn/user-profile/00965.jpeg")
