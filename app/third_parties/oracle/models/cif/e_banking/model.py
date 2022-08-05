from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.basic_information.model import (  # noqa
    Customer
)
from app.third_parties.oracle.models.master_data.customer import (  # noqa
    CustomerContactType
)
from app.third_parties.oracle.models.master_data.e_banking import (  # noqa
    EBankingNotification
)
from app.third_parties.oracle.models.master_data.others import (  # noqa
    MethodAuthentication
)


class TdAccount(Base):
    __tablename__ = 'crm_td_account'
    __table_args__ = {'comment': 'Tài khoản Tiết kiệm'}

    id = Column('td_account_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Tài khoản Tiết kiệm')
    customer_id = Column(VARCHAR(36), comment='Mã khách hàng')
    td_account_number = Column('td_account_num', VARCHAR(16), comment='Số tài khoản tiết kiệm,')
    currency_id = Column(VARCHAR(36), comment='Danh mục loại tiền')
    account_type_id = Column('acc_type_id', VARCHAR(36), comment='Loại nhóm sản phẩm (gói) tài khoản')
    account_class_id = Column('acc_class_id', VARCHAR(36), comment='Loại hình tài khoản')
    maker_id = Column(VARCHAR(36), comment='người thực hiện')
    maker_at = Column(DateTime, comment='ngày thực hiện')
    checker_id = Column(VARCHAR(36), comment='người phê duyệt')
    checker_at = Column(DateTime, comment='ngày phê duyệt')
    approve_status = Column('approve_status', NUMBER(1, 0, False), server_default=text("0 "), comment='trạng phái phê duyệt')
    active_flag = Column('acc_active_flag', NUMBER(1, 0, False), comment='trạng thái hoạt động')
    updated_at = Column(DateTime, comment='ngày cập nhật')
    amount = Column('amount', NUMBER(), comment='Số dư hiện tại')
    pay_in_amount = Column('pay_in_amount', NUMBER(), comment='Thông tin nguồn tiền đầu vào')
    pay_in_casa_account = Column('pay_in_casa_account', VARCHAR(36), comment='Tài khoản nguồn tiền đầu vào')
    pay_out_interest_casa_account = Column('pay_out_interest_casa_account', VARCHAR(36), comment='Tài khoản nhận lãi')
    pay_out_casa_account = Column('pay_out_casa_account', VARCHAR(36), comment='Tài khoản nhận gốc')
    td_contract_num = Column('td_contract_num', VARCHAR(50), comment='Số hợp đồng')
    fcc_transaction_num = Column('fcc_transaction_num', VARCHAR(100), comment='Số bút toán (FCC)')
    maturity_date = Column(DateTime, nullable=False, comment='Ngày đáo hạn')
    td_serial = Column('td_serial', VARCHAR(20), comment='Số serial')
    td_interest_type = Column('td_interest_type', VARCHAR(20), comment='Hình thức lãi')
    td_interest = Column('td_interest', VARCHAR(5), comment='Lãi suất tiết kiệm (%)')
    td_rollover_type = Column('td_rollover_type', VARCHAR(2), comment='Chỉ định khi đến hạn:I = Tái ký gốc + lãi ,P = Tái ký gốc')
    pay_in_type = Column('pay_in_type', VARCHAR(36), comment='Phương thức hạch toán (Tiền mặt, TKTT, TK treo đơn vị)')


class TdAccountResign(Base):
    __tablename__ = 'crm_td_account_resign'
    __table_args__ = {'comment': 'Thông tin tái ký'}

    id = Column('td_account_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Liên kết với tài khoản tiết kiệm')
    pay_out_casa_account_resign = Column('pay_out_casa_account', VARCHAR(36), comment='Tài khoản nhận lãi')
    td_interest_class_resign = Column('td_interest_class', VARCHAR(36), comment='Hình thức lãi')
    acc_class_id_resign = Column('acc_class_id', VARCHAR(50), comment='Loại hình tài khoản')
    acc_type_id_resign = Column('acc_type_id', VARCHAR(50), comment='Loại nhóm sản phẩm (gói) tài khoản')


class TdInterestType(Base):
    __tablename__ = 'crm_td_interest_type'
    __table_args__ = {'comment': 'Hình thức lãi'}

    id = Column('td_interest_type_id', VARCHAR(50), primary_key=True, comment='ID hình thức lãi')
    code = Column('td_interest_type_code', VARCHAR(50), comment='Code hình thức lãi')
    name = Column('td_interest_type_name', VARCHAR(50), comment='Name hình thức lãi')


class EBankingReceiverNotificationRelationship(Base):
    __tablename__ = 'crm_eb_receiver_noti_relationship'
    __table_args__ = {'comment': 'Mối quan hệ thông tin nhận thông báo: Bố mẹ,vợ chồng,...'}

    id = Column('reg_receiver_noti_relationship_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Mối quan hệ thông tin nhận thông báo: Bố mẹ,vợ chồng,...')
    e_banking_register_balance_casa_id = Column('eb_reg_balance_casa_id', VARCHAR(36), nullable=False,
                                                comment='Mã Đăng ký Biến động số dư các loại tài khoản Thanh toán')
    relationship_type_id = Column(VARCHAR(36), nullable=False, comment='Mã Quan hệ khách hàng')
    mobile_number = Column('mobile_num', VARCHAR(10), nullable=False, comment='Số Điện thoại')
    full_name = Column(VARCHAR(100), nullable=False, comment='Tên đầy đủ')


class EBankingInfoAuthentication(Base):
    __tablename__ = 'crm_eb_info_authen'
    __table_args__ = {'comment': 'Liên kết thông tin tài khoản ib với hình thức xác thực'}

    id = Column('eb_info_authen_id', primary_key=True, comment='Liên kết thông tin tài khoản ib với hình thức xác thực')
    e_banking_info_id = Column('eb_info_id', ForeignKey('crm_ebanking_info.eb_info_id'),
                               comment='Liên kết thông tin tài khoản ib với hình thức xác thực')
    method_authentication_id = Column('method_authen_id', ForeignKey('crm_method_authen.method_authen_id'),
                                      comment='Danh mục Hình thức xác thực Vân tay Khuôn mặt SMS SOFT TOKEN HARD TOKEN')


class EBankingInfo(Base):
    __tablename__ = 'crm_ebanking_info'
    __table_args__ = {'comment': 'Thông tin e-banking'}

    id = Column('eb_info_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Thông tin e-banking')
    customer_id = Column(VARCHAR(36), comment='Mã khách hàng')
    method_active_password_id = Column('eb_method_active_pw_id', VARCHAR(36),
                                       comment='Hình thức nhận mật khẩu kích hoạt lần đầu')
    account_name = Column('eb_account_name', VARCHAR(100), comment='Tên đăng nhập')
    note = Column('eb_note', VARCHAR(1000), comment='Ghi chú nội dungg')
    approval_status = Column(NUMBER(1, 0, False), comment='Tình trạng phê duyệt')
    method_payment_fee_flag = Column('eb_method_payment_fee_flag', NUMBER(1, 0, False),
                                     comment='Cờ thanh toán phí tiền mặt - chuyển khoản')
    reset_password_flag = Column('eb_reset_password_flag', NUMBER(1, 0, False), comment='Cờ tùy chọn reset password')
    active_account_flag = Column('eb_active_account_flag', NUMBER(1, 0, False),
                                 comment='Cờ tùy chọn trạng thái kích hoạt ebanking')
    account_payment_fee = Column('eb_account_payment_fee', VARCHAR(50), comment='Số tài khoản thanh toán phí')


class EBankingRegisterBalance(Base):
    __tablename__ = 'crm_eb_reg_balance'
    __table_args__ = {'comment': '(Đăng ký Biến động số dư các loại tài khoản Thanh toán/ Tiết kiệm)'}

    id = Column('eb_reg_balance_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Đăng ký Biến động số dư các loại tài khoản ')
    account_id = Column(VARCHAR(36), comment='Số tài khoản ')
    e_banking_register_account_type = Column('eb_reg_account_type', VARCHAR(50),
                                             comment='Loại tài khoản ( tài khoản tiết kiệm, tài khoản thanh tóan, ..)')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), comment='Mã khách hàng')
    name = Column('eb_reg_balance_name', VARCHAR(100), comment='Tên Đăng ký Biến động số dư các loại tài khoản ')
    mobile_number = Column('mobile_num', VARCHAR(10), comment='Số điện thoại')
    full_name = Column(VARCHAR(100), comment='Tên đầy đủ')

    customer = relationship('Customer')


class EBankingRegisterBalanceNotification(Base):
    __tablename__ = 'crm_eb_reg_balance_noti'
    __table_args__ = {'comment': 'Tùy chọn thông báo - Tài khoản thanh toán/TKTK'}

    id = Column('eb_reg_balance_casa_noti_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    # e_banking_register_account_type = Column('eb_reg_account_type', VARCHAR(50), nullable=False,
    #                                          comment='Loại tài khoản ( tài khoản tiết kiệm, tài khoản thanh tóan, ..)')
    # customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    eb_notify_id = Column(ForeignKey('crm_eb_notification.eb_notify_id'), nullable=False,
                          comment='Mã Danh mục tùy chọn thông báo')
    eb_reg_balance_id = Column(ForeignKey('crm_eb_reg_balance.eb_reg_balance_id'), nullable=False, comment='ID Bảng Đăng ký Biến động số dư các loại tài khoản Thanh toán/ Tiết kiệm')

    # customer = relationship('Customer')
    e_banking_notify = relationship('EBankingNotification')
    eb_reg_balance = relationship('EBankingRegisterBalance')


class EBankingRegisterBalanceOption(Base):
    __tablename__ = 'crm_eb_reg_balance_option'
    __table_args__ = {'comment': '(Hình thức thông báo: OTT, SMS của TKTT/TKTK)'}

    id = Column('eb_reg_balance_option_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    customer_contact_type_id = Column('cust_contact_type_id',
                                      ForeignKey('crm_cust_contact_type.cust_contact_type_id'), nullable=False,
                                      comment='Mã loại xác thực ( ott/sms/token,..)')
    e_banking_register_account_type = Column('eb_reg_account_type', VARCHAR(50), nullable=False,
                                             comment='Loại tài khoản ( tài khoản tiết kiệm, tài khoản thanh tóan, ..)')
    created_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')

    customer_contact_type = relationship('CustomerContactType')
    customer = relationship('Customer')


class EBankingResetPassword(Base):
    __tablename__ = 'crm_ebanking_reset_pass'
    __table_args__ = {'comment': 'Cấp lại mật khẩu e-banking'}

    id = Column('eb_reset_pass_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Cấp lại mật khẩu e-banking')
    e_banking_info_id = Column('eb_info_id', ForeignKey('crm_ebanking_info.eb_info_id'),
                               comment='Mã Thông tin e-banking')
    e_banking_method_new_password_id = Column('eb_method_new_pass_id', VARCHAR(36),
                                              comment='Mã Id  tạo pass mới ')
    upload_file_url = Column(VARCHAR(1000), comment='đường dẫn url')
    conclusion_flag = Column(NUMBER(1, 0, False), comment='Trạng thái thực hiện yêu cầu')
    conclusion_note = Column(VARCHAR(1000), comment='Ghi chú')

    eb_info = relationship('EBankingInfo')
