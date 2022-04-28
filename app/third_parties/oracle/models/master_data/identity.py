from sqlalchemy import VARCHAR, Column, DateTime, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class ImageType(Base):
    __tablename__ = 'crm_image_type'
    __table_args__ = {'comment': 'Loại hình ảnh'}

    id = Column('image_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id loại hình ảnh định danh')
    code = Column('image_type_code', VARCHAR(50), nullable=False, comment='(UN) Mã code loại ảnh')
    name = Column('image_type_name', VARCHAR(255), nullable=False, comment='Tên loại ảnh')
    detail = Column('image_type_detail', VARCHAR(500), comment='Chi tiết loại ảnh')


class FingerType(Base):
    __tablename__ = 'crm_finger_type'
    __table_args__ = {'comment': 'Loại ngón tay trên bàn tay'}

    id = Column('finger_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Mã loại  vân tay')
    code = Column('finger_type_code', VARCHAR(50), nullable=False, comment='(UN) Mã code vân tay')
    name = Column('finger_type_name', VARCHAR(255), nullable=False, comment='Tên vân tay')
    order_no = Column(NUMBER(2, 0, False), comment='sắp xếp')


class HandSide(Base):
    __tablename__ = 'crm_hand_side'
    __table_args__ = {'comment': 'Loại bàn tay'}

    id = Column('hand_side_id', VARCHAR(36), primary_key=True, server_default=text("""\
sys_guid()
"""), comment='(PK) Id loại bàn tay')
    code = Column('hand_side_code', VARCHAR(50), nullable=False, comment='Mã bàn tay')
    name = Column('hand_side_name', VARCHAR(255), nullable=False, comment='Tên bàn tay')


class PassportCode(Base):
    __tablename__ = 'crm_passport_code'
    __table_args__ = {'comment': 'Mã số hộ chiếu'}

    id = Column('passport_code_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id số hộ chiếu')
    code = Column('passport_code_code', VARCHAR(50), nullable=False, comment='(PK) Mã số hộ chiếu')
    name = Column('passport_code_name', VARCHAR(255), nullable=False, comment='Tên số hộ chiếu')


class PassportType(Base):
    __tablename__ = 'crm_passport_type'
    __table_args__ = {'comment': 'Loại hộ chiếu'}

    id = Column('passport_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id loại hộ chiếu')
    code = Column('passport_type_code', VARCHAR(50), nullable=False, comment='Mã loại loại hộ chiếu')
    name = Column('passport_type_name', VARCHAR(255), nullable=False, comment='Tên loại hộ chiếu')


class CustomerIdentityType(Base):
    __tablename__ = 'crm_cust_identity_type'
    __table_args__ = {'comment': 'Loại giấy tờ định danh chính'}

    id = Column('identity_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Mã loại giấy tờ định danh')
    code = Column('identity_type_code', VARCHAR(50), nullable=False, comment='(UN) Mã code loại giấy tờ định danh')
    name = Column('identity_type_name', VARCHAR(255), nullable=False, comment='Tên loại loại giấy tờ định danh')
    updated_at = Column(DateTime, comment='Ngày cập nhập')


class CustomerIdentityDocumentType(Base):
    __tablename__ = 'crm_cust_identity_document_type'
    __table_args__ = {'comment': """Loại giấy tờ định danh Loại GTDD trả về là loại giấy tờ đã được server phân loại,
                        và có các giá trị tương ứng như sau:
                            \n`0` : Hộ chiếu.
                            \n`1` : Chứng minh nhân dân cũ (9 số).
                            \n`2` : Chứng minh nhân dân mới (12 số).
                            \n`3` : Căn cước công dân cũ (không gắn chíp).
                            \n`4` : Căn cước công dân mới (có gắn chíp)"""}

    identity_type_id = Column('identity_type_id', VARCHAR(36))
    id = Column('identity_document_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Mã loại giấy tờ định danh')
    code = Column('identity_document_type_code', VARCHAR(50), nullable=False, comment='(UN) Mã code loại giấy tờ định danh')
    name = Column('identity_document_type_name', VARCHAR(255), nullable=False, comment='Tên loại loại giấy tờ định danh')
    updated_at = Column(DateTime, comment='Ngày cập nhập')


class CustomerSubIdentityType(Base):
    __tablename__ = 'crm_cust_sub_identity_type'
    __table_args__ = {'comment': 'Loại giấy tờ định danh phụ'}

    id = Column('sub_identity_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Mã loại giấy tờ định danh phụ')
    code = Column('sub_identity_type_code', VARCHAR(50), nullable=False,
                  comment='(UN) Mã code loại giấy tờ định danh phụ')
    name = Column('sub_identity_type_name', VARCHAR(255), nullable=False, comment='Tên loại giấy tờ định danh phụ')
    active_flag = Column('sub_identity_type_active_flag', NUMBER(1, 0, False), comment='cờ hoạt động')
    created_at = Column(DateTime, nullable=False, server_default=text("""\
    sysdate
    """), comment='Ngày tạo')
    updated_at = Column(DateTime, nullable=False, comment='Ngày cập nhật')
    order_no = Column(NUMBER(2, 0, False), nullable=False, comment='Sắp xếp')


class PlaceOfIssue(Base):
    __tablename__ = 'crm_place_of_issue'
    __table_args__ = {'comment': 'Nơi cấp giấy tờ định danh'}

    id = Column('place_of_issue_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id nơi phát hành/Nơi cấp Giấy tờ định danh')
    country_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id quốc gia')
    code = Column('place_of_issue_code', VARCHAR(50), server_default=text("null "), comment='Mã nơi phát hành/Nơi cấp')
    name = Column('place_of_issue_name', VARCHAR(255), nullable=False, comment='Tên nơi phát hành/Nơi cấp')
