from sqlalchemy import CLOB, VARCHAR, Column, DateTime, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class Statistic(Base):
    __tablename__ = 'crm_ekyc_statistics'

    id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    customer_id = Column(VARCHAR(36), nullable=False, comment="Mã khách hàng (ekyc)")
    transaction_id = Column(VARCHAR(36), nullable=False, comment="Mã giao dịch")
    full_name = Column(VARCHAR(50), nullable=False, comment="Họ và tên khách hàng")
    cif = Column(VARCHAR(7), comment="Số CIF")
    phone_number = Column(VARCHAR(10), nullable=False, comment="Số điện thoại")
    document_id = Column(VARCHAR(15), nullable=False, comment="Số GTDD")
    document_type = Column(NUMBER(2), nullable=False, comment="Loại giấy tờ")
    status = Column(VARCHAR(20), nullable=False, comment="Trạng thái")
    status_id = Column(NUMBER(2, 0), comment="ID Trạng thái")
    trans_date = Column(DateTime, comment="Ngày giao dịch")
    ekyc_step = Column(VARCHAR(20), comment="Nghiệp vụ")
    kss_status = Column(VARCHAR(20), comment="Trạng thái kiểm soát sau")
    kss_status_id = Column(NUMBER(2, 0), comment="ID Trạng thái kiểm soát sau")
    date_kss = Column(DateTime, comment="Ngày kiểm soát sau")
    user_kss = Column(VARCHAR(15), comment="Người kiểm soát sau")
    approve_status = Column(VARCHAR(15), comment="Trạng thái phê duyệt")
    approve_status_id = Column(NUMBER(2, 0), comment="ID Trạng thái phê duyệt")
    date_approve = Column(DateTime, comment="Ngày phê duyệt")
    user_approve = Column(VARCHAR(15), comment="Người phê duyệt")
    transaction_data = Column(CLOB, comment='Transaction data')
    created_date = Column(DateTime, comment="Ngày tạo")
    updated_date = Column(DateTime, comment="Ngày cập nhập")
