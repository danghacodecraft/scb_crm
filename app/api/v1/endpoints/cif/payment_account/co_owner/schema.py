from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse

############################################################
# Response
############################################################


class SignatureResponse(DropdownResponse):
    image_url: str = Field(..., description='Hình ảnh mẫu chữ ký')


class BasicInformationResponse(BaseSchema):
    cif_number: str = Field(..., description='Số CIF của đồng sở hữu')
    customer_relationship: DropdownResponse = Field(..., description='Mỗi quan hệ với khách hàng')
    full_name_vn: str = Field(..., description='Tên tiếng việt của đồng sở hữu')
    date_of_birth: date = Field(..., description='Ngày sinh của đồng sở hữu')
    gender: DropdownResponse = Field(..., description='Giới tính của đồng sở hữu')
    nationality: DropdownResponse = Field(..., description='Quốc tịch của đồng sở hữu')
    mobile_number: str = Field(..., description='Số ĐTDD')
    signature_1: SignatureResponse = Field(..., description='Mẫu chữ ký 1 của đồng sở hữu')
    signature_2: SignatureResponse = Field(..., description='Mẫu chữ ký 2 của đồng sở hữu')


class IdentityDocumentResponse(BaseSchema):
    identity_number: str = Field(..., description='Số CMND/CCCD/HC')
    issued_date: date = Field(..., description='Ngày cấp')
    expired_date: date = Field(..., description='Ngày hết hạn')
    place_of_issue: DropdownResponse = Field(..., description='Nơi cấp')


class AddressInformationResponse(BaseSchema):
    content_address: str = Field(..., description='Địa chỉ liên hệ')
    resident_address: str = Field(..., description='Địa chỉ thường trú')


class AccountHolderResponse(BaseSchema):
    id: str = Field(..., description='Mã định danh của đồng sở hữu')
    full_name_vn: str = Field(..., description='Tên tiếng việt của đồng sở hữu')
    basic_information: BasicInformationResponse = Field(..., description='Thông tin cơ bản của đồng sở hữu')
    identity_document: IdentityDocumentResponse = Field(..., description='Giấy tờ định danh của đồng sở hữu')
    address_information: AddressInformationResponse = Field(..., description='Địa chỉ liên hệ của đồng sở hữu')


class SignatureAgreementAuthorResponse(BaseSchema):
    id: str = Field(..., description='Mã định danh của đồng sở hữu')
    full_name_vn: str = Field(..., description='Tên tiếng việt của đồng sở hữu')


class AgreementAuthorResponse(BaseSchema):
    id: str = Field(..., description='Mã danh mục thỏa thuận và uỷ quyền')
    code: str = Field(..., description='Code danh mục thỏa thuận và uỷ quyền')
    content: str = Field(..., description='Nội dung của danh mục thỏa thuận và uỷ quyền')
    agreement_flag: bool = Field(..., description='Thỏa thuận chữ ký các hồ sơ chứng từ.`True`: Có , `False`: Không')
    method_sign: DropdownResponse = Field(..., description='Phương thức ký')
    signature_list: List[SignatureAgreementAuthorResponse] = Field(..., description='Chữ ký của đồng sở hữu')


class AccountHolderSuccessResponse(BaseSchema):
    joint_account_holder_flag: bool = Field(..., description='Có đồng chủ sở hữu. `True`: Có , `False`: Không')
    number_of_joint_account_holder: int = Field(..., description='Số lượng đồng sở hữu')
    joint_account_holders: List[AccountHolderResponse] = Field(..., description='Thông tin cá nhân')
    agreement_authorization: List[AgreementAuthorResponse] = Field(..., description='Danh mục thỏa thuận và uỷ quyền')


############################################################
# Request
############################################################

class AccountRequest(BaseSchema):
    cif_number: str = Field(..., description='Số CIF của đồng sở hữu')


class SignatureAgreementAuthorRequest(BaseSchema):
    id: str = Field(..., description='Mã định danh của đồng sở hữu')
    full_name_vn: str = Field(..., description='Tên tiếng việt của đồng sở hữu')


class AgreementAuthorRequest(BaseSchema):
    id: str = Field(..., description='Mã danh mục thỏa thuận và uỷ quyền')
    agreement_flag: bool = Field(..., description='Thỏa thuận chữ ký các hồ sơ chứng từ.`True`: Có , `False`: Không')
    method_sign: DropdownRequest = Field(..., description='Phương thức ký')
    signature_list: List[SignatureAgreementAuthorRequest] = Field(..., description='Chữ ký của đồng sở hữu')


class AccountHolderRequest(BaseSchema):
    joint_account_holder_flag: bool = Field(..., description='Có đồng chủ sở hữu. `True`: Có , `False`: Không')
    joint_account_holders: List[AccountRequest] = Field(..., description='Danh sách các đồng sở hữu')
    agreement_authorization: List[AgreementAuthorRequest] = Field(..., description='Danh mục thỏa thuận và ủy quyền')
