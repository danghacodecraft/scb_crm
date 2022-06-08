from pydantic import Field

from app.api.base.schema import BaseSchema


class SaveCasaSuccessResponse(BaseSchema):
    account_id: str = Field(..., description="Mã TKTT")
