import aiohttp
from starlette import status

from app.settings.service import SERVICE

ERROR_CALL_SERVICE_TEMPLATE = "ERROR_CALL_SERVICE_TEMPLATE"


class ServiceTMS:
    tms_service = SERVICE["tms"]
    #
    # # __host = tms_service['url']
    __header = tms_service['headers']

    # __server_auth = ['server-auth']
    # __author = tms_service['authorization']

    def start(self):
        self.session = aiohttp.ClientSession()  # noqa

    async def stop(self):
        await self.session.close()
        self.session = None  # noqa

    async def fill_form(self, body: dict):

        # path = "/api/v2/van-hanh/mau-chung-1/ciffff/thu-muc-cif-1/crm-gdtv/fill_data/"
        method = "POST"
        # url = f"{self.__host}{path}"

        url = "http://192.168.73.135:9002/api/v2/van-hanh/mau-chung-1/ciffff/thu-muc-cif-1/crm-bm001/fill_data/"

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
                    # data_parse_url = urlparse(data['file_url'])
                    # new_data_parse_url = data_parse_url._replace(netloc='', scheme='')

                    # data['file_url'] = f"/cdn{new_data_parse_url.geturl()}"

                    return True, data

        except Exception:  # noqa

            return False, ERROR_CALL_SERVICE_TEMPLATE
