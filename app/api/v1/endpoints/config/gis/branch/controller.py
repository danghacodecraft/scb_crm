from app.api.base.controller import BaseController
from app.settings.event import service_dwh
from app.utils.error_messages import ERROR_CALL_SERVICE_DWH


class CtrBranch(BaseController):
    async def ctr_branch(self):
        is_success, branch = await service_dwh.branch()

        if not is_success:
            return self.response_exception(
                loc="branch",
                msg=ERROR_CALL_SERVICE_DWH,
                detail=str(branch)
            )

        return self.response(branch)
