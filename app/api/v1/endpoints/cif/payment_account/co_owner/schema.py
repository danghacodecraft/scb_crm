from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest, OptionalDropdownResponse

############################################################
# Response
############################################################


class SignatureResponse(BaseSchema):
    id: Optional[str] = Field(..., description="Id giấy tờ định danh")
    image_url: Optional[str] = Field(..., description="Hình ảnh mẫu chữ ký")


class SignatureListResponse(BaseSchema):
    cif_number: Optional[str] = Field(..., description="CIF_NUMBER")
    full_name_vn: Optional[str] = Field(..., description="Tên tiếng việt")


class BasicInformationResponse(BaseSchema):
    cif_number: Optional[str] = CustomField(
        description="Số CIF của đồng sở hữu"
    ).OptionalCIFNumberField
    customer_relationship: OptionalDropdownResponse = Field(
        None, description="Mỗi quan hệ với khách hàng"
    )
    full_name_vn: Optional[str] = Field(
        None, description="Tên tiếng việt của đồng sở hữu"
    )
    date_of_birth: Optional[date] = Field(None, description="Ngày sinh của đồng sở hữu")
    gender: OptionalDropdownResponse = Field(
        None, description="Giới tính của đồng sở hữu"
    )
    nationality: OptionalDropdownResponse = Field(
        None, description="Quốc tịch của đồng sở hữu"
    )
    mobile_number: Optional[str] = Field(None, description="Số ĐTDD")
    signature: Optional[List[SignatureResponse]] = Field(
        ..., description="Mẫu chữ ký của đồng sở hữu"
    )


class IdentityDocumentResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số CMND/CCCD/HC")
    # identity_type: OptionalDropdownResponse = Field(..., description='Loại giấy tờ định danh')
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    # Rollback lại thành OptionalDropdown tránh 500 error
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


class AddressInformationResponse(BaseSchema):
    contact_address: Optional[str] = Field(..., description="Địa chỉ liên hệ")
    resident_address: Optional[str] = Field(..., description="Địa chỉ thường trú")


class AccountHolderResponse(BaseSchema):
    document_file: str = Field(..., description="Tập tin đính kèm")
    id: str = Field(..., description="Mã định danh của đồng sở hữu")
    avatar_url: Optional[str] = Field(..., description="Tên tiếng việt của đồng sở hữu")
    basic_information: BasicInformationResponse = Field(
        ..., description="Thông tin cơ bản của đồng sở hữu"
    )
    identity_document: IdentityDocumentResponse = Field(
        ..., description="Giấy tờ định danh của đồng sở hữu"
    )
    address_information: AddressInformationResponse = Field(
        ..., description="Địa chỉ liên hệ của đồng sở hữu"
    )


class SignatureAgreementAuthorResponse(BaseSchema):
    id: str = Field(..., description="Mã định danh của đồng sở hữu")
    full_name_vn: str = Field(..., description="Tên tiếng việt của đồng sở hữu")


class AgreementAuthorResponse(BaseSchema):
    id: str = Field(..., description="Mã danh mục thỏa thuận và uỷ quyền")
    code: str = Field(..., description="Code danh mục thỏa thuận và uỷ quyền")
    name: str = Field(..., description="Nội dung của danh mục thỏa thuận và uỷ quyền")
    active_flag: Optional[bool] = Field(
        ...,
        description="Thỏa thuận chữ ký các hồ sơ chứng từ.`True`: Có , `False`: Không",
    )
    method_sign: Optional[int] = Field(..., description="Phương thức ký")
    signature_list: Optional[List[SignatureListResponse]] = Field(..., description='Danh sách chữ ký')


class AccountHolderSuccessResponse(BaseSchema):
    joint_account_holder_flag: bool = Field(
        ..., description="Có đồng chủ sở hữu. `True`: Có , `False`: Không"
    )
    number_of_joint_account_holder: int = Field(..., description="Số lượng đồng sở hữu")
    joint_account_holders: List[AccountHolderResponse] = Field(
        ..., description="Thông tin cá nhân"
    )
    agreement_authorization: Optional[List[AgreementAuthorResponse]] = Field(
        ..., description="Danh mục thỏa thuận và uỷ quyền"
    )


############################################################
# Request
############################################################


class AccountRequest(BaseSchema):
    cif_number: str = CustomField(description="Số CIF của đồng sở hữu").CIFNumberField
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ của khách hàng với đồng sở hữu")


class SignatureAgreementAuthorRequest(BaseSchema):
    cif_number: str = CustomField(
        description="Mã định danh của đồng sở hữu"
    ).CIFNumberField
    full_name_vn: str = Field(..., description="Tên tiếng việt của đồng sở hữu")


class AgreementAuthorRequest(BaseSchema):
    agreement_author_id: str = Field(..., description="Mã danh mục thỏa thuận và uỷ quyền")
    agreement_flag: bool = Field(
        ...,
        description="Thỏa thuận chữ ký các hồ sơ chứng từ.`True`: Có , `False`: Không",
    )
    method_sign: int = Field(..., description="Phương thức ký")
    signature_list: Optional[List[SignatureAgreementAuthorRequest]] = Field(
        ..., description="Chữ ký của đồng sở hữu"
    )


class AccountHolderRequest(BaseSchema):
    joint_account_holder_flag: bool = Field(
        ..., description="Có đồng chủ sở hữu. `True`: Có , `False`: Không"
    )
    number: str = Field(..., description="Số văn bản")
    create_at: date = Field(..., description="Ngày lập")
    address_flag: bool = Field(..., description="Nơi lập")
    file_uuid: str = Field(..., description="Tập tin đính kèm")
    joint_account_holders: List[AccountRequest] = Field(
        ..., description="Danh sách các đồng sở hữu"
    )
    agreement_authorization: List[AgreementAuthorRequest] = Field(
        ..., description="Danh mục thỏa thuận và ủy quyền"
    )


########################################################################################################################
# dùng chung phần schema với lấy data của đồng sở hữu
########################################################################################################################


class DetailCoOwnerResponse(BaseSchema):
    id: str = Field(..., description="Mã định danh của đồng sở hữu")
    basic_information: BasicInformationResponse = Field(
        ..., description="Thông tin cơ bản của đồng sở hữu"
    )
    identity_document: IdentityDocumentResponse = Field(
        ..., description="Giấy tờ định danh của đồng sở hữu"
    )
    address_information: AddressInformationResponse = Field(
        ..., description="Địa chỉ liên hệ của đồng sở hữu"
    )
    avatar_url: Optional[str] = Field(..., description="URL hình ảnh đại diện của người dùng")
