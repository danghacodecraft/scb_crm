from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.address import (  # noqa
    AddressCountry
)
from app.third_parties.oracle.models.master_data.customer import (  # noqa
    CustomerCategory, CustomerClassification, CustomerEconomicProfession,
    CustomerStatus, CustomerType
)
from app.third_parties.oracle.models.master_data.others import (  # noqa
    Channel, KYCLevel
)


class Customer(Base):
    __tablename__ = 'crm_customer'

    id = Column('customer_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động khách hàng')
    cif_number = Column('cif_num', VARCHAR(9), unique=True, comment='Mã khách hàng')
    full_name = Column(VARCHAR(105), nullable=False, comment='Tên đầy đủ không dấu')
    full_name_vn = Column(VARCHAR(105), nullable=False, comment='Tên đầy đủ có dấu')
    first_name = Column(VARCHAR(105), nullable=False, comment='Tên')
    middle_name = Column(VARCHAR(105), comment='Tên lót')
    last_name = Column(VARCHAR(105), nullable=False, comment='Họ')
    short_name = Column(VARCHAR(105), nullable=False, comment='Tên viết tắt')
    email = Column(VARCHAR(100), comment='Email')
    telephone_number = Column('telephone_num', VARCHAR(12), comment='Số điện thoại bàn')
    mobile_number = Column('mobile_num', VARCHAR(10), comment='Số điện thoại di động')
    fax_number = Column('fax_num', VARCHAR(10), comment='Số fax')
    tax_number = Column('tax_num', VARCHAR(100), comment='Số tax')
    self_selected_cif_flag = Column(NUMBER(1, 0, False), nullable=False, comment='Cờ cif thông thường/ tự chọn')
    legal_agreement_flag = Column(NUMBER(1, 0, False), comment='Cờ thỏa thuận pháp lý (có/không)')
    advertising_marketing_flag = Column(NUMBER(1, 0, False), comment='Cờ nhận quảng cáo từ SCB ( có/không)')
    customer_relationship_flag = Column('cust_relationship_flag', NUMBER(1, 0, False),
                                        comment='Cờ mối quan hệ khách hàng (có/không)')
    active_flag = Column(NUMBER(1, 0, False), nullable=False, comment='Cờ trạng thái hoạt động')
    open_cif_at = Column(DateTime, nullable=False, comment='Ngày mở Cif')
    open_branch_id = Column(VARCHAR(36), nullable=False, comment='Mã Thông tin đơn vị kinh doanh theo FCC')
    kyc_level_id = Column(ForeignKey('crm_kyc_level.kyc_level_id'), nullable=False, comment='Cấp độ KYC')
    customer_type_id = Column('cust_type_id', ForeignKey('crm_cust_type.cust_type_id'), comment='Mã loại khách hàng')
    customer_category_id = Column('cust_category_id', ForeignKey('crm_cust_category.cust_category_id'),
                                  comment='Mã đối tượng khách hàng')
    customer_economic_profession_id = Column('economic_profession_id',
                                             ForeignKey('crm_cust_economic_profession.cust_economic_profession_id'),
                                             comment='Mã ngành nghề kinh tế')
    nationality_id = Column(ForeignKey('crm_address_country.country_id'), nullable=False, comment='Mã quốc tịch')
    customer_classification_id = Column('cust_classification_id',
                                        ForeignKey('crm_cust_classification.cust_classification_id'),
                                        nullable=False, comment='Mã phân hạng khách hàng')
    customer_professional_id = Column('cust_professional_id', VARCHAR(36), nullable=False,
                                      comment='Mã nghề nghiệp khách hàng')
    customer_status_id = Column('cust_status_id',
                                ForeignKey('crm_customer_status.cust_status_id'),
                                nullable=False, comment='Mã Trạng thái khách hàng: đóng băng, mở')
    channel_id = Column(ForeignKey('crm_channel.channel_id'), nullable=False, comment='Mã kênh tạo khách hàng')
    avatar_url = Column(VARCHAR(100), comment='Đường dẫn hình ảnh đại diện')
    complete_flag = Column(NUMBER(1, 0, False), comment='Tạo CIF thành công')

    grade_name = Column(VARCHAR(100), comment='Xếp hạng tín dụng Khách hàng')

    channel = relationship('Channel')
    customer_category = relationship('CustomerCategory')
    customer_classification = relationship('CustomerClassification')
    customer_status = relationship('CustomerStatus')
    customer_type = relationship('CustomerType')
    customer_economic_profession = relationship('CustomerEconomicProfession')
    kyc_level = relationship('KYCLevel')
    nationality = relationship('AddressCountry')
