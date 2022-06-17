from typing import Optional

from pydantic import Field, validator

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OptionalDropdownRequest,
    OptionalDropdownResponse
)
########################################################################################################################
# Response
########################################################################################################################
# Chi tiết tài khoản thanh toán
from app.utils.constant.casa import ACCOUNT_ALLOW_NUMBER_LENGTH
from app.utils.error_messages import (
    ERROR_ACCOUNT_LENGTH_NOT_ALLOWED, MESSAGE_STATUS
)


class PaymentAccountResponse(BaseSchema):
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
    approve_status: Optional[int] = Field(..., description="Trạng thái phê duyệt tài khoản", nullable=True)


class CheckExistCasaAccountNumberResponse(BaseSchema):
    is_existed: bool = Field(..., description="Cờ đã tồn tại hay chưa <br>`True` => tồn tại <br>`False` => chưa tồn tại")


########################################################################################################################
# Request Body
########################################################################################################################
# Chi tiết tài khoản thanh toán
class SavePaymentAccountRequest(BaseSchema):
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


class CheckExistCasaAccountRequest(BaseSchema):
    casa_account_number: str = Field(..., description='Số tài khoản thanh toán', min_length=1)
