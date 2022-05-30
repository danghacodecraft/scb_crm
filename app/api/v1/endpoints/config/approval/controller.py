from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.approval.repository import (
    repos_get_stage_action
)
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import (
    StageAction, StageStatus
)
from app.utils.constant.approval import CIF_APPROVE_STAGES
from app.utils.error_messages import ERROR_APPROVAL_STAGE_NOT_EXISTED


class CtrConfigApproval(BaseController):
    async def ctr_stage_action(self, stage_code: str):
        if stage_code:
            if stage_code not in CIF_APPROVE_STAGES:
                return self.response_exception(msg=ERROR_APPROVAL_STAGE_NOT_EXISTED)
            stage_action_info = self.call_repos(await repos_get_stage_action(
                stage_code=stage_code,
                session=self.oracle_session
            ))
        else:
            stage_action_info = self.call_repos(
                await repos_get_data_model_config(
                    session=self.oracle_session,
                    model=StageAction
                )
            )
        return self.response(stage_action_info)

    async def ctr_stage_status(self):
        stage_action_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=StageStatus
            )
        )
        return self.response(stage_action_info)
