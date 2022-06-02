import asyncio
from typing import List, Optional, Any
from urllib.parse import urlparse

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.third_parties.oracle.base import SessionLocal
from app.third_parties.oracle.models.document_file.model import DocumentFile
from app.utils.constant.document_file import DOCUMENT_FILE_TYPE_CODE_FILE, DOCUMENT_FILE_FOLDER_CODE_DEFAULT
from app.utils.functions import generate_uuid


class ServiceFile:
    session: Optional[aiohttp.ClientSession] = None
    oracle_session: Optional[SessionLocal] = None

    url = SERVICE["file"]['url']
    cdn = SERVICE["file"]['service_file_cdn']
    headers = {
        "server-auth": SERVICE["file"]['server-auth'],
        "AUTHORIZATION": SERVICE["file"]['authorization']
    }

    def start(self):
        self.session = aiohttp.ClientSession()
        self.oracle_session = SessionLocal()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def __call_upload_file(
            self,
            file: bytes,
            name: str,
            return_download_file_url_flag: bool,
            save_to_db_flag: bool = False,
            booking_id: Optional[str] = None,
            **kwargs
    ) -> tuple[bool, Any]:
        """
            Upload file lưu vào DB -> current_user
            Upload file không lưu vào DB -> current_user=None
        """
        api_url = f'{self.url}/api/v1/files/'

        form_data = aiohttp.FormData()
        form_data.add_field('file', value=file, filename=name)
        form_data.add_field('return_download_file_url_flag', value=str(return_download_file_url_flag))

        try:
            async with self.session.post(
                    url=api_url,
                    data=form_data,
                    headers=self.headers
            ) as response:
                logger.log("SERVICE", f"[FILE] {response.status} : {api_url}")

                if response.status != status.HTTP_201_CREATED:
                    return await response.json()

                upload_file_response_body = await response.json()
                if upload_file_response_body['file_url']:
                    upload_file_response_body['file_url'] = self.replace_with_cdn(upload_file_response_body['file_url'])

                # Lưu vào DB
                document_file_id = None
                if save_to_db_flag:
                    document_file_id = generate_uuid()
                    document_file = dict(
                        id=document_file_id,
                        file_uuid=upload_file_response_body['uuid'],
                        root_id=document_file_id,
                        booking_id=booking_id,
                        document_file_type_id=DOCUMENT_FILE_TYPE_CODE_FILE
                        if 'document_file_type_id' not in kwargs.keys()
                        else kwargs.get('document_file_type_id'),
                        document_file_folder_id=DOCUMENT_FILE_FOLDER_CODE_DEFAULT
                        if 'document_file_folder_id' not in kwargs.keys()
                        else kwargs.get('document_file_folder_id'),
                    )

                    {document_file.update({key: value}) for key, value in kwargs.items()}

                    self.oracle_session.add(DocumentFile(**document_file))
                    self.oracle_session.commit()

                upload_file_response_body.update(
                    document_file_id=document_file_id
                )

                return True, upload_file_response_body
        except Exception as ex:
            logger.error(str(ex))
            return False, str(ex)

    async def upload_file(
            self,
            file: bytes,
            name: str,
            booking_id: Optional[str] = None,
            return_download_file_url_flag: bool = True,
            save_to_db_flag: bool = False,
            **kwargs
    ) -> tuple[bool, Any]:
        """
        Upload file lưu vào DB -> current_user
        Upload file không lưu vào DB -> current_user=None
        """
        return await self.__call_upload_file(
            booking_id=booking_id,
            save_to_db_flag=save_to_db_flag,
            file=file,
            name=name,
            return_download_file_url_flag=return_download_file_url_flag,
            **kwargs
        )

    async def upload_multi_file(self, files: List[bytes], names: List[str],
                                return_download_file_url_flag: bool = True) -> Optional[List[dict]]:
        coroutines = []
        for index, file in enumerate(files):
            # coroutines.append(self.__call_upload_file(file=file))
            coroutines.append(
                asyncio.ensure_future(
                    self.__call_upload_file(
                        file=file,
                        name=names[index],
                        return_download_file_url_flag=return_download_file_url_flag
                    )
                )
            )

        return list(await asyncio.gather(*coroutines))

    async def download_file(self, uuid: str) -> Optional[dict]:
        api_url = f"{self.url}/api/v1/files/{uuid}/download/"

        try:
            async with self.session.get(url=api_url, headers=self.headers) as response:
                logger.log("SERVICE", f"[FILE] {response.status} : {api_url}")

                if response.status != status.HTTP_200_OK:
                    return None

                file_download_response_body = await response.json()

                file_download_response_body['file_url'] = self.replace_with_cdn(file_download_response_body['file_url'])
        except Exception as ex:
            logger.error(str(ex))
            return None

        return file_download_response_body

    async def download_multi_file(self, uuids: List[str]) -> Optional[List[dict]]:
        api_url = f"{self.url}/api/v1/files/download/"

        try:
            async with self.session.get(url=api_url, headers=self.headers, params={'uuid': uuids}) as response:
                logger.log("SERVICE", f"[FILE] {response.status} : {api_url}")

                if response.status != status.HTTP_200_OK:
                    return None

                multi_file_download_response_body = await response.json()
        except Exception as ex:
            logger.error(str(ex))
            return None

        for file_download_response_body in multi_file_download_response_body:
            file_download_response_body['file_url'] = self.replace_with_cdn(file_download_response_body['file_url'])

        return multi_file_download_response_body

    async def is_exist_multi_file(self, uuids: List[str]) -> Optional[bool]:
        """
        Nếu tất cả UUID tồn tại thì trả về True
        Nếu có ít nhất một UUID không tồn tại thì False
        :param uuids:
        :return:
        """
        api_url = f"{self.url}/api/v1/files/exist/?{'&'.join([f'uuid={uuid}' for uuid in uuids])}"

        try:
            async with self.session.get(url=api_url, headers=self.headers) as response:
                logger.log("SERVICE", f"[FILE] {response.status} : {api_url}")

                if response.status == status.HTTP_200_OK:
                    return True
                else:
                    return False
        except Exception as ex:
            logger.error(str(ex))
            return None

    def replace_with_cdn(self, file_url: str) -> str:
        if self.cdn:
            file_url_parse_result = urlparse(file_url)

            # Thay thế link tải file từ service bằng CDN config theo dự án
            return file_url.replace(f'{file_url_parse_result.scheme}://{file_url_parse_result.netloc}', self.cdn)
        else:
            return file_url

    async def get_file_info(self, uuid: str) -> Optional[dict]:
        api_url = f"{self.url}/api/v1/files/{uuid}/"

        try:
            async with self.session.get(url=api_url, headers=self.headers) as response:
                logger.log("SERVICE", f"[FILE] {response.status} : {api_url}")

                if response.status != status.HTTP_200_OK:
                    return None

                file_info_response_body = await response.json()

        except Exception as ex:
            logger.error(str(ex))
            return None

        return file_info_response_body
