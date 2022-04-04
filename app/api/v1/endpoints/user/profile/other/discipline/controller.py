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

        return self.response_paging(data=[{
            "effective_date": datetime_to_date(string_to_datetime(discipline["NGAY_HIEU_LUC"]))
            if discipline["NGAY_HIEU_LUC"] else None,
            "end_date": datetime_to_date(string_to_datetime(discipline["NGAY_KET_THUC"]))
            if discipline["NGAY_KET_THUC"] else None,
            "titles": discipline["CHUC_DANH"],
            "department": discipline["DON_VI_PHONG_BAN"],
            "reasons": discipline["LY_DO_KY_LUAT"],
            "detailed_reason": discipline["LY_DO_CHI_TIET_KY_LUAT"],
            "detected_date": discipline["NGAY_PHAT_HIEN"],
            "violation_date": discipline["NGAY_VI_PHAM"],
            "total_damage": discipline["TONG_GIA_TRI_THIET_HAI"],
            "number": discipline["SO_QUYET_DINH"],
            # "deleter": # TODO không có người xóa kỷ luật
            "signer": discipline["NGAY_PHAT_HIEN"],
        } for discipline in disciplines])
