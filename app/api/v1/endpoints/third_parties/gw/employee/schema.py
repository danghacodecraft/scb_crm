from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


class GWEmployeeInfoResponse(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên")
    staff_name: str = Field(..., description="Tên nhân viên")
    fullname_vn: str = Field(..., description="Tên đầy đủ")
    work_location: str = Field(..., description="Địa điểm làm việc")
    email: str = Field(..., description="Địa chỉ email SCB")
    contact_mobile: str = Field(..., description="Điện thoại liên lạc")
    internal_mobile: str = Field(..., description="Điện thoại nội bộ")
    title_code: str = Field(..., description="Mã chức danh")
    title_name: str = Field(..., description="Tên chức danh")
    branch_org: List = Field(..., description="Cây đơn vị")
    avatar: str = Field(..., description="Hình ảnh đại diện nhân viên")


class GWEmployeeListResponse(BaseSchema):
    total_items: int = Field(..., description="Tổng số nhân viên")
    employee_infos: List[GWEmployeeInfoResponse] = Field(..., description="Thông tin danh sách nhân viên")


class GWRetrieveEmployeeInfoResponse(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên")
    staff_name: str = Field(..., description="Tên nhân viên")
    fullname_vn: str = Field(..., description="Tên đầy đủ")
    email: str = Field(..., description="Địa chỉ email SCB")
    contact_mobile: str = Field(..., description="Điện thoại liên lạc")
    internal_mobile: str = Field(..., description="Điện thoại nội bộ")
    title_code: str = Field(..., description="Mã chức danh")
    title_name: str = Field(..., description="Tên chức danh")
    avatar: str = Field(..., description="Hình ảnh đại diện nhân viên")
    direct_management: str = Field(..., description="Cấp quản lý trực tiếp")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    place_of_birth: str = Field(..., description="Nơi sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    ethnic: Optional[str] = Field(..., description="Dân tộc")
    religion: Optional[str] = Field(..., description="Tôn giáo")
    nationality: Optional[str] = Field(..., description="Quốc tịch")
    marital_status: Optional[str] = Field(..., description="Tình trạng hôn nhân")


class GWRetrieveEmployeeIdentityInfo(BaseSchema):
    number: str = Field(..., description="")
    issued_date: Optional[date] = Field(..., description="")
    expired_date: Optional[date] = Field(..., description="")
    place_of_issue: str = Field(..., description="")


class GWRetrieveEmployeeAddressInfo(BaseSchema):
    original_address_line: str = Field(..., description="")


class GWRetrieveEmployeeEducationInfo(BaseSchema):
    academy: str = Field(..., description="Trình độ văn hóa")
    education_level: str = Field(..., description="Trình độ học vấn")
    education_skill: str = Field(..., description="Trình độ chuyên môn")
    major: str = Field(..., description="Chuyên ngành")
    school_name: str = Field(..., description="Trường học")
    training_form: str = Field(..., description="Hình thức đào tạo")
    degree: str = Field(..., description="Xếp loại")
    gpa: str = Field(..., description="Điểm tốt nghiệp")


class GWRetrieveEmployeeLanguageInfo(BaseSchema):
    english: str = Field(..., description="Ngoại ngữ")
    english_level: str = Field(..., description="Trình độ")
    english_mark: str = Field(..., description="Điểm tốt nghiệp")
    english_issue_date: Optional[date] = Field(..., description="Ngày nhận chứng chỉ")


class GWRetrieveEmployeeProfileInfo(BaseSchema):
    join_date: Optional[date] = Field(..., description="Ngày vào làm việc")
    probation_date: Optional[date] = Field(..., description="Ngày vào thử việc")
    official_date: Optional[date] = Field(..., description="Ngày vào chính thức")
    jobtitle_name: str = Field(..., description="Chức danh hiện tại")
    temp_jobtitle_name: str = Field(..., description="Chức danh tạm thời")
    seniority_date: Optional[date] = Field(..., description="Ngày thâm niên")
    resident_status: str = Field(..., description="Đối tượng cư trú ( 1:có , 0:không)")
    department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")
    org_department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")
    temp_department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")


class GWRetrieveEmployeeContractInfo(BaseSchema):
    contract_type: str = Field(..., description="Loại hợp đồng")
    contract_name: str = Field(..., description="Số hợp đồng")
    contract_effected_date: Optional[date] = Field(..., description="Ngày bắt đầu HĐ")
    contract_expired_date: Optional[date] = Field(..., description="Ngày kết thúc HĐ")
    schedule_of_contract_num: str = Field(..., description="Số phụ lục HĐ")
    schedule_of_contract_effected_date: Optional[date] = Field(..., description="Ngày bắt đầu PL")
    schedule_of_contract_expired_date: Optional[date] = Field(..., description="Ngày kết thúc PL")
    stop_job_date: Optional[date] = Field(..., description="Ngày nghỉ việc")


class GWRetrieveEmployeeResponse(BaseSchema):
    employee_info: GWRetrieveEmployeeInfoResponse = Field(..., description="Thông tin nhân viên")
    department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")
    identity_info: GWRetrieveEmployeeIdentityInfo = Field(..., description="Thông tin giấy tờ định danh")
    address_info: GWRetrieveEmployeeAddressInfo = Field(..., description="Thông tin địa chỉ")
    education_info: GWRetrieveEmployeeEducationInfo = Field(..., description="Thông tin trình độ học vấn")
    language_info: GWRetrieveEmployeeLanguageInfo = Field(..., description="Thôn tin ngôn ngữ")
    certificate_infos: List = Field(..., description="Thông tin danh sách chứng chỉ")
    profile_info: GWRetrieveEmployeeProfileInfo = Field(..., description="Thông tin hồ sơ")
    contract_info: GWRetrieveEmployeeContractInfo = Field(..., description="Thông tin hợp đồng")


class GWEmployeeWorkingProcessItemResponse(BaseSchema):
    company: str = Field(..., description="Tên công ty")
    from_date: Optional[date] = Field(..., description="Từ ngày")
    to_date: Optional[date] = Field(..., description="Đến ngày")
    position: str = Field(..., description="Vị trí")


class GWEmployeeWorkingProcessResponse(BaseSchema):
    total_items: int = Field(..., description="Tổng số quá trình việc làm")
    working_process_infos: List[GWEmployeeWorkingProcessItemResponse] = Field(
        ..., description="Thông tin quá trình công tác")
