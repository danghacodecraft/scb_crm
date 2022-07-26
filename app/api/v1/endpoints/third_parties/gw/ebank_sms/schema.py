from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema

# GW selectMobileNumberSMSByAccountCASA


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoRequest(BaseSchema):
    ebank_sms_indentify_num: str = Field(..., description="Số tài khoản thanh toán", example="1380104914870005")


class GWSelectMobileNumberSMSByAccountCASARequest(BaseSchema):
    ebank_sms_info: SelectMobileNumberSMSByAccountCASAEbankSMSInfoRequest


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemBranchInfoResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị đăng ký dịch vụ", example="")
    branch_name_vn: str = Field(..., description="Tên đơn vị đăng ký dịch vụ", example="")


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemResponse(BaseSchema):
    ebank_sms_indentify_num: str = Field(..., description="Số điện thoại", example="")
    ebank_sms_full_name: str = Field(..., description="Họ và tên", example="")
    ebank_sms_owner_phone: str = Field(..., description="Loại số điện thoại: Chính chủ: 'Y', người thân: 'N'",
                                       example="")
    ebank_sms_relations: str = Field(..., description="Mối quan hệ với số điện thoại chính. VD: Bố mẹ, Vợ chồng",
                                     example="")
    ebank_sms_reg_date: date = Field(..., description="Ngày đăng ký", example="")
    ebank_sms_status: str = Field(..., description="Trạng thái hoạt động", example="")
    branch_info: SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemBranchInfoResponse


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoListResponse(BaseSchema):
    ebank_sms_info_item: SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemResponse


class GWSelectMobileNumberSMSByAccountCASAResponse(BaseSchema):
    ebank_sms_info_list: List[SelectMobileNumberSMSByAccountCASAEbankSMSInfoListResponse]
##
