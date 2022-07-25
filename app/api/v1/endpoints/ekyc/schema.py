from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema


class CreateEKYCCustomerRequest(BaseSchema):
    customer_id: str = Field(..., description='Mã khách hàng (ekyc)')
    transaction_id: str = Field(..., description="Mã giao dịch")
    full_name: str = Field(..., description="Họ và tên khách hàng")
    cif: str = Field(None, description="Số CIF")
    phone_number: str = Field(..., description="Số điện thoại")
    document_id: str = Field(..., description="Số GTDD")
    document_type: int = Field(..., description="Loại giấy tờ")
    status: str = Field(..., description="Trạng thái")
    status_id: int = Field(..., description="ID Trạng thái")
    trans_date: date = Field(..., description="Ngày giao dịch")
    ekyc_step: str = Field(..., description="Nghiệp vụ")
    kss_status: str = Field(..., description="Trạng thái kiểm soát sau")
    kss_status_id: int = Field(..., description="ID Trạng thái kiểm soát sau")
    date_kss: date = Field(..., description="Ngày kiểm soát sau")
    user_kss: str = Field(..., description="Người kiểm soát sau")
    approve_status: str = Field(..., description="Trạng thái phê duyệt")
    approve_status_id: int = Field(..., description="ID Trạng thái phê duyệt")
    date_approve: date = Field(..., description="Ngày phê duyệt")
    user_approve: str = Field(..., description="Người phê duyệt")
    created_date: date = Field(..., description="Ngày tạo")
    updated_date: date = Field(..., description="Ngày cập nhập")


class CreateEKYCCustomerResponse(BaseSchema):
    customer_id: str = Field(..., description='Mã khách hàng (ekyc)')
