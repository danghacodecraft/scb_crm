from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.account import (  # noqa
    AccountClass, AccountStructureType, AccountType
)
from app.third_parties.oracle.models.master_data.others import (  # noqa
    Currency, HrmEmployee
)


class CasaAccount(Base):
    __tablename__ = 'crm_casa_account'
    __table_args__ = {'comment': 'Tài khoản Thanh toán'}

    id = Column('casa_account_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã tài khoản thanh toán')
    customer_id = Column(VARCHAR(36), nullable=False, comment='Mã khách hàng')
    case_account_number = Column('case_account_num', VARCHAR(16), nullable=False, comment='Số tài khoản thanh toán')
    currency_id = Column(ForeignKey('crm_currency.currency_id'), nullable=False, comment='Mã tiền tệ')
    acc_type_id = Column(ForeignKey('crm_acc_type.acc_type_id'), nullable=False,
                         comment='Mã loại nhóm sản phẩm (gói) tài khoản')
    acc_class_id = Column(ForeignKey('crm_acc_class.acc_class_id'), nullable=False, comment='Mã loại hình tài khoản')
    acc_structure_type_id = Column('acc_structrure_type_id',
                                   ForeignKey('crm_acc_structure_type.acc_structure_type_id'), nullable=False,
                                   comment='Mã loại kết cấu tài khoản')
    staff_type_id = Column(VARCHAR(36), nullable=False, comment='Mã Danh mục Loại nhân viên giới thiệu')
    acc_salary_org_name = Column(VARCHAR(100), comment='Tên tài khoản chi lương nguồn')
    acc_salary_org_acc = Column(VARCHAR(100), comment='Số tài khoản chi lương nguồn')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Mã người thực hiện')
    maker_at = Column(DateTime, nullable=False, comment='Thời gian thực hiện')
    checker_id = Column(VARCHAR(36), nullable=False, comment='Mã người duyệt')
    checker_at = Column(DateTime, comment='Thời gian duyệt')
    approve_status = Column(VARCHAR(3), comment='Trạng thái duyệt')
    self_selected_account_flag = Column(NUMBER(1, 2, True), comment='Loại Tài khoản tự chọn')
    acc_active_flag = Column(NUMBER(1, 2, True), comment='Cờ kích hoạt tài khoản')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Thời gian cập nhật')

    account_class = relationship('AccountClass')
    account_structure_type = relationship('AccountStructureType')
    account_type = relationship('AccountType')
    currency = relationship('Currency')


# class CrmCasaAccountEmployee(CrmStaffType):
class CasaAccountEmployee(Base):
    __tablename__ = 'crm_casa_account_employee'
    __table_args__ = {'comment': 'KPI Tài khoản thanh toán'}

    staff_type_id = Column(ForeignKey('crm_staff_type.staff_type_id'), primary_key=True,
                           comment='mã Danh mục Loại nhân viên giới thiệu')
    employee_id = Column(ForeignKey('hrm_employee.id'), nullable=False, comment='Mã nhân viên')
    casa_account_id = Column(ForeignKey('crm_casa_account.casa_account_id'), nullable=False,
                             comment='Tài khoản thanh toán')
    effective_kpi_at = Column(DateTime, nullable=False, comment='Ngày hiệu lực')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')

    casa_account = relationship('CasaAccount')
    employee = relationship('HrmEmployee')


class JointAccountHolder(Base):
    __tablename__ = 'crm_joint_account_holder'
    __table_args__ = {'comment': 'Thông tin đồng chủ sở hữu'}

    id = Column('joint_account_holder_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Thông tin đồng chủ sở hữu')
    cif_num = Column(VARCHAR(9), nullable=False, comment='Mã Khách hàng')
    casa_account_id = Column(ForeignKey('crm_casa_account.casa_account_id'), nullable=False,
                             comment='Số tài khoản hiện tại')
    joint_account_holder_flag = Column(NUMBER(1, 2, True), comment='Cờ đồng sở hữu tài khoản')
    joint_account_holder_no = Column(NUMBER(4, 2, True), comment='Số thứ tự tài khoản người đồng sở hữu')

    casa_account = relationship('CasaAccount')


class AgreementAuthorization(Base):
    __tablename__ = 'crm_agreement_authorization'
    __table_args__ = {'comment': 'Thông tin Thỏa thuận - ủy quyền'}

    id = Column('agreement_author_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID chính')
    code = Column('agreement_author_code', VARCHAR(50), comment='Mã code')
    name = Column('agreement_author_name', VARCHAR(1000), comment='Tên ủy quyền')
    method_sign = Column(NUMBER(1, 2, True), comment='Phương thức kí')
    agreement_flag = Column(NUMBER(1, 2, True), comment='Cờ ủy quyền')
    active_flag = Column('agreement_active_flag', NUMBER(1, 2, True), comment='Cờ trạng thái kích hoạt')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')


class JointAccountHolderAgreementAuthorization(Base):
    __tablename__ = 'crm_joint_acc_agree'
    __table_args__ = {'comment': 'Thỏa thuận/ ủy quyền đồng sở hữu'}

    agreement_authorization_id = Column('agreement_author_id',
                                        ForeignKey('crm_agreement_authorization.agreement_author_id'), primary_key=True,
                                        server_default=text("sys_guid() "), comment='Mã thỏa thuận - ủy quyền')
    joint_account_holder_id = Column('joint_account_holder_id',
                                     ForeignKey('crm_joint_account_holder.joint_account_holder_id'),
                                     comment='Mã Thông tin đồng chủ sở hữu'),

    agreement_authorization = relationship('AgreementAuthorization')
    joint_account_holder = relationship('JointAccountHolder')
