from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.settings.service import SERVICE
from app.utils.address_functions.functions import matching_place_residence
from app.utils.constant.cif import (
    CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE, SOA_GENDER_TYPE_MALE
)
from app.utils.constant.soa import (
    SOA_DATETIME_FORMAT, SOA_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT,
    SOA_REPONSE_STATUS_SUCCESS
)
from app.utils.error_messages import ERROR_INVALID_URL, MESSAGE_STATUS
from app.utils.functions import date_string_to_other_date_string_format


class ServiceSOA:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["soa"]['url']
    username = SERVICE["soa"]["authorization_username"]
    password = SERVICE["soa"]["authorization_password"]
    soa_basic_auth = aiohttp.BasicAuth(login=username, password=password, encoding='utf-8')

    def start(self):
        self.session = aiohttp.ClientSession(auth=self.soa_basic_auth)

    async def stop(self):
        await self.session.close()
        self.session = None

    async def retrieve_customer_ref_data_mgmt(self, cif_number: str):
        """
        Input: cif_number - Số CIF
        Output: (is_success, is_existed/error_message) - Thành công, Có tồn tại/ Lỗi Service SOA
        """
        is_success = True
        request_data = {
            "retrieveCustomerRefDataMgmt_in": {
                "transactionInfo": {
                    "clientCode": "INAPPTABLET",  # TODO
                    "cRefNum": "CRM1641783511239",  # TODO
                    "branchInfo": {
                        "branchCode": "001"  # TODO
                    }
                },
                "CIFInfo": {
                    "CIFNum": cif_number
                }
            }
        }
        api_url = f"{self.url}{SOA_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT}"
        return_data = dict(
            is_existed=False
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[SOA] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    logger.error(f"[STATUS]{str(response.status)} [ERROR_INFO]")
                    return_data.update(message="Service SOA Status error please try again later")
                    return False, return_data

                response_data = await response.json()

                # Nếu tồn tại CIF
                if response_data["retrieveCustomerRefDataMgmt_out"]["transactionInfo"]["transactionReturn"] == SOA_REPONSE_STATUS_SUCCESS:
                    customer_info = response_data["retrieveCustomerRefDataMgmt_out"]["customerInfo"]
                    customer_address = customer_info["address"]
                    customer_identity = customer_info["IDInfo"]

                    _, resident_address = matching_place_residence(customer_address["address_vn"])
                    _, contact_address = matching_place_residence(customer_address["address1"])
                    return_data.update({
                        "is_existed": True,
                        "data": {
                            "id": cif_number,
                            "avatar_url": None,  # TODO
                            "basic_information": {
                                "cif_number": cif_number,
                                "full_name_vn": customer_info["fullname_vn"] if customer_info["fullname_vn"] else None,
                                "date_of_birth": date_string_to_other_date_string_format(
                                    customer_info["birthDay"],
                                    from_format=DATETIME_INPUT_OUTPUT_FORMAT
                                ) if customer_info["birthDay"] else None,
                                "gender": CRM_GENDER_TYPE_MALE
                                if customer_info["gender"] == SOA_GENDER_TYPE_MALE
                                else CRM_GENDER_TYPE_FEMALE,
                                "nationality": customer_info["nationlityCode"],
                                "telephone_number": customer_address["telephoneNum"],
                                "mobile_number": customer_address["mobileNum"],
                                "email": customer_address["email"],
                            },
                            "identity_document": {
                                "identity_number": customer_identity["IDNum"],
                                "issued_date": date_string_to_other_date_string_format(
                                    customer_identity["IDIssuedDate"],
                                    from_format=SOA_DATETIME_FORMAT
                                ) if customer_identity["IDIssuedDate"] else None,
                                "place_of_issue": customer_identity["IDIssuedLocation"],
                                # TODO: T ĐỒNG THÁP/ĐỒNG THÁP
                                "expired_date": None  # TODO
                            },
                            "address_information": {
                                "contact_address": {
                                    "province": contact_address["province_code"],
                                    "district": contact_address["district_code"],
                                    "ward": contact_address["ward_code"],
                                    "number_and_street": contact_address["street_name"]
                                },
                                "resident_address": {
                                    "province": resident_address["province_code"],
                                    "district": resident_address["district_code"],
                                    "ward": resident_address["ward_code"],
                                    "number_and_street": resident_address["street_name"]
                                }
                            }
                        }
                    })

        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return_data.update(message="Connect to service SOA error please try again later")
            return False, return_data

        except KeyError as ex:
            logger.error(str(ex))
            return_data.update(message="Key error " + str(ex))
            return False, return_data

        except aiohttp.InvalidURL as ex:
            logger.error(str(ex))
            return_data.update(message=MESSAGE_STATUS[ERROR_INVALID_URL] + ": " + str(ex))
            return False, return_data

        return is_success, return_data