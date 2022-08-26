import json

import aiohttp
from starlette import status


class ServiceTMS:
    def __init__(self, init_service):
        self.session = None
        self.tms_service = init_service
        self.tms_url = self.tms_service["tms"]['url']
        self.tms_header = self.tms_service["tms"]['headers']

    def start(self):
        self.session = aiohttp.ClientSession()  # noqa

    async def stop(self):
        await self.session.close()
        self.session = None  # noqa

    async def fill_form(self, body: dict, path: str):
        url = f"{self.tms_url}{path}fill_data_and_show_list_detail_field/"
        body = json.dumps(body)
        try:
            async with self.session.post(
                    url=url,
                    headers=self.tms_header,
                    data=body
            ) as res:
                # handle response
                if res.status == status.HTTP_500_INTERNAL_SERVER_ERROR:
                    return False, {
                        "url": url,
                        "headers": self.tms_header,
                        "message": f"Status: {res.status}",
                    }
                elif res.status != status.HTTP_200_OK:
                    return False, {
                        "url": url,
                        "headers": self.tms_header,
                        "message": f"Status: {res.status}" + str(await res.json()),
                    }

                data = await res.json()

                return True, data

        except Exception as ex:  # noqa
            return False, {
                "url": url,
                "headers": self.tms_header,
                "message": str(ex),
            }
