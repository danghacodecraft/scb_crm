from typing import Optional, Tuple

import aiohttp
from aiohttp.typedefs import StrOrURL
from aiohttp.web_exceptions import HTTPException
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC
from app.utils.functions import convert_string_to_uuidv4


class ServiceEKYC:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["ekyc"]['url']
    proxy: Optional[StrOrURL] = None
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        form_data = aiohttp.FormData()
        form_data.add_field("file", value=file, filename=filename)
        form_data.add_field("type", value=str(identity_type))

        try:
            async with self.session.post(url=api_url, data=form_data, headers=headers,
                                         ssl=False) as response:
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.post(url=api_url, data=form_data, headers=headers,
                                         ssl=False) as response:
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        data = {
            "image_face_1_uuid": face_uuid,
            "image_face_2_uuid": avatar_image_uuid
        }

        try:
            async with self.session.post(url=api_url, json=data, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[COMPARE FACE] {response.status} : {api_url}")

                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                elif response.status == status.HTTP_400_BAD_REQUEST or response.status == status.HTTP_404_NOT_FOUND:
                    return False, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC + " STATUS " + str(response.status)
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        is_success = True
        request_body = {
            "document_type": document_type,
            "data": data
        }

        try:
            async with self.session.post(url=api_url, json=request_body, headers=headers,
                                         ssl=False) as response:
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, headers=headers, params=query_data,
                                        ssl=False) as response:
                logger.log("SERVICE", f"[EKYC LIST KSS] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, headers=headers, params=query_param,
                                        ssl=False) as response:
                logger.log("SERVICE", f"[EKYC LIST BRACNH] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC LIST ZONE] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC PROFILESTATISTICS] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        query = {
            'month': months
        }
        try:
            async with self.session.get(url=api_url, headers=headers, params=query, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC STATISTICS] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        query = {
            'customer_id': postcheck_uuid
        }
        try:
            async with self.session.get(url=api_url, headers=headers, params=query, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC HISTORY] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.put(url=api_url, json=request_data, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC UPDATE POST CHECK] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, headers=headers, params=query_param, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC STATISTICS] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC CUSTOMER DETAIL] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.post(url=api_url, headers=headers, json=payload_data, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC POST CONTROL] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, params=query_params, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC GET CONTROL] {response.status} : {api_url}")
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

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        headers['X-TRANSACTION-ID'] = "CRM_"

        form_data = aiohttp.FormData()
        form_data.add_field('file', value=file, filename=name)
        try:
            async with self.session.post(url=api_url, data=form_data, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC UPLOAD FILE] {response.status} : {api_url}")
                if response.status == status.HTTP_201_CREATED:
                    return True, await response.json()
                elif response.status >= status.HTTP_500_INTERNAL_SERVER_ERROR:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status),
                        "api_url": api_url,
                        "response": None
                    }
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

    async def compare_signature(self, cif_id: str, uuid_ekyc: str, sign_uuid: str):
        api_url = f"{self.url}/api/v1/face-service/compare_signature/"

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        UUIDV4 = convert_string_to_uuidv4(cif_id)
        headers['X-TRANSACTION-ID'] = f"CRM_{UUIDV4}"

        json_body = {
            "image_sign_1_uuid": uuid_ekyc,
            "image_sign_2_uuid": sign_uuid
        }
        try:
            async with self.session.post(url=api_url, json=json_body, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC COMPARE SIGNATURE] {response.status} : {api_url}")

                if response.status == status.HTTP_200_OK:
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

    async def add_finger_ekyc(self, cif_id: str, json_body: dict):
        api_url = f"{self.url}/api/v1/finger-service/add/"

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        UUIDV4 = convert_string_to_uuidv4(cif_id)
        headers['X-TRANSACTION-ID'] = f"CRM_{UUIDV4}"

        try:
            async with self.session.post(url=api_url, json=json_body, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC ADD FINGER] {response.status} : {api_url}")
                if response.status == status.HTTP_201_CREATED:
                    return True, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status),
                        "api_url": api_url,
                        "response": {}
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def compare_finger_ekyc(self, cif_id: str, json_body: dict):
        api_url = f"{self.url}/api/v1/finger-service/verify/"

        headers = self.headers
        # thay đổi giá trị x-transaction-id
        UUIDV4 = convert_string_to_uuidv4(cif_id)
        headers['X-TRANSACTION-ID'] = f"CRM_{UUIDV4}"

        try:
            async with self.session.post(url=api_url, json=json_body, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC COMPARE FINGER] {response.status} : {api_url}")

                if response.status == status.HTTP_200_OK:
                    return True, await response.json()
                else:
                    return False, {
                        "message": ERROR_CALL_SERVICE_EKYC,
                        "detail": "STATUS " + str(response.status),
                        "api_url": api_url,
                        "response": {},
                    }

        except Exception as ex:
            logger.error(str(ex))
            return False, {"message": str(ex)}

    async def dowload_file(self, uuid: str, ):
        api_url = f"{self.url}/api/v1/file-service/{uuid}/"
        headers = self.headers
        # thay đổi giá trị x-transaction-id+
        headers['X-TRANSACTION-ID'] = "CRM_"

        try:
            async with self.session.get(url=api_url, headers=headers, ssl=False) as response:
                logger.log("SERVICE", f"[EKYC DOWNLOAD FILE] {response.status} : {api_url}")
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
