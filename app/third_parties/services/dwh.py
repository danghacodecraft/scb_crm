from typing import Optional

import aiohttp as aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE_DWH


class ServiceDWH:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["dwh"]['url']

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def detail(self, employee_id: str):
        method = "GET"
        path = f"/api/v1/employee/emp_detail/?emp={employee_id}"
        url = f"{self.url}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url
                ) as res:
                    # handle response
                    if res.status != status.HTTP_200_OK:
                        return False, {
                            "url": url,
                            "message": await res.json(),
                        }

                    data = await res.json()

                    return True, data

        except Exception as ex:  # noqa
            logger.error(str(ex))
            return False, ERROR_CALL_SERVICE_DWH
