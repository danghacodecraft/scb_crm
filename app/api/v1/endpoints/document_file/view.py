from fastapi import APIRouter, Depends, File, Path, UploadFile
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.document_file.controller import CtrDocumentFile
from app.api.v1.endpoints.document_file.schema import DocumentFileResponse

router = APIRouter()


@router.post(
    path="/{booking_id}/document_file/",
    name="Tạo tập tin tài liệu",
    description="Tạo tập tin tài liệu",
    responses=swagger_response(
        response_model=ResponseData[DocumentFileResponse],
        success_status_code=status.HTTP_201_CREATED
    ),
    status_code=status.HTTP_201_CREATED
)
async def view_document_file(
        file: UploadFile = File(..., description='File cần upload'),
        booking_id: str = Path(..., description='Booking ID'),
        ekyc_flag: bool = File(False, description='`true` is call ekyc'),
        current_user=Depends(get_current_user_from_header()),
):
    document_file = await CtrDocumentFile(current_user).ctr_document_file(
        file,
        ekyc_flag=ekyc_flag,
        booking_id=booking_id)
    return ResponseData(**document_file)
