from operator import itemgetter

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_add_finger_ekyc, repos_compare_finger_ekyc, repos_get_data_finger,
    repos_get_id_finger_ekyc, repos_save_compare_finger, repos_save_fingerprint
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
    ACTIVE_FLAG_ACTIVED, ACTIVE_FLAG_CREATE_FINGERPRINT,
    ACTIVE_FLAG_DISACTIVED, FRONT_FLAG_CREATE_FINGERPRINT, HAND_SIDE_LEFT_CODE,
    IMAGE_TYPE_FINGERPRINT
)
from app.utils.functions import dropdown, generate_uuid, now, parse_file_uuid


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, cif_id: str, finger_request: TwoFingerPrintRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        fingerprints = []
        fingerprints.extend(finger_request.fingerprint_1)
        fingerprints.extend(finger_request.fingerprint_2)

        # các uuid cần phải gọi qua service file để check
        image_uuids = []
        save_identity_image = []
        save_identity_image_transaction = []

        identity = self.call_repos(await repos_get_customer_identity(cif_id=cif_id, session=self.oracle_session))

        for fingerprint in fingerprints:
            identity_image_id = generate_uuid()
            uuid = parse_file_uuid(fingerprint.image_url)

            fingerprint.image_url = uuid
            image_uuids.append(uuid)

            id_ekyc = self.call_repos(await repos_add_finger_ekyc(cif_id=cif_id, uuid=fingerprint.uuid_ekyc))

            save_identity_image.append({
                "id": identity_image_id,
                'identity_id': identity.id,
                'image_type_id': IMAGE_TYPE_FINGERPRINT,
                'image_url': fingerprint.image_url,
                'hand_side_id': fingerprint.hand_side.id,
                'finger_type_id': fingerprint.finger_type.id,
                'vector_data': None,
                'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
                'maker_id': self.current_user.code,
                'maker_at': now(),
                'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT,
                "ekyc_uuid": fingerprint.uuid_ekyc,
                "ekyc_id": id_ekyc
            })

            save_identity_image_transaction.append({
                "identity_image_id": identity_image_id,
                "image_url": fingerprint.image_url,
                "active_flag": ACTIVE_FLAG_ACTIVED,
                'maker_id': self.current_user.code,
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
                identity_id=identity.id,
                log_data=finger_request.json(),
                session=self.oracle_session,
                save_identity_image=save_identity_image,
                save_identity_image_transaction=save_identity_image_transaction,
                created_by=self.current_user.username
            )
        )
        return self.response(data=data)

    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))

        fingerprint_1 = []
        fingerprint_2 = []

        image_uuids = [row.CustomerIdentityImageTransaction.image_url for row in fingerprint_data]
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        for row in fingerprint_data:
            row.CustomerIdentityImageTransaction.image_url = uuid__link_downloads[row.CustomerIdentityImageTransaction.image_url]

            fingerprint = {
                'image_url': row.CustomerIdentityImageTransaction.image_url,
                'hand_side': dropdown(row.HandSide),
                'finger_type': dropdown(row.FingerType)
            }
            if row.HandSide.code == HAND_SIDE_LEFT_CODE:
                fingerprint_1.append(fingerprint)
            else:
                fingerprint_2.append(fingerprint)
        return self.response(data={
            'fingerprint_1': fingerprint_1,
            'fingerprint_2': fingerprint_2
        })

    async def ctr_compare_fingerprint(self, cif_id: str, uuid: CompareFingerPrintRequest):
        finger_id_ekycs = self.call_repos(await repos_get_id_finger_ekyc(cif_id=cif_id, session=self.oracle_session))

        id_fingers = []
        image_uuids = []

        for finger_print in finger_id_ekycs:
            id_fingers.append(finger_print.ekyc_id)
            image_uuids.append(finger_print.image_url)

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        compare_finger_response = self.call_repos(await repos_compare_finger_ekyc(
            cif_id=cif_id,
            uuid=uuid,
            id_fingers=id_fingers,
            session=self.oracle_session
        ))

        response_data = []
        data_compare = []
        data_compare_trans = []
        for item in compare_finger_response['customers']:
            for finger in finger_id_ekycs:
                if item['id'] == finger.ekyc_id:
                    compare_finger = {
                        "id": item['id'],
                        "image_url": finger.image_url,
                        "similarity_percent": item['accuracy']
                    }
                    compare_finger['image_url'] = uuid__link_downloads[compare_finger['image_url']]
                    data_compare_image = {
                        "id": generate_uuid(),
                        "identity_id": finger.identity_id,
                        "identity_image_id": finger.id,
                        "compare_image_url": finger.image_url,
                        "similar_percent": item['accuracy'],
                        "maker_id": self.current_user.code,
                        "maker_at": now()
                    }
                    data_compare.append(data_compare_image)
                    data_compare_image_trans = {
                        "compare_image_id": data_compare_image['id'],
                        "identity_image_id": data_compare_image['identity_image_id'],
                        "is_identity_compare": ACTIVE_FLAG_DISACTIVED,
                        "compare_image_url": data_compare_image['compare_image_url'],
                        "similar_percent": data_compare_image['similar_percent'],
                        "maker_id": data_compare_image['maker_id'],
                        "maker_at": data_compare_image['maker_at']
                    }
                    data_compare_trans.append(data_compare_image_trans)
                    response_data.append(compare_finger)
        self.call_repos(await repos_save_compare_finger(
            compare_images=data_compare,
            compare_image_transactions=data_compare_trans,
            session=self.oracle_session
        ))
        return self.response(data=sorted(response_data, key=itemgetter('similarity_percent'), reverse=True))
