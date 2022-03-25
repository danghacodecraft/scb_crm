from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.form.repository import (
    repos_get_approval_form
)


class CtrApprovalFormResponse(BaseController):
    async def ctr_get_approval_form(self):
        approval_form_info = self.call_repos(await repos_get_approval_form())
        return self.response(data=approval_form_info)
