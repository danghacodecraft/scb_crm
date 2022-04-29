from datetime import date

from pydantic import Field
from pydantic.class_validators import Optional

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.cif import AddressRequest
from app.api.v1.schemas.utils import DropdownRequest


class FrontSideIdentityCitizenCardRequest(BaseSchema):
    identity_image_url: str = Field(..., description="url hình ảnh mặt trước CMND/CCCD")
    identity_avatar_image_uuid: str = Field(..., description="Hình ảnh khuôn mặt")
    face_compare_image_url: str = Field(..., description="Hình ảnh chụp khuôn mặt")
    face_uuid_ekyc: str = Field(..., description="uuid lấy từ so sánh khuôn mặt")


class BackSideIdentityCitizenCardRequest(BaseSchema):
    identity_image_url: str = Field(..., description="url hình ảnh mặt sau CMND/CCCD")


class OCRAddressIdentityCitizenCardRequest(BaseSchema):
    resident_address: AddressRequest = Field(..., description="Địa chỉ thường trú")
    contact_address: AddressRequest = Field(..., description="Địa chỉ liên lạc")


class CifInformationRequest(BaseSchema):
    self_selected_cif_flag: bool = Field(..., description="Cờ CIF thông thường/ tự chọn")
    cif_number: Optional[str] = CustomField(description='Số CIF yêu cầu').OptionalCIFNumberField
    customer_classification: DropdownRequest = Field(..., description="Đối tượng khách hàng")
    customer_economic_profession: DropdownRequest = Field(..., description="Mã ngành KT")


#######################################################################################################################
# CMND
#######################################################################################################################
# III. OCR -> CMND
class OCRDocumentIdentityCardRequest(BaseSchema):
    identity_number: str = Field(..., description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")


class OCRBasicInformationIdentityCardRequest(BaseSchema):
    full_name_vn: str = Field(..., description="Họ và tên")
    gender: DropdownRequest = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    province: DropdownRequest = Field(..., description="Quê quán")
    ethnic: DropdownRequest = Field(..., description="Dân tộc")
    region: DropdownRequest = Field(..., description="Tôn giáo")
    identity_characteristic: str = Field(..., description="Đặc điểm nhận dạng")
    father_fullname_vn: str = Field(..., description="Họ tên cha")
    mother_fullname: str = Field(..., description="Họ tên mẹ")


class OCRResultIdentityCardRequest(BaseSchema):
    identity_document: OCRDocumentIdentityCardRequest = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInformationIdentityCardRequest = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardRequest = Field(..., description="Thông tin địa chỉ")


class IdentityDocumentTypeRequest(BaseSchema):
    id: str = Field(..., description="Chuỗi định danh: CMND, CCCD, HC")
    type_id: int = Field(..., description="""
        \n`0`: Hộ chiếu.
        \n`1`: CMND cũ (9 số).
        \n`2`: CMND mới (12 số).
        \n`3`: CCCD cũ (không gắn chíp).
        \n`4`: CCCD mới (có gắn chíp).
    """)


class IdentityCardSaveRequest(BaseSchema):
    cif_id: str = Field(None, description="ID định danh cif")
    cif_information: CifInformationRequest = Field(..., description="Thông tin CIF")
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt trước")
    back_side_information: BackSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultIdentityCardRequest = Field(..., description="Phân tích OCR")


#######################################################################################################################
# CCCD
#######################################################################################################################
# III. OCR -> CCCD
class OCRDocumentCitizenCardRequest(BaseSchema):
    identity_number: str = Field(..., description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    mrz_content: str = Field(..., description="MRZ")
    qr_code_content: str = Field(..., description="Nội dung QR code")


class OCRBasicInformationCitizenCardRequest(BaseSchema):
    full_name_vn: str = Field(..., description="Họ và tên")
    gender: DropdownRequest = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    province: DropdownRequest = Field(..., description="Quê quán")
    identity_characteristic: str = Field(..., description="Đặc điểm nhận dạng")


class OCRResultCitizenCardRequest(BaseSchema):
    identity_document: OCRDocumentCitizenCardRequest = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInformationCitizenCardRequest = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardRequest = Field(..., description="Thông tin địa chỉ")


class CitizenCardSaveRequest(BaseSchema):
    cif_id: str = Field(None, description="ID định danh cif")
    cif_information: CifInformationRequest = Field(..., description="Thông tin CIF")
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt trước")
    back_side_information: BackSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultCitizenCardRequest = Field(..., description="Phân tích OCR")


# #####################################################################################################################
# Passport
# #####################################################################################################################
class InformationPassportRequest(BaseSchema):
    identity_image_url: str = Field(..., description="URL hình ảnh hộ chiếu")
    identity_avatar_image_uuid: str = Field(..., description="Hình ảnh khuôn mặt hộ chiếu")
    face_compare_image_url: str = Field(..., description="Hình ảnh chụp khuôn mặt")
    face_uuid_ekyc: str = Field(..., description="uuid lấy từ so sánh khuôn mặt")


class OCRDocumentPassportRequest(BaseSchema):
    identity_number: str = Field(..., description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    passport_type: DropdownRequest = Field(..., description="Loại")
    passport_code: DropdownRequest = Field(..., description="Mã số")


class OCRBasicInformationPassportRequest(BaseSchema):
    full_name_vn: str = Field(..., description="Họ và tên")
    gender: DropdownRequest = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    place_of_birth: DropdownRequest = Field(..., description="Nơi sinh")
    identity_card_number: str = Field(..., description="Số CMND")
    mrz_code: str = Field(..., description="Mã MRZ")


class OCRResultPassportRequest(BaseSchema):
    identity_document: OCRDocumentPassportRequest = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInformationPassportRequest = Field(..., description="Thông tin cơ bản")


class PassportSaveRequest(BaseSchema):
    cif_id: str = Field(..., description="ID định danh cif")
    cif_information: CifInformationRequest = Field(..., description="Thông tin CIF")
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Loại giấy tờ định danh")
    passport_information: InformationPassportRequest = Field(..., description="Thông tin hộ chiếu")
    ocr_result: OCRResultPassportRequest = Field(..., description="Phân tích OCR")


class FaceCompareRequest(BaseSchema):
    face_image_url: str = Field(..., description="Url hình ảnh khuôn mặt đối chiếu")
