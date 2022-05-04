from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.cif import AddressRequest
from app.api.v1.schemas.utils import DropdownRequest

########################################################################################################################
# request detail giấy tờ định danh
########################################################################################################################


# Thông tin dùng chung
########################################################################################################################
# I. Thông tin mặt trước CMND, CCCD
class FrontSideIdentityCitizenCardRequest(BaseSchema):
    identity_image_url: str = Field(..., min_length=1, description="URL hình ảnh mặt trước CMND/CCCD")
    identity_avatar_image_uuid: str = Field(..., min_length=1, description="Hình ảnh khuôn mặt CMND/CCCD")
    face_compare_image_url: str = Field(..., min_length=1, description="Hình ảnh chụp khuôn mặt")
    face_uuid_ekyc: str = Field(..., min_length=1, description="uuid lấy từ so sánh khuôn mặt")


# II. Thông tin mặt sau CMND, CCCD
class BackSideIdentityCitizenCardRequest(BaseSchema):
    identity_image_url: str = Field(..., min_length=1, description="URL hình ảnh mặt sau CMND/CCCD")


# III. Phân tích OCR -> 3. Thông tin địa chỉ CMND, CCCD
class OCRAddressIdentityCitizenCardRequest(BaseSchema):  # noqa
    resident_address: AddressRequest = Field(..., description="Nơi thường trú")
    contact_address: AddressRequest = Field(..., description="Địa chỉ liên hệ")


class CifInformationRequest(BaseSchema):
    self_selected_cif_flag: bool = Field(..., description='Cờ CIF thông thường/ tự chọn. '
                                                          '`False`: thông thường. '
                                                          '`True`: tự chọn')
    cif_number: Optional[str] = CustomField(description='Số CIF yêu cầu').OptionalCIFNumberField
    customer_classification: DropdownRequest = Field(..., description='Đối tượng khách hàng')
    customer_economic_profession: DropdownRequest = Field(..., description='Mã ngành KT')


########################################################################################################################
# Giấy tờ định danh - CMND
########################################################################################################################
# III. Phân tích OCR -> 1. Giấy tờ định danh (CMND)
class OCRDocumentIdentityCardRequest(BaseSchema):
    identity_number: str = Field(..., min_length=1, description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")


# III. Phân tích OCR -> 2. Thông tin cơ bản (CMND)
class OCRBasicInfoIdentityCardRequest(BaseSchema):
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên")
    gender: DropdownRequest = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    province: DropdownRequest = Field(..., description="Quê quán")
    ethnic: DropdownRequest = Field(None, description="Dân tộc")  # CMND
    religion: DropdownRequest = Field(None, description="Tôn giáo")  # CMND
    identity_characteristic: str = Field(None, description="Đặc điểm nhận dạng")  # CMND
    father_full_name_vn: str = Field(None, description="Họ tên cha")  # CMND
    mother_full_name_vn: str = Field(None, description="Họ tên mẹ")  # CMND


# III. Phân tích OCR (CMND)
class OCRResultIdentityCardRequest(BaseSchema):  # noqa
    identity_document: OCRDocumentIdentityCardRequest = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInfoIdentityCardRequest = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardRequest = Field(..., description="Thông tin địa chỉ")


# REQUEST CMND
class IdentityDocumentTypeRequest(BaseSchema):
    id: str = Field(..., min_length=1, description="""Chuỗi định danh chấp nhận các giá trị tương ứng sau:
        \n`HO_CHIEU` : Hộ Chiếu.
        \n`CMND` : Chứng Minh Nhân Dân.
        \n`CCCD` : Căn Cước Công Dân.""")
    type_id: int = Field(..., description="""Loại GTDD trả về là loại giấy tờ đã được server phân loại,
    và có các giá trị tương ứng như sau:
        \n`0` : Hộ chiếu.
        \n`1` : Chứng minh nhân dân cũ (9 số).
        \n`2` : Chứng minh nhân dân mới (12 số).
        \n`3` : Căn cước công dân cũ (không gắn chíp).
        \n`4` : Căn cước công dân mới (có gắn chíp). """)


class IdentityCardSaveRequest(BaseSchema):
    cif_id: str = Field(None, description="ID định danh CIF")
    cif_information: CifInformationRequest = Field(..., description="Thông tin CIF")
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt trước")
    back_side_information: BackSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultIdentityCardRequest = Field(..., description="Phân tích OCR")


########################################################################################################################
# Giấy tờ định danh - CCCD
########################################################################################################################

# III. Phân tích OCR -> 1. Giấy tờ định danh (CCCD)
class OCRDocumentCitizenCardRequest(BaseSchema):  # noqa
    identity_number: str = Field(..., min_length=1, description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    mrz_content: str = Field(None, min_length=90, max_length=90, description="MRZ")  # CCCD
    qr_code_content: str = Field(None, description="Nội dung QR Code")  # CCCD
    signer: str = Field(..., description="Người ký")


# III. Phân tích OCR -> 2. Thông tin cơ bản (CCCD)
class OCRBasicInfoCitizenCardRequest(BaseSchema):
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên")
    gender: DropdownRequest = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownRequest = Field(None, description="Quốc tịch")
    province: DropdownRequest = Field(..., description="Quê quán")
    identity_characteristic: str = Field(..., min_length=1, description="Đặc điểm nhận dạng")


# III. Phân tích OCR -> 3. Thông tin địa chỉ (CCCD)
class OCRResultCitizenCardRequest(BaseSchema):  # noqa
    identity_document: OCRDocumentCitizenCardRequest = Field(..., description="Giấy tờ định danh")
    basic_information: OCRBasicInfoCitizenCardRequest = Field(..., description="Thông tin cơ bản")
    address_information: OCRAddressIdentityCitizenCardRequest = Field(..., description="Thông tin địa chỉ")


# REQUEST CCCD
class CitizenCardSaveRequest(BaseSchema):
    cif_id: str = Field(None, description="ID định danh CIF")  # noqa
    cif_information: CifInformationRequest = Field(..., description="Thông tin CIF")
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Loại giấy tờ định danh")
    front_side_information: FrontSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt trước")
    back_side_information: BackSideIdentityCitizenCardRequest = Field(..., description="Thông tin mặt sau")
    ocr_result: OCRResultCitizenCardRequest = Field(..., description="Phân tích OCR")


########################################################################################################################
# Giấy tờ định danh - Hộ chiếu
########################################################################################################################

# I. Thông tin Hộ chiếu
class InformationPassportRequest(BaseSchema):
    identity_image_url: str = Field(..., min_length=1, description="URL hình ảnh Hộ chiếu")
    identity_avatar_image_uuid: str = Field(..., min_length=1, description="Hình ảnh khuôn mặt Hộ chiếu")
    face_compare_image_url: str = Field(..., min_length=1, description="Hình ảnh chụp khuôn mặt")
    face_uuid_ekyc: str = Field(..., min_length=1, description="uuid lấy từ so sánh khuôn mặt")


# II. Phân tích OCR -> 1. Giấy tờ định danh (Hộ Chiếu)
class OCRDocumentPassportRequest(BaseSchema):  # noqa
    identity_number: str = Field(..., min_length=1, description="Số GTĐD")
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    passport_type: DropdownRequest = Field(..., description="Loại")
    passport_code: DropdownRequest = Field(..., description="Mã số")


# II. Phân tích OCR -> 2. Thông tin cơ bản (Hộ Chiếu)
class BasicInfoPassportRequest(BaseSchema):
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên")
    gender: DropdownRequest = Field(..., description="Giới tính")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownRequest = Field(..., description="Quốc tịch")
    place_of_birth: DropdownRequest = Field(..., description="Nơi sinh")
    identity_card_number: str = Field(..., min_length=1, description="Số CMND")
    mrz_content: str = Field(None, min_length=88, max_length=88, description="Mã MRZ")


# II. Phân tích OCR (HC)
class OCRResultPassportRequest(BaseSchema):
    identity_document: OCRDocumentPassportRequest = Field(..., description="Giấy tờ định danh")
    basic_information: BasicInfoPassportRequest = Field(..., description="Thông tin cơ bản")


# REQUEST HC
class PassportSaveRequest(BaseSchema):
    cif_id: str = Field(None, description="ID định danh CIF")
    cif_information: CifInformationRequest = Field(..., description="Thông tin CIF")
    identity_document_type: IdentityDocumentTypeRequest = Field(..., description="Loại giấy tờ định danh")
    passport_information: InformationPassportRequest = Field(..., description="Thông tin hộ chiếu")
    ocr_result: OCRResultPassportRequest = Field(..., description="Phân tích OCR")


########################################################################################################################
# Others
########################################################################################################################
# So sánh khuôn mặt
class FaceCompareRequest(BaseSchema):
    face_image_url: str = Field(..., min_length=1, description="URL hình ảnh khuôn mặt đối chiếu")


class OcrEkycRequest(BaseSchema):
    document_type: int = Field(..., description='Loại giấy tờ tùy thân được lấy từ ocr_result_ekyc')
    data: dict = Field(..., description='thông tin ocr_result_ekyc (cả 2 mặt) của giấy tờ tùy thân')
