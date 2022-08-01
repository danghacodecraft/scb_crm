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
    id: str = Field(..., description="Mã mẫu chữ ký")
    image_url: str = Field(..., description="Ảnh mẫu chữ ký")


class BasicInformationResponse(BaseSchema):
    cif_number: str = Field(description="Số CIF của đồng sở hữu")
    customer_relationship: OptionalDropdownResponse = Field(None,
                                                            description="Mối quan hệ của khách hàng với đồng sở hữu")
    full_name_vn: str = Field(..., description="Họ và tên")
    date_of_birth: str = Field(..., description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    mobile_number: str = Field(..., description="Số ĐTDĐ")
    signature: List[SignatureResponse] = Field(None, description="Mẫu chữ ký")


class IdentityDocumentResponse(BaseSchema):
    identity_number: str = Field(..., description="Số CMND/CCCD/Hộ Chiếu")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


class AddressInformationResponse(BaseSchema):
    contact_address: Optional[str] = Field(..., description="Địa chỉ liên hệ")
    resident_address: Optional[str] = Field(..., description="Địa chỉ thường trú")


class JointAccountHoldersResponse(BaseSchema):
    id: str = Field(..., description="Mã đồng sở hữu")
    basic_information: BasicInformationResponse = Field(..., description="Thông tin cơ bản")
    identity_document: IdentityDocumentResponse = Field(..., description="Giấy tờ định danh")
    address_information: AddressInformationResponse = Field(..., description="Thông tin địa chỉ")


class SignatureAgreementAuthorResponse(BaseSchema):
    cif_number: str = CustomField(
        description="Mã định danh của đồng sở hữu"
    ).CIFNumberField
    full_name_vn: str = Field(..., description="Tên tiếng việt của đồng sở hữu")


class AgreementAuthorResponse(BaseSchema):
    id: str = Field(..., description="Mã danh mục thỏa thuận và uỷ quyền")
    code: str = Field(..., description="Code danh mục thỏa thuận và uỷ quyền")
    name: str = Field(..., description="Nội dung của danh mục thỏa thuận và uỷ quyền")
    agreement_flag: Optional[bool] = Field(
        ...,
        description="Thỏa thuận chữ ký các hồ sơ chứng từ.True: Có , False: Không",
    )
    method_sign: Optional[int] = Field(..., description="Phương thức ký")
    signature_list: Optional[List[SignatureAgreementAuthorResponse]] = Field(
        ..., description="Chữ ký của đồng sở hữu"
    )


class CoOwnerInfoResponse(BaseSchema):
    full_name_vn: str = Field(..., description="Tên tiếng việt của khách hàng")
    avatar_url: str = Field(..., description="Url ảnh đại diện của khách hàng")


class FileUuidInfoResponse(BaseSchema):
    uuid: str = Field(..., description="Uuid file")
    file_url: str = Field(..., description="Url của file")
    file_name: str = Field(..., description="Tên file")
    file_content_type: str = Field(..., description="Loại file")
    file_size: str = Field(..., description="Kích thước file")


class DocumentListResponse(BaseSchema):
    file_uuid: FileUuidInfoResponse = Field(..., description="Thông tin file")


class GetCoOwnerResponse(BaseSchema):
    joint_account_holder_flag: bool = Field(
        ..., description="Có đồng chủ sở hữu. `True`: Có , `False`: Không"
    )
    document_no: str = Field(..., description="Số văn bản")
    created_at: date = Field(..., description="Ngày lập")
    address_flag: bool = Field(..., description="Nơi lập")
    document_address: Optional[str] = Field(None, description="Thông tin địa chỉ file")
    file_uuid: Optional[FileUuidInfoResponse] = Field(None, description="Thông tin đồng sở hữu")
    number_of_joint_account_holder: int = Field(..., description="Số lượng đồng sở hữu")
    joint_account_holders: List[JointAccountHoldersResponse] = Field(..., description="Thông tin đồng sở hữu")
    agreement_authorization: List[AgreementAuthorResponse] = Field(
        ..., description="Danh mục thỏa thuận và ủy quyền"
    )


class ListCoOwnerResponse(BaseSchema):
    document_no: str = Field(..., description="Số văn bản")
    create_at: date = Field(..., description="Ngày lập")
    expiration_date: date = Field(..., description="Ngày hết hiệu lực")
    document_address: str = Field(..., description="Nơi lập")


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
    method_sign: int = Field(
        ...,
        description="Phương thức ký. "
                    "`1`: Chữ ký của tất cả các đồng sở hữu,"
                    "`2`: Chữ ký của một trong bất kỳ các đồng chủ tài khoản,"
                    "`3`: Chữ ký của các đồng chủ tài khoản sau")
    signature_list: Optional[List[SignatureAgreementAuthorRequest]] = Field(
        None, description="Chữ ký của đồng sở hữu"
    )


class AccountHolderRequest(BaseSchema):
    joint_account_holder_flag: bool = Field(
        ..., description="Có đồng chủ sở hữu. `True`: Có , `False`: Không"
    )
    document_no: str = Field(..., description="Số văn bản")
    created_at: date = Field(..., description="Ngày lập")
    address_flag: bool = Field(..., description="Nơi lập")
    document_address: Optional[str] = Field(None, description="Thông tin địa chỉ file")
    file_uuid: Optional[str] = Field(None, description="Tập tin đính kèm")
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
