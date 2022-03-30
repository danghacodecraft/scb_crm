from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.schema import UserInfoResponse

router = APIRouter()


@router.get(
    path="/",
    name="[HỒ SƠ CÔNG TÁC] - B. QUYẾT ĐỊNH HỢP ĐỒNG",
    description="[HỒ SƠ CÔNG TÁC] - B. QUYẾT ĐỊNH HỢP ĐỒNG",
    responses=swagger_response(
        response_model=ResponseData[UserInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_current_user(
        current_user=Depends(get_current_user_from_header())
):
    # user_info = await CtrUser(is_init_oracle_session=False, current_user=current_user).ctr_get_current_user_info()
    return ResponseData[UserInfoResponse]({})
