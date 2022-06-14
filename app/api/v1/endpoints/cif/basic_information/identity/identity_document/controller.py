from typing import Optional, Union

from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_compare_face, repos_get_detail_identity,
    repos_get_identity_image_transactions, repos_get_identity_information,
    repos_save_identity, repos_upload_identity_document_and_ocr,
    repos_validate_ekyc
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, OcrEkycRequest,
    PassportSaveRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_check_not_exist_cif_number, repos_get_booking
)
from app.api.v1.endpoints.file.controller import CtrFile
from app.api.v1.endpoints.file.validator import file_validator
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.api.v1.validator import validate_history_data
from app.settings.config import DATE_INPUT_OUTPUT_EKYC_FORMAT
from app.settings.event import service_ekyc
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressType, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerClassification, CustomerEconomicProfession, CustomerGender
)
from app.third_parties.oracle.models.master_data.identity import (
    PassportCode, PassportType, PlaceOfIssue
)
from app.third_parties.oracle.models.master_data.others import Nation, Religion
from app.utils.constant.approval import CIF_STAGE_BEGIN
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.cif import (
    ADDRESS_COUNTRY_CODE_VN, CHANNEL_AT_THE_COUNTER, CONTACT_ADDRESS_CODE,
    CRM_GENDER_TYPE_MALE, CUSTOMER_UNCOMPLETED_FLAG,
    EKYC_DOCUMENT_TYPE_NEW_CITIZEN, EKYC_DOCUMENT_TYPE_NEW_IDENTITY,
    EKYC_DOCUMENT_TYPE_OLD_CITIZEN, EKYC_DOCUMENT_TYPE_OLD_IDENTITY,
    EKYC_DOCUMENT_TYPE_PASSPORT, EKYC_GENDER_TYPE_FEMALE,
    EKYC_GENDER_TYPE_MALE, EKYC_IDENTITY_TYPE, IDENTITY_DOCUMENT_TYPE,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, IDENTITY_DOCUMENT_TYPE_TYPE,
    IDENTITY_IMAGE_FLAG_BACKSIDE, IDENTITY_IMAGE_FLAG_FRONT_SIDE,
    IMAGE_TYPE_CODE_IDENTITY, PROFILE_HISTORY_DESCRIPTIONS_INIT_CIF,
    PROFILE_HISTORY_STATUS_INIT, RESIDENT_ADDRESS_CODE, CRM_TITLE_TYPE_MALE, CRM_GENDER_TYPE_FEMALE,
    CRM_TITLE_TYPE_FEMALE
)
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_OPEN_CIF, IDM_MENU_CODE_OPEN_CIF,
    IDM_PERMISSION_CODE_OPEN_CIF
)
from app.utils.error_messages import (  # noqa
    ERROR_CALL_SERVICE_EKYC, ERROR_IDENTITY_DOCUMENT_NOT_EXIST,
    ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST, ERROR_IDENTITY_TYPE_NOT_EXIST,
    ERROR_INVALID_URL, ERROR_NO_DATA, ERROR_NOT_NULL,
    ERROR_WRONG_TYPE_IDENTITY, MESSAGE_STATUS
)
from app.utils.functions import (  # noqa
    calculate_age, date_to_string, datetime_to_string, dropdown, now,
    orjson_dumps, parse_file_uuid
)
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, make_short_name, split_name
)


class CtrIdentityDocument(BaseController):
    async def detail_identity(self, cif_id: str):
        detail_data = self.call_repos(
            await repos_get_detail_identity(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        front_side_image = None
        back_side_image = None
        identity_image = None
        if detail_data['identity_document_type']['id'] == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            identity_image = detail_data['passport_information']['identity_image_url']
            compare_image = detail_data['passport_information']['face_compare_image_url']
            fingerprints = detail_data['passport_information']['fingerprint']
            image_uuids = [identity_image, compare_image]
        else:
            front_side_image = detail_data['front_side_information']['identity_image_url']
            back_side_image = detail_data['back_side_information']['identity_image_url']
            compare_image = detail_data['front_side_information']['face_compare_image_url']
            fingerprints = detail_data['back_side_information']['fingerprint']
            image_uuids = [front_side_image, back_side_image, compare_image]

        fingerprint_image_uuids = []
        for fingerprint in fingerprints:
            fingerprint_image_uuids.append(fingerprint['image_url'])
        image_uuids = image_uuids + fingerprint_image_uuids

        # uuid__link_downloads sẽ trả về 1 dict dạng { uuid: url } nên map chỉ cần gán uuid vào là được
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        if detail_data['identity_document_type']['id'] == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            detail_data['passport_information']['identity_image_url'] = uuid__link_downloads[identity_image]
            detail_data['passport_information']['face_compare_image_url'] = uuid__link_downloads[compare_image]
        else:
            detail_data['front_side_information']['identity_image_url'] = uuid__link_downloads[front_side_image]
            detail_data['back_side_information']['identity_image_url'] = uuid__link_downloads[back_side_image]
            detail_data['front_side_information']['face_compare_image_url'] = uuid__link_downloads[compare_image]

        for fingerprint in fingerprints:
            fingerprint['image_url'] = uuid__link_downloads[fingerprint['image_url']]

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        detail_data.update(
            booking=dict(
                id=booking.id,
                code=booking.code
            )
        )

        return detail_data['identity_document_type']['code'], self.response(data=detail_data)

    async def get_identity_log_list(self, cif_id: str):
        identity_image_transactions = self.call_repos(await repos_get_identity_image_transactions(
            cif_id=cif_id, session=self.oracle_session
        ))
        identity_log_infos = []
        if not identity_image_transactions:
            return self.response(data=identity_log_infos)

        # các uuid cần phải gọi qua service file để check
        image_uuids = [
            identity_image_transaction.image_url for identity_image_transaction in identity_image_transactions
        ]

        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        date__identity_images = {}

        for identity_image_transaction in identity_image_transactions:
            maker_at = date_to_string(identity_image_transaction.maker_at)

            if maker_at not in date__identity_images.keys():
                date__identity_images[maker_at] = []

            date__identity_images[maker_at].append({
                "image_url": uuid__link_downloads[identity_image_transaction.image_url]
            })

        identity_log_infos = [{
            "reference_flag": True if index == 0 else False,
            "created_date": created_date,
            "identity_images": identity_images
        } for index, (created_date, identity_images) in enumerate(date__identity_images.items())]

        identity_log_infos[0]["reference_flag"] = True

        return self.response(data=identity_log_infos)

    async def save_identity(
            self,
            booking_id: Optional[str],
            identity_document_request: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest]
    ):

        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        # Kiểm tra xem Booking_id đã sử dụng chưa
        await CtrBooking().is_used_booking(booking_id=booking_id)

        # check quyền user
        self.call_repos(await PermissionController.ctr_approval_check_permission(
            auth_response=self.current_user,
            menu_code=IDM_MENU_CODE_OPEN_CIF,
            group_role_code=IDM_GROUP_ROLE_CODE_OPEN_CIF,
            permission_code=IDM_PERMISSION_CODE_OPEN_CIF,
            stage_code=CIF_STAGE_BEGIN
        ))

        current_user = self.current_user.user_info
        current_user_code = current_user.code
        # Dữ liệu validate chung
        validate_religion_name = None
        validate_ethnic_name = None
        ekyc_document_type_request = None

        if identity_document_request.identity_document_type.id not in IDENTITY_DOCUMENT_TYPE:
            return self.response_exception(msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='identity_document_type -> id')

        # trong body có truyền cif_id khác None thì lưu lại, truyền bằng None thì sẽ là tạo mới
        cif_id = identity_document_request.cif_id

        customer: Optional[Customer] = None
        customer_identity: Optional[CustomerIdentity] = None
        customer_individual_info: Optional[CustomerIndividualInfo] = None
        # customer_resident_address: Optional[CustomerAddress] = None
        customer_contact_address: Optional[CustomerAddress] = None

        is_create = True
        if cif_id:
            # móc dữ liệu đã có để so sánh với identity_document_request
            customer, customer_identity, customer_individual_info, customer_resident_address, customer_contact_address \
                = self.call_repos(await repos_get_identity_information(customer_id=cif_id, session=self.oracle_session))

            is_create = False

        cif_information = identity_document_request.cif_information
        identity_document = identity_document_request.ocr_result.identity_document
        basic_information = identity_document_request.ocr_result.basic_information
        identity_document_type_id = identity_document_request.identity_document_type.id
        address_information = None
        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            address_information = identity_document_request.ocr_result.address_information  # CMND, CCCD

        # RULE: Nếu không chọn số cif tùy chỉnh thì không được gửi cif_number lên
        if not identity_document_request.cif_information.self_selected_cif_flag \
                and identity_document_request.cif_information.cif_number:
            return self.response_exception(
                msg='',
                detail='CIF number is not allowed to be sent if self-selected CIF flag is false'
            )

        # RULE: Nếu chọn số cif tùy chỉnh thì phải gửi cif_number lên
        if identity_document_request.cif_information.self_selected_cif_flag \
                and not identity_document_request.cif_information.cif_number:
            return self.response_exception(
                msg='',
                detail='CIF number is required if self-selected CIF flag is true'
            )

        # RULE: số CIF không được khách hàng khác sử dụng
        if is_create or (customer.cif_number != cif_information.cif_number):
            self.call_repos(await repos_check_not_exist_cif_number(
                cif_number=cif_information.cif_number,
                session=self.oracle_session
            ))

        full_name_vn = identity_document_request.ocr_result.basic_information.full_name_vn
        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        first_name, middle_name, last_name = split_name(full_name)
        if first_name is None and middle_name is None and last_name is None:
            return self.response_exception(msg='', detail='Can not split name to fist, middle and last name')

        # check customer_economic_profession_id
        customer_economic_profession_id = identity_document_request.cif_information.customer_economic_profession.id
        if is_create or (customer.customer_economic_profession_id != customer_economic_profession_id):
            await self.get_model_object_by_id(model_id=customer_economic_profession_id,
                                              model=CustomerEconomicProfession,
                                              loc='customer_economic_profession_id')

        # check customer_classification_id
        customer_classification_id = identity_document_request.cif_information.customer_classification.id
        if is_create or (customer.customer_classification_id != customer_classification_id):
            await self.get_model_object_by_id(model_id=customer_classification_id,
                                              model=CustomerClassification,
                                              loc='customer_classification_id')

        # check identity_document_type_type_id
        identity_document_type_type_id = identity_document_request.identity_document_type.type_id
        if identity_document_type_type_id not in EKYC_IDENTITY_TYPE:
            return self.response_exception(
                msg=ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST,
                detail=MESSAGE_STATUS[ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST],
                loc="identity_document_type -> type_id"
            )

        # check nationality_id
        nationality_id = "VN"  # TODO: do Model bắt buộc không được Null
        if basic_information.nationality:
            nationality_id = basic_information.nationality.id
        if nationality_id:
            if is_create or (customer_individual_info.country_of_birth_id != nationality_id):
                await self.get_model_object_by_id(
                    model_id=nationality_id,
                    model=AddressCountry,
                    loc='nationality_id'
                )

        # dict dùng để tạo mới hoặc lưu lại customer
        saving_customer = {
            "cif_number": identity_document_request.cif_information.cif_number,
            "self_selected_cif_flag": identity_document_request.cif_information.self_selected_cif_flag,
            "full_name": full_name,
            "full_name_vn": full_name_vn,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "short_name": make_short_name(first_name, middle_name, last_name),
            "active_flag": True,
            "open_cif_at": now(),
            "open_branch_id": current_user.hrm_branch_code,
            "kyc_level_id": "EKYC_1",  # TODO
            "customer_category_id": "I_11",  # TODO
            "customer_economic_profession_id": customer_economic_profession_id,
            "nationality_id": nationality_id,
            "customer_classification_id": customer_classification_id,
            "customer_status_id": "1",  # TODO
            "channel_id": CHANNEL_AT_THE_COUNTER,  # TODO
            "avatar_url": None,
            "complete_flag": CUSTOMER_UNCOMPLETED_FLAG
        }
        ################################################################################################################

        place_of_issue_id = identity_document.place_of_issue.id
        # RULE: Trường hợp đặc biệt: dù tạo mới, cập nhật hay không cũng phải dùng để validate field bên EKYC
        # if is_create or (customer_identity.place_of_issue_id != place_of_issue_id):
        validate_place_of_issue = await self.get_model_object_by_id(model_id=place_of_issue_id, model=PlaceOfIssue,
                                                                    loc='place_of_issue_id')
        validate_place_of_issue_name = validate_place_of_issue.name
        # RULE: Trường hợp đặc biệt, giá trị "TPHCM" ở core không đúng với chuẩn giá trị GTDD của chính phủ quy định
        # Nên việc validate không hợp lệ, cần phải thay đổi để validate
        # RULE: Trường hợp đặc biệt: Do data validate gửi xuống EKYC yêu cầu phải là "Tp Hồ Chí Minh"
        if validate_place_of_issue_name == "TPHCM":
            validate_place_of_issue_name = "Tp Hồ Chí Minh"

        # dict dùng để tạo mới hoặc lưu lại customer_identity
        saving_customer_identity = {
            "identity_type_id": identity_document_request.identity_document_type.id,
            "identity_num": identity_document.identity_number,
            "issued_date": identity_document.issued_date,
            "expired_date": identity_document.expired_date,
            "place_of_issue_id": place_of_issue_id,
            "maker_at": now(),
            "maker_id": current_user_code,
            "updater_at": now(),
            "updater_id": current_user_code,
            "ocr_result": orjson_dumps(identity_document_request.ocr_result_ekyc)
        }

        gender_id = basic_information.gender.id
        title_id = None
        if gender_id == CRM_GENDER_TYPE_MALE:
            title_id = CRM_TITLE_TYPE_MALE

        if gender_id == CRM_GENDER_TYPE_FEMALE:
            title_id = CRM_TITLE_TYPE_FEMALE

        # RULE: Trường hợp đặc biệt: dù tạo mới, cập nhật hay không cũng phải dùng để validate field bên EKYC
        # if is_create or (customer_individual_info.gender_id != gender_id):
        validate_gender = await self.get_model_object_by_id(model_id=gender_id, model=CustomerGender,
                                                            loc='gender_id')
        validate_gender_code = validate_gender.code

        religion_id = None
        ethnic_id = None
        identity_characteristic = None
        father_full_name_vn = None
        mother_full_name_vn = None
        if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            province_id = basic_information.place_of_birth.id
        else:
            province_id = basic_information.province.id
            identity_characteristic = basic_information.identity_characteristic
            if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
                # check ethnic_id
                ethnic_id = basic_information.ethnic.id
                # RULE: Trường hợp đặc biệt: dù tạo mới, cập nhật hay không cũng phải dùng để validate field bên EKYC
                # if is_create or (customer_individual_info.nation_id != ethnic_id):
                validate_ethnic = await self.get_model_object_by_id(model_id=ethnic_id, model=Nation, loc='ethnic_id')
                validate_ethnic_name = validate_ethnic.name

                # check religion_id
                religion_id = basic_information.religion.id
                if is_create or (customer_individual_info.religion_id != religion_id):
                    await self.get_model_object_by_id(model_id=religion_id, model=Religion, loc='religion_id')

                father_full_name_vn = basic_information.father_full_name_vn
                mother_full_name_vn = basic_information.mother_full_name_vn

        # check place_of_birth or province.id        # check place_of_birth or province.id
        # RULE: Trường hợp đặc biệt: dù tạo mới, cập nhật hay không cũng phải dùng để validate field bên EKYC
        # if is_create or (customer_individual_info.place_of_birth_id != province_id):
        validate_place_of_birth = await self.get_model_object_by_id(model_id=province_id, model=AddressProvince,
                                                                    loc='province_id')
        validate_place_of_birth_name = validate_place_of_birth.name

        # Nên việc validate không hợp lệ, cần phải thay đổi để validate
        # RULE: Trường hợp đặc biệt: Do data validate gửi xuống EKYC yêu cầu phải là "Tp Hồ Chí Minh"
        if validate_place_of_birth_name == "TPHCM":
            validate_place_of_birth_name = "Tp Hồ Chí Minh"

        # dict dùng để tạo mới hoặc lưu lại customer_individual_info
        saving_customer_individual_info = {
            "gender_id": gender_id,
            "place_of_birth_id": province_id,
            "country_of_birth_id": nationality_id,
            "religion_id": religion_id,
            "nation_id": ethnic_id,
            "date_of_birth": basic_information.date_of_birth,
            "under_15_year_old_flag": True if calculate_age(basic_information.date_of_birth) < 15 else False,
            "identifying_characteristics": identity_characteristic,
            "father_full_name": father_full_name_vn,
            "mother_full_name": mother_full_name_vn,
            "title_id": title_id
        }

        ################################################################################################################

        ekyc_request_data = dict(
            document_id=saving_customer_identity['identity_num'],
            date_of_birth=date_to_string(basic_information.date_of_birth, _format=DATE_INPUT_OUTPUT_EKYC_FORMAT),
            full_name=full_name_vn,
            date_of_issue=date_to_string(identity_document.issued_date, _format=DATE_INPUT_OUTPUT_EKYC_FORMAT),
            place_of_issue=validate_place_of_issue_name
        )

        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            resident_address = await self.get_model_object_by_code(
                model_code=RESIDENT_ADDRESS_CODE, model=AddressType, loc='resident_address'
            )
            # check resident_address_province_id
            resident_address_province_id = address_information.resident_address.province.id
            # RULE: Trường hợp đặc biệt: dù tạo mới, cập nhật hay không cũng phải dùng để validate field bên EKYC
            # if is_create or (customer_resident_address.address_province_id != resident_address_province_id):
            resident_address_province = await self.get_model_object_by_id(model_id=resident_address_province_id,
                                                                          model=AddressProvince,
                                                                          loc='resident_address -> province -> id')
            resident_address_province_name = resident_address_province.name
            # RULE: Trường hợp đặc biệt: Do data validate gửi xuống EKYC yêu cầu phải là "Tp Hồ Chí Minh"
            if resident_address_province_name == "TPHCM":
                resident_address_province_name = "Tp Hồ Chí Minh"

            # check resident_address_district_id
            resident_address_district_id = address_information.resident_address.district.id
            # RULE: Trường hợp đặc biệt: dù tạo mới, cập nhật hay không cũng phải dùng để validate field bên EKYC
            # if is_create or (customer_resident_address.address_district_id != resident_address_district_id):
            resident_address_district = await self.get_model_object_by_id(model_id=resident_address_district_id,
                                                                          model=AddressDistrict,
                                                                          loc='resident_address -> district -> id')
            resident_address_district_name = resident_address_district.name

            # check resident_address_ward_id
            resident_address_ward_id = address_information.resident_address.ward.id
            # RULE: Trường hợp đặc biệt: dù tạo mới, cập nhật hay không cũng phải dùng để validate field bên EKYC
            # if is_create or (customer_resident_address.address_ward_id != resident_address_ward_id):
            resident_address_ward = await self.get_model_object_by_id(
                model_id=resident_address_ward_id,
                model=AddressWard,
                loc='resident_address -> ward -> id'
            )
            resident_address_ward_name = resident_address_ward.name

            # check resident_address_number_and_street
            resident_address_number_and_street = address_information.resident_address.number_and_street
            if not resident_address_number_and_street:
                return self.response_exception(
                    msg=ERROR_NOT_NULL,
                    detail="number_and_street " + MESSAGE_STATUS[ERROR_NOT_NULL],
                    loc="resident_address -> number_and_street"
                )

            # dict dùng để tạo mới hoặc lưu lại customer_resident_address
            saving_customer_resident_address = {
                "address_type_id": resident_address.id,
                "address_country_id": nationality_id,
                "address_province_id": resident_address_province_id,
                "address_district_id": resident_address_district_id,
                "address_ward_id": resident_address_ward_id,
                "address": resident_address_number_and_street,
                "address_domestic_flag": True if nationality_id == ADDRESS_COUNTRY_CODE_VN else False
            }
            ###########################################################################################################

            contact_address = await self.get_model_object_by_code(
                model_code=CONTACT_ADDRESS_CODE, model=AddressType, loc='resident_address'
            )

            # check contact_address_province_id
            contact_address_province_id = address_information.contact_address.province.id
            if is_create or (customer_contact_address.address_province_id != contact_address_province_id):
                await self.get_model_object_by_id(model_id=contact_address_province_id, model=AddressProvince,
                                                  loc='contact_address -> province -> id')

            # check contact_address_district_id
            contact_address_district_id = address_information.contact_address.district.id
            if is_create or (customer_contact_address.address_district_id != contact_address_district_id):
                await self.get_model_object_by_id(model_id=contact_address_district_id, model=AddressDistrict,
                                                  loc='contact_address -> district -> id')

            # check contact_address_ward_id
            contact_address_ward_id = address_information.contact_address.ward.id
            if is_create or (customer_contact_address.address_ward_id != contact_address_ward_id):
                await self.get_model_object_by_id(model_id=contact_address_ward_id, model=AddressWard,
                                                  loc='contact_address -> ward -> id')

            # check contact_address_number_and_street
            contact_address_number_and_street = address_information.contact_address.number_and_street
            if not contact_address_number_and_street:
                return self.response_exception(
                    msg=ERROR_NOT_NULL,
                    detail="number_and_street " + MESSAGE_STATUS[ERROR_NOT_NULL],
                    loc="contact_address -> number_and_street"
                )

            # dict dùng để tạo mới hoặc lưu lại customer_contact_address
            saving_customer_contact_address = {
                "address_type_id": contact_address.id,
                "address_country_id": nationality_id,
                "address_province_id": contact_address_province_id,
                "address_district_id": contact_address_district_id,
                "address_ward_id": contact_address_ward_id,
                "address": contact_address_number_and_street,
                "address_domestic_flag": True,  # Địa chỉ liên lạc đối với CMND/CCCD là địa chỉ trong nước
            }
            ############################################################################################################

            if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
                signer = identity_document_request.ocr_result.identity_document.signer
                if not signer:
                    return self.response_exception(
                        msg=ERROR_NO_DATA,
                        detail="No Signer",
                        loc="front_side_information -> ocr_result -> identity_document -> signer"
                    )
                saving_customer_identity.update({
                    "qrcode_content": identity_document_request.ocr_result.identity_document.qr_code_content,
                    "mrz_content": identity_document_request.ocr_result.identity_document.mrz_content,
                    "signer": signer
                })
            ############################################################################################################

            front_side_information_identity_image_uuid = parse_file_uuid(
                url=identity_document_request.front_side_information.identity_image_url
            )
            face_compare_image_url = parse_file_uuid(
                identity_document_request.front_side_information.face_compare_image_url)
            if not front_side_information_identity_image_uuid:
                return self.response_exception(
                    msg=ERROR_INVALID_URL,
                    detail=MESSAGE_STATUS[ERROR_INVALID_URL],
                    loc="front_side_information -> identity_image_url"
                )
            identity_image_uuid = front_side_information_identity_image_uuid

            identity_avatar_image_uuid = identity_document_request.front_side_information.identity_avatar_image_uuid
            # Thêm avatar với Image Type là khuôn mặt vào DB

            back_side_information_identity_image_uuid = parse_file_uuid(
                identity_document_request.back_side_information.identity_image_url)
            if not front_side_information_identity_image_uuid:
                return self.response_exception(
                    msg=ERROR_INVALID_URL,
                    detail=MESSAGE_STATUS[ERROR_INVALID_URL],
                    loc="back_side_information -> identity_image_url"
                )
            compare_face_uuid_ekyc = identity_document_request.front_side_information.face_uuid_ekyc
            saving_customer_identity_images = [
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": front_side_information_identity_image_uuid,
                    "avatar_image_uuid": identity_avatar_image_uuid,
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": current_user_code,
                    "maker_at": now(),
                    "updater_id": current_user_code,
                    "updater_at": now(),
                    "identity_image_front_flag": IDENTITY_IMAGE_FLAG_FRONT_SIDE
                },
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": back_side_information_identity_image_uuid,
                    # lưu CMND, CCCD mặt sau k có avatar
                    "avatar_image_uuid": None,
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": current_user_code,
                    "maker_at": now(),
                    "updater_id": current_user_code,
                    "updater_at": now(),
                    "identity_image_front_flag": IDENTITY_IMAGE_FLAG_BACKSIDE
                }
            ]

            place_of_residence = f"{resident_address_number_and_street}, " \
                                 f"{resident_address_ward_name}, " \
                                 f"{resident_address_district_name}, " \
                                 f"{resident_address_province_name}"

            # VALIDATE: EKYC CMND
            if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:

                ekyc_request_data.update(
                    place_of_origin=validate_place_of_birth_name,
                    place_of_residence=place_of_residence,
                    ethnicity=validate_ethnic_name,
                    religion=validate_religion_name,
                    personal_identification=identity_characteristic
                )

                if identity_document_type_type_id == EKYC_DOCUMENT_TYPE_OLD_IDENTITY:
                    ekyc_document_type_request = identity_document_type_type_id

                if identity_document_type_type_id == EKYC_DOCUMENT_TYPE_NEW_IDENTITY:
                    ekyc_document_type_request = identity_document_type_type_id
                    ekyc_request_data.update(
                        father_name=father_full_name_vn,
                        mother_name=mother_full_name_vn,
                        date_of_expiry=date_to_string(identity_document.expired_date,
                                                      _format=DATE_INPUT_OUTPUT_EKYC_FORMAT),
                        gender=EKYC_GENDER_TYPE_MALE if validate_gender_code == CRM_GENDER_TYPE_MALE else EKYC_GENDER_TYPE_FEMALE,
                    )
            # VALIDATE: EKYC CCCD
            else:
                ekyc_request_data.update(
                    place_of_origin=validate_place_of_birth_name,
                    place_of_residence=place_of_residence,
                    date_of_expiry=date_to_string(identity_document.expired_date,
                                                  _format=DATE_INPUT_OUTPUT_EKYC_FORMAT),
                    gender=EKYC_GENDER_TYPE_MALE if validate_gender_code == CRM_GENDER_TYPE_MALE else EKYC_GENDER_TYPE_FEMALE,
                    personal_identification=identity_characteristic,
                    signer=identity_document_request.ocr_result.identity_document.signer
                )

                if identity_document_type_type_id == EKYC_DOCUMENT_TYPE_OLD_CITIZEN:
                    ekyc_document_type_request = identity_document_type_type_id

                if identity_document_type_type_id == EKYC_DOCUMENT_TYPE_NEW_CITIZEN:
                    mrz_content = identity_document_request.ocr_result.identity_document.mrz_content
                    ekyc_document_type_request = identity_document_type_type_id
                    ekyc_request_data.update(
                        mrz_1=mrz_content[:30] if mrz_content else None,
                        mrz_2=mrz_content[30:60] if mrz_content else None,
                        mrz_3=mrz_content[60:] if mrz_content else None,
                        qr_code=identity_document_request.ocr_result.identity_document.qr_code_content,
                    )

        # HO_CHIEU
        else:
            if identity_document_type_type_id == EKYC_DOCUMENT_TYPE_PASSPORT:
                ekyc_document_type_request = identity_document_type_type_id

            saving_customer_resident_address = None
            saving_customer_contact_address = None
            identity_number_in_passport = identity_document_request.ocr_result.basic_information.identity_card_number
            # check passport_type
            await self.get_model_object_by_id(
                model_id=identity_document_request.ocr_result.identity_document.passport_type.id,
                model=PassportType,
                loc="passport_type"
            )

            # check passport_code
            await self.get_model_object_by_id(
                model_id=identity_document_request.ocr_result.identity_document.passport_code.id,
                model=PassportCode,
                loc="passport_code"
            )

            saving_customer_identity.update({
                "passport_type_id": identity_document_request.ocr_result.identity_document.passport_type.id,
                "passport_code_id": identity_document_request.ocr_result.identity_document.passport_code.id,
                "identity_number_in_passport": identity_number_in_passport,
                "mrz_content": identity_document_request.ocr_result.basic_information.mrz_content
            })
            ############################################################################################################

            compare_face_uuid_ekyc = identity_document_request.passport_information.face_uuid_ekyc
            face_compare_image_url = parse_file_uuid(
                identity_document_request.passport_information.face_compare_image_url)
            identity_image_uuid = parse_file_uuid(identity_document_request.passport_information.identity_image_url)
            if not identity_image_uuid:
                return self.response_exception(
                    msg=ERROR_INVALID_URL,
                    detail=MESSAGE_STATUS[ERROR_INVALID_URL],
                    loc="passport_information -> identity_image_url"
                )
            identity_avatar_image_uuid = identity_document_request.passport_information.identity_avatar_image_uuid
            saving_customer_identity_images = [
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": identity_image_uuid,
                    "avatar_image_uuid": identity_avatar_image_uuid,
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": current_user_code,
                    "maker_at": now(),
                    "updater_id": current_user_code,
                    "updater_at": now(),
                    "identity_image_front_flag": None
                }
            ]

            # VALIDATE: EKYC HO_CHIEU
            # Mỗi dòng có tổng cộng 44 ký tự bao gồm dấu "<".
            passport_mrz_content = identity_document_request.ocr_result.basic_information.mrz_content
            mrz_1 = passport_mrz_content[:44]
            mrz_2 = passport_mrz_content[44:]

            ekyc_request_data.update(
                date_of_expiry=date_to_string(identity_document.expired_date, _format=DATE_INPUT_OUTPUT_EKYC_FORMAT),
                gender=EKYC_GENDER_TYPE_MALE if validate_gender_code == CRM_GENDER_TYPE_MALE else EKYC_GENDER_TYPE_FEMALE,
                mrz_1=mrz_1,
                mrz_2=mrz_2,
                nationality="Việt Nam",  # TODO
                id_card_number=identity_number_in_passport
            )

        # RULE: Trường hợp gửi type_id không nằm trong identity_document_type_id
        if ekyc_document_type_request is None:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_WRONG_TYPE_IDENTITY],
                detail=f"{IDENTITY_DOCUMENT_TYPE_TYPE}",
                loc="identity_document_type -> type_id"
            )
        # is_valid, validate_response = await service_ekyc.validate(data=ekyc_request_data,
        #                                                           document_type=ekyc_document_type_request)
        # if not is_valid:
        #     errors = validate_response['errors']
        #     return_errors = []
        #     for key, value in errors.items():
        #         return_errors.append(f"{key} -> {value}")
        #     return self.response_exception(msg=ERROR_CALL_SERVICE_EKYC, detail=', '.join(return_errors))

        # So sánh khuôn mặt
        if not compare_face_uuid_ekyc:
            return self.response_exception(
                msg=ERROR_INVALID_URL,
                detail=MESSAGE_STATUS[ERROR_INVALID_URL],
                loc="passport_information -> face_uuid_ekyc"
            )
        await self.check_exist_multi_file(uuids=[identity_image_uuid, face_compare_image_url])

        is_success, compare_response = await service_ekyc.compare_face(
            face_uuid=compare_face_uuid_ekyc,
            avatar_image_uuid=identity_avatar_image_uuid,
            booking_id=booking_id
        )

        if not is_success:
            return self.response_exception(
                loc="face_uuid_ekyc",
                msg=ERROR_CALL_SERVICE_EKYC,
                detail=compare_response['message']
            )
        similar_percent = compare_response['data']['similarity_percent']

        # dict dùng để tạo mới hoặc lưu lại CustomerCompareImage
        saving_customer_compare_image = {
            "id": compare_face_uuid_ekyc,
            "compare_image_url": face_compare_image_url,
            "similar_percent": similar_percent,  # gọi qua eKYC để check
            "maker_id": current_user_code,
            "maker_at": now()
        }

        # Lưu hình ảnh Compare thành avatar khách hàng
        saving_customer.update(avatar_url=face_compare_image_url)
        ############################################################################################################

        ################################################################################################################
        # Thêm avatar thành Hình ảnh định danh Khuôn mặt
        ################################################################################################################
        avatar_image_uuid_service = await CtrFile().upload_ekyc_file(
            uuid_ekyc=identity_avatar_image_uuid,
            booking_id=booking_id
        )
        ################################################################################################################
        # Tạo data TransactionDaily và các TransactionStage khác cho bước mở CIF
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            business_type_id=BUSINESS_TYPE_INIT_CIF
        )

        (
            saving_transaction_stage_status, saving_transaction_stage, saving_transaction_stage_phase,
            saving_transaction_stage_lane, saving_transaction_stage_role, saving_transaction_daily,
            saving_transaction_sender
        ) = transaction_datas

        request_data = await parse_identity_model_to_dict(
            request=identity_document_request,
            identity_document_type_id=identity_document_type_id
        )

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_CIF,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_datas)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        info_save_document = self.call_repos(
            await repos_save_identity(
                identity_document_type_id=identity_document_type_id,
                customer_id=None if is_create else customer.id,
                identity_id=None if is_create else customer_identity.id,
                saving_customer=saving_customer,
                saving_customer_identity=saving_customer_identity,
                saving_customer_individual_info=saving_customer_individual_info,
                saving_customer_resident_address=saving_customer_resident_address,
                saving_customer_contact_address=saving_customer_contact_address,
                saving_customer_compare_image=saving_customer_compare_image,
                saving_customer_identity_images=saving_customer_identity_images,
                saving_transaction_stage_status=saving_transaction_stage_status,
                saving_transaction_stage=saving_transaction_stage,
                saving_transaction_stage_phase=saving_transaction_stage_phase,
                saving_transaction_stage_lane=saving_transaction_stage_lane,
                saving_transaction_stage_role=saving_transaction_stage_role,
                saving_transaction_daily=saving_transaction_daily,
                saving_transaction_sender=saving_transaction_sender,
                # saving_transaction_receiver=saving_transaction_receiver,
                avatar_image_uuid_service=avatar_image_uuid_service,
                identity_avatar_image_uuid_ekyc=identity_avatar_image_uuid,
                booking_id=booking_id,
                request_data=orjson_dumps(request_data),
                history_datas=orjson_dumps(history_datas),
                current_user=current_user,
                session=self.oracle_session
            )
        )
        return self.response(data=info_save_document)

    async def upload_identity_document_and_ocr(self, identity_type: int, image_file: UploadFile, booking_id: str):

        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        if identity_type not in EKYC_IDENTITY_TYPE:
            return self.response_exception(msg=ERROR_IDENTITY_TYPE_NOT_EXIST, loc='identity_type')

        image_file_name = image_file.filename
        image_data = await image_file.read()

        self.call_validator(await file_validator(image_data))

        upload_info = self.call_repos(
            await repos_upload_identity_document_and_ocr(
                image_file=image_data,
                image_file_name=image_file_name,
                identity_type=identity_type,
                session=self.oracle_session
            )
        )

        return self.response(data=upload_info)

    async def compare_face(self, face_image: UploadFile, identity_image_uuid: str, booking_id: Optional[str]):

        face_image_data = await face_image.read()
        self.call_validator(await file_validator(face_image_data))

        face_compare_info = self.call_repos(
            await repos_compare_face(
                face_image_data=face_image_data,
                identity_image_uuid=identity_image_uuid,
                booking_id=booking_id
            )
        )

        return self.response(data=face_compare_info)

    async def validate_ekyc(self, ocr_ekyc_request: OcrEkycRequest, booking_id: Optional[str]):

        qc_code = ocr_ekyc_request.qr_code

        if not ocr_ekyc_request.data:
            return self.response_exception(msg=ERROR_NO_DATA)

        request_body = {
            "document_type": ocr_ekyc_request.document_type,
            "data": ocr_ekyc_request.data
        }

        if ocr_ekyc_request.document_type == EKYC_DOCUMENT_TYPE_NEW_CITIZEN:
            request_body['data'].update({
                'qr_code': qc_code
            })
        response = self.call_repos(await repos_validate_ekyc(
            request_body=request_body,
            booking_id=booking_id
        ))

        return self.response(data=response)


async def parse_identity_model_to_dict(
        identity_document_type_id,
        request
):
    request_cif_information = request.cif_information
    request_identity_document_type = request.identity_document_type

    request_ocr_result_identity_document = request.ocr_result.identity_document
    request_ocr_result_basic_information = request.ocr_result.basic_information

    request_data = {
        "cif_id": str(request.cif_id),
        "cif_information": {
            "self_selected_cif_flag": str(request_cif_information.self_selected_cif_flag),
            "cif_number": str(request_cif_information.cif_number),
            "customer_classification": {
                "id": str(request_cif_information.customer_classification.id)
            },
            "customer_economic_profession": {
                "id": str(request_cif_information.customer_economic_profession.id)
            }
        },
        "identity_document_type": {
            "id": request_identity_document_type.id,
            "type_id": request_identity_document_type.type_id
        },
        "ocr_result": {
            "identity_document": {
                "identity_number": request_ocr_result_identity_document.identity_number,
                "issued_date": date_to_string(request_ocr_result_identity_document.issued_date),
                "place_of_issue": {
                    "id": request_ocr_result_identity_document.place_of_issue.id,
                },
                "expired_date": date_to_string(request_ocr_result_identity_document.expired_date)
            },
            "basic_information": {
                "full_name_vn": request_ocr_result_basic_information.full_name_vn,
                "gender": {
                    "id": request_ocr_result_basic_information.gender.id
                },
                "date_of_birth": date_to_string(request_ocr_result_basic_information.date_of_birth),
                "nationality": {
                    "id": request_ocr_result_basic_information.nationality.id
                }
            }
        }
    }

    if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
        request_front_side_information = request.front_side_information
        request_back_side_information = request.back_side_information
        request_address_information_resident_address = request.ocr_result.address_information.resident_address
        request_address_information_contact_address = request.ocr_result.address_information.contact_address
        request_data.update({
            "front_side_information": {
                "identity_image_url": request_front_side_information.identity_image_url,
                "identity_avatar_image_uuid": request_front_side_information.identity_avatar_image_uuid,
                "face_compare_image_url": request_front_side_information.face_compare_image_url,
                "face_uuid_ekyc": request_front_side_information.face_uuid_ekyc
            },
            "back_side_information": {
                "identity_image_url": request_back_side_information.identity_image_url
            }
        })
        request_data["ocr_result"].update(dict(address_information={
            "resident_address": {
                "province": {
                    "id": request_address_information_resident_address.province.id
                },
                "district": {
                    "id": request_address_information_resident_address.district.id
                },
                "ward": {
                    "id": request_address_information_resident_address.ward.id
                },
                "number_and_street": request_address_information_resident_address.number_and_street
            },
            "contact_address": {
                "province": dict(id=request_address_information_contact_address.province.id),
                "district": {
                    "id": request_address_information_contact_address.district.id
                },
                "ward": {
                    "id": request_address_information_contact_address.ward.id
                },
                "number_and_street": request_address_information_contact_address.number_and_street
            }
        }))
        request_data["ocr_result"]['basic_information'].update({
            "province": {
                "id": request_ocr_result_basic_information.province.id
            },
            "identity_characteristic": str(request_ocr_result_basic_information.identity_characteristic),
        })

        if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
            request_data['ocr_result']['basic_information'].update({
                "ethnic": {
                    "id": str(request_ocr_result_basic_information.ethnic.id)
                },
                "religion": {
                    "id": str(request_ocr_result_basic_information.religion.id)
                },
                "father_full_name_vn": str(request_ocr_result_basic_information.father_full_name_vn),
                "mother_full_name_vn": str(request_ocr_result_basic_information.mother_full_name_vn)
            })
        else:
            request_data['ocr_result']['identity_document'].update({
                "mrz_content": str(request_ocr_result_identity_document.mrz_content),
                "qr_code_content": str(request_ocr_result_identity_document.qr_code_content),
                "signer": request_ocr_result_identity_document.signer
            })
    else:

        request_data['ocr_result']['identity_document'].update({
            "passport_type": {
                "id": request_ocr_result_identity_document.passport_type.id
            },
            "passport_code": {
                "id": request_ocr_result_identity_document.passport_code.id
            },
            "identity_card_number": request_ocr_result_basic_information.identity_card_number,
            "mrz_content": str(request_ocr_result_basic_information.mrz_content)
        })
        request_passport_information = request.passport_information
        request_data.update({
            "passport_information": {
                "identity_image_url": request_passport_information.identity_image_url,
                "identity_avatar_image_uuid": request_passport_information.identity_avatar_image_uuid,
                "face_compare_image_url": request_passport_information.face_compare_image_url,
                "face_uuid_ekyc": request_passport_information.face_uuid_ekyc
            }
        })
    return request_data
