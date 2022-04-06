from typing import Optional

import aiohttp as aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE_DWH


class ServiceDWH:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["dwh"]['url']
    header = SERVICE["dwh"]['url']
    headers = {
        "AUTHORIZATION": SERVICE["dwh"]['headers']['authorization'],
    }

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

    async def detail_work_process(self, employee_id: str):
        method = "GET"
        path = f"/api/v1/employee/emp_detail_work_process/?emp={employee_id}"
        url = f"{self.url}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.headers
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

    async def kpi(self, employee_id: str):
        method = "GET"
        path = f"/api/v1/employee/emp_detail_kpi/?emp={employee_id}"
        url = f"{self.url}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.headers
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

    async def discipline(self, employee_id: str):
        method = "GET"
        path = f"/api/v1/employee/emp_detail_discipline/?emp={employee_id}"
        url = f"{self.url}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.headers
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

    async def felicitation(self, employee_id: str):
        method = "GET"
        path = f"/api/v1/employee/emp_detail_bonus/?emp={employee_id}"
        url = f"{self.url}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.headers
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

    async def sub_info(self, employee_id: str):
        method = "GET"
        path = f"/api/v1/employee/emp_detail_other/?emp={employee_id}"
        url = f"{self.url}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.headers
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

    async def training_in_scb(self, employee_id: str):
        method = "GET"
        path = f"/api/v1/employee/emp_detail_training/?emp={employee_id}"
        url = f"{self.url}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.headers
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