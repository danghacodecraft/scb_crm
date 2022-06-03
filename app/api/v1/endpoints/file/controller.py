from typing import List, Optional

from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.file.repository import (
    repos_download_ekyc_file, repos_download_file, repos_download_multi_file,
    repos_upload_file, repos_upload_multi_file
)
from app.api.v1.endpoints.file.validator import (
    file_validator, multi_file_validator
)
from app.third_parties.services.ekyc import ServiceEKYC
from app.utils.functions import now


class CtrFile(BaseController):
    async def upload_file(
            self,
            file_upload: UploadFile,
            ekyc_flag: bool,
            booking_id: Optional[str],
            save_to_db_flag: bool = False
    ):
        data_file_upload = await file_upload.read()

        self.call_validator(await file_validator(data_file_upload))

        is_success, info_file = self.call_repos(await repos_upload_file(
            file=data_file_upload,
            name=file_upload.filename,
            ekyc_flag=ekyc_flag,
            save_to_db_flag=save_to_db_flag,
            booking_id=booking_id
        ))
        if not is_success:
            return self.response_exception(msg="ERROR_INSERT_DOCUMENT_FILE", detail=str(info_file))

        info_file['created_at'] = now()
        return self.response(data=info_file)

    async def upload_multi_file(self, file_uploads: List[UploadFile]):
        data_file_uploads = [await file_upload.read() for file_upload in file_uploads]
        names = [file_upload.filename for file_upload in file_uploads]

        self.call_validator(await multi_file_validator(data_file_uploads))

        info_files = self.call_repos(await repos_upload_multi_file(files=data_file_uploads, names=names))
        for info_file in info_files:
            info_file['created_at'] = now()

        return self.response(data=info_files)

    async def download_file(self, uuid: str):
        info = self.call_repos(await repos_download_file(uuid=uuid))

        # TODO: service file sửa download thì xóa dòng này
        info['uuid'] = uuid

        return self.response(data=info)

    async def download_multi_file(self, uuids: List[str]):
        if not uuids:
            return self.response_exception(msg='LIST_UUID_EMPTY', detail='List uuid can not be empty', loc='uuids')

        info = self.call_repos(await repos_download_multi_file(uuids=uuids))
        return self.response(data=info)

    async def upload_ekyc_file(self, uuid_ekyc: str, booking_id: Optional[str]):
        info = self.call_repos(await repos_download_ekyc_file(
            uuid=uuid_ekyc,
            booking_id=booking_id
        ))

        service = ServiceEKYC()
        info_file = await service.upload_file_ekyc(info=info, booking_id=booking_id)

        return self.response(data=info_file)
