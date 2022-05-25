from typing import ForwardRef, List

from pydantic import Field

from app.api.base.schema import BaseGWSchema

GWOrgInfo = ForwardRef('GWOrgInfoResponse')


class GWOrgInfoResponse(BaseGWSchema):
    id: str = Field(..., description="Mã nhân viên")
    parent_id: str = Field(..., description="Tên nhân viên")
    name: str = Field(..., description="Tên đầy đủ")
    short_name: str = Field(..., description="Địa điểm làm việc")
    path: str = Field(..., description="Địa chỉ email SCB")
    path_description: str = Field(..., description="Điện thoại liên lạc")
    order_by: str = Field(..., description="Điện thoại nội bộ")
    childs: List[GWOrgInfo] = Field(..., description="Tổ chức cấp con")


GWOrgInfoResponse.update_forward_refs()


class GWOrgInfoFromParentResponse(BaseGWSchema):
    id: str = Field(..., description="Mã nhân viên")
    parent_id: str = Field(..., description="Tên nhân viên")
    name: str = Field(..., description="Tên đầy đủ")
    short_name: str = Field(..., description="Địa điểm làm việc")
    path: str = Field(..., description="Địa chỉ email SCB")
    path_description: str = Field(..., description="Điện thoại liên lạc")
    order_by: str = Field(..., description="Điện thoại nội bộ")


class GWOrgInfoFromChildResponse(BaseGWSchema):
    id: str = Field(..., description="Mã nhân viên")
    parent_id: str = Field(..., description="Tên nhân viên")
    name: str = Field(..., description="Tên đầy đủ")
    short_name: str = Field(..., description="Địa điểm làm việc")
    path: str = Field(..., description="Địa chỉ email SCB")
    path_description: str = Field(..., description="Điện thoại liên lạc")
    order_by: str = Field(..., description="Điện thoại nội bộ")
