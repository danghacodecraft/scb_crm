from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.felicitation.repository import (
    repos_felicitation
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrFelicitation(BaseController):
    async def ctr_felicitation(self):
        current_user = self.current_user
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        gw_felicitations = self.call_repos(await repos_felicitation(current_user=current_user))

        felicitations = gw_felicitations['selectRewardInfoFromCode_out']['data_output'][
            'reward_info_list']['reward_info_item']

        response_felicitations = [dict(
            effective_date=None,
            decision_number=None,
            titles=None,
            commend_level=None,
            title=None,
            department=None,
            reason=None,
            formality=None,
            amount=None,
            sign_date=None,
            signer=None
        )]

        if felicitations:
            response_felicitations = []
            for felicitation in felicitations:
                effective_date = felicitation["reward_effect_date"]
                effective_date = datetime_to_date(string_to_datetime(effective_date)) if effective_date else None
                decision_number = felicitation["reward_num"]
                titles = felicitation["reward_title"]
                commend_level = felicitation["reward_level"]
                title = felicitation["reward_jobtitle"]
                department = felicitation["reward_department"]
                reason = felicitation["reward_reason"]
                formality = felicitation["reward_form"]
                amount = felicitation["reward_of_amount"]
                sign_date = felicitation["reward_signing_date"]
                sign_date = datetime_to_date(string_to_datetime(sign_date)) if sign_date else None
                signer = felicitation["reward_signer"]

                response_felicitations.append(dict(
                    effective_date=effective_date,
                    decision_number=decision_number,
                    titles=titles,
                    commend_level=commend_level,
                    title=title,
                    department=department,
                    reason=reason,
                    formality=formality,
                    amount=amount,
                    sign_date=sign_date,
                    signer=signer
                ))

        return self.response(data=response_felicitations)
