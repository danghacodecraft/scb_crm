from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.common_repository import (
    repos_get_next_receiver, repos_get_next_stage, repos_get_previous_stage,
    repos_get_previous_transaction_daily, repos_get_stage_information
)
from app.api.v1.endpoints.approval.repository import (
    repos_approval_get_face_authentication, repos_approve,
    repos_get_approval_identity_faces, repos_get_approval_process,
    repos_get_compare_image_transactions
)
from app.api.v1.endpoints.approval.schema import ApprovalRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.approval import (
    CIF_STAGE_APPROVE_KSS, CIF_STAGE_APPROVE_KSV, CIF_STAGE_BEGIN,
    CIF_STAGE_COMPLETED, CIF_STAGE_INIT
)
from app.utils.constant.cif import BUSINESS_TYPE_INIT_CIF, IMAGE_TYPE_FACE
from app.utils.error_messages import (
    ERROR_APPROVAL_INCORRECT_UPLOAD_FACE, ERROR_APPROVAL_UPLOAD_FACE,
    ERROR_CONTENT_NOT_NULL, ERROR_STAGE_COMPLETED, MESSAGE_STATUS
)
from app.utils.functions import generate_uuid, now, orjson_dumps, orjson_loads


class CtrApproval(BaseController):
    async def ctr_approval_process(self, cif_id: str):
        transactions = self.call_repos((await repos_get_approval_process(cif_id=cif_id, session=self.oracle_session)))
        response_data = []
        lst_parent = {}

        for _, _, _, _, transaction_root_daily in transactions:
            lst_parent.update({transaction_root_daily.created_at.date(): []})

        for parent_key, parent_value in lst_parent.items():
            childs = []

            for booking_customer, _, transaction_daily, transaction_sender, transaction_root_daily in transactions:
                content = orjson_loads(transaction_root_daily.data)
                if parent_key == transaction_root_daily.created_at.date():
                    childs.append({
                        "user_id": transaction_sender.user_id,
                        "full_name_vn": transaction_sender.user_fullname,
                        "avatar_url": None,
                        "position": {
                            "id": transaction_sender.position_id,
                            "code": transaction_sender.position_code,
                            "name": transaction_sender.position_name
                        },
                        "created_at": transaction_root_daily.created_at,
                        "content": content['content'] if content else ""
                    })
            response_data.append({
                "created_at": parent_key,
                "logs": childs
            })

        return self.response(data=response_data)

    async def ctr_get_approval(self, cif_id: str, amount: int):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        ################################################################################################################
        # THÔNG TIN XÁC THỰC
        ################################################################################################################
        # Khuôn mặt
        created_at = None
        identity_face_images = []
        identity_face_image_uuids = []
        image_uuids = []

        compare_face_uuid = None

        # Lấy tất cả hình ảnh ở bước GTDD
        face_transactions = self.call_repos(await repos_get_approval_identity_faces(
            cif_id=cif_id,
            session=self.oracle_session
        ))
        identity_image_ids = []
        for identity, identity_image in face_transactions:
            identity_face_uuid = identity_image.image_url
            created_at = identity_image.maker_at
            image_uuids.append(identity_face_uuid)
            identity_image_ids.append(identity_image.id)

        # Lấy hình ảnh so sánh, số nhiều nhưng cùng chung uuid
        compare_image_transactions = self.call_repos(await repos_get_compare_image_transactions(
            identity_image_ids=identity_image_ids,
            session=self.oracle_session
        ))

        distinct_identity_images = {}
        for compare_image, compare_image_transaction in compare_image_transactions:
            compare_face_uuid = compare_image_transaction.compare_image_url
            image_uuids.append(compare_image_transaction.compare_image_url)
            for identity, identity_image in face_transactions:
                if compare_image_transaction.identity_image_id == identity_image.id:
                    distinct_identity_images.update({
                        identity_image.image_url: compare_image_transaction.similar_percent
                    })
                    identity_face_image_uuids.append(compare_image_transaction.compare_image_url)
        image_uuids.extend(identity_face_image_uuids)

        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        for distinct_identity_image in distinct_identity_images:
            identity_face_images.append(dict(
                url=uuid__link_downloads[distinct_identity_image],
                similar_percent=distinct_identity_images[distinct_identity_image]
            ))

        face_authentication = dict(
            compare_face_url=uuid__link_downloads[compare_face_uuid] if compare_face_uuid else None,
            # compare_face_url=compare_face_url,
            compare_face_uuid=compare_face_uuid,
            created_at=created_at,
            identity_face_images=identity_face_images,
        )

        authentication = dict(
            face=face_authentication
        )

        ################################################################################################################

        ################################################################################################################
        # PHÊ DUYỆT
        ################################################################################################################

        # Kiểm tra xem đang ở bước nào của giao dịch
        _, _, previous_transaction_daily, previous_transaction_stage, _, previous_transaction_sender = self.call_repos(
            await repos_get_previous_stage(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        previous_stage_code = None
        stage_teller = dict()
        teller_is_disable = True
        teller_is_completed = False
        teller_content = None
        teller_created_at = None
        teller_created_by = None

        stage_supervisor = dict()
        supervisor_stage_code = None
        supervisor_is_disable = True
        supervisor_is_completed = False
        supervisor_content = None
        supervisor_created_at = None
        supervisor_created_by = None

        stage_audit = dict()
        audit_stage_code = None
        audit_is_disable = True
        audit_is_completed = False
        audit_content = None
        audit_created_at = None
        audit_created_by = None

        if previous_transaction_stage:
            previous_stage_code = previous_transaction_stage.transaction_stage_phase_code

        stages = []
        # GDV chưa gửi hồ sơ
        if previous_stage_code == CIF_STAGE_BEGIN:
            teller_is_disable = False
            teller_stage_code = None
        # KSV nhận hồ sơ từ GDV
        elif previous_stage_code == CIF_STAGE_INIT:
            teller_stage_code = previous_stage_code
            teller_is_completed = True
            teller_content = orjson_loads(previous_transaction_daily.data)["content"]
            teller_created_at = previous_transaction_daily.created_at
            teller_created_by = previous_transaction_sender.user_fullname

            supervisor_is_disable = False

        # KSS nhận hồ sơ từ KSV
        elif previous_stage_code == CIF_STAGE_APPROVE_KSV:
            audit_is_disable = False

            supervisor_stage_code = previous_stage_code
            supervisor_transaction_daily = previous_transaction_daily
            supervisor_transaction_sender = previous_transaction_sender
            supervisor_is_completed = True
            supervisor_content = orjson_loads(supervisor_transaction_daily.data)["content"]
            supervisor_created_at = supervisor_transaction_daily.created_at
            supervisor_created_by = supervisor_transaction_sender.user_fullname

            teller_transaction_daily, teller_transaction_sender, teller_transaction_stage, _ = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=supervisor_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            teller_stage_code = teller_transaction_stage.transaction_stage_phase_code
            teller_is_completed = True
            teller_content = orjson_loads(teller_transaction_daily.data)["content"]
            teller_created_at = teller_transaction_daily.created_at
            teller_created_by = teller_transaction_sender.user_fullname

        # KSS đã duyệt hồ sơ
        else:
            audit_stage_code = previous_stage_code
            audit_transaction_daily = previous_transaction_daily
            audit_transaction_sender = previous_transaction_sender
            audit_is_completed = True
            audit_content = orjson_loads(audit_transaction_daily.data)["content"]
            audit_created_at = audit_transaction_daily.created_at
            audit_created_by = audit_transaction_sender.user_fullname

            supervisor_transaction_daily, supervisor_transaction_sender, supervisor_transaction_stage, _ = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=audit_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            supervisor_stage_code = supervisor_transaction_stage.transaction_stage_phase_code
            supervisor_is_completed = True
            supervisor_content = orjson_loads(supervisor_transaction_daily.data)["content"]
            supervisor_created_at = supervisor_transaction_daily.created_at
            supervisor_created_by = supervisor_transaction_sender.user_fullname

            teller_transaction_daily, teller_transaction_sender, teller_transaction_stage, _ = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=supervisor_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            teller_stage_code = teller_transaction_stage.transaction_stage_phase_code
            teller_is_completed = True
            teller_content = orjson_loads(teller_transaction_daily.data)["content"]
            teller_created_at = teller_transaction_daily.created_at
            teller_created_by = teller_transaction_sender.user_fullname

        stage_teller.update(dict(
            stage_code=teller_stage_code,
            is_disable=teller_is_disable,
            is_completed=teller_is_completed,
            content=teller_content,
            created_at=teller_created_at,
            created_by=teller_created_by
        ))
        stage_supervisor.update(dict(
            stage_code=supervisor_stage_code,
            is_disable=supervisor_is_disable,
            is_completed=supervisor_is_completed,
            content=supervisor_content,
            created_at=supervisor_created_at,
            created_by=supervisor_created_by
        ))
        stage_audit.update(dict(
            stage_code=audit_stage_code,
            is_disable=audit_is_disable,
            is_completed=audit_is_completed,
            content=audit_content,
            created_at=audit_created_at,
            created_by=audit_created_by
        ))

        stages.extend([stage_teller, stage_supervisor, stage_audit])
        ################################################################################################################

        return self.response(data=dict(
            cif_id=cif_id,
            stages=stages,
            authentication=authentication
        ))

    async def ctr_approve(
            self,
            cif_id: str,
            request: ApprovalRequest
    ):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        current_user = self.current_user

        ################################################################################################################
        # THÔNG TIN XÁC THỰC
        ################################################################################################################

        ################################################################################################################
        # Khuôn mặt
        authentications = self.call_repos(await repos_approval_get_face_authentication(
            cif_id=cif_id,
            session=self.oracle_session
        ))

        face_authentications = {}
        for _, identity_image, identity_image_transaction, _, compare_image_transaction in authentications:
            if identity_image.image_type_id == IMAGE_TYPE_FACE:
                face_authentications.update({
                    identity_image_transaction.image_url: None
                })

        # Kiểm tra xem khuôn mặt đã upload chưa
        if not face_authentications:
            return self.response_exception(
                msg=ERROR_APPROVAL_UPLOAD_FACE,
                detail=MESSAGE_STATUS[ERROR_APPROVAL_UPLOAD_FACE]
            )

        _, _, _, _, new_compare_image_transaction = authentications[0]
        # Kiểm tra xem khuôn mặt gửi lên có đúng không
        # Hình ảnh kiểm tra sẽ là hình ảnh của lần Upload mới nhất
        if new_compare_image_transaction.compare_image_url != request.authentication.compare_face_image_uuid:
            return self.response_exception(
                msg=ERROR_APPROVAL_INCORRECT_UPLOAD_FACE,
                detail=MESSAGE_STATUS[ERROR_APPROVAL_INCORRECT_UPLOAD_FACE],
                loc="authentication -> compare_face_image_uuid"
            )

        # TODO: Vân Tay, Chữ Ký

        ################################################################################################################
        # PHÊ DUYỆT
        ################################################################################################################
        content = request.approval.content
        reject_flag = request.approval.reject_flag
        business_type_id = BUSINESS_TYPE_INIT_CIF

        _, _, _, previous_transaction_stage, _, _ = self.call_repos(
            await repos_get_previous_stage(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        ################################################################################################################
        # PREVIOUS STAGE
        ################################################################################################################
        is_stage_init = True
        previous_stage_code = None
        if previous_transaction_stage:
            is_stage_init = False
            _, previous_stage, _, _, _, _, _ = self.call_repos(
                await repos_get_stage_information(
                    business_type_id=business_type_id,
                    stage_id=previous_transaction_stage.transaction_stage_phase_code,
                    session=self.oracle_session
                ))
            previous_stage_code = previous_stage.code

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
            current_stage = self.call_repos(await repos_get_next_stage(
                business_type_id=business_type_id,
                current_stage_code=previous_stage_code,
                session=self.oracle_session
            ))
            current_stage_code = current_stage.code

        if current_stage_code == CIF_STAGE_COMPLETED:
            return self.response_exception(
                msg=ERROR_STAGE_COMPLETED,
                loc=f"current_stage: {current_stage_code}",
                detail=MESSAGE_STATUS[ERROR_STAGE_COMPLETED]
            )

        current_stage_status, current_stage, _, current_lane, _, current_phase, current_stage_role = self.call_repos(
            await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=current_stage_code,
                session=self.oracle_session
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

        if current_stage:
            current_stage_status_code = current_stage_status.code
            current_stage_status_name = current_stage_status.name
            current_stage_name = current_stage.name
            current_lane_code = current_lane.code
            current_lane_name = current_lane.name
            current_phase_code = current_phase.code
            current_phase_name = current_phase.name
            current_stage_role_code = current_stage_role.code
            current_stage_role_name = current_stage_role.name

        ################################################################################################################
        # NEXT STAGE
        ################################################################################################################
        next_stage = self.call_repos(await repos_get_next_stage(
            business_type_id=business_type_id,
            current_stage_code=current_stage_code,
            session=self.oracle_session
        ))
        next_stage_code = next_stage.code
        next_stage_role_code = None
        if next_stage_code != CIF_STAGE_COMPLETED:
            _, next_stage, _, _, _, _, next_stage_role = self.call_repos(await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=next_stage_code,
                session=self.oracle_session
            ))
            next_stage_role_code = next_stage_role.code

        saving_transaction_stage_status_id = generate_uuid()
        saving_transaction_stage_id = generate_uuid()
        saving_transaction_stage_lane_id = generate_uuid()
        saving_transaction_stage_phase_id = generate_uuid()
        saving_transaction_stage_role_id = generate_uuid()
        transaction_daily_id = generate_uuid()

        saving_transaction_stage_status = dict(
            id=saving_transaction_stage_status_id,
            code=current_stage_status_code,
            name=current_stage_status_name
        )

        saving_transaction_stage_lane = dict(
            id=saving_transaction_stage_lane_id,
            code=current_lane_code,
            name=current_lane_name
        )

        saving_transaction_stage_phase = dict(
            id=saving_transaction_stage_phase_id,
            code=current_phase_code,
            name=current_phase_name
        )

        saving_transaction_stage_role = dict(
            id=saving_transaction_stage_role_id,
            code=current_stage_role_code,
            name=current_stage_role_name
        )

        saving_transaction_stage = dict(
            id=saving_transaction_stage_id,
            status_id=saving_transaction_stage_status_id,
            lane_id=saving_transaction_stage_lane_id,
            phase_id=saving_transaction_stage_phase_id,
            business_type_id=business_type_id,
            sla_transaction_id=None,  # TODO
            transaction_stage_phase_code=current_stage_code,
            transaction_stage_phase_name=current_stage_name
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
            is_reject=False,
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
            position_name=current_user.hrm_position_name
        )

        receiver_branch = None
        receiver_lane = self.call_repos(await repos_get_next_receiver(
            business_type_id=business_type_id,
            current_stage_id=current_stage_code,
            reject_flag=reject_flag,
            session=self.oracle_session
        ))
        if receiver_lane:
            receiver_branch = await self.get_model_object_by_id(
                model_id=receiver_lane.branch_id,
                model=Branch,
                loc="next_receiver -> branch_id"
            )
            # receiver_department = await self.get_model_object_by_id(
            #     model_id=next_receiver.department_id,
            #     model=Department,
            #     loc="next_receiver -> department_id"
            # )

        saving_transaction_receiver = dict(
            transaction_id=transaction_daily_id,
            user_id=current_user.code,
            user_name=current_user.username,
            user_fullname=current_user.name,
            user_email=current_user.email,
            branch_id=receiver_branch.id if receiver_lane else None,
            branch_code=receiver_branch.code if receiver_lane else None,
            branch_name=receiver_branch.name if receiver_lane else None,
            department_id=receiver_lane.department_id if receiver_lane else None,
            department_code=None,  # TODO
            department_name=None,  # TODO
            position_id=None,  # TODO
            position_code=None,  # TODO
            position_name=None  # TODO
        )

        approval_process = self.call_repos((await repos_approve(
            cif_id=cif_id,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_transaction_receiver=saving_transaction_receiver,
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
        if current_stage_code == CIF_STAGE_INIT:
            description = f"{current_stage_role_code} đã gửi hồ sơ cho {next_stage_role_code}."
        else:
            # KSV
            if current_stage_code == CIF_STAGE_APPROVE_KSV:
                if not reject_flag:
                    description = f"Hoàn tất hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role_code}" \
                                  f". Hồ sơ đã gửi cho {next_stage_role_code}."
                else:
                    if not content:
                        return self.response_exception(msg=ERROR_CONTENT_NOT_NULL, loc="content")
                    description = f"Hồ sơ bị từ chối. Lý do: {content}"
            # KSS
            elif current_stage_code == CIF_STAGE_APPROVE_KSS:
                if not reject_flag:
                    description = f"Hoàn thành hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role_code}."
                else:
                    if not content:
                        return self.response_exception(msg=ERROR_CONTENT_NOT_NULL, loc="content")
                    description = f"Hồ sơ bị từ chối. Lý do: {content}"
            else:
                return self.response_exception(msg=ERROR_STAGE_COMPLETED, loc="description")

        return description
