from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import PagingResponse, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.dashboard.dashboard_360.document_list.controller import (
    CtrDocumentList
)
from app.api.v1.endpoints.dashboard.dashboard_360.document_list.schema import (
    DocumentListResponse
)

router = APIRouter()


@router.get(
    path="/{cif_number}/",
    name="Document List",
    description="Danh sách tài liệu",
    responses=swagger_response(
        response_model=ResponseData[DocumentListResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_document_list(
        cif_number: str = Path(..., description='Số CIF'),
        current_user=Depends(get_current_user_from_header()),
        pagination_params: PaginationParams = Depends(),
):
    transaction_list_response = await CtrDocumentList(
        current_user=current_user,
        pagination_params=pagination_params,
    ).ctr_document_list(cif_number=cif_number)

    return PagingResponse[DocumentListResponse](**transaction_list_response)
