from typing import List, Optional

from loguru import logger
from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    generate_booking_code, get_optional_model_object_by_code_or_name,
    repos_get_model_object_by_id_or_code,
    write_transaction_log_and_update_booking
)
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.event import service_ekyc, service_file
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity,
    CustomerIdentityImage, CustomerIdentityImageTransaction
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, BookingCustomer, TransactionDaily,
    TransactionReceiver, TransactionSender
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, FingerType, HandSide, PassportCode, PassportType,
    PlaceOfIssue
)
from app.third_parties.oracle.models.master_data.others import (
    Nation, Religion, TransactionStage, TransactionStageStatus
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_ACTIVED, ADDRESS_COUNTRY_CODE_VN, BUSINESS_FORM_TTCN_GTDD_GTDD,
    BUSINESS_FORM_TTCN_GTDD_KM, BUSINESS_TYPE_INIT_CIF, CONTACT_ADDRESS_CODE,
    CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE, DROPDOWN_NONE_DICT,
    EKYC_DOCUMENT_TYPE, EKYC_GENDER_TYPE_FEMALE,
    EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, IMAGE_TYPE_CODE_FACE,
    IMAGE_TYPE_CODE_IDENTITY, IMAGE_TYPE_FACE, RESIDENT_ADDRESS_CODE
)
from app.utils.constant.ekyc import EKYC_DATE_FORMAT
from app.utils.error_messages import (
    ERROR_BOOKING_CODE_EXISTED, ERROR_CALL_SERVICE_EKYC,
    ERROR_CALL_SERVICE_FILE, ERROR_CIF_ID_NOT_EXIST,
    ERROR_COMPARE_IMAGE_IS_EXISTED, MESSAGE_STATUS
)
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown, generate_uuid, now,
    orjson_dumps
)
from app.utils.vietnamese_converter import convert_to_unsigned_vietnamese


########################################################################################################################
# Chi tiết A. Giấy tờ định danh
########################################################################################################################
async def repos_get_detail_identity(cif_id: str, session: Session) -> ReposReturn:
    place_of_birth = aliased(AddressProvince, name='PlaceOfBirth')

    identities = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress,
            CustomerIdentityImage,
            CustomerIdentityType,
            CustomerCompareImage,
            HandSide,
            FingerType,
            PlaceOfIssue,
            CustomerGender,
            AddressCountry,
            place_of_birth,
            AddressProvince,
            AddressDistrict,
            AddressWard,
            Nation,
            Religion,
            PassportType,
            PassportCode
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .outerjoin(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .outerjoin(CustomerIdentityImage, CustomerIdentity.id == CustomerIdentityImage.identity_id)
        .outerjoin(CustomerCompareImage, CustomerIdentityImage.id == CustomerCompareImage.identity_image_id)
        .outerjoin(CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id)

        .outerjoin(HandSide, CustomerIdentityImage.hand_side_id == HandSide.id)
        .outerjoin(FingerType, CustomerIdentityImage.finger_type_id == FingerType.id)
        .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .join(AddressCountry, CustomerIndividualInfo.country_of_birth_id == AddressCountry.id)
        .outerjoin(place_of_birth, CustomerIndividualInfo.place_of_birth_id == place_of_birth.id)
        .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .outerjoin(Nation, CustomerIndividualInfo.nation_id == Nation.id)
        .outerjoin(Religion, CustomerIndividualInfo.religion_id == Religion.id)
        .outerjoin(PassportType, CustomerIdentity.passport_type_id == PassportType.id)
        .outerjoin(PassportCode, CustomerIdentity.passport_code_id == PassportCode.id)
        .filter(
            Customer.id == cif_id
        )
        .order_by(desc(CustomerIdentityImage.updater_at))
    ).all()

    if not identities:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    first_row = identities[0]

    lasted_identity_id = first_row.CustomerIdentity.id  # customer identity id mới nhất
    identity_document_type_id = first_row.CustomerIdentityType.id  # Loại giấy tờ định danh mới nhất

    # vì join với address bị lặp dữ liệu nên cần lọc những fingerprint_ids
    fingerprint_ids = []
    fingerprints = []
    for row in identities:
        if row.CustomerIdentity.id == lasted_identity_id \
                and row.CustomerIdentityImage.hand_side_id \
                and row.CustomerIdentityImage.finger_type_id \
                and row.CustomerIdentityImage.id not in fingerprint_ids:
            fingerprint_ids.append(row.CustomerIdentityImage.id)
            fingerprints.append({
                "image_url": row.CustomerIdentityImage.image_url,
                "hand_side": dropdown(row.HandSide),
                "finger_type": dropdown(row.FingerType)
            })

    response_data = {
        "identity_document_type": dropdown(first_row.CustomerIdentityType),
        "ocr_result": {}
    }

    # CMND, CCCD
    if identity_document_type_id in [IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD, IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD]:
        # Mặt trước
        for row in identities:
            if row.CustomerIdentityImage.identity_image_front_flag == 1:
                response_data["front_side_information"] = {
                    "identity_image_url": row.CustomerIdentityImage.image_url,
                    "face_compare_image_url": row.CustomerCompareImage.compare_image_url,
                    "identity_avatar_image_uuid": row.CustomerIdentityImage.avatar_image_uuid,
                    "face_uuid_ekyc": row.CustomerCompareImage.id,
                    "similar_percent": row.CustomerCompareImage.similar_percent
                }
                break

        # Mặt sau
        for row in identities:
            if row.CustomerIdentityImage.identity_image_front_flag == 0 \
                    and row.CustomerIdentityImage.hand_side_id is None \
                    and row.CustomerIdentityImage.finger_type_id is None:
                response_data["back_side_information"] = {
                    "identity_image_url": row.CustomerIdentityImage.image_url,
                    "fingerprint": fingerprints,
                    "updated_at": row.CustomerIdentityImage.updater_at,
                    "updated_by": row.CustomerIdentityImage.updater_id
                }
                break

        resident_address = None  # noqa
        for row in identities:
            if row.CustomerIdentity.identity_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:

                if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                    resident_address = {
                        "province": dropdown(row.AddressProvince) if row.AddressProvince else DROPDOWN_NONE_DICT,
                        "district": dropdown(row.AddressDistrict)if row.AddressDistrict else DROPDOWN_NONE_DICT,
                        "ward": dropdown(row.AddressWard) if row.AddressWard else DROPDOWN_NONE_DICT,
                        "number_and_street": row.CustomerAddress.address
                    }
                    break

        contact_address = None  # noqa
        for row in identities:
            if row.CustomerIdentity.identity_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
                if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                    contact_address = {
                        "province": dropdown(row.AddressProvince) if row.AddressProvince else DROPDOWN_NONE_DICT,
                        "district": dropdown(row.AddressDistrict) if row.AddressDistrict else DROPDOWN_NONE_DICT,
                        "ward": dropdown(row.AddressWard) if row.AddressWard else DROPDOWN_NONE_DICT,
                        "number_and_street": row.CustomerAddress.address
                    }
                    break

        response_data['ocr_result'].update(**{
            'address_information': {
                'resident_address': resident_address,
                'contact_address': contact_address
            }
        })

        # CMND
        if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
            response_data['ocr_result'].update(**{
                'identity_document': {
                    "identity_number": first_row.CustomerIdentity.identity_num,
                    "issued_date": first_row.CustomerIdentity.issued_date,
                    "place_of_issue": dropdown(first_row.PlaceOfIssue) if first_row.PlaceOfIssue else DROPDOWN_NONE_DICT,
                    "expired_date": first_row.CustomerIdentity.expired_date
                },
                'basic_information': {
                    "full_name_vn": first_row.Customer.full_name_vn,
                    "gender": dropdown(first_row.CustomerGender) if first_row.CustomerGender else DROPDOWN_NONE_DICT,
                    "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
                    "nationality": dropdown(first_row.AddressCountry) if first_row.AddressCountry else DROPDOWN_NONE_DICT,
                    "province": dropdown(first_row.PlaceOfBirth) if first_row.PlaceOfBirth else DROPDOWN_NONE_DICT,
                    "ethnic": dropdown(first_row.Nation) if first_row.Nation else DROPDOWN_NONE_DICT,
                    "religion": dropdown(first_row.Religion) if first_row.Religion else DROPDOWN_NONE_DICT,
                    "identity_characteristic": first_row.CustomerIndividualInfo.identifying_characteristics,
                    "father_full_name_vn": first_row.CustomerIndividualInfo.father_full_name,
                    "mother_full_name_vn": first_row.CustomerIndividualInfo.mother_full_name
                }
            })

        # CCCD
        else:
            response_data['ocr_result'].update(**{
                'identity_document': {
                    "identity_number": first_row.CustomerIdentity.identity_num,
                    "issued_date": first_row.CustomerIdentity.issued_date,
                    "expired_date": first_row.CustomerIdentity.expired_date,
                    "place_of_issue": dropdown(first_row.PlaceOfIssue) if first_row.PlaceOfIssue else DROPDOWN_NONE_DICT,
                    "mrz_content": first_row.CustomerIdentity.mrz_content,
                    "qr_code_content": first_row.CustomerIdentity.qrcode_content,
                    "signer": first_row.CustomerIdentity.signer
                },
                'basic_information': {
                    "full_name_vn": first_row.Customer.full_name_vn,
                    "gender": dropdown(first_row.CustomerGender) if first_row.CustomerGender else DROPDOWN_NONE_DICT,
                    "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
                    "nationality": dropdown(first_row.AddressCountry) if first_row.AddressCountry else DROPDOWN_NONE_DICT,
                    "province": dropdown(first_row.PlaceOfBirth) if first_row.PlaceOfBirth else DROPDOWN_NONE_DICT,
                    "identity_characteristic": first_row.CustomerIndividualInfo.identifying_characteristics,
                }
            })

    # HO_CHIEU
    else:
        # Vì Compare Image không chỉ so sánh Mỗi khuôn mặt mà có cả vân tay, chữ ký
        # => tìm Compare Image so sánh khuôn mặt trong GTDD
        for row in identities:
            if row.CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_IDENTITY and \
                    row.CustomerIdentity.identity_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
                response_data['passport_information'] = {
                    "identity_image_url": row.CustomerIdentityImage.image_url,
                    "face_compare_image_url": row.CustomerCompareImage.compare_image_url,
                    "identity_avatar_image_uuid": row.CustomerIdentityImage.avatar_image_uuid,
                    "face_uuid_ekyc": row.CustomerCompareImage.id,
                    "similar_percent": row.CustomerCompareImage.similar_percent,
                    "fingerprint": fingerprints,
                }

                response_data['ocr_result'] = {
                    'identity_document': {
                        "identity_number": row.CustomerIdentity.identity_num,
                        "issued_date": row.CustomerIdentity.issued_date,
                        "place_of_issue": dropdown(row.PlaceOfIssue) if row.PlaceOfIssue else DROPDOWN_NONE_DICT,
                        "expired_date": row.CustomerIdentity.expired_date,
                        "passport_type": dropdown(row.PassportType) if row.PassportType else DROPDOWN_NONE_DICT,
                        "passport_code": dropdown(row.PassportCode) if row.PassportCode else DROPDOWN_NONE_DICT
                    },
                    'basic_information': {
                        "full_name_vn": row.Customer.full_name_vn,
                        "gender": dropdown(row.CustomerGender),
                        "date_of_birth": row.CustomerIndividualInfo.date_of_birth,
                        "nationality": dropdown(row.AddressCountry) if row.AddressCountry else DROPDOWN_NONE_DICT,
                        "place_of_birth": dropdown(row.PlaceOfBirth) if row.PlaceOfBirth else DROPDOWN_NONE_DICT,
                        "identity_card_number": row.CustomerIdentity.identity_number_in_passport,
                        "mrz_content": row.CustomerIdentity.mrz_content
                    }
                }

    return ReposReturn(data=response_data)


########################################################################################################################

########################################################################################################################
# Lịch sử thay đổi giấy tờ định danh
########################################################################################################################
async def repos_get_identity_image_transactions(
        cif_id: str,
        session: Session
):
    identity_image_transactions = session.execute(
        select(
            CustomerIdentityImageTransaction,
        )
        .join(CustomerIdentityImage, CustomerIdentityImageTransaction.identity_image_id == CustomerIdentityImage.id)
        .join(CustomerIdentity, and_(
            CustomerIdentityImage.identity_id == CustomerIdentity.id,
            CustomerIdentity.customer_id == cif_id,
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_IDENTITY
        ))
        .order_by(desc(CustomerIdentityImageTransaction.maker_at))
    ).scalars().all()

    return ReposReturn(data=identity_image_transactions)


########################################################################################################################
# Lưu lại A. Giấy tờ định danh
########################################################################################################################
@auto_commit
async def repos_save_identity(
        identity_document_type_id: str,
        customer_id: Optional[str],
        identity_id: Optional[str],
        saving_customer: dict,
        saving_customer_identity: dict,
        saving_customer_individual_info: dict,
        saving_customer_resident_address: Optional[dict],  # CMND, CCCD mới có
        saving_customer_contact_address: Optional[dict],  # CMND, CCCD mới có
        saving_customer_compare_image: dict,
        saving_customer_identity_images: List[dict],
        saving_transaction_stage_status: dict,
        saving_transaction_stage: dict,
        saving_transaction_daily: dict,
        saving_transaction_sender: dict,
        saving_transaction_receiver: dict,
        avatar_image_uuid_service,
        identity_avatar_image_uuid_ekyc: str,
        request_data: dict,
        history_datas: List,
        current_user: UserInfoResponse,
        session: Session
) -> ReposReturn:
    current_user_code = current_user.code
    current_user_branch_id = current_user.hrm_branch_id
    new_first_identity_image_id = generate_uuid()  # ID ảnh mặt trước hoặc ảnh hộ chiếu
    new_second_identity_image_id = generate_uuid()  # ID ảnh mặt sau

    # Kiểm tra uuid khuôn mặt đã tồn tại trong DB chưa
    customer_compare_image = session.execute(
        select(
            CustomerCompareImage
        )
        .filter(CustomerCompareImage.id == saving_customer_compare_image['id'])
    ).scalar()
    if customer_compare_image:
        return ReposReturn(
            is_error=True,
            msg=ERROR_COMPARE_IMAGE_IS_EXISTED
        )
    # Tạo mới
    if not customer_id:
        new_customer_id = generate_uuid()
        new_identity_id = generate_uuid()

        customer_id = new_customer_id  # Lấy id sau khi create thành công
        # create new Customer
        saving_customer['id'] = new_customer_id
        session.add(
            Customer(**saving_customer)
        )

        # create new CustomerIndividualInfo
        saving_customer_individual_info['customer_id'] = new_customer_id
        session.add(
            CustomerIndividualInfo(**saving_customer_individual_info)
        )

        # create new CustomerIdentity
        saving_customer_identity['id'] = new_identity_id
        saving_customer_identity['customer_id'] = new_customer_id
        session.add(
            CustomerIdentity(**saving_customer_identity)
        )
        is_error, create_response = await create_customer_identity_image_and_customer_compare_image(
            identity_id=new_identity_id,
            new_first_identity_image_id=new_first_identity_image_id,
            new_second_identity_image_id=new_second_identity_image_id,
            saving_customer_identity_images=saving_customer_identity_images,
            saving_customer_compare_image=saving_customer_compare_image,
            is_create=True,
            session=session
        )
        if is_error:
            return ReposReturn(is_error=True, msg=create_response['message'])

        compare_transaction_parent_id = create_response['compare_transaction_parent_id']

        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            # create new CustomerAddress for resident address
            saving_customer_resident_address['customer_id'] = new_customer_id
            session.add(
                CustomerAddress(**saving_customer_resident_address)
            )

            # create new CustomerAddress for contact address
            saving_customer_contact_address['customer_id'] = new_customer_id
            session.add(
                CustomerAddress(**saving_customer_contact_address)
            )

        new_booking_id = generate_uuid()
        is_existed, booking_code = await generate_booking_code(
            branch_code=current_user_branch_id,
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            session=session
        )

        if is_existed:
            return ReposReturn(
                is_error=True,
                msg=ERROR_BOOKING_CODE_EXISTED,
                detail=MESSAGE_STATUS[ERROR_BOOKING_CODE_EXISTED]
            )

        # create booking & log
        session.add_all([
            # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSSINESS_FORM
            TransactionStageStatus(**saving_transaction_stage_status),
            TransactionStage(**saving_transaction_stage),
            TransactionDaily(**saving_transaction_daily),
            TransactionSender(**saving_transaction_sender),
            TransactionReceiver(**saving_transaction_receiver),
            Booking(
                id=new_booking_id,
                code=booking_code,
                transaction_id=saving_transaction_daily['transaction_id'],
                business_type_id=BUSINESS_TYPE_INIT_CIF,
                branch_id=current_user_branch_id,
                created_at=now(),
                updated_at=now()
            ),
            BookingCustomer(
                booking_id=new_booking_id,
                customer_id=new_customer_id
            ),
            BookingBusinessForm(
                booking_id=new_booking_id,
                business_form_id=BUSINESS_FORM_TTCN_GTDD_GTDD,
                save_flag=True,  # Save_flag đổi lại thành True do Business Form giờ là những Tab nhỏ nhiều cấp
                form_data=orjson_dumps(request_data),
                log_data=orjson_dumps(history_datas),
                created_at=now(),
                updated_at=now()
            ),
            # Hiện tại Tab khuôn mặt không có chức năng lưu
            # vì api GTDD đã upload khuôn mặt nên Tab này coi như hoàn thành
            BookingBusinessForm(
                booking_id=new_booking_id,
                business_form_id=BUSINESS_FORM_TTCN_GTDD_KM,
                save_flag=True,
                form_data=orjson_dumps(request_data),
                created_at=now(),
                updated_at=now()
            )
        ])

    # Update
    else:
        # Cập nhật 1 cif_number đã tồn tại
        saving_customer_identity.update({
            "id": identity_id,
            "customer_id": customer_id
        })
        saving_customer_individual_info.update({"customer_id": customer_id})

        session.execute(update(Customer).filter(
            Customer.id == customer_id
        ).values(**saving_customer))

        session.execute(update(CustomerIdentity).filter(
            CustomerIdentity.customer_id == customer_id
        ).values(saving_customer_identity))

        session.execute(update(CustomerIndividualInfo).filter(
            CustomerIndividualInfo.customer_id == customer_id
        ).values(saving_customer_individual_info))

        # Passport thì không có địa chỉ
        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            saving_customer_resident_address.update({"customer_id": customer_id})
            saving_customer_contact_address.update({"customer_id": customer_id})

            session.execute(update(CustomerAddress).filter(and_(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE,
            )).values(saving_customer_resident_address))
            session.execute(update(CustomerAddress).filter(and_(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE,
            )).values(saving_customer_contact_address))

        # ảnh chụp giấy tờ
        saving_customer_compare_image['identity_id'] = identity_id

        for saving_customer_identity_image in saving_customer_identity_images:
            saving_customer_identity_image['identity_id'] = identity_id

        is_error, message = await create_customer_identity_image_and_customer_compare_image(
            identity_id=identity_id,
            new_first_identity_image_id=new_first_identity_image_id,
            new_second_identity_image_id=new_second_identity_image_id,
            saving_customer_identity_images=saving_customer_identity_images,
            saving_customer_compare_image=saving_customer_compare_image,
            is_create=False,
            session=session
        )
        if is_error:
            return ReposReturn(is_error=True, msg=message)

        is_success, booking_response = await write_transaction_log_and_update_booking(
            log_data=request_data,
            session=session,
            customer_id=customer_id,
            business_form_id=BUSINESS_FORM_TTCN_GTDD_GTDD
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=booking_response['msg'])

        booking_code = booking_response['booking_code']

        # Tìm CustomerCompareImageTransaction trước đó
        previous_compare_image_transaction = session.execute(
            select(
                CustomerIdentity,
                CustomerCompareImage,
                CustomerCompareImageTransaction
            )
            .join(CustomerCompareImage, CustomerIdentity.id == CustomerCompareImage.identity_id)
            .join(CustomerCompareImageTransaction, CustomerCompareImage.id == CustomerCompareImageTransaction.compare_image_id)
            .filter(CustomerIdentity.customer_id == customer_id)
            .order_by(desc(CustomerCompareImageTransaction.maker_at))
        ).first()
        if not previous_compare_image_transaction:
            return ReposReturn(is_error=True, detail="Previous Compare Image Transaction is not existed")
        _, _, compare_image_transaction = previous_compare_image_transaction
        compare_transaction_parent_id = compare_image_transaction.id

    identity_image_uuid = generate_uuid()
    identity_avatar_image_uuid = generate_uuid()
    identity_id = saving_customer_identity['id']
    session.add_all([
        CustomerCompareImage(**saving_customer_compare_image),
        CustomerCompareImageTransaction(**{
            "compare_transaction_parent_id": compare_transaction_parent_id,
            "compare_image_id": saving_customer_compare_image['id'],
            "identity_image_id": saving_customer_compare_image['identity_image_id'],
            "is_identity_compare": ACTIVE_FLAG_ACTIVED,
            "compare_image_url": saving_customer_compare_image['compare_image_url'],
            "similar_percent": saving_customer_compare_image['similar_percent'],
            "maker_id": saving_customer_compare_image['maker_id'],
            "maker_at": saving_customer_compare_image['maker_at']
        }),
        # Tạo Khuôn mặt từ CompareImage, khuôn mặt này sẽ sử dụng để so sánh phê duyệt
        CustomerIdentityImage(**dict(
            id=identity_image_uuid,
            identity_id=identity_id,
            image_type_id=IMAGE_TYPE_FACE,
            image_url=saving_customer_compare_image['compare_image_url'],
            active_flag=True,
            maker_id=current_user_code,
            maker_at=now(),
            ekyc_uuid=saving_customer_compare_image['id']
        )),
        CustomerIdentityImageTransaction(**dict(
            identity_image_id=identity_image_uuid,
            image_url=saving_customer_compare_image['compare_image_url'],
            active_flag=True,
            maker_id=current_user_code,
            maker_at=now()
        )),
        # Tạo avatar
        CustomerIdentityImage(**dict(
            id=identity_avatar_image_uuid,
            identity_id=identity_id,
            image_type_id=IMAGE_TYPE_CODE_FACE,
            image_url=avatar_image_uuid_service['data']['uuid'],
            avatar_image_uuid=None,
            hand_side_id=None,
            finger_type_id=None,
            vector_data=None,
            active_flag=True,
            maker_id=current_user_code,
            maker_at=now(),
            identity_image_front_flag=None,
            ekyc_uuid=identity_avatar_image_uuid_ekyc
        )),
        CustomerIdentityImageTransaction(**dict(
            identity_image_id=identity_avatar_image_uuid,
            image_url=avatar_image_uuid_service['data']['uuid'],
            active_flag=True,
            maker_id=current_user.code,
            maker_at=now()
        ))
    ])

    return ReposReturn(data=dict(
        cif_id=customer_id,
        booking_code=booking_code
    ))


########################################################################################################################


########################################################################################################################
# Repo khác
########################################################################################################################
async def repos_get_identity_information(customer_id: str, session: Session):
    identities = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .filter(Customer.id == customer_id)
    ).all()

    if not identities:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    customer, customer_identity, customer_individual_info, _ = identities[0]
    customer_resident_address: Optional[CustomerAddress] = None
    customer_contact_address: Optional[CustomerAddress] = None
    for _, _, _, customer_address in identities:
        if customer_address.address_type_id == RESIDENT_ADDRESS_CODE:
            customer_resident_address = customer_address
        if customer_address.address_type_id == CONTACT_ADDRESS_CODE:
            customer_contact_address = customer_address

    return ReposReturn(data=(
        customer, customer_identity, customer_individual_info, customer_resident_address, customer_contact_address
    ))


async def create_customer_identity_image_and_customer_compare_image(
        identity_id,
        new_first_identity_image_id,
        new_second_identity_image_id,
        saving_customer_identity_images,
        saving_customer_compare_image,
        is_create: bool,
        session: Session
):
    """
        Tạo giấy tờ định danh và lưu log
    """
    # create new CustomerIdentityImage ảnh mặt trước hoặc hộ chiếu
    new_first_identity_image = saving_customer_identity_images[0]
    new_first_identity_image['id'] = new_first_identity_image_id
    new_first_identity_image['identity_id'] = identity_id

    session.add_all([
        CustomerIdentityImage(**new_first_identity_image),
        CustomerIdentityImageTransaction(**{
            "identity_image_id": new_first_identity_image['id'],
            "image_url": new_first_identity_image['image_url'],
            "active_flag": True,
            "maker_id": new_first_identity_image['maker_id'],
            "maker_at": new_first_identity_image['maker_at']
        })
    ])
    # create new CustomerIdentityImage ảnh mặt sau
    if len(saving_customer_identity_images) > 1:
        new_second_identity_image = saving_customer_identity_images[1]
        new_second_identity_image['id'] = new_second_identity_image_id
        new_second_identity_image['identity_id'] = identity_id
        session.add_all([
            CustomerIdentityImage(**new_second_identity_image),
            CustomerIdentityImageTransaction(**{
                "identity_image_id": new_second_identity_image['id'],
                "image_url": new_second_identity_image['image_url'],
                "active_flag": True,
                "maker_id": new_second_identity_image['maker_id'],
                "maker_at": new_second_identity_image['maker_at']
            })
        ])
    # create new CustomerCompareImage
    compare_transaction_parent_id = None
    saving_customer_compare_image['identity_id'] = identity_id
    saving_customer_compare_image['identity_image_id'] = new_first_identity_image_id
    # Nếu cập nhật giấy tờ định danh, hình ảnh đối chiếu cập nhật lại
    if not is_create:
        try:
            compare_transaction_parent_id = session.execute(
                select(
                    CustomerCompareImageTransaction.id
                )
                .join(CustomerIdentityImage,
                      CustomerCompareImageTransaction.identity_image_id == CustomerIdentityImage.id)
                .join(CustomerCompareImage,
                      CustomerCompareImageTransaction.compare_image_id == CustomerCompareImage.id)
                .order_by(desc(CustomerCompareImageTransaction.maker_at))
            ).scalars().first()
        except Exception as ex:
            logger.error(str(ex))
            return True, dict(mesage="Write Transaction Error")

    return False, dict(compare_transaction_parent_id=compare_transaction_parent_id)


########################################################################################################################
# Gọi qua eKYC để OCR giấy tờ định danh
########################################################################################################################
async def repos_upload_identity_document_and_ocr(
        identity_type: int,
        image_file: bytes,
        image_file_name: str,
        session: Session
):
    is_success, ocr_response = await service_ekyc.ocr_identity_document(
        file=image_file,
        filename=image_file_name,
        identity_type=identity_type
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_EKYC, detail=ocr_response.get('message', ''))

    file_response = await service_file.upload_file(file=image_file, name=image_file_name)

    if not file_response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

    ocr_response_data = dict(
        identity_document_type=dict(
            id=ocr_response.get('document_type'),
            code=ocr_response.get('document_type'),
            name=EKYC_DOCUMENT_TYPE[ocr_response.get('document_type')]
        )
    )

    if identity_type == EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD:
        response_data = await mapping_ekyc_front_side_identity_card_ocr_data(
            image_url=file_response['file_url'],
            ocr_data=ocr_response.get('data', {}),
            session=session
        )
    elif identity_type == EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD:
        response_data = await mapping_ekyc_back_side_identity_card_ocr_data(
            image_url=file_response['file_url'],
            ocr_data=ocr_response.get('data', {}),
            session=session
        )
    elif identity_type == EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD:
        response_data = await mapping_ekyc_front_side_citizen_card_ocr_data(
            image_url=file_response['file_url'],
            ocr_data=ocr_response.get('data', {}),
            session=session
        )
    elif identity_type == EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD:
        response_data = await mapping_ekyc_back_side_citizen_card_ocr_data(
            image_url=file_response['file_url'],
            ocr_data=ocr_response.get('data', {}),
            session=session
        )
    else:
        response_data = await mapping_ekyc_passport_ocr_data(
            image_url=file_response['file_url'],
            ocr_data=ocr_response.get('data', {}),
            session=session
        )

    ocr_response_data.update(response_data)

    return ReposReturn(data=ocr_response_data)


async def mapping_ekyc_front_side_identity_card_ocr_data(image_url: str, ocr_data: dict, session: Session):
    repos_return_vietnamese_nationality = await repos_get_model_object_by_id_or_code(
        model_id=None,
        model_code=ADDRESS_COUNTRY_CODE_VN,
        model=AddressCountry,
        loc='nationality:VN',
        session=session
    )

    try:
        place_of_origin = ocr_data.get('place_of_origin', ', ').split(', ')[-1]
    except ValueError:
        place_of_origin = None

    optional_place_of_origin = await get_optional_model_object_by_code_or_name(
        model_name=place_of_origin,
        model=AddressProvince,
        session=session
    )

    province_code = ocr_data.get('address_info').get('province_code')
    province_name = ocr_data.get('address_info').get('province_name')

    district_code = ocr_data.get('address_info').get('district_code')
    district_name = ocr_data.get('address_info').get('district_name')

    ward_code = ocr_data.get('address_info').get('ward_code')
    ward_name = ocr_data.get('address_info').get('ward_name')

    number_and_street = ocr_data.get('address_info').get('street_name')

    optional_province = await get_optional_model_object_by_code_or_name(
        model_name=province_name,
        model_code=province_code,
        model=AddressProvince,
        session=session
    )
    optional_district = await get_optional_model_object_by_code_or_name(
        model_name=district_name,
        model_code=district_code,
        model=AddressDistrict,
        session=session
    )
    optional_ward = await get_optional_model_object_by_code_or_name(
        model_name=ward_name,
        model_code=ward_code,
        model=AddressWard,
        session=session
    )

    resident_address = {
        "province": dropdown(optional_province) if optional_province else DROPDOWN_NONE_DICT,
        "district": dropdown(optional_district) if optional_district else DROPDOWN_NONE_DICT,
        "ward": dropdown(optional_ward) if optional_ward else DROPDOWN_NONE_DICT,
        "number_and_street": number_and_street if number_and_street else None
    }

    optional_identity_number = ocr_data.get('document_id')
    optional_expired_date = ocr_data.get('date_of_expiry')
    optional_date_of_birth = ocr_data.get('date_of_birth')

    front_side_identity_card_info = {
        "front_side_information": {
            "identity_image_url": image_url,
            "identity_avatar_image_uuid": ocr_data.get('avatar_image') if ocr_data.get('avatar_image') else None
        },
        "ocr_result": {
            "identity_document": {
                "identity_number": optional_identity_number if optional_identity_number else None,
                "expired_date": date_string_to_other_date_string_format(
                    optional_expired_date,
                    from_format=EKYC_DATE_FORMAT
                ) if optional_expired_date else None
            },
            "basic_information": {
                "full_name_vn": ocr_data.get('full_name'),
                "date_of_birth": date_string_to_other_date_string_format(
                    ocr_data.get('date_of_birth'),
                    from_format=EKYC_DATE_FORMAT
                ) if optional_date_of_birth else None,
                "nationality": dropdown(repos_return_vietnamese_nationality.data)
                if not repos_return_vietnamese_nationality.is_error else DROPDOWN_NONE_DICT,
                "province": dropdown(optional_place_of_origin) if optional_place_of_origin else DROPDOWN_NONE_DICT,
            },
            "address_information": {
                "resident_address": resident_address,
                "contact_address": resident_address
            }
        }
    }

    return front_side_identity_card_info


async def mapping_ekyc_passport_ocr_data(image_url: str, ocr_data: dict, session: Session):
    optional_place_of_issue = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('place_of_issue'),
        model=PlaceOfIssue,
        session=session
    )

    optional_passport_code = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('passport_code'),
        model=PassportCode,
        session=session
    )

    optional_gender = await get_optional_model_object_by_code_or_name(
        model_code=CRM_GENDER_TYPE_FEMALE if ocr_data.get('gender') == EKYC_GENDER_TYPE_FEMALE else CRM_GENDER_TYPE_MALE,
        model=CustomerGender,
        session=session
    )

    optional_nationality = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('nationality', '/').split('/')[0],  # Việt Nam/Vietnamese
        model=AddressCountry,
        session=session
    )

    optional_place_of_birth = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('place_of_origin'),  # Việt Nam/Vietnamese
        model=AddressProvince,
        session=session
    )
    # ocr trả date_of_birth là 00/00/00
    if ocr_data.get('date_of_birth') and ocr_data.get('date_of_birth') != '00/00/00':
        optional_date_of_birth = date_string_to_other_date_string_format(ocr_data.get('date_of_birth'), from_format=EKYC_DATE_FORMAT)
    else:
        optional_date_of_birth = None

    optional_identity_number = ocr_data.get('document_id')
    optional_issued_date = ocr_data.get('date_of_issue')
    optional_expired_date = ocr_data.get('date_of_expiry')
    optional_identity_card_number = ocr_data.get('id_card_number')

    passport_info = {
        "passport_information": {
            "identity_image_url": image_url,
            "identity_avatar_image_uuid": ocr_data.get('avatar_image') if ocr_data.get('avatar_image') else None
        },
        "ocr_result": {
            "identity_document":
                {
                    "identity_number": optional_identity_number if optional_identity_number else None,
                    "issued_date": date_string_to_other_date_string_format(
                        optional_issued_date,
                        from_format=EKYC_DATE_FORMAT
                    ) if optional_issued_date else None,
                    "place_of_issue": dropdown(optional_place_of_issue) if optional_place_of_issue else DROPDOWN_NONE_DICT,
                    "expired_date": date_string_to_other_date_string_format(
                        optional_expired_date,
                        from_format=EKYC_DATE_FORMAT
                    ) if optional_expired_date else None,
                    "passport_type": {  # TODO: chỗ này bên Ekyc chưa thấy trả vể
                        "id": "string",
                        "code": "string",
                        "name": "string"
                    },
                    "passport_code": dropdown(optional_passport_code) if optional_passport_code else DROPDOWN_NONE_DICT,
                },
            "basic_information":
                {
                    "full_name_vn": ocr_data.get('full_name'),
                    "gender": dropdown(optional_gender) if optional_gender else DROPDOWN_NONE_DICT,
                    "date_of_birth": optional_date_of_birth,
                    "nationality": dropdown(optional_nationality) if optional_nationality else DROPDOWN_NONE_DICT,
                    "place_of_birth": dropdown(optional_place_of_birth) if optional_place_of_birth else DROPDOWN_NONE_DICT,
                    "identity_card_number": optional_identity_card_number if optional_identity_card_number else None,
                    "mrz_content": f"{ocr_data.get('mrz_1', '')}{ocr_data.get('mrz_2', '')}"
                }
        }
    }

    return passport_info


async def mapping_ekyc_back_side_identity_card_ocr_data(image_url: str, ocr_data: dict, session: Session):
    optional_ethnic = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('ethnicity'),
        model=Nation,
        session=session
    )

    optional_place_of_issue = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('place_of_issue'),
        model=PlaceOfIssue,
        session=session
    )

    optional_religion = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('religion'),
        model=Religion,
        session=session
    )

    optional_date_of_issue = ocr_data.get('date_of_issue')

    back_side_identity_card_info = {
        "back_side_information": {
            "identity_image_url": image_url,
        },
        "ocr_result": {
            "identity_document": {
                "issued_date": date_string_to_other_date_string_format(
                    optional_date_of_issue,
                    from_format=EKYC_DATE_FORMAT
                ) if optional_date_of_issue else None,
                "place_of_issue": dropdown(optional_place_of_issue) if optional_place_of_issue else DROPDOWN_NONE_DICT,
            },
            "basic_information": {
                "ethnic": dropdown(optional_ethnic) if optional_ethnic else DROPDOWN_NONE_DICT,
                "religion": dropdown(optional_religion) if optional_ethnic else DROPDOWN_NONE_DICT,
                "identity_characteristic": ocr_data.get('personal_identification'),
            }
        }
    }

    return back_side_identity_card_info


async def mapping_ekyc_front_side_citizen_card_ocr_data(image_url: str, ocr_data: dict, session: Session):
    optional_gender = await get_optional_model_object_by_code_or_name(
        model_code=CRM_GENDER_TYPE_FEMALE if ocr_data.get(
            'gender') == EKYC_GENDER_TYPE_FEMALE else CRM_GENDER_TYPE_MALE,
        model=CustomerGender,
        session=session
    )

    optional_nationality = await get_optional_model_object_by_code_or_name(
        model_name=convert_to_unsigned_vietnamese(ocr_data.get('nationality', '/').split('/')[0]),
        # Việt Nam/Vietnamese
        model=AddressCountry,
        session=session
    )

    try:
        # TODO: tách tỉnh ra query. Hỏi thăm bên eKYC xem có case đặc biệt không
        place_of_origin = ocr_data.get('place_of_origin', ', ').split(', ')[-1]
    except ValueError:
        place_of_origin = None

    optional_place_of_origin = await get_optional_model_object_by_code_or_name(
        model_name=place_of_origin,
        model=AddressProvince,
        session=session
    )

    optional_province = await get_optional_model_object_by_code_or_name(
        model_code=ocr_data.get('address_info', {}).get('province_code'),
        model=AddressProvince,
        session=session
    )
    optional_district = await get_optional_model_object_by_code_or_name(
        model_code=ocr_data.get('address_info', {}).get('district_code'),
        model=AddressDistrict,
        session=session
    )
    optional_ward = await get_optional_model_object_by_code_or_name(
        model_code=ocr_data.get('address_info', {}).get('ward_code'),
        model=AddressWard,
        session=session
    )
    optional_number_and_street = ocr_data.get('address_info', {}).get('street_name')

    resident_address = {
        "province": dropdown(optional_province) if optional_province else DROPDOWN_NONE_DICT,
        "district": dropdown(optional_district) if optional_district else DROPDOWN_NONE_DICT,
        "ward": dropdown(optional_ward) if optional_ward else DROPDOWN_NONE_DICT,
        "number_and_street": optional_number_and_street if optional_number_and_street else None
    }

    optional_identity_avatar_image_uuid = ocr_data.get('avatar_image')
    optional_identity_number = ocr_data.get('document_id')
    optional_issued_date = ocr_data.get('date_of_issue')
    optional_expired_date = ocr_data.get('date_of_expiry')
    optional_full_name_vn = ocr_data.get('full_name')
    optional_date_of_birth = ocr_data.get('date_of_birth')

    front_side_citizen_card_info = {
        "front_side_information": {
            "identity_image_url": image_url,
            "identity_avatar_image_uuid": optional_identity_avatar_image_uuid if optional_identity_avatar_image_uuid else None
        },
        "ocr_result": {
            "identity_document": {
                "identity_number": optional_identity_number if optional_identity_number else None,
                "issued_date": date_string_to_other_date_string_format(
                    optional_issued_date,
                    from_format=EKYC_DATE_FORMAT
                ) if optional_issued_date else None,
                "expired_date": date_string_to_other_date_string_format(
                    optional_expired_date,
                    from_format=EKYC_DATE_FORMAT
                ) if optional_expired_date else None
            },
            "basic_information": {
                "full_name_vn": optional_full_name_vn if optional_full_name_vn else None,
                "gender": dropdown(optional_gender) if optional_gender else DROPDOWN_NONE_DICT,
                "date_of_birth": date_string_to_other_date_string_format(
                    optional_date_of_birth,
                    from_format=EKYC_DATE_FORMAT
                ) if optional_date_of_birth else None,
                "nationality": dropdown(optional_nationality) if optional_nationality else DROPDOWN_NONE_DICT,
                "province": dropdown(optional_place_of_origin) if optional_place_of_origin else DROPDOWN_NONE_DICT,
            },
            "address_information": {
                "resident_address": resident_address,
                "contact_address": resident_address
            }
        }
    }

    return front_side_citizen_card_info


async def mapping_ekyc_back_side_citizen_card_ocr_data(image_url: str, ocr_data: dict, session: Session):
    mrz_content1 = ocr_data.get('mrz_1') if ocr_data.get('mrz_1') else ''
    mrz_content2 = ocr_data.get('mrz_2') if ocr_data.get('mrz_2') else ''
    mrz_content3 = ocr_data.get('mrz_3') if ocr_data.get('mrz_3') else ''
    signer = ocr_data.get("signer") if ocr_data.get('signer') else ''
    optional_mrz_content = mrz_content1 + mrz_content2 + mrz_content3

    optional_place_of_issue = await get_optional_model_object_by_code_or_name(
        model_name=ocr_data.get('place_of_issue'),
        model=PlaceOfIssue,
        session=session
    )

    optional_issued_date = ocr_data.get('date_of_issue')
    optional_identity_characteristic = ocr_data.get('personal_identification')

    back_side_identity_card_info = {
        "back_side_information": {
            "identity_image_url": image_url,
        },
        "ocr_result": {
            "identity_document": {
                "issued_date": date_string_to_other_date_string_format(
                    optional_issued_date,
                    from_format=EKYC_DATE_FORMAT
                ) if optional_issued_date else None,
                "place_of_issue": dropdown(optional_place_of_issue) if optional_place_of_issue else DROPDOWN_NONE_DICT,
                "mrz_content": optional_mrz_content if optional_mrz_content else None,
                "signer": signer
            },
            "basic_information": {
                "identity_characteristic": optional_identity_characteristic if optional_identity_characteristic else None,
            }
        }
    }

    return back_side_identity_card_info


########################################################################################################################
# So sánh khuôn mặt đối chiếu với khuôn mặt trên giấy tờ định danh
########################################################################################################################
async def repos_compare_face(face_image_data: bytes, identity_image_uuid: str, session: Session):
    is_success_add_face, add_face_info = await service_ekyc.add_face(file=face_image_data)

    if not is_success_add_face:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_EKYC, detail=add_face_info.get('message', ''))

    face_uuid = add_face_info.get('data').get('uuid')
    is_success, compare_face_info = await service_ekyc.compare_face(face_uuid, identity_image_uuid)

    if not is_success:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_EKYC,
            detail=compare_face_info['message'],
            loc="identity_image_uuid, face_image"
        )

    return ReposReturn(data={
        "similar_percent": compare_face_info.get('data').get('similarity_percent'),
        "face_uuid_ekyc": face_uuid
    })
