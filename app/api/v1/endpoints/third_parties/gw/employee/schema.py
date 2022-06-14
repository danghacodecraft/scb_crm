from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseGWSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


class GWEmployeeInfoResponse(BaseGWSchema):
    staff_code: Optional[str] = Field(..., description="Mã nhân viên")
    staff_name: Optional[str] = Field(..., description="Tên nhân viên")
    fullname_vn: Optional[str] = Field(..., description="Tên đầy đủ")
    work_location: Optional[str] = Field(..., description="Địa điểm làm việc")
    email: Optional[str] = Field(..., description="Địa chỉ email SCB")
    contact_mobile: Optional[str] = Field(..., description="Điện thoại liên lạc")
    internal_mobile: Optional[str] = Field(..., description="Điện thoại nội bộ")
    title_code: Optional[str] = Field(..., description="Mã chức danh")
    title_name: Optional[str] = Field(..., description="Tên chức danh")
    branch_org: Optional[List] = Field(..., description="Cây đơn vị")
    avatar: Optional[str] = Field(..., description="Hình ảnh đại diện nhân viên")


class GWEmployeeListResponse(BaseGWSchema):
    total_items: int = Field(..., description="Tổng số nhân viên")
    employee_infos: List[GWEmployeeInfoResponse] = Field(..., description="Thông tin danh sách nhân viên")


class GWRetrieveEmployeeInfoResponse(BaseGWSchema):
    staff_code: Optional[str] = Field(..., description="Mã nhân viên")
    staff_name: Optional[str] = Field(..., description="Tên nhân viên")
    fullname_vn: Optional[str] = Field(..., description="Tên đầy đủ")
    email: Optional[str] = Field(..., description="Địa chỉ email SCB")
    contact_mobile: Optional[str] = Field(..., description="Điện thoại liên lạc")
    internal_mobile: Optional[str] = Field(..., description="Điện thoại nội bộ")
    title_code: Optional[str] = Field(..., description="Mã chức danh")
    title_name: Optional[str] = Field(..., description="Tên chức danh")
    avatar: Optional[str] = Field(..., description="Hình ảnh đại diện nhân viên")
    direct_management: Optional[str] = Field(..., description="Cấp quản lý trực tiếp")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    place_of_birth: Optional[str] = Field(..., description="Nơi sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    ethnic: Optional[str] = Field(..., description="Dân tộc")
    religion: Optional[str] = Field(..., description="Tôn giáo")
    nationality: Optional[str] = Field(..., description="Quốc tịch")
    marital_status: Optional[str] = Field(..., description="Tình trạng hôn nhân")


class GWRetrieveEmployeeIdentityInfo(BaseGWSchema):
    number: Optional[str] = Field(..., description="CMND/Hộ chiếu, số đăng ký kinh doanh nếu là khách hàng doanh nghiệp")
    issued_date: Optional[date] = Field(..., description="Ngày cấp chứng minh nhân dân hoặc hộ chiếu")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn chứng minh nhân dân hoặc hộ chiếu")
    place_of_issue: Optional[str] = Field(..., description="Nơi cấp chứng minh nhân dân hoặc hộ chiếu")


class GWRetrieveEmployeeAddressInfo(BaseGWSchema):
    number_and_street: Optional[str] = Field(..., description="tên đường, số nhà")
    country: OptionalDropdownResponse = Field(..., description="tên quốc gia")
    province: OptionalDropdownResponse = Field(..., description="tên thành phố")
    district: OptionalDropdownResponse = Field(..., description="tên quận, huyện")
    ward: OptionalDropdownResponse = Field(..., description="tên phường")


class GWRetrieveEmployeeEducationInfo(BaseGWSchema):
    academy: Optional[str] = Field(..., description="Trình độ văn hóa")
    education_level: Optional[str] = Field(..., description="Trình độ học vấn")
    education_skill: Optional[str] = Field(..., description="Trình độ chuyên môn")
    major: Optional[str] = Field(..., description="Chuyên ngành")
    school_name: Optional[str] = Field(..., description="Trường học")
    training_form: Optional[str] = Field(..., description="Hình thức đào tạo")
    degree: Optional[str] = Field(..., description="Xếp loại")
    gpa: Optional[str] = Field(..., description="Điểm tốt nghiệp")


class GWRetrieveEmployeeLanguageInfo(BaseGWSchema):
    english: Optional[str] = Field(..., description="Ngoại ngữ")
    english_level: Optional[str] = Field(..., description="Trình độ")
    english_mark: Optional[str] = Field(..., description="Điểm tốt nghiệp")
    english_issue_date: Optional[date] = Field(..., description="Ngày nhận chứng chỉ")


class GWRetrieveEmployeeProfileInfo(BaseGWSchema):
    join_date: Optional[date] = Field(..., description="Ngày vào làm việc")
    probation_date: Optional[date] = Field(..., description="Ngày vào thử việc")
    official_date: Optional[date] = Field(..., description="Ngày vào chính thức")
    jobtitle_name: Optional[str] = Field(..., description="Chức danh hiện tại")
    temp_jobtitle_name: Optional[str] = Field(..., description="Chức danh tạm thời")
    seniority_date: Optional[date] = Field(..., description="Ngày thâm niên")
    resident_status: Optional[str] = Field(..., description="Đối tượng cư trú ( 1:có , 0:không)")
    department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")
    org_department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")
    temp_department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")


class GWRetrieveEmployeeContractInfo(BaseGWSchema):
    contract_type: Optional[str] = Field(..., description="Loại hợp đồng")
    contract_name: Optional[str] = Field(..., description="Số hợp đồng")
    contract_effected_date: Optional[date] = Field(..., description="Ngày bắt đầu HĐ")
    contract_expired_date: Optional[date] = Field(..., description="Ngày kết thúc HĐ")
    schedule_of_contract_num: Optional[str] = Field(..., description="Số phụ lục HĐ")
    schedule_of_contract_effected_date: Optional[date] = Field(..., description="Ngày bắt đầu PL")
    schedule_of_contract_expired_date: Optional[date] = Field(..., description="Ngày kết thúc PL")
    stop_job_date: Optional[date] = Field(..., description="Ngày nghỉ việc")


class GWRetrieveEmployeeResponse(BaseGWSchema):
    employee_info: GWRetrieveEmployeeInfoResponse = Field(..., description="Thông tin nhân viên")
    department_info: OptionalDropdownResponse = Field(..., description="Thông tin Đơn vị/Phòng ban")
    identity_info: GWRetrieveEmployeeIdentityInfo = Field(..., description="Thông tin giấy tờ định danh")
    original_address: GWRetrieveEmployeeAddressInfo = Field(..., description="Thông tin địa chỉ Nguyên quán")
    resident_address: GWRetrieveEmployeeAddressInfo = Field(..., description="Thông tin địa chỉ cư trú")
    contact_address: GWRetrieveEmployeeAddressInfo = Field(..., description="Thông tin địa chỉ liên lạc")
    education_info: GWRetrieveEmployeeEducationInfo = Field(..., description="Thông tin trình độ học vấn")
    language_info: GWRetrieveEmployeeLanguageInfo = Field(..., description="Thôn tin ngôn ngữ")
    certificate_infos: List = Field(..., description="Thông tin danh sách chứng chỉ")
    profile_info: GWRetrieveEmployeeProfileInfo = Field(..., description="Thông tin hồ sơ")
    contract_info: GWRetrieveEmployeeContractInfo = Field(..., description="Thông tin hợp đồng")


class GWEmployeeWorkingProcessItemResponse(BaseGWSchema):
    company: Optional[str] = Field(..., description="Tên công ty")
    from_date: Optional[date] = Field(..., description="Từ ngày")
    to_date: Optional[date] = Field(..., description="Đến ngày")
    position: Optional[str] = Field(..., description="Vị trí")


class GWEmployeeWorkingProcessResponse(BaseGWSchema):
    total_items: int = Field(..., description="Tổng số quá trình công tác của nhân viên")
    working_process_infos: List[GWEmployeeWorkingProcessItemResponse] = Field(
        ..., description="Thông tin quá trình công tác của nhân viên")


class GWEmployeeRewardItemResponse(BaseGWSchema):
    effect_date: Optional[date] = Field(..., description="Ngày hiệu lực")
    number: Optional[str] = Field(..., description="Số quyết định")
    title: Optional[str] = Field(..., description="Danh hiệu")
    level: Optional[str] = Field(..., description="Cấp khen thưởng")
    jobtitle: Optional[str] = Field(..., description="Chức danh")
    department: Optional[str] = Field(..., description="Đơn vị/Phòng ban")
    reason: Optional[str] = Field(..., description="Lý do khen thưởng")
    form: Optional[str] = Field(..., description="Hình thức khen thưởng")
    of_amount: Optional[str] = Field(..., description="Số tiền khen thưởng")
    signing_date: Optional[date] = Field(..., description="Ngày ký")
    signer: Optional[str] = Field(..., description="Người ký")


class GWEmployeeRewardResponse(BaseGWSchema):
    total_items: int = Field(..., description="Tổng số khen thưởng của nhân viên")
    reward_infos: List[GWEmployeeRewardItemResponse] = Field(..., description="Thông tin khen thưởng của nhân viên")


class GWEmployeeDisciplineItemResponse(BaseGWSchema):
    effect_date: Optional[date] = Field(..., description="Ngày hiệu lực")
    expire_date: Optional[date] = Field(..., description="Ngày kết thúc")
    jobtitle: Optional[str] = Field(..., description="Chức danh")
    department: Optional[str] = Field(..., description="Đơn vị/Phòng ban")
    reason: Optional[str] = Field(..., description="Lý do kỷ luật")
    description: Optional[str] = Field(..., description="Lý do chi tiết")


class GWEmployeeDisciplineResponse(BaseGWSchema):
    total_items: int = Field(..., description="Tổng số vi phạm kỷ luật của nhân viên")
    reward_infos: List[GWEmployeeDisciplineItemResponse] = Field(...,
                                                                 description="Thông tin vi phạm kỷ luật của nhân viên")


class GWEmployeeTopicItemResponse(BaseGWSchema):
    code: Optional[str] = Field(..., description="Mã khóa học")
    name: Optional[str] = Field(..., description="Tên khóa học")
    from_date: Optional[date] = Field(..., description="Từ ngày")
    to_date: Optional[date] = Field(..., description="Đến ngày")
    result: Optional[str] = Field(..., description="Kết quả")
    description: Optional[str] = Field(..., description="Chủ đề")


class GWEmployeeTopicResponse(BaseGWSchema):
    total_items: int = Field(..., description="Tổng số khóa học của nhân viên")
    topic_infos: List[GWEmployeeTopicItemResponse] = Field(..., description="Thông tin khóa học của nhân viên")


class GWEmployeeKpisItemResponse(BaseGWSchema):
    period_name: Optional[str] = Field(..., description="Kỳ đánh giá")
    total_point: Optional[str] = Field(..., description="Tổng điểm kpis")
    completed: Optional[str] = Field(..., description="Tỷ lệ hoàn thành")
    grade_name: Optional[str] = Field(..., description="Kết quả/ xếp hạng")
    note: Optional[str] = Field(..., description="Ghi chú")


class GWEmployeeKpisResponse(BaseGWSchema):
    total_items: int = Field(..., description="Tổng số khóa học của nhân viên")
    kpis_infos: List[GWEmployeeKpisItemResponse] = Field(..., description="Thông tin khóa học của nhân viên")


class GWEmployeeRecruitmentInfoResponse(BaseGWSchema):
    code: Optional[str] = Field(..., description="Mã yêu cầu tuyển dụng")
    reason: Optional[str] = Field(..., description="Lý do tuyển dụng")
    presenter: Optional[str] = Field(..., description="Người giới thiệu")
    replace_staff: Optional[str] = Field(..., description="Nhân viên thay thế")
    note: Optional[str] = Field(..., description="Ghi chú tuyển dụng")
    other: Optional[str] = Field(..., description="Thông tin khác")


class GWEmployeeStaffOtherResponse(BaseGWSchema):
    seniority_month: Optional[str] = Field(..., description="Tháng thâm niên cộng thêm")
    annual_number: Optional[str] = Field(..., description="Số phép năm ưu đãi")
    recruitment_info: GWEmployeeRecruitmentInfoResponse = Field(..., description="Thông tin tuyển dụng")
