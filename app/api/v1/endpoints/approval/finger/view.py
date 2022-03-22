from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.finger.controller import CtrFingers
from app.api.v1.endpoints.approval.finger.schema import FingersResponse

router = APIRouter()


@router.get(
    path="/finger/",
    name="Vân tay phê duyệt",
    description="Vân tay phê duyệt",
    responses=swagger_response(
        response_model=ResponseData[FingersResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_fingers(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    fingers_info = await CtrFingers(current_user).ctr_get_fingerprint(cif_id)
    return ResponseData[FingersResponse](**fingers_info)
