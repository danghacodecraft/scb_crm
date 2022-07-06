from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.common_repository import (
    repos_get_next_stage, repos_get_previous_stage,
    repos_get_previous_transaction_daily, repos_get_stage_codes_in_business,
    repos_get_stage_information, repos_get_stage_teller,
    repos_open_cif_get_previous_stage
)
from app.api.v1.endpoints.approval.repository import (
    repos_approval_get_face_authentication, repos_approve,
    repos_get_approval_identity_faces, repos_get_approval_identity_images,
    repos_get_approval_process, repos_get_business_job_codes,
    repos_get_business_jobs, repos_get_business_jobs_by_open_casa,
    repos_get_compare_image_transactions, repos_get_list_audit
)
from app.api.v1.endpoints.approval.schema import ApprovalRequest
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_get_sla_transaction_parent_from_stage_transaction_id
)
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_employee_info_from_code
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType
)
from app.third_parties.oracle.models.master_data.others import BusinessJob
from app.third_parties.services.idm import ServiceIDM
from app.utils.constant.approval import (
    APPROVE_AUDIT_STAGES, APPROVE_SUPERVISOR_STAGES, CIF_STAGE_APPROVE_KSS,
    CIF_STAGE_APPROVE_KSV, CIF_STAGE_COMPLETED, CIF_STAGE_INIT,
    COMPLETED_STAGES, INIT_RESPONSE, INIT_STAGES, STAGE_BEGINS
)
from app.utils.constant.business_type import (
    BUSINESS_TYPE_INIT_CIF, BUSINESS_TYPES
)
from app.utils.constant.casa import RECEIVING_METHOD_IDENTITY_CASES
from app.utils.constant.cif import (
    DROPDOWN_NONE_DICT, IMAGE_TYPE_FACE, IMAGE_TYPE_FINGERPRINT,
    IMAGE_TYPE_SIGNATURE
)
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_GDV, IDM_GROUP_ROLE_CODE_KSV, IDM_MENU_CODE_TTKH,
    IDM_PERMISSION_CODE_GDV, IDM_PERMISSION_CODE_KSS, IDM_PERMISSION_CODE_KSV
)
from app.utils.error_messages import (
    ERROR_APPROVAL_INCORRECT_UPLOAD_FACE,
    ERROR_APPROVAL_INCORRECT_UPLOAD_FINGERPRINT,
    ERROR_APPROVAL_INCORRECT_UPLOAD_SIGNATURE,
    ERROR_APPROVAL_NO_DATA_IN_IDENTITY_STEP,
    ERROR_APPROVAL_NO_SIGNATURE_IN_IDENTITY_STEP,
    ERROR_APPROVAL_UPLOAD_SIGNATURE, ERROR_BUSINESS_TYPE_NOT_EXIST,
    ERROR_CIF_ID_NOT_EXIST, ERROR_CONTENT_NOT_NULL, ERROR_PERMISSION,
    ERROR_STAGE_COMPLETED, ERROR_VALIDATE, ERROR_WRONG_STAGE_ACTION,
    MESSAGE_STATUS, ERROR_FIELD_REQUIRED
)
from app.utils.functions import (
    dropdown, generate_uuid, now, orjson_dumps, orjson_loads
)


class CtrApproval(BaseController):
    async def ctr_approval_process(self, booking_id: str):
        transactions = self.call_repos((await repos_get_approval_process(
            booking_id=booking_id,
            session=self.oracle_session
        )))
        response_data = []
        lst_parent = {}

        for _, _, _, transaction_sender, transaction_root_daily in transactions:
            lst_parent.update({transaction_root_daily.created_at.date(): []})

        for parent_key, parent_value in lst_parent.items():
            childs = []

            for booking_customer, _, transaction_daily, transaction_sender, transaction_root_daily in transactions:
                content = orjson_loads(transaction_root_daily.data)
                employee_info = self.call_repos(await repos_gw_get_employee_info_from_code(
                    employee_code=transaction_sender.user_id, current_user=self.current_user))
                avatar = ServiceIDM().replace_with_cdn(employee_info['selectEmployeeInfoFromCode_out']['data_output']['employee_info']['avatar'])
                if parent_key == transaction_root_daily.created_at.date():
                    childs.append({
                        "user_id": transaction_sender.user_id,
                        "full_name_vn": transaction_sender.user_fullname,
                        "avatar_url": avatar,
                        "position": {
                            "id": transaction_sender.position_id,
                            "code": transaction_sender.position_code,
                            "name": transaction_sender.position_name
                        },
                        "department": {
                            "id": transaction_sender.department_id,
                            "code": transaction_sender.department_code,
                            "name": transaction_sender.department_name
                        },
                        "branch": {
                            "id": transaction_sender.branch_id,
                            "code": transaction_sender.branch_code,
                            "name": transaction_sender.branch_name
                        },
                        "title": {
                            "id": transaction_sender.title_id,
                            "code": transaction_sender.title_code,
                            "name": transaction_sender.title_name
                        },
                        "created_at": transaction_root_daily.created_at,
                        "content": content['content'] if content else ""
                    })
            response_data.append({
                "created_at": parent_key,
                "logs": childs
            })

        return self.response(data=response_data)

    async def ctr_get_approval(self, booking_id: str, amount: int): # noqa
        # current_user = self.current_user.user_info
        auth_response = self.current_user

        ################################################################################################################
        # THÔNG TIN XÁC THỰC
        ################################################################################################################
        # Khuôn mặt
        created_at = None
        init_identity_face_images = []
        identity_face_images = []
        identity_face_image_uuids = []
        image_face_uuids = []

        compare_face_uuid = None
        cif_id = None
        authentication = None
        business_type = await CtrBooking().ctr_get_business_type(booking_id=booking_id)
        if business_type.code == BUSINESS_TYPE_INIT_CIF:
            customer_info = await CtrBooking().ctr_get_customer_from_booking(
                booking_id=booking_id
            )

            if not customer_info:
                return self.response_exception(msg=ERROR_CIF_ID_NOT_EXIST, loc=f"booking_id {booking_id}")

            cif_id = customer_info.id

            # check cif tồn tại
            await self.get_model_object_by_id(model_id=cif_id, model=Customer, loc="cif_id")

            transactions = self.call_repos(await repos_get_approval_identity_images(
                cif_id=cif_id,
                session=self.oracle_session
            ))

            (
                face_transactions, fingerprint_transactions, signature_transactions
            ) = await self.check_data_in_identity_step_and_get_faces_fingerprints_signatures(transactions)

            identity_image_ids = []
            for identity, identity_image in face_transactions:
                identity_face_uuid = identity_image.image_url
                image_face_uuids.append(identity_face_uuid)
                identity_image_ids.append(identity_image.id)

            # Lấy hình ảnh so sánh, số nhiều nhưng cùng chung uuid
            compare_image_transactions = self.call_repos(await repos_get_compare_image_transactions(
                identity_image_ids=identity_image_ids,
                session=self.oracle_session
            ))

            distinct_identity_images = {}
            for compare_image, compare_image_transaction in compare_image_transactions:
                compare_face_uuid = compare_image_transaction.compare_image_url
                created_at = compare_image_transaction.maker_at
                image_face_uuids.append(compare_image_transaction.compare_image_url)
                for identity, identity_image in face_transactions:
                    if compare_image_transaction.identity_image_id == identity_image.id:
                        distinct_identity_images.update({
                            identity_image.image_url: compare_image_transaction.similar_percent
                        })
                        identity_face_image_uuids.append(compare_image_transaction.compare_image_url)
            image_face_uuids.extend(identity_face_image_uuids)

            # gọi đến service file để lấy link download
            uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_face_uuids)

            for distinct_identity_image in distinct_identity_images:
                identity_face_images.append(dict(
                    url=uuid__link_downloads[distinct_identity_image],
                    similar_percent=distinct_identity_images[distinct_identity_image]
                ))

            # RULE: Nếu chưa upload -> Trả null hết (Lấy 2 hình mới nhất)
            if not identity_face_images and not compare_face_uuid:
                # for identity, identity_image in face_transactions:
                #     init_identity_face_images.append(dict(
                #         url=uuid__link_downloads[identity_image.image_url],
                #         similar_percent=None
                #     ))
                identity_face_images = init_identity_face_images
                created_at = None

            face_authentication = dict(
                compare_url=uuid__link_downloads[compare_face_uuid] if compare_face_uuid else None,
                # compare_face_url=compare_face_url,
                compare_uuid=compare_face_uuid,
                created_at=created_at,
                identity_images=identity_face_images,
            )

            ############################################################################################################
            # Chữ kí - signature
            created_at = None
            init_identity_signature_images = []
            identity_signature_images = []
            identity_signature_image_uuids = []
            image_signature_uuids = []

            compare_signature_uuid = None

            identity_signature_image_ids = []
            for identity, identity_image in signature_transactions:
                identity_signature_uuid = identity_image.image_url
                image_signature_uuids.append(identity_signature_uuid)
                identity_signature_image_ids.append(identity_image.id)

            # Lấy hình ảnh so sánh, số nhiều nhưng cùng chung uuid
            compare_signature_image_transactions = self.call_repos(await repos_get_compare_image_transactions(
                identity_image_ids=identity_signature_image_ids,
                session=self.oracle_session
            ))

            distinct_signature_identity_images = {}
            for compare_image, compare_image_transaction in compare_signature_image_transactions[:2]:
                compare_signature_uuid = compare_image_transaction.compare_image_url
                created_at = compare_image_transaction.maker_at
                image_signature_uuids.append(compare_signature_uuid)
                for identity, identity_image in signature_transactions:
                    if compare_image_transaction.identity_image_id == identity_image.id:
                        distinct_signature_identity_images.update({
                            identity_image.image_url: compare_image_transaction.similar_percent
                        })
                        identity_signature_image_uuids.append(compare_image_transaction.compare_image_url)
            image_signature_uuids.extend(identity_signature_image_uuids)

            # gọi đến service file để lấy link download
            uuid_signature_link_downloads = await self.get_link_download_multi_file(uuids=image_signature_uuids)

            for distinct_identity_image in distinct_signature_identity_images:
                identity_signature_images.append(dict(
                    url=uuid_signature_link_downloads[distinct_identity_image],
                    similar_percent=distinct_signature_identity_images[distinct_identity_image]
                ))

            # RULE: Nếu chưa upload -> Lấy 2 hình mới nhất
            if not identity_signature_images and not compare_signature_uuid:
                for identity, identity_image in signature_transactions: # noqa
                    init_identity_signature_images.append(dict(
                        # url=uuid_signature_link_downloads[identity_image.image_url],
                        url=None,
                        similar_percent=None
                    ))
                identity_signature_images = init_identity_signature_images

            signature_authentication = dict(
                compare_url=uuid_signature_link_downloads[compare_signature_uuid] if compare_signature_uuid else None,
                compare_uuid=compare_signature_uuid,
                created_at=created_at,
                identity_images=identity_signature_images,
            )
            ############################################################################################################
            # Vân tay - fingerprint
            created_at = None
            init_identity_fingerprint_images = []
            identity_fingerprint_images = []
            identity_fingerprint_image_uuids = []
            image_fingerprint_uuids = []

            compare_fingerprint_uuid = None

            identity_fingerprint_image_ids = []
            for _, identity_image in fingerprint_transactions:
                identity_fingerprint_uuid = identity_image.image_url
                image_fingerprint_uuids.append(identity_fingerprint_uuid)
                identity_fingerprint_image_ids.append(identity_image.id)

            # Lấy hình ảnh so sánh, số nhiều nhưng cùng chung uuid
            compare_fingerprint_image_transactions = self.call_repos(await repos_get_compare_image_transactions(
                identity_image_ids=identity_fingerprint_image_ids,
                session=self.oracle_session
            ))

            distinct_fingerprint_identity_images = {}
            # lấy 2 trong số các chữ ký query
            for compare_image, compare_image_transaction in compare_fingerprint_image_transactions[:2]:
                compare_fingerprint_uuid = compare_image_transaction.compare_image_url
                created_at = compare_image_transaction.maker_at
                image_fingerprint_uuids.append(compare_fingerprint_uuid)

                for identity, identity_image in fingerprint_transactions:
                    if compare_image_transaction.identity_image_id == identity_image.id:
                        distinct_fingerprint_identity_images.update({
                            identity_image.image_url: compare_image_transaction.similar_percent
                        })
                        identity_fingerprint_image_uuids.append(compare_image_transaction.compare_image_url)

            image_fingerprint_uuids.extend(identity_fingerprint_image_uuids)

            # gọi đến service file để lấy link download
            uuid_fingerprint_link_downloads = await self.get_link_download_multi_file(uuids=image_fingerprint_uuids)

            for distinct_identity_image in distinct_fingerprint_identity_images:
                identity_fingerprint_images.append(dict(
                    url=uuid_fingerprint_link_downloads[distinct_identity_image],
                    similar_percent=distinct_fingerprint_identity_images[distinct_identity_image]
                ))

            # RULE: Nếu chưa upload -> Lấy 2 hình mới nhất
            if not identity_fingerprint_images and not compare_fingerprint_uuid:
                for identity, identity_image in fingerprint_transactions:   # noqa
                    init_identity_fingerprint_images.append(dict(
                        # url=uuid_fingerprint_link_downloads[identity_image.image_url],
                        url=None,
                        similar_percent=None
                    ))
                identity_fingerprint_images = init_identity_fingerprint_images

            fingerprint_authentication = dict(
                compare_url=uuid_fingerprint_link_downloads[compare_fingerprint_uuid] if compare_fingerprint_uuid else None,
                compare_uuid=compare_fingerprint_uuid,
                created_at=created_at,
                identity_images=identity_fingerprint_images,
            )

            authentication = dict(
                face=face_authentication,
                signature=signature_authentication,
                fingerprint=fingerprint_authentication
            )

            ############################################################################################################

        ################################################################################################################
        # PHÊ DUYỆT
        ################################################################################################################

        # Kiểm tra xem đang ở bước nào của giao dịch
        (
            _, previous_transaction_daily, previous_transaction_stage, _, previous_transaction_sender,
            previous_transaction_stage_action
        ) = self.call_repos(
            await repos_open_cif_get_previous_stage(
                booking_id=booking_id,
                session=self.oracle_session
            ))

        previous_transaction_stage_is_reject = previous_transaction_stage.is_reject
        is_open_cif = False

        previous_stage_code = None

        stage_teller = dict()
        teller_is_reject = False
        teller_stage_code = None
        teller_is_disable = True
        teller_is_completed = False
        teller_content = None
        teller_created_at = None
        teller_created_by = None
        dropdown_action_teller = DROPDOWN_NONE_DICT

        stage_supervisor = dict()
        supervisor_is_reject = False
        supervisor_stage_code = None
        supervisor_is_disable = True
        supervisor_is_completed = False
        supervisor_content = None
        supervisor_created_at = None
        supervisor_created_by = None
        dropdown_action_supervisor = DROPDOWN_NONE_DICT

        stage_audit = dict()
        audit_is_reject = False
        audit_stage_code = None
        audit_is_disable = True
        audit_is_completed = False
        audit_content = None
        audit_created_at = None
        audit_created_by = None
        dropdown_action_audit = DROPDOWN_NONE_DICT

        if previous_transaction_stage:
            previous_stage_code = previous_transaction_stage.transaction_stage_phase_code

        stages = []

        is_role_audit = self.call_repos(await PermissionController.ctr_approval_check_permission_stage(
            auth_response=auth_response,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_KSV,
            permission_code=IDM_PERMISSION_CODE_KSS,
            stage_code=CIF_STAGE_APPROVE_KSS
        ))
        is_role_supervisor = self.call_repos(await PermissionController.ctr_approval_check_permission_stage(
            auth_response=auth_response,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_KSV,
            permission_code=IDM_PERMISSION_CODE_KSV,
            stage_code=CIF_STAGE_APPROVE_KSV
        ))
        is_role_teller = self.call_repos(await PermissionController.ctr_approval_check_permission_stage(
            auth_response=auth_response,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_GDV,
            permission_code=IDM_PERMISSION_CODE_GDV,
            stage_code=CIF_STAGE_INIT
        ))

        # Chỉ những người có rule mới được xem phê duyệt
        # if not (is_stage_audit or is_stage_supervisor or is_stage_teller):
        #     return self.response_exception(
        #         loc=f"Stage: {previous_stage_code}, "
        #             f"User: {current_user.username}, "
        #             f"IDM_MENU_CODE: {IDM_MENU_CODE_OPEN_CIF}, "
        #             f"IDM_GROUP_ROLE_CODE: {IDM_GROUP_ROLE_CODE_APPROVAL}, "
        #             f"IDM_PERMISSION_CODE: {IDM_PERMISSION_CODE_KSS}",
        #         msg=ERROR_PERMISSION,
        #         error_status_code=status.HTTP_403_FORBIDDEN
        #     )

        business_type = await CtrBooking().ctr_get_business_type(booking_id=booking_id)
        stage_codes = self.call_repos(await repos_get_stage_codes_in_business(
            business_type_code=business_type.code,
            session=self.oracle_session
        ))

        # Chưa có hồ sơ nào trước đó, GDV gửi hồ sơ đi
        if previous_stage_code in STAGE_BEGINS:
            # if not is_stage_teller:
            #     return self.response_exception(
            #         loc=f"Stage: {previous_stage_code}, "
            #             f"User: {current_user.username}, "
            #             f"IDM_MENU_CODE: {IDM_MENU_CODE_OPEN_CIF}, "
            #             f"IDM_GROUP_ROLE_CODE: {IDM_GROUP_ROLE_CODE_OPEN_CIF}, "
            #             f"IDM_PERMISSION_CODE: {IDM_PERMISSION_CODE_OPEN_CIF}",
            #         msg=ERROR_PERMISSION,
            #         error_status_code=status.HTTP_403_FORBIDDEN
            #     )
            if is_role_teller:
                teller_is_disable = False

        # Hồ sơ GDV đã gửi
        elif previous_stage_code in INIT_STAGES:
            teller_is_reject = previous_transaction_stage_is_reject
            teller_stage_code = previous_stage_code
            teller_is_completed = True
            teller_content = orjson_loads(previous_transaction_daily.data)["content"]
            teller_created_at = previous_transaction_daily.created_at
            teller_created_by = previous_transaction_sender.user_fullname
            teller_is_disable = False

            if is_role_supervisor:
                # return self.response_exception(
                #     loc=f"Stage: {previous_stage_code}, "
                #         f"User: {current_user.username}, "
                #         f"IDM_MENU_CODE: {IDM_MENU_CODE_OPEN_CIF}, "
                #         f"IDM_GROUP_ROLE_CODE: {IDM_GROUP_ROLE_CODE_APPROVAL}, "
                #         f"IDM_PERMISSION_CODE: {IDM_PERMISSION_CODE_KSV}",
                #     msg=ERROR_PERMISSION,
                #     error_status_code=status.HTTP_403_FORBIDDEN
                # )
                supervisor_is_disable = False
                teller_is_disable = True
                audit_is_disable = True

            audit_transaction = self.call_repos(await repos_get_previous_transaction_daily(
                transaction_daily_id=previous_transaction_daily.transaction_id,
                session=self.oracle_session
            ))
            if audit_transaction:
                (
                    audit_transaction_daily, audit_transaction_sender, audit_transaction_stage, _,
                    audit_transaction_stage_action
                ) = audit_transaction
                audit_transaction_stage = audit_transaction_stage.transaction_stage_phase_code
                if audit_transaction_stage in stage_codes:
                    audit_stage_code = audit_transaction_stage
                    audit_content = orjson_loads(audit_transaction_daily.data)["content"]
                    audit_created_at = audit_transaction_daily.created_at
                    audit_created_by = audit_transaction_sender.user_fullname
                    dropdown_action_audit = dropdown(audit_transaction_stage_action)

                supervisor_transaction = self.call_repos(await repos_get_previous_transaction_daily(
                    transaction_daily_id=audit_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
                if supervisor_transaction:
                    (
                        supervisor_transaction_daily, supervisor_transaction_sender, supervisor_transaction_stage, _,
                        supervisor_transaction_stage_action
                    ) = supervisor_transaction
                    supervisor_transaction_stage_code = supervisor_transaction_stage.transaction_stage_phase_code
                    if supervisor_transaction_stage_code in stage_codes:
                        supervisor_stage_code = supervisor_transaction_stage_code
                        supervisor_content = orjson_loads(supervisor_transaction_daily.data)["content"]
                        supervisor_created_at = supervisor_transaction_daily.created_at
                        supervisor_created_by = supervisor_transaction_sender.user_fullname
                        dropdown_action_supervisor = dropdown(supervisor_transaction_stage_action)

        # KSV đã xử lý hồ sơ
        elif previous_stage_code in APPROVE_SUPERVISOR_STAGES:
            supervisor_transaction_stage_action = previous_transaction_stage_action
            if previous_transaction_stage_action:
                dropdown_action_supervisor = dropdown(supervisor_transaction_stage_action)

            supervisor_stage_code = previous_stage_code
            supervisor_transaction_daily = previous_transaction_daily
            supervisor_transaction_sender = previous_transaction_sender
            supervisor_is_completed = True
            supervisor_content = orjson_loads(supervisor_transaction_daily.data)["content"]
            supervisor_created_at = supervisor_transaction_daily.created_at
            supervisor_created_by = supervisor_transaction_sender.user_fullname

            (
                teller_transaction_daily, teller_transaction_sender, teller_transaction_stage, _,
                teller_transaction_stage_action
            ) = self.call_repos(await repos_get_previous_transaction_daily(
                transaction_daily_id=supervisor_transaction_daily.transaction_id,
                session=self.oracle_session
            ))
            teller_is_reject = teller_transaction_stage.is_reject
            teller_stage_code = teller_transaction_stage.transaction_stage_phase_code
            teller_is_completed = True
            teller_content = orjson_loads(teller_transaction_daily.data)["content"]
            teller_created_at = teller_transaction_daily.created_at
            teller_created_by = teller_transaction_sender.user_fullname

            supervisor_is_reject = previous_transaction_stage_is_reject

            if supervisor_is_reject and is_role_teller:
                teller_is_disable = False
            if not supervisor_is_reject and is_role_audit:
                audit_is_disable = False
                is_open_cif = True

        # KSS đã xử lý hồ sơ
        elif previous_stage_code in APPROVE_AUDIT_STAGES:
            audit_transaction_stage = previous_transaction_stage
            audit_is_reject = previous_transaction_stage.is_reject
            audit_stage_code = previous_stage_code
            audit_transaction_daily = previous_transaction_daily
            audit_transaction_sender = previous_transaction_sender
            audit_is_completed = True
            audit_content = orjson_loads(audit_transaction_daily.data)["content"]
            audit_created_at = audit_transaction_daily.created_at
            audit_created_by = audit_transaction_sender.user_fullname

            if previous_transaction_stage_action:
                dropdown_action_audit = dropdown(previous_transaction_stage_action)

            supervisor_transaction_daily, supervisor_transaction_sender, supervisor_transaction_stage, _, supervisor_transaction_stage_action = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=audit_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            supervisor_is_reject = supervisor_transaction_stage.is_reject
            supervisor_stage_code = supervisor_transaction_stage.transaction_stage_phase_code
            supervisor_is_completed = True
            supervisor_content = orjson_loads(supervisor_transaction_daily.data)["content"]
            supervisor_created_at = supervisor_transaction_daily.created_at
            supervisor_created_by = supervisor_transaction_sender.user_fullname
            dropdown_action_supervisor = dropdown(supervisor_transaction_stage_action)

            teller_transaction_daily, teller_transaction_sender, teller_transaction_stage, _, teller_transaction_stage_action = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=supervisor_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            teller_stage_code = teller_transaction_stage.transaction_stage_phase_code
            teller_is_completed = True
            teller_content = orjson_loads(teller_transaction_daily.data)["content"]
            teller_created_at = teller_transaction_daily.created_at
            teller_created_by = teller_transaction_sender.user_fullname
            dropdown_action_teller = dropdown(teller_transaction_stage_action)

            if is_role_teller and audit_transaction_stage.is_reject:
                teller_is_disable = False

        stage_teller.update(dict(
            stage_code=teller_stage_code,
            is_reject=teller_is_reject,
            is_disable=teller_is_disable,
            is_completed=teller_is_completed,
            content=teller_content,
            action=dropdown_action_teller,
            created_at=teller_created_at,
            created_by=teller_created_by
        ))
        stage_supervisor.update(dict(
            stage_code=supervisor_stage_code,
            is_reject=supervisor_is_reject,
            is_disable=supervisor_is_disable,
            is_completed=supervisor_is_completed,
            content=supervisor_content,
            action=dropdown_action_supervisor,
            created_at=supervisor_created_at,
            created_by=supervisor_created_by
        ))
        stage_audit.update(dict(
            stage_code=audit_stage_code,
            is_reject=audit_is_reject,
            is_disable=audit_is_disable,
            is_completed=audit_is_completed,
            content=audit_content,
            action=dropdown_action_audit,
            created_at=audit_created_at,
            created_by=audit_created_by
        ))

        stages.extend([stage_teller, stage_supervisor, stage_audit])
        ################################################################################################################

        return self.response(data=dict(
            cif_id=cif_id,
            stages=stages,
            authentication=authentication,
            is_open_cif=is_open_cif
        ))

    async def ctr_approve(
            self,
            cif_id: str,
            booking_id: str,
            request: ApprovalRequest
    ):
        auth_response = self.current_user
        current_user = self.current_user.user_info
        business_type = await CtrBooking().ctr_get_business_type(booking_id=booking_id)
        business_type_id = business_type.code
        face_authentications = []
        fingerprint_authentications = []
        signature_authentications = []

        # check cif tồn tại
        await self.get_model_object_by_id(model_id=cif_id, model=Customer, loc="cif_id")

        booking_business_form = await CtrBooking().ctr_get_booking_business_form(
            booking_id=booking_id, session=self.oracle_session
        )
        form_data = orjson_loads(booking_business_form.form_data)
        # TH1: Method không có cif
        if form_data['receiving_method'] in RECEIVING_METHOD_IDENTITY_CASES:
            return self.response_exception(
                msg=f"{form_data['receiving_method']}",
                detail="Đang nâng cấp"
            )
        # TH2: Method BẮT BUỘC có cif
        elif not cif_id:
            return self.response_exception(
                msg=ERROR_FIELD_REQUIRED,
                loc='cif_id'
            )

        ############################################################################################################
        # THÔNG TIN XÁC THỰC
        ############################################################################################################

        # Lấy tất cả hình ảnh ở bước GTDD
        transactions = self.call_repos(await repos_get_approval_identity_images(
            cif_id=cif_id,
            session=self.oracle_session
        ))
        await self.check_data_in_identity_step_and_get_faces_fingerprints_signatures(transactions)

        ############################################################################################################
        # Thông tin xác thực
        authentications = self.call_repos(await repos_approval_get_face_authentication(
            cif_id=cif_id,
            session=self.oracle_session
        ))

        for _, identity_image, identity_image_transaction, _, compare_image_transaction in authentications:
            if identity_image.image_type_id == IMAGE_TYPE_FACE:
                face_authentications.append({
                    identity_image_transaction.image_url: compare_image_transaction.compare_image_url
                })
            if identity_image.image_type_id == IMAGE_TYPE_FINGERPRINT:
                fingerprint_authentications.append({
                    identity_image_transaction.image_url: compare_image_transaction.compare_image_url
                })
            if identity_image.image_type_id == IMAGE_TYPE_SIGNATURE:
                signature_authentications.append({
                    identity_image_transaction.image_url: compare_image_transaction.compare_image_url
                })

        # # Kiểm tra xem khuôn mặt đã upload chưa
        # if not face_authentications:
        #     return self.response_exception(
        #         msg=ERROR_APPROVAL_UPLOAD_FACE,
        #         detail=MESSAGE_STATUS[ERROR_APPROVAL_UPLOAD_FACE]
        #     )

        # # Kiểm tra xem VÂN TAY đã upload chưa
        # if not fingerprint_authentications:
        #     return self.response_exception(
        #         msg=ERROR_APPROVAL_UPLOAD_FINGERPRINT,
        #         detail=MESSAGE_STATUS[ERROR_APPROVAL_UPLOAD_FINGERPRINT]
        #     )

        # Kiểm tra xem chữ ký đã upload chưa
        if not signature_authentications:
            return self.response_exception(
                msg=ERROR_APPROVAL_UPLOAD_SIGNATURE,
                detail=MESSAGE_STATUS[ERROR_APPROVAL_UPLOAD_SIGNATURE]
            )
        ############################################################################################################

        ################################################################################################################
        # THÔNG TIN BIỂU MẪU
        ################################################################################################################
        # TODO: Kiểm tra số biểu mẫu gửi xuống có bằng với số biểu mẫu liên quan hay không

        ################################################################################################################
        # PHÊ DUYỆT
        ################################################################################################################
        content = request.approval.content
        reject_flag = request.approval.reject_flag
        action_id = request.approval.action_id

        _, _, previous_transaction_stage = self.call_repos(
            await repos_get_previous_stage(
                booking_id=booking_id,
                session=self.oracle_session
            )
        )

        if not previous_transaction_stage:
            return self.response_exception(msg="No Previous Transaction Stage")

        ################################################################################################################
        # PREVIOUS STAGE
        ################################################################################################################
        is_stage_init = True
        previous_stage_code = None
        previous_transaction_stage_is_reject = previous_transaction_stage.is_reject
        previous_stage_is_reject = False
        is_give_back = False
        if previous_transaction_stage:
            is_stage_init = False
            _, previous_stage, _, _, _, _, _, _, _ = self.call_repos(
                await repos_get_stage_information(
                    business_type_id=business_type_id,
                    stage_id=previous_transaction_stage.transaction_stage_phase_code,
                    session=self.oracle_session,
                    reject_flag=previous_transaction_stage_is_reject,
                    stage_action_id=action_id
                ))
            previous_stage_code = previous_stage.code
            previous_stage_is_reject = previous_stage.is_reject

        ################################################################################################################
        # CURRENT STAGE
        if is_stage_init:
            # Cập nhật trạng thái đã duyệt hình ảnh này
            face_transactions = self.call_repos(await repos_get_approval_identity_faces(
                cif_id=cif_id,
                session=self.oracle_session
            ))
            identity_image_ids = []
            for identity, identity_image in face_transactions:
                identity_image_ids.append(identity_image.id)

            # Lấy hình ảnh so sánh, số nhiều nhưng cùng chung uuid
            compare_image_transactions = self.call_repos(await repos_get_compare_image_transactions(
                identity_image_ids=identity_image_ids,
                session=self.oracle_session
            ))
            if not compare_image_transactions:
                return self.response_exception(msg="No Compare Image")

            for compare_image, compare_image_transaction in compare_image_transactions:
                compare_image_transaction.approved_at = now()
                compare_image_transaction.approved_id = current_user.code

            current_stage_code = CIF_STAGE_INIT
        else:
            # Nếu là bước GDV
            if previous_stage_is_reject or previous_stage_code in STAGE_BEGINS:
                current_stage = self.call_repos(await repos_get_stage_teller(
                    business_type_id=business_type_id,
                    session=self.oracle_session
                ))
                is_give_back = True

                if not request.authentication:
                    return self.response_exception(
                        msg=ERROR_VALIDATE,
                        detail="Field required",
                        loc="authentication"
                    )

                ####################################################################################################
                # [Thông tin xác thực] Khuôn mặt
                if face_authentications:
                    if not request.authentication.face:
                        return self.response_exception(
                            msg=ERROR_VALIDATE,
                            detail="Field required",
                            loc="authentication -> face"
                        )
                    new_face_compare_image_transaction_uuid = list(face_authentications[0].values())[0]

                    # Kiểm tra xem khuôn mặt gửi lên có đúng không
                    # Hình ảnh kiểm tra sẽ là hình ảnh của lần Upload mới nhất
                    if new_face_compare_image_transaction_uuid != request.authentication.face.compare_face_image_uuid:
                        return self.response_exception(
                            msg=ERROR_APPROVAL_INCORRECT_UPLOAD_FACE,
                            detail=MESSAGE_STATUS[ERROR_APPROVAL_INCORRECT_UPLOAD_FACE],
                            loc="authentication -> face -> compare_face_image_uuid"
                        )
                ####################################################################################################

                ####################################################################################################
                # [Thông tin xác thực] Vân tay
                if fingerprint_authentications:
                    if not request.authentication.fingerprint:
                        return self.response_exception(
                            msg=ERROR_VALIDATE,
                            detail="Field required",
                            loc="authentication -> fingerprint"
                        )
                    new_fingerprint_compare_image_transaction_uuid = list(fingerprint_authentications[0].values())[0]
                    # Kiểm tra xem vân tay gửi lên có đúng không
                    # Hình ảnh kiểm tra sẽ là hình ảnh của lần Upload mới nhất
                    if new_fingerprint_compare_image_transaction_uuid != request.authentication.fingerprint.compare_face_image_uuid:
                        return self.response_exception(
                            msg=ERROR_APPROVAL_INCORRECT_UPLOAD_FINGERPRINT,
                            detail=MESSAGE_STATUS[ERROR_APPROVAL_INCORRECT_UPLOAD_FINGERPRINT],
                            loc="authentication -> fingerprint -> compare_face_image_uuid"
                        )
                ####################################################################################################

                ####################################################################################################
                # [Thông tin xác thực] Chữ ký
                if not request.authentication.signature:
                    return self.response_exception(
                        msg=ERROR_VALIDATE,
                        detail="Field required",
                        loc="authentication -> signature"
                    )
                new_signature_compare_image_transaction_uuid = list(signature_authentications[0].values())[0]
                # Kiểm tra xem chữ ký gửi lên có đúng không
                # Hình ảnh kiểm tra sẽ là hình ảnh của lần Upload mới nhất
                if new_signature_compare_image_transaction_uuid != request.authentication.signature.compare_face_image_uuid:
                    return self.response_exception(
                        msg=ERROR_APPROVAL_INCORRECT_UPLOAD_SIGNATURE,
                        detail=MESSAGE_STATUS[ERROR_APPROVAL_INCORRECT_UPLOAD_SIGNATURE],
                        loc="authentication -> signature -> compare_face_image_uuid"
                    )
                ####################################################################################################
            else:
                current_stage = self.call_repos(await repos_get_next_stage(
                    business_type_id=business_type_id,
                    current_stage_code=previous_stage_code,
                    session=self.oracle_session,
                    reject_flag=reject_flag,
                ))
            current_stage_code = current_stage.code

        if current_stage_code == CIF_STAGE_COMPLETED:
            return self.response(
                data=dict(
                    cif_id=cif_id,
                    previous_stage=previous_stage_code,
                    current_stage=current_stage_code,
                    next_stage=None
                )
            )

        (
            current_stage_status, current_stage, _, current_lane, current_stage_phase, current_phase, current_stage_role,
            current_stage_action, current_stage_sla
        ) = self.call_repos(await repos_get_stage_information(
            business_type_id=business_type_id,
            stage_id=current_stage_code,
            session=self.oracle_session,
            reject_flag=reject_flag,
            stage_action_id=action_id,
            is_give_back=is_give_back
        ))

        current_stage_status_code = None
        current_stage_status_name = None
        current_stage_name = None
        current_lane_code = None
        current_lane_name = None
        current_phase_code = None
        current_phase_name = None
        current_stage_role_code = None
        current_stage_role_name = None
        current_stage_action_code = None
        current_stage_action_name = None

        if current_stage:
            ############################################################################################################
            # check quyền user
            if current_stage_code in INIT_STAGES:
                self.call_repos(await PermissionController.ctr_approval_check_permission(
                    auth_response=auth_response,
                    menu_code=IDM_MENU_CODE_TTKH,
                    group_role_code=IDM_GROUP_ROLE_CODE_GDV,
                    permission_code=IDM_PERMISSION_CODE_GDV,
                    stage_code=CIF_STAGE_INIT
                ))
            elif current_stage_code in APPROVE_SUPERVISOR_STAGES:
                self.call_repos(await PermissionController.ctr_approval_check_permission(
                    auth_response=auth_response,
                    menu_code=IDM_MENU_CODE_TTKH,
                    group_role_code=IDM_GROUP_ROLE_CODE_KSV,
                    permission_code=IDM_PERMISSION_CODE_KSV,
                    stage_code=CIF_STAGE_APPROVE_KSV
                ))
            elif current_stage_code in APPROVE_AUDIT_STAGES:
                self.call_repos(await PermissionController.ctr_approval_check_permission(
                    auth_response=auth_response,
                    menu_code=IDM_MENU_CODE_TTKH,
                    group_role_code=IDM_GROUP_ROLE_CODE_KSV,
                    permission_code=IDM_PERMISSION_CODE_KSS,
                    stage_code=CIF_STAGE_APPROVE_KSS
                ))
            # Những user khác chỉ có quyền xem không có quyền thực hiện bất kì hành động nào trong phê duyệt
            else:
                return self.response_exception(
                    loc=f"Stage: {current_stage_code}, User: {current_user.code}",
                    msg=ERROR_PERMISSION,
                    detail=MESSAGE_STATUS[ERROR_PERMISSION],
                    error_status_code=status.HTTP_403_FORBIDDEN
                )
            ############################################################################################################
            current_stage_status_code = current_stage_status.code
            current_stage_status_name = current_stage_status.name
            current_stage_name = current_stage.name
            current_lane_code = current_lane.code
            current_lane_name = current_lane.name
            current_phase_code = current_phase.code
            current_phase_name = current_phase.name
            current_stage_role_code = current_stage_role.code
            current_stage_role_name = current_stage_role.name
            if current_stage_code not in INIT_STAGES:
                # Nếu truyền vào Param StageAction giả
                if not current_stage_action:
                    return self.response_exception(
                        loc=f"Stage Action: {action_id}, reject_flag: {reject_flag}, Stage: {current_stage_code}",
                        msg=ERROR_WRONG_STAGE_ACTION
                    )
                current_stage_action_code = current_stage_action.code
                current_stage_action_name = current_stage_action.name

        ################################################################################################################
        # NEXT STAGE
        ################################################################################################################
        if current_stage.is_reject and current_stage_code in APPROVE_SUPERVISOR_STAGES:
            next_stage = self.call_repos(await repos_get_stage_teller(
                business_type_id=business_type_id,
                session=self.oracle_session
            ))
        else:
            next_stage = self.call_repos(await repos_get_next_stage(
                business_type_id=business_type_id,
                current_stage_code=current_stage_code,
                session=self.oracle_session
            ))
        next_stage_code = next_stage.code
        next_stage_role_code = None
        if next_stage_code not in COMPLETED_STAGES:
            _, _, _, _, _, _, next_stage_role, _, _ = self.call_repos(await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=next_stage_code,
                session=self.oracle_session,
                reject_flag=reject_flag,
                stage_action_id=action_id
            ))
            next_stage_role_code = next_stage_role.code

        saving_transaction_stage_status_id = generate_uuid()
        saving_sla_transaction_id = generate_uuid()
        saving_transaction_stage_id = generate_uuid()
        saving_transaction_stage_lane_id = generate_uuid()
        saving_transaction_stage_phase_id = generate_uuid()
        saving_transaction_stage_role_id = generate_uuid()
        transaction_daily_id = generate_uuid()
        transaction_stage_action_id = generate_uuid()

        saving_transaction_stage_status = dict(
            id=saving_transaction_stage_status_id,
            code=current_stage_status_code,
            name=current_stage_status_name,
            created_at=now(),
            updated_at=now()
        )

        saving_transaction_stage_lane = dict(
            id=saving_transaction_stage_lane_id,
            code=current_lane_code,
            name=current_lane_name,
            created_at=now(),
            updated_at=now()
        )

        saving_transaction_stage_phase = dict(
            id=saving_transaction_stage_phase_id,
            code=current_phase_code,
            name=current_phase_name,
            created_at=now(),
            updated_at=now()
        )

        saving_transaction_stage_role = dict(
            id=saving_transaction_stage_role_id,
            transaction_stage_id=saving_transaction_stage_id,
            code=current_stage_role_code,
            name=current_stage_role_name,
            created_at=now(),
            updated_at=now()
        )

        saving_transaction_stage_action = dict(
            id=transaction_stage_action_id,
            code=current_stage_action_code,
            name=current_stage_action_name,
            created_at=now(),
            updated_at=now()
        )

        sla_trans_parent = self.call_repos(await repos_get_sla_transaction_parent_from_stage_transaction_id(
            stage_sla_transaction_id=previous_transaction_stage.sla_transaction_id, session=self.oracle_session
        ))

        saving_sla_transaction = dict(
            id=saving_sla_transaction_id,
            parent_id=sla_trans_parent.id,
            root_id=sla_trans_parent.root_id,
            sla_id=current_stage_sla.id,
            sla_name=current_stage_sla.name,
            sla_deadline=current_stage_sla.deadline,
            active_flag=1,
            created_at=now()
        )

        saving_transaction_stage = dict(
            id=saving_transaction_stage_id,
            status_id=saving_transaction_stage_status_id,
            lane_id=saving_transaction_stage_lane_id,
            phase_id=saving_transaction_stage_phase_id,
            business_type_id=business_type_id,
            sla_transaction_id=saving_sla_transaction_id,
            transaction_stage_phase_code=current_stage_code,
            transaction_stage_phase_name=current_stage_name,
            is_reject=reject_flag,
            action_id=transaction_stage_action_id,
            created_at=now(),
            updated_at=now()
        )

        description = await self.get_description(
            current_stage_code=current_stage_code,
            current_stage_role_code=current_stage_role_code,
            next_stage_role_code=next_stage_role_code,
            reject_flag=reject_flag,
            content=content
        )
        json_data = dict(content=content)
        saving_transaction_daily = dict(
            transaction_id=transaction_daily_id,
            transaction_stage_id=saving_transaction_stage_id,
            transaction_parent_id=None,
            transaction_root_id=None,
            is_reject=reject_flag,
            data=orjson_dumps(json_data),
            description=description,
            created_at=now(),
            updated_at=now()
        )

        saving_transaction_sender = dict(
            transaction_id=transaction_daily_id,
            user_id=current_user.code,
            user_name=current_user.username,
            user_fullname=current_user.name,
            user_email=current_user.email,
            branch_id=current_user.hrm_branch_id,
            branch_code=current_user.hrm_branch_code,
            branch_name=current_user.hrm_branch_name,
            department_id=current_user.hrm_department_id,
            department_code=current_user.hrm_department_code,
            department_name=current_user.hrm_department_name,
            position_id=current_user.hrm_position_id,
            position_code=current_user.hrm_position_code,
            position_name=current_user.hrm_position_name,
            title_id=current_user.hrm_title_id,
            title_code=current_user.hrm_title_code,
            title_name=current_user.hrm_title_name,
            created_at=now(),
            updated_at=now()
        )

        # receiver_branch = None
        # receiver_lane = self.call_repos(await repos_get_next_receiver(
        #     business_type_id=business_type_id,
        #     current_stage_id=current_stage_code,
        #     reject_flag=reject_flag,
        #     session=self.oracle_session
        # ))
        # if receiver_lane:
        #     receiver_branch = await self.get_model_object_by_id(
        #         model_id=receiver_lane.branch_id,
        #         model=Branch,
        #         loc="next_receiver -> branch_id"
        #     )
        #     # receiver_department = await self.get_model_object_by_id(
        #     #     model_id=next_receiver.department_id,
        #     #     model_id=next_receiver.department_id,
        #     #     model=Department,
        #     #     loc="next_receiver -> department_id"
        #     # )

        # if reject_flag and current_stage_code != CIF_STAGE_INIT:
        #     receiver_user = self.call_repos(
        #         await repos_get_transaction_daily(cif_id=cif_id, session=self.oracle_session)
        #     )
        #     saving_transaction_receiver = dict(
        #         transaction_id=transaction_daily_id,
        #         user_id=receiver_user.user_id,
        #         user_name=receiver_user.user_name,
        #         user_fullname=receiver_user.user_fullname,
        #         user_email=receiver_user.user_email,
        #         branch_id=receiver_user.branch_id,
        #         branch_code=receiver_user.branch_code,
        #         branch_name=receiver_user.branch_name,
        #         department_id=receiver_user.department_id,
        #         department_code=receiver_user.department_code,
        #         department_name=receiver_user.department_name,
        #         position_id=receiver_user.position_id,
        #         position_code=receiver_user.position_code,
        #         position_name=receiver_user.position_name,
        #         title_id=current_user.hrm_title_id,
        #         title_code=current_user.hrm_title_code,
        #         title_name=current_user.hrm_title_name
        #     )
        # else:
        #     saving_transaction_receiver = dict(
        #         transaction_id=transaction_daily_id,
        #         user_id=None,
        #         user_name=None,
        #         user_fullname=None,
        #         user_email=None,
        #         branch_id=None,
        #         branch_code=None,
        #         branch_name=None,
        #         department_id=None,
        #         department_code=None,
        #         department_name=None,
        #         position_id=None,
        #         position_code=None,
        #         position_name=None,
        #         title_id=current_user.hrm_title_id,
        #         title_code=current_user.hrm_title_code,
        #         title_name=current_user.hrm_title_name
        #     )

        approval_process = self.call_repos((await repos_approve(
            cif_id=cif_id,
            business_type_id=business_type_id,
            booking_id=booking_id,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_transaction_stage_action=saving_transaction_stage_action,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            is_stage_init=is_stage_init,
            session=self.oracle_session
        )))

        approval_process.update(
            previous_stage=previous_stage_code,
            current_stage=current_stage_code,
            next_stage=next_stage_code,
        )

        return self.response(approval_process)

    async def get_description(
        self,
        current_stage_code: str,
        current_stage_role_code: str,
        next_stage_role_code: str,
        reject_flag: bool,
        content: str
    ):
        # GDV
        if current_stage_code in INIT_STAGES:
            description = f"{current_stage_role_code} đã gửi hồ sơ cho {next_stage_role_code}."
        else:
            # KSV
            if current_stage_code in APPROVE_SUPERVISOR_STAGES:
                if not reject_flag:
                    description = f"Hoàn tất hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role_code}" \
                                  f". Hồ sơ đã gửi cho {next_stage_role_code}."
                else:
                    if not content:
                        return self.response_exception(msg=ERROR_CONTENT_NOT_NULL, loc="content")
                    description = f"Hồ sơ bị từ chối. Lý do: {content}"
            # KSS
            elif current_stage_code in APPROVE_AUDIT_STAGES:
                if not reject_flag:
                    description = f"Hoàn thành hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role_code}."
                else:
                    if not content:
                        return self.response_exception(msg=ERROR_CONTENT_NOT_NULL, loc="content")
                    description = f"Hồ sơ bị từ chối. Lý do: {content}"
            else:
                return self.response_exception(msg=ERROR_STAGE_COMPLETED)

        return description

    async def ctr_get_list_audit(self):
        list_audit = self.call_repos(await repos_get_list_audit(session=self.oracle_session))
        case = {
            "PHE_DUYET_KSV": "Chờ phê duyệt",
            "PHE_DUYET_KSS": "Đã phê duyệt",
            "TU_CHOI_PHE_DUYET": "Từ chối",
        }
        case2 = {
            "PHE_DUYET_KSV": "Hợp lệ",
            "PHE_DUYET_KSS": "Hợp lệ",
            "TU_CHOI_PHE_DUYET": "Không hợp lệ",
        }

        response_datas = []
        for (
            booking_code,
            business_type,
            cif_number,
            customer_full_name_vn,
            customer_mobile_number,
            customer_identity_id,
            customer_identity_type,
            transaction_daily_transaction_id,
            transaction_stage_id,
            transaction_stage_transaction_stage_phase_code,
            transaction_stage_transaction_stage_phase_name,
            transaction_stage_status_id,
            transaction_stage_status_code,
            transaction_stage_status_name,
            _
        ) in list_audit:
            customer_identity_type = await self.get_model_object_by_code(
                model_code=customer_identity_type,
                model=CustomerIdentityType,
                loc="identity_type"
            )
            customer_identity_type = dropdown(customer_identity_type)
            response_datas.append(dict(
                booking_code=booking_code,
                cif_number=cif_number,
                full_name_vn=customer_full_name_vn,
                mobile_number=customer_mobile_number,
                identity_type=customer_identity_type,
                business_type=dropdown(business_type),
                transaction_status=dict(
                    value="",
                    created_at=""
                ),
                audit_status=dict(
                    value=case2[transaction_stage_transaction_stage_phase_code],
                    created_at=""
                ),
                approval_status=dict(
                    value=case[transaction_stage_transaction_stage_phase_code],
                    created_at=""
                )
            ))

        return self.response_paging(
            total_items=len(response_datas),
            data=response_datas
        )

    async def check_data_in_identity_step_and_get_faces_fingerprints_signatures(self, transactions):
        """
        Input: CustomerIdentity, CustomerIdentityImage
        Output: (face_transactions, fingerprint_transactions, signature_transactions)
        """
        is_existed_signature = False
        face_transactions = []
        fingerprint_transactions = []
        signature_transactions = []
        for transaction in transactions:
            _, customer_identity_image = transaction
            image_type_id = customer_identity_image.image_type_id
            if image_type_id == IMAGE_TYPE_FACE:
                face_transactions.append(transaction)
                continue
            if image_type_id == IMAGE_TYPE_FINGERPRINT:
                fingerprint_transactions.append(transaction)
                continue
            if image_type_id == IMAGE_TYPE_SIGNATURE:
                is_existed_signature = True
                signature_transactions.append(transaction)
                continue
        errors = []
        # if not is_existed_face:
        #     errors.append(MESSAGE_STATUS[ERROR_APPROVAL_NO_FACE_IN_IDENTITY_STEP])
        # if not is_existed_fingerprint:
        #     errors.append(MESSAGE_STATUS[ERROR_APPROVAL_NO_FINGERPRINT_IN_IDENTITY_STEP])
        if not is_existed_signature:
            errors.append(MESSAGE_STATUS[ERROR_APPROVAL_NO_SIGNATURE_IN_IDENTITY_STEP])
        if errors:
            return self.response_exception(
                msg=ERROR_APPROVAL_NO_DATA_IN_IDENTITY_STEP,
                detail=', '.join(set(errors)),
                error_status_code=status.HTTP_403_FORBIDDEN
            )
        return face_transactions, fingerprint_transactions, signature_transactions

    async def ctr_get_business_jobs(self, booking_id: str, cif_id: str, business_type_code: str):
        # TODO: Kiểm tra booking_id, cif_id, business_type_code
        # Casa Account không cần cif_id
        if business_type_code not in BUSINESS_TYPES:
            self.response_exception(msg=ERROR_BUSINESS_TYPE_NOT_EXIST, loc=f'business_type_code: {business_type_code}')

        business_jobs = []
        if business_type_code == BUSINESS_TYPE_INIT_CIF:
            if not cif_id:
                return self.response_exception(msg=ERROR_CIF_ID_NOT_EXIST, loc="query -> cif_id")
            business_jobs = self.call_repos(await repos_get_business_jobs(
                cif_id=cif_id,
                session=self.oracle_session
            ))
        else:
            business_jobs = self.call_repos(await repos_get_business_jobs_by_open_casa(
                booking_id=booking_id,
                session=self.oracle_session
            ))

        business_job_codes = self.call_repos(await repos_get_business_job_codes(
            business_type_code=business_type_code,
            session=self.oracle_session
        ))

        mapping_datas = {}
        for business_job_code in business_job_codes:
            mapping_datas.update({business_job_code.code: INIT_RESPONSE})

        for business_job in business_jobs:
            mapping_datas[business_job.business_job_id] = dict(
                error_code=business_job.error_code,
                error_description=business_job.error_desc,
                status=business_job.complete_flag
            )

        response_datas = []
        for business_job_id, value in mapping_datas.items():
            job = dropdown(await self.get_model_object_by_id(
                model=BusinessJob, model_id=business_job_id, loc=f'business_job_id: {business_job_id}'
            ))
            response_datas.append(dict(
                job=job,
                status=value['status'],
                code=value['error_code'],
                description=value['error_description']
            ))

        return self.response(data=response_datas)
