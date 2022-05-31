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
    GW_EMPLOYEES, GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD,
    GW_ENDPOINT_URL_RETRIEVE_DISCIPLINE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_LIST_FROM_ORG_ID,
    GW_ENDPOINT_URL_RETRIEVE_KPIS_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_OPEN_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REWARD_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_STAFF_OTHER_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_TOPIC_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_WORKING_PROCESS_INFO_FROM_CODE,
    GW_ENDPOINT_URL_SELECT_EMPLOYEE_INFO_FROM_CODE,
    GW_HISTORY_CHANGE_FIELD_ACCOUNT, GW_HISTOTY_ACOUNT_NUM,
    GW_HISTOTY_CHANGE_FIELD_ACCOUNT, GW_SELECT_CATEGORY
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

    ####################################################################################################################
    # START --- CASA
    ####################################################################################################################

    async def get_casa_account_from_cif(self, current_user: UserInfoResponse, casa_cif_number: str):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_CURRENT_ACCOUNT_FROM_CIF,
                "transaction_value": {
                    "cif_num": casa_cif_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCurrentAccountFromCIF_in", data_input=data_input
        )

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
        data_input = {
            "transaction_info": {
                "transaction_name": GW_CURRENT_ACCOUNT_CASA,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveCurrentAccountCASA_in", data_input=data_input
        )

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
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number,
                    "P_FDATE": date_to_string(from_date),
                    "P_TDATE": date_to_string(to_date)
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportHisCaSaFromAcc_in", data_input=data_input
        )

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
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number,
                    "P_FDATE": date_to_string(from_date),
                    "P_TDATE": date_to_string(to_date)
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportStatementCaSaFromAcc_in", data_input=data_input
        )

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

    async def get_report_casa_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
    ):
        """
        Lấy thông tin biểu đồ hình tròn
        """
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportCaSaFromAcc_in", data_input=data_input
        )

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

    async def get_open_casa_account(
            self,
            current_user: UserInfoResponse,
            cif_info,
            account_info,
            staff_info_checker,
            staff_info_maker,
            udf_info

    ):
        """
        Mở tài khoản thanh toán
        """
        data_input = {
            "customer_info": {
                "cif_info": {
                    "cif_num": cif_info.cif_num
                },
                "account_info": {
                    "acc_spl": account_info.acc_spl,
                    "account_num": account_info.account_num,
                    "account_currency": account_info.account_currency,
                    "account_class_code": account_info.account_class_code,
                },
                "staff_info_checker": {
                    "staff_name": staff_info_checker.staff_name
                },
                "staff_info_maker": {
                    "staff_name": staff_info_maker.staff_name
                },
                "udf_info": {
                    "udf_json_array": [
                        {
                            "UDF_NAME": item.UDF_NAME,
                            "UDF_VALUE": item.UDF_VALUE
                        }
                        for item in udf_info.udf_json_array]
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="openCASA_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_OPEN_CASA_ACCOUNT}"

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

    ####################################################################################################################
    # END --- CASA
    ####################################################################################################################

    ####################################################################################################################
    # START --- DEPOSIT TD
    ####################################################################################################################
    async def get_report_statement_td_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
            from_date: date,
            to_date: date
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number,
                    "P_FDATE": date_to_string(from_date),
                    "P_TDATE": date_to_string(to_date)
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportStatementTDFromAcc_in", data_input=data_input
        )

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

    async def select_report_td_from_cif_data_input(
            self,
            current_user: UserInfoResponse,
            transaction_name: str,
            endpoint: str,
            account_number: str,
            from_date: Optional[date],
            to_date: Optional[date]
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number,
                    "P_FDATE": date_to_string(from_date),
                    "P_TDATE": date_to_string(to_date)
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportTDFromCif_in", data_input=data_input
        )

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

    async def get_deposit_account_from_cif(self, current_user: UserInfoResponse, account_cif_number):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_DEPOSIT_ACCOUNT_FROM_CIF,
                "transaction_value": {
                    "cif_num": account_cif_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectDepositAccountFromCIF_in", data_input=data_input
        )

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
        data_input = {
            "transaction_info": {
                "transaction_name": GW_DEPOSIT_ACCOUNT_TD,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveDepositAccountTD_in", data_input=data_input
        )

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

    ####################################################################################################################
    # END --- DEPOSIT TD
    ####################################################################################################################

    ####################################################################################################################
    # START --- CUSTOMER
    ####################################################################################################################

    async def get_customer_info_list(
            self,
            current_user: UserInfoResponse,
            cif_number: str,
            identity_number: str,
            mobile_number: str,
            full_name: str
    ):
        data_input = {
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
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCustomerRefDataMgmtCIFNum_in", data_input=data_input
        )

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
        data_input = {
            "transaction_info": {
                "transaction_name": "CustFromCIF",
                "transaction_value": {
                    "cif_num": customer_cif_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveCustomerRefDataMgmt_in", data_input=data_input
        )

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
        data_input = {
            "transaction_info": {
                "transaction_name": GW_CO_OWNER_REF_DATA_MGM_ACC_NUM,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCoownerRefDataMgmtAccNum_in", data_input=data_input
        )

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
        data_input = {
            "transaction_info": {
                "transaction_name": GW_AUTHORIZED_REF_DATA_MGM_ACC_NUM,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectAuthorizedRefDataMgmtAccNum_in", data_input=data_input
        )

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

    ####################################################################################################################
    # END --- CUSTOMER
    ####################################################################################################################

    ####################################################################################################################
    # START --- EMPLOYEE
    ####################################################################################################################
    async def get_employee_info_from_code(self, current_user: UserInfoResponse, employee_code):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_EMPLOYEE_FROM_CODE,
                "transaction_value": {
                    "employee_code": employee_code
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectEmployeeInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_EMPLOYEE_INFO_FROM_CODE}"

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
        data_input = {
            "transaction_info": {
                "transaction_name": GW_EMPLOYEE_FROM_NAME,
                "transaction_value": {
                    "employee_name": employee_name
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectEmployeeInfoFromUserName_in", data_input=data_input
        )

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

    async def get_employee_list_from_org_id(self, current_user: UserInfoResponse, org_id):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_EMPLOYEES,
                "transaction_value": {
                    "org_id": org_id
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectEmployeeListFromOrgId_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_LIST_FROM_ORG_ID}"

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

    async def get_retrieve_employee_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code,
                "staff_type": "CHI_TIET",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveEmployeeInfoFromCode_in", data_input=data_input
        )

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

    async def get_working_process_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectWorkingProcessInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_WORKING_PROCESS_INFO_FROM_CODE}"

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

    async def get_reward_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code,
                "staff_type": "KHEN_THUONG",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectRewardInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REWARD_INFO_FROM_CODE}"

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

    async def get_discipline_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code,
                "staff_type": "KY_LUAT",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectDisciplineInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_DISCIPLINE_INFO_FROM_CODE}"

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

    async def get_topic_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code,
                "staff_type": "DAO_TAO_NOI_BO",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectTopicInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_TOPIC_INFO_FROM_CODE}"

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

    async def get_kpis_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectKpisInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_KPIS_INFO_FROM_CODE}"

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

    async def get_staff_other_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code,
                "staff_type": "OTHER_INFO",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectStaffOtherInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_STAFF_OTHER_INFO_FROM_CODE}"

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
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "id": id
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=function_name, data_input=data_input
        )

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

    ####################################################################################################################
    # END --- EMPLOYEE
    ####################################################################################################################

    ####################################################################################################################
    # START --- CATEGORY
    ####################################################################################################################
    async def get_select_category(self, current_user: UserInfoResponse, transaction_name: str, transaction_value: str):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": transaction_value
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCategory_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_SELECT_CATEGORY}"

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

    ####################################################################################################################
    # END --- CATEGORY
    ####################################################################################################################
    # START --- HISTORY
    ####################################################################################################################
    async def get_history_change_field(self, current_user: UserInfoResponse):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_HISTOTY_CHANGE_FIELD_ACCOUNT,
                "transaction_value": {
                    "account_num": GW_HISTOTY_ACOUNT_NUM
                }
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="historyChangeFieldAccount_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_HISTORY_CHANGE_FIELD_ACCOUNT}"

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

    ####################################################################################################################
    # END --- HISTORY
    ####################################################################################################################
    # START --- CIF
    ####################################################################################################################
    async def open_cif(
            self,
            cif_id: str,
            customer_info: dict,
            account_info: dict,
            current_user
    ):
        data_input = {
            "customer_info": customer_info,
            "account_info": account_info
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="openCIFAuthorise_in", data_input=data_input
        )

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
        except Exception as ex:
            logger.error(str(ex))
            return False, {'message': str(ex)}

    ####################################################################################################################
    # END --- CIF
    ####################################################################################################################

    ####################################################################################################################
    # START --- UTILS
    ####################################################################################################################
    @staticmethod
    def gw_create_request_body(current_user: UserInfoResponse, data_input: dict,
                               function_name: str):
        return {
            function_name: {
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
                "data_input": data_input
            }
        }
    ####################################################################################################################
    # END --- UTILS
    ####################################################################################################################
