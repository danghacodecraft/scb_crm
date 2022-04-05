from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.discipline.repository import (
    repos_discipline
)
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrDiscipline(BaseController):
    async def ctr_discipline(self, employee_id: str):
        is_success, disciplines = self.call_repos(
            await repos_discipline(
                employee_id=employee_id
            )
        )
        if not is_success:
            self.response_exception(msg=str(disciplines))

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
                effective_date = discipline["NGAY_HIEU_LUC"]
                effective_date = datetime_to_date(string_to_datetime(effective_date)) if effective_date else None

                end_date = discipline["NGAY_KET_THUC"]
                end_date = datetime_to_date(string_to_datetime(end_date)) if end_date else None

                titles = discipline["CHUC_DANH"]
                department = discipline["DON_VI_PHONG_BAN"]
                reason = discipline["LY_DO_KY_LUAT"]
                detailed_reason = discipline["LY_DO_CHI_TIET_KY_LUAT"]
                detected_date = discipline["NGAY_PHAT_HIEN"]
                violation_date = discipline["NGAY_VI_PHAM"]
                total_damage = discipline["TONG_GIA_TRI_THIET_HAI"]
                number = discipline["SO_QUYET_DINH"]
                deleter = None  # TODO không có người xóa kỷ luật
                signer = discipline["NGAY_PHAT_HIEN"]

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
