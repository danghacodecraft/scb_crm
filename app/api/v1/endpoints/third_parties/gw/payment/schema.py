from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema, ResponseRequestSchema
########################################################################################################################
# Request
########################################################################################################################
from app.api.v1.others.fee.schema import (
    FeeInfoResponse, MultipleFeeInfoRequest
)
from app.api.v1.schemas.utils import DropdownRequest


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


class AccountAmountBlockRequest(BaseSchema):
    account_amount_blocks: List[AccountAmountBlockDetailRequest] = Field(..., description="Danh sách tài khoản")
    fee_info: MultipleFeeInfoRequest = Field(..., description="Phương thức tính phí")


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


class AccountUnlockRequest(BaseSchema):
    account_number: str = Field(...)
    account_amount_block: List[AccountAmountUnblock] = Field(...)


# II. Bảng kê
class StatementInfoRequest(ResponseRequestSchema):
    denominations: str = Field(..., description="Mệnh giá")
    amount: int = Field(..., description="Số lượng")


# III.1 Thông tin quản lý
class ManagementInfoRequest(BaseSchema):
    direct_staff_code: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")


# III.2 Thông tin khách hàng giao dịch
class SenderInfoRequest(BaseSchema):
    cif_flag: bool = Field(..., description="Cờ có CIF chưa, `true` = Có CIF, `false` = Chưa có CIF")
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
    statement: List[StatementInfoRequest] = Field(..., description="II.Thông tin bảng kê")
    management_info: ManagementInfoRequest = Field(..., description="III.1. Thông tin quản lý")
    sender_info: SenderInfoRequest = \
        Field(..., description="III.2. Thông tin khách hàng giao dịch")


class AccountAmountUnblockRequest(BaseSchema):
    account_unlock: List[AccountUnlockRequest] = Field(..., description="Danh sách tài khoản")
    transaction_fee_info: TransactionFeeInfoRequest = Field(..., description="Thông tin thanh toán phí giao dịch")


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
    booking_id: str = Field(..., description="Booking_id")
    account_amount_blocks: List[AccountAmountBlockDetailRequest] = Field(..., description="Danh sách tài khoản")
    fee_info: FeeInfoResponse = Field(..., description="Phương thức tính phí")


class AccountAmountBlockPDResponse(PaymentSuccessResponse):
    booking_id: str = Field(..., description="Booking_id")


class GWCasaTransferAccountResponse(BaseSchema):
    booking_id: str = Field(..., description="Booking")
    p_contract_ref: Optional[str] = Field(..., description="Mã hợp đồng")
