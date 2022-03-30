from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.face.repository import (
    repos_save_approval_compare_face
)
from app.api.v1.endpoints.approval.repository import repos_get_approval_identity_faces
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.file.repository import repos_upload_file
from app.api.v1.endpoints.file.validator import file_validator
from app.settings.event import service_ekyc
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC
from app.utils.functions import now


class CtrApproveFace(BaseController):
    async def ctr_upload_face(
            self,
            cif_id: str,
            amount: int,  # Số lượng hình ảnh so sánh
            image_file: UploadFile
    ):
        current_user = self.current_user
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        image_data = await image_file.read()

        # Validate File
        self.call_validator(await file_validator(image_data))

        # upload file vào service file -> lấy uuid_service_file, uuid_ekyc
        face_info = self.call_repos(await repos_upload_file(
            file=image_data,
            name=image_file.filename,
            ekyc_flag=True
        ))
        compare_face_uuid_ekyc = face_info['uuid_ekyc']
        compare_face_uuid = face_info['uuid']

        # Lấy tất cả hình ảnh mới nhất ở bước GTDD
        face_transactions = self.call_repos(await repos_get_approval_identity_faces(
            cif_id=cif_id,
            session=self.oracle_session
        ))

        first_customer_identity, first_customer_identity_image = face_transactions[0]
        identity_image_id = first_customer_identity_image.id
        customer_identity_id = first_customer_identity.id

        face_images = {}
        face_image_uuids = []
        if amount != 2:
            amount = amount

        for index, (customer_identity, customer_identity_image) in enumerate(face_transactions, 1):
            # uuid của service file
            # {
            #     uuid_ekyc: {
            #         "uuid": uuid/image_url
            #     }
            # }
            face_images.update({
                customer_identity_image.ekyc_uuid: {
                    "uuid": customer_identity_image.image_url
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
            is_success, compare_face_info = await service_ekyc.compare_face(compare_face_uuid_ekyc, face_uuid_ekyc)
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_EKYC,
                    detail=compare_face_info['message'],
                    loc=f"index {index}, face_uuid: {face_uuid_ekyc}, compare_face_image_uuid: {compare_face_uuid_ekyc}"
                )
            compare_face_image_url = uuid__link_downloads[compare_face_image['uuid']]
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
        # Lưu lại hình ảnh vào DB

        self.call_repos(await repos_save_approval_compare_face(
            saving_customer_compare_images=saving_customer_compare_images,
            saving_customer_compare_image_transactions=saving_customer_compare_image_transactions,
            session=self.oracle_session
        ))

        return self.response(data={
            "cif_id": cif_id,
            "compare_face_image_url": compare_face_image_url,
            "compare_face_image_uuid": compare_face_uuid,
            "created_at": now(),
            "face_image_urls": [dict(
                url=face_image["url"],
                similar_percent=face_image['similar_percent']
            ) for face_image_uuid, face_image in face_images.items()]
        })
