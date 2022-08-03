from datetime import date, datetime
from typing import Optional, List

from pydantic import Field, validator

from app.api.base.schema import BaseSchema
from app.settings.config import DATE_INPUT_OUTPUT_FORMAT
from app.utils.constant.ekyc import EKYC_DATE_FORMAT
from app.utils.functions import date_string_to_other_date_string_format


class InfoStep(BaseSchema):
    step: str = Field(...)
    step_status: str = Field(...)
    update_at: datetime = Field(...)
    reason: str = Field(None)
    start_date: date = Field(None)
    end_date: date = Field(None)


class EKYCStep(BaseSchema):
    transaction_id: str = Field(...)
    info_step: List[InfoStep] = Field(...)


class CreateEKYCCustomerRequest(BaseSchema):
    customer_id: Optional[str] = Field(..., description='Mã khách hàng (ekyc)')
    transaction_id: Optional[str] = Field(None)
    date_of_issue: Optional[date] = Field(None)
    date_of_birth: Optional[date] = Field(None)
    document_id: Optional[str] = Field(None)
    document_type: Optional[int] = Field(None)
    date_of_expiry: Optional[date] = Field(None)
    place_of_issue: Optional[str] = Field(None)
    qr_code_data: Optional[str] = Field(None)
    full_name: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)
    place_of_residence: Optional[str] = Field(None)
    place_of_origin: Optional[str] = Field(None)
    nationality: Optional[str] = Field(None)
    address_1: Optional[str] = Field(None)
    address_2: Optional[str] = Field(None)
    address_3: Optional[str] = Field(None)
    address_4: Optional[str] = Field(None)
    permanent_address: Optional[dict] = Field(None)
    phone_number: Optional[str] = Field(None)
    ocr_data: Optional[dict] = Field(None)
    ocr_data_errors: Optional[dict] = Field(None)
    faces_matching_percent: Optional[float] = Field(None)
    extra_info: Optional[dict] = Field(None)
    receive_ads: Optional[bool] = Field(None)
    longitude: Optional[float] = Field(None)
    latitude: Optional[float] = Field(None)
    cif: Optional[str] = Field(None)
    account_number: Optional[str] = Field(None)
    job_title: Optional[str] = Field(None)
    organization: Optional[str] = Field(None)
    organization_address: Optional[str] = Field(None)
    organization_phone_number: Optional[str] = Field(None)
    position: Optional[str] = Field(None)
    salary_range: Optional[str] = Field(None)
    tax_number: Optional[str] = Field(None)
    open_biometric: Optional[bool] = Field(None)
    avatar_image_url: Optional[str] = Field(None)
    avatar_image_uri: Optional[str] = Field(None)
    attachment_info: Optional[list] = Field(None)
    finger_ids: Optional[list] = Field(None)
    face_ids: Optional[list] = Field(None)
    ekyc_level: Optional[str] = Field(None)
    ekyc_step: Optional[List[EKYCStep]] = Field(None)
    kss_status: Optional[str] = Field(None)
    status: Optional[str] = Field(None)
    user_eb: Optional[str] = Field(None, description="Username Ebanking")

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

    @validator('*')
    def check_blank_str(cls, v):
        if v == '':
            return None
        return v


class CreateEKYCCustomerResponse(BaseSchema):
    customer_id: Optional[str] = Field(..., description='Mã khách hàng (ekyc)')
