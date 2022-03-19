from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.face.repository import (
    repos_get_approval_compare_faces
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.file.repository import repos_upload_file
from app.api.v1.endpoints.file.validator import file_validator
from app.settings.event import service_ekyc
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC


class CtrApproveFace(BaseController):
    async def ctr_upload_face(
            self,
            cif_id: str,
            amount: int,  # Số lượng hình ảnh so sánh
            image_file: UploadFile
    ):
        # cif_id = request.image_file
        # amount = request.image_file  # Số lượng hình ảnh so sánh
        # image_file = request.image_file

        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # image_file_name = image_file.filename
        image_data = await image_file.read()

        # Validate File
        self.call_validator(await file_validator(image_data))

        # upload file vào service file -> lấy uuid_service_file, uuid_ekyc
        face_info = self.call_repos(await repos_upload_file(
            file=image_data,
            name=image_file.filename,
            ekyc_flag=True
        ))
        face_uuid_ekyc = face_info['uuid_ekyc']
        face_uuid = face_info['uuid']

        # Lấy 2 hình ảnh mới nhất ở bước GTDD
        face_transactions = self.call_repos(await repos_get_approval_compare_faces(
            cif_id=cif_id,
            session=self.oracle_session
        ))

        compare_face_images = {}
        compare_face_image_urls = []
        compare_face_image_uuids = []
        if amount != 2:
            amount = amount

        for index, (_, customer_compare_image_transaction) in enumerate(face_transactions, 1):
            # uuid của service file
            compare_face_images.update({
                customer_compare_image_transaction.compare_image_id: {
                    "uuid": customer_compare_image_transaction.compare_image_url,
                    "uuid_ekyc": customer_compare_image_transaction.compare_image_id
                }
            })
            compare_face_image_uuids.append(customer_compare_image_transaction.compare_image_url)

            # lấy link url của compare face
            compare_face_image_urls.append(customer_compare_image_transaction.compare_image_url)

            if index == amount:
                break

        total_face_images = []
        total_face_images.extend(compare_face_image_uuids)
        total_face_images.append(face_uuid)

        uuid__link_downloads = await self.get_link_download_multi_file(uuids=total_face_images)
        # so sánh ảnh được thêm vào với 2 ảnh khuôn mặt so sánh ở bước GTDD
        for index, (compare_face_uuid_ekyc, compare_face_image) in enumerate(compare_face_images.items()):
            is_success, compare_face_info = await service_ekyc.compare_face(face_uuid_ekyc, compare_face_uuid_ekyc)
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_EKYC,
                    detail=compare_face_info['message'],
                    loc=f"index {index}, face_uuid: {face_uuid_ekyc}, compare_face_image_uuid: {compare_face_uuid_ekyc}"
                )
            compare_face_image.update(dict(
                url=uuid__link_downloads[compare_face_image['uuid']],
                similar_percent=compare_face_info['data']['similarity_percent']
            ))

        face_url = uuid__link_downloads[face_uuid]

        return self.response(data={
            "cif_id": cif_id,
            "face_url": face_url,
            "compare_face_image_urls": [dict(
                url=uuid__link_downloads[compare_face_image['uuid']],
                similar_percent=compare_face_image['similar_percent']
            ) for (compare_face_uuid_ekyc, compare_face_image) in compare_face_images.items()],
        })
