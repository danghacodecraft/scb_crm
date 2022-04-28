from app.api.base.controller import BaseController
from app.settings.event import service_dwh
from app.utils.error_messages import ERROR_CALL_SERVICE_DWH


class CtrBranchgeojson(BaseController):
    async def ctr_branchgeojson(self):
        is_success, branchgeojson = await service_dwh.branchgeojson()

        if not is_success:
            return self.response_exception(
                loc="branchgeojson",
                msg=ERROR_CALL_SERVICE_DWH,
                detail=str(branchgeojson)
            )

        return self.response(branchgeojson)
