from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import IndirectSaleStaffResponse, SaleStaffResponse


class OtherInformationResponse(BaseSchema):
    legal_agreement_flag: bool = Field(..., description="cờ thỏa thuận pháp lý `True`: có , `False`: không ")
    advertising_marketing_flag: bool = Field(..., description="Cờ đồng ý nhận SMS, Email tiếp thị quảng cáo từ SCB."
                                                              "`True`: có,"
                                                              "False: không."
                                             )
    sale_staff: SaleStaffResponse = Field(..., description="Mã nhân viên kinh doanh")
    indirect_sale_staff: IndirectSaleStaffResponse = Field(..., description="Mã nhân viên kinh doanh gián tiếp")
