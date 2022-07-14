from typing import Optional

from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.customer_service.repository import (
    repos_create_booking_kss, repos_create_post_check,
    repos_get_customer_detail, repos_get_history_post_post_check,
    repos_get_list_branch, repos_get_list_kss, repos_get_list_zone,
    repos_get_post_control, repos_get_statistics, repos_get_statistics_month,
    repos_get_statistics_profiles, repos_save_customer_ekyc,
    repos_update_post_check
)
from app.api.v1.endpoints.customer_service.schema import (
    CreatePostCheckRequest, QueryParamsKSSRequest, UpdatePostCheckRequest
)
from app.api.v1.endpoints.third_parties.gw.casa_account.repository import (
    repos_gw_change_status_account, repos_gw_get_casa_account_info
)
from app.settings.config import DATE_INPUT_OUTPUT_FORMAT
from app.utils.constant.business_type import BUSINESS_TYPE_EKYC_AUDIT
from app.utils.constant.cif import (
    CRM_GENDER_TYPE_FEMALE, EKYC_DOCUMENT_TYPE_NEW_CITIZEN,
    EKYC_DOCUMENT_TYPE_OLD_CITIZEN, EKYC_DOCUMENT_TYPE_PASSPORT,
    EKYC_GENDER_TYPE_FEMALE, EKYC_GENDER_TYPE_MALE
)
from app.utils.constant.ekyc import (
    EKYC_DATE_FORMAT, EKYC_DEFAULT_VALUE, GROUP_ROLE_CODE_AP,
    GROUP_ROLE_CODE_IN, GROUP_ROLE_CODE_VIEW, MENU_CODE, MENU_CODE_VIEW
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
            group_role_code=GROUP_ROLE_CODE_VIEW)
        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST KSS',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN)

        query_data = {}
        query_data.update({'cif_phone_number_gttt_name': query_params.cif_phone_number_gttt_name}) if query_params.cif_phone_number_gttt_name else None
        query_data.update({'transaction_id': query_params.transaction_id}) if query_params.transaction_id else None
        query_data.update({'tran_type_id': query_params.tran_type_id}) if query_params.tran_type_id else None
        query_data.update({'approve_status': query_params.approve_status}) if query_params.approve_status else None
        query_data.update({'branch_id': query_params.branch_id}) if query_params.branch_id else None
        query_data.update({'zone_id': query_params.zone_id}) if query_params.zone_id else None
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

        return self.response(data=post_control_response)

    async def ctr_history_post_check(self, postcheck_uuid: str):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
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

        return self.response(data=history_post_check)

    async def ctr_statistics_month(self, months: int):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
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

    async def ctr_get_statistics_profiles(self):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
            group_role_code=GROUP_ROLE_CODE_VIEW)

        if not is_success:
            return self.response_exception(
                msg=MESSAGE_STATUS[ERROR_PERMISSION],
                loc='LIST GET POST CONTROL',
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        statistics_profiles = self.call_repos(await repos_get_statistics_profiles())

        return self.response(data=statistics_profiles)

    async def ctr_get_statistics(self, search_type: int, selected_date: str):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
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

        # TODO
        booking_id, booking_code = self.call_repos(await repos_create_booking_kss( # noqa
            business_type_code=BUSINESS_TYPE_EKYC_AUDIT,
            current_user=current_user.user_info,
            payload_data=payload_data,
            session=self.oracle_session
        ))
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
        if history_status:
            if history_status[-1]['kss_status'] == "Không hợp lệ" and history_status[-1]['approve_status'] == "Đã Duyệt":
                account_number = self.call_repos(await repos_gw_change_status_account( # noqa
                    current_user=current_user.user_info,
                    account_number=customer_detail.get('account_number')
                ))

        return self.response(data=update_post_check)

    async def ctr_get_customer_detail(self, postcheck_uuid: str):
        current_user = self.current_user

        is_success, response = self.check_permission(
            current_user=current_user,
            menu_code=MENU_CODE,
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
        if not national:
            customer_detail['nationality'] = 'Việt Nam'
        transaction_id = customer_detail.get('transaction_id')
        ekyc_step = []
        for item in customer_detail.get('ekyc_step'):
            if transaction_id == item.get('transaction_id'):
                ekyc_step.extend(item.get('info_step'))

        customer_detail.update({
            "resident_status": "Cư Trú",
            "ekyc_step": ekyc_step
        })

        account_number = customer_detail.get('account_number')
        if account_number:
            account_detail = self.call_repos(await repos_gw_get_casa_account_info(
                account_number=account_number,
                current_user=self.current_user.user_info
            ))
            account_status = account_detail['retrieveCurrentAccountCASA_out']['data_output']['customer_info']['account_info']['account_status']
            for key, value in account_status[0].items():
                if key == "AC_STAT_NO_DR":
                    if value == "N":
                        customer_detail.update(dict(
                            account_status="Mở"
                        ))
                    else:
                        customer_detail.update(dict(
                            account_status="Đóng"
                        ))

        return self.response(data=customer_detail)

    async def ctr_save_customer_ekyc(
            self,
            face_ids: int,
            ocr_result_ekyc_data: dict,
            gender: str,
            date_of_expiry: str,
            phone_number: str,
            booking_id: Optional[str],
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
            booking_id=booking_id
        ))

        return self.response(data=customer)
