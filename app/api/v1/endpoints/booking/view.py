from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.booking.controller import CtrNewsComment
from app.api.v1.endpoints.booking.schema import (
    CreateBookingRequest, CreateBookingResponse, NewsCommentRequest,
    NewsCommentResponse
)
from app.api.v1.others.booking.controller import CtrBooking

router = APIRouter()


@router.post(
    path="/",
    name="Tạo Booking",
    description="Tạo Booking",
    responses=swagger_response(
        response_model=ResponseData[CreateBookingResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_booking(
        request: CreateBookingRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    create_booking_data = await CtrBooking(current_user).ctr_create_booking(
        business_type_code=request.business_type_code
    )
    return ResponseData[CreateBookingResponse](**create_booking_data)


@router.post(
    path="/{booking_id}/comment/",
    name="Tạo bình luận",
    description="Tạo bình luận",
    responses=swagger_response(
        response_model=ResponseData[NewsCommentResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_news_comment(
        data_request: NewsCommentRequest,
        booking_id: str = Path(..., description='Booking ID'),
        current_user=Depends(get_current_user_from_header()),

):
    news_comment = await CtrNewsComment(current_user).ctr_news_comment(data_comment=data_request, booking_id=booking_id)
    return ResponseData(**news_comment)
