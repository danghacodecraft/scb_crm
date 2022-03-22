from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.finger.repository import (
    repos_get_data_finger
)
from app.utils.constant.cif import HAND_SIDE_LEFT_CODE
from app.utils.functions import dropdown


class CtrFingers(BaseController):
    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))

        left_hand = []
        right_hand = []

        image_uuids = [row.CustomerIdentityImageTransaction.image_url for row in fingerprint_data]
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        for row in fingerprint_data:
            row.CustomerIdentityImageTransaction.image_url = uuid__link_downloads[row.CustomerIdentityImageTransaction.image_url]

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
