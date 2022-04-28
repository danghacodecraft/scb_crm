from app.api.base.controller import BaseController
from app.settings.event import service_dwh
from app.utils.error_messages import ERROR_CALL_SERVICE_DWH


class CtrRegion(BaseController):
    async def ctr_region(self):
        is_success, region = await service_dwh.region()

        if not is_success:
            return self.response_exception(
                loc="region",
                msg=ERROR_CALL_SERVICE_DWH,
                detail=str(region)
            )

        return self.response(region)
