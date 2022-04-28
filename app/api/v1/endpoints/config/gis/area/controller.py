from app.api.base.controller import BaseController
from app.settings.event import service_dwh
from app.utils.error_messages import ERROR_CALL_SERVICE_DWH


class CtrArea(BaseController):
    async def ctr_area(self):
        is_success, area = await service_dwh.area()

        if not is_success:
            return self.response_exception(
                loc="area",
                msg=ERROR_CALL_SERVICE_DWH,
                detail=str(area)
            )

        return self.response(area)
