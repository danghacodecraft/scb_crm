from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.felicitation.repository import (
    repos_felicitation
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrFelicitation(BaseController):
    async def ctr_felicitation(self):
        if not self.current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = self.current_user.code

        is_success, felicitations = self.call_repos(
            await repos_felicitation(
                employee_id=employee_id
            )
        )

        if not is_success:
            return self.response_exception(msg=str(felicitations))

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
                effective_date = felicitation["NGAY_HIEU_LUC"]
                effective_date = datetime_to_date(string_to_datetime(effective_date)) if effective_date else None
                decision_number = felicitation["SO_QUYET_DINH"]
                titles = felicitation["DANH_HIEU"]
                commend_level = felicitation["CAP_KHEN_THUONG"]
                title = felicitation["CHUC_DANH"]
                department = felicitation["DON_VI_PHONG_BAN"]
                reason = felicitation["LY_DO_KHEN_TUONG"]
                formality = felicitation["HINH_THUC_KHEN_THUONG"]
                amount = felicitation["SO_TIEN_THUONG"]
                sign_date = felicitation["NGAY_KY"]
                sign_date = datetime_to_date(string_to_datetime(sign_date)) if sign_date else None
                signer = felicitation["NGUOI_KY"]

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
