from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class ListKSS(BaseSchema):
    customer_id: Optional[str] = Field(..., description="Id customer")
    transaction_id: Optional[str] = Field(..., description="Mã giao dịch")
    full_name: Optional[str] = Field(..., description="Họ và tên")
    cif: Optional[str] = Field(..., description="Số Cif")
    phone_number: Optional[str] = Field(..., description="Số điện thoại")
    document_id: Optional[str] = Field(..., description="Số CMND/căn cước công dân/hộ chiếu")
    document_type: Optional[int] = Field(..., description="Loại giấy tờ giao dịch: "
                                                          "0: Hộ chiếu, "
                                                          "1: CMND cũ (9 số), "
                                                          "2: CMND mới (12 số), "
                                                          "3: CCCD cũ, "
                                                          "4: CCCD mới (gắn chíp)")
    status: Optional[str] = Field(..., description="Trạng thái")
    trans_date: Optional[str] = Field(..., description="Trạng thái giao dịch")
    ekyc_step: Optional[str] = Field(..., description="Nghiệp vụ")
    kss_status: Optional[str] = Field(..., description="Trạng thái kiểm soát sau")
    date_kss: Optional[str] = Field(..., description="Ngày kiểm soát sau")
    user_kss: Optional[str] = Field(..., description="Người kiểm soát sau")
    approve_status: Optional[str] = Field(..., description="Trạng thái phê duyệt")
    date_approve: Optional[str] = Field(..., description="Ngày phê duyệt")
    user_approve: Optional[str] = Field(..., description="Người thái phê duyệt")


class KSSResponse(BaseSchema):
    detail: List[ListKSS] = Field(..., description='Dữ liệu danh sách kiểm soát sau')
    total_page: Optional[int] = Field(..., description='Tổng page')
    total_record: Optional[int] = Field(..., description='Tổng record')
    page: Optional[int] = Field(..., description='Số page')


class QueryParamsKSSRequest(BaseSchema):
    tran_type_id: Optional[str] = Field(None, description="Theo loại giao dịch")
    transaction_id: Optional[str] = Field(None, description='Theo mã giao dịch')
    approve_status: Optional[str] = Field(None, description='Theo trạng thái phê duyệt')
    branch_id: Optional[str] = Field(None, description='Theo đơn vị')
    step_status: Optional[str] = Field(None, description='Theo trạng thái giao dịch')
    zone_id: Optional[str] = Field(None, description='Theo vùng')
    start_date: Optional[str] = Field(None, description='Từ ngày')
    end_date: Optional[str] = Field(None, description='Đến ngày')
    cif_phone_number_gttt_name: Optional[str] = Field(None, description="Filter by cif, phone number, gttt, full name")
    page_num: Optional[int] = Field(None, description='Số trang')
    record_per_page: Optional[int] = Field(None, description='Số record')


####################################################################################################
# Branch
####################################################################################################


class BranchResponse(BaseSchema):
    id: int = Field(..., description='ID của vùng')
    code: str = Field(..., description='Code đơn vị')
    name: str = Field(..., description='Tên đơn vị')


####################################################################################################
# vùng
####################################################################################################


class ZoneRequest(BaseSchema):
    id: int = Field(..., description='Id vùng')
    name: str = Field(..., description='Tên vùng')


###################################################################################################
# thông tin hậu kiểm của khách hàng
###################################################################################################
class ListPostControlResponse(BaseSchema):
    check_list_id: int = Field(..., description='ID của danh mục kiểm tra')
    check_list_desc: Optional[str] = Field(None, description='Danh mục kiểm tra')
    answer: str = Field(..., description='Đánh giá')
    note: Optional[str] = Field(None, description='Mô tả')


class PostControlResponse(BaseSchema):
    kss_status: str = Field(..., description="Trạng thái của KSS")
    status: str = Field(..., description='Trạng thái hậu kiểm')
    approve_status: Optional[str] = Field(..., description="Trạng thái phê duyệt")
    post_control: List[ListPostControlResponse] = Field(...)


#############################################################################################
# lịch sử hậu kiểm
#############################################################################################


class HistoryPostCheckResponse(BaseSchema):
    id: int = Field(..., description='ID of History Post-control')
    kss_status: str = Field(..., description='Status post-control description')
    kss_status_old: str = Field(..., description='Status old post-control description')
    create_date_format: Optional[str] = Field(..., description='Create date')
    approve_status: str = Field(..., description='Trạng thái phê duyệt')
    approve_date_format: Optional[str] = Field(..., description='Ngày phê duyệt')
    status: str = Field(..., description='Status posst-control')
    status_old: str = Field(..., description='Status old post-control')
    result: str = Field(..., description='Kết quả đánh giá')
    create_user: str = Field(..., description='User create')
    approve_user: str = Field(..., description='User approve')


####################################################################################################
# thống kê theo tháng
####################################################################################################


class StatisticsMonth(BaseSchema):
    month: str = Field(..., description='Thống kê theo tháng')
    total: int = Field(..., description='Thống kê giao dịch của khách hàng')
    success: int = Field(..., description='Tổng hợp giao dịch thành công của khách hàng.')
    refuse: int = Field(..., description='Tổng số giao dịch bị khách hàng từ chối')


####################################################################################################
# Thống kê hồ sơ hậu kiểm
####################################################################################################


class StatisticsProfilesResponse(BaseSchema):
    total: int = Field(..., description="Tổng cộng")
    success: int = Field(..., description="Thành công")
    canceled: int = Field(..., description="Hủy bỏ")
    processing: int = Field(..., description="Chờ hậu kiểm")
    rejected: int = Field(..., description="Cần xác minh")


####################################################################################################
# Thống kê số liệu API POST
####################################################################################################

class StatisticsResponse(BaseSchema):
    time: str = Field(..., description='Thống kê theo thời gian')
    total: int = Field(..., description='Thống kê giao dịch của khách hàng')
    success: int = Field(..., description='Tổng hợp giao dịch thành công của khách hàng.')


####################################################################################################
# create post check
####################################################################################################


class PostCheck(BaseSchema):
    check_list_id: int = Field(..., description='ID của danh mục kiểm tra')
    check_list_desc: str = Field(..., description='Danh mục kiểm tra')
    answer: str = Field(..., description='Đánh giá')
    note: Optional[str] = Field(None, description='Mô tả')


class CreatePostCheckRequest(BaseSchema):
    customer_id: str = Field(..., description='Id của khách hàng')
    kss_status: str = Field(..., description='Trạng thái hậu kiểm')
    username: str = Field(..., description='User hậu kiểm')
    post_control: List[PostCheck] = Field(...)


####################################################################################################
# phê duyệt hậu kiểm
####################################################################################################


class UpdatePostCheckRequest(BaseSchema):
    customer_id: str = Field(..., description='Id của khách hàng')
    history_post_control_id: int = Field(..., description='ID của lịch sử hậu kiểm')
    username: str = Field(..., description='User hậu kiểm')
    is_approve: bool = Field(..., description='Loại phê duyệt - true : Đã duyệt, false : Từ chối')


####################################################################################################
# Chi tiết thông tin khách hàng
####################################################################################################


class AttachmentInfoResponse(BaseSchema):
    uuid: str = Field(None, description='`uuid` của tệp đính kèm')
    url: str = Field(..., description='`URL` của tệp đính kèm')
    attachment_file_name: str = Field(None, description='`name` của tệp đính kèm')
    attachment_type: str = Field(None, description='`type` của tệp đính kèm')


class PermanentAddressResponse(BaseSchema):
    province: str = Field(..., description='Tên tỉnh/thành phố')
    province_value: str = Field(..., description='Mã tỉnh/thành phố')
    district: str = Field(..., description='Tên quận/huyện')
    district_value: str = Field(..., description='Mã quận/huyện')
    ward: str = Field(..., description='Tên phường/xã')
    ward_value: str = Field(..., description='Mã phường/xã')
    street: str = Field(..., description='Số nhà, tên đường')


class CustomerDetailResponse(BaseSchema):
    attachment_info: List[AttachmentInfoResponse] = Field(None, description='Thông tin tập tin đính kèm')
    avatar_image_url: str = Field(None, description='Url của hình avatar')
    transaction_id: str = Field(..., description='Mã giao dịch')
    document_id: str = Field(..., description='Số CMND/căn cước công dân/hộ chiếu')
    document_type: int = Field(..., description="""Mã giao dịch,
        `0`: Hộ chiếu,
        `1`: CMND cũ (9 số),
        `2`: CMND mới (12 số),
        `3`: CCCD cũ,
        `4`: CCCD mới (gắn chíp),
    """)
    date_of_issue: str = Field(..., description='Ngày cấp, phải theo định dạng `DD/MM/YYYY`')
    date_of_expiry: Optional[str] = Field(
        None,
        description='Ngày hết hạn, nếu không phải `không thời hạn` thì phải theo định dạng `DD/MM/YYYY`')
    place_of_issue: str = Field(..., description='Nơi cấp')
    qr_code_data: Optional[str] = Field(
        None,
        description='Dữ liệu có được bằng việc quét mã QR code (đối với CCCD gắn chíp)')
    finger_ids: List = Field(None, description='Danh sách các ID của hình chụp vân tay khách hàng trong hệ thống')
    full_name: str = Field(..., description='Họ và tên')
    cif: Optional[str] = Field(None, description='Số CIF_NUMBER')
    account_number: Optional[str] = Field(None, description='Số tài khoản thanh toán')
    date_of_birth: str = Field(..., description='Ngày sinh, phải theo định dạng `DD/MM/YYYY`')
    gender: str = Field(None, description='Giới tính')
    place_of_residence: str = Field(None, description='Nơi DKHK thường trú')
    place_of_origin: str = Field(..., description='Nguyên quán (nơi sinh, nếu là hộ chiếu)')
    nationality: str = Field(None, description='Quốc tịch')
    permanent_address: PermanentAddressResponse = Field(..., description='Địa chỉ thường trú của khách hàng')
    phone_number: str = Field(..., description='Số điện thoại')
    longitude: float = Field(None, description='Kinh độ')
    latitude: float = Field(None, description='Vĩ độ')
    job_title: str = Field(None, description='Nghề nghiệp')
    organization: str = Field(None, description='Cơ quan')
    organization_address: str = Field(None, description='Địa chỉ cơ quan')
    organization_phone_number: str = Field(None, description='Điện thoại cơ quan')
    position: str = Field(None, description='Chức vụ')
    salary_range: str = Field(None, description='Thu nhập bình quân 3 tháng')
    tax_number: str = Field(None, description='Mã số thuế')
    receive_ads: bool = Field(None, description='Nhận thông tin quảng cáo từ SCB')
    open_biometric: bool = Field(..., description='Bất/Tắt sinh trắc học eKYC')
    ocr_data: Optional[dict] = Field(..., description='Dữ liệu trích xuất từ giấy tờ tùy thân')
    orc_data_errors: dict = Field(None,
                                  description='Lỗi kiểm tra giả mạo thông tin được trích xuất từ giấy tờ tùy thân')
    faces_matching_percent: float = Field(
        None,
        description='Tỷ lệ phần trăm giống nhau giữa hình ảnh trên giấy tờ và hình ảnh thật')
    extra_info: dict = Field(None, description='Thông tin khác')
    ekyc_level: Optional[str] = Field(..., description="Level ekyc")
    account_status: Optional[str] = Field(None, description="Trạng thái tài khoản")
    kss_status: Optional[str] = Field(None, description="Trạng thái giao dịch")
