from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, LargeBinary, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base


class CustomerIdentity(Base):
    __tablename__ = 'crm_cust_identity'
    __table_args__ = {'comment': 'Bảng thông tin Giấy tờ định danh'}

    id = Column('identity_id', VARCHAR(36), primary_key=True, server_default=text("SYS_GUID() "),
                comment='Id Giấy tờ định danh')
    identity_type_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Loại giấy tờ định danh ')
    customer_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Khách hàng')
    # TODO: fix it
    identity_num = Column(VARCHAR(50), nullable=False, comment='Số Giấy tờ định danh')
    issued_date = Column(DateTime, nullable=False, comment='Ngày cấp')
    expired_date = Column(DateTime, nullable=False, comment='Ngày hết hạn')
    place_of_issue_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Nơi cấp')
    passport_type_id = Column(
        VARCHAR(36), comment='(FK) Id Loại hộ chiếu (Trên dòng mã máy quét). Not null nếu Id loại GTDD là Hộ chiếu'
    )
    passport_code_id = Column(
        VARCHAR(36), comment='(FK) Id Mã số hộ chiếu (Trên dòng mã máy quét). Not null nếu Id loại GTDD là Hộ chiếu'
    )
    primary_flag = Column(NUMBER(1, 0, False), comment='Cờ sử dụng làm giấy tờ định danh chính')
    mrz_content = Column(VARCHAR(500), comment='Nội dung MRZ. Not null nếu Id loại GTDD là Hộ chiếu')
    qrcode_content = Column(VARCHAR(500), comment='Nội dung QRCode. Not null nếu Id loại GTDD là Hộ chiếu')
    maker_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Người tạo')
    updater_at = Column(DateTime, comment='Ngày cập nhật')
    updater_id = Column(VARCHAR(36), comment='Người cập nhật')
    identity_number_in_passport = Column('identity_num_pp', VARCHAR(50), comment='Số CMND trong Hộ chiếu')
    signer = Column(VARCHAR(100), comment='Người ký GTDD')


class CustomerIdentityImage(Base):
    __tablename__ = 'crm_cust_identity_image'
    __table_args__ = {'comment': 'Thông tin hình ảnh định danh khách hàng'}

    id = Column('identity_image_id', VARCHAR(36), primary_key=True, server_default=text("""\
sys_guid()
"""), comment='(PK) Id Hình ảnh định danh')
    identity_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Giấy tờ định danh')
    image_type_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Loại giấy tờ định danh')
    image_url = Column(VARCHAR(200), nullable=False, comment='Đường dẫn hình')
    avatar_image_uuid = Column('AVATAR_IMAGE', nullable=False, comment='Đường dẫn hình avatar')
    hand_side_id = Column(VARCHAR(36),
                          comment='(FK) Id Loại bàn tay (trái phải). NotNull nếu Loại giấy tờ định danh là Vân tay')
    finger_type_id = Column(VARCHAR(36), comment='(FK) Id Loại ngón tay. NotNull nếu Loại giấy tờ định danh là Vân tay')
    vector_data = Column(
        LargeBinary,
        comment='dữ liệu ảnh vector vân tay/khuôn mặt. NotNull nếu Loại giấy tờ định danh là Vân tay/khuôn mặt'
    )
    active_flag = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                         comment='Cờ kích hoạt (Có/không tương ứng tick xanh đỏ)')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Mã người thực hiện')
    maker_at = Column(DateTime, nullable=False, comment='Thời gian thực hiện')
    updater_id = Column(VARCHAR(36), comment='Mã người cập nhật')
    updater_at = Column(DateTime, comment='Thời gian cập nhật')
    identity_image_front_flag = Column(NUMBER(1, 0, False),
                                       comment='Nếu giấy giờ tịnh danh là CMND:\n'
                                               'Giá trị 1: mặt trước\n'
                                               'Giá trị 0: mặt sau\n')

    ekyc_uuid = Column('ekyc_image_uuid', VARCHAR(36), comment='UUID hình trong hệ thống eKYC')
    ekyc_id = Column('ekyc_id', VARCHAR(36), comment='eKYC ID dùng cho các trường hợp compare')


class CustomerIdentityImageTransaction(Base):
    __tablename__ = 'crm_cust_identity_image_transaction'
    __table_args__ = {'comment': 'Lịch sử chỉnh sửa hình ảnh định danh'}

    id = Column('transaction_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id Lịch sử chỉnh sửa hình ảnh định danh')
    identity_image_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Hình ảnh thông tin định danh')
    image_url = Column(VARCHAR(200), nullable=False, comment='Đường dẫn hình ảnh')
    active_flag = Column(NUMBER(1, 0, False), comment='Trạng thái kích hoạt (Có/không tương ứng tick xanh đỏ)')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Người thực hiện')
    maker_at = Column(DateTime, nullable=False, comment='Ngày thực hiện')
    approved_id = Column('approver_id', VARCHAR(36), comment='Người duyệt')
    approved_at = Column('approver_at', DateTime, comment='Ngày duyệt')


class CustomerCompareImage(Base):
    __tablename__ = 'crm_cust_compare_image'
    __table_args__ = {'comment': 'Thông tin hình ảnh đối chiếu'}

    id = Column('compare_image_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id Thông tin hình ảnh đối chiếu '
                        '(Hình gốc được so sánh với hình ảnh upload bên crm_cust_identity_image)')
    identity_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Thông tin Giấy tờ định danh')
    identity_image_id = Column(ForeignKey('crm_cust_identity_image.identity_image_id'), nullable=False,
                               comment='(FK) ID Hình ảnh Giấy tờ định danh')
    compare_image_url = Column(VARCHAR(200), nullable=False, comment='Đường dẫn hình ảnh')
    similar_percent = Column(NUMBER(asdecimal=False), nullable=False, comment='Phần trăm tương đồng (range 0 - 100)')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Mã người thực hiện')
    maker_at = Column(DateTime, nullable=False, comment='Thời gian thực hiện')

    identity_image = relationship('CustomerIdentityImage')


class CustomerCompareImageTransaction(Base):
    __tablename__ = 'crm_cust_compare_image_transaction'
    __table_args__ = {'comment': 'Lịch sử chỉnh sửa hình ảnh đối chiếu'}

    id = Column('compare_transaction_id', VARCHAR(36), primary_key=True, server_default=text("""\
sys_guid()
"""), comment='(PK) Id Thay đổi hình ảnh đối chiếu giấy tờ định danh')
    compare_transaction_parent_id = Column(VARCHAR(36),
                                           comment='Id cấp cha Thay đổi hình ảnh đối chiếu giấy tờ định danh')
    compare_image_id = Column(
        VARCHAR(36), nullable=False,
        comment='(FK) Id Hình ảnh đối chiếu (Hình gốc được so sánh với hình ảnh upload bên crm_cust_identity_image)'
    )
    identity_image_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Hình ảnh giấy tờ định danh')
    compare_image_url = Column(VARCHAR(200), nullable=False, comment='Đường dẫn hình ảnh')
    similar_percent = Column(NUMBER(asdecimal=False), nullable=False, comment='Phần trăm tương đồng (range 0-100)')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Mã người thực hiện')
    maker_at = Column(DateTime, nullable=False, comment='Thời gian thực hiện')

    is_identity_compare = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                                 comment='Cờ đánh dấu giấy tờ nằm ở phần GTĐD')

    is_approved = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                         comment='Cờ đánh dấu giấy tờ đã duyệt')

    approved_id = Column('approver_id', VARCHAR(36), comment='Mã người duyệt')
    approved_at = Column('approver_at', DateTime, comment='Thời gian duyệt')


class CustomerSubIdentity(Base):
    __tablename__ = 'crm_cust_sub_identity'
    __table_args__ = {'comment': 'Giấy tờ định danh phụ'}

    id = Column('sub_identity_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id Giấy tờ định danh phụ')
    sub_identity_type_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Loại Giấy tờ định danh phụ')
    name = Column('sub_identity_name', VARCHAR(80), nullable=False, comment='Tên Giấy tờ định danh phụ')
    number = Column('sub_dentity_num', VARCHAR(36), nullable=False, comment='Số GTDD')
    symbol = Column('sub_identity_symbol', VARCHAR(10), comment='Ký hiệu')
    full_name = Column('sub_identity_full_name', VARCHAR(50), nullable=False, comment='Tên họ đầy đủ')
    date_of_birth = Column(DateTime, nullable=False, comment='Ngày sinh')
    passport_number = Column('passport_num', VARCHAR(50), nullable=False, comment='Số hộ chiếu')
    sub_identity_expired_date = Column(DateTime, nullable=False, comment='Ngày hết hạn')
    place_of_issue_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Nơi cấp')
    customer_id = Column(VARCHAR(36), nullable=False, comment='(FK) Id Thông tin khách hàng')
    maker_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    maker_id = Column(VARCHAR(36), nullable=False, comment='Người tạo')
    updater_at = Column(DateTime, comment='Ngày cập nhập')
    updater_id = Column(VARCHAR(36), comment='Người cập nhật')
    issued_date = Column(DateTime, nullable=False, comment='Ngày cấp')
