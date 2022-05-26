import aiohttp
from starlette import status

from app.settings.service import SERVICE


class ServiceTMS:
    tms_service = SERVICE["tms"]
    __host = tms_service['url']
    __header = tms_service['headers']

    def start(self):
        self.session = aiohttp.ClientSession()  # noqa

    async def stop(self):
        await self.session.close()
        self.session = None  # noqa

    async def fill_form(self, body: dict, path: str):
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
                    if res.status == status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return False, {
                            "url": url,
                            "headers": self.__header,
                            "message": f"Status: {res.status}",
                        }
                    elif res.status != status.HTTP_200_OK:
                        return False, {
                            "url": url,
                            "headers": self.__header,
                            "message": f"Status: {res.status}" + await res.json(),
                        }

                    data = await res.json()

                    return True, data

        except Exception as ex:  # noqa
            return False, {
                "url": url,
                "headers": self.__header,
                "message": ex,
            }
