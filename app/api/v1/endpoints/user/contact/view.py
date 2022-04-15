from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.contact.controller import CtrContact
from app.api.v1.endpoints.user.contact.schema import ContactResponse
from app.api.v1.endpoints.user.contact.success_example import SUCCESS_EXAMPLE

router = APIRouter()


@router.get(
    path="/contact",
    name="Thông tin nhân viên",
    description="Thông tin nhân viên",
    responses=swagger_response(
        response_model=ResponseData[ContactResponse],
        success_status_code=status.HTTP_200_OK,
        success_examples=SUCCESS_EXAMPLE

    )
)
async def view_contact_info(current_user=Depends(get_current_user_from_header())):
    contact = await CtrContact(current_user).ctr_contact()

    return ResponseData[ContactResponse](**contact)
