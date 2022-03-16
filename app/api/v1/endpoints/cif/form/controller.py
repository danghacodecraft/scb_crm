from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_current_stage, repos_get_next_receiver, repos_get_next_stage,
    repos_get_stage_information, repos_get_previous_stage
)
from app.api.v1.endpoints.cif.form.repository import (
    repos_approval_process, repos_approve
)
from app.api.v1.endpoints.cif.form.schema import CifApproveRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.approval import (
    CIF_STAGE_APPROVE_KSS, CIF_STAGE_APPROVE_KSV, CIF_STAGE_INIT
)
from app.utils.constant.cif import BUSINESS_TYPE_INIT_CIF
from app.utils.functions import generate_uuid, now


class CtrForm(BaseController):
    async def ctr_approval_process(self, cif_id: str):
        approval_process = self.call_repos((await repos_approval_process(cif_id)))
        return self.response(approval_process)

    async def ctr_approve(
            self,
            cif_id: str,
            request: CifApproveRequest
    ):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        content = request.content
        reject_flag = request.reject_flag
        business_type_id = BUSINESS_TYPE_INIT_CIF
        current_user = self.current_user

        booking_customer, booking, transaction_daily, current_stage, current_stage_status = self.call_repos(
            await repos_get_current_stage(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        is_stage_init = False
        # Nếu là Bước đầu tiên - GDV Gửi hồ sơ để phê duyệt
        if not current_stage:
            is_stage_init = True
            current_stage_code = CIF_STAGE_INIT
        else:
            current_stage_code = current_stage.transaction_stage_phase_code

        previous_stage_status, previous_stage = self.call_repos(await repos_get_previous_stage(
            business_type_id=business_type_id,
            current_stage_code=current_stage_code,
            session=self.oracle_session
        ))
        (previous_stage_status, previous_stage, previous_stage_lane, previous_lane, previous_stage_phase, previous_phase, previous_stage_role) = self.call_repos(
            await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=previous_stage.code,
                session=self.oracle_session
            ))
        print("-------------------------PREVIOUS STAGE-------------------------------------------------------")
        print(previous_stage_status.id, previous_stage.id, previous_stage_lane.lane_id, previous_lane.id,
              previous_stage_phase.phase_id,
              previous_phase.id, previous_stage_role.code)

        current_stage_status, current_stage, current_stage_lane, current_lane, current_stage_phase, current_phase, current_stage_role = self.call_repos(
            await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=current_stage_code,
                session=self.oracle_session
            ))
        print("-------------------------CURRENT STAGE-------------------------------------------------------")
        print(current_stage_status.id, current_stage.id, current_stage_lane.lane_id, current_lane.id,
              current_stage_phase.phase_id,
              current_phase.id, current_stage_role.code)

        next_stage_status, next_stage = self.call_repos(await repos_get_next_stage(
            business_type_id=business_type_id,
            current_stage_code=current_stage_code,
            session=self.oracle_session
        ))

        next_stage_status, next_stage, next_stage_lane, next_lane, next_stage_phase, next_phase, next_stage_role = self.call_repos(
            await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=next_stage.id,
                session=self.oracle_session
            ))
        print("-------------------------NEXT STAGE-------------------------------------------------------")
        print(next_stage_status.id, next_stage.id, next_stage_lane.lane_id, next_lane.id,
              next_stage_phase.phase_id,
              next_phase.id, next_stage_role.code)

        saving_transaction_stage_status_id = generate_uuid()
        saving_transaction_stage_id = generate_uuid()
        saving_transaction_stage_lane_id = generate_uuid()
        saving_transaction_stage_phase_id = generate_uuid()
        saving_transaction_stage_role_id = generate_uuid()
        transaction_daily_id = generate_uuid()

        saving_transaction_stage_status = dict(
            id=saving_transaction_stage_status_id,
            code=current_stage_status.code,
            name=current_stage_status.name
        )

        saving_transaction_stage_lane = dict(
            id=saving_transaction_stage_lane_id,
            code=current_lane.code,
            name=current_lane.name
        )

        saving_transaction_stage_phase = dict(
            id=saving_transaction_stage_phase_id,
            code=current_phase.code,
            name=current_phase.name
        )

        saving_transaction_stage_role = dict(
            id=saving_transaction_stage_role_id,
            code=current_stage_role.code,
            name=current_stage_role.name
        )

        saving_transaction_stage = dict(
            id=saving_transaction_stage_id,
            status_id=saving_transaction_stage_status_id,
            lane_id=saving_transaction_stage_lane_id,
            phase_id=saving_transaction_stage_phase_id,
            business_type_id=business_type_id,
            sla_transaction_id=None,  # TODO
            transaction_stage_phase_code=current_stage.code,
            transaction_stage_phase_name=current_stage.name
        )

        json_data = dict(content=content)
        is_completed_cif = False
        # GDV
        if current_stage_code == CIF_STAGE_INIT:
            description = f"{current_stage_role.code} đã gửi hồ sơ cho {next_stage_role.code}."
            print(current_stage_code)
            print("GDV")
        else:
            # KSV
            if current_stage_code == CIF_STAGE_APPROVE_KSV:
                if not reject_flag:
                    description = f"Hoàn tất hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role.code}. Hồ sơ đã gửi cho {next_stage_role.code}."
                else:
                    if not content:
                        return self.response_exception(msg="Content Not None", loc="content")
                    description = f"Hồ sơ bị từ chối."
                print(current_stage_code)
                print("KSV")
            # KSS
            elif current_stage_code == CIF_STAGE_APPROVE_KSS:
                if not reject_flag:
                    is_completed_cif = True
                    description = f"Hoàn thành hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role.code}."
                else:
                    if not content:
                        return self.response_exception(msg="Content Not None", loc="content")
                    description = f"Hồ sơ bị từ chối."
                print(current_stage_code)
                print("KSS")
            else:
                print(current_stage_code)
                return self.response_exception(msg="Stage has been completed")

        saving_transaction_daily = dict(
            transaction_id=transaction_daily_id,
            transaction_stage_id=saving_transaction_stage_id,
            transaction_parent_id=None,
            transaction_root_id=None,
            is_reject=False,
            data=str(json_data),
            description=description,
            created_at=now(),
            updated_at=now()
        )

        # sender_branch = await self.get_model_object_by_id(
        #     model_id=current_user.branch_id,
        #     model=Branch,
        #     loc="stage_lane"
        # )

        # sender_department = await self.get_model_object_by_id(
        #     model_id=stage_lane.department_id,
        #     model=Department,
        #     loc="stage_lane"
        # )

        saving_transaction_sender = dict(
            transaction_id=transaction_daily_id,
            user_id=current_user.user_id,
            user_name=current_user.username,
            user_fullname=current_user.full_name_vn,
            user_email=current_user.email,
            branch_id=None,  # TODO
            branch_code=None,  # TODO
            branch_name=None,  # TODO
            department_id=None,  # TODO
            department_code=None,  # TODO
            department_name=None,  # TODO
            position_id=None,  # TODO
            position_code=None,  # TODO
            position_name=None  # TODO
        )

        receiver = None
        receiver_branch = None
        if not is_completed_cif:
            _, receiver = self.call_repos(await repos_get_next_receiver(
                business_type_id=business_type_id,
                stage_id=next_stage.code,
                reject_flag=reject_flag,
                session=self.oracle_session
            ))

            receiver_branch = await self.get_model_object_by_id(
                model_id=receiver.branch_id,
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
            user_id=current_user.user_id,
            user_name=current_user.username,
            user_fullname=current_user.full_name_vn,
            user_email=current_user.email,
            branch_id=receiver_branch.id if receiver else None,
            branch_code=receiver_branch.code if receiver else None,
            branch_name=receiver_branch.name if receiver else None,
            department_id=receiver.department_id if receiver else None,
            department_code=None,  # TODO
            department_name=None,  # TODO
            position_id=None,  # TODO
            position_code=None,  # TODO
            position_name=None  # TODO
        )

        print("saving_transaction_stage_status", saving_transaction_stage_status)
        print("saving_transaction_stage_lane", saving_transaction_stage_lane)
        print("saving_transaction_stage_phase", saving_transaction_stage_phase)
        print("saving_transaction_stage_role", saving_transaction_stage_role)
        print("saving_transaction_stage", saving_transaction_stage)
        print("saving_transaction_daily", saving_transaction_daily)
        print("saving_transaction_sender", saving_transaction_sender)
        print("saving_transaction_receiver", saving_transaction_receiver)

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
            previous_stage=previous_stage.code,
            current_stage=current_stage_code,
            next_stage=next_stage.code,
        )

        return self.response(approval_process)
