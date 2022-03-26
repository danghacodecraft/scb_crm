import aiohttp
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE_TEMPLATE


class ServiceTMS:
    tms_service = SERVICE["tms"]
    __host = tms_service['url']
    __header = tms_service['headers']

    def start(self):
        self.session = aiohttp.ClientSession()  # noqa

    async def stop(self):
        await self.session.close()
        self.session = None  # noqa

    async def fill_form(self, body: dict):

        path = "/api/v2/van-hanh/mau-chung-1/ciffff/thu-muc-cif-1/crm-bm001/fill_data/"
        method = "POST"
        url = f"{self.__host}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.__header,
                        json=body
                ) as res:
                    # handle response
                    if res.status != status.HTTP_200_OK:
                        return False, {
                            "url": url,
                            "headers": self.__header,
                            "message": await res.json(),
                        }

                    data = await res.json()

                    return True, data

        except Exception:  # noqa

            return False, ERROR_CALL_SERVICE_TEMPLATE
