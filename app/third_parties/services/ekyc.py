from typing import Optional, Tuple

import aiohttp
from aiohttp.typedefs import StrOrURL
from aiohttp.web_exceptions import HTTPException
from loguru import logger
from starlette import status

from app.settings.config import APPLICATION
from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC


class ServiceEKYC:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["ekyc"]['url']
    proxy: Optional[StrOrURL] = APPLICATION["ekyc_proxy"] if APPLICATION["ekyc_proxy"] != "" else None
    headers = {
        "X-TRANSACTION-ID": SERVICE["ekyc"]['x-transaction-id'],
        "AUTHORIZATION": SERVICE["ekyc"]['authorization'],
        "X-DEVICE-INFO": "eyJkZXZpY2VOYW1lIjoibWluaOKAmXMgaVBob25lIiwib3MiOiJJT1MiLCJtb2RlbCI6ImlQaG9uZSBYUiIsInBob25lX"
                         "251bWJlciI6IjA5MDI0MDk2NjQiLCJtYW51ZmFjdHVyZXIiOiJBcHBsZSIsIm9zVmVyc2lvbiI6IjE0LjEifQ"  # TODO
    }

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def ocr_identity_document(self, file: bytes, filename: str, identity_type: int) -> Tuple[bool, dict]:
        api_url = f"{self.url}/api/v1/card-service/ocr/"

        form_data = aiohttp.FormData()
        form_data.add_field("file", value=file, filename=filename)
        form_data.add_field("type", value=str(identity_type))

        try:
            async with self.session.post(url=api_url, data=form_data, headers=self.headers,
                                         proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def add_face(self, file: bytes):
        """
        Thêm 1 ảnh người vào trong eKYC
        """
        api_url = f"{self.url}/api/v1/face-service/add/"
        form_data = aiohttp.FormData()
        form_data.add_field("file", value=file, filename='abc.jpg')

        try:
            async with self.session.post(url=api_url, data=form_data, headers=self.headers,
                                         proxy=self.proxy) as response:
                logger.log("SERVICE", f"[ADD FACE] {response.status} : {api_url}")
                if response.status == status.HTTP_201_CREATED:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS" + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {
                "message": str({
                    "proxy": self.proxy,
                    "type": type(self.proxy),
                    "url": api_url,
                    "res": str(ex)
                }),
            }

    async def compare_face(self, face_uuid: str, avatar_image_uuid: str):
        """
        So sánh khuôn mặt trong 2 ảnh
        """
        api_url = f"{self.url}/api/v1/face-service/compare/"

        data = {
            "image_face_1_uuid": face_uuid,
            "image_face_2_uuid": avatar_image_uuid
        }

        try:
            async with self.session.post(url=api_url, json=data, headers=self.headers, proxy=self.proxy) as response:
                logger.log("SERVICE", f"[COMPARE FACE] {response.status} : {api_url}")

                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST or response.status == status.HTTP_404_NOT_FOUND:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except HTTPException as ex:
            logger.error(str(ex))
            return False, {
                "message": str({
                    "proxy": self.proxy,
                    "type": type(self.proxy),
                    "url": api_url,
                    "res": str(ex)
                }),
            }

    async def validate(self, data, document_type):
        api_url = f"{self.url}/api/v1/card-service/validate/"

        is_success = True
        request_body = {
            "document_type": document_type,
            "data": data
        }

        try:
            async with self.session.post(url=api_url, json=request_body, headers=self.headers,
                                         proxy=self.proxy) as response:
                logger.log("SERVICE", f"[VALIDATE] {response.status} : {api_url}")
                if response.status != status.HTTP_200_OK:
                    return False, {
                        "errors": {
                            "message": ERROR_CALL_SERVICE_EKYC,
                            "detail": "STATUS " + str(response.status)
                        }
                    }
                response_body = await response.json()
                if not response_body['success']:
                    is_success = False

                return is_success, response_body
        except Exception as ex:
            logger.error(str(ex))
            return False, {"errors": {"message": "eKYC error please try again later"}}

    async def get_list_kss(self, query_data):
        api_url = f"{self.url}/api/v1/customer-service/crm/"

        try:
            async with self.session.get(url=api_url, headers=self.headers, params=query_data,
                                        proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def get_list_branch(self, query_param: dict):
        api_url = f"{self.url}/api/v1/customer-service/crm/branch"
        try:
            async with self.session.get(url=api_url, headers=self.headers, params=query_param,
                                        proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }
        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def get_list_zone(self):
        api_url = f"{self.url}/api/v1/customer-service/crm/zone/"

        try:
            async with self.session.get(url=api_url, headers=self.headers, proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {
                "message": str({
                    "proxy": self.proxy,
                    "type": type(self.proxy),
                    "url": api_url,
                    "res": str(ex)
                }),
            }

    async def get_statistics_profiles(self):
        api_url = f"{self.url}/api/v1/customer-service/crm/profilestatistics"
        try:
            async with self.session.get(url=api_url, headers=self.headers, proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def get_statistics_months(self, months: int):
        api_url = f"{self.url}/api/v1/customer-service/crm/statisticsbymonth/"

        query = {
            'month': months
        }
        try:
            async with self.session.get(url=api_url, headers=self.headers, params=query, proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def get_history_post_check(self, postcheck_uuid: str):
        api_url = f"{self.url}/api/v1/customer-service/crm/postcontrolhistory/"

        query = {
            'customer_id': postcheck_uuid
        }
        try:
            async with self.session.get(url=api_url, headers=self.headers, params=query, proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def update_post_check(self, request_data):
        api_url = f"{self.url}/api/v1/customer-service/crm/postcontrol/"

        try:
            async with self.session.put(url=api_url, json=request_data, headers=self.headers,
                                        proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                elif response.status == status.HTTP_404_NOT_FOUND:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def get_statistics(self, query_param: dict):
        api_url = f"{self.url}/api/v1/customer-service/crm/statistics/"

        try:
            async with self.session.get(url=api_url, headers=self.headers, params=query_param,
                                        proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def get_customer_detail(self, postcheck_uuid: str):
        api_url = f"{self.url}/api/v1/customer-service/crm/{postcheck_uuid}/"

        try:
            async with self.session.get(url=api_url, headers=self.headers, proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                elif response.status == status.HTTP_404_NOT_FOUND:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def create_post_check(self, payload_data: dict):
        api_url = f"{self.url}/api/v1/customer-service/crm/postcontrol/"

        try:
            async with self.session.post(url=api_url, headers=self.headers, json=payload_data,
                                         proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_201_CREATED:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                elif response.status == status.HTTP_404_NOT_FOUND:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)

                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def get_post_control(self, query_params):
        api_url = f"{self.url}/api/v1/customer-service/crm/postcontrol/"

        try:
            async with self.session.get(url=api_url, params=query_params, headers=self.headers,
                                        proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")
                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST:
                    return False, await response.json()
                elif response.status == status.HTTP_404_NOT_FOUND:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status)

                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def upload_file(self, file: bytes, name):
        api_url = f"{self.url}/api/v1/file-service/"

        form_data = aiohttp.FormData()
        form_data.add_field('file', value=file, filename=name)
        try:
            async with self.session.post(url=api_url, data=form_data, headers=self.headers,
                                         proxy=self.proxy) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")

                if response.status == status.HTTP_201_CREATED:
                    return True, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status),
                        "api_url": api_url,
                        "response": await response.json()
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}
