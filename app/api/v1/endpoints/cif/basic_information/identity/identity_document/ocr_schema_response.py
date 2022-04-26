from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse

# Thông tin dùng chung
########################################################################################################################


# I. Thông tin mặt trước CMND, CCCD
class FrontSideIdentityCitizenCardResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh mặt trước CMND/CCCD")
    identity_avatar_image_uuid: Optional[str] = Field(
        ..., description="Hình ảnh chân dung trên GTĐD dùng để so sánh với khuôn mặt"
    )


class AddressResponse(BaseSchema):
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/Thành phố", nullable=True)
    district: OptionalDropdownResponse = Field(..., description="Quận/Huyện", nullable=True)
    ward: OptionalDropdownResponse = Field(..., description="Phường/Xã", nullable=True)
    number_and_street: Optional[str] = Field(..., description="Số nhà, tên đường", nullable=True)


# III. Phân tích OCR -> 3. Thông tin địa chỉ CMND, CCCD
class OCRAddressIdentityCitizenCardResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Nơi thường trú")
    contact_address: AddressResponse = Field(..., description="Địa chỉ liên hệ")


########################################################################################################################
# Giấy tờ định danh - CMND
########################################################################################################################
# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class OCRFrontSideDocumentIdentityCardResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số GTĐD", nullable=True)
    expired_date: Optional[date] = Field(..., description="Có giá trị đến", nullable=True)


# III. Phân tích OCR -> 2. Thông tin cơ bản (CMND)
class OCRFrontSideBasicInfoIdentityCardResponse(BaseSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên", nullable=True)
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh", nullable=True)
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    province: OptionalDropdownResponse = Field(..., description="Quê quán", nullable=True)


# III. Phân tích OCR (CMND)
class OCRResultFrontSideIdentityCardResponse(BaseSchema):
    identity_document: OCRFrontSideDocumentIdentityCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRFrontSideBasicInfoIdentityCardResponse = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardResponse = Field(..., description="Thông tin địa chỉ")


# RESPONSE CMND
class OCRFrontSideIdentityCardResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt trước")
    ocr_result: OCRResultFrontSideIdentityCardResponse = Field(...,
                                                               description="Phân tích OCR thông tin mặt trước CMND")


class BackSideIdentityCardResponse(BaseSchema):
    identity_image_url: Optional[str] = Field(..., description="URL hình ảnh mặt sau CMND", nullable=True)


class OCRBackSideIdentityDocumentIdentityCardResponse(BaseSchema):
    issued_date: Optional[date] = Field(..., description="Ngày cấp", nullable=True)
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp", nullable=True)


class OCRBackSideBasicInformationIdentityCardResponse(BaseSchema):
    ethnic: OptionalDropdownResponse = Field(..., description="Dân tộc", nullable=True)
    religion: OptionalDropdownResponse = Field(..., description="Tôn giáo", nullable=True)
    identity_characteristic: Optional[str] = Field(..., description="Đặc điểm nhận dạng", nullable=True)


class OCRResultBackSideIdentityCardResponse(BaseSchema):
    identity_document: OCRBackSideIdentityDocumentIdentityCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBackSideBasicInformationIdentityCardResponse = Field(..., description="Thông tin cơ bản")


class OCRBackSideIdentityCardResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    back_side_information: BackSideIdentityCardResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultBackSideIdentityCardResponse = Field(..., description="Phân tích OCR mặt sau CMND")


########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################

# I. Thông tin Hộ chiếu
class InformationPassportResponse(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh Hộ chiếu")
    identity_avatar_image_uuid: Optional[str] = Field(
        ..., description="Hình ảnh chân dung trên GTĐD dùng để so sánh với khuôn mặt"
    )


# II. Phân tích OCR -> 1. Giấy tờ định danh (Hộ Chiếu)
class OCRDocumentPassportResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số GTĐD", nullable=True)
    issued_date: Optional[date] = Field(..., description="Ngày cấp", nullable=True)
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp", nullable=True)
    expired_date: Optional[date] = Field(..., description="Có giá trị đến", nullable=True)
    passport_type: OptionalDropdownResponse = Field(..., description="Loại", nullable=True)
    passport_code: OptionalDropdownResponse = Field(..., description="Mã số", nullable=True)


# II. Phân tích OCR -> 2. Thông tin cơ bản (Hộ Chiếu)
class OCRBasicInfoPassportResponse(BaseSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên", nullable=True)
    gender: OptionalDropdownResponse = Field(..., description="Giới tính", nullable=True)
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh", nullable=True)
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch", nullable=True)
    place_of_birth: OptionalDropdownResponse = Field(..., description="Nơi sinh", nullable=True)
    identity_card_number: Optional[str] = Field(..., description="Số CMND", nullable=True)
    mrz_content: Optional[str] = Field(None, description="Mã MRZ", nullable=True)


# II. Phân tích OCR (HC)
class OCRResultPassportResponse(BaseSchema):
    identity_document: OCRDocumentPassportResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInfoPassportResponse = Field(..., description="Thông tin cơ bản")


# RESPONSE HC
class OCRPassportResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    passport_information: InformationPassportResponse = Field(..., description="Thông tin hộ chiếu")
    ocr_result: OCRResultPassportResponse = Field(..., description="Phân tích OCR")


########################################################################################################################

########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################

# III. Phân tích OCR (CCCD) -> Giấy tờ định danh
class OCRFrontSideDocumentCitizenCardResponse(OCRFrontSideDocumentIdentityCardResponse):
    expired_date: Optional[date] = Field(..., description="Có giá trị đến", nullable=True)


# III. Phân tích OCR (CCCD) -> Thông tin cơ bản
class OCRFrontSideBasicInfoCitizenCardResponse(OCRFrontSideBasicInfoIdentityCardResponse):
    gender: OptionalDropdownResponse = Field(..., description="Giới tính", nullable=True)


# III. Phân tích OCR (CCCD)
class OCRResultFrontSideCitizenCardResponse(BaseSchema):
    identity_document: OCRFrontSideDocumentCitizenCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRFrontSideBasicInfoCitizenCardResponse = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardResponse = Field(..., description="Thông tin địa chỉ")


class OCRFrontSideCitizenCardResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt trước")
    ocr_result: OCRResultFrontSideCitizenCardResponse = Field(...,
                                                              description="Phân tích OCR thông tin mặt trước CCCD")


class BackSideCitizenCardResponse(BaseSchema):
    identity_image_url: Optional[str] = Field(..., description="URL hình ảnh mặt sau CMND", nullable=True)


class OCRBackSideIdentityDocumentCitizenCardResponse(BaseSchema):
    issued_date: Optional[date] = Field(..., description="Ngày cấp", nullable=True)
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp", nullable=True)
    mrz_content: Optional[str] = Field(..., description="Mã MRZ", nullable=True)
    signer: Optional[str] = Field(..., description="Người ký", nullable=True)


class OCRBackSideBasicInformationCitizenCardResponse(BaseSchema):
    identity_characteristic: Optional[str] = Field(..., description="Đặc điểm nhận dạng", nullable=True)


class OCRResultBackSideCitizenCardResponse(BaseSchema):
    identity_document: OCRBackSideIdentityDocumentCitizenCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBackSideBasicInformationCitizenCardResponse = Field(..., description="Thông tin cơ bản")


class OCRBackSideCitizenCardResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    back_side_information: BackSideCitizenCardResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultBackSideCitizenCardResponse = Field(..., description="Phân tích OCR mặt sau CCCD")
########################################################################################################################


########################################################################################################################
# So sánh khuôn mặt đối chiếu với khuôn mặt trên giấy tờ định danh
########################################################################################################################
class CompareSuccessResponse(BaseSchema):
    similar_percent: int = Field(
        ...,
        description="Tỉ lệ chính xác giữa khuôn mặt đối chiếu với khuôn mặt trên giấy tờ định danh"
    )
    face_uuid_ekyc: str = Field(..., description="uuid của `face_image` trả về từ hệ thống eKYC, "
                                                 "dùng để lưu trong API `Lưu Giấy tờ định danh`")
