from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.document_file.repository import (
    repo_add_document_file, repos_upload_file
)
from app.api.v1.endpoints.file.validator import file_validator
from app.third_parties.oracle.models.cif.form.model import Booking
from app.utils.constant.utils import DOCUMENT_FILE_FOLDR, DOCUMENT_FILE_TYPE
from app.utils.functions import generate_uuid


class CtrDocumentFile(BaseController):
    async def ctr_document_file(self, file_upload: UploadFile, ekyc_flag: bool, booking_id):
        # Validate: check tồn tại booking_id
        await self.get_model_object_by_id(model_id=booking_id, model=Booking, loc="booking_id")
        current_user = self.current_user.user_info
        uuid = generate_uuid()

        data_file_upload = await file_upload.read()
        self.call_validator(await file_validator(data_file_upload))

        info_file = self.call_repos(await repos_upload_file(
            file=data_file_upload,
            name=file_upload.filename,
            ekyc_flag=ekyc_flag,
            booking_id=booking_id
        ))

        data_insert = {
            "id": uuid,
            "booking_id": booking_id,
            "document_file_type_id": DOCUMENT_FILE_TYPE,
            "document_file_folder_id": DOCUMENT_FILE_FOLDR,
            "root_id": uuid,
            "file_uuid": info_file['file_url'],
            "created_by_branch_name": current_user.hrm_branch_name,
            "created_by_branch_code": current_user.hrm_branch_code,
            "created_by_user_name": current_user.name,
            "created_by_user_code": current_user.code,
            "updated_by_user_name": current_user.name,
            "updated_by_user_code": current_user.code
        }

        self.call_repos(
            await repo_add_document_file(
                data=data_insert,
                session=self.oracle_session
            )
        )

        return self.response(data=data_insert)
