from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class AccountAmountBlockRequest(BaseSchema):
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


class AmountUnblockDetail(BaseSchema):
    amount: int = Field(..., description="Số dư")
    hold_code: str = Field(..., description="Mã lý do")
    expiry_date: str = Field(..., description='Ngày hết hiệu lực')
    remarks: str = Field(..., description="Ghi chú")


class AccountAmountUnblock(BaseSchema):
    account_ref_no: str = Field(..., description="Số tham chiếu của lệnh phong tỏa tài khoản trước đó")
    p_type_unblock: str = Field(..., description="Loại hình giải tỏa: C:Toàn phần/P: Một phần")
    p_blk_detail: Optional[AmountUnblockDetail] = Field(None,
                                                        description="Chi tiết giải tỏa một phần (NULL nếu giải tỏa toàn phần)")


class PBlkChargeRequest(BaseSchema):
    charge_name: str = Field(..., description="Danh mục thu phí")
    charge_amount: int = Field(..., description="Số tiền thu phí")
    waived: str = Field(..., description="Có thu tính phí hay không")


class PayInCashRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    account_currency: str = Field(..., description="Loại tiền trong tài khoản")
    account_opening_amount: str = Field(..., description="Số tiền gửi vào")
    p_blk_charge: Optional[List[PBlkChargeRequest]] = Field(None, description="Danh mục phí")


########################################################################################################################
# Response
########################################################################################################################
class AccountAmountBlockResponse(BaseSchema):
    booking_id: str = Field(..., description="Booking_id khởi tạo khi phong tỏa tài khoản")
    account_ref_no: str = Field(..., description="Số tham chiếu của lệnh phong tỏa tài khoản")


class AccountAmountUnblockResponse(BaseSchema):
    booking_id: str = Field(..., description="Booking_id khởi tạo khi phong tỏa tài khoản")
