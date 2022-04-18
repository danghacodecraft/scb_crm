from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.other_information.repository import (
    repos_other_info, repos_update_other_info
)
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationUpdateRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.others import HrmEmployee


class CtrOtherInfo(BaseController):
    async def ctr_other_info(self, cif_id: str):
        other_information = self.call_repos(await repos_other_info(cif_id, self.oracle_session))
        return self.response(other_information)

    async def ctr_update_other_info(self, cif_id: str, update_other_info_req: OtherInformationUpdateRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        hrm_employee_ids = []
        if update_other_info_req.sale_staff:
            hrm_employee_ids.append(update_other_info_req.sale_staff.id)
        if update_other_info_req.indirect_sale_staff:
            hrm_employee_ids.append(update_other_info_req.indirect_sale_staff.id)

        # check exist hrm_employee_ids
        await self.get_model_objects_by_ids(model_ids=hrm_employee_ids, model=HrmEmployee, loc='staff_id')

        update_other_info = self.call_repos(
            await repos_update_other_info(
                cif_id=cif_id,
                update_other_info_req=update_other_info_req,
                current_user=self.current_user.user_info,
                session=self.oracle_session
            )
        )

        return self.response(update_other_info)
