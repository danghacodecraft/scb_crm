from operator import itemgetter
from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.finger.repository import (
    repos_compare_finger_ekyc, repos_get_data_finger, repos_get_id_finger_ekyc,
    repos_save_compare_finger
)
from app.api.v1.endpoints.file.repository import repos_upload_file
from app.utils.constant.cif import ACTIVE_FLAG_DISACTIVED, HAND_SIDE_LEFT_CODE
from app.utils.functions import dropdown, generate_uuid, now


class CtrFingers(BaseController):
    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))

        left_hand = []
        right_hand = []

        image_uuids = [row.CustomerIdentityImageTransaction.image_url for row in fingerprint_data]
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        for row in fingerprint_data:
            row.CustomerIdentityImageTransaction.image_url = uuid__link_downloads[
                row.CustomerIdentityImageTransaction.image_url]

            fingerprint = {
                'image_id': row.CustomerIdentityImage.id,
                'make_at': row.CustomerIdentityImageTransaction.maker_at,
                'image_url': row.CustomerIdentityImageTransaction.image_url,
                'hand_side': dropdown(row.HandSide),
                'finger_type': dropdown(row.FingerType)
            }
            if row.HandSide.code == HAND_SIDE_LEFT_CODE:
                left_hand.append(fingerprint)
            else:
                right_hand.append(fingerprint)
        return self.response(data={
            'left_hand': left_hand,
            'right_hand': right_hand
        })

    async def ctr_compare_fingerprint(
        self,
        cif_id: str,
        finger_img,
        booking_id: Optional[str] = None
    ):
        current_user = self.current_user.user_info
        finger_id_ekycs = self.call_repos(await repos_get_id_finger_ekyc(cif_id=cif_id, session=self.oracle_session))

        data_finger_img = await finger_img.read()
        info_finger_img = self.call_repos(await repos_upload_file(
            file=data_finger_img,
            name=finger_img.filename,
            ekyc_flag=True,
            booking_id=booking_id
        ))

        id_fingers = []
        image_uuids = []

        for finger_print in finger_id_ekycs:
            id_fingers.append(finger_print.ekyc_id)
            image_uuids.append(finger_print.image_url)

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        compare_finger_response = self.call_repos(await repos_compare_finger_ekyc(
            cif_id=cif_id,
            uuid_ekyc=info_finger_img['uuid_ekyc'],
            id_fingers=id_fingers
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
                        "similarity_percent": item['accuracy'],
                        "uuid": info_finger_img['uuid']
                    }
                    compare_finger['image_url'] = uuid__link_downloads[compare_finger['image_url']]
                    data_compare_image = {
                        "id": generate_uuid(),
                        "identity_id": finger.identity_id,
                        "identity_image_id": finger.id,
                        "compare_image_url": info_finger_img['uuid'],
                        "similar_percent": item['accuracy'],
                        "maker_id": current_user.code,
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
