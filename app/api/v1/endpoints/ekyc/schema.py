from datetime import date
from typing import Optional

from pydantic import Field, validator

from app.api.base.schema import BaseSchema
from app.settings.config import DATE_INPUT_OUTPUT_FORMAT
from app.utils.constant.ekyc import EKYC_DATE_FORMAT
from app.utils.functions import date_string_to_other_date_string_format


class CreateEKYCCustomerRequest(BaseSchema):
    date_of_issue: date = Field(...)
    date_of_birth: date = Field(...)
    transaction_id: Optional[str] = Field(...)
    document_id: str = Field(...)
    document_type: int = Field(...)
    date_of_expiry: date = Field(None)
    place_of_issue: str = Field(None)
    qr_code_data: str = Field(...)
    customer_id: Optional[str] = Field(..., description='Mã khách hàng (ekyc)')
    full_name: str = Field(...)
    gender: str = Field(...)
    place_of_residence: str = Field(...)
    place_of_origin: str = Field(...)
    nationality: str = Field(...)
    address_1: str = Field(...)
    address_2: str = Field(...)
    address_3: str = Field(...)
    address_4: str = Field(...)
    permanent_address: dict = Field(...)
    phone_number: str = Field(...)
    ocr_data: dict = Field(...)
    ocr_data_errors: dict = Field(...)
    faces_matching_percent: Optional[float] = Field(...)
    extra_info: Optional[dict] = Field(...)
    receive_ads: bool = Field(...)
    longitude: Optional[float] = Field(...)
    latitude: Optional[float] = Field(...)
    cif: str = Field(...)
    account_number: str = Field(...)
    job_title: str = Field(...)
    organization: str = Field(...)
    organization_address: str = Field(...)
    organization_phone_number: str = Field(...)
    position: str = Field(...)
    salary_range: str = Field(...)
    tax_number: str = Field(...)
    open_biometric: bool = Field(...)
    avatar_image_url: str = Field(...)
    avatar_image_uri: str = Field(...)
    attachment_info: Optional[list] = Field(...)
    finger_ids: Optional[list] = Field(...)
    face_ids: Optional[list] = Field(...)
    ekyc_level: str = Field(...)
    ekyc_step: Optional[list] = Field(...)
    kss_status: str = Field(...)
    status: str = Field(...)

    @validator('*', pre=True)
    def check_date(cls, v):
        value = date_string_to_other_date_string_format(
            v,
            from_format=EKYC_DATE_FORMAT,
            to_format=DATE_INPUT_OUTPUT_FORMAT
        )
        if value:
            return value
        return v


class CreateEKYCCustomerResponse(BaseSchema):
    customer_id: str = Field(..., description='Mã khách hàng (ekyc)')
