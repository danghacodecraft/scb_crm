from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import (
    ResponseRequestSchema, TMSCreatedUpdatedBaseModel, TMSResponseSchema
)
from app.api.v1.endpoints.approval_v2.template.schema import (
    TMSStatementResponse
)
from app.api.v1.schemas.utils import DropdownRequest


class FeeDetailInfoRequest(TMSResponseSchema):
    fee_id: Optional[str] = Field(..., description="Mã loại phí")
    amount: Optional[str] = Field(..., description='Số tiền phí')
    content: Optional[str] = Field(..., description='Nội dung')


class MultipleFeeInfoRequest(TMSResponseSchema):
    """
    Schema dùng chung cho phí
    """
    method_type: Optional[str] = Field(..., description="Phương thức tính phí")
    account_number: Optional[str] = Field("", description='STK')
    fee_details: List[FeeDetailInfoRequest] = Field(..., description="Danh sách phí")


class AmountUnblockDetail(TMSResponseSchema):
    amount: Optional[str] = Field("", description="Số dư")
    hold_code: Optional[str] = Field("", description="Mã lý do")
    expiry_date: Optional[str] = Field(default="", description='Ngày hết hiệu lực')
    remarks: Optional[str] = Field("", description="Ghi chú")


class AccountAmountUnblock(TMSResponseSchema):
    account_ref_no: Optional[str] = Field("", description="Số tham chiếu của lệnh phong tỏa tài khoản trước đó")
    p_type_unblock: Optional[str] = Field("", description="Loại hình giải tỏa: C:Toàn phần/P: Một phần")
    checkox_value: Optional[str] = Field(
        "", description='C: Toàn bộ số tiền tạm khóa/ P: Một phần số tiền tạm khóa, số tiền:'
    )
    p_blk_detail: Optional[AmountUnblockDetail] = Field('',
                                                        description="Chi tiết giải tỏa một phần (NULL nếu giải tỏa toàn phần)")


class AccountUnlockRequest(TMSResponseSchema):
    account_number: Optional[str] = Field(...)
    account_amount_block: List[AccountAmountUnblock] = Field(...)


class StatementInfoRequest(ResponseRequestSchema):
    denominations: Optional[str] = Field("", description="Mệnh giá")
    amount: Optional[str] = Field("", description="Số lượng")
    into_money: Optional[str] = Field("", description="Thành tiền")


class ManagementInfoRequest(TMSResponseSchema):
    indirect_staff_code: Optional[str] = Field(default='', description="Mã nhân viên quản lý gián tiếp")
    direct_staff_code: Optional[str] = Field(default='', description="Mã nhân viên kinh doanh")


class SenderInfoRequest(TMSResponseSchema):
    # cif_flag: Optional[bool] = Field(, description="Cờ có CIF chưa, `true` = Có CIF, `false` = Chưa có CIF")
    cif_number: Optional[str] = Field('', description="Số CIF")
    fullname_vn: Optional[str] = Field('', description="Người giao dịch")
    identity: Optional[str] = Field('', description="Thông tin giấy tờ định danh")
    issued_date: Optional[date] = Field('', description="Ngày cấp")
    place_of_issue: Optional[DropdownRequest] = Field('', description="Nơi cấp")
    address_full: Optional[str] = Field('', description="Địa chỉ")
    mobile_phone: Optional[str] = Field('', description="SĐT")
    telephone: Optional[str] = Field('', description="SĐT")
    otherphone: Optional[str] = Field('', description="SĐT")
    note: Optional[str] = Field('', description="Ghi chú")


class TransactionFeeInfoRequest(TMSResponseSchema):
    fee_info: MultipleFeeInfoRequest = Field(..., description="I. Phương thức tính phí")
    statement: TMSStatementResponse = Field(..., description="I.Thông tin bảng kê")
    management_info: ManagementInfoRequest = Field(..., description="III.1. Thông tin quản lý")
    sender_info: SenderInfoRequest = \
        Field(..., description="III.2. Thông tin khách hàng giao dịch")


class TMSAccountAmountUnblockRequest(TMSCreatedUpdatedBaseModel):
    account_unlock: List[AccountUnlockRequest] = Field(..., description="Danh sách tài khoản")
    transaction_fee_info: TransactionFeeInfoRequest = Field(..., description="Thông tin thanh toán phí giao dịch")
