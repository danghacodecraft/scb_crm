from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import StageAction


class CtrStageAction(BaseController):
    async def ctr_stage_action(self):
        stage_action_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=StageAction
            )
        )
        return self.response(stage_action_info)
