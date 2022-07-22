from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.sub_info.repository import (
    repos_sub_info
)
from app.utils.constant.gw import GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE_OUT
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrSubInfo(BaseController):
    async def ctr_sub_info(self):
        current_user = self.current_user
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        gw_sub_infos = self.call_repos(
            await repos_sub_info(current_user=current_user))

        sub_infos = gw_sub_infos[GW_FUNC_SELECT_STAFF_OTHER_INFO_FROM_CODE_OUT]['data_output']['staff_other']
        recruitment_info = sub_infos['recruitment_info']

        return self.response_paging(data={
            "recruit_info": {
                "code": recruitment_info["recruitment_code"],
                "reason": recruitment_info["recruitment_reason"],
                "introducer": recruitment_info["recruitment_presenter"],
                "replacement_staff": recruitment_info["replace_staff"],
                "note": recruitment_info["recruitment_note"]
            },
            "other_info": {
                "other_info": recruitment_info["recruitment_other"],
                "dateoff": sub_infos["seniority_month"],
                "annual_leave": sub_infos["annual_number"]
            }
        } if sub_infos else {
            "recruit_info": {
                "code": None,
                "reason": None,
                "introducer": None,
                "replacement_staff": None,
                "note": None
            },
            "other_info": {
                "other_info": None,
                "dateoff": None,
                "annual_leave": None
            }
        })
