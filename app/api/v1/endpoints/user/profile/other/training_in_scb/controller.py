from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.training_in_scb.repository import (
    repos_training_in_scb
)
from app.utils.constant.gw import GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE_OUT
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrTrainingInSCB(BaseController):
    async def ctr_training_in_scb(self):
        current_user = self.current_user
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        gw_training_in_scbs = self.call_repos(await repos_training_in_scb(current_user=current_user))

        training_in_scbs = gw_training_in_scbs[GW_FUNC_SELECT_TOPIC_INFO_FROM_CODE_OUT]['data_output'][
            'topic_info_list']['topic_info_item']

        response_training_in_scbs = [dict(
            topic=None,
            code=None,
            name=None,
            from_date=None,
            to_date=None,
            result=None
        )]

        if training_in_scbs:

            response_training_in_scbs = []
            for training_in_scb in training_in_scbs:
                topic = training_in_scb["topic_description"]
                code = training_in_scb["topic_code"]
                name = training_in_scb["topic_name"]

                from_date = training_in_scb["from_date"]
                from_date = datetime_to_date(string_to_datetime(from_date)) if from_date else None

                to_date = training_in_scb["to_date"]
                to_date = datetime_to_date(string_to_datetime(to_date)) if to_date else None

                result = training_in_scb["topic_result"]

                response_training_in_scbs.append(dict(
                    topic=topic,
                    code=code,
                    name=name,
                    from_date=from_date,
                    to_date=to_date,
                    result=result
                ))

        return self.response(data=response_training_in_scbs)
