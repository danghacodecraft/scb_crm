from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema, CreatedUpdatedBaseModel


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


########################################################################################################################
# update user
########################################################################################################################


class UserUpdateRequest(BaseSchema):
    full_name_vn: str = Field(..., description='Họ và tên người dùng')
    avatar_url: str = Field(..., description='Link avatar')


class UserUpdateResponse(CreatedUpdatedBaseModel):
    user_id: str = Field(..., description='Id người dùng')
    full_name_vn: str = Field(..., description='Họ và tên người dùng')


EXAMPLE_REQ_UPDATE_USER = {
    "ex1": {
        "summary": "A normal example",
        "description": "A **normal** item works correctly.",
        "value": {
            "full_name_vn": "Foo",
            "avatar_url": "/cdn/abc.jpg"
        },
    },
    "ex2": {
        "summary": "An example with converted data",
        "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
        "value": {
            "full_name_vn": "Foo",
            "avatar_url": "A very nice Item"
        },
    }
}

EXAMPLE_RES_SUCCESS_UPDATE_USER = {
    "ex1": {
        "summary": "Thành công 1",
        "value": {
            "data": {
                "created_at": "16 10:46:08-10-2021",
                "created_by": "system",
                "updated_at": "16 10:46:08-10-2021",
                "updated_by": "system",
                "user_id": "9651cdfd9a9a4eb691f9a3a125ac46b0",
                "full_name_vn": "abc"
            },
            "errors": []
        }
    },
    "ex2": {
        "summary": "Thành công 2",
        "value": {
            "data": {
                "created_at": "16 10:46:50-10-2021",
                "created_by": "system",
                "updated_at": "16 10:46:50-10-2021",
                "updated_by": "system",
                "user_id": "9651cdfd9a9a4eb691f9a3a125ac46b0",
                "full_name_vn": "xyz"
            },
            "errors": []
        }
    }
}

EXAMPLE_RES_FAIL_UPDATE_USER = {
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
        "summary": "Truyền không đúng kiểu dữ liệu",
        "value": {
            "data": "null",  # do FastAPI đang generate file openapi.json với option bỏ qua None nên tạm thời để vậy
            "errors": [
                {
                    "loc": "body -> avatar_url",
                    "msg": "VALIDATE_ERROR",
                    "detail": "str type expected"
                }
            ]
        }
    }
}

########################################################################################################################


class UserBannerResponse(BaseSchema):
    banner_link_512: str = Field(..., description="Link 512")
    banner_link_1024: str = Field(..., description="Link 1024")
    banner_link_2560: str = Field(..., description="Link 2560")
