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
    casa_account_number = Column('casa_account_num', VARCHAR(16), nullable=False, comment='Số tài khoản thanh toán')
    currency_id = Column(ForeignKey('crm_currency.currency_id'), nullable=False, comment='Mã tiền tệ')
    acc_type_id = Column(ForeignKey('crm_acc_type.acc_type_id'), nullable=False,
                         comment='Mã loại nhóm sản phẩm (gói) tài khoản')
    acc_class_id = Column(ForeignKey('crm_acc_class.acc_class_id'), nullable=False, comment='Mã loại hình tài khoản')
    acc_structure_type_id = Column('acc_structrure_type_id',
                                   ForeignKey('crm_acc_structure_type.acc_structure_type_id'), nullable=True,
                                   comment='Mã loại kết cấu tài khoản')
    staff_type_id = Column(VARCHAR(36), nullable=False, comment='Mã Danh mục Loại nhân viên giới thiệu')
    acc_salary_org_name = Column(VARCHAR(100), comment='Tên tài khoản chi lương nguồn')
    acc_salary_org_acc = Column(VARCHAR(100), comment='Số tài khoản chi lương nguồn')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Mã người thực hiện')
    maker_at = Column(DateTime, nullable=False, comment='Thời gian thực hiện')
    checker_id = Column(VARCHAR(36), nullable=False, comment='Mã người duyệt')
    checker_at = Column(DateTime, comment='Thời gian duyệt')
    approve_status = Column(NUMBER(10), comment='Trạng thái duyệt, 0: Thất bại, 1: Thành công')
    self_selected_account_flag = Column(NUMBER(1, 0, False), comment='Loại Tài khoản tự chọn')
    acc_active_flag = Column(NUMBER(1, 0, False), comment='Cờ kích hoạt tài khoản')
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

    joint_account_holder_id = Column('joint_account_holder_id', VARCHAR(36), primary_key=True,
                                     server_default=text("sys_guid() "),
                                     comment='Mã Thông tin đồng chủ sở hữu')
    cif_num = Column(VARCHAR(9), nullable=False, comment='Mã Khách hàng')
    relationship_type_id = Column(ForeignKey('crm_cust_relationship_type.cust_relationship_type_id'), nullable=False,
                                  comment='Mối quan hệ với khách hàng hiện tại')
    joint_account_holder_no = Column(NUMBER(4, 2, True), comment='Số thứ tự tài khoản người đồng sở hữu')
    joint_acc_agree_id = Column('join_acc_agree_id', ForeignKey('crm_joint_acc_agree.joint_acc_agree_id'),
                                comment='Mã thỏa thuận/ ủy quyền đồng sở hữu')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')


class AgreementAuthorization(Base):
    __tablename__ = 'crm_agreement_authorization'
    __table_args__ = {'comment': 'Thông tin Thỏa thuận - ủy quyền'}

    id = Column('agreement_author_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID chính')
    code = Column('agreement_author_code', VARCHAR(50), comment='Mã code')
    name = Column('agreement_author_name', VARCHAR(1000), comment='Tên ủy quyền')
    active_flag = Column('agreement_active_flag', NUMBER(1, 2, True), comment='Cờ trạng thái kích hoạt')

    agreement_author_type = Column('agreement_author_type', VARCHAR(20), comment='Loại tài khoản thỏa thuận ủy quyền (FD, DD, CSD, TD)')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')


class JointAccountHolderAgreementAuthorization(Base):
    __tablename__ = 'crm_joint_acc_agree'
    __table_args__ = {'comment': 'Thỏa thuận/ ủy quyền đồng sở hữu'}

    joint_acc_agree_id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    active_flag = Column(NUMBER(1, 0, False), nullable=False, comment="Trạng thái thỏa thuận/ ủy quyền")
    casa_account_id = Column(VARCHAR(36), nullable=False, comment="Số tài khoản hiện tại")
    in_scb_flag = Column(NUMBER(1), comment="Cờ đánh dấu văn bản trong hay ngoài SCB")
    joint_acc_agree_document_file_id = Column(ForeignKey('crm_document_file.document_file_id'),
                                              comment="Id  mã loại thẻ")
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')
    end_date = Column(DateTime, comment='Ngày kết thúc')
    joint_acc_agree_document_no = Column(VARCHAR(100), comment="Số văn bản")
    joint_acc_agree_document_address = Column(VARCHAR(255), nullable=False, comment="Thông tin địa chỉ")


class MethodSign(Base):
    __tablename__ = 'crm_method_sign'
    __table_args__ = {'comment': 'Thông tin phương thức ký'}

    id = Column('method_sign_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    method_sign_type = Column(NUMBER(2), nullable=False, comment="Phương thức ký (1, 2, 3)")
    agreement_author_id = Column(VARCHAR(36), comment="Mã thông tin thỏa thuận - ủy quyền")
    joint_acc_agree_id = Column(VARCHAR(36), comment="Mã thỏa thuận - ủy quyền")
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')
    agreement_flag = Column(NUMBER(1, 0, False), nullable=False, comment="Đánh dấu đồng ý nội dung")
    agree_join_acc_cif_num = Column(VARCHAR(7), nullable=True, comment="Số CIF tài khoản tham gia ký văn bản đồng ý Chủ sở hữu")
    agree_join_acc_name = Column(VARCHAR(100), nullable=True, comment="Tên tài khoản tham gia ký văn bản đồng ý Chủ sở hữu")
