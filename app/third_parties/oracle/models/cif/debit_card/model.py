from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.basic_information.model import (  # noqa
    Customer
)
from app.third_parties.oracle.models.master_data.address import (  # noqa
    AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.card import (  # noqa
    BrandOfCard, CardIssuanceFee, CardIssuanceType, CardType
)
from app.third_parties.oracle.models.master_data.customer import (  # noqa
    CustomerType
)
from app.third_parties.oracle.models.master_data.others import Branch  # noqa


class CardDeliveryAddress(Base):
    __tablename__ = 'crm_card_delivery_address'
    __table_args__ = {'comment': 'Địa chỉ giao nhận thẻ'}

    id = Column('card_delivery_address_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã địa chỉ giao nhận thẻv(PK)')
    branch_id = Column(VARCHAR(36), comment='Mã đơn vị (FK)')
    province_id = Column(ForeignKey('crm_address_province.province_id'), comment='Mã tỉnh (FK)')
    district_id = Column(ForeignKey('crm_address_district.district_id'),
                         comment='Mã Thông tin quận huyện (FK)')
    ward_id = Column(ForeignKey('crm_address_ward.ward_id'), comment='Mã Thông tin xã phường (FK)')
    card_delivery_address_address = Column(VARCHAR(500), comment='Địa chỉ')
    card_delivery_address_note = Column(VARCHAR(500), comment='Ghi chú')

    province = relationship('AddressProvince')
    district = relationship('AddressDistrict')
    ward = relationship('AddressWard')


class DebitCard(Base):
    __tablename__ = 'crm_debit_card'
    __table_args__ = {'comment': 'THẺ Ghi nợ'}

    id = Column('card_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='Mã thẻ (PK)')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), comment='Mã khách hàng')

    card_issuance_type_id = Column(ForeignKey('crm_card_issuance_type.card_issuance_type_id'),
                                   comment='Mã nơi phát hành Đối tượng khách hàng')
    customer_type_id = Column('cust_type_id', ForeignKey('crm_cust_type.cust_type_id'), comment=' Mã loại khách hàng')
    brand_of_card_id = Column(ForeignKey('crm_brand_of_card.brand_of_card_id'),
                              comment='Mã thương hiệu thẻ (Visa, master)')
    card_issuance_fee_id = Column(ForeignKey('crm_card_issuance_fee.card_issuance_fee_id'),
                                  comment='Mã Phí phát hành thẻ')
    card_delivery_address_id = Column(ForeignKey('crm_card_delivery_address.card_delivery_address_id'),
                                      comment='Mã địa chỉ giao nhận thẻv(PK)')
    parent_card_id = Column(ForeignKey('crm_debit_card.card_id'), comment='Mã thẻ cấp cha')
    card_registration_flag = Column(NUMBER(1, 0, False), comment='Trạng thái đk thẻ')
    payment_online_flag = Column(NUMBER(1, 0, False), comment='Trạng thái thanh toán')
    first_name_on_card = Column(VARCHAR(21), comment='Họ in trên thẻ')
    middle_name_on_card = Column(VARCHAR(21), comment='Tên đệm in trên thẻ')
    last_name_on_card = Column(VARCHAR(21), comment='Tên in trên thẻ')
    card_delivery_address_flag = Column(
        NUMBER(1, 0, False),
        comment='Trạng thái địa chỉ giao thẻ (0: giao tại đơn vị SCB, 1: địa chỉ tùy chọn)'
    )
    created_at = Column(DateTime, comment='ngày tạo')
    active_flag = Column(NUMBER(1, 0, False), comment='Trạng thái hoạt động (Có/không)')

    brand_of_card = relationship('BrandOfCard')
    card_delivery_address = relationship('CardDeliveryAddress')
    card_issuance_fee = relationship('CardIssuanceFee')
    card_issuance_type = relationship('CardIssuanceType')
    customer_type = relationship('CustomerType')
    customer = relationship('Customer')
    parent_card = relationship('DebitCard', remote_side=[id])
    approval_status = Column('approval_status', NUMBER(1, 0, False), nullable=False, default=0,
                             comment='Trạng thái phê duyệt thẻ ghi nợ')
    src_code = Column('card_src_code', VARCHAR(36), comment='Source Code loại thẻ')
    pro_code = Column('card_pro_code', VARCHAR(36), comment='Promote Code loại thẻ')
    card_group = Column('card_group', VARCHAR(36), comment='Loại thẻ')


class DebitCardType(Base):
    __tablename__ = 'crm_debit_card_type'
    __table_args__ = {'comment': 'LOẠI thẻ ghi nợ'}

    card_id = Column(ForeignKey('crm_debit_card.card_id'), primary_key=True, comment='Mã thẻ (PK)')
    card_type_id = Column(ForeignKey('crm_card_type.card_type_id'), primary_key=True, comment='Mã Đối tượng khách hàng')
    card_type = relationship('CardType')
    card = relationship('DebitCard')
