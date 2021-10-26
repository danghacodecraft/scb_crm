from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.payment_account.co_owner.controller import (
    CtrCoOwner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest, AccountHolderSuccessResponse, DetailCoOwnerResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="B. Thông tin đồng sở hữu",
    description="Tạo dữ liệu tab `THÔNG TIN ĐỒNG SỞ HỮU` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_personal(
        co_owner: AccountHolderRequest,
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    co_owner_data = await CtrCoOwner(current_user).ctr_save_co_owner(cif_id, co_owner)
    return ResponseData[SaveSuccessResponse](**co_owner_data)


@router.get(
    path="/",
    name="B. Thông tin đồng sở hữu",
    description="Lấy dữ liệu tab `THÔNG TIN ĐỒNG SỞ HỮU` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[AccountHolderSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_co_owner(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    co_owner_data = await CtrCoOwner(current_user).ctr_co_owner(cif_id)
    return ResponseData[AccountHolderSuccessResponse](**co_owner_data)


@router.get(
    path="/detail-co-owner/",
    name="Lấy thông tin đồng sở hữu qua số CIF",
    description="Lấy dữ liệu `THÔNG TIN ĐỒNG SỞ HỮU` thông qua số CIF",
    responses=swagger_response(
        response_model=ResponseData[DetailCoOwnerResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_detail_co_owner(
        cif_id: str = Path(..., description='Id CIF ảo'),
        cif_number: str = Query(..., description='Số CIF cần lấy thông tin'),
        current_user=Depends(get_current_user_from_header())
):
    detail_co_owner = await CtrCoOwner(current_user).detail_co_owner(
        cif_id=cif_id,
        cif_number_need_to_find=cif_number
    )

    return ResponseData[DetailCoOwnerResponse](**detail_co_owner)
