from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.others import StageAction
from app.utils.functions import dropdown


async def repos_get_stage_action(stage_code: str, session: Session):
    stage_action_datas = session.execute(
        select(
            StageAction
        )
        .filter(
            StageAction.stage_id == stage_code
        )
    ).scalars().all()
    return ReposReturn(data=[dropdown(stage_action_data) for stage_action_data in stage_action_datas])
