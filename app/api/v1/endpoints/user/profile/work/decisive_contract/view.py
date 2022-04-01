from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.work.decisive_contract.controller import (
    CtrDecisiveContract
)
from app.api.v1.endpoints.user.profile.work.decisive_contract.schema import (
    ContractInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[HỒ SƠ CÔNG TÁC] - B. QUYẾT ĐỊNH HỢP ĐỒNG",
    description="[HỒ SƠ CÔNG TÁC] - B. QUYẾT ĐỊNH HỢP ĐỒNG",
    responses=swagger_response(
        response_model=ResponseData[ContractInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_decisive_contract(
        current_user=Depends(get_current_user_from_header()) # noqa
):
    user_info = await CtrDecisiveContract().ctr_decisive_contract()
    return ResponseData[ContractInfoResponse](**user_info)
