from datetime import date

from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_save_identity, repos_upload_identity_document_and_ocr
)
from app.api.v1.endpoints.file.controller import CtrFile
from app.api.v1.endpoints.file.repository import repos_upload_file
from app.api.v1.validator import validate_history_data
from app.settings.event import service_ekyc
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.utils.constant.cif import (
    ADDRESS_COUNTRY_CODE_VN, BUSINESS_TYPE_INIT_CIF, CHANNEL_AT_THE_MOBILE,
    CLASSIFICATION_PERSONAL, CONTACT_ADDRESS_CODE, CUSTOMER_UNCOMPLETED_FLAG,
    EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD, EKYC_IDENTITY_TYPE_PASSPORT,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, IDENTITY_IMAGE_FLAG_BACKSIDE,
    IDENTITY_IMAGE_FLAG_FRONT_SIDE, IDENTITY_PASSPORT_TYPE_ID_DEFAULT,
    IMAGE_TYPE_CODE_IDENTITY, PROFILE_HISTORY_DESCRIPTIONS_INIT_CIF,
    PROFILE_HISTORY_STATUS_INIT, RESIDENT_ADDRESS_CODE
)
from app.utils.constant.ekyc import EKYC_FLAG
from app.utils.functions import calculate_age, datetime_to_string, now
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, make_short_name, split_name
)


class CtrIdentityMobile(BaseController):

    async def save_identity_mobile(
            self,
            full_name_vn: str,
            date_of_birth: date,
            gender_id: str,
            nationality_id: str,
            identity_number: str,
            issued_date: date,
            expired_date: date,
            place_of_issue_id: str,
            identity_type: str,
            front_side_image: UploadFile,
            back_side_image: UploadFile,
            avatar_image: UploadFile,
            signature_image: UploadFile,
    ):

        if not front_side_image or not avatar_image:
            return self.response_exception(msg='MISSING IMAGE')
        current_user = self.current_user
        # check back_side khi truyền identity_type không phải hộ chiếu
        if identity_type != IDENTITY_DOCUMENT_TYPE_PASSPORT and not back_side_image:
            return self.response_exception(msg='MISSING BACK_SIDE')

        # check validate field
        await self.get_model_object_by_id(model_id=gender_id, model=CustomerGender, loc='identity_mobile -> gender_id')
        await self.get_model_object_by_id(model_id=nationality_id, model=AddressCountry, loc='nationality_id')
        front_side_image_name = front_side_image.filename
        front_side_image = await front_side_image.read()

        # upload file front_side to service
        upload_front_side = self.call_repos(await repos_upload_file(
            file=front_side_image,
            name=front_side_image_name,
            ekyc_flag=EKYC_FLAG
        ))

        orc_data_front_side = None
        orc_data_back_side = None
        upload_back_side = None
        if identity_type == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            orc_data_front_side = self.call_repos(await repos_upload_identity_document_and_ocr(
                image_file=front_side_image,
                image_file_name=front_side_image_name,
                identity_type=EKYC_IDENTITY_TYPE_PASSPORT,
                session=self.oracle_session
            ))

        if back_side_image:
            back_side_image_name = back_side_image.filename
            back_side_image = await back_side_image.read()

            # upload file back_side to service
            upload_back_side = self.call_repos(await repos_upload_file(
                file=back_side_image,
                name=back_side_image_name,
                ekyc_flag=EKYC_FLAG
            ))

            # orc giấy tờ định danh
            if identity_type == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
                orc_data_front_side = self.call_repos(await repos_upload_identity_document_and_ocr(
                    image_file=front_side_image,
                    image_file_name=front_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD,
                    session=self.oracle_session
                ))

                orc_data_back_side = self.call_repos(await(repos_upload_identity_document_and_ocr(
                    image_file=back_side_image,
                    image_file_name=back_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD,
                    session=self.oracle_session
                )))

            if identity_type == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
                orc_data_front_side = self.call_repos(await repos_upload_identity_document_and_ocr(
                    image_file=front_side_image,
                    image_file_name=front_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD,
                    session=self.oracle_session
                ))

                orc_data_back_side = self.call_repos(await(repos_upload_identity_document_and_ocr(
                    image_file=back_side_image,
                    image_file_name=back_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD,
                    session=self.oracle_session
                )))

        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        first_name, middle_name, last_name = split_name(full_name)

        # data sử dụng lưu customer
        saving_customer = {  # noqa
            "cif_number": None,
            "self_selected_cif_flag": False,
            "full_name": full_name,
            "full_name_vn": full_name_vn,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "short_name": make_short_name(first_name, middle_name, last_name),
            "active_flag": True,
            "open_cif_at": now(),
            "open_branch_id": "000",  # TODO
            "kyc_level_id": "KYC_1",  # TODO
            "customer_category_id": "D0682B44BEB3830EE0530100007F1DDC",  # TODO
            "customer_economic_profession_id": None,
            "nationality_id": nationality_id,
            "customer_classification_id": CLASSIFICATION_PERSONAL,  # TODO hash core loại khách hàng
            "customer_status_id": "1",  # TODO
            "channel_id": CHANNEL_AT_THE_MOBILE,  # TODO
            "avatar_url": None,
            "complete_flag": CUSTOMER_UNCOMPLETED_FLAG
        }
        print('orc_data_front_side', orc_data_front_side)
        print('orc_data_back_side', orc_data_back_side)
        print(orc_data_front_side['ocr_result']['identity_document']['identity_number'])
        if orc_data_front_side['ocr_result']['identity_document']['identity_number'] != identity_number:
            return self.response_exception(msg='identity_number not same')
        # tạo customer_identity

        saving_customer_identity = {  # noqa
            "identity_type_id": identity_type,
            "identity_num": orc_data_front_side['ocr_result']['identity_document']['identity_number'],
            "issued_date": issued_date,
            "expired_date": expired_date,
            "place_of_issue_id": place_of_issue_id,
            "maker_at": now(),
            "maker_id": current_user.user_info.code,
            "updater_at": now(),
            "updater_id": current_user.user_info.code
        }
        if identity_type == "HO_CHIEU":
            saving_customer_identity.update({
                "mrz_content": orc_data_front_side['ocr_result']['basic_information']['mrz_content'],
                "passport_type_id": IDENTITY_PASSPORT_TYPE_ID_DEFAULT,
                "passport_code_id": orc_data_front_side['ocr_result']['identity_document']['passport_code']['id'],
                "identity_number_in_passport": orc_data_front_side['ocr_result']['basic_information']['identity_card_number']
            })
        if identity_type == "CCCD":
            saving_customer_identity.update({
                "qrcode_content": None,
                "mrz_content": orc_data_back_side['ocr_result']['identity_document']['mrz_content']
            })
        print('saving_customer_identity', saving_customer_identity)
        religion_id = None
        ethnic_id = None
        identity_characteristic = None
        address_province_id = None
        address_district_id = None
        address_ward_id = None
        resident_address_number_and_street = None

        contact_province_id = None
        contact_district_id = None
        contact_ward_id = None
        contact_number_and_street = None
        orc_gender_id = None
        if identity_type == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            province_id = orc_data_front_side['ocr_result']['basic_information']['place_of_birth']['id']
            orc_gender_id = orc_data_front_side['ocr_result']['basic_information']['gender']['id']
        else:
            # CCCD
            province_id = orc_data_front_side['ocr_result']['basic_information']['province']['id']
            identity_characteristic = orc_data_back_side['ocr_result']['basic_information']['identity_characteristic']

            # địa chỉ thường trú
            resident_address = orc_data_front_side['ocr_result']['address_information']['resident_address']
            address_province_id = resident_address['province']['id']
            address_district_id = resident_address['district']['id']
            address_ward_id = resident_address['ward']['id']
            resident_address_number_and_street = resident_address['number_and_street']

            # địa chỉ tạm trú
            contact_address = orc_data_front_side['ocr_result']['address_information']['contact_address']
            contact_province_id = contact_address['province']['id']
            contact_district_id = contact_address['district']['id']
            contact_ward_id = contact_address['ward']['id']
            contact_number_and_street = contact_address['number_and_street']
            # CMND
            if identity_type == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
                # dân tộc
                ethnic_id = orc_data_back_side['ocr_result']['basic_information']['ethnic']['id']
                # tôn giáo
                religion_id = orc_data_back_side['ocr_result']['basic_information']['religion']['id']
            else:
                # trường hợp cccd có giới tính
                orc_gender_id = orc_data_front_side['ocr_result']['basic_information']['gender']['id']

        print('orc_data_front_side', orc_data_front_side)
        # dict dùng để tạo mới hoặc lưu lại customer_individual_info
        if orc_gender_id and orc_gender_id != gender_id:
            return self.response_exception(msg='gender_id is not same')

        saving_customer_individual_info = {  # noqa
            "gender_id": gender_id,
            "place_of_birth_id": province_id,
            "country_of_birth_id": nationality_id,
            "religion_id": religion_id,
            "nation_id": ethnic_id,
            "date_of_birth": date_of_birth,
            "under_15_year_old_flag": True if calculate_age(date_of_birth) < 15 else False,
            "identifying_characteristics": identity_characteristic,
            "father_full_name": None,
            "mother_full_name": None
        }

        print('saving_customer_individual_info', saving_customer_individual_info)
        # dict dùng để lưu lại customer_resident_address

        saving_customer_resident_address = {  # noqa
            "address_type_id": RESIDENT_ADDRESS_CODE,
            "address_country_id": nationality_id,
            "address_province_id": address_province_id,
            "address_district_id": address_district_id,
            "address_ward_id": address_ward_id,
            "address": resident_address_number_and_street,
            "address_domestic_flag": True if nationality_id == ADDRESS_COUNTRY_CODE_VN else False
        }
        print('saving_customer_resident_address', saving_customer_resident_address)
        saving_customer_contact_address = {  # noqa
            "address_type_id": CONTACT_ADDRESS_CODE,
            "address_country_id": nationality_id,
            "address_province_id": contact_province_id,
            "address_district_id": contact_district_id,
            "address_ward_id": contact_ward_id,
            "address": contact_number_and_street,
            "address_domestic_flag": True,  # Địa chỉ liên lạc đối với CMND/CCCD là địa chỉ trong nước
        }
        # compare avatar
        if identity_type == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            saving_customer_identity_images = [
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": upload_front_side['uuid'],
                    "avatar_image_uuid": orc_data_front_side['passport_information']['identity_avatar_image_uuid'],
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": current_user.user_info.code,
                    "maker_at": now(),
                    "updater_id": current_user.user_info.code,
                    "updater_at": now(),
                    "identity_image_front_flag": None
                }
            ]
        else:
            saving_customer_identity_images = [
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": upload_front_side['uuid'],
                    "avatar_image_uuid": orc_data_front_side['front_side_information']['identity_avatar_image_uuid'],
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": current_user.user_info.code,
                    "maker_at": now(),
                    "updater_id": current_user.user_info.code,
                    "updater_at": now(),
                    "identity_image_front_flag": IDENTITY_IMAGE_FLAG_FRONT_SIDE
                },
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": upload_back_side['uuid'],
                    # lưu CMND, CCCD mặt sau k có avatar
                    "avatar_image_uuid": None,
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": current_user.user_info.code,
                    "maker_at": now(),
                    "updater_id": current_user.user_info.code,
                    "updater_at": now(),
                    "identity_image_front_flag": IDENTITY_IMAGE_FLAG_BACKSIDE
                }
            ]
        # upload avatar with ekyc = true
        avatar_image_name = avatar_image.filename
        avatar_image = await avatar_image.read()
        upload_avatar = self.call_repos(await repos_upload_file(
            file=avatar_image,
            name=avatar_image_name,
            ekyc_flag=EKYC_FLAG
        ))
        # compare avatar_image with identity_avatar_image_uuid từ orc front_side
        if identity_type != 'HO_CHIEU':
            is_success, compare_response = await service_ekyc.compare_face(
                face_uuid=upload_avatar['uuid_ekyc'],
                avatar_image_uuid=orc_data_front_side['front_side_information']['identity_avatar_image_uuid']
            )
            identity_avatar_image_uuid = orc_data_front_side['front_side_information']['identity_avatar_image_uuid']
            # Thêm avatar thành Hình ảnh định danh Khuôn mặt
            ################################################################################################################
            avatar_image_uuid_service = await CtrFile().upload_ekyc_file(
                uuid_ekyc=orc_data_front_side['front_side_information']['identity_avatar_image_uuid'])
        ################################################################################################################

        else:
            is_success, compare_response = await service_ekyc.compare_face(
                face_uuid=upload_avatar['uuid_ekyc'],
                avatar_image_uuid=orc_data_front_side['passport_information']['identity_avatar_image_uuid']
            )
            identity_avatar_image_uuid = orc_data_front_side['passport_information']['identity_avatar_image_uuid']

            avatar_image_uuid_service = await CtrFile().upload_ekyc_file(
                uuid_ekyc=orc_data_front_side['passport_information']['identity_avatar_image_uuid'])

        # lưu CustomerCompareImage
        if not is_success:
            return self.response_exception(msg='COMPARE_FACE_MOBILE')
        saving_customer_compare_image = {
            "id": upload_avatar['uuid_ekyc'],
            "compare_image_url": upload_avatar['uuid'],
            "similar_percent": compare_response['data']['similarity_percent'],  # gọi qua eKYC để check
            "maker_id": current_user.user_info.code,
            "maker_at": now()
        }
        ################################################################################################################
        # Tạo data TransactionDaily và các TransactionStage khác cho bước mở CIF
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            business_type_id=BUSINESS_TYPE_INIT_CIF
        )
        (saving_transaction_stage_status, saving_transaction_stage, saving_transaction_daily, saving_transaction_sender,
         saving_transaction_receiver) = transaction_datas

        history_datas = [dict(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_CIF,
            completed_at=datetime_to_string(now()),
            created_at=datetime_to_string(now()),
            status=PROFILE_HISTORY_STATUS_INIT,
            branch_id=current_user.user_info.hrm_branch_id,
            branch_code=current_user.user_info.hrm_branch_code,
            branch_name=current_user.user_info.hrm_branch_name,
            user_id=current_user.user_info.code,
            user_name=current_user.user_info.name,
            position_id=current_user.user_info.hrm_position_id,
            position_code=current_user.user_info.hrm_position_code,
            position_name=current_user.user_info.hrm_position_name
        )]
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
                identity_document_type_id=identity_type,
                customer_id=None,
                identity_id=None,
                saving_customer=saving_customer,
                saving_customer_identity=saving_customer_identity,
                saving_customer_individual_info=saving_customer_individual_info,
                saving_customer_resident_address=saving_customer_resident_address,
                saving_customer_contact_address=saving_customer_contact_address,
                saving_customer_compare_image=saving_customer_compare_image,
                saving_customer_identity_images=saving_customer_identity_images,
                saving_transaction_stage_status=saving_transaction_stage_status,
                saving_transaction_stage=saving_transaction_stage,
                saving_transaction_daily=saving_transaction_daily,
                saving_transaction_sender=saving_transaction_sender,
                saving_transaction_receiver=saving_transaction_receiver,
                avatar_image_uuid_service=avatar_image_uuid_service,
                identity_avatar_image_uuid_ekyc=identity_avatar_image_uuid,
                request_data={"mytest": "hmmm"},
                history_datas=history_datas,
                current_user=current_user.user_info,
                session=self.oracle_session
            )
        )
        return self.response(data=info_save_document)
