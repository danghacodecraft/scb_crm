from sqlalchemy import CLOB, VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.others import (  # noqa
    BusinessType, Lane
)


class Comment(Base):
    __tablename__ = 'crm_comment'

    id = Column('comment_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động bình luận'
                )
    content = Column('content', VARCHAR(500), comment='Nội dung bình luận')
    parent_id = Column('comment_parent_id', VARCHAR(36), comment='Comment cha')
    assign_ids = Column('assign_user_ids', CLOB, comment='Danh sách người được nhắc trong comment')
    user_id = Column('user_id', VARCHAR(36), comment='Mã user tạo tin')
    user_name = Column('user_name', VARCHAR(255), comment='Tên user tạo tin')
    branch_id = Column(VARCHAR(36), comment='Mã đơn vị')
    branch_code = Column(VARCHAR(10), comment='Mã code đơn vị')
    branch_name = Column(VARCHAR(100), comment='Tên đơn vị')
    file_uuid = Column(VARCHAR(36), comment='File')
    lane_id = Column(ForeignKey('crm_lane.lane_id'), comment="ID luồng xử lý")
    business_type_id = Column(ForeignKey('crm_business_type.business_type_id'), comment="Tên bước thực hiện")
    active_flag = Column('active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')

    lane = relationship('Lane')
    business_type = relationship('BusinessType')
