from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


########################################################################################################################
# Request
########################################################################################################################
class AccountAmountBlockRequest(BaseSchema):
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


# ---------------------------------------------- REDEEM-ACCOUNT --------------------------------------------------------#

class AccountInfo(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")


class RedemptionDetails(BaseSchema):
    redemption_mode: str = Field(...)
    redemption_amount: int = Field(...)
    waive_penalty: str = Field(...)
    waive_interest: str = Field(...)


class PayoutDetails(BaseSchema):
    payout_component: str = Field(...)
    payout_mode: str = Field(...)
    payout_amount: int = Field(...)
    offset_account: str = Field(...)


class PayoutDetailRequest(BaseSchema):
    redemption_details: RedemptionDetails = Field(...)
    payout_details: Optional[List[PayoutDetails]] = Field(None)


class RedeemAccountRequest(BaseSchema):
    account_info: AccountInfo = Field(..., description="Thông tin tài khoản")
    p_payout_detail: PayoutDetailRequest = Field(
        ...,
        description="""REDEMPTION_MODE: Loại tất toán (N: Tất toán toàn phần, Y: Tất toán một phần),
            \nREDEMPTION_AMOUNT: Số tiền tất toán (0 đối với Mode N),
            \nWAIVE_PENALTY: N (Mặc định là N),
            \nWAIVE_INTEREST: N (Mặc định là N)
            \nPAYOUT_COMPONENT: Loại tiền trả về (P là trả gốc, I là trả lãi, null đối với mode N, bắt buộc là 2 dòng I và P đối với mode Y),
            \nPAYOUT_MODE: (Loại trả tiền, S là trả về tài khoản, C là trả về tiền mặt, dốid với mode Y chỉ có thể dùng S),
            \nPAYOUT_AMOUNT:Số tiền gốc trả về đối với payout là P, Số tiền lãi trả về đối với payout là I),
            \nOFFSET_ACCOUNT: Số tài khoản trả tiền.
        """
    )


########################################################################################################################
# Response
########################################################################################################################


class PaymentSuccessResponse(BaseSchema):
    booking_id: str = Field(..., description="Booking_id khởi tạo khi phong tỏa tài khoản")


class AccountAmountBlockResponse(PaymentSuccessResponse):
    account_ref_no: str = Field(..., description="Số tham chiếu của lệnh phong tỏa tài khoản")
