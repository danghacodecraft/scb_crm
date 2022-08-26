from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema, TMSCreatedUpdatedBaseModel
from app.api.v1.endpoints.approval_v2.template.amount_unblock_template.schema import (
    ManagementInfoRequest, MultipleFeeInfoRequest, SenderInfoRequest
)
from app.api.v1.endpoints.approval_v2.template.withdraw.schema import (
    TMSStatementResponse
)


class FeePaymentInfoRequest(BaseSchema):
    fee_info: MultipleFeeInfoRequest = Field(..., description="I. Phương thức tính phí")
    statement: TMSStatementResponse = Field(..., description="I.Thông tin bảng kê")
    management_info: List[ManagementInfoRequest] = Field(..., description="III.1. Thông tin quản lý")
    sender_info: SenderInfoRequest = \
        Field(..., description="III.2. Thông tin khách hàng giao dịch")


class AccountAmountBlockDetailRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    amount: int = Field(..., description="Số dư bị phong tỏa")
    amount_block_type: str = Field(
        ...,
        description="Loại phong tỏa"
                    "(value='F':FLEXCUBE, value='S':Switch,"
                    "value='P':PreAuth, value='E':Escrow,"
                    "value='A':System,"
                    "value='C':Account, value='B':Bulk Salary, value='I':P2P)"
    )
    hold_code: str = Field(..., description="Mã lý do bị phong tỏa")
    effective_date: str = Field(..., description="Ngày hiệu lực phong tỏa. format`DD/MM/YYYY`")
    expiry_date: str = Field(None, description="Ngày hết hiệu lực phong tỏa. format`DD/MM/YYYY`")
    remarks: str = Field(..., description="Ghi chú")
    verify_available_balance: str = Field(
        ...,
        description="Có hoặc không kiểm tra giá trị số dư trước khi phong tỏa. Giá trị Y/N"
    )


class TMSAccountAmountBlockResponse(TMSCreatedUpdatedBaseModel):
    account_amount_blocks: List[AccountAmountBlockDetailRequest] = Field(..., description="Danh sách tài khoản")
    fee_payment_info: FeePaymentInfoRequest = Field(..., description="Thông tin thanh toán phí")
