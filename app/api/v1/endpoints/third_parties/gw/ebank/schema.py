from pydantic import Field

from app.api.base.schema import BaseSchema


class CifInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số CIF")


class GWRetrieveEbankByCIFNumberRequest(BaseSchema):
    cif_info: CifInfoRequest = Field(..., description="Dữ liệu đầu vào")


class EbankInfoItemResponse(BaseSchema):
    ebank_name: str = Field(..., description="Tên dịch vụ ebank")
    ebank_status: str = Field(..., description="Trạng thái dịch vụ ebank")


class GWRetrieveEbankByCIFNumberResponse(BaseSchema):
    ebank_info_item: EbankInfoItemResponse = Field(..., description="Thông tin Ebank")
