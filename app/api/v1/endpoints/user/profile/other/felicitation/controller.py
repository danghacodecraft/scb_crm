from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.felicitation.repository import (
    repos_felicitation
)
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrFelicitation(BaseController):
    async def ctr_felicitation(self, employee_id: str):
        is_success, felicitations = self.call_repos(
            await repos_felicitation(
                employee_id=employee_id
            )
        )

        if not is_success:
            return self.response_exception(msg=str(felicitations))

        return self.response_paging(data=[{
            "effective_date": datetime_to_date(string_to_datetime(felicitation["NGAY_HIEU_LUC"]))
            if felicitation["NGAY_HIEU_LUC"] else None,
            "decision_number": felicitation["SO_QUYET_DINH"],
            "titles": felicitation["DANH_HIEU"],
            "commend_level": felicitation["CAP_KHEN_THUONG"],
            "title": felicitation["CHUC_DANH"],
            "department": felicitation["DON_VI_PHONG_BAN"],
            "reason": felicitation["LY_DO_KHEN_TUONG"],
            "formality": felicitation["HINH_THUC_KHEN_THUONG"],
            "amount": felicitation["SO_TIEN_THUONG"],
            "sign_date": datetime_to_date(string_to_datetime(felicitation["NGAY_KY"]))
            if felicitation["NGAY_KY"] else None,
            "signer": felicitation["NGUOI_KY"]
        } for felicitation in felicitations])
