from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.cv.contact_info.repository import (
    repos_contact_info
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrContact_Info(BaseController):
    async def ctr_contact_info(self):
        if not self.current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = self.current_user.code

        is_success, contact_info = self.call_repos(
            await repos_contact_info(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(contact_info))

        domicile = dict(
            number_and_street=None,
            nationality=None,
            province=None,
            district=None,
            ward=None
        )
        response_contact = dict(
            domicile=domicile,
            resident=domicile,
            temporary=domicile,
            contact=domicile
        )

        response_contact_other = dict(
            contactor=None,
            relationship=None,
            mobile_number=None
        )
        response_guardian = dict(
            guardian=None,
            relationship=None,
            mobile_number=None
        )
        response_other = dict(
            contact=response_contact_other,
            guardian=response_guardian,
            expiration_date=None
        )
        response_contact_info = dict(
            contact_info=response_contact,
            other_info=response_other,
        )

        if contact_info:
            domicile_contact = contact_info['curriculum_vitae']['contact']['per']
            resident_contact = contact_info['curriculum_vitae']['contact']['per']
            temporary_contact = contact_info['curriculum_vitae']['contact']['per']
            contact_contact = contact_info['curriculum_vitae']['contact']['per']
            contactor = contact_info['curriculum_vitae']['contact']['family']

            response_contact_info = {
                "contact_info": {
                    "domicile": {
                        "number_and_street": domicile_contact['address'],
                        "nationality": domicile_contact['nation'],
                        "province": domicile_contact['province'],
                        "district": domicile_contact['ward'],
                        "ward": domicile_contact['address']
                    },
                    "resident": {
                        "number_and_street": resident_contact['address'],
                        "nationality": resident_contact['nation'],
                        "province": resident_contact['province'],
                        "district": resident_contact['ward'],
                        "ward": resident_contact['address']
                    },
                    "temporary": {
                        "number_and_street": temporary_contact['address'],
                        "nationality": temporary_contact['nation'],
                        "province": temporary_contact['province'],
                        "district": temporary_contact['ward'],
                        "ward": temporary_contact['address']
                    },
                    "contact": {
                        "number_and_street": contact_contact['address'],
                        "nationality": contact_contact['nation'],
                        "province": contact_contact['province'],
                        "district": contact_contact['ward'],
                        "ward": contact_contact['address']
                    }
                },
                "other_info": {
                    "contact": {
                        "contactor": contactor['name'],
                        "relationship": contactor['relation'],
                        "mobile_number": contactor['phone']
                    },
                    "guardian": {  # Todo Người bảo lãnh không tìm thấy
                        "guardian": "Nguyễn Xuân An",
                        "relationship": "Bạn bè",
                        "mobile_number": "0909125649"
                    },
                    "expiration_date": "2021-10-01"  # Todo Ngày hết hiệu lực
                }
            }

        return self.response(data=response_contact_info)
