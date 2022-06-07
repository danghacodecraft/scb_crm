from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.template.folder.repository import (
    repos_get_approval_template_folder_info
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.cif.basic_information.model import Customer


class CtrTemplateFolder(BaseController):
    async def ctr_get_approval_template_folder_info(self, cif_id: str):
        # check cif tồn tại
        await self.get_model_object_by_id(model_id=cif_id, model=Customer, loc="cif_id")

        approval_form_info = self.call_repos(await repos_get_approval_template_folder_info(cif_id=cif_id))
        return self.response(data=approval_form_info)
