import asyncio
from typing import List, Optional
from urllib.parse import urlparse

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE


class ServiceFile:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["file"]['url']
    cdn = SERVICE["file"]['service_file_cdn']
    headers = {
        "server-auth": SERVICE["file"]['server-auth'],
        "AUTHORIZATION": SERVICE["file"]['authorization']
    }

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def __call_upload_file(self, file: bytes, name: str, return_download_file_url_flag: bool) -> Optional[dict]:
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
                    return None

                upload_file_response_body = await response.json()
                if upload_file_response_body['file_url']:
                    upload_file_response_body['file_url'] = self.replace_with_cdn(upload_file_response_body['file_url'])

                return upload_file_response_body
        except Exception as ex:
            logger.error(str(ex))
            return None

    async def upload_file(self, file: bytes, name: str, return_download_file_url_flag: bool = True) -> Optional[dict]:
        return await self.__call_upload_file(
            file=file,
            name=name,
            return_download_file_url_flag=return_download_file_url_flag
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
