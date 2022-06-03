from typing import List, Optional

from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_get_data_finger, repos_get_identity_image, repos_save_fingerprint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    TwoFingerPrintRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking, repos_get_customer_identity,
    repos_get_initializing_customer
)
from app.api.v1.others.booking.controller import CtrBooking
from app.settings.event import service_ekyc, service_file
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.cif import (
    ACTIVE_FLAG_ACTIVED, ACTIVE_FLAG_CREATE_FINGERPRINT,
    ACTIVE_FLAG_DISACTIVED, FRONT_FLAG_CREATE_FINGERPRINT, HAND_SIDE_LEFT_CODE,
    IMAGE_TYPE_FINGERPRINT
)
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC
from app.utils.functions import dropdown, generate_uuid, now, parse_file_uuid


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, cif_id: str, finger_request: TwoFingerPrintRequest):
        current_user = self.current_user.user_info
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        is_create = True

        fingerprints = []
        fingerprints.extend(finger_request.fingerprint_1)
        fingerprints.extend(finger_request.fingerprint_2)

        # các uuid cần phải gọi qua service file để check
        image_uuids = []
        save_identity_image = []
        save_identity_image_transaction = []

        identity = self.call_repos(await repos_get_customer_identity(cif_id=cif_id, session=self.oracle_session))
        # lấy danh sách chữ ký theo identity
        identity_image = self.call_repos(await repos_get_identity_image(
            identity_id=identity.id,
            session=self.oracle_session
        ))
        # update active_flag tại identity_image
        update_identity_image = []
        if identity_image:
            is_create = False
            for item in identity_image:
                item.active_flag = 0
                update_identity_image.append({
                    "id": item.id,
                    'identity_id': item.identity_id,
                    'image_type_id': item.image_type_id,
                    'image_url': item.image_url,
                    'hand_side_id': item.hand_side_id,
                    'finger_type_id': item.finger_type_id,
                    'vector_data': None,
                    'active_flag': ACTIVE_FLAG_DISACTIVED,
                    'maker_id': item.maker_id,
                    'maker_at': now(),
                    'identity_image_front_flag': item.identity_image_front_flag,
                    "ekyc_uuid": item.ekyc_uuid,
                    "ekyc_id": item.ekyc_id
                })
        # tạo dữ liệu gửi lên từ request
        id_ekycs = []
        for fingerprint in fingerprints:
            identity_image_id = generate_uuid()
            uuid = parse_file_uuid(fingerprint.image_url)

            fingerprint.image_url = uuid
            image_uuids.append(uuid)
            # check id_ekyc k được trùng
            if fingerprint.id_ekyc in id_ekycs:
                return self.response_exception(msg='ID_EKYC is not exist')
            id_ekycs.append(fingerprint.id_ekyc)

            save_identity_image.append({
                "id": identity_image_id,
                'identity_id': identity.id,
                'image_type_id': IMAGE_TYPE_FINGERPRINT,
                'image_url': fingerprint.image_url,
                'hand_side_id': fingerprint.hand_side.id,
                'finger_type_id': fingerprint.finger_type.id,
                'vector_data': None,
                'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
                'maker_id': current_user.code,
                'maker_at': now(),
                'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT,
                "ekyc_uuid": fingerprint.uuid_ekyc,
                "ekyc_id": fingerprint.id_ekyc
            })

            save_identity_image_transaction.append({
                "identity_image_id": identity_image_id,
                "image_url": fingerprint.image_url,
                "active_flag": ACTIVE_FLAG_ACTIVED,
                'maker_id': current_user.code,
                "maker_at": now()
            })

        # gọi qua service file để check exist list uuid
        await self.check_exist_multi_file(uuids=image_uuids)

        hand_side_ids = []
        finger_type_ids = []

        for item in fingerprints:
            hand_side_ids.append(item.hand_side.id)
            finger_type_ids.append(item.finger_type.id)

        # check exits hand_side_ids, finger_type_ids
        await self.get_model_objects_by_ids(model_ids=hand_side_ids, model=HandSide, loc='hand_side -> id')
        await self.get_model_objects_by_ids(model_ids=finger_type_ids, model=FingerType, loc='finger_type -> id')

        data = self.call_repos(
            await repos_save_fingerprint(
                cif_id=cif_id,
                is_create=is_create,
                log_data=finger_request.json(),
                session=self.oracle_session,
                save_identity_image=save_identity_image,
                save_identity_image_transaction=save_identity_image_transaction,
                update_identity_image=update_identity_image,
                created_by=current_user.username
            )
        )

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        data.update(booking=dict(
            id=booking.id,
            code=booking.code
        ))

        return self.response(data=data)

    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))

        fingerprint_1 = []
        fingerprint_2 = []

        image_uuids = [row.CustomerIdentityImageTransaction.image_url for row in fingerprint_data]
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        for row in fingerprint_data:
            row.CustomerIdentityImageTransaction.image_url = uuid__link_downloads[
                row.CustomerIdentityImageTransaction.image_url]

            fingerprint = {
                'image_url': row.CustomerIdentityImageTransaction.image_url,
                'hand_side': dropdown(row.HandSide),
                'finger_type': dropdown(row.FingerType),
                'id_ekyc': row.CustomerIdentityImage.ekyc_id,
                'uuid_ekyc': row.CustomerIdentityImage.ekyc_uuid,
                'maker_at': row.CustomerIdentityImageTransaction.maker_at
            }
            if row.HandSide.code == HAND_SIDE_LEFT_CODE:
                fingerprint_1.append(fingerprint)
            else:
                fingerprint_2.append(fingerprint)
        return self.response(data={
            'fingerprint_1': fingerprint_1,
            'fingerprint_2': fingerprint_2
        })

    async def ctr_add_fingerprint(
            self,
            cif_id: str,
            file: UploadFile,
            ids_finger: List,
            booking_id: Optional[str]
    ):

        # Check exist Booking
        await CtrBooking().ctr_get_booking(
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            booking_id=booking_id,
            cif_id=cif_id,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        response_data = {}

        file_upload = await file.read()
        # upload service file
        is_success, response = await service_file.upload_file(file=file_upload, name=file.filename)

        # upload file ekyc
        is_success, uuid_ekyc = await service_ekyc.upload_file(
            file=file_upload,
            name=file.filename,
            booking_id=booking_id
        )

        # body add finger call ekyc
        json_body_add_finger = {
            "uuid": uuid_ekyc['uuid']
        }

        is_success_add_finger, id_finger = await service_ekyc.add_finger_ekyc(
            booking_id=booking_id,
            json_body=json_body_add_finger
        )
        if not is_success_add_finger:
            return self.response_exception(msg=ERROR_CALL_SERVICE_EKYC, loc="ADD_FINGERPRINT", detail=str(id_finger))

        response_data.update({
            "image_url": response['file_url'],
            "uuid_ekyc": uuid_ekyc['uuid'],
            "id_ekyc": id_finger['id']
        })

        if ids_finger:
            json_compare = {
                "uuid": uuid_ekyc['uuid'],
                "id_fingers": ids_finger,
                "limit": len(ids_finger)
            }

            is_success_compare, compare = await service_ekyc.compare_finger_ekyc(
                booking_id=booking_id,
                json_body=json_compare
            )

            if not is_success_compare:
                return self.response_exception(msg=ERROR_CALL_SERVICE_EKYC, loc="ADD_FINGERPRINT", detail=str(compare))

            response_data.update({
                "compare": compare['customers']
            })

        return self.response(data=response_data)
