from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.constant.gw import (
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF
)


class ServiceGW:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["gw"]['url']

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def get_casa_account_from_cif(self, casa_cif_number):
        request_data = {
            "selectCurrentAccountFromCIF_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": "SCB Cống Quỳnh",
                        "branch_code": "137"
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": "CurrentAccountFromCIF",
                        "transaction_value": {
                            "cif_num": casa_cif_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_deposit_account_from_cif(self, account_cif_number):
        request_data = {
            "selectDepositAccountFromCIF_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": "SCB Cống Quỳnh",
                        "branch_code": "137"
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": "DepositAccountFromCIF",
                        "transaction_value": {
                            "cif_num": account_cif_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data
