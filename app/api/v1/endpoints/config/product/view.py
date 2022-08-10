from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.product.controller import CtrConfigProduct
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/fee-category/",
    name="Fee Category",
    description="Lấy dữ liệu loại phí tài khoản",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_product_fee_category(
        current_user=Depends(get_current_user_from_header())
):
    product_fee_category = await CtrConfigProduct(current_user).ctr_product_fee_category_info()
    return ResponseData[List[DropdownResponse]](**product_fee_category)
