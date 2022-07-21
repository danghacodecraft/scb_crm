from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.discipline.repository import (
    repos_discipline
)
from app.utils.constant.gw import GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE_OUT
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrDiscipline(BaseController):
    async def ctr_discipline(self):
        current_user = self.current_user
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        gw_disciplines = self.call_repos(await repos_discipline(current_user=current_user))

        disciplines = gw_disciplines[GW_FUNC_SELECT_DISCIPLINE_INFO_FROM_CODE_OUT]['data_output'][
            'discipline_info_list']['discipline_info_item']

        response_disciplines = [dict(
            effective_date=None,
            end_date=None,
            titles=None,
            department=None,
            reason=None,
            detailed_reason=None,
            detected_date=None,
            violation_date=None,
            total_damage=None,
            number=None,
            deleter=None,
            signer=None
        )]

        if disciplines:
            response_disciplines = []
            for discipline in disciplines:
                effective_date = discipline["discipline_effect_date"]
                effective_date = datetime_to_date(string_to_datetime(effective_date)) if effective_date else None

                end_date = discipline["discipline_expire_date"]
                end_date = datetime_to_date(string_to_datetime(end_date)) if end_date else None

                titles = discipline["discipline_jobtitle"]
                department = discipline["discipline_department"]
                reason = discipline["discipline_reason"]
                detailed_reason = discipline["discipline_description"]
                detected_date = discipline["detection_date"]
                violation_date = discipline["violation_date"]
                total_damage = discipline["discipline_total"]
                number = discipline["discipline_num"]
                deleter = discipline["discipline_remover"]
                signer = discipline["discipline_signer"]

                response_disciplines.append(dict(
                    effective_date=effective_date,
                    end_date=end_date,
                    titles=titles,
                    department=department,
                    reason=reason,
                    detailed_reason=detailed_reason,
                    detected_date=detected_date,
                    violation_date=violation_date,
                    total_damage=total_damage,
                    number=number,
                    deleter=deleter,
                    signer=signer
                ))

        return self.response_paging(data=response_disciplines)
