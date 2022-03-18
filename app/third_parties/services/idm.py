import json
from typing import Dict, Union

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE_IDM


class ServiceIDM:
    HOST = SERVICE["idm"]['host']

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def login(self, username, password) -> (bool, Union[str, Dict]):
        """
        Input: username,password, app_code từ login của CRM
        Output: Thông tin user từ IDM
        """
        headers = SERVICE["idm"]['headers']
        path = "/api/v1/staff/login"
        url = f'{self.HOST}{path}'

        data_user_login = {
            'username': username,
            'password': password,
            "app_code": "CRM"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method='post',
                        url=url,
                        data=json.dumps(data_user_login),
                        headers=headers
                ) as response:

                    if response.status == status.HTTP_200_OK:
                        return True, await response.json()
                    if response.status == status.HTTP_400_BAD_REQUEST:
                        return False, await response.json()
                    return False, {
                        "message": ERROR_CALL_SERVICE_IDM,
                        "detail": "STATUS " + str(response.status)
                    }
        except Exception as ex:
            logger.exception(ex)
            return False, {"message": str(ex)}
