from pydantic import Field

from app.api.base.schema import BaseSchema
from app.utils.constant.business_type import BUSINESS_TYPES
from app.utils.functions import make_description_from_dict


class CreateBookingRequest(BaseSchema):
    business_type_code: str = Field(..., description=f"Loại nghiệp vụ: {make_description_from_dict(BUSINESS_TYPES)}")


class CreateBookingResponse(BaseSchema):
    booking_id: str = Field(..., description="Booking ID")


class NewsCommentResponse(BaseSchema):
    comment_id: str = Field(..., description="id tin tức")


class NewsCommentRequest(BaseSchema):
    content: str = Field(..., description='Nội dung comment')
