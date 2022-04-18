from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.sub_info.repository import (
    repos_sub_info
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrSubInfo(BaseController):
    async def ctr_sub_info(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        is_success, sub_infos = self.call_repos(
            await repos_sub_info(
                employee_id=employee_id
            )
        )
        if not is_success:
            return self.response_exception(msg=str(sub_infos))

        return self.response_paging(data={
            "recruit_info": {
                "code": sub_infos[0]["MA_TUYEN_DUNG"],
                "reason": sub_infos[0]["LY_DO_TUYEN_DUNG"],
                "introducer": sub_infos[0]["NGUOI_GIOI_THIEU"],
                "replacement_staff": sub_infos[0]["NV_THAY_THE"],
                "note": sub_infos[0]["NOTE"]
            },
            "other_info": {
                "other_info": sub_infos[0]["THONG_TIN_KHAC"],
                "dateoff": sub_infos[0]["THAM_NIEN_THEM"],
                "annual_leave": sub_infos[0]["PHEP_NAM_UU_DAI"]
            }
        } if len(sub_infos) > 0 else {
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
