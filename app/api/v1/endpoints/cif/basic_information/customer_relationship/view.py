from typing import List

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.customer_relationship.controller import (
    CtrCustomerRelationship
)
from app.api.v1.endpoints.cif.basic_information.customer_relationship.schema import (
    DetailCustomerRelationshipResponse, SaveCustomerRelationshipRequest
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.get(
    path="/",
    name="5. Mối quan hệ khách hàng",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[DetailCustomerRelationshipResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_customer_relationship = CtrCustomerRelationship(current_user)

    detail_customer_relationship_info = await ctr_customer_relationship.detail(
        cif_id=cif_id
    )

    return ResponseData[DetailCustomerRelationshipResponse](
        **detail_customer_relationship_info
    )


@router.post(
    path="/",
    name="5. Mối quan hệ khách hàng",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save(
        cif_id: str = Path(..., description='Id CIF ảo'),
        customer_relationship_save_request: List[SaveCustomerRelationshipRequest] = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    ctr_customer_relationship = CtrCustomerRelationship(current_user)

    save_customer_relationship_info = await ctr_customer_relationship.save(
        cif_id=cif_id,
        customer_relationship_save_request=customer_relationship_save_request
    )

    return ResponseData[SaveSuccessResponse](
        **save_customer_relationship_info
    )
