from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval_v2.fingerprint.repository import (
    repos_save_approval_compare_fingerprint
)
from app.api.v1.endpoints.approval_v2.fingerprint.schema import (
    ApprovalFingerprintRequest
)
from app.api.v1.endpoints.approval_v2.repository import (
    repos_get_approval_identity_images_by_image_type_id
)
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.settings.event import service_ekyc
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.cif import IMAGE_TYPE_FINGERPRINT
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC
from app.utils.functions import now


class CtrApproveFingerprint(BaseController):
    async def ctr_upload_fingerprint(
            self,
            request: ApprovalFingerprintRequest,
            booking_id: Optional[str]
    ):
        current_user = self.current_user.user_info
        # # check cif đang tạo
        # self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # Check exist Booking
        booking = await CtrBooking().ctr_get_initializing_booking(
            booking_id=booking_id
        )

        compare_fingerprint_uuid = request.compare_uuid
        compare_fingerprint_uuid_ekyc = request.compare_uuid_ekyc

        cif_id = None
        saving_booking_compare_images = []

        # Nếu là nghiệp vụ mở CIF
        saving_customer_compare_images = []
        saving_customer_compare_image_transactions = []
        fingerprint_images = {}
        if booking.business_type_id == BUSINESS_TYPE_INIT_CIF:
            customer = await CtrBooking(current_user=self.current_user).ctr_get_customer_from_booking(booking_id=booking_id)
            cif_id = customer.id
            (
                saving_customer_compare_images, saving_customer_compare_image_transactions, compare_fingerprint_image_url,
                fingerprint_images
            ) = await self.upload_fingerprint_open_cif(
                cif_id=cif_id, booking_id=booking_id, amount=request.amount,
                compare_fingerprint_uuid=compare_fingerprint_uuid,
                compare_fingerprint_uuid_ekyc=compare_fingerprint_uuid_ekyc, current_user=current_user
            )
            for index, saving_customer_compare_image_transaction in enumerate(saving_customer_compare_image_transactions):
                for uuid_ekyc, fingerprint_image in fingerprint_images.items():
                    saving_booking_compare_images.append(dict(
                        image_type_id=IMAGE_TYPE_FINGERPRINT,
                        image_uuid=fingerprint_image['uuid'],
                        image_ekyc_uuid=uuid_ekyc,
                        is_image_original=True,
                        compare_image_uuid=saving_customer_compare_image_transaction['compare_image_url'],
                        compare_image_ekyc_uuid=saving_customer_compare_image_transaction['compare_image_id'],
                        compare_percent=saving_customer_compare_image_transaction['similar_percent'],
                        booking_id=booking_id,
                        created_at=now(),
                    ))
        else:
            saving_booking_compare_images.append(dict(
                image_type_id=IMAGE_TYPE_FINGERPRINT,
                image_uuid=None,
                image_ekyc_uuid=None,
                is_image_original=False,
                compare_image_uuid=compare_fingerprint_uuid,
                compare_image_ekyc_uuid=compare_fingerprint_uuid_ekyc,
                compare_percent=None,
                booking_id=booking_id,
                created_at=now(),
            ))

        # Lưu lại hình ảnh vào DB
        self.call_repos(await repos_save_approval_compare_fingerprint(
            saving_customer_compare_images=saving_customer_compare_images,
            saving_customer_compare_image_transactions=saving_customer_compare_image_transactions,
            saving_booking_compare_images=saving_booking_compare_images,
            session=self.oracle_session
        ))

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=[compare_fingerprint_uuid])
        compare_fingerprint_url = uuid__link_downloads[compare_fingerprint_uuid]

        return self.response(data={
            "cif_id": cif_id,
            "compare_fingerprint_image_url": compare_fingerprint_url,
            "compare_fingerprint_image_uuid": compare_fingerprint_uuid,
            "created_at": now(),
            "fingerprint_image_urls": [dict(
                url=fingerprint_image["url"],
                similar_percent=fingerprint_image['similar_percent']
            ) for fingerprint_image_uuid, fingerprint_image in fingerprint_images.items()]
        })

    async def upload_fingerprint_open_cif(
            self,
            cif_id: str,
            booking_id: str,
            amount: int,
            compare_fingerprint_uuid: str,
            compare_fingerprint_uuid_ekyc: str,
            current_user: UserInfoResponse
    ):
        """
        Upload fingerprint cho trường hợp mở cif
        """
        # Lấy tất cả hình ảnh mới nhất ở bước GTDD
        fingerprint_transactions = self.call_repos(await repos_get_approval_identity_images_by_image_type_id(
            image_type_id=IMAGE_TYPE_FINGERPRINT,
            identity_type="FINGERPRINT",
            booking_id=booking_id,
            session=self.oracle_session
        ))

        first_customer_identity, first_customer_identity_image, _, _ = fingerprint_transactions[0]
        customer_identity_id = first_customer_identity.id

        fingerprint_images = {}
        fingerprint_image_uuids = []
        if amount != 2:
            amount = amount

        ids_finger = []
        for index, (customer_identity, customer_identity_image, _, _) in enumerate(fingerprint_transactions, 1):
            # uuid của service file
            # {
            #     uuid_ekyc: {
            #         "uuid": uuid/image_url
            #         "identity_image_id": id
            #     }
            # }
            fingerprint_images.update({
                customer_identity_image.ekyc_uuid: {
                    "uuid": customer_identity_image.image_url,
                    "identity_image_id": customer_identity_image.id
                }
            })
            fingerprint_image_uuids.append(customer_identity_image.image_url)

            ids_finger.append(customer_identity_image.ekyc_id)

            if index == amount:
                break

        total_fingerprint_images = []
        total_fingerprint_images.extend(fingerprint_image_uuids)
        total_fingerprint_images.append(compare_fingerprint_uuid)

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=total_fingerprint_images)

        saving_customer_compare_images = []
        saving_customer_compare_image_transactions = []
        # so sánh ảnh được thêm vào với 2 ảnh chữ ký so sánh ở bước GTDD
        for index, (fingerprint_uuid_ekyc, compare_fingerprint_image) in enumerate(fingerprint_images.items()):
            compare_fingerprint_image_uuid = compare_fingerprint_image['uuid']
            identity_image_id = compare_fingerprint_image['identity_image_id']
            is_success, compare_fingerprint_info = await service_ekyc.compare_finger_ekyc(
                json_body=dict(
                    uuid=compare_fingerprint_uuid_ekyc,
                    id_fingers=ids_finger,
                    limit=len(ids_finger)
                )
            )
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_EKYC,
                    detail=compare_fingerprint_info['message'],
                    loc=f"index {index}, fingerprint_uuid: {fingerprint_uuid_ekyc}, compare_fingerprint_image_uuid: {compare_fingerprint_uuid_ekyc}"
                )

            for customer in compare_fingerprint_info['customers']:
                similar_percent = customer['accuracy']

                compare_fingerprint_image_url = uuid__link_downloads[compare_fingerprint_image_uuid]
                compare_fingerprint_image.update(dict(
                    url=compare_fingerprint_image_url,
                    similar_percent=similar_percent
                ))

                # Lưu các chữ ký được so sánh
                saving_customer_compare_images.append(dict(
                    id=compare_fingerprint_uuid_ekyc,
                    identity_id=customer_identity_id,
                    identity_image_id=identity_image_id,
                    compare_image_url=compare_fingerprint_uuid,
                    similar_percent=similar_percent,
                    maker_id=current_user.code,
                    maker_at=now()
                ))
                saving_customer_compare_image_transactions.append(dict(
                    compare_image_id=compare_fingerprint_uuid_ekyc,
                    compare_image_url=compare_fingerprint_uuid,
                    identity_image_id=identity_image_id,
                    similar_percent=similar_percent,
                    maker_id=current_user.code,
                    is_approved=True,
                    maker_at=now()
                ))

        compare_fingerprint_image_url = uuid__link_downloads[compare_fingerprint_uuid]

        return (
            saving_customer_compare_images, saving_customer_compare_image_transactions, compare_fingerprint_image_url,
            fingerprint_images
        )
