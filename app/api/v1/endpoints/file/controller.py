from typing import List

import aiohttp
from fastapi import UploadFile
from starlette import status

from app.api.base.controller import BaseController
from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.file.repository import (
    repos_dowload_ekyc_file, repos_download_file, repos_download_multi_file,
    repos_upload_file, repos_upload_multi_file
)
from app.api.v1.endpoints.file.validator import (
    file_validator, multi_file_validator
)
from app.settings.event import service_file
from app.third_parties.services.ekyc import ServiceEKYC
from app.utils.error_messages import ERROR_CALL_SERVICE_FILE, ERROR_INVALID_URL
from app.utils.functions import now, replace_with_cdn


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

    async def upload_ekyc_file(self, uuid_ekyc: str):
        info = self.call_repos(await repos_dowload_ekyc_file(uuid=uuid_ekyc))
        async with aiohttp.ClientSession() as session:
            url = ServiceEKYC().url
            uri = info["uri"]
            url = replace_with_cdn(
                cdn=uri if uri.startswith('/') else url + '/cdn/' + uri,
                file_url=url
            )
            async with session.get(url, ssl=False) as resp:
                if resp.status == status.HTTP_200_OK:
                    file = resp.content
                    info_file = await service_file.upload_file(file=file, name=info["file_name"])
                    if not info_file:
                        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

                    return self.response(data=info_file)
                else:
                    return self.response(data={
                        "message": ERROR_INVALID_URL,
                        "detail": f"Invalid: {url}"
                    })
