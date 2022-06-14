from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.signature.repository import (
    repos_compare_signature, repos_get_signature_data, repos_save_signature
)
from app.api.v1.endpoints.approval.signature.schema import SignaturesRequest
from app.api.v1.endpoints.cif.repository import (
    repos_get_customer_identity, repos_get_initializing_customer
)
from app.api.v1.endpoints.file.repository import repos_upload_file
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_SIGNATURE, IMAGE_TYPE_SIGNATURE
)
from app.utils.functions import (
    datetime_to_date, generate_uuid, now, parse_file_uuid
)


class CtrSignature(BaseController):
    async def ctr_save_signature(self, cif_id: str, signatures: SignaturesRequest):
        current_user = self.current_user.user_info
        # check len signature request
        if len(signatures.signatures) != 2:
            return self.response_exception(
                msg='signature must be equal 2',
                loc='ERROR_SAVE_SIGNATURE',
                detail='Can not save signature'
            )
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        # lấy các uuid cần check
        image_uuids = []
        for signature in signatures.signatures:
            uuid = parse_file_uuid(signature.image_url)
            signature.image_url = uuid
            image_uuids.append(uuid)

        # gọi qua service file để check exist list uuid
        await self.check_exist_multi_file(uuids=image_uuids)

        identity = self.call_repos(await repos_get_customer_identity(cif_id=cif_id, session=self.oracle_session))
        save_identity_image = []
        save_identity_image_transaction = []
        for signature in signatures.signatures:
            identity_image_id = generate_uuid()

            save_identity_image.append({
                'id': identity_image_id,
                'identity_id': identity.id,
                'image_type_id': IMAGE_TYPE_SIGNATURE,
                'image_url': signature.image_url,
                'hand_side_id': None,
                'finger_type_id': None,
                'vector_data': None,
                'active_flag': ACTIVE_FLAG_CREATE_SIGNATURE,
                'maker_id': current_user.code,
                'maker_at': now(),
                'identity_image_front_flag': None,
                'ekyc_uuid': signature.uuid_ekyc,
                'ekyc_id': None
            })

            save_identity_image_transaction.append({
                "identity_image_id": identity_image_id,
                "image_url": signature.image_url,
                "active_flag": ACTIVE_FLAG_CREATE_SIGNATURE,
                'maker_id': current_user.code,
                "maker_at": now()
            })

        data = self.call_repos(
            await repos_save_signature(
                cif_id=cif_id,
                save_identity_image=save_identity_image,
                save_identity_image_transaction=save_identity_image_transaction,
                log_data=signatures.json(),
                session=self.oracle_session,
                created_by=current_user.username
            )
        )

        return self.response(data=data)

    async def ctr_get_signature(self, cif_id: str):
        signature_data = self.call_repos(await repos_get_signature_data(cif_id=cif_id, session=self.oracle_session))

        image_uuids = [signature.image_url for signature in signature_data]

        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        date__signatures = {}
        for customer_identity_image in signature_data:
            signature = {
                'identity_image_id': customer_identity_image.id,
                'image_url': customer_identity_image.image_url,
                'active_flag': customer_identity_image.active_flag
            }
            date_str = datetime_to_date(customer_identity_image.maker_at)

            if date_str not in date__signatures:
                date__signatures[date_str] = []
            # gán lại image_url từ uuid query trong db thành link download
            signature['image_url'] = uuid__link_downloads[signature['image_url']]
            date__signatures[date_str].append(signature)

        return self.response(data=[{
            'created_date': data_str,
            'signature': signature
        } for data_str, signature in date__signatures.items()])

    async def ctr_compare_signature(self, cif_id: str, signature_img, booking_id: Optional[str]):

        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            booking_id=booking_id,
            cif_id=cif_id,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        current_user = self.current_user.user_info
        data_signature_img = await signature_img.read()

        is_success, info_signature_img = self.call_repos(await repos_upload_file(
            file=data_signature_img,
            name=signature_img.filename,
            ekyc_flag=True))

        compare_signatures = self.call_repos(await repos_compare_signature(
            cif_id=cif_id,
            uuid_ekyc=info_signature_img['uuid_ekyc'],
            uuid=info_signature_img['uuid'],
            session=self.oracle_session,
            user_id=current_user.code,
            booking_id=booking_id
        ))

        image_uuids = [signature['image_url'] for signature in compare_signatures]
        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)
        date__signatures = []

        for signature in compare_signatures:
            compare_signature = {
                "image_url": signature['image_url'],
                "similarity_percent": signature['similarity_percent'],
                "uuid": info_signature_img['uuid']
            }
            compare_signature['image_url'] = uuid__link_downloads[compare_signature['image_url']]
            date__signatures.append(compare_signature)

        return self.response(data=date__signatures)
