from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class UserInfoResponse(BaseSchema):
    username: str = Field(None, description='Username người dùng')
    name: str = Field(None, description='Họ và tên người dùng')
    code: str = Field(None, description='Mã nhân viên')
    avatar_url: str = Field(None, description='Avatar url')
    token: str = Field(..., description='Token')
    email: Optional[str] = Field(None, description='Email')
    hrm_department_id: str = Field(None, description="ID Phòng ban")
    hrm_department_code: str = Field(None, description="Mã Phòng ban")
    hrm_department_name: str = Field(None, description="Tên Phòng ban")
    hrm_branch_id: str = Field(None, description="ID Chi nhánh/Hội sở")
    hrm_branch_code: str = Field(None, description="Mã Chi nhánh/Hội sở")
    hrm_branch_name: str = Field(None, description="Tên Chi nhánh/Hội sở")
    hrm_title_id: str = Field(None, description="ID Chức danh")
    hrm_title_code: str = Field(None, description="Mã Chức danh")
    hrm_title_name: str = Field(None, description="Tên Chức danh")
    hrm_position_id: str = Field(None, description="ID Chức vụ")
    hrm_position_code: str = Field(None, description="Mã Chức vụ")
    hrm_position_name: str = Field(None, description="Tên Chức vụ")
    fcc_current_date: date = Field(None, description="Ngày giao dịch trên hệ thống")


class PermissionResponse(BaseSchema):
    permission_id: str = Field(None, description='ID quyền')
    permission_name: str = Field(None, description='Tên quyền')
    permission_code: str = Field(None, description='Mã quyền')
    active_flag: int = Field(None, description='Cờ họat động')


class GroupListResponse(BaseSchema):
    group_role_id: str = Field(None, description="ID Nhóm quyền")
    group_role_name: str = Field(None, description="Tên Nhóm quyền")
    group_role_code: str = Field(None, description="Mã Nhóm quyền")
    permission_list: List[PermissionResponse] = Field(..., description="Danh sách quyền")
    is_permission: bool = Field(None, description="Cờ có quyền hay không")


class MenuListResponse(BaseSchema):
    parent_id: str = Field(None, description="ID Menu cha")
    menu_id: str = Field(None, description="ID Menu")
    menu_name: str = Field(None, description="Tên Menu")
    menu_code: str = Field(None, description="Mã Menu")
    group_role_list: List[GroupListResponse] = Field(..., description='Danh sách `Nhóm quyền`', nullable=True)


class AuthResponse(BaseSchema):
    user_info: UserInfoResponse = Field(..., description='Thông tin người dùng')
    menu_list: List[MenuListResponse] = Field(..., description='Danh sách menu', nullable=True)


EXAMPLE_RES_FAIL_LOGIN = {
    "ex1": {
        "summary": "Không gửi đúng basic auth",
        "value": {
            "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
            "errors": [
                {
                    "loc": "null",
                    "msg": "null",
                    "detail": "Not authenticated"
                }
            ]
        }
    },
    "ex2": {
        "summary": "Sai tên đăng nhập hoặc mật khẩu",
        "value": {
            "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
            "errors": [
                {
                    "loc": "username, password",
                    "msg": "USERNAME_OR_PASSWORD_INVALID",
                    "detail": "Username or password is invalid"
                }
            ]
        }
    }
}

EXAMPLE_RES_SUCCESS_DETAIL_USER = {"ex1": {
    "summary": "Đăng nhập thành công",
    "value": {
        "data": {
            "user_info": {
                "username": "TUONGHD",
                "name": "Hồ Đình Tưởng",
                "code": "00965",
                "avatar": "/cdn-profile/00965.jpeg",
                "token": "VFVPTkdIRDo1ZGViNWQzMzdjOGFlODU1NjQ3MTdkZGU2NWY0ODYxOTMwYWU1Yzc1",
                "email": "tuonghd@scb.com.vn",
                "hrm_department_id": "12518",
                "hrm_department_code": "68",
                "hrm_department_name": "Mảng Phát triển Ứng dụng nội bộ",
                "hrm_branch_id": "000",
                "hrm_branch_code": "000",
                "hrm_branch_name": "HO",
                "hrm_title_id": "028-146",
                "hrm_title_code": "028-146",
                "hrm_title_name": "Giám đốc Phát triển Ứng dụng nội bộ",
                "hrm_position_id": "028",
                "hrm_position_code": "028",
                "hrm_position_name": "Giám đốc Mảng"
            },
            "menu_list": [
                {
                    "parent_id": "null",
                    "menu_id": "6bf48caf-fcbe-481c-852c-0e0ce8f0cefc",
                    "menu_name": "Quản lý",
                    "menu_code": "CRM",
                    "group_role_list": [
                        {
                            "group_role_id": "6b11731a-dab2-4988-a247-c2abf61e6f8f",
                            "group_role_name": "Quản lý crm",
                            "group_role_code": "QUANLY",
                            "permission_list": [
                                {
                                    "permission_id": "b0b2afe2-67ba-49d8-a8cf-08b202efb272",
                                    "permission_name": "Đăng nhập",
                                    "permission_code": "ACCESS",
                                    "active_flag": 1
                                },
                                {
                                    "permission_id": "391d4698-b403-4dc8-93fd-dc8fe1ee9dde",
                                    "permission_name": "read",
                                    "permission_code": "READ",
                                    "active_flag": 1
                                },
                                {
                                    "permission_id": "63124d5c-96ce-407f-81bb-388bb10b8f61",
                                    "permission_name": "edit",
                                    "permission_code": "EDIT",
                                    "active_flag": 1
                                }
                            ],
                            "is_permission": True
                        }
                    ]
                },
                {
                    "parent_id": "6bf48caf-fcbe-481c-852c-0e0ce8f0cefc",
                    "menu_id": "9fc91d04-de5a-4429-b97d-281c09c96729",
                    "menu_name": "Mở CIF",
                    "menu_code": "CIF",
                    "group_role_list": []
                }
            ]
        },
        "errors": []
    }
}}


class UserBannerResponse(BaseSchema):
    banner_link_512: str = Field(..., description="Link 512")
    banner_link_1024: str = Field(..., description="Link 1024")
    banner_link_2560: str = Field(..., description="Link 2560")


class RefreshTokenResponse(BaseSchema):
    refresh_token: str = Field(..., description="Refresh token")


EXAMPLE_RES_REFRESH_TOKEN = {
    "ex1": {
        "summary": "Lấy refresh token thành công",
        "value": {
            "data": {
                "refresh_token": "eJx1kE1ymzAAha+iYV3bgB0Hd1XsYsAZcP0DSVYeAQIUG4kKicbOZNXpQTpd9QrNstOD+CYFFxY0k41meN/Te088SZzuEZHeS4t9YdlXH+ne0T6ttutruNUi0/BMfpeVq8FCx85MLs04PvmYjA3n9r4wdbxW76x5cBzvF"
                                 "+Z2owmCl+l4Rh+nx6k2pFhRY2s1FX4+XE+S+RfZFvNTIMqDFi78+ek24Y8e/KwYq9S6shPpnURghqolbiKO55dvBOgkBf6fnxUJaVQTWZNHSvUpCsQas++5ei3BEnLIdoIdKnEQRqSXMxrjAxrwVGTB4HK1/5CjughlE"
                                 "Ne+UhCofCjCoB/SrF+SCqUs20Uoh4xniPBd0+Kcf/0gCbjB55evGSjo7+8cFFC89jdDr7UGBQySMG1jrKUNNssGccwPqCUzy7s3XODb1TGzbNcCN7bhVGZ9Cza6BxzdNbtSk5LTAnNMSRvU7W3/myx3Slt5JPdUdfR/"
                                 "UkNfPw5HlazKQ6UTdlHfiGpZd9U/9bIpDsNdKBir4yPI0aVAmfQUpadOpOe/Ri7alQ=="
            },
            "errors": []
        }
    }
}

EXAMPLE_RES_FAIL_REFRESH_TOKEN = {
    "ex1": {
        "summary": "Lấy refresh token thất bại", "value": {
            "data": "null",
            "errors": [
                {
                    "loc": "null",
                    "msg": "INVALID_TOKEN",
                    "detail": "Token is invalid"
                }
            ]
        }}}
