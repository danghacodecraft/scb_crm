from typing import List

from fastapi import APIRouter, Depends,Query
from starlette import status

from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.blacklist.controller import CtrBlackList
from app.api.v1.endpoints.blacklist.schema import (
    BlacklistResponse
)

router = APIRouter()


@router.get(
    path='/',
    name="Xem dữ liệu blacklist",
    description="Xem dữ liệu blacklist",
    responses=swagger_response(
        response_model=List[BlacklistResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_blacklist(
        pagination_params: PaginationParams = Depends(),
        id: int = Query(None , description='id'),
        identity_id: str =Query(None , description='Giấy tờ định danh'),
        cif_num:str =Query(None, description='số cif' ),
        casa_account:str=Query(None, description='Số tài khoản ngân hàng tại SCB'),
) -> List[BlacklistResponse]:
    return await CtrBlackList().ctr_view_blacklist(pagination_params,
                                                   id,
                                                   identity_id,
                                                   cif_num,
                                                   casa_account
                                                   )


