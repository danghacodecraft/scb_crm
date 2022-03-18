from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.face.repository import (
    repos_get_approval_compare_faces
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.file.validator import file_validator
from app.settings.event import service_ekyc
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC


class CtrApproveFace(BaseController):
    async def ctr_upload_face(
            self,
            cif_id: str,
            image_file: UploadFile
    ):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # image_file_name = image_file.filename
        image_data = await image_file.read()

        # Validate File
        self.call_validator(await file_validator(image_data))

        # lấy uuid_ekyc
        is_success_add_face, add_face_info = await service_ekyc.add_face(file=image_data)
        if not is_success_add_face:
            return self.response_exception(msg=ERROR_CALL_SERVICE_EKYC, detail=add_face_info.get('message', ''))
        face_uuid = add_face_info.get('data').get('uuid')

        # Lấy 2 hình ảnh mới nhất ở bước GTDD

        face_transactions = self.call_repos(await repos_get_approval_compare_faces(session=self.oracle_session))

        compare_face_images = []
        number_of_compare_face_image = 2

        for index, (
                customer, customer_identity, customer_identity_image, customer_compare_image,
                customer_compare_image_transaction
        ) in enumerate(face_transactions):
            compare_face_images.append(customer_compare_image_transaction.compare_image_id)
            if index == number_of_compare_face_image:
                break
        total_face_images = []
        total_face_images.extend(total_face_images)
        total_face_images.append(face_uuid)

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=total_face_images)

        compare_face_image_urls = []
        # so sánh ảnh được thêm vào với 2 ảnh khuôn mặt so sánh ở bước GTDD
        for index, compare_face_image in enumerate(compare_face_images):
            compare_face_image_urls.append(uuid__link_downloads[compare_face_image])
            is_success, compare_face_info = await service_ekyc.compare_face(face_uuid, compare_face_image)
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_EKYC,
                    detail=compare_face_info['message'],
                    loc=f"index {index}, face_uuid: {face_uuid}, compare_face_image: {compare_face_image}"
                )

        face_url = uuid__link_downloads[face_uuid]

        return self.response(data={
            "cif_id": cif_id,
            "face_url": face_url,
            "compare_face_image_urls": compare_face_image_urls,
        })
