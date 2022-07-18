from typing import List

from fastapi import APIRouter, Depends, File, Header, Query, UploadFile
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.file.controller import CtrFile
from app.api.v1.endpoints.file.schema import (
    FileServiceDownloadFileResponse, FileServiceResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="Upload file",
    description="Upload một file",
    responses=swagger_response(
        response_model=ResponseData[FileServiceResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_file_upload(
        BOOKING_ID: str = Header( # noqa
            ..., description="Mã phiên giao dịch"
        ),
        file: UploadFile = File(..., description='File cần upload'),
        save_to_db_flag: bool = File(False, description='Có lưu vào DB không'),
        ekyc_flag: bool = File(False, description='`true` is call ekyc'),
        current_user=Depends(get_current_user_from_header()),  # noqa
):
    file_response = await CtrFile(is_init_oracle_session=False, current_user=current_user).upload_file(
        file,
        ekyc_flag=ekyc_flag,
        save_to_db_flag=save_to_db_flag,
        booking_id=BOOKING_ID
    )
    return ResponseData[FileServiceResponse](**file_response)


@router.post(
    path="/multi-upload/",
    name="Upload multi-file",
    description="Upload nhiều file. "
                "Lưu ý: `Thứ tự trả về có thể không giống thứ tự gửi lên -> Cần tự check thứ tự theo tên file`",
    responses=swagger_response(
        response_model=ResponseData[List[FileServiceResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_file_multi_upload(
        file: List[UploadFile] = File(
            ...,
            description='Muốn upload nhiều file thì gửi nhiều key value với key là `file`, value là `file cần upload`'
        ),
        current_user=Depends(get_current_user_from_header()),  # noqa
):
    res = await CtrFile(is_init_oracle_session=False).upload_multi_file(file)
    return ResponseData[List[FileServiceResponse]](**res)


@router.get(
    path="/{uuid}/download/",
    name="Get link download file",
    description="Lấy link tải của một file",
    responses=swagger_response(
        response_model=ResponseData[FileServiceDownloadFileResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_download_file(
        uuid: str = Query(..., description='Chuỗi định danh của file cần tải'),
        current_user=Depends(get_current_user_from_header()),  # noqa
):
    res = await CtrFile(is_init_oracle_session=False).download_file(uuid)
    return ResponseData[FileServiceDownloadFileResponse](**res)


@router.get(
    path="/download/",
    name="Get link download multi-file",
    description="Lấy link tải của nhiều file",
    responses=swagger_response(
        response_model=ResponseData[List[FileServiceDownloadFileResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_download_multi_file(
        uuid: List[str] = Query(
            ...,
            description='Muốn tải nhiều file thì gửi nhiều query parameter `uuid`'
        ),
        current_user=Depends(get_current_user_from_header()),  # noqa
):
    res = await CtrFile(is_init_oracle_session=False).download_multi_file(uuid)
    return ResponseData[List[FileServiceDownloadFileResponse]](**res)
