from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.address import (  # noqa
    AddressCountry
)


class KYCLevel(Base):
    __tablename__ = 'crm_kyc_level'

    id = Column('kyc_level_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID cấp độ KYC')
    code = Column('kyc_level_code', VARCHAR(50), nullable=False, comment='Mã cấp độ KYC')
    name = Column('kyc_level_name', VARCHAR(255), nullable=False,
                  comment='Tên KCY ( Giấy tờ định danh, vân tay, khuôn mặt,..)')
    active_flag = Column('active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column('order_no', NUMBER(3, 0, False), comment='Sắp xếp')


class Channel(Base):
    __tablename__ = 'crm_channel'

    id = Column('channel_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID kênh tạo thông tin')
    code = Column('channel_code', VARCHAR(50), nullable=False, comment='Mã kênh tạo thông tin')
    name = Column('channel_name', VARCHAR(255), nullable=False, comment='Tên kênh tạo thông tin')
    active_flag = Column('channel_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái kênh')
    order_no = Column('order_no', NUMBER(3, 0, False), comment='Sắp xếp')


class BranchRegion(Base):
    __tablename__ = 'crm_branch_region'

    id = Column('branch_region_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID đơn vị vùng')
    code = Column('branch_region_code', VARCHAR(50), nullable=False, comment='Mã đơn vị vùng')
    name = Column('branch_region_name', VARCHAR(255), nullable=False, comment='Tên đơn vị vùng')


class BusinessType(Base):
    __tablename__ = 'crm_business_type'

    id = Column('business_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID loại nghiệp vụ')
    code = Column(VARCHAR(50), nullable=False, comment='Mã code loại nghiệp vụ')
    name = Column(VARCHAR(500), nullable=False, comment='Tên loại nghiệp vụ')
    description = Column(VARCHAR(1000), comment='Mô tả loại nghiệp vụ')
    active_flag = Column(NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')
    created_at = Column(DateTime, nullable=False, server_default=text("sysdate "), comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')


class BusinessForm(Base):
    __tablename__ = 'crm_business_form'

    id = Column('business_form_id', VARCHAR(36), primary_key=True)
    code = Column('business_form_code', VARCHAR(20), nullable=False)
    name = Column('business_form_name', VARCHAR(200), nullable=False)
    business_type_id = Column(VARCHAR(36), nullable=False)
    parent_id = Column('business_form_parent_id', VARCHAR(36), nullable=False)
    order_no = Column(NUMBER(asdecimal=False), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class BusinessJob(Base):
    __tablename__ = 'crm_business_job'

    id = Column('business_job_id', VARCHAR(36), primary_key=True)
    code = Column('business_job_code', VARCHAR(20), nullable=False)
    name = Column('business_job_name', VARCHAR(200), nullable=False)
    active_flag = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "), comment='Trạng thái hoạt động')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    business_type_id = Column(VARCHAR(36), nullable=False)
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class Branch(Base):
    __tablename__ = 'crm_branch'

    id = Column('branch_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID đơn vị')
    region_id = Column('branch_region_id', VARCHAR(36), nullable=False, comment='ID đơn vị vùng')
    province_id = Column('branch_province_id', VARCHAR(36), nullable=False, comment='ID tỉnh/thành')
    district_id = Column('branch_district_id', VARCHAR(36), nullable=False, comment='ID quận/huyện')
    ward_id = Column('branch_ward_id', VARCHAR(36), nullable=False, comment='ID phường/xã')
    code = Column('branch_code', VARCHAR(3), nullable=False, comment='Mã đơn vị')
    name = Column('branch_name', VARCHAR(255), nullable=False, comment='Tên đơn vị')
    parent_code = Column('parent_branch_code', VARCHAR(3), nullable=False, comment='Mã cấp cha đơn vị')
    tax_code = Column('branch_tax_code', VARCHAR(15), nullable=False, comment='Mã số thuế đơn vị')
    phone_number = Column('branch_phone_num', VARCHAR(12), nullable=False, comment='Số điện thoại đơn vị')
    active_flag = Column('branch_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    address = Column('branch_address', VARCHAR(255), nullable=False, comment='Địa chỉ đơn vị')


class ResidentStatus(Base):
    __tablename__ = 'crm_resident_status'

    id = Column('resident_status_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID trạng thái cư trú/dân cư')
    code = Column('resident_status_code', VARCHAR(50), nullable=False, comment='Mã trạng thái cư trú/dân cư')
    name = Column('resident_status_name', VARCHAR(255), nullable=False, comment='Tên trạng thái cư trú/dân cư')
    active_flag = Column('resident_status_active_flag', NUMBER(1, 0, False), nullable=False,
                         comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class AverageIncomeAmount(Base):
    __tablename__ = 'crm_average_income_amount'

    id = Column('average_income_amount_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID thu nhập theo loại tháng gần nhất')
    code = Column('average_income_amount_code', VARCHAR(50), nullable=False,
                  comment='Mã thu nhập theo loại tháng gần nhất')
    name = Column('average_income_amount_name', VARCHAR(255), nullable=False,
                  comment='Tên thu nhập theo loại tháng gần nhất')
    active_flag = Column('average_income_amount_active_flag', NUMBER(1, 0, False), nullable=False,
                         comment='Trạng thái hoạt động')
    month_number = Column('month_num', NUMBER(2, 0, False), nullable=False, comment='Loại tháng gần nhất (3, 6, 9)')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class Career(Base):
    __tablename__ = 'crm_career'

    id = Column('career_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID nghề nghiệp')
    code = Column('career_code', VARCHAR(50), nullable=False, comment='Mã nghề nghiệp')
    name = Column('career_name', VARCHAR(255), nullable=False, comment='Tên nghề nghiệp')
    active_flag = Column('career_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class Currency(Base):
    __tablename__ = 'crm_currency'
    __table_args__ = {'comment': 'Danh mục loại tiền:\n - VND\n - USD\n - ......'}

    id = Column('currency_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='Mã tiền tệ')
    code = Column('currency_code', VARCHAR(50), nullable=False, comment='Mã tiền tệ code ( vd: VND..)')
    name = Column('currency_name', VARCHAR(255), nullable=False, comment='Tên tiền tệ')
    active_flag = Column('currency_active_flag', NUMBER(1, 0, False), comment='Cờ kích hoạt tiền tệ')
    order_no = Column(NUMBER(3, 2, True), comment='Thứ tự sắp xếp')


class FatcaCategory(Base):
    __tablename__ = 'crm_fatca_category'

    id = Column('fatca_category_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID danh mục FATCA')
    code = Column('fatca_category_code', VARCHAR(50), nullable=False, comment='Mã danh mục FATCA')
    name = Column('fatca_category_name', VARCHAR(1000), nullable=False, comment='Tên danh mục FATCA')
    active_flag = Column('fatca_category_active_flag', NUMBER(1, 0, False), nullable=False,
                         comment='Trạng thái hoạt động')
    version = Column('fatca_category_version', VARCHAR(10), nullable=False, comment='Phiên bản danh mục FATCA')
    created_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class MethodAuthentication(Base):
    __tablename__ = 'crm_method_authen'
    __table_args__ = {
        'comment': 'Danh mục Hình thức xác thực\n\n  '
                   '1. Vân tay\n  '
                   '2. Khuôn mặt\n  '
                   '3. SMS\n  '
                   '4. SOFT TOKEN\n  '
                   '5. HARD TOKEN'
    }

    id = Column('method_authen_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID chính')
    code = Column('method_authen_code', VARCHAR(10), comment='Mã code')
    name = Column('method_authen_name', VARCHAR(100), comment='Tên')
    active_flag = Column('method_authen_active_flag', NUMBER(1, 0, False), comment='Trạng thái')
    order_no = Column(NUMBER(4, 2, True), comment='Sắp xếp')


class Position(Base):
    __tablename__ = 'crm_position'

    id = Column('position_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chức vụ')
    code = Column('position_code', VARCHAR(50), nullable=False, comment='Mã chức vụ')
    name = Column('position_name', VARCHAR(255), nullable=False, comment='Tên chức vụ')
    active_flag = Column('position_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(4, 2, True), comment='Sắp xếp')


class MaritalStatus(Base):
    __tablename__ = 'crm_marital_status'

    id = Column('marital_status_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID tình trạng hôn nhân')
    code = Column('marital_status_code', VARCHAR(50), nullable=False, comment='Mã tình trạng hôn nhân')
    name = Column('marital_status_name', VARCHAR(255), nullable=False, comment='Tên tình trạng hôn nhân')
    active_flag = Column('marital_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class Nation(Base):
    __tablename__ = 'crm_nation'

    id = Column('nation_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID dân tộc')
    code = Column('nation_code', VARCHAR(50), nullable=False, comment='Mã dân tộc')
    name = Column('nation_name', VARCHAR(255), nullable=False, comment='Tên dân tộc')
    active_flag = Column('nation_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class Religion(Base):
    __tablename__ = 'crm_religion'

    id = Column('religion_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID tôn giáo')
    code = Column('religion_code', VARCHAR(50), nullable=False, comment='Mã tôn giáo')
    name = Column('religion_name', VARCHAR(255), nullable=False, comment='Tên tôn giáo')
    active_flag = Column('religion_active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column(NUMBER(3, 0, False), comment='Sắp xếp')


class HrmEmployee(Base):
    __tablename__ = 'hrm_employee'
    __table_args__ = {'comment': 'Thông tin nhân viên lấy từ hệ thống HR'}

    id = Column(VARCHAR(36), primary_key=True, comment='Mã nhân viên')
    fullname_vn = Column(VARCHAR(255), nullable=False, comment='Tên nhân viên')
    user_name = Column(VARCHAR(255), nullable=False, comment='Tài khoản AD nhân viên')
    email = Column(VARCHAR(255), nullable=False, comment='Email nội bộ')
    job_title = Column(VARCHAR(255), nullable=False, comment='Chức danh')
    department_id = Column(VARCHAR(36), nullable=False, comment='Mã phòng ban')
    active = Column(NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động (Có/không)')


class StaffType(Base):
    __tablename__ = 'crm_staff_type'
    __table_args__ = {
        'comment': 'Danh mục Loại nhân viên giới thiệu:\n\n  '
                   '1. Nhân viên kinh doanh\n  '
                   '2. Nhân viên giới thiệu gian tiếp'
    }

    id = Column('staff_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chính')
    code = Column('staff_type_code', VARCHAR(50), nullable=False, comment='Mã code')
    name = Column('staff_type_name', VARCHAR(105), nullable=False, comment='Tên')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')


class Sla(Base):
    __tablename__ = 'crm_sla'
    __table_args__ = {'comment': 'SLA'}

    id = Column('sla_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Giai đoạn xử lý')
    code = Column('sla_code', VARCHAR(20), comment='Mã code Giai đoạn xử lý')
    name = Column('sla_name', VARCHAR(50), comment='Tên Giai đoạn xử lý')
    deadline = Column('sla_deadline', NUMBER(10, 0, False), comment='deadline')
    active_flag = Column(NUMBER(1, 0, False), comment='trạng thái')
    created_at = Column(DateTime, comment='ngày tạo')
    updated_at = Column(DateTime, comment='ngày cập nhật')


########################################################################################################################
#                                 WORKFLOW APPROVAL                                                                    #
########################################################################################################################

class Phase(Base):
    __tablename__ = 'crm_phase'

    id = Column('phase_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID Giai đoạn xử lý')
    business_type_id = Column(ForeignKey('crm_business_type.business_type_id'), nullable=False,
                              comment='ID loại nghiệp vụ (Vd: Mở TK thanh toán, TK Tiết kiệm, EB...)')
    code = Column('phase_code', VARCHAR(50), nullable=False, comment='Mã code Giai đoạn xử lý')
    name = Column('phase_name', VARCHAR(250), nullable=False, comment='Tên Giai đoạn xử lý')

    business_type = relationship('BusinessType')
    stage = relationship('StagePhase')


class Lane(Base):
    __tablename__ = 'crm_lane'

    id = Column('lane_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID Luồng xử lý')
    business_type_id = Column(ForeignKey('crm_business_type.business_type_id'), nullable=False,
                              comment='ID loại nghiệp vụ (Vd: Mở TK thanh toán, TK Tiết kiệm, EB...)')
    code = Column('lane_code', VARCHAR(50), nullable=False, comment='Mã Luồng xử lý')
    name = Column('lane_name', VARCHAR(250), nullable=False, comment='Tên Luồng xử lý')
    created_at = Column(DateTime, nullable=False, server_default=text("sysdate "), comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')

    business_type = relationship('BusinessType')


class Stage(Base):
    __tablename__ = 'crm_stage'
    __table_args__ = {'comment': 'Bước xử lý\n\n  1.  Khởi tạo\n  2.  Gửi duyệt'}

    id = Column('stage_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã bước thực hiện')
    status_id = Column('stage_status_id', ForeignKey('crm_stage_status.stage_status_id'),
                       comment='Mã trạng thái của bước thực hiện')
    parent_id = Column('stage_parent_id', ForeignKey('crm_stage.stage_id'), comment='Mã bước thực hiện cấp cha')
    business_type_id = Column(ForeignKey('crm_business_type.business_type_id'),
                              comment='Mã loại nghiệp vụ (Vd: Mở TK thanh toán, TK Tiết kiệm, EB...)')
    name = Column('stage_name', VARCHAR(250), comment='Tên bước hiện')
    code = Column('stage_code', VARCHAR(50), comment='Mã bước thực hiện kiểu chữ(vd: IN, DUYET)')
    sla_id = Column(ForeignKey('crm_sla.sla_id'), comment='mã Giai đoạn xử lý')

    responsible_flag = Column('stage_responsible_flag', NUMBER(1, 0, False),
                              comment='Cờ người chịu trách nhiệm của bước thực hiện')

    is_reject = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                       comment='Cờ đánh dấu trạng thái TRẢ hồ sơ')

    created_at = Column(DateTime, comment='Ngày tạo bước thực hiện')
    updated_at = Column(DateTime, comment='Ngày cập nhật bước thực hiện')

    business_type = relationship('BusinessType')
    sla = relationship('Sla')
    parent = relationship('Stage', remote_side=[id])
    status = relationship('StageStatus')
    phase = relationship('StagePhase')


class StageStatus(Base):
    __tablename__ = 'crm_stage_status'
    __table_args__ = {'comment': 'Trạng thái xử lý'}

    id = Column('stage_status_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã trạng thái của bước thực hiện')
    code = Column('stage_status_code', VARCHAR(50), comment='Tên trạng thái của bước thực hiện')
    business_type_id = Column(ForeignKey('crm_business_type.business_type_id'),
                              comment='Mã trạng thái của bước thực hiện kiểu chữ (vd: KHOI_TAO) ')
    name = Column('stage_status_name', VARCHAR(250),
                  comment='Mã loại nghiệp vụ (Vd: Mở TK thanh toán, TK Tiết kiệm, EB...)')
    created_at = Column(DateTime, comment='Ngày tạo trạng thái của bước thực hiện')
    updated_at = Column(DateTime, comment='Ngày cập nhật trạng thái của bước thực hiện')

    business_type = relationship('BusinessType')


class StageRole(Base):
    __tablename__ = 'crm_stage_role'
    __table_args__ = {'comment': 'Quyền xử lý Bước'}

    id = Column('stage_role_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã quyền thực hiện bước')
    stage_id = Column(ForeignKey('crm_stage.stage_id'), comment='Mã bước thực hiện')
    code = Column('stage_role_code', VARCHAR(50), comment='Mã quyền thưc hiện bước kiểu text ( vd: NHAP, DUYET)')
    name = Column('stage_role_name', VARCHAR(250), comment='Tên quyền thực hiện bước')
    created_at = Column(DateTime, comment='Ngày tạo bước thực hiện')

    stage = relationship('Stage')


class TransactionStageLane(Base):
    __tablename__ = 'crm_transaction_stage_lane'
    __table_args__ = {'comment': 'Phân luồng từng giai đoạn'}

    id = Column('transaction_stage_lane_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã luồng của bước thực hiện')
    code = Column('transaction_stage_lane_code', VARCHAR(50), comment=' Mã code phân luồng')
    name = Column('transaction_stage_lane_name', VARCHAR(250), comment='Tên phân luồng')
    department_id = Column(VARCHAR(36), comment='Mã phòng ban thực hiện')
    branch_id = Column(VARCHAR(36), comment='Mã đơn vị thực hiện')


class TransactionStagePhase(Base):
    __tablename__ = 'crm_transaction_stage_phase'
    __table_args__ = {'comment': 'Giai đoạn xử lý của bước giao dịch'}

    id = Column('transaction_stage_phase_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID chính')
    code = Column('transaction_stage_phase_code', VARCHAR(50), comment='Mã code')
    name = Column('transaction_stage_phase_name', VARCHAR(250), comment='Tên')


class TransactionStageRole(Base):
    __tablename__ = 'crm_transaction_stage_role'
    __table_args__ = {'comment': 'Vai trò từng giai đoạn'}

    id = Column('transaction_stage_role_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã quyền thực hiện bước')
    transaction_stage_id = Column(VARCHAR(36), comment='Mã bước thực hiện')
    code = Column('transaction_stage_role_code', VARCHAR(50),
                  comment='Mã quyền thưc hiện bước kiểu text ( vd: NHAP, DUYET)')
    name = Column('transaction_stage_role_name', VARCHAR(250), comment='Tên quyền thực hiện bước')


class TransactionStageStatus(Base):
    __tablename__ = 'crm_transaction_stage_status'
    __table_args__ = {'comment': 'Trạng thái từng giai đoạn'}

    id = Column('transaction_stage_status_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID trạng thái của bước thực hiện')
    code = Column('transaction_stage_status_code', VARCHAR(50),
                  comment='Mã trạng thái của bước thực hiện kiểu chữ (vd: KHOI_TAO) ')
    name = Column('transaction_stage_status_name', VARCHAR(250), comment='Tên trạng thái của bước thực hiện')


class TransactionJob(Base):
    __tablename__ = 'crm_transaction_job'

    transaction_id = Column(VARCHAR(36), primary_key=True)
    booking_id = Column(VARCHAR(36), nullable=False)
    business_job_id = Column(VARCHAR(36), nullable=False)
    complete_flag = Column(NUMBER(1, 0, False), nullable=False)
    error_code = Column(VARCHAR(20), nullable=False)
    error_desc = Column(VARCHAR(500), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class SlaTransaction(Base):
    __tablename__ = 'crm_sla_transaction'
    __table_args__ = {'comment': 'giao dịch SLA'}

    id = Column('sla_transaction_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã giao dịch SLA')
    parent_id = Column('sla_parent_transaction_id', VARCHAR(36), comment='Mã id cha')
    sla_id = Column(ForeignKey('crm_sla.sla_id'), comment='Mã SLA')
    sla_name = Column(VARCHAR(50), comment='Tên giao dịch SLA')
    sla_deadline = Column(NUMBER(10, 0, False), comment='dealine')
    active_flag = Column(NUMBER(1, 0, False), comment='trạng thái')
    created_at = Column(DateTime, comment='ngày tạo')

    sla = relationship('Sla')


class TransactionStage(Base):
    __tablename__ = 'crm_transaction_stage'
    __table_args__ = {'comment': 'Giai đoạn giao dịch'}

    id = Column('transaction_stage_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã bước  giao dịch')
    status_id = Column('transaction_stage_status_id',
                       ForeignKey('crm_transaction_stage_status.transaction_stage_status_id'),
                       comment='Mã trạng thái của  giao dịch')
    lane_id = Column('transaction_stage_lane_id', ForeignKey('crm_transaction_stage_lane.transaction_stage_lane_id'),
                     comment='Mã thông tin đơn vị và phòng ban thực hiện')
    phase_id = Column('transaction_stage_phase_id',
                      ForeignKey('crm_transaction_stage_phase.transaction_stage_phase_id'),
                      comment='Mã giai đoạn')
    business_type_id = Column(ForeignKey('crm_business_type.business_type_id'), comment='Tên bước hiện')
    sla_transaction_id = Column(VARCHAR(36), comment='Mã bước thực hiện kiểu chữ(vd: IN, DUYET)')
    transaction_stage_phase_code = Column(VARCHAR(50), comment='Mã bước thực hiện kiểu chữ(vd: IN, DUYET)')
    transaction_stage_phase_name = Column(VARCHAR(250), comment='Tên bước hiện')
    responsible_flag = Column(NUMBER(1, 0, False), comment='Cờ người chịu trách nhiệm của bước thực hiện')
    action_id = Column(
        'transaction_stage_action_id',
        ForeignKey('crm_transaction_stage_action.transaction_stage_action_id'),
        comment='Mã hành động'
    )

    business_type = relationship('BusinessType')
    lane = relationship('TransactionStageLane')
    phase = relationship('TransactionStagePhase')
    status = relationship('TransactionStageStatus')
    action = relationship('TransactionStageAction')


class StagePhase(Base):
    __tablename__ = 'crm_stage_phase'
    __table_args__ = {'comment': '''Giai đoạn xử lý
                      1. Mở CIF
                      2. Upload giấy tờ
                      3. Ebank'''}

    phase_id = Column('phase_id', ForeignKey('crm_phase.phase_id'), comment='Mã Giai đoạn xử lý', primary_key=True)
    stage_id = Column('stage_id', ForeignKey('crm_stage.stage_id'), comment='Mã bước thực hiện', primary_key=True)
    phase = relationship("Phase")
    stage = relationship("Stage")


class StageLane(Base):
    __tablename__ = 'crm_stage_lane'
    __table_args__ = {'comment': '''Luồng xử lý
                        1. Phòng A
                        2. Phòng B
                        3. Khối A'''}

    lane_id = Column(
        'lane_id', ForeignKey('crm_lane.lane_id'), comment='Mã luồng xử lý của bước thực hiện', primary_key=True
    )
    stage_id = Column('stage_id', ForeignKey('crm_stage.stage_id'), comment='Mã bước  thực hiện', primary_key=True)
    branch_id = Column(
        'branch_id', VARCHAR(36), ForeignKey('crm_branch.branch_id'), comment='ID Chi nhánh', primary_key=True
    )
    department_id = Column('department_id', VARCHAR(36), nullable=False, comment='ID Phòng ban')

    lane = relationship('Lane')
    stage = relationship('Stage')
    branch = relationship('Branch')


class StageAction(Base):
    __tablename__ = 'crm_stage_action'
    id = Column(
        'stage_action_id', VARCHAR(36),
        primary_key=True, comment='Mã gen tự động hành động',
        server_default=text("sys_guid() ")
    )
    code = Column('stage_action_code', VARCHAR(50), nullable=False, comment='Mã hành động')
    name = Column('stage_action_name', VARCHAR(250), nullable=False, comment='Tên hành động')
    group_id = Column('stage_action_group_id', VARCHAR(36), comment='Nhóm hành động')
    status_id = Column(
        'stage_status_id', VARCHAR(36),
        ForeignKey('crm_stage_status.stage_status_id'),
        nullable=False, comment='Trạng thái hành động'
    )
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')

    status = relationship('StageStatus')


class TransactionStageAction(Base):
    __tablename__ = 'crm_transaction_stage_action'

    id = Column(
        'transaction_stage_action_id', VARCHAR(36),
        primary_key=True, comment='Mã gen tự động hành động',
        server_default=text("sys_guid() ")
    )
    code = Column('transaction_stage_action_code', VARCHAR(50), nullable=False, comment='Mã hành động')
    name = Column('transaction_stage_action_name', VARCHAR(250), nullable=False, comment='Tên hành động')
    group_id = Column('transaction_stage_action_group_id', VARCHAR(36), comment='Nhóm hành động')
    status_id = Column(
        'transaction_stage_status_id', VARCHAR(36),
        ForeignKey('crm_transaction_stage_status.transaction_stage_status_id'),
        comment='Trạng thái hành động', nullable=False
    )
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')

    status = relationship('TransactionStageStatus')
