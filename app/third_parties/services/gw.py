import asyncio
import json
from datetime import date
from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.api.v1.endpoints.third_parties.gw.email.schema import (
    open_ebank_failure_response, open_ebank_success_response
)
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.utils.constant.debit_card import (
    GW_DEFAULT_CUSTOMER_EDUCATION, GW_DEFAULT_CUSTOMER_NATIONALITY,
    GW_DEFAULT_CUSTOMER_RESIDENT_STATUS, GW_DEFAULT_CUSTOMER_RESIDENT_TYPE,
    GW_DEFAULT_EMAIL, GW_DEFAULT_EMPLOYEE_DURATION, GW_DEFAULT_EMPLOYEE_SINCE,
    GW_DEFAULT_RESIDENT_SINCE, GW_DEFAULT_VISA_EXPIRE_DATE, GW_DEFAULT_ZERO,
    IDENTITY_DOCUMENT_TYPE_NEW_IC, IDENTITY_DOCUMENT_TYPE_PASSPORT,
    IDENTITY_DOCUMENT_TYPE_PASSPORT_CODE, MARITAL_STATUS_DISVORSED,
    MARITAL_STATUS_MARRIED, MARITAL_STATUS_OTHERS, MARITAL_STATUS_SINGLE,
    RESIDENT, GW_DEFAULT_apprvDeviation, GW_DEFAULT_casaAcctTyp,
    GW_DEFAULT_decsnStat, GW_DEFAULT_delivOpt, GW_DEFAULT_emerRelt,
    GW_DEFAULT_smsInfo, GW_DEFAULT_spcEmpWorkNat
)
from app.utils.constant.gw import (
    GW_AUTHORIZED_REF_DATA_MGM_ACC_NUM, GW_CO_OWNER_REF_DATA_MGM_ACC_NUM,
    GW_CURRENT_ACCOUNT_CASA, GW_CURRENT_ACCOUNT_FROM_CIF,
    GW_CUSTOMER_REF_DATA_MGMT_CIF_NUM, GW_DEFAULT_NO, GW_DEFAULT_VALUE,
    GW_DEFAULT_YES, GW_DEPOSIT_ACCOUNT_FROM_CIF, GW_DEPOSIT_ACCOUNT_TD,
    GW_EMPLOYEE_FROM_CODE, GW_EMPLOYEE_FROM_NAME, GW_EMPLOYEES,
    GW_ENDPOINT_URL_CHECK_EXITS_ACCOUNT_CASA,
    GW_ENDPOINT_URL_CHECK_USERNAME_IB_MB_EXIST,
    GW_ENDPOINT_URL_DEPOSIT_OPEN_ACCOUNT_TD,
    GW_ENDPOINT_URL_HISTORY_CHANGE_FIELD, GW_ENDPOINT_URL_INTERBANK_TRANSFER,
    GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_CARD_NUMBER,
    GW_ENDPOINT_URL_INTERNAL_TRANSFER, GW_ENDPOINT_URL_OPEN_CARDS,
    GW_ENDPOINT_URL_OPEN_INTERNET_BANKING, GW_ENDPOINT_URL_OPEN_MB,
    GW_ENDPOINT_URL_PAY_IN_CASH,
    GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_CARD_NUMBER,
    GW_ENDPOINT_URL_PAYMENT_AMOUNT_BLOCK,
    GW_ENDPOINT_URL_PAYMENT_AMOUNT_UNBLOCK, GW_ENDPOINT_URL_REDEEM_ACCOUNT,
    GW_ENDPOINT_URL_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA,
    GW_ENDPOINT_URL_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_CARD_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_CHANGE_STATUS_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_CLOSE_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD,
    GW_ENDPOINT_URL_RETRIEVE_DISCIPLINE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_EBANK_BY_CIF_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_LIST_FROM_ORG_ID,
    GW_ENDPOINT_URL_RETRIEVE_IB_INFO_BY_CIF,
    GW_ENDPOINT_URL_RETRIEVE_INTERNET_BANKING_BY_CIF_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_KPIS_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_MB_INFO_BY_CIF,
    GW_ENDPOINT_URL_RETRIEVE_OPEN_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REWARD_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_STAFF_OTHER_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_TELE_TRANSFER_INFO,
    GW_ENDPOINT_URL_RETRIEVE_TOPIC_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_WORKING_PROCESS_INFO_FROM_CODE,
    GW_ENDPOINT_URL_SELECT_ACCOUNT_TD_BY_MOBILE_NUM,
    GW_ENDPOINT_URL_SELECT_BRANCH_BY_BRANCH_ID,
    GW_ENDPOINT_URL_SELECT_BRANCH_BY_REGION_ID,
    GW_ENDPOINT_URL_SELECT_CARD_INFO, GW_ENDPOINT_URL_SELECT_CATEGORY,
    GW_ENDPOINT_URL_SELECT_DATA_FOR_CHART_DASHBOARD,
    GW_ENDPOINT_URL_SELECT_EMPLOYEE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA,
    GW_ENDPOINT_URL_SELECT_SERIAL_NUMBER,
    GW_ENDPOINT_URL_SELECT_SERVICE_PACK_IB,
    GW_ENDPOINT_URL_SELECT_STATISTIC_BANKING_BY_PERIOD,
    GW_ENDPOINT_URL_SELECT_SUMMARY_CARD_BY_DATE,
    GW_ENDPOINT_URL_SELECT_USER_INFO, GW_ENDPOINT_URL_SEND_EMAIL,
    GW_ENDPOINT_URL_SEND_SMS_VIA_EB_GW,
    GW_ENDPOINT_URL_SUMMARY_BP_TRANS_BY_INVOICE,
    GW_ENDPOINT_URL_SUMMARY_BP_TRANS_BY_SERVICE, GW_ENDPOINT_URL_TELE_TRANSFER,
    GW_ENDPOINT_URL_TT_LIQUIDATION, GW_ENDPOINT_URL_WITHDRAW,
    GW_FUNC_AMOUNT_BLOCK, GW_FUNC_AMOUNT_BLOCK_IN, GW_FUNC_AMOUNT_BLOCK_OUT,
    GW_FUNC_AMOUNT_UNBLOCK, GW_FUNC_AMOUNT_UNBLOCK_IN,
    GW_FUNC_AMOUNT_UNBLOCK_OUT, GW_FUNC_CASH_WITHDRAWS,
    GW_FUNC_CASH_WITHDRAWS_IN, GW_FUNC_CASH_WITHDRAWS_OUT,
    GW_FUNC_CHECK_USERNAME_IB_MB_EXIST, GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_IN,
    GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_OUT, GW_FUNC_INTERBANK_TRANSFER,
    GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM,
    GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM_IN,
    GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM_OUT,
    GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM,
    GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM_IN,
    GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM_OUT,
    GW_FUNC_INTERBANK_TRANSFER_IN, GW_FUNC_INTERBANK_TRANSFER_OUT,
    GW_FUNC_INTERNAL_TRANSFER, GW_FUNC_INTERNAL_TRANSFER_IN,
    GW_FUNC_INTERNAL_TRANSFER_OUT, GW_FUNC_OPEN_CARDS, GW_FUNC_OPEN_CARDS_IN,
    GW_FUNC_OPEN_CARDS_OUT, GW_FUNC_OPEN_MB, GW_FUNC_OPEN_MB_IN,
    GW_FUNC_OPEN_MB_OUT, GW_FUNC_PAY_IN_CARD,
    GW_FUNC_PAY_IN_CARD_247_BY_ACC_NUM, GW_FUNC_PAY_IN_CARD_247_BY_ACC_NUM_IN,
    GW_FUNC_PAY_IN_CARD_247_BY_ACC_NUM_OUT,
    GW_FUNC_PAY_IN_CARD_247_BY_CARD_NUM,
    GW_FUNC_PAY_IN_CARD_247_BY_CARD_NUM_IN,
    GW_FUNC_PAY_IN_CARD_247_BY_CARD_NUM_OUT, GW_FUNC_PAY_IN_CARD_IN,
    GW_FUNC_PAY_IN_CARD_OUT, GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA,
    GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA_IN,
    GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA_OUT,
    GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER,
    GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER_IN,
    GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER_OUT,
    GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE,
    GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_IN,
    GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT,
    GW_FUNC_RETRIEVE_IB_INFO_BY_CIF, GW_FUNC_RETRIEVE_IB_INFO_BY_CIF_IN,
    GW_FUNC_RETRIEVE_IB_INFO_BY_CIF_OUT, GW_FUNC_RETRIEVE_MB_INFO_BY_CIF,
    GW_FUNC_RETRIEVE_MB_INFO_BY_CIF_IN, GW_FUNC_RETRIEVE_MB_INFO_BY_CIF_OUT,
    GW_FUNC_RETRIEVE_SERIAL_NUMBER, GW_FUNC_RETRIEVE_SERIAL_NUMBER_IN,
    GW_FUNC_RETRIEVE_SERIAL_NUMBER_OUT,
    GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM,
    GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM_IN,
    GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM_OUT,
    GW_FUNC_SELECT_BRANCH_BY_BRANCH_ID, GW_FUNC_SELECT_BRANCH_BY_BRANCH_ID_IN,
    GW_FUNC_SELECT_BRANCH_BY_BRANCH_ID_OUT, GW_FUNC_SELECT_BRANCH_BY_REGION_ID,
    GW_FUNC_SELECT_BRANCH_BY_REGION_ID_IN,
    GW_FUNC_SELECT_BRANCH_BY_REGION_ID_OUT, GW_FUNC_SELECT_CARD_INFO,
    GW_FUNC_SELECT_CARD_INFO_IN, GW_FUNC_SELECT_CARD_INFO_OUT,
    GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE,
    GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE_IN,
    GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE_OUT,
    GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE,
    GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_IN,
    GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT,
    GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_USERNAME,
    GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_USERNAME_IN,
    GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_USERNAME_OUT,
    GW_FUNC_SELECT_EMPLOYEE_LIST_FROM_ORG_ID,
    GW_FUNC_SELECT_EMPLOYEE_LIST_FROM_ORG_ID_IN,
    GW_FUNC_SELECT_EMPLOYEE_LIST_FROM_ORG_ID_OUT,
    GW_FUNC_SELECT_KPIS_INFO_FROM_CODE, GW_FUNC_SELECT_KPIS_INFO_FROM_CODE_IN,
    GW_FUNC_SELECT_KPIS_INFO_FROM_CODE_OUT,
    GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA,
    GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA_IN,
    GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA_OUT,
    GW_FUNC_SELECT_REWARD_INFO_FROM_CODE,
    GW_FUNC_SELECT_REWARD_INFO_FROM_CODE_IN,
    GW_FUNC_SELECT_REWARD_INFO_FROM_CODE_OUT, GW_FUNC_SELECT_SERVICE_PACK_IB,
    GW_FUNC_SELECT_SERVICE_PACK_IB_IN, GW_FUNC_SELECT_SERVICE_PACK_IB_OUT,
    GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE,
    GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE_IN,
    GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE_OUT,
    GW_FUNC_SELECT_STATISTIC_BANKING_BY_PERIOD,
    GW_FUNC_SELECT_STATISTIC_BANKING_BY_PERIOD_IN,
    GW_FUNC_SELECT_STATISTIC_BANKING_BY_PERIOD_OUT,
    GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE,
    GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE_IN,
    GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE_OUT,
    GW_FUNC_SELECT_USER_INFO_BY_USER_ID,
    GW_FUNC_SELECT_USER_INFO_BY_USER_ID_IN,
    GW_FUNC_SELECT_USER_INFO_BY_USER_ID_OUT,
    GW_FUNC_SELECT_WORKING_PROCESS_INFO_FROM_CODE,
    GW_FUNC_SELECT_WORKING_PROCESS_INFO_FROM_CODE_IN,
    GW_FUNC_SELECT_WORKING_PROCESS_INFO_FROM_CODE_OUT, GW_FUNC_SEND_EMAIL,
    GW_FUNC_SEND_EMAIL_KEY, GW_FUNC_SEND_EMAIL_OUT, GW_FUNC_SEND_SMS_VIA_EB_GW,
    GW_FUNC_SEND_SMS_VIA_EB_GW_IN, GW_FUNC_SEND_SMS_VIA_EB_GW_OUT,
    GW_FUNC_SUMMARY_BP_TRANS_BY_INVOICE,
    GW_FUNC_SUMMARY_BP_TRANS_BY_INVOICE_IN,
    GW_FUNC_SUMMARY_BP_TRANS_BY_INVOICE_OUT,
    GW_FUNC_SUMMARY_BP_TRANS_BY_SERVICE,
    GW_FUNC_SUMMARY_BP_TRANS_BY_SERVICE_IN,
    GW_FUNC_SUMMARY_BP_TRANS_BY_SERVICE_OUT, GW_FUNC_TELE_TRANSFER,
    GW_FUNC_TELE_TRANSFER_IN, GW_FUNC_TELE_TRANSFER_OUT,
    GW_FUNC_TT_LIQUIDATION, GW_FUNC_TT_LIQUIDATION_IN,
    GW_FUNC_TT_LIQUIDATION_OUT, GW_FUNCTION_OPEN_CASA, GW_HISTORY_ACCOUNT_NUM,
    GW_HISTORY_CHANGE_FIELD_ACCOUNT, GW_RESPONSE_STATUS_SUCCESS,
    GW_RETRIEVE_CASA_ACCOUNT_DETAIL, GW_SELF_SELECTED_ACCOUNT_FLAG,
    GW_SELF_UNSELECTED_ACCOUNT_FLAG
)
from app.utils.email_templates.email_template import EMAIL_TEMPLATES
from app.utils.error_messages import ERROR_CALL_SERVICE_GW
from app.utils.functions import date_to_string, datetime_to_string, now


class ServiceGW:
    session: Optional[aiohttp.ClientSession] = None
    GW_EMAIL_DATA_INPUT__EMAIL_TO = None

    def __init__(self, init_service):
        self.email_templates = EMAIL_TEMPLATES
        self.url = init_service['gw']['url']
        self.GW_EMAIL_DATA_INPUT__EMAIL_TO = init_service['gw']['email']
        self.GW_SMS_MOBILE = init_service['gw']['sms_mobile']
        self.production = init_service['production']['production_flag']

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def call_api(self, api_url: str, request_data: json, output_key: str, service_name: str, is_form_data=False,
                       customers=None, is_open_ebank_success=False):
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
        response = None
        try:
            if not is_form_data:
                async with self.session.post(url=api_url, json=request_data) as response:
                    logger.log("SERVICE", f"[GW][{service_name}] {response.status} {api_url}")
                    if response.status != status.HTTP_200_OK:
                        if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                            return_error = await response.json()
                            return_data.update(
                                status=response.status,
                                errors=return_error['errors']
                            )
                        else:
                            return_data.update(status=response.status)
                        return False, return_data
                    else:
                        return_data = await response.json()
                        if return_data[output_key]['transaction_info']['transaction_error_code'] \
                                != GW_RESPONSE_STATUS_SUCCESS:
                            return False, return_data
                        return True, return_data
            else:
                form_data = aiohttp.FormData()
                if customers and is_open_ebank_success:
                    open_ebank_response = open_ebank_failure_response(
                        customers=customers,
                        email_templates=self.email_templates, template_key=GW_FUNC_SEND_EMAIL_KEY)
                    request_data['sendEmail_in.data_input.email_content_html'] = open_ebank_response.get('data')
                    request_data['sendEmail_in.data_input.email_subject'] = open_ebank_response.get('title')
                    if not self.production:
                        request_data['sendEmail_in.data_input.email_to'] = self.GW_EMAIL_DATA_INPUT__EMAIL_TO

                elif customers and not is_open_ebank_success:
                    open_ebank_response = open_ebank_success_response(
                        customers=customers,
                        email_templates=self.email_templates, template_key=GW_FUNC_SEND_EMAIL_KEY)
                    request_data['sendEmail_in.data_input.email_content_html'] = open_ebank_response.get('data')
                    request_data['sendEmail_in.data_input.email_subject'] = open_ebank_response.get('title')
                    if not self.production:
                        request_data['sendEmail_in.data_input.email_to'] = self.GW_EMAIL_DATA_INPUT__EMAIL_TO

                for key, value in request_data.items():
                    if key == "sendEmail_in.data_input.email_attachment_file" and value is not None:
                        for file in value:
                            form_data.add_field(name=key, value=await file.read(), filename=file.filename,
                                                content_type=file.content_type)
                    elif value:
                        if isinstance(value, list):
                            for item in value:
                                form_data.add_field(key, item)
                        else:
                            form_data.add_field(key, value)

                async with self.session.post(url=api_url, data=form_data) as response:
                    logger.log("SERVICE", f"[GW][{service_name}] {response.status} {api_url}")
                    if response.status != status.HTTP_200_OK:
                        if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                            return_error = await response.json()
                            return_data.update(
                                status=response.status,
                                errors=return_error['errors']
                            )
                        else:
                            return_data.update(status=response.status)
                        return False, return_data
                    else:
                        return_data = await response.json()
                        if return_data[output_key]['transaction_info']['transaction_error_code'] \
                                != GW_RESPONSE_STATUS_SUCCESS:
                            return False, return_data
                        return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data
        except asyncio.exceptions.TimeoutError as ex:
            logger.error(str(ex))
            return_error['errors'] = dict(
                loc="SERVICE GW",
                msg=ERROR_CALL_SERVICE_GW,
                detail="Time out"
            )
            return_data.update(
                status=response.status,
                errors=return_error['errors']
            )
        except Exception as ex:
            logger.error(str(ex))
            return_error = dict(
                loc="SERVICE GW",
                msg=ERROR_CALL_SERVICE_GW,
                detail=ex
            )

            return_data.update(
                status=response.status if not response else status.HTTP_400_BAD_REQUEST,
                errors=return_error.get('detail')
            )

        return False, return_data

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
                    return_data.update(status=response.status)
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
            cif_number,
            self_selected_account_flag: bool,
            casa_account_info,
            maker_staff_name
    ):
        """
        Mở tài khoản thanh toán
        """
        account_num = casa_account_info.casa_account_number if casa_account_info.casa_account_number else ''
        data_input = {
            "customer_info": {
                "cif_info": {
                    "cif_num": cif_number
                },
                "account_info": {
                    "acc_spl": GW_SELF_SELECTED_ACCOUNT_FLAG if self_selected_account_flag else GW_SELF_UNSELECTED_ACCOUNT_FLAG,
                    "account_num": account_num,
                    "account_currency": casa_account_info.currency_id,
                    "account_class_code": casa_account_info.acc_class_id,
                    "p_blk_cust_account": "",
                    "p_blk_provision_main": "",
                    "p_blk_provdetails": "",
                    "p_blk_report_gentime1": "",
                    "p_blk_accmaintinstr": "",
                    "p_blk_report_gentime2": "",
                    "p_blk_multi_account_generation": "",
                    "p_blk_account_generation": "",
                    "p_blk_interim_details": "",
                    "p_blk_accprdres": "",
                    "p_blk_acctxnres": "",
                    "p_blk_authbicdetails": "",
                    "p_blk_acstatuslines": "",
                    "p_blk_jointholders": "",
                    "p_blk_acccrdrlmts": "",
                    "p_blk_intdetails": "",
                    "p_blk_intprodmap": "",
                    "p_blk_inteffdtmap": "",
                    "p_blk_intsde": "",
                    "p_blk_tddetails": "",
                    "p_blk_amount_dates": "",
                    "p_blk_turnovers": "",
                    "p_blk_noticepref": "",
                    "p_blk_acc_nominees": "",
                    "p_blk_dcdmaster": "",
                    "p_blk_tdpayindetails": "",
                    "p_blk_tdpayoutdetails": "",
                    "p_blk_tod_renew": "",
                    "p_blk_od_limit": "",
                    "p_blk_doctype_checklist": "",
                    "p_blk_doctype_remarks": "",
                    "p_blk_sttms_od_coll_linkages": "",
                    "p_blk_cust_acc_check": "",
                    "p_blk_cust_acc_card": "",
                    "p_blk_intermediary": "",
                    "p_blk_summary": "",
                    "p_blk_accls_rollover": "",
                    "p_blk_promotions": "",
                    "p_blk_link_pricing": "",
                    "p_blk_linkedentities": "",
                    "p_blk_custacc_icccspcn": "",
                    "p_blk_custacc_icchspcn": "",
                    "p_blk_custacc_iccinstr": "",
                    "p_blk_custaccdet": "",
                    "p_blk_custacc_sicdiary": "",
                    "p_blk_custacc_stccusbl": "",
                    "p_blk_accclose": "",
                    "p_blk_acc_svcacsig": "",
                    "p_blk_sttms_debit": "",
                    "p_blk_tddetailsprn": "",
                    "p_blk_extsys_ws_master": "",
                    "p_blk_custacc_iccintpo": "",
                    "p_blk_sttms_cust_account": "",
                    "p_blk_customer_acc": "",
                    "p_blk_customer_accis": "",
                    "p_blk_master": "",
                    "p_blk_sttms_cust_acc_swp": "",
                    "p_blk_acc_chnl": ""
                },
                "staff_info_checker": {
                    "staff_name": current_user.username
                    # "staff_name": current_user.username
                },
                "staff_info_maker": {
                    "staff_name": maker_staff_name
                },
                "udf_info": {
                    "udf_json_array": []
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNCTION_OPEN_CASA, data_input=data_input
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
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    if return_data['openCASA_out']['transaction_info']['transaction_error_code'] \
                            != GW_RESPONSE_STATUS_SUCCESS:
                        return False, return_data, request_data

                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

    async def get_close_casa_account(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        """
        Đóng tài khoản thanh toán
        """

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="closeCASA_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CLOSE_CASA_ACCOUNT}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='closeCASA_out',
            service_name='CLOSE_CASA'
        )
        return response_data

    async def get_tele_transfer(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_TELE_TRANSFER_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_TELE_TRANSFER_INFO}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_TELE_TRANSFER_OUT,
            service_name=GW_FUNC_TELE_TRANSFER
        )
        return response_data

    async def get_ben_name_by_account_number(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveBenNameByAccNum_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_ACCOUNT_NUMBER}"

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

    async def get_ben_name_by_card_number(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveBenNameByCardNum_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_CARD_NUMBER}"

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

    async def change_status_account(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="accountChangeStatus_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CHANGE_STATUS_ACCOUNT_NUMBER}"

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
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

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
            cif_number: str
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_CIF": cif_number
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

    async def deposit_open_account_td(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="openTD_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_DEPOSIT_OPEN_ACCOUNT_TD}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='openTD_out',
            service_name='OPEN_TD'
        )
        return response_data

    ####################################################################################################################
    # END --- DEPOSIT TD
    ####################################################################################################################
    ####################################################################################################################
    # START --- RETRIEVE EBANK
    ####################################################################################################################
    async def get_retrieve_ebank_td(self, current_user: UserInfoResponse, cif_num):
        data_input = {
            "cif_info": {
                "cif_num": cif_num
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveEbankStatusByCif_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EBANK_BY_CIF_NUMBER}"

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
    # END --- RETRIEVE EBANK
    ####################################################################################################################
    ####################################################################################################################
    # START --- RETRIEVE RETRIEVE INTERNET BANKING
    ####################################################################################################################
    async def get_retrieve_internet_banking(self, current_user: UserInfoResponse, cif_num):
        data_input = {
            "cif_info": {
                "cif_num": cif_num
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveIBInfoByCif_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_INTERNET_BANKING_BY_CIF_NUMBER}"

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
    # END --- RETRIEVE INTERNET BANKING
    ####################################################################################################################
    ####################################################################################################################
    # START --- OPEN INTERNET BANKING
    ####################################################################################################################
    async def get_open_ib(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="openIB_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_OPEN_INTERNET_BANKING}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='openIB_out',
            service_name='openIB'
        )
        return response_data

    ####################################################################################################################
    # END --- OPEN INTERNET BANKING
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
            current_user=current_user, function_name=GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_EMPLOYEE_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE
        )
        return response_data

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
            current_user=current_user, function_name=GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_USERNAME_IN,
            data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_USERNAME_OUT,
            service_name=GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_USERNAME
        )
        return response_data

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
            current_user=current_user, function_name=GW_FUNC_SELECT_EMPLOYEE_LIST_FROM_ORG_ID_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_LIST_FROM_ORG_ID}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_EMPLOYEE_LIST_FROM_ORG_ID_OUT,
            service_name=GW_FUNC_SELECT_EMPLOYEE_LIST_FROM_ORG_ID
        )
        return response_data

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
            current_user=current_user, function_name=GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE
        )
        return response_data

    async def get_working_process_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_WORKING_PROCESS_INFO_FROM_CODE_IN,
            data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_WORKING_PROCESS_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_WORKING_PROCESS_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_SELECT_WORKING_PROCESS_INFO_FROM_CODE
        )
        return response_data

    async def get_reward_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
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
            current_user=current_user, function_name=GW_FUNC_SELECT_REWARD_INFO_FROM_CODE_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REWARD_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_REWARD_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_SELECT_REWARD_INFO_FROM_CODE
        )
        return response_data

    async def get_discipline_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
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
            current_user=current_user, function_name=GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_DISCIPLINE_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE
        )
        return response_data

    async def get_topic_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
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
            current_user=current_user, function_name=GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_TOPIC_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE
        )
        return response_data

    async def get_kpis_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": str(int(current_user.code))
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_KPIS_INFO_FROM_CODE_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_KPIS_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_KPIS_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_SELECT_KPIS_INFO_FROM_CODE
        )
        return response_data

    async def get_staff_other_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
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
            current_user=current_user, function_name=GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE_IN, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_STAFF_OTHER_INFO_FROM_CODE}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE_OUT,
            service_name=GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE
        )
        return response_data

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

        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_CATEGORY}"

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
                "transaction_name": GW_HISTORY_CHANGE_FIELD_ACCOUNT,
                "transaction_value": {
                    "account_num": GW_HISTORY_ACCOUNT_NUM
                }
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="historyChangeFieldAccount_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_HISTORY_CHANGE_FIELD}"

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
            data_input,
            current_user
    ):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="openCIFAuthorise_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='openCIFAuthorise_out',
            service_name='OPEN_CIF'
        )
        return response_data

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
                "data_input": data_input if len(data_input) != 0 else ""
            }
        }

    ####################################################################################################################
    # END --- UTILS
    ####################################################################################################################
    # START --- CHECK_EXIST_CASA_ACCOUNT_NUMBER
    ####################################################################################################################
    async def check_exist_casa_account_number(self, current_user: UserInfoResponse, casa_account_number):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_RETRIEVE_CASA_ACCOUNT_DETAIL,
                "transaction_value": {
                    "account_num": casa_account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveCurrentAccountCASA_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_CHECK_EXITS_ACCOUNT_CASA}"

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
    # END --- CHECK_EXIST_CASA_ACCOUNT_NUMBER
    ####################################################################################################################
    ####################################################################################################################
    # start --- withdraw
    ####################################################################################################################
    async def gw_withdraw(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_CASH_WITHDRAWS_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_WITHDRAW}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_CASH_WITHDRAWS_OUT,
            service_name=GW_FUNC_CASH_WITHDRAWS
        )
        return response_data

    ####################################################################################################################
    # end --- withdraw
    ####################################################################################################################

    ####################################################################################################################
    # start --- payment
    ####################################################################################################################

    async def gw_payment_amount_block(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_AMOUNT_BLOCK_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAYMENT_AMOUNT_BLOCK}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_AMOUNT_BLOCK_OUT,
            service_name=GW_FUNC_AMOUNT_BLOCK
        )
        return response_data

    async def gw_payment_amount_unblock(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_AMOUNT_UNBLOCK_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAYMENT_AMOUNT_UNBLOCK}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_AMOUNT_UNBLOCK_OUT,
            service_name=GW_FUNC_AMOUNT_UNBLOCK
        )
        return response_data

    async def gw_interbank_transfer(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_INTERBANK_TRANSFER_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_INTERBANK_TRANSFER_OUT,
            service_name=GW_FUNC_INTERBANK_TRANSFER
        )

        return response_data

    async def gw_payment_redeem_account(self, request_data):
        api_url = f"{self.url}{GW_ENDPOINT_URL_REDEEM_ACCOUNT}"

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
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
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

    async def gw_pay_in_cash(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_PAY_IN_CARD_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAY_IN_CASH}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_PAY_IN_CARD_OUT,
            service_name=GW_FUNC_PAY_IN_CARD
        )

    async def gw_pay_in_cash_247_by_acc_num(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_PAY_IN_CARD_247_BY_ACC_NUM_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_ACCOUNT_NUMBER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_PAY_IN_CARD_247_BY_ACC_NUM_OUT,
            service_name=GW_FUNC_PAY_IN_CARD_247_BY_ACC_NUM
        )

    async def gw_payment_internal_transfer(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_INTERNAL_TRANSFER_IN, data_input=data_input)
        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERNAL_TRANSFER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_INTERNAL_TRANSFER_OUT,
            service_name=GW_FUNC_INTERNAL_TRANSFER
        )

    async def gw_tele_transfer(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_TELE_TRANSFER_IN, data_input=data_input)

        api_url = f"{self.url}{GW_ENDPOINT_URL_TELE_TRANSFER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_TELE_TRANSFER_OUT,
            service_name=GW_FUNC_TELE_TRANSFER
        )

    async def gw_payment_tt_liquidation(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_TT_LIQUIDATION_IN, data_input=data_input)
        api_url = f"{self.url}{GW_ENDPOINT_URL_TT_LIQUIDATION}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_TT_LIQUIDATION_OUT,
            service_name=GW_FUNC_TT_LIQUIDATION
        )

    async def gw_payment_interbank_transfer(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_INTERBANK_TRANSFER_IN, data_input=data_input)

        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_INTERBANK_TRANSFER_OUT,
            service_name=GW_FUNC_INTERBANK_TRANSFER
        )

    async def gw_payment_interbank_transfer_247_by_account_number(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM_IN,
            data_input=data_input)
        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_ACCOUNT_NUMBER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM_OUT,
            service_name=GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM
        )

    async def gw_payment_interbank_transfer_247_by_card_number(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM_IN,
            data_input=data_input)

        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_CARD_NUMBER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM_OUT,
            service_name=GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM
        )

    async def gw_pay_in_cash_247_by_card_num(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_PAY_IN_CARD_247_BY_CARD_NUM_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_CARD_NUMBER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key=GW_FUNC_PAY_IN_CARD_247_BY_CARD_NUM_OUT,
            service_name=GW_FUNC_PAY_IN_CARD_247_BY_CARD_NUM
        )

    ####################################################################################################################
    # start --- user
    ####################################################################################################################
    async def gw_detail_user(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_USER_INFO_BY_USER_ID_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_USER_INFO}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_USER_INFO_BY_USER_ID_OUT,
            service_name=GW_FUNC_SELECT_USER_INFO_BY_USER_ID
        )
        return response_data

    ####################################################################################################################
    # START --- SERIAL
    ####################################################################################################################
    async def get_select_serial(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_RETRIEVE_SERIAL_NUMBER_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_SERIAL_NUMBER}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_RETRIEVE_SERIAL_NUMBER_OUT,
            service_name=GW_FUNC_RETRIEVE_SERIAL_NUMBER
        )
        return response_data

    ####################################################################################################################
    # Branch Location
    ####################################################################################################################
    async def select_branch_by_region_id(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_BRANCH_BY_REGION_ID_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_BRANCH_BY_REGION_ID}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_BRANCH_BY_REGION_ID_OUT,
            service_name=GW_FUNC_SELECT_BRANCH_BY_REGION_ID
        )
        return response_data

    async def select_branch_by_branch_id(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_BRANCH_BY_BRANCH_ID_IN, data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_BRANCH_BY_BRANCH_ID}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_BRANCH_BY_BRANCH_ID_OUT,
            service_name=GW_FUNC_SELECT_BRANCH_BY_BRANCH_ID
        )
        return response_data

    ####################################################################################################################

    ####################################################################################################################
    # Statistic
    ####################################################################################################################
    async def select_statistic_banking_by_period(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_STATISTIC_BANKING_BY_PERIOD_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_STATISTIC_BANKING_BY_PERIOD}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_STATISTIC_BANKING_BY_PERIOD_OUT,
            service_name=GW_FUNC_SELECT_STATISTIC_BANKING_BY_PERIOD
        )
        return response_data

    async def select_summary_card_by_date(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectSummaryCardsByDate_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_SUMMARY_CARD_BY_DATE}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='selectSummaryCardsByDate_out',
            service_name='selectSummaryCardsByDate'
        )
        return response_data

    async def select_data_for_chard_dashboard(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectDataForChartDashBoard_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_DATA_FOR_CHART_DASHBOARD}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='selectDataForChartDashBoard_out',
            service_name='selectDataForChartDashBoard'
        )
        return response_data

    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # EbankSms
    ####################################################################################################################
    async def select_mobile_number_sms_by_account_casa(self, current_user: UserInfoResponse, ebank_sms_indentify_num):
        data_input = {
            "ebank_sms_info":
                {
                    "ebank_sms_indentify_num": ebank_sms_indentify_num
                }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA_OUT,
            service_name=GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA
        )
        return response_data

    async def select_account_td_by_mobile_num(self, current_user: UserInfoResponse, ebank_sms_indentify_num):
        data_input = {
            "ebank_sms_info":
                {
                    "ebank_sms_indentify_num": ebank_sms_indentify_num
                }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_ACCOUNT_TD_BY_MOBILE_NUM}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM_OUT,
            service_name=GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM
        )
        return response_data

    async def register_sms_service_by_account_casa(self, current_user: UserInfoResponse,
                                                   account_info,
                                                   ebank_sms_info_list,
                                                   staff_info_checker,
                                                   staff_info_maker):
        data_input = {
            "account_info": account_info,
            "ebank_sms_info_list": ebank_sms_info_list,
            "staff_info_checker": staff_info_checker,
            "staff_info_maker": staff_info_maker,
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA_OUT,
            service_name=GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA
        )
        return response_data

    async def register_sms_service_by_mobile_number(self, current_user: UserInfoResponse,
                                                    account_info,
                                                    customer_info,
                                                    staff_info_checker,
                                                    staff_info_maker):
        data_input = {
            "account_info": account_info,
            "customer_info": customer_info,
            "staff_info_checker": staff_info_checker,
            "staff_info_maker": staff_info_maker,
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER_OUT,
            service_name=GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER
        )
        return response_data

    async def send_sms_via_eb_gw(self,
                                 current_user: UserInfoResponse,
                                 message,
                                 mobile=None):
        data_input = {
            "message": message,
            "mobile": self.GW_SMS_MOBILE if not self.production else mobile,
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SEND_SMS_VIA_EB_GW_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SEND_SMS_VIA_EB_GW}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SEND_SMS_VIA_EB_GW_OUT,
            service_name=GW_FUNC_SEND_SMS_VIA_EB_GW
        )
        return response_data

    ####################################################################################################################

    ####################################################################################################################
    # EbankIBMB
    ####################################################################################################################
    async def check_username_ib_mb_exist(self, current_user: UserInfoResponse, transaction_name, transaction_value):
        data_input = {
            "transaction_info":
                {
                    "transaction_name": transaction_name,
                    "transaction_value": transaction_value
                }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_CHECK_USERNAME_IB_MB_EXIST}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_OUT,
            service_name=GW_FUNC_CHECK_USERNAME_IB_MB_EXIST
        )
        return response_data

    async def retrieve_ib_info_by_cif(self, current_user: UserInfoResponse, cif_num):
        data_input = {
            "cif_info":
                {
                    "cif_num": cif_num
                }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_RETRIEVE_IB_INFO_BY_CIF_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_IB_INFO_BY_CIF}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_RETRIEVE_IB_INFO_BY_CIF_OUT,
            service_name=GW_FUNC_RETRIEVE_IB_INFO_BY_CIF
        )
        return response_data

    async def retrieve_mb_info_by_cif(self, current_user: UserInfoResponse, cif_num):
        data_input = {
            "cif_info":
                {
                    "cif_num": cif_num
                }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_RETRIEVE_MB_INFO_BY_CIF_IN,
            data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_MB_INFO_BY_CIF}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_RETRIEVE_MB_INFO_BY_CIF_OUT,
            service_name=GW_FUNC_RETRIEVE_MB_INFO_BY_CIF
        )
        return response_data

    async def summary_bp_trans_by_service(self, current_user: UserInfoResponse, cif_num, transaction_val_date,
                                          transaction_val_date_to_date):
        data_input = {
            "cif_info": {
                "cif_num": cif_num
            },
            "transaction_info": {
                "transaction_val_date": str(transaction_val_date),
                "transaction_val_date_to_date": str(transaction_val_date_to_date)
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SUMMARY_BP_TRANS_BY_SERVICE_IN,
            data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SUMMARY_BP_TRANS_BY_SERVICE}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SUMMARY_BP_TRANS_BY_SERVICE_OUT,
            service_name=GW_FUNC_SUMMARY_BP_TRANS_BY_SERVICE
        )
        return response_data

    async def summary_bp_trans_by_invoice(self, current_user: UserInfoResponse, cif_num, transaction_val_date,
                                          transaction_val_date_to_date):
        data_input = {
            "cif_info": {
                "cif_num": cif_num
            },
            "transaction_info": {
                "transaction_val_date": str(transaction_val_date),
                "transaction_val_date_to_date": str(transaction_val_date_to_date)
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SUMMARY_BP_TRANS_BY_INVOICE_IN,
            data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SUMMARY_BP_TRANS_BY_INVOICE}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SUMMARY_BP_TRANS_BY_INVOICE_OUT,
            service_name=GW_FUNC_SUMMARY_BP_TRANS_BY_INVOICE
        )
        return response_data

    async def open_mb(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_OPEN_MB_IN,
            data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_OPEN_MB}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_OPEN_MB_OUT,
            service_name=GW_FUNC_OPEN_MB
        )
        return response_data

    async def select_service_pack_ib(self, current_user: UserInfoResponse):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_SERVICE_PACK_IB_IN,
            data_input={}
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_SERVICE_PACK_IB}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_SERVICE_PACK_IB_OUT,
            service_name=GW_FUNC_SELECT_SERVICE_PACK_IB
        )
        return response_data

    ####################################################################################################################
    # Email
    ####################################################################################################################

    async def send_email(self,
                         current_user: UserInfoResponse,
                         product_code,
                         list_email_to,
                         list_email_cc,
                         list_email_bcc,
                         email_subject,
                         email_content_html,
                         list_email_attachment_file,
                         email_template=None,
                         customers=None,
                         is_open_ebank_success=False
                         ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SEND_EMAIL,
            data_input={}
        ).get(GW_FUNC_SEND_EMAIL, {}).get('transaction_info', {})

        return await self.call_api(
            request_data={
                'sendEmail_in.transaction_info.client_code': request_data.get('client_code'),
                'sendEmail_in.transaction_info.client_ref_num': request_data.get('client_ref_num'),
                'sendEmail_in.transaction_info.client_ip': request_data.get('client_ip'),
                'sendEmail_in.transaction_info.server_ref_num': request_data.get('server_ref_num'),
                'sendEmail_in.transaction_info.branch_info.branch_name':
                    request_data.get('branch_info', {}).get('branch_name'),
                'sendEmail_in.transaction_info.branch_info.branch_code': request_data.get('branch_info',
                                                                                          {}).get('branch_code'),
                'sendEmail_in.data_input.product_code': product_code,
                'sendEmail_in.data_input.email_to': list_email_to,
                'sendEmail_in.data_input.email_cc': list_email_cc,
                'sendEmail_in.data_input.email_bcc': list_email_bcc,
                'sendEmail_in.data_input.email_subject': email_subject,
                'sendEmail_in.data_input.email_content_html': email_content_html
                if not email_template else email_template,
                'sendEmail_in.data_input.email_attachment_file': list_email_attachment_file,
            },
            api_url=f"{self.url}{GW_ENDPOINT_URL_SEND_EMAIL}",
            output_key=GW_FUNC_SEND_EMAIL_OUT,
            service_name=GW_FUNC_SEND_EMAIL,
            is_form_data=True,
            customers=customers,
            is_open_ebank_success=is_open_ebank_success
        )

    ###################################################################################################################
    # CardWorks
    ###################################################################################################################
    async def open_cards(self, current_user: UserInfoResponse,
                         cif_number: str,
                         casa_account_number: str,
                         card_info,
                         customer_info,
                         maker_staff_name: str,
                         direct_staff: str,
                         indirect_staff: str,
                         casa_currency_number: str
                         ):

        # mapping các field đúng với Card core
        # tình trạng hôn nhân
        marital_status = customer_info.CustomerIndividualInfo.marital_status_id
        if marital_status not in [MARITAL_STATUS_SINGLE, MARITAL_STATUS_MARRIED, MARITAL_STATUS_DISVORSED]:
            marital_status = MARITAL_STATUS_OTHERS

        # thẻ định danh
        if customer_info.CustomerIdentity.identity_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT_CODE:
            identity_code = IDENTITY_DOCUMENT_TYPE_PASSPORT
        else:
            identity_code = IDENTITY_DOCUMENT_TYPE_NEW_IC

        # đinh cư hay chưa
        if customer_info.CustomerIndividualInfo.resident_status_id == RESIDENT:
            resident_pr_stat = GW_DEFAULT_YES
        else:
            resident_pr_stat = GW_DEFAULT_NO

        data_input = {
            "sequenceNo": datetime_to_string(now(), _format="%Y%m%d%H%M%S%f")[:-4],
            "fi": "970429",
            "srcSystm": "CRM",
            "cif_info": {
                "cif_num": cif_number
            },
            "account_info": {
                "account_type": card_info["account_type"]
            },
            "card_info": {
                "card_indicator": card_info["card_indicator"],
                "card_type": card_info["card_type"],
                "card_auto_renew": card_info["card_auto_renew"],
                "card_release_form": card_info["card_release_form"],
                "card_block_online_trans": card_info["card_block_online_trans"],
                "card_contact_less": card_info["card_contact_less"],
                "card_relation_to_primany": card_info["card_relation_to_primany"],
                "card_mother_name": card_info["card_mother_name"],
                "card_secure_question": card_info["card_secure_question"],
                "card_bill_option": card_info["card_bill_option"],
                "card_statement_delivery_option": card_info["card_statement_delivery_option"]
            },
            "prinCrdNo": GW_DEFAULT_VALUE,
            "customer_info": {
                "birthday": datetime_to_string(customer_info.CustomerIndividualInfo.date_of_birth, _format="%Y-%m-%d"),
                "title": card_info["title"],
                "full_name_vn": customer_info.Customer.full_name_vn,
                "last_name": customer_info.Customer.last_name,
                "first_name": customer_info.Customer.first_name,
                "middle_name": customer_info.Customer.middle_name,
                "current_official": GW_DEFAULT_VALUE,
                "embPhoto": GW_DEFAULT_VALUE,
                "gender": customer_info.CustomerIndividualInfo.gender_id,
                # @TODO: hard nationality, resident_status, customer_type
                "nationality": GW_DEFAULT_CUSTOMER_NATIONALITY,
                "martial_status": marital_status,
                "resident_status": GW_DEFAULT_CUSTOMER_RESIDENT_STATUS,
                "mthToStay": GW_DEFAULT_ZERO,
                "prStat": resident_pr_stat,
                "vsExpDate": GW_DEFAULT_VISA_EXPIRE_DATE,
                "education": GW_DEFAULT_CUSTOMER_EDUCATION,
                "customer_type": card_info["card_customer_type"]
            },
            "id_info": {
                "id_name": identity_code,
                "id_num": customer_info.CustomerIdentity.identity_num,
                "id_num_by_cif": GW_DEFAULT_VALUE,
                "id_issued_location": customer_info.CustomerIdentity.place_of_issue_id,
                "id_issued_date": datetime_to_string(customer_info.CustomerIdentity.issued_date, _format="%Y-%m-%d"),
            },
            "srcCde": card_info["srcCde"],
            "promoCde": card_info["promoCde"],
            "branch_issued": {
                "branhch_code": current_user.hrm_branch_code
            },
            "direct_staff": {
                "staff_code": direct_staff
            },
            "indirect_staff": {
                "staff_code": indirect_staff
            },
            "imgId": GW_DEFAULT_VALUE,
            "contract_info": {
                "contract_name": GW_DEFAULT_VALUE
            },
            "resident_info": {
                "address_info": {
                    "line": customer_info.CustomerAddress.address,
                    "ward_name": customer_info.AddressWard.name,
                    "contact_address_line": GW_DEFAULT_VALUE,
                    "city_code": customer_info.AddressProvince.id,
                    "district_name": customer_info.AddressDistrict.name,
                    "city_name": customer_info.CustomerAddress.address,
                    "country_name": customer_info.AddressCountry.id,
                    "telephone1": customer_info.Customer.telephone_number
                },
                # @TODO: resident_type tạm hard Local
                "customer_info": {
                    "resident_type": GW_DEFAULT_CUSTOMER_RESIDENT_TYPE,
                    "resident_since": GW_DEFAULT_RESIDENT_SINCE
                }
            },
            # @TODO: hard code địa chỉ nhận sao kê là địa chỉ KH luôn
            "correspondence_info": {
                "address_info": {
                    "line": customer_info.CustomerAddress.address,
                    "ward_name": customer_info.AddressWard.name,
                    "contact_address_line": GW_DEFAULT_VALUE,
                    "city_code": customer_info.AddressProvince.id,
                    "district_name": customer_info.AddressDistrict.name,
                    "city_name": customer_info.CustomerAddress.address,
                    "country_name": customer_info.AddressCountry.id,
                    "telephone1": customer_info.Customer.telephone_number,
                    "mobile_phone": customer_info.Customer.mobile_number
                },
                "smsInd": GW_DEFAULT_NO,
                "email": GW_DEFAULT_EMAIL
            },
            "office_info": {
                "customer_info": {
                    "biz_line": GW_DEFAULT_VALUE,
                    "employee_nature": GW_DEFAULT_VALUE,
                    "cor_capital": GW_DEFAULT_VALUE,
                    "biz_position": GW_DEFAULT_VALUE,
                    "employee_since": GW_DEFAULT_EMPLOYEE_SINCE,
                    "office_name": GW_DEFAULT_VALUE
                },
                "address_info": {
                    "line": GW_DEFAULT_VALUE,
                    "ward_name": GW_DEFAULT_VALUE,
                    "contact_address_line": GW_DEFAULT_VALUE,
                    "city_code": GW_DEFAULT_VALUE,
                    "district_name": GW_DEFAULT_VALUE,
                    "city_name": GW_DEFAULT_VALUE,
                    "country_name": GW_DEFAULT_VALUE,
                    "telephone1": GW_DEFAULT_VALUE,
                    "phone_ext1": GW_DEFAULT_VALUE,
                    "telephone2": GW_DEFAULT_VALUE,
                    "phone_ext2": GW_DEFAULT_VALUE,
                    "fax_no": GW_DEFAULT_VALUE
                }
            },
            "previous_employer_info": {
                "customer_info": {
                    "office_name": GW_DEFAULT_VALUE,
                    "employee_since": GW_DEFAULT_EMPLOYEE_SINCE,
                    "employee_duration": GW_DEFAULT_EMPLOYEE_DURATION
                },
                "address_info": {
                    "line": GW_DEFAULT_VALUE,
                    "ward_name": GW_DEFAULT_VALUE,
                    "contact_address_line": GW_DEFAULT_VALUE,
                    "city_code": GW_DEFAULT_VALUE,
                    "district_name": GW_DEFAULT_VALUE,
                    "city_name": GW_DEFAULT_VALUE,
                    "country_name": GW_DEFAULT_VALUE,
                    "telephone1": GW_DEFAULT_VALUE,
                    "phone_ext1": GW_DEFAULT_VALUE
                }
            },
            "personal_details": {
                "ownHouseLand": GW_DEFAULT_NO,
                "ownCar": GW_DEFAULT_NO,
                "noOfDepen": GW_DEFAULT_ZERO,
                "avgSpendMth": GW_DEFAULT_ZERO,
                "bankPrd": GW_DEFAULT_VALUE,
                "bankOthrPrd": GW_DEFAULT_VALUE,
                "othrCCBankName": GW_DEFAULT_VALUE,
                "othrCCLimit": GW_DEFAULT_VALUE,
                "othrLoanBankName": GW_DEFAULT_VALUE,
                "othrLoanInstallMth": GW_DEFAULT_VALUE,
                "delivByBrchInd": card_info["delivByBrchInd"],
                "delivOpt": GW_DEFAULT_delivOpt
            },
            "delivery_info": {
                "address_info": {
                    "line": card_info["address_info_line"] if card_info["address_info_line"] else "",
                    "ward_name": card_info["address_info_ward_name"] if card_info["address_info_ward_name"] else "",
                    "contact_address_line": GW_DEFAULT_VALUE,
                    "city_code": GW_DEFAULT_VALUE,
                    "district_name": card_info["address_info_district_name"] if card_info["address_info_district_name"] else "",
                    "city_name": card_info["address_info_city_name"] if card_info["address_info_city_name"] else "",
                    "country_name": GW_DEFAULT_VALUE
                },
                "delivBrchId": card_info["delivBrchId"]
            },
            "spouse_company_info": {
                "spcName": GW_DEFAULT_VALUE,
                "spcIdInd": GW_DEFAULT_VALUE,
                "spcNewId": GW_DEFAULT_VALUE,
                "spcEmpName": GW_DEFAULT_VALUE,
                "address_info": {
                    "line": GW_DEFAULT_VALUE,
                    "ward_name": GW_DEFAULT_VALUE,
                    "contact_address_line": GW_DEFAULT_VALUE,
                    "city_code": GW_DEFAULT_VALUE,
                    "district_name": GW_DEFAULT_VALUE,
                    "city_name": GW_DEFAULT_VALUE,
                    "country_name": GW_DEFAULT_VALUE,
                    "telephone1": GW_DEFAULT_VALUE,
                    "phone_ext1": GW_DEFAULT_VALUE
                },
                "spcEmpPosi": GW_DEFAULT_VALUE,
                "spcEmpSince": GW_DEFAULT_EMPLOYEE_SINCE,
                "spcEmpWorkNat": GW_DEFAULT_spcEmpWorkNat
            },
            "emergency_info": {
                "emerContcPrsn": customer_info.Customer.full_name_vn,
                "emerGender": customer_info.CustomerIndividualInfo.gender_id,
                "emerPhoneNo": customer_info.Customer.telephone_number,
                "emerMobileNo": customer_info.Customer.mobile_number,
                "emerRelt": GW_DEFAULT_emerRelt
            },
            "card_addon_data": {
                "payMeth": GW_DEFAULT_ZERO,
                "payCASA": GW_DEFAULT_ZERO,
                "payAmt": GW_DEFAULT_ZERO,
                "casaAcctNo": casa_account_number,
                "casaAcctTyp": GW_DEFAULT_casaAcctTyp,
                "casaCurCde": casa_currency_number,
                "recomCrdNo": GW_DEFAULT_VALUE,
                "recomName": GW_DEFAULT_VALUE,
                "remark": GW_DEFAULT_VALUE,
                "apprvDeviation": GW_DEFAULT_apprvDeviation,
                "addData1": GW_DEFAULT_VALUE,
                "addData2": GW_DEFAULT_VALUE,
                "smsInfo": GW_DEFAULT_smsInfo,
                "narrative": "CRM WS",
                "attachment": GW_DEFAULT_VALUE,
                "decsnStat": GW_DEFAULT_decsnStat
            },
            "checker_info": {
                "staff_code": current_user.username
            },
            # @TODO: chưa có approver
            "approver_info": {
                "staff_code": current_user.username
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_OPEN_CARDS_IN,
            data_input=data_input
        )

        response_data = await self.call_api(
            request_data=request_data,
            api_url=f"{self.url}{GW_ENDPOINT_URL_OPEN_CARDS}",
            output_key=GW_FUNC_OPEN_CARDS_OUT,
            service_name=GW_FUNC_OPEN_CARDS
        )

        return response_data

    async def select_card_info(self, current_user: UserInfoResponse,
                               card_branched):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNC_SELECT_CARD_INFO_IN,
            data_input={
                "card_branched": card_branched
            }
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_CARD_INFO}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key=GW_FUNC_SELECT_CARD_INFO_OUT,
            service_name=GW_FUNC_SELECT_CARD_INFO
        )
        return response_data

########################################################################################################################
