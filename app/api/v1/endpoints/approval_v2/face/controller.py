from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval_v2.face.repository import (
    repos_save_approval_compare_face
)
from app.api.v1.endpoints.approval_v2.face.schema import ApprovalFaceRequest
from app.api.v1.endpoints.approval_v2.repository import (
    repos_get_approval_identity_images_by_image_type_id
)
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.settings.event import service_ekyc
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.cif import IMAGE_TYPE_FACE
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC
from app.utils.functions import now


class CtrApproveFace(BaseController):
    async def ctr_upload_face(
            self,
            request: ApprovalFaceRequest,
            booking_id: Optional[str]
    ):
        current_user = self.current_user.user_info
        # # check cif đang tạo
        # self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # Check exist Booking
        booking = await CtrBooking().ctr_get_initializing_booking(
            booking_id=booking_id
        )

        compare_face_uuid = request.compare_uuid
        compare_face_uuid_ekyc = request.compare_uuid_ekyc

        cif_id = None
        saving_booking_compare_images = []

        # Nếu là nghiệp vụ mở CIF
        saving_customer_compare_images = []
        saving_customer_compare_image_transactions = []
        face_images = {}
        if booking.business_type_id == BUSINESS_TYPE_INIT_CIF:
            (
                saving_customer_compare_images, saving_customer_compare_image_transactions, compare_face_image_url,
                face_images
            ) = await self.upload_face_open_cif(
                booking_id=booking_id, amount=request.amount, compare_face_uuid=compare_face_uuid,
                compare_face_uuid_ekyc=compare_face_uuid_ekyc, current_user=current_user
            )
            # Lấy tất cả hình ảnh mới nhất ở bước GTDD
            face_transactions = self.call_repos(await repos_get_approval_identity_images_by_image_type_id(
                image_type_id=IMAGE_TYPE_FACE,
                identity_type="FACE",
                booking_id=booking_id,
                session=self.oracle_session
            ))
            for index, saving_customer_compare_image_transaction in enumerate(saving_customer_compare_image_transactions):
                for customer_identity, customer_identity_image, _, _ in face_transactions:
                    saving_booking_compare_images.append(dict(
                        image_type_id=IMAGE_TYPE_FACE,
                        image_uuid=customer_identity_image.id,
                        image_ekyc_uuid=customer_identity_image.ekyc_uuid,
                        is_image_original=True,
                        compare_image_uuid=saving_customer_compare_image_transaction['compare_image_url'],
                        compare_image_ekyc_uuid=saving_customer_compare_image_transaction['compare_image_id'],
                        compare_percent=saving_customer_compare_image_transaction['similar_percent'],
                        booking_id=booking_id,
                        created_at=now(),
                    ))
        else:
            saving_booking_compare_images.append(dict(
                image_type_id=IMAGE_TYPE_FACE,
                image_uuid=None,
                image_ekyc_uuid=None,
                is_image_original=False,
                compare_image_uuid=compare_face_uuid_ekyc,
                compare_image_ekyc_uuid=compare_face_uuid_ekyc,
                compare_percent=None,
                booking_id=booking_id,
                created_at=now(),
            ))

        # Lưu lại hình ảnh vào DB
        self.call_repos(await repos_save_approval_compare_face(
            saving_customer_compare_images=saving_customer_compare_images,
            saving_customer_compare_image_transactions=saving_customer_compare_image_transactions,
            saving_booking_compare_images=saving_booking_compare_images,
            session=self.oracle_session
        ))

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=[compare_face_uuid])
        compare_face_url = uuid__link_downloads[compare_face_uuid]

        return self.response(data={
            "cif_id": cif_id,
            "compare_face_image_url": compare_face_url,
            "compare_face_image_uuid": compare_face_uuid,
            "created_at": now(),
            "face_image_urls": [dict(
                url=face_image["url"],
                similar_percent=face_image['similar_percent']
            ) for face_image_uuid, face_image in face_images.items()]
        })

    async def upload_face_open_cif(
            self,
            booking_id: str,
            amount: int,
            compare_face_uuid: str,
            compare_face_uuid_ekyc: str,
            current_user: UserInfoResponse
    ):
        """
        Upload face cho trường hợp mở cif
        """
        # Lấy tất cả hình ảnh mới nhất ở bước GTDD
        face_transactions = self.call_repos(await repos_get_approval_identity_images_by_image_type_id(
            image_type_id=IMAGE_TYPE_FACE,
            identity_type="FACE",
            booking_id=booking_id,
            session=self.oracle_session
        ))

        first_customer_identity, first_customer_identity_image, _, _ = face_transactions[0]
        customer_identity_id = first_customer_identity.id

        face_images = {}
        face_image_uuids = []
        if amount != 2:
            amount = amount

        for index, (customer_identity, customer_identity_image, _, _) in enumerate(face_transactions, 1):
            # uuid của service file
            # {
            #     uuid_ekyc: {
            #         "uuid": uuid/image_url
            #         "identity_image_id": id
            #     }
            # }
            face_images.update({
                customer_identity_image.ekyc_uuid: {
                    "uuid": customer_identity_image.image_url,
                    "identity_image_id": customer_identity_image.id
                }
            })
            face_image_uuids.append(customer_identity_image.image_url)

            if index == amount:
                break

        total_face_images = []
        total_face_images.extend(face_image_uuids)
        total_face_images.append(compare_face_uuid)

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=total_face_images)

        saving_customer_compare_images = []
        saving_customer_compare_image_transactions = []
        # so sánh ảnh được thêm vào với 2 ảnh khuôn mặt so sánh ở bước GTDD
        for index, (face_uuid_ekyc, compare_face_image) in enumerate(face_images.items()):
            compare_face_image_uuid = compare_face_image['uuid']
            identity_image_id = compare_face_image['identity_image_id']
            is_success, compare_face_info = await service_ekyc.compare_face(
                face_uuid=compare_face_uuid_ekyc,
                avatar_image_uuid=face_uuid_ekyc,
                # booking_id=booking_id
            )
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_EKYC,
                    detail=compare_face_info['message'],
                    loc=f"index {index}, face_uuid: {face_uuid_ekyc}, compare_face_image_uuid: {compare_face_uuid_ekyc}"
                )
            compare_face_image_url = uuid__link_downloads[compare_face_image_uuid]
            similar_percent = compare_face_info['data']['similarity_percent']
            compare_face_image.update(dict(
                url=compare_face_image_url,
                similar_percent=similar_percent
            ))

            # Lưu các khuôn mặt được so sánh
            saving_customer_compare_images.append(dict(
                id=compare_face_uuid_ekyc,
                identity_id=customer_identity_id,
                identity_image_id=identity_image_id,
                compare_image_url=compare_face_uuid,
                similar_percent=similar_percent,
                maker_id=current_user.code,
                maker_at=now()
            ))
            saving_customer_compare_image_transactions.append(dict(
                compare_image_id=compare_face_uuid_ekyc,
                compare_image_url=compare_face_uuid,
                identity_image_id=identity_image_id,
                similar_percent=similar_percent,
                maker_id=current_user.code,
                is_approved=True,
                maker_at=now()
            ))

        compare_face_image_url = uuid__link_downloads[compare_face_uuid]

        return (
            saving_customer_compare_images, saving_customer_compare_image_transactions, compare_face_image_url,
            face_images
        )
