from pydantic import Field

from app.api.base.schema import BaseSchema


class ApprovalFaceSuccess(BaseSchema):
    cif_id: str = Field(..., description='Id CIF ảo')
