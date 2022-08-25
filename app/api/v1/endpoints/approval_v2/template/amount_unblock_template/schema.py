from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import (
    BaseSchema, ResponseRequestSchema, TMSCreatedUpdatedBaseModel
)
from app.api.v1.endpoints.approval_v2.template.schema import (
    TMSStatementResponse
)
from app.api.v1.schemas.utils import DropdownRequest


class FeeDetailInfoRequest(BaseSchema):
    fee_id: Optional[str] = Field(..., description="Mã loại phí")
    amount: str = Field(..., description='Số tiền phí')
    content: str = Field(..., description='Nội dung')


class MultipleFeeInfoRequest(BaseSchema):
    """
    Schema dùng chung cho phí
    """
    method_type: str = Field(..., description="Phương thức tính phí")
    account_number: Optional[str] = Field(None, description='STK')
    fee_details: List[FeeDetailInfoRequest] = Field(..., description="Danh sách phí")


class AmountUnblockDetail(BaseSchema):
    amount: str = Field(..., description="Số dư")
    hold_code: str = Field(..., description="Mã lý do")
    expiry_date: str = Field(..., description='Ngày hết hiệu lực')
    remarks: str = Field(..., description="Ghi chú")


class AccountAmountUnblock(BaseSchema):
    account_ref_no: str = Field(..., description="Số tham chiếu của lệnh phong tỏa tài khoản trước đó")
    p_type_unblock: str = Field(..., description="Loại hình giải tỏa: C:Toàn phần/P: Một phần")
    p_blk_detail: Optional[AmountUnblockDetail] = Field(None,
                                                        description="Chi tiết giải tỏa một phần (NULL nếu giải tỏa toàn phần)")


class AccountUnlockRequest(BaseSchema):
    account_number: str = Field(...)
    account_amount_block: List[AccountAmountUnblock] = Field(...)


class StatementInfoRequest(ResponseRequestSchema):
    denominations: str = Field(..., description="Mệnh giá")
    amount: str = Field(..., description="Số lượng")


class ManagementInfoRequest(BaseSchema):
    direct_staff_code: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")


class SenderInfoRequest(BaseSchema):
    # cif_flag: Optional[bool] = Field(, description="Cờ có CIF chưa, `true` = Có CIF, `false` = Chưa có CIF")
    cif_number: Optional[str] = Field(None, description="Số CIF")
    fullname_vn: Optional[str] = Field(None, description="Người giao dịch")
    identity: Optional[str] = Field(None, description="Thông tin giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: Optional[DropdownRequest] = Field(None, description="Nơi cấp")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    mobile_phone: Optional[str] = Field(None, description="SĐT")
    telephone: Optional[str] = Field(None, description="SĐT")
    otherphone: Optional[str] = Field(None, description="SĐT")
    note: Optional[str] = Field(None, description="Ghi chú")


class TransactionFeeInfoRequest(BaseSchema):
    fee_info: MultipleFeeInfoRequest = Field(..., description="I. Phương thức tính phí")
    statement: TMSStatementResponse = Field(..., description="I.Thông tin bảng kê")
    management_info: ManagementInfoRequest = Field(..., description="III.1. Thông tin quản lý")
    sender_info: SenderInfoRequest = \
        Field(..., description="III.2. Thông tin khách hàng giao dịch")


class TMSAccountAmountUnblockRequest(TMSCreatedUpdatedBaseModel):
    account_unlock: List[AccountUnlockRequest] = Field(..., description="Danh sách tài khoản")
    transaction_fee_info: TransactionFeeInfoRequest = Field(..., description="Thông tin thanh toán phí giao dịch")
