from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.file.schema import FileServiceResponse
from app.api.v1.endpoints.mobile.controller import CtrIdentityMobile
from app.api.v1.endpoints.mobile.schema import IdentityMobileRequest

router = APIRouter()


@router.post(
    path="/cif/identity/",
    name="Thu thập DTDD",
    description="Thu thập DTDD",
    responses=swagger_response(
        response_model=ResponseData[FileServiceResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def save_identity_mobile(
        request: IdentityMobileRequest = Depends(IdentityMobileRequest.upload_identity_mobile),
        current_user=Depends(get_current_user_from_header())
):
    response_data = await CtrIdentityMobile(current_user).save_identity_mobile(
        request=request
    )
    return ResponseData(**response_data)
