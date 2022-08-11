from typing import Optional

from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.post_check.repository import (
    repos_create_post_check, repos_get_customer_detail,
    repos_get_history_post_post_check, repos_get_list_branch,
    repos_get_list_kss, repos_get_list_zone, repos_get_post_control,
    repos_get_statistics, repos_get_statistics_month,
    repos_get_statistics_profiles, repos_save_customer_ekyc,
    repos_update_post_check
)
from app.api.v1.endpoints.post_check.schema import (
    CreatePostCheckRequest, QueryParamsKSSRequest, UpdatePostCheckRequest
)
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_change_status_account, repos_gw_get_casa_account_info
)
from app.api.v1.endpoints.third_parties.gw.ebank_sms.repository import (
    repos_gw_send_sms_via_eb_gw
)
from app.api.v1.endpoints.third_parties.gw.email.repository import (
    repos_gw_send_email
)
from app.settings.config import DATE_INPUT_OUTPUT_FORMAT
from app.utils.constant.cif import (
    CRM_GENDER_TYPE_FEMALE, EKYC_DOCUMENT_TYPE_NEW_CITIZEN,
    EKYC_DOCUMENT_TYPE_OLD_CITIZEN, EKYC_DOCUMENT_TYPE_PASSPORT,
    EKYC_GENDER_TYPE_FEMALE, EKYC_GENDER_TYPE_MALE
)
from app.utils.constant.ekyc import (
    EKYC_DATE_FORMAT, EKYC_DEFAULT_VALUE, EKYC_REGION_ZONE_MAPPING,
    ERROR_CODE_FAILED_EKYC, ERROR_CODE_PROCESSING_EKYC, GROUP_ROLE_CODE_AP,
    GROUP_ROLE_CODE_AP_EX, GROUP_ROLE_CODE_IN, GROUP_ROLE_CODE_IN_EX,
    GROUP_ROLE_CODE_VIEW, GROUP_ROLE_CODE_VIEW_EX, MENU_CODE, MENU_CODE_VIEW,
    MESSAGE_EMAIL_SUBJECT, MESSAGE_SMS_INVALID, STATUS_CLOSE, STATUS_FAILED,
    STATUS_OPEN
)
from app.utils.error_messages import ERROR_PERMISSION, MESSAGE_STATUS
from app.utils.functions import (
    date_string_to_other_date_string_format, gen_qr_code
)


class CtrKSS(BaseController):

    async def ctr_get_list_kss(
        self,
        query_params: QueryParamsKSSRequest
    ):

        current_user = self.current_user
        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW
        )
        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST KSS',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN)

        # Map region to zone: Phía eKYC có danh mục Vùng khác với danh mục khu vực của GW
        # TODO: Hard theo danh sách vùng để map EKYC_REGION_ZONE_MAPPING
        try:
            zone_id = list(filter(lambda x: x['region_code'] == query_params.zone_id, EKYC_REGION_ZONE_MAPPING))[0]['zone_id']
        except IndexError:
            zone_id = None

        query_data = {}
        query_data.update({'cif_phone_number_gttt_name': query_params.cif_phone_number_gttt_name}) if query_params.cif_phone_number_gttt_name else None
        query_data.update({'transaction_id': query_params.transaction_id}) if query_params.transaction_id else None
        query_data.update({'tran_type_id': query_params.tran_type_id}) if query_params.tran_type_id else None
        query_data.update({'approve_status': query_params.approve_status}) if query_params.approve_status else None
        query_data.update({'branch_id': query_params.branch_id}) if query_params.branch_id else None
        query_data.update({'zone_id': zone_id}) if zone_id else None
        query_data.update(
            {
                'start_date': date_string_to_other_date_string_format(
                    query_params.start_date,
                    from_format=DATE_INPUT_OUTPUT_FORMAT,
                    to_format=EKYC_DATE_FORMAT
                )
            }
        ) if query_params.start_date else None
        query_data.update(
            {
                'end_date': date_string_to_other_date_string_format(
                    query_params.end_date,
                    from_format=DATE_INPUT_OUTPUT_FORMAT,
                    to_format=EKYC_DATE_FORMAT
                )
            }
        ) if query_params.end_date else None
        query_data.update({'page_num': query_params.page_num}) if query_params.page_num else None
        query_data.update({'record_per_page': query_params.record_per_page}) if query_params.record_per_page else None
        query_data.update({'step_status': query_params.step_status}) if query_params.step_status else None

        list_kss = self.call_repos(await repos_get_list_kss(query_data=query_data))

        return self.response(data=list_kss)

    async def ctr_get_list_branch(self, zone_id: int):

        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST BRANCH',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN)

        query_param = {
            'zone_id': zone_id
        } if zone_id else None

        list_branch = self.call_repos(await repos_get_list_branch(
            query_param=query_param
        ))

        branchs = [{
            'id': branch['zone_id'],
            'code': branch['code'],
            'name': branch['name']
        } for branch in list_branch]

        return self.response(data=branchs)

    async def ctr_get_list_zone(self):

        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST ZONE',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN)

        list_zone = self.call_repos(await repos_get_list_zone())

        return self.response(data=list_zone)

    async def ctr_get_post_control(
            self,
            postcheck_uuid: str,
            post_control_his_id: int
    ):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST GET POST CONTROL',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        query_params = {
            'customer_id': postcheck_uuid
        }
        query_params.update({'post_control_his_id': post_control_his_id}) if post_control_his_id else None
        post_control_response = self.call_repos(await repos_get_post_control(
            query_params=query_params
        ))
        # if post_control_response['kss_status'] == 'Hợp lệ' or post_control_response['kss_status'] == 'Cần xác minh':
        #     post_control_response['approve_status'] = None

        return self.response(data=post_control_response)

    async def ctr_history_post_check(self, postcheck_uuid: str):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST GET POST CONTROL',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        history_post_check = self.call_repos(await repos_get_history_post_post_check(
            postcheck_uuid=postcheck_uuid
        ))

        # response_datas = []
        # for history in history_post_check:
        #     if (
        #             history['kss_status_old'] == 'Chờ hậu kiểm'
        #             and (history['kss_status'] == 'Hợp lệ' or history['kss_status'] == 'Cần xác minh')
        #     ):
        #         history['approve_status'] = history['approve_user'] = None
        #     response_datas.append(history)

        return self.response(data=history_post_check)

    async def ctr_statistics_month(self, months: int):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST GET POST CONTROL',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        statistics_months = self.call_repos(await repos_get_statistics_month(months=months))

        return self.response(statistics_months)

    async def ctr_get_statistics_profiles(
            self,
            selected_date,
            start_date,
            end_date
    ):
        current_user = self.current_user
        query_data = {}
        query_data.update(
            {
                'start_date': date_string_to_other_date_string_format(
                    start_date,
                    from_format=DATE_INPUT_OUTPUT_FORMAT,
                    to_format=EKYC_DATE_FORMAT
                )
            }
        ) if start_date else None
        query_data.update(
            {
                'selected_date': date_string_to_other_date_string_format(
                    selected_date,
                    from_format=DATE_INPUT_OUTPUT_FORMAT,
                    to_format=EKYC_DATE_FORMAT
                )
            }
        ) if selected_date else None
        query_data.update(
            {
                'end_date': date_string_to_other_date_string_format(
                    end_date,
                    from_format=DATE_INPUT_OUTPUT_FORMAT,
                    to_format=EKYC_DATE_FORMAT
                )
            }
        ) if end_date else None
        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST GET POST CONTROL',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        statistics_profiles = self.call_repos(await repos_get_statistics_profiles(query_data=query_data))

        return self.response(data=statistics_profiles)

    async def ctr_get_statistics(self, search_type: int, selected_date: str):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST GET POST CONTROL',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        query_param = {}

        query_param.update({'search_type': search_type}) if search_type else None
        query_param.update({'selected_date': selected_date}) if selected_date else None

        statistics = self.call_repos(await repos_get_statistics(query_param=query_param))

        return self.response(data=statistics)

    async def ctr_create_post_check(self, post_check_request: CreatePostCheckRequest):
        current_user = self.current_user
        # role nhập
        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE_VIEW,
            group_role_code_ex=GROUP_ROLE_CODE_IN_EX,
            group_role_code=GROUP_ROLE_CODE_IN)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='CREATE_POST_CHECK',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        post_control_request = [{
            "check_list_id": post_control.check_list_id,
            "check_list_desc": post_control.check_list_desc,
            "answer": post_control.answer,
            "note": post_control.note if post_control.note else EKYC_DEFAULT_VALUE
        } for post_control in post_check_request.post_control]

        payload_data = {
            "customer_id": post_check_request.customer_id,
            "kss_status": post_check_request.kss_status,
            "username": post_check_request.username,
            "post_control": post_control_request
        }

        post_check_response = self.call_repos(await repos_create_post_check(payload_data=payload_data))

        return self.response(data=post_check_response)

    async def ctr_update_post_check(
            self,
            postcheck_update_request: UpdatePostCheckRequest
    ):

        current_user = self.current_user
        # role duyệt
        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE_VIEW,
            group_role_code_ex=GROUP_ROLE_CODE_AP_EX,
            group_role_code=GROUP_ROLE_CODE_AP)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='UPDATE POST CHECK',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        request_data = {
            "customer_id": postcheck_update_request.customer_id,
            "history_post_control_id": postcheck_update_request.history_post_control_id,
            "username": postcheck_update_request.username,
            "is_approve": postcheck_update_request.is_approve
        }

        update_post_check = self.call_repos(await repos_update_post_check(
            request_data=request_data
        ))
        # lấy lịch sử trạng thái hậu kiểm cuối cùng
        history_status = self.call_repos(await repos_get_history_post_post_check(
            postcheck_uuid=postcheck_update_request.customer_id
        ))
        customer_detail = self.call_repos(await repos_get_customer_detail(
            postcheck_uuid=postcheck_update_request.customer_id
        ))
        response_data = {
            "customer_id": update_post_check['customer_id'],
            'error_msg': None
        }
        if history_status:
            if history_status[-1]['kss_status'] == "Không hợp lệ" and history_status[-1]['approve_status'] == "Đã Duyệt":
                is_success_gw, account_number = self.call_repos(await repos_gw_change_status_account(  # noqa
                    current_user=current_user.user_info,
                    account_number=customer_detail.get('account_number')
                ))
                if not is_success_gw:
                    response_data['error_msg'] = str(account_number)

                self.call_repos(await repos_gw_send_email(
                    product_code='CRM',
                    list_email_to=customer_detail.get('extra_info').get('email'),
                    list_email_cc=None,
                    list_email_bcc=None,
                    email_subject=MESSAGE_EMAIL_SUBJECT,
                    email_content_html=None,
                    list_email_attachment_file=None,
                    current_user=current_user,
                    customers=customer_detail.get('full_name'),
                    is_open_ebank_success=True))

                # khóa tài khoản mới gửi email and sms
                self.call_repos(await repos_gw_send_sms_via_eb_gw(
                    message=MESSAGE_SMS_INVALID,
                    mobile=customer_detail['phone_number'],
                    current_user=current_user))

        return self.response(data=response_data)

    async def ctr_get_customer_detail(self, postcheck_uuid: str):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code_ex=GROUP_ROLE_CODE_VIEW_EX,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='CUSTOMER_DETAIL',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        customer_detail = self.call_repos(await repos_get_customer_detail(
            postcheck_uuid=postcheck_uuid
        ))

        national = customer_detail.get('nationality')

        for key, value in customer_detail.items():
            # reformat date from dd/mm/yyyy to yyyy-mm-dd
            if isinstance(value, str) and "/" in value and len(value) == 10:
                customer_detail[key] = date_string_to_other_date_string_format(value, '%d/%m/%Y', '%Y-%m-%d')

        if not national:
            customer_detail['nationality'] = 'Việt Nam'
        transaction_id = customer_detail.get('transaction_id')
        ekyc_step = []
        for item in customer_detail.get('ekyc_step'):
            if transaction_id == item.get('transaction_id'):
                ekyc_step.extend(item.get('info_step'))

        customer_detail.update({
            "error_code_ekyc": None,
            "ekyc_step": ekyc_step
        })

        account_number = customer_detail.get('account_number')
        if account_number:
            account_detail = self.call_repos(await repos_gw_get_casa_account_info(
                account_number=account_number,
                current_user=self.current_user.user_info
            ))
            account_status = account_detail['retrieveCurrentAccountCASA_out']['data_output']['customer_info']['account_info']['account_status']
            if account_status:
                for key, value in account_status[0].items():
                    if key == "AC_STAT_NO_DR":
                        if value == "N":
                            customer_detail.update(dict(
                                account_status=STATUS_OPEN
                            ))
                        else:
                            customer_detail.update(dict(
                                account_status=STATUS_CLOSE
                            ))
        if customer_detail['status'] == "Thất bại":
            customer_detail['ekyc_level'] = None

        if customer_detail['ekyc_step']:
            first_row = customer_detail['ekyc_step'][0]
            if STATUS_FAILED in first_row['step_status']:
                if customer_detail.get('status') == "REJECTED":
                    customer_detail['error_code_ekyc'] = ERROR_CODE_FAILED_EKYC[first_row['step']]
                if customer_detail.get('status') == "PROCESSING":
                    customer_detail['error_code_ekyc'] = ERROR_CODE_PROCESSING_EKYC[first_row['step']]

        return self.response(data=customer_detail)

    async def ctr_save_customer_ekyc(
            self,
            face_ids: int,
            ocr_result_ekyc_data: dict,
            gender: str,
            date_of_expiry: str,
            phone_number: str,
            front_image: Optional[str] = None,
            front_image_name: Optional[str] = None,
            back_image: Optional[str] = None,
            back_image_name: Optional[str] = None,
            avatar_image: Optional[str] = None,
            avatar_image_name: Optional[str] = None,
    ):

        gender = EKYC_GENDER_TYPE_FEMALE if gender == CRM_GENDER_TYPE_FEMALE else EKYC_GENDER_TYPE_MALE
        ocr_data = ocr_result_ekyc_data.get('data')

        if ocr_result_ekyc_data['document_type'] == EKYC_DOCUMENT_TYPE_PASSPORT:
            body = {
                "document_id": ocr_data.get('document_id'),
                "document_type": ocr_result_ekyc_data['document_type'],
                "date_of_issue": ocr_data.get('date_of_issue'),
                "place_of_issue": ocr_data.get('place_of_issue'),
                "full_name": ocr_data.get('full_name'),
                "date_of_birth": ocr_data.get('date_of_birth'),
                "place_of_origin": ocr_data.get('place_of_origin'),
                "date_of_expiry": ocr_data.get('date_of_expiry'),
                "gender": ocr_data.get('gender'),
                "phone_number": phone_number,
                "face_ids": [face_ids],
                "ocr_data": ocr_data,
                "attachment_info": {
                    'front_image': front_image,
                    "front_image_name": front_image_name,
                    "avatar_image": avatar_image,
                    "avatar_image_name": avatar_image_name
                }
            }
        else:
            body = {
                "document_id": ocr_data.get('document_id'),
                "document_type": ocr_result_ekyc_data['document_type'],
                "date_of_issue": ocr_data.get('date_of_issue'),
                "place_of_issue": ocr_data.get('place_of_issue'),
                "full_name": ocr_data.get('full_name'),
                "date_of_birth": ocr_data.get('date_of_birth'),
                "place_of_residence": ocr_data.get('place_of_residence'),
                "place_of_origin": ocr_data.get('place_of_origin'),
                "phone_number": phone_number,
                "face_ids": [face_ids],
                "ocr_data": ocr_data,
                "attachment_info": {
                    'front_image': front_image,
                    "front_image_name": front_image_name,
                    "back_image": back_image,
                    "back_image_name": back_image_name,
                    "avatar_image": avatar_image,
                    "avatar_image_name": avatar_image_name
                }
            }

            if ocr_result_ekyc_data['document_type'] == EKYC_DOCUMENT_TYPE_OLD_CITIZEN:
                body.update({
                    "date_of_expiry": ocr_data.get('date_of_expiry'),
                    "gender": ocr_data.get('gender'),
                })

            elif ocr_result_ekyc_data['document_type'] == EKYC_DOCUMENT_TYPE_NEW_CITIZEN:
                body.update({
                    "qr_code_data": gen_qr_code(ocr_data),
                    "date_of_expiry": ocr_data.get('date_of_expiry'),
                    "gender": ocr_data.get('gender'),
                })
            else:
                body.update({
                    "date_of_expiry": date_of_expiry,
                    "gender": gender,
                })

        customer = self.call_repos(await repos_save_customer_ekyc(
            body_request=body,
        ))

        return self.response(data=customer)
