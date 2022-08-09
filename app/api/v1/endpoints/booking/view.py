from typing import List

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.booking.controller import CtrNewsComment, CtrNewState
from app.api.v1.endpoints.booking.schema import (
    CommentResponse, CreateBookingRequest, CreateBookingResponse,
    NewsCommentRequest, NewsCommentResponse, StateResponse
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
        business_type_code=request.business_type_code,
        booking_code_flag=True
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


@router.get(
    path="/{booking_id}/comment/",
    name="Thông tin bình luận",
    description="Thông tin bình luận",
    responses=swagger_response(
        response_model=ResponseData[List[CommentResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_comment_by_news(
        booking_id: str = Path(..., description='Booking ID'),
        current_user=Depends(get_current_user_from_header()),

):
    news_comment = await CtrNewsComment(current_user).ctr_get_comment_by_booking_id(booking_id=booking_id)
    return ResponseData[List[CommentResponse]](**news_comment)


@router.post(
    path="/{booking_id}/state/",
    name="Cập nhật trạng thái mới nhất của hồ sơ",
    description="Cập nhật trạng thái mới nhất của hồ sơ",
    responses=swagger_response(
        response_model=ResponseData[StateResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_state(
        state: StateResponse,
        booking_id: str = Path(..., description='Booking ID'),
        current_user=Depends(get_current_user_from_header()),

):
    news_state = await CtrNewState(current_user).ctr_update_state(booking_id=booking_id, data_update=state)
    return ResponseData(**news_state)


@router.get(
    path="/{booking_id}/state/",
    name="Thông tin trạng thái hồ sơ",
    description="Thông tin trạng thái hồ sơ",
    responses=swagger_response(
        response_model=ResponseData[StateResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_state_by_booking_id(
        booking_id: str = Path(..., description='Booking ID'),
        current_user=Depends(get_current_user_from_header()),

):
    state = await CtrNewState(current_user).get_state(booking_id=booking_id)
    return ResponseData[StateResponse](**state)
