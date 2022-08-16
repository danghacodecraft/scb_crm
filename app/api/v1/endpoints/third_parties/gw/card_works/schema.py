from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class OpenCardsCifInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số CIF",
                         example="4218356")


class OpenCardsAccountInfoRequest(BaseSchema):
    account_type: str = Field(...,
                              description="""Loại tài khoản
- 3 : LOCAL CREDIT ACCOUNT PROVIDER.

- 5: PREPAID CARD ACCOUNT PROVIDER.

- 2 : ATM CARD ACCOUNT PROVIDER.

- 8: MC/VS CREDIT CARD ACCOUNT PROVIDER.""",
                              example="2")


class OpenCardsCardInfoRequest(BaseSchema):
    card_indicator: str = Field(..., description="Loại thẻ. Thẻ chính: 'B', thẻ phụ: 'S'",
                                example="B")
    card_type: str = Field(..., description="Chương trình thẻ. Mặc định: MDP",
                           example="MDP")
    card_auto_renew: str = Field(...,
                                 description="""Hỗ trợ gia hạn thẻ.
- Giá trị 'Y': Có.

- giá trị 'N' : không""",
                                 example="N")
    card_release_form: str = Field(..., description=""""Hình thức mở thẻ.
- 'Q' ; Quick - Phát hành nhanh

- 'N' : Normal - Phát hành thường""",
                                   example="Q")
    card_block_online_trans: str = Field(..., description="""Khóa giao dịch thẻ Trực tuyến.
- ‘Y’ - Yes - Có

- ‘N’ - No - Không""",
                                         example="N")
    card_contact_less: str = Field(..., description="""Giao dịch không tiếp xúc
- ‘Y’ – Yes

- ‘N’ - No""",
                                   example="Y")
    card_relation_to_primany: str = Field(..., description="""Quan hệ với thẻ chính
- ‘H’ – Husband

- ‘W’ – Wife

- ‘F’ – Father

- ‘O’ – Others

- ‘M’ – Mother

- ‘N’ – Son

- ‘D’ – Daughter

- ‘S’ – Sister

- ‘B’ – Brother

- ‘R’ – Relative""",
                                          example="O")
    card_mother_name: str = Field(..., description="Tên mẹ của khách hàng",
                                  example="NGUYEN THI DIEU")
    card_secure_question: str = Field(..., description="Câu hỏi bí mật - Ngườ bạn thân nhất của bạn",
                                      example="THONG")
    card_bill_option: str = Field(..., description="""Nơi nhân hóa  đơn
- ‘H’ – Residence - Nơi cư trú

- ‘C’ – Mailing - Thư tín

- ‘O’ – Office - Văn phòng """,
                                  example="H")
    card_statement_delivery_option: str = Field(..., description="""Nơi nhân sao kê
- ‘M’ – Email

- ‘P’ – Post

- ‘B’ – Both""",
                                                example="B")


class OpenCardsIdInfoRequest(BaseSchema):
    id_name: str = Field(..., description="""Loại giấy tờ định danh:
- ‘F’ – Police

- ‘M’ – Military

- ‘N’ – New IC

- ‘O’ – Others

- ‘P’ – Passport""",
                         example="LY THANH QUAN")
    id_num: str = Field(..., description="Số giấy tờ định danh",
                        example="280855130")
    id_num_by_cif: str = Field(..., description="Mặc định rỗng",
                               example="")
    id_issued_location: str = Field(..., description="Nơi cấp giấy tờ định danh",
                                    example="BINH DUONG")
    id_issued_date: date = Field(..., description="Ngày cấp giấy tờ định danh. Định dạng: yyyy-MM-dd. VD: 2020-08-20",
                                 example="2014-08-06")


class OpenCardsCustomerInfoRequest(BaseSchema):
    birthday: date = Field(..., description="Ngày sinh. Định dạng yyyy-MM-dd",
                           example="1986-05-15")
    title: str = Field(..., description="Danh xưng (MR, MRS,v.v...)",
                       example="MR")
    full_name_vn: str = Field(..., description="Họ tên đầy đủ",
                              example="LY THANH QUAN")
    last_name: str = Field(..., description="Họ khách hàng dập trên thẻ",
                           example="LY")
    first_name: str = Field(..., description="Tên khách hàng dập trên thẻ",
                            example="QUAN")
    middle_name: str = Field(..., description="Tên lót khách hàng dập trên thẻ",
                             example="THANH")
    current_official: str = Field(..., description="Tên công ty dập trên thẻ. Mặc định """,
                                  example="SCB")
    embPhoto: str = Field(..., description="Hình để dập thẻ. Mặc định """,
                          example="")
    gender: str = Field(..., description="""Giới tính:
- ‘M’ – Male - Nam

- ‘F’ – Female - Nữ""",
                        example="M")
    nationality: str = Field(..., description="""Quốc tịch. Gồm 2 chữ số mã Quốc tịch. VD:
- 'VN' - VietNam

- ‘MY’ - Malaysia

- ‘TH’ -  Thailand """,
                             example="VN")
    martial_status: str = Field(..., description="""Trạng thái hôn nhân:
- ‘S’ – Single - Độc thân

- ‘M’ – Married - Đã kết hôn

- ‘D’ – Divorced - Đã ly dị

- ‘O’ – Others - Khác""",
                                example="M")
    resident_status: str = Field(..., description="""Hình thức cư trú
- ‘L’ – Local - Bản xứ

- 'F' - Foreigner - Người nước ngoài""",
                                 example="L")
    mthToStay: str = Field(..., description="Thời gian còn lại ở VN. Giá trị mặc định 0",
                           example="0")
    prStat: str = Field(..., description="""Đăng ký định cư hay chưa ?
- 'Y' - Yes

- 'N' - No""",
                        example="Y")
    vsExpDate: str = Field(..., description="Ngày hết hạn VISA. Default 000000",
                           example="000000")
    education: str = Field(..., description="""Trình độ học vấn
- 01 - PRIMARY SCHOOL

- 02 - SECONDARY SCHOOL

- 03 - HIGH SCHOOL

- 04 - COLLEGE - UNIVERSITY

- 05 - MASTER

- 06 - DOCTER

- 07 - OTHERS
""",
                           example="04")
    customer_type: str = Field(..., description=""" Nhóm KH
- 01        KHONG SU DUNG TU NGAY 01072019

- 02        CBNV SCB

- 03        KHCN VIP

- 04        KHCN QUAN HE TIEN GUI CO KY HAN

- 05        LANH DAO CAO CAP NHA NUOC

- 06        KH CBNV THUOC TCCL TAI SCB

- 07        KH CHUNG MINH THU NHAP (CBNV HANH CHINH SU NGHIEP, CHUNG MINH THU NHAP...)

- 08        KH KHAC (CO DONG, DVCNT...)

- 09        KH CO TSBD

- 10        CHU DN/ NGUOI DIEU HANH DN CO QUY MO LON TAI VN (NGUOI VN)

- 11        CHU DN/ NGUOI DIEU HANH DN CO QUY MO LON TAI VN (NGUOI NUOC NGOAI)

- 12        KHCN/HO KINH DOANH QUAN HE TIN DUNG TAI SCB

- 13        CONG TY THOI DAI

- 14        CONG TY SINH TAI

- 15        CONG TY BAO LONG

- 16        CONG TY TAN VIET

- 17        CONG TY LIEN KET KHAC

- 18        KHCN QUAN HE TIEN GUI CO KY HAN - PRE APPROVE

- 19        KHACH HANG TIEN VAY - PRE APPROVE

- 20        KHACH HANG GRAB

- 21        KHACH HANG VIP RUBY MIEN PHI PHAT HANH NHANH

- 22        KHACH HANG VIP DIAMOND MIEN PHI PHAT HANH NHANH

- 23        KHACH HANG DIAMOND PLUS MIEN PHI PHAT HANH NHANH

- 24        KH PHONG TOA SO TIET KIEM

- 25        KH DUOC LANH DAO GIOI THIEU

- 26        KH CO THE NH KHAC

- 27        KH BONG SEN VANG

- 28        KH DU LICH/CONG TAC NUOC NGOAI

- 29        KH BAO HIEM

- 30        KH VIP PREMIER

- 31        VAY NHANH UU DAI - VUNG CHAI TUONG LAI

- 32        KH TO CHUC

- 33        KH BAO HIEM - PRE APPROVE

- 34        KH CHUYEN TIEN THANH TOAN - PRE APPROVE

- 35        KH CO CON DU HOC-TRUONG CO HOC PHI CAO TAI VN

- 36        KHCN QUAN HE TIEN GUI THANH TOAN CASA

- 37        KHCN QUAN HE TIEN GUI THANH TOAN CASA - PRE APPROVE

- 38        DOI TAC LK NHOM 1

- 39        DOI TAC LK NHOM 2

- 40        PAYROLL-PLUS

- 41        THANH VIEN HOI DN TPHCM

- 99        KH VIP DUOC MIEN PHI THUONG NIEN
""",
                               example="03")


class OpenCardsBranchIssueRequest(BaseSchema):
    branhch_code: str = Field(..., description="Mã đơn vị mở thẻ",
                              example="001")


class OpenCardsDirectStaffRequest(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên giới thiệu trực tiếp",
                            example="15316")


class OpenCardsIndirectStaffRequest(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên giới thiệu gián tiếp",
                            example="12316")


class OpenCardsContractInfoRequest(BaseSchema):
    contract_name: str = Field(..., description="Số hợp đồng. Mặc định ",
                               example="")


class OpenCardsResidentAddressInfoRequest(BaseSchema):
    line: str = Field(..., description="Địa chỉ cư trú",
                      example="927 TRAN HUNG DAO")
    ward_name: str = Field(..., description="Địa chỉ cư trú",
                           example="PHUONG 1")
    contact_address_line: str = Field(..., description="Địa chỉ cư trú. Mặc định ",
                                      example="")
    city_code: str = Field(..., description="Mã bưu điện. VD: 70",
                           example="70")
    district_name: str = Field(..., description="Quận/ Huyện",
                               example="QUAN 5")
    city_name: str = Field(..., description="Tỉnh/Thành",
                           example="TP HCM")
    country_name: str = Field(..., description="""Quốc gia. Gồm 2 chữ số mã Quốc tịch. VD:
- 'VN' - VietNam

- ‘MY’ - Malaysia

- ‘TH’ -  Thailand """,
                              example="VN")
    telephone1: str = Field(..., description="Số điện thoại cố định",
                            example="0274333777")


class OpenCardsResidentCustomerInfoRequest(BaseSchema):
    resident_type: str = Field(..., description="""Loại hình cư trú:
- ‘L’– Living With Parents

- ‘O’ – Others

- ‘P’ – Own Property

- ‘R’ – Rented Property

- ‘V’ – Relatives Loại hình cư trú.
""",
                               example="P")
    resident_since: str = Field(..., description=" Thời gian bắt đầu cư trú. Mặc định 000000",
                                example="000000")


class OpenCardsResidentInfoRequest(BaseSchema):
    address_info: OpenCardsResidentAddressInfoRequest
    customer_info: OpenCardsResidentCustomerInfoRequest


class OpenCardsCorrespondenceAddressInfoRequest(BaseSchema):
    line: str = Field(..., description=" Địa chỉ liên hệ",
                      example="927 TRAN HUNG DAO")
    ward_name: str = Field(..., description="Địa chỉ liên hệ",
                           example="PHUONG 1")
    contact_address_line: str = Field(..., description=" Địa chỉ liên hệ. Mặc định """,
                                      example="")
    city_code: str = Field(..., description="Mã bưu điện. VD: 70",
                           example="70")
    district_name: str = Field(..., description="Quận/ Huyện",
                               example="QUAN 5")
    city_name: str = Field(..., description="Tỉnh/Thành",
                           example="TP HCM")
    country_name: str = Field(..., description="""Quốc gia. Gồm 2 chữ số mã Quốc tịch. VD:
- 'VN' - VietNam

- ‘MY’ - Malaysia

- ‘TH’ -  Thailand """,
                              example="VN")
    telephone1: str = Field(..., description="Số điện thoại cố định",
                            example="0274333777")
    mobile_phone: str = Field(..., description="Số điện thoại di động",
                              example="0909555888")


class OpenCardsCorrespondenceRequest(BaseSchema):
    address_info: OpenCardsCorrespondenceAddressInfoRequest
    smsInd: str = Field(..., description="""Sao kê gửi qua SMS.
- 'Y' - Yes

- 'N' - No""",
                        example="Y")
    email: str = Field(..., description="",
                       example="quanlt1@scb.com.vn")


class OpenCardsOfficeCustomerInfoRequest(BaseSchema):
    biz_line: str = Field(..., description=""" Loại hình kinh doanh
    "
- 8002	BAN HANG

- 8003	BAN HANG KY THUAT

- 8004	BAN LE/BAN SI

- 8005	BAO HIEM

- 8006	BAT DONG SAN

- 8010	BIEN PHIEN DICH

- 8012	CHUNG KHOAN

- 8021	CO KHI

- 8022	CONG NGHE CAO

- 8031	DAU KHI

- 8033	DET MAY/DA GIAY

- 8040	DICH VU KHACH HANG

- 8101	DIEN/DIEN TU

- 8102	DUOC PHAM/CONG NGHE SINH HOC

- 8103	GIAO DUC/DAO TAO

- 8111	HANG CAO CAP

- 8112	HANG GIA DUNG/CHAM SOC CA NHAN

- 8113	HANG KHONG/DU LICH/KHACH SAN

- 8121	HANH CHANH/THU KY

- 8122	HOA HOC/HOA SINH

- 8123	HOACH DINH/DU AN

- 8124	INTERNET/ONLINE MEDIA

- 8201	IT - PHAN MEM

- 8202	IT-PHAN CUNG/MANG

- 8203	KE TOAN/KIEM TOAN

- 8204	KE TOAN/TAI CHINH

- 8205	KHAC

- 8206	KHO VAN

- 8207	KIEN TRUC/THIET KE NOI THAT

- 8208	MARKETING

- 8209	MOI TRUONG/XU LY CHAT THAI

- 8210	MY THUAT/THIET KE

- 8211	NGAN HANG

- 8212	NHAN SU

- 8213	NONG NGHIEP/LAM NGHIEP

- 8214	O TO

- 8231	PHAP LY

- 8232	PHI CHINH PHU/PHI LOI NHUAN

- 8233	QA/QC

- 8234	QUANG CAO/KHUYEN MAI/DOI NGOAI

- 8240	SAN PHAM CONG NGHIEP

- 8251	SAN XUAT

- 8252	TAI CHINH/DAU TU

- 8253	THOI TRANG/LIFESTYLE

- 8254	THUC PHAM

- 8301	THUC PHAM/DO UONG

- 8302	TRUYEN HINH/TRUYEN THONG/BAO CHI

- 8303	TU VAN (61)

- 8304	VAN CHUYEN/GIAO NHAN

- 8305	VAT TU/CUNG VAN

- 8306	VIEN THONG

- 8307	XAY DUNG

- 8311	XUAT NHAP KHAU

- 8312	Y TE/CHAM SOC SUC KHOE

- 8853	FINANCIAL SERVICES
""",
                          example="")
    employee_nature: str = Field(..., description="Mặc định """,
                                 example="")
    cor_capital: str = Field(..., description="Qui mô công ty. Mặc định """,
                             example="")
    biz_position: str = Field(..., description="Chức vụ. Mặc định """,
                              example="")
    employee_since: str = Field(..., description="Thời gian bắt đầu công tác. Mặc định 000000",
                                example="000000")
    office_name: str = Field(..., description="Tên Công ty . Mặc định """,
                             example="")


class OpenCardsOfficeAddressInfoRequest(BaseSchema):
    line: str = Field(..., description=" Địa chỉ công ty . Mặc định """,
                      example="927 TRAN HUNG DAO")
    ward_name: str = Field(..., description=" Địa chỉ công ty . Mặc định """,
                           example="PHUONG 1")
    contact_address_line: str = Field(..., description=" Địa chỉ công ty . Mặc định """,
                                      example="")
    city_code: str = Field(..., description="Mã bưu điện. Mặc định """,
                           example="70")
    district_name: str = Field(..., description="Quận/ Huyện. Mặc định """,
                               example="QUAN 5")
    city_name: str = Field(..., description="Tỉnh/Thành . Mặc định """,
                           example="TP HCM")
    country_name: str = Field(..., description="""Quốc gia. Gồm 2 chữ số mã Quốc tịch. VD:
- 'VN' - VietNam

- ‘MY’ - Malaysia

- ‘TH’ -  Thailand
Mặc định "" """,
                              example="VN")
    telephone1: str = Field(..., description="Số điện thoại cố định. Mặc định """,
                            example="0274333777")
    phone_ext1: str = Field(..., description="Số nội bộ. Mặc định """,
                            example="805")
    telephone2: str = Field(..., description="Số điện thoại cố định. Mặc định """,
                            example="")
    phone_ext2: str = Field(..., description="Số nội bộ. Mặc định """,
                            example="")
    fax_no: str = Field(..., description="Fax",
                        example="")


class OpenCardsOfficeInfoRequest(BaseSchema):
    customer_info: OpenCardsOfficeCustomerInfoRequest
    address_info: OpenCardsOfficeAddressInfoRequest


class OpenCardsPreviousEmployerCustomerInfoRequest(BaseSchema):
    office_name: str = Field(..., description="Tên Công ty . Mặc định """,
                             example="")
    employee_since: str = Field(..., description="Thời gian bắt đầu công tác. Mặc định 000000",
                                example="000000")
    employee_duration: str = Field(..., description="Thời gian làm việc. Mặc định 0",
                                   example="0")


class OpenCardsPreviousEmployerAddressInfoRequest(BaseSchema):
    line: str = Field(..., description=" Địa chỉ công ty . Mặc định """,
                      example="927 TRAN HUNG DAO")
    ward_name: str = Field(..., description=" Địa chỉ công ty . Mặc định """,
                           example="PHUONG 1")
    contact_address_line: str = Field(..., description=" Địa chỉ công ty . Mặc định """,
                                      example="")
    city_code: str = Field(..., description="Mã bưu điện. Mặc định """,
                           example="70")
    district_name: str = Field(..., description="Quận/ Huyện. Mặc định """,
                               example="QUAN 5")
    city_name: str = Field(..., description="Tỉnh/Thành . Mặc định """,
                           example="TP HCM")
    country_name: str = Field(..., description="""Quốc gia. Gồm 2 chữ số mã Quốc tịch. VD:
- 'VN' - VietNam

- ‘MY’ - Malaysia

- ‘TH’ -  Thailand

- Mặc định "" """,
                              example="VN")
    telephone1: str = Field(..., description="Số điện thoại cố định. Mặc định """,
                            example="0274333777")
    phone_ext1: str = Field(..., description="Số nội bộ. Mặc định """,
                            example="805")


class OpenCardsPreviousEmployerInfoRequest(BaseSchema):
    customer_info: OpenCardsPreviousEmployerCustomerInfoRequest
    address_info: OpenCardsPreviousEmployerAddressInfoRequest


class OpenCardsPersonalDetailsRequest(BaseSchema):
    ownHouseLand: str = Field(..., description="""Có Nhà/ Đất.
- 'Y' - Yes

- 'N' - No""",
                              example="Y")
    ownCar: str = Field(..., description=""""Có xe Ô tô
- 'Y' - Yes

- 'N' - No""",
                        example="Y")
    noOfDepen: str = Field(..., description="""Số người phụ thuộc. Mặc định 0""",
                           example="0")
    avgSpendMth: str = Field(..., description="Chi tiêu trung bình hàng tháng. Mặc định 0",
                             example="0")
    bankPrd: str = Field(..., description="Mặc định """,
                         example="")
    bankOthrPrd: str = Field(..., description="Mặc định """,
                             example="")
    othrCCBankName: str = Field(..., description="Mặc định """,
                                example="")
    othrCCLimit: str = Field(..., description="Mặc định """,
                             example="")
    othrLoanBankName: str = Field(..., description="Mặc định """,
                                  example="")
    othrLoanInstallMth: str = Field(..., description="Mặc định """,
                                    example="")
    delivByBrchInd: str = Field(..., description="""Gửi theo Chi nhánh.
- 'Y' - Yes

- 'N' - No""",
                                example="Y")
    delivOpt: str = Field(..., description="""Nơi nhân hóa  đơn
- ‘H’ – Residence - Nơi cư trú

- ‘C’ – Mailing - Thư tín

- ‘O’ – Office - Văn phòng
""",
                          example="H")


class OpenCardsDeliveryAddressInfoRequest(BaseSchema):
    line: str = Field(..., description=" Địa chỉ ",
                      example="927 TRAN HUNG DAO")
    ward_name: str = Field(..., description=" Địa chỉ ",
                           example="PHUONG 1")
    contact_address_line: str = Field(..., description=" Địa chỉ",
                                      example="")
    city_code: str = Field(..., description="Mã bưu điện",
                           example="70")
    district_name: str = Field(..., description="Quận/ Huyện",
                               example="QUAN 5")
    city_name: str = Field(..., description="Tỉnh/Thành ",
                           example="TP HCM")
    country_name: str = Field(..., description="""Quốc gia. Gồm 2 chữ số mã Quốc tịch. VD:
- 'VN' - VietNam

- ‘MY’ - Malaysia

- ‘TH’ -  Thailand
""",
                              example="VN")


class OpenCardsDeliveryInfoRequest(BaseSchema):
    address_info: OpenCardsDeliveryAddressInfoRequest
    delivBrchId: str = Field(..., description="Mã chi nhánh gửi",
                             example="000")


class OpenCardsSpouseCompanyAddressInfoRequest(BaseSchema):
    line: str = Field(..., description="Mặc định """,
                      example="927 TRAN HUNG DAO")
    ward_name: str = Field(..., description="Mặc định """,
                           example="PHUONG 1")
    contact_address_line: str = Field(..., description="Mặc định """,
                                      example="")
    city_code: str = Field(..., description="Mặc định """,
                           example="70")
    district_name: str = Field(..., description="Mặc định """,
                               example="QUAN 5")
    city_name: str = Field(..., description="Mặc định """,
                           example="TP HCM")
    country_name: str = Field(..., description="Mặc định """,
                              example="VN")
    telephone1: str = Field(..., description="Mặc định """,
                            example="")
    phone_ext1: str = Field(..., description="Mặc định """,
                            example="")


class OpenCardsSpouseCompanyInfoRequest(BaseSchema):
    spcName: str = Field(..., description="Mặc định """,
                         example="")
    spcIdInd: str = Field(..., description="Mặc định """,
                          example="")
    spcNewId: str = Field(..., description="Mặc định """,
                          example="")
    spcEmpName: str = Field(..., description="Mặc định """,
                            example="")
    address_info: OpenCardsSpouseCompanyAddressInfoRequest
    spcEmpPosi: str = Field(..., description="Mặc định """,
                            example="")
    spcEmpSince: str = Field(..., description="Mặc định 000000",
                             example="000000")
    spcEmpWorkNat: str = Field(..., description="""Loại hình thu nhập:
- ‘E’ – Salaried

- ‘S’ – Self-Employed

- ‘U’ – Unemployed""",
                               example="S")


class OpenCardsEmergencyInfoRequest(BaseSchema):
    emerContcPrsn: str = Field(..., description="Tên người liên hệ khẩn cấp",
                               example="TRAN VAN DANG")
    emerGender: str = Field(..., description="""Giới tính người liên hệ khẩn cấp
- 'M' - Male

- 'F' - Female""",
                            example="M")
    emerPhoneNo: str = Field(..., description="Số điện thoại cố định người liên hệ khẩn cấp",
                             example="0908555999")
    emerMobileNo: str = Field(..., description="Số điện thoại di động người liên hệ khẩn cấp",
                              example="0909555866")
    emerRelt: str = Field(..., description="""Mối quan hệ với chủ Thẻ
- ‘H’ – Husband

- ‘W’ – Wife

- ‘F’ – Father

- ‘O’ – Others

- ‘M’ – Mother

- ‘N’ – Son

- ‘D’ – Daughter

- ‘S’ – Sister
- ‘B’ – Brother

- ‘R’ – Relative""",
                          example="B")


class OpenCardsCardAddonDataRequest(BaseSchema):
    payMeth: str = Field(..., description="Debit default = 0",
                         example="0")
    payCASA: str = Field(..., description="Debit default = 0",
                         example="0")
    payAmt: str = Field(..., description="Debit default = 0",
                        example="0")
    casaAcctNo: str = Field(..., description="Số tài khoản CASA",
                            example="1370106438990001")
    casaAcctTyp: str = Field(..., description="Loại tài khoản CASA. Mặc định 20",
                             example="20")
    casaCurCde: str = Field(..., description="Loại tiền tệ tài khoản CASA. VD: 704",
                            example="704")
    recomCrdNo: str = Field(..., description="Số thẻ người giới thiệu",
                            example="")
    recomName: str = Field(..., description="Tên người giới thiệu.",
                           example="")
    remark: str = Field(..., description="Ghi chú. Mặc định """,
                        example="")
    apprvDeviation: str = Field(..., description="giá trị NOTE",
                                example="NOTE")
    addData1: str = Field(..., description="Mặc định """,
                          example="")
    addData2: str = Field(..., description="Mặc định """,
                          example="")
    smsInfo: str = Field(..., description="Bắt buộc nhập khi tạo thẻ phụ. Mặc định 1",
                         example="0")
    narrative: str = Field(..., description="Diễn giải",
                           example="CRM WS")
    attachment: str = Field(..., description="Mặc định",
                            example="")
    decsnStat: str = Field(..., description="Trạng thái duyệt. Mặc định AM",
                           example="AM")


class OpenCardsCheckerInfoRequest(BaseSchema):
    staff_code: str = Field(..., description="User kiểm tra",
                            example="HANHDTD")


class OpenCardsApproverInfoRequest(BaseSchema):
    staff_code: str = Field(..., description="User phê duyệt",
                            example="HOANND2")


class OpenCardsRequest(BaseSchema):
    sequenceNo: str = Field(..., description="Số giao dịch, gồm 15 chữ số",
                            example="2022061315025580")
    fi: str = Field(..., description="Giá trị mặc định: 970429 (Gồm 6 chữ số)",
                    example="970429")
    srcSystm: str = Field(..., description="Tên chương trình gọi vào WS. VD: CRM",
                          example="CRM")
    cif_info: OpenCardsCifInfoRequest
    account_info: OpenCardsAccountInfoRequest
    card_info: OpenCardsCardInfoRequest
    prinCrdNo: str = Field(..., description="Thông tin thẻ chính. Nếu Card Index là thẻ phụ ('S' ) "
                                            "thì phải điền số thẻ chính (LOC + 4 last digits). Ngược lại bỏ qua",
                           example="")
    customer_info: OpenCardsCustomerInfoRequest
    id_info: OpenCardsIdInfoRequest
    srcCde: str = Field(..., description="Giá trị mặc định DM410",
                        example="DM410")
    branch_issued: OpenCardsBranchIssueRequest
    direct_staff: OpenCardsDirectStaffRequest
    promoCde: str = Field(..., description="Mã chương trình khuyến mãi. VD: PR97",
                          example="PR97")
    indirect_staff: OpenCardsIndirectStaffRequest
    imgId: str = Field(..., description="Mã hình ảnh. Mặc định """,
                       example="")
    contract_info: OpenCardsContractInfoRequest
    resident_info: OpenCardsResidentInfoRequest
    correspondence_info: OpenCardsCorrespondenceRequest
    office_info: OpenCardsOfficeInfoRequest
    previous_employer_info: OpenCardsPreviousEmployerInfoRequest
    personal_details: OpenCardsPersonalDetailsRequest
    delivery_info: OpenCardsDeliveryInfoRequest
    spouse_company_info: OpenCardsSpouseCompanyInfoRequest
    emergency_info: OpenCardsEmergencyInfoRequest
    card_addon_data: OpenCardsCardAddonDataRequest
    checker_info: OpenCardsCheckerInfoRequest
    approver_info: OpenCardsApproverInfoRequest


########################################################################################################################

# selectCardInfo


class SelectCardInfoRequest(BaseSchema):
    card_branched: str = Field(...,
                               description="""Thương hiệu Thẻ.
- Mặc định: Tất cả - `ALL`.
- Giá trị: `VS` - VISA, `MC` - MASTERCARD""",
                               example="VS")


class SelectCardInfoCardInfoItemResponse(BaseSchema):
    card_branched: str = Field(..., description="Thương hiệu Thẻ")
    card_group: str = Field(..., description="Nhóm Thẻ")
    card_description: str = Field(..., description="Mô tả thông tin Thẻ")
    card_src_code: str = Field(..., description="Source Code")
    card_pro_code: str = Field(..., description="Promote Code")
    card_fee_type: str = Field(..., description="Loại phí")
    card_fee_desc: str = Field(..., description="Mô tả phí")
    card_type: str = Field(..., description="""Loại thẻ:
- 'B' - Thẻ chính
- 'S' - Thẻ phụ
- '*' - Thẻ chính và thẻ phụ
    """)
    card_type_desc: str = Field(..., description="Mô tả loại Thẻ")
    card_fee_amount: str = Field(..., description="Số tiền phí")
    card_fee_amount_vat: str = Field(..., description="Thuế VAT trên số tiền phí")


class SelectCardInfoCardInfoListResponse(BaseSchema):
    card_info_item: SelectCardInfoCardInfoItemResponse


class SelectCardInfoResponse(BaseSchema):
    card_info_list: List[SelectCardInfoCardInfoListResponse]
