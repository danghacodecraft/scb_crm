from typing import List, Optional

from pydantic import Field

from app.api.base.schema import TMSCreatedUpdatedBaseModel, TMSResponseSchema
from app.api.v1.endpoints.approval_v2.template.amount_unblock_template.schema import (
    ManagementInfoRequest, MultipleFeeInfoRequest, SenderInfoRequest
)
from app.api.v1.endpoints.approval_v2.template.withdraw.schema import (
    TMSStatementResponse
)
from app.api.v1.schemas.utils import DropdownResponse


class FeePaymentInfoRequest(TMSResponseSchema):
    fee_info: MultipleFeeInfoRequest = Field('', description="I. Phương thức tính phí")
    statement: TMSStatementResponse = Field('', description="I.Thông tin bảng kê")
    management_info: List[ManagementInfoRequest] = Field('', description="III.1. Thông tin quản lý")
    sender_info: SenderInfoRequest = \
        Field('', description="III.2. Thông tin khách hàng giao dịch")


class FeeDetailInfoResponse(TMSResponseSchema):
    payer: Optional[str] = Field(None, description="Bên thanh toán phí")
    fee_category: Optional[DropdownResponse] = Field(None, description="Nhóm phí")
    fee: Optional[DropdownResponse] = Field(None, description="Mã loại phí")
    amount: Optional[str] = Field(None, description='Số tiền phí')
    vat: Optional[str] = Field(None, description='Thuế VAT')
    total: Optional[str] = Field(None, description='Tổng phí')
    actual_total: Optional[str] = Field(None, description="Số tiền thực chuyển")
    note: str = Field(None, description='Nội dung')
    ref_num: str = Field(None, description='Số bút toán')


class FeeInfoResponse(TMSResponseSchema):
    method_type: Optional[str] = Field('', description="Phương thức tính phí:")
    account_number: Optional[str] = Field('', description='STK')
    account_owner: Optional[str] = Field('', description="Chủ tài khoản")
    fee_details: List[FeeDetailInfoResponse] = Field('', description="Danh sách phí")
    total_fee: Optional[str] = Field('', description="Tổng phí")


class AccountAmountBlockDetailRequest(TMSResponseSchema):
    account_number: Optional[str] = Field('', description="Số tài khoản")
    amount: Optional[str] = Field('', description="Số dư bị phong tỏa")
    amount_block_type: Optional[str] = Field(
        '',
        description="Loại phong tỏa"
                    "(value='F':FLEXCUBE, value='S':Switch,"
                    "value='P':PreAuth, value='E':Escrow,"
                    "value='A':System,"
                    "value='C':Account, value='B':Bulk Salary, value='I':P2P)"
    )
    hold_code: Optional[str] = Field('', description="Mã lý do bị phong tỏa")
    effective_date: Optional[str] = Field('', description="Ngày hiệu lực phong tỏa. format`DD/MM/YYYY`")
    expiry_date: Optional[str] = Field('', description="Ngày hết hiệu lực phong tỏa. format`DD/MM/YYYY`")
    remarks: Optional[str] = Field('', description="Ghi chú")
    verify_available_balance: Optional[str] = Field(
        '',
        description="Có hoặc không kiểm tra giá trị số dư trước khi phong tỏa. Giá trị Y/N"
    )


# class TMSAccountAmountBlockResponse(TMSCreatedUpdatedBaseModel):
#     account_amount_blocks: List[AccountAmountBlockDetailRequest] = Field('', description="Danh sách tài khoản")
#     fee_payment_info: FeePaymentInfoRequest = Field('', description="Thông tin thanh toán phí")

class FeePaymentInfoResponse(TMSResponseSchema):
    fee_info: FeeInfoResponse = Field(..., description="Phương thức tính phí")
    statement: TMSStatementResponse = Field(..., description="II.Thông tin bảng kê")
    management_info: ManagementInfoRequest = Field(..., description="III.1. Thông tin quản lý")
    sender_info: SenderInfoRequest = \
        Field(..., description="III.2. Thông tin khách hàng giao dịch")


class TMSAccountAmountBlockResponse(TMSCreatedUpdatedBaseModel):
    account_amount_blocks: List[AccountAmountBlockDetailRequest] = Field(..., description="Danh sách tài khoản")
    fee_payment_info: FeePaymentInfoResponse = Field(..., description='thông tin phí')
    customer_cif_number: Optional[str] = Field('')
