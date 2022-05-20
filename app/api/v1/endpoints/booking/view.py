from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.booking.schema import (
    CreateBookingRequest, CreateBookingResponse
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
