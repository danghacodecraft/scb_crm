from typing import List

import requests
from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.file.repository import (
    repos_download_file, repos_download_multi_file, repos_upload_file,
    repos_upload_file_ekyc, repos_upload_multi_file
)
from app.api.v1.endpoints.file.validator import (
    file_validator, multi_file_validator
)
from app.settings.event import service_file
from app.utils.error_messages import ERROR_CALL_SERVICE_FILE
from app.utils.functions import now


class CtrFile(BaseController):
    async def upload_file(self, file_upload: UploadFile, ekyc_flag: bool):
        data_file_upload = await file_upload.read()

        self.call_validator(await file_validator(data_file_upload))

        info_file = self.call_repos(await repos_upload_file(
            file=data_file_upload,
            name=file_upload.filename,
            ekyc_flag=ekyc_flag
        ))

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

    async def upload_file_ekyc(self, uuid: str):
        info = self.call_repos(await repos_upload_file_ekyc(uuid=uuid))
        # TODO : lỗi url ekyc trả về
        url = "https://scb-ekycapp.minerva.vn/cdn/ekyc-dev/198401/23-03-2022/80dd96880f7c464d94c6" \
              "febf10462377?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ekyc-dev%2F20220323%2Fus" \
              "-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220323T085444Z&X-Amz-Expires=3600&X-Amz-SignedHeader" \
              "s=host&X-Amz-Signature=f1b50851c5fac7385b4b4d11dc6a3a2e61e56958420d7c8ed26154f7a0fae597"

        file = requests.get(url)

        info_file = await service_file.upload_file(file=file.content, name=info["file_name"])
        if not info_file:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

        return self.response(data=info_file)
