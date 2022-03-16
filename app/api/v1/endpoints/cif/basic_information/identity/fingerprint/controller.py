from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_add_finger_ekyc, repos_compare_finger_ekyc, repos_get_data_finger,
    repos_save_fingerprint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    CompareFingerPrintRequest, TwoFingerPrintRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_customer_identity, repos_get_initializing_customer
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_FINGERPRINT, FRONT_FLAG_CREATE_FINGERPRINT,
    HAND_SIDE_LEFT_CODE, IMAGE_TYPE_FINGERPRINT
)
from app.utils.functions import dropdown, now, parse_file_uuid


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, cif_id: str, finger_request: TwoFingerPrintRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        fingerprints = []
        fingerprints.extend(finger_request.fingerprint_1)
        fingerprints.extend(finger_request.fingerprint_2)

        # các uuid cần phải gọi qua service file để check
        image_uuids = []
        list_data_insert = []

        identity = self.call_repos(await repos_get_customer_identity(cif_id=cif_id, session=self.oracle_session))

        for fingerprint in fingerprints:
            uuid = parse_file_uuid(fingerprint.image_url)
            fingerprint.image_url = uuid
            image_uuids.append(uuid)
            id_ekyc = self.call_repos(await repos_add_finger_ekyc(cif_id=cif_id, uuid=fingerprint.uuid_ekyc))

            list_data_insert.append({
                'identity_id': identity.id,
                'image_type_id': IMAGE_TYPE_FINGERPRINT,
                'image_url': fingerprint.image_url,
                'hand_side_id': fingerprint.hand_side.id,
                'finger_type_id': fingerprint.finger_type.id,
                'vector_data': None,
                'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
                'maker_id': self.current_user.user_id,
                'maker_at': now(),
                'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT,
                "ekyc_uuid": fingerprint.uuid_ekyc,
                "ekyc_id": id_ekyc
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

        # list_data_insert = [{
        #     'identity_id': identity.id,
        #     'image_type_id': IMAGE_TYPE_FINGERPRINT,
        #     'image_url': item.image_url,
        #     'hand_side_id': item.hand_side.id,
        #     'finger_type_id': item.finger_type.id,
        #     'vector_data': None,
        #     'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
        #     'maker_id': self.current_user.user_id,
        #     'maker_at': now(),
        #     'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT
        # } for item in fingerprints]

        data = self.call_repos(
            await repos_save_fingerprint(
                cif_id=cif_id,
                identity_id=identity.id,
                log_data=finger_request.json(),
                session=self.oracle_session,
                list_data_insert=list_data_insert,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=data)

    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))

        fingerprint_1 = []
        fingerprint_2 = []

        image_uuids = [finger.image_url for finger, _, _ in fingerprint_data]
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        for customer_identity_image, hand_side, finger_print in fingerprint_data:
            customer_identity_image.image_url = uuid__link_downloads[customer_identity_image.image_url]

            fingerprint = {
                'image_url': customer_identity_image.image_url,
                'hand_side': dropdown(hand_side),
                'finger_type': dropdown(finger_print)
            }
            if hand_side.code == HAND_SIDE_LEFT_CODE:
                fingerprint_1.append(fingerprint)
            else:
                fingerprint_2.append(fingerprint)
        return self.response(data={
            'fingerprint_1': fingerprint_1,
            'fingerprint_2': fingerprint_2
        })

    async def ctr_compare_fingerprint(self, cif_id: str, uuid: CompareFingerPrintRequest):

        compare_finger_response = self.call_repos(await repos_compare_finger_ekyc(
            cif_id=cif_id,
            uuid=uuid,
            session=self.oracle_session
        ))

        return self.response(data=compare_finger_response)
