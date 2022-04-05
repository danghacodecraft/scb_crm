from fastapi import APIRouter, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.work.contract.controller import (
    CtrContract
)
from app.api.v1.endpoints.user.profile.work.contract.schema import (
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
async def view_contract_info(
        employee_id: str = Query(..., description="employee_id")
):
    contract_info = await CtrContract().ctr_contract_info(employee_id=employee_id)
    return ResponseData[ContractInfoResponse](**contract_info)
