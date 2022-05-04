from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import AddressResponse, FingerPrintResponse
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse

########################################################################################################################
# response detail giấy tờ định danh
########################################################################################################################


# Thông tin dùng chung
########################################################################################################################
# I. Thông tin mặt trước CMND, CCCD
class FrontSideIdentityCitizenCardResponse(BaseSchema):
    identity_image_url: str = Field(..., min_length=1, description="URL hình ảnh mặt trước CMND/CCCD")
    face_compare_image_url: str = Field(..., min_length=1, description="Hình ảnh chụp khuôn mặt")
    identity_avatar_image_uuid: str = Field(..., description='Hình ảnh khuôn mặt CMND/CCCD')
    face_uuid_ekyc: str = Field(..., description='uuid lấy từ so sánh khuôn mặt')
    similar_percent: int = Field(..., description="Tỉ lệ so khớp với Hình ảnh chụp khuôn mặt")


# II. Thông tin mặt sau CMND, CCCD
class BackSideIdentityCitizenCardResponse(BaseSchema):
    identity_image_url: str = Field(..., min_length=1, description="URL hình ảnh mặt sau CMND/CCCD")
    fingerprint: List[FingerPrintResponse] = Field(..., description="Vân tay")
    updated_at: datetime = Field(..., description='Cập nhật vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
                                 example='2021-15-12 06:07:08')
    updated_by: str = Field(..., min_length=1, description="Người cập nhật")


# III. Phân tích OCR -> 3. Thông tin địa chỉ CMND, CCCD
class OCRAddressIdentityCitizenCardResponse(BaseSchema):  # noqa
    resident_address: AddressResponse = Field(..., description="Nơi thường trú")
    contact_address: AddressResponse = Field(..., description="Địa chỉ liên hệ")


########################################################################################################################
# Giấy tờ định danh - CMND
########################################################################################################################
# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class OCRDocumentIdentityCardResponse(BaseSchema):
    identity_number: str = Field(..., min_length=1, description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")


# III. Phân tích OCR -> 2. Thông tin cơ bản (CMND)
class OCRBasicInfoIdentityCardResponse(BaseSchema):
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên")
    gender: DropdownResponse = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    province: DropdownResponse = Field(..., description="Quê quán")
    ethnic: DropdownResponse = Field(None, description="Dân tộc")  # CMND
    religion: DropdownResponse = Field(None, description="Tôn giáo")  # CMND
    identity_characteristic: str = Field(None, description="Đặc điểm nhận dạng")  # CMND
    father_full_name_vn: str = Field(None, description="Họ tên cha")  # CMND
    mother_full_name_vn: str = Field(None, description="Họ tên mẹ")  # CMND


# III. Phân tích OCR (CMND)
class OCRResultIdentityCardResponse(BaseSchema):  # noqa
    identity_document: OCRDocumentIdentityCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInfoIdentityCardResponse = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardResponse = Field(..., description="Thông tin địa chỉ")


# RESPONSE CMND
class IdentityCardDetailResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt trước")
    back_side_information: BackSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultIdentityCardResponse = Field(..., description="Phân tích OCR")


########################################################################################################################
# Giấy tờ định danh - CCCD
########################################################################################################################

# III. Phân tích OCR -> 1. Giấy tờ định danh (CCCD)
class OCRDocumentCitizenCardResponse(BaseSchema):
    identity_number: str = Field(..., min_length=1, description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")
    mrz_content: str = Field(None, description="MRZ")  # CCCD
    qr_code_content: str = Field(None, description="Nội dung QR Code")  # CCCD
    signer: Optional[str] = Field(None, description="Người ký")  # CCCD


# III. Phân tích OCR -> 2. Thông tin cơ bản (CCCD)
class OCRBasicInfoCitizenCardResponse(BaseSchema):
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    province: OptionalDropdownResponse = Field(..., description="Quê quán")
    identity_characteristic: str = Field(..., min_length=1, description="Đặc điểm nhận dạng")


# III. Phân tích OCR -> 3. Thông tin địa chỉ (CCCD)
class OCRResultCitizenCardResponse(BaseSchema):  # noqa
    identity_document: OCRDocumentCitizenCardResponse = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInfoCitizenCardResponse = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardResponse = Field(..., description="Thông tin địa chỉ")


# RESPONSE CCCD
class CitizenCardDetailResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt trước")
    back_side_information: BackSideIdentityCitizenCardResponse = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultCitizenCardResponse = Field(..., description="Phân tích OCR")


########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################

# I. Thông tin Hộ chiếu
class InformationPassportResponse(BaseSchema):
    identity_image_url: str = Field(..., min_length=1, description="URL hình ảnh Hộ chiếu")
    face_compare_image_url: str = Field(..., min_length=1, description="Hình ảnh chụp khuôn mặt")
    identity_avatar_image_uuid: str = Field(..., description="Hình ảnh khuôn mặt Hộ chiếu ")
    face_uuid_ekyc: str = Field(..., description='uuid lấy từ so sánh khuôn mặt')
    similar_percent: int = Field(..., description="Tỉ lệ so khớp với Hình ảnh chụp khuôn mặt")
    fingerprint: List[FingerPrintResponse] = Field(..., description="Danh sách các vân tay đối chiếu")


# II. Phân tích OCR -> 1. Giấy tờ định danh (Hộ Chiếu)
class OCRDocumentPassportResponse(BaseSchema):
    identity_number: str = Field(..., min_length=1, description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    passport_type: OptionalDropdownResponse = Field(..., description="Loại")
    passport_code: OptionalDropdownResponse = Field(..., description="Mã số")


# II. Phân tích OCR -> 2. Thông tin cơ bản (Hộ Chiếu)
class BasicInfoPassportResponse(BaseSchema):
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    place_of_birth: OptionalDropdownResponse = Field(..., description="Nơi sinh")
    identity_card_number: str = Field(..., min_length=1, description="Số CMND")
    mrz_content: str = Field(None, description="Mã MRZ")


# II. Phân tích OCR (HC)
class OCRResultPassportResponse(BaseSchema):
    identity_document: OCRDocumentPassportResponse = Field(..., description="Giấy tờ định danh")
    basic_information: BasicInfoPassportResponse = Field(..., description="Thông tin cơ bản")


# RESPONSE HC
class PassportDetailResponse(BaseSchema):
    identity_document_type: DropdownResponse = Field(..., description="Loại giấy tờ định danh")
    passport_information: InformationPassportResponse = Field(..., description="Thông tin hộ chiếu")
    ocr_result: OCRResultPassportResponse = Field(..., description="Phân tích OCR")


########################################################################################################################


########################################################################################################################
# Response Lịch sử thay đổi giấy tờ định danh
########################################################################################################################
class IdentityImage(BaseSchema):
    image_url: str = Field(..., min_length=1, description="URL hình ảnh định danh")


class LogResponse(BaseSchema):
    reference_flag: bool = Field(..., description="Cờ giấy tờ định danh dùng để so sánh với hình gốc")
    created_date: date = Field(..., description="Ngày ghi log")
    identity_images: List[IdentityImage] = Field(..., description="Danh sách hình ảnh")


########################################################################################################################
# Response Validate ekyc
########################################################################################################################
class ValidateResponse(BaseSchema):
    success: bool = Field(..., description='Trạng thái validate ekyc')
    warning: dict = Field(..., description='Cảnh báo các trường đang không đúng với validate')
