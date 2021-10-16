from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import (
    CustomerClassification, CustomerEconomicProfession, KYCLevel
)


class CifInformationRes(BaseSchema):
    self_selected_cif_flag: bool = Field(..., description='Cờ CIF thông thường/ tự chọn. '
                                                          '`False`: thông thường. '
                                                          '`True`: tự chọn')
    cif_number: str = Field(..., description='Số CIF yêu cầu')
    customer_classification: CustomerClassification = Field(..., description='Đối tượng khách hàng')
    customer_economic_profession: CustomerEconomicProfession = Field(..., description='Mã ngành KT')
    kyc_level: KYCLevel = Field(..., description='Cấp độ KYC')
