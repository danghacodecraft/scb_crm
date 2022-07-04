from app.api.base.controller import BaseController


class CtrConfigDeposit(BaseController):
    async def ctr_get_rollover_type(self):
        rollover_type = [
            {
                "id": "I",
                "code": "I",
                "name": "Tái ký gốc + lãi"
            },
            {
                "id": "P",
                "code": "P",
                "name": "Tái ký gốc"
            }
        ]
        return self.response(data=rollover_type)
