from datetime import date
from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.service import SERVICE
from app.utils.constant.gw import (
    GW_AUTHORIZED_REF_DATA_MGM_ACC_NUM, GW_CO_OWNER_REF_DATA_MGM_ACC_NUM,
    GW_CURRENT_ACCOUNT_CASA, GW_CURRENT_ACCOUNT_FROM_CIF,
    GW_CUSTOMER_REF_DATA_MGMT_CIF_NUM, GW_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_DEPOSIT_ACCOUNT_TD, GW_EMPLOYEE_FROM_CODE, GW_EMPLOYEE_FROM_NAME,
    GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT
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

    async def get_report_statement_casa_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
            from_date: date,
            to_date: date
    ):
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
                            "P_FDATE": date_to_string(from_date),
                            "P_TDATE": date_to_string(to_date)
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

    async def get_report_statement_td_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
            from_date: date,
            to_date: date
    ):

        request_data = {
            "selectReportStatementTDFromAcc_in": {
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
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT}"

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
            "selectReportCaSaFromAcc_in": {
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
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT}"

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

    async def get_customer_info_list(
            self,
            current_user: UserInfoResponse,
            cif_number: str,
            identity_number: str,
            mobile_number: str,
            full_name: str
    ):
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
                            "cif_num": cif_number,
                            "id_num": identity_number,
                            "mobile_num": mobile_number,
                            "full_name": full_name
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

    async def get_co_owner(self, current_user: UserInfoResponse, account_number):
        request_data = {
            "selectCoownerRefDataMgmtAccNum_in": {
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
                        "transaction_name": GW_CO_OWNER_REF_DATA_MGM_ACC_NUM,
                        "transaction_value": {
                            "account_num": account_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM}"

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

    async def get_authorized(self, current_user: UserInfoResponse, account_number):
        request_data = {
            "selectAuthorizedRefDataMgmtAccNum_in": {
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
                        "transaction_name": GW_AUTHORIZED_REF_DATA_MGM_ACC_NUM,
                        "transaction_value": {
                            "account_num": account_number
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM}"

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

    async def get_employee_info_from_code(self, current_user: UserInfoResponse, employee_code):
        request_data = {
            "selectEmployeeInfoFromCode_in": {
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
                        "transaction_name": GW_EMPLOYEE_FROM_CODE,
                        "transaction_value": {
                            "employee_code": employee_code
                            # "13952"
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE}"

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

    async def get_employee_info_from_user_name(self, current_user: UserInfoResponse, employee_name):
        request_data = {
            "selectEmployeeInfoFromUserName_in": {
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
                        "transaction_name": GW_EMPLOYEE_FROM_NAME,
                        "transaction_value": {
                            "employee_name": employee_name
                            # "thanhdv3"
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME}"

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

    async def select_org_info(self, current_user: UserInfoResponse, transaction_name: str, endpoint: str,
                              function_name: str, id: str):
        request_data = {
            function_name: {
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
                        "transaction_name": transaction_name,
                        "transaction_value": {
                            "id": id
                        }
                    }
                }
            }
        }
        api_url = f"{self.url}{endpoint}"

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

    async def select_report_td_from_cif_data_input(
            self,
            current_user: UserInfoResponse,
            transaction_name: str,
            endpoint: str,
            account_number: str,
            from_date: Optional[date],
            to_date: Optional[date]
    ):
        request_data = {
            "selectReportTDFromCif_in": {
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
        api_url = f"{self.url}{endpoint}"

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

    async def open_cif(self, cif_id: str, current_user):

        request_data = {
            "openCIFAuthorise_in": {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "10.4.x.x",
                    "branch_info": {
                        "branch_code": current_user.user_info.hrm_branch_code,
                        "branch_name": current_user.user_info.hrm_branch_name
                    }
                },
                "data_input": {
                    "customer_info": {
                        "customer_type": "I",
                        "customer_category": "I_11",
                        "cus_ekyc": "EKYC_3",
                        "full_name": "Đỗ Văn Thạnh",
                        "gender": "F",
                        "telephone": "0904741808",
                        "mobile_phone": "0904741808",
                        "email": "",
                        "place_of_birth": "VN",
                        "birthday": "1998-11-11",
                        "tax": "",
                        "resident_status": "N",
                        "legal_guardian": "",
                        "co_owner": "",
                        "nationality": "VN",
                        "birth_country": "",
                        "language": "ENG",
                        "local_code": "101",
                        "current_official": "",
                        "biz_license_issue_date": "",
                        "cor_capital": "",
                        "cor_email": "",
                        "cor_fax": "",
                        "cor_tel": "",
                        "cor_mobile": "",
                        "cor_country": "",
                        "cor_desc": "",
                        "coowner_relationship": "",
                        "martial_status": "M",
                        "p_us_res_status": "N",
                        "p_vst_us_prev": "N",
                        "p_field9": "",
                        "p_field10": "",
                        "p_field11": "",
                        "p_field12": "",
                        "p_field13": "",
                        "p_field14": "",
                        "p_field15": "",
                        "p_field16": "",
                        "cif_info": {
                            "cif_auto": "Y",
                            "cif_num": ""
                        },
                        "id_info_main": {
                            "id_num": "187690394",
                            "id_issued_date": "2019-11-04",
                            "id_expired_date": "2023-11-04",
                            "id_issued_location": "HCM",
                            "id_type": "ID CARD/PASSPORT"
                        },
                        "address_info_i": {
                            "line": "P TRÚC BẠCH Q BA ĐÌNH TP HÀ NỘI",
                            "ward_name": "P TRÚC BẠCH",
                            "district_name": "Q BA ĐÌNH",
                            "city_name": "TP HÀ NỘI",
                            "country_name": "VN",
                            "same_addr": "Y"
                        },
                        "address_contact_info_i": {
                            "contact_address_line": "",
                            "contact_address_ward_name": "",
                            "contact_address_district_name": "",
                            "contact_address_city_name": "",
                            "contact_address_country_name": ""
                        },
                        "address_info_c": {
                            "line": "ABC",
                            "ward_name": "P PHÚC XÁ",
                            "district_name": "Q BA ĐÌNH",
                            "city_name": "TP HÀ NỘI",
                            "country_name": "VN",
                            "cor_same_addr ": "Y"
                        },
                        "address_contact_info_c": {
                            "contact_address_line": "P PHÚC XÁ",
                            "contact_address_ward_name": "P PHÚC XÁ",
                            "contact_address_district_name": "Q BA ĐÌNH",
                            "contact_address_city_name": "TP HÀ NỘI",
                            "contact_address_country_name": "VN"
                        },
                        "id_info_extra": {
                            "id_num": "",
                            "id_issued_date": "",
                            "id_expired_date": "",
                            "id_issued_location": "",
                            "id_type": ""
                        },
                        "branch_info": {
                            "branch_code": "000"
                        },
                        "job_info": {
                            "professional_code": "T_0806",
                            "position": "",
                            "official_telephone": "",
                            "address_office_info": {
                                "address_full": ""
                            }
                        },
                        "staff_info_checker": {
                            "staff_name": "HOANT2"
                        },
                        "staff_info_maker": {
                            "staff_name": "KHANHLQ"
                        },
                        "udf_info": {
                            "udf_name": "CN_00_CUNG_CAP_TT_FATCA~THU_NHAP_BQ_03_THANG~NGHE_NGHIEP~NHAN_SMS_EMAIL_TIEP_THI_QUANG_CAO~CUNG_CAP_DOANH_THU_THUAN~THOA_THUAN_PHAP_LY~KHTC_DOI_TUONG",
                            "udf_value": "CO~TNBQ_001~BAC_SI~DONG_Y~KHONG~KHONG~THONG THUONG"
                        }
                    },
                    "acccount_info": {
                        "account_class_code": "",
                        "account_auto_create_cif": "",
                        "account_currency": "",
                        "acc_auto": "",
                        "account_num": ""
                    }
                }
            }

        }

        print('request', request_data)
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF}"

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
