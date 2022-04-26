from datetime import date
from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.service import SERVICE
from app.utils.constant.gw import (
    GW_CURRENT_ACCOUNT_CASA, GW_CURRENT_ACCOUNT_FROM_CIF,
    GW_CUSTOMER_REF_DATA_MGMT_CIF_NUM, GW_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_DEPOSIT_ACCOUNT_TD, GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT
)
from app.utils.functions import date_to_string


class ServiceGW:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["gw"]['url']

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def get_casa_account_from_cif(self, current_user: UserInfoResponse, casa_cif_number: str):
        request_data = {
            "selectCurrentAccountFromCIF_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": GW_CURRENT_ACCOUNT_FROM_CIF,
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

    async def get_casa_account(self, current_user: UserInfoResponse, account_number: str):
        request_data = {
            "retrieveCurrentAccountCASA_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": GW_CURRENT_ACCOUNT_CASA,
                        "transaction_value": {
                            "account_num": account_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA}"

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

    async def get_report_history_casa_account(
        self,
        current_user: UserInfoResponse,
        account_number: str,
        transaction_name: str,
        from_date: date,
        to_date: date
    ):
        request_data = {
            "selectReportHisCaSaFromAcc_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": transaction_name,
                        "transaction_value": {
                            "P_ACC": account_number,
                            "P_FDATE": date_to_string(from_date),
                            "P_TDATE": date_to_string(to_date)
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT}"

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
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
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

    async def get_report_casa_account(
        self,
        current_user: UserInfoResponse,
        account_number: str,
        transaction_name: str,
    ):
        """
        Lấy thông tin biểu đồ hình tròn
        """
        request_data = {
            "selectReportHisCaSaFromAcc_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": transaction_name,
                        "transaction_value": {
                            "P_ACC": account_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT}"

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
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
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

    async def get_report_statement_casa_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str
    ):
        """
        Lấy thông tin lịch sử giao dịch TKTT
        """
        request_data = {
            "selectReportStatementCaSaFromAcc_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": transaction_name,
                        "transaction_value": {
                            "P_ACC": account_number,
                            "P_FDATE": "2016-02-01",
                            "P_TDATE": "2016-02-28"
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT}"

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
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
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

    async def get_deposit_account_from_cif(self, current_user: UserInfoResponse, account_cif_number):
        request_data = {
            "selectDepositAccountFromCIF_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": GW_DEPOSIT_ACCOUNT_FROM_CIF,
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

    async def get_deposit_account_td(self, current_user: UserInfoResponse, account_number):
        request_data = {
            "retrieveDepositAccountTD_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": GW_DEPOSIT_ACCOUNT_TD,
                        "transaction_value": {
                            "account_num": account_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD}"

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

    async def get_customer_info_list(self, current_user: UserInfoResponse, customer_cif_number):
        request_data = {
            "selectCustomerRefDataMgmtCIFNum_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": GW_CUSTOMER_REF_DATA_MGMT_CIF_NUM,
                        "transaction_value": {
                            "cif_num": customer_cif_number,
                            "id_num": "",
                            "mobile_num": "",
                            "full_name": ""
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM}"

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

    async def get_customer_info_detail(self, current_user: UserInfoResponse, customer_cif_number):
        request_data = {
            "retrieveCustomerRefDataMgmt_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": {
                    "transaction_info": {
                        "transaction_name": "CustFromCIF",
                        "transaction_value": {
                            "cif_num": customer_cif_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT}"

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
