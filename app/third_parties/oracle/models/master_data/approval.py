from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.others import (  # noqa
    StageStatus, TransactionStageStatus
)


class StageAction(Base):
    __tablename__ = 'crm_stage_action'

    id = Column('stage_action_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động hành động')
    code = Column('stage_action_code', VARCHAR(50), nullable=False, comment='Mã hành động')
    name = Column('stage_action_name', VARCHAR(250), nullable=False, comment='Tên hành động')
    group_id = Column('stage_action_group_id', VARCHAR(36), comment='Nhóm hành động')
    status_id = Column(
        ForeignKey('crm_stage_status.stage_status_id'), VARCHAR(36),
        nullable=False, comment='Trạng thái hành động'
    )
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')

    status = relationship('StageStatus')


class TransactionStageAction(Base):
    __tablename__ = 'crm_transaction_stage_action'

    id = Column('transaction_stage_action_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động hành động')
    code = Column('transaction_stage_action_code', VARCHAR(50), nullable=False, comment='Mã hành động')
    name = Column('transaction_stage_action_name', VARCHAR(250), nullable=False, comment='Tên hành động')
    group_id = Column('transaction_stage_action_group_id', VARCHAR(36), comment='Nhóm hành động')
    status_id = Column(
        ForeignKey('crm_transaction_stage_status.transaction_stage_status_id'), VARCHAR(36),
        nullable=False, comment='Trạng thái hành động'
    )
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')

    status = relationship('TransactionStageStatus')
