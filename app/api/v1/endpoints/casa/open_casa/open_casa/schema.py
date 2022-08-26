from typing import List, Optional

from pydantic import Field, validator

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OptionalDropdownRequest,
    OptionalDropdownResponse
)
from app.utils.constant.casa import ACCOUNT_ALLOW_NUMBER_LENGTH
from app.utils.error_messages import (
    ERROR_ACCOUNT_LENGTH_NOT_ALLOWED, MESSAGE_STATUS
)


class SavePaymentAccountRequest(BaseSchema):
    booking_business_form_id: Optional[str] = Field(
        ...,
        description="Mã giao dịch tài khoản thanh toán, "
                    "nếu có truyền vào thì là cập nhật thông tin tài khoản đó"
                    "nếu tạo mới thì không cần truyền id"
    )
    self_selected_account_flag: bool = Field(..., description="""Cờ tự chọn số tài khoản
                                                              \nSố tài khoản thường => `False`
                                                              \nSố tài khoản yêu cầu => `True`""")
    currency: DropdownRequest = Field(..., description="Loại tiền")
    account_type: DropdownRequest = Field(..., description="Gói tài khoản")
    account_class: DropdownRequest = Field(..., description="Loại hình tài khoản")
    # account_structure_type_level_1: OptionalDropdownRequest = Field(None, description="Kiểu kiến trúc cấp 1")
    account_structure_type_level_2: OptionalDropdownRequest = Field(..., description="Kiểu kiến trúc cấp 2")
    # account_structure_type_level_3: OptionalDropdownRequest = Field(..., description="Kiểu kiến trúc cấp 3")
    casa_account_number: Optional[str] = Field(None, description="""Số tài khoản
                                                \n`self_selected_account_flag`=`True` => Bắt buộc truyền lên
                                                \n`self_selected_account_flag`=`False` => Không bắt buộc truyền lên""",
                                               min_length=1)
    account_salary_organization_account: Optional[str] = Field(..., description="Tài khoản của tổ chức chi lương", min_length=1)

    @validator('casa_account_number', 'account_salary_organization_account')
    def check_account_number_length(cls, v):
        if v is None:
            v = ''
        assert len(v) in ACCOUNT_ALLOW_NUMBER_LENGTH, MESSAGE_STATUS[ERROR_ACCOUNT_LENGTH_NOT_ALLOWED]
        return v


class CasaOpenCasaRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    casa_accounts: List[SavePaymentAccountRequest] = Field(..., description="Danh sách TKTT")


class CasaAccountInfoResponse(BaseSchema):
    booking_business_form_id: str = Field(..., description="Mã giao dịch tài khoản thanh toán")
    self_selected_account_flag: bool = Field(..., description="""Cờ tự chọn số tài khoản
                                                                  \nSố tài khoản thường => `False`
                                                                  \nSố tài khoản yêu cầu => `True`""")
    currency: DropdownResponse = Field(..., description="Loại tiền")
    account_type: DropdownResponse = Field(..., description="Gói tài khoản")
    account_class: DropdownResponse = Field(..., description="Loại hình tài khoản")
    account_structure_type_level_1: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 1")
    account_structure_type_level_2: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 2")
    account_structure_type_level_3: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 3")
    casa_account_number: Optional[str] = Field(..., description="Số tài khoản", nullable=True)
    account_salary_organization_account: Optional[str] = Field(..., description="Tài khoản của tổ chức chi lương",
                                                               nullable=True)
    account_salary_organization_name: Optional[str] = Field(..., description="Chủ tài khoản chi lương", nullable=True)
    approve_status: Optional[bool] = Field(..., description="Trạng thái phê duyệt tài khoản", nullable=True)


class CasaAccountResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    account_info: CasaAccountInfoResponse = Field(..., description="Chi tiết tài khoản thanh toán")


class CasaOpenCasaResponse(BaseSchema):
    booking_parent_id: str = Field(..., description="Mã giao dịch")
    transaction_code: str = Field(..., description="Mã giao dịch")
    read_only: bool = Field(..., description="có read only không")
    total_item: int = Field(..., description="Tổng số TKTT")
    casa_accounts: List[CasaAccountResponse] = Field(..., description="Danh sách TKTT")
