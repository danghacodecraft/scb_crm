from sqlalchemy import VARCHAR, Column
from sqlalchemy.dialects.oracle import NUMBER, DATE

from app.third_parties.oracle.base import Base


class Blacklist(Base):
    __tablename__ = 'crm_cust_blacklist'
    id = Column('id', NUMBER, primary_key=True, comment='id')
    full_name = Column('full_name', VARCHAR(30), nullable=True, comment='Họ và tên')
    date_of_birth = Column('date_of_birth', DATE, nullable=True, comment='Ngày sinh')
    identity_id = Column('identity_id', VARCHAR(50), nullable=False, comment='giấy tờ định danh')
    issued_date = Column('issued_date', DATE, nullable=True, comment='ngày cấp')
    place_of_issue_id = Column('place_of_issue_id', VARCHAR(500), nullable=True, comment='nơi cấp')
    cif_num = Column('cif_num', VARCHAR(10), nullable=True, comment='số cif')
    casa_account_num = Column('casa_account_num', VARCHAR(20), nullable=True, comment='tài khoản ngân hàng tại SCB')
    branch_id = Column('branch_id', VARCHAR(5), nullable=True, comment='Mã chi nhánh')
    date_open_account_number = Column('date_open_account_number', DATE, nullable=True, comment='ngày mở tài khoản')
    mobile_num = Column('mobile_num', VARCHAR(25), nullable=True,  comment='số điện thoại cá nhân')
    place_of_residence = Column('place_of_residence', VARCHAR(500), nullable=True, comment='Địa chỉ hộ khẩu')
    place_of_origin = Column('place_of_origin', VARCHAR(500), nullable=True, comment='nơi sinh')
    reason = Column('reason', VARCHAR(1000), nullable=True, comment='chuyên đề')
    job_content = Column('job_content', VARCHAR(500), nullable=True, comment='Nôi dung công việc')
    blacklist_source = Column('blacklist_source', VARCHAR(500), nullable=True, comment='nguồn')
    document_no = Column('document_no', VARCHAR(20), nullable=True, comment='Số công văn đến')
    blacklist_area = Column('blacklist_area', VARCHAR(500), nullable=True, comment='khu vực')
