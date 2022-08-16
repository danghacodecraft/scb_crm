from sqlalchemy import VARCHAR, Column, text

from app.third_parties.oracle.base import Base


class BrandOfCard(Base):
    __tablename__ = 'crm_brand_of_card'
    __table_args__ = {'comment': 'Thương hiệu thẻ'}

    id = Column('brand_of_card_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã thương hiệu thẻ (PK)')
    code = Column('brand_of_card_code', VARCHAR(50), nullable=False, comment='Mã code thương hiệu thẻ')
    name = Column('brand_of_card_name', VARCHAR(255), nullable=False, comment='Tên thương hiệu thẻ')
    logo_url = Column('brand_of_card_logo_url', VARCHAR(500), nullable=False, comment='Url logo thương hiệu thẻ')
    image_url = Column('brand_of_card_img_url', VARCHAR(500), nullable=False, comment='Url hình thẻ mẫu')


class CardIssuanceFee(Base):
    __tablename__ = 'crm_card_issuance_fee'
    __table_args__ = {'comment': 'Phí phát hành thẻ'}

    id = Column('card_issuance_fee_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    code = Column('card_issuance_fee_code', VARCHAR(50), nullable=False)
    name = Column('card_issuance_fee_name', VARCHAR(255), nullable=False)


class CardIssuanceType(Base):
    __tablename__ = 'crm_card_issuance_type'
    __table_args__ = {'comment': 'Hình thức phát hành thẻ'}

    id = Column('card_issuance_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Hình thức phát hành thẻ (PK)')
    code = Column('card_issuance_type_code', VARCHAR(50), nullable=False, comment='Mã code Hình thức phát hành thẻ')
    name = Column('card_issuance_type_name', VARCHAR(255), nullable=False, comment='Tên Hình thức phát hành thẻ')


class CardCustomerType(Base):
    __tablename__ = 'crm_card_cust_type'
    __table_args__ = {'comment': 'Nhóm khách hàng dùng cho thẻ ghi nợ'}

    id = Column('card_cust_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Nhóm khách hàng (PK)')
    code = Column('card_cust_type_code', VARCHAR(50), nullable=False, comment='Mã code Nhóm khách hàng')
    name = Column('card_cust_type_name', VARCHAR(255), nullable=False, comment='Tên Nhóm khách hàng')


class CardType(Base):
    __tablename__ = 'crm_card_type'
    __table_args__ = {'comment': 'Loại thẻ (tính vật lý: vật lý, phi vạt lý)'}

    id = Column('card_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Loại thẻ (PK)')
    code = Column('card_type_code', VARCHAR(50), nullable=False, comment='Mã code Loại thẻ')
    name = Column('card_type_name', VARCHAR(255), nullable=False, comment='Tên Loại thẻ')
