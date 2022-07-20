from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.approval.repository import (
    repos_get_stage_action
)
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import StageStatus


class CtrConfigApproval(BaseController):
    async def ctr_stage_action(self, business_type_code: str, role_code: str):
        stage_action_info = self.call_repos(await repos_get_stage_action(
            business_type_code=business_type_code,
            role_code=role_code,
            session=self.oracle_session
        ))
        return self.response(stage_action_info)

    async def ctr_stage_status(self):
        stage_action_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=StageStatus
            )
        )
        return self.response(stage_action_info)
