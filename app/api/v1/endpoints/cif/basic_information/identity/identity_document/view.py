from typing import List, Union

import pydantic
from fastapi import (
    APIRouter, Body, Depends, File, Form, Header, Path, UploadFile
)
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.controller import (
    CtrIdentityDocument
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.example import (
    save_identity_examples
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.ocr_schema_response import (
    CompareSuccessResponse, OCRBackSideCitizenCardResponse,
    OCRBackSideIdentityCardResponse, OCRFrontSideCitizenCardResponse,
    OCRFrontSideIdentityCardResponse, OCRPassportResponse
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, OcrEkycRequest,
    PassportSaveRequest
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_response import (
    CitizenCardDetailResponse, IdentityCardDetailResponse, LogResponse,
    PassportDetailResponse, ValidateResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse
from app.utils.constant.cif import (
    EKYC_IDENTITY_TYPE, EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD
)
from app.utils.functions import make_description_from_dict

router = APIRouter()


@router.get(
    path="/",
    name="1. GTĐD - A. GTĐD - Chi tiết",
    description="Chi tiết",
    responses=swagger_response(
        response_model=Union[
            ResponseData[IdentityCardDetailResponse],
            ResponseData[CitizenCardDetailResponse],
            ResponseData[PassportDetailResponse]
        ],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrIdentityDocument(current_user)

    identity_document_type_id, detail_info = await ctr_identity_document.detail_identity(cif_id=cif_id)

    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
        return ResponseData[IdentityCardDetailResponse](**detail_info)
    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
        return ResponseData[CitizenCardDetailResponse](**detail_info)
    else:
        return ResponseData[PassportDetailResponse](**detail_info)


@router.get(
    path="/log/",
    name="1. GTĐD - A. GTĐD - Lịch sử",
    description="Lịch sử",
    responses=swagger_response(
        response_model=ResponseData[List[LogResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_logs(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrIdentityDocument(current_user)

    logs_info = await ctr_identity_document.get_identity_log_list(
        cif_id=cif_id
    )

    return ResponseData[List[LogResponse]](
        **logs_info
    )


########################################################################################################################

# router_special dùng để khai báo cho việc sử dụng các api khi cif_id chưa có
router_special = APIRouter()


@router_special.post(
    path="/basic-information/identity/identity-document/",
    name="1. GTĐD - A. GTĐD - Lưu",
    description="Lưu Giấy tờ định danh",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_save(
        request: Request,
        identity_document_request: Union[PassportSaveRequest, IdentityCardSaveRequest, CitizenCardSaveRequest] = Body(
            ...,
            examples=save_identity_examples
        ),
        current_user=Depends(get_current_user_from_header())
):
    # Vì 2 Model CMND, CCCD có cùng dạng ở level 1 nên phải kiểm tra để parse data sang model chuẩn tránh việc nhầm lẫn
    if isinstance(identity_document_request, IdentityCardSaveRequest):
        request_body = await request.json()
        request_body_identity_document_type_id = request_body['identity_document_type']['id']
        if request_body_identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
            try:
                identity_document_request = CitizenCardSaveRequest(**request_body)
            except pydantic.error_wrappers.ValidationError as ex:
                raise RequestValidationError(ex.raw_errors)

    save_info = await CtrIdentityDocument(current_user).save_identity(identity_document_request)
    return ResponseData[SaveSuccessResponse](**save_info)


@router_special.post(
    path="/basic-information/identity/identity-document/ocr/",
    name="1. GTĐD - A. GTĐD - Upload & OCR",
    description="Upload ảnh giấy tờ tùy thân + Lấy thông tin OCR của giấy tờ tùy thân",
    responses=swagger_response(
        response_model=Union[
            ResponseData[OCRFrontSideIdentityCardResponse],
            ResponseData[OCRBackSideIdentityCardResponse],
            ResponseData[OCRFrontSideCitizenCardResponse],
            ResponseData[OCRBackSideCitizenCardResponse],
            ResponseData[OCRPassportResponse],
        ],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_upload_identity_document_image(
        identity_type: int = Form(
            ..., description=f"Loại giấy tờ định danh: {make_description_from_dict(EKYC_IDENTITY_TYPE)}"
        ),
        image_file: UploadFile = File(..., description='File hình ảnh giấy tờ định danh'),
        BOOKING_ID: str = Header(None, description="Mã phiên giao dịch"), # noqa
        current_user=Depends(get_current_user_from_header())
):
    upload_info = await CtrIdentityDocument(current_user).upload_identity_document_and_ocr(
        image_file=image_file,
        identity_type=identity_type,
        booking_id=BOOKING_ID
    )

    if identity_type == EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD:
        return ResponseData[OCRFrontSideIdentityCardResponse](**upload_info)
    elif identity_type == EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD:
        return ResponseData[OCRBackSideIdentityCardResponse](**upload_info)
    elif identity_type == EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD:
        return ResponseData[OCRFrontSideCitizenCardResponse](**upload_info)
    elif identity_type == EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD:
        return ResponseData[OCRBackSideCitizenCardResponse](**upload_info)
    else:
        return ResponseData[OCRPassportResponse](**upload_info)


@router_special.post(
    path="/basic-information/identity/identity-document/compare-face/",
    name="1. GTĐD - A. GTĐD - So Sánh Khuôn Mặt",
    description="So sánh độ chính xác khuôn mặt trong giấy tờ tùy thân và khuôn mặt chụp thực tế",
    responses=swagger_response(
        response_model=ResponseData[CompareSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_compare_face(
        face_image: UploadFile = File(..., description="URL hình ảnh khuôn mặt đối chiếu"),
        identity_image_uuid: str = File(...,
                                        description='ID hình ảnh giấy tờ định danh có được sau khi gọi API '
                                        '`Upload ảnh giấy tờ tùy thân + Lấy thông tin OCR của giấy tờ tùy thân`'),
        BOOKING_ID: str = Header(None, description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    face_compare_info = await CtrIdentityDocument(current_user).compare_face(
        face_image=face_image,
        identity_image_uuid=identity_image_uuid,
        booking_id=BOOKING_ID
    )
    return ResponseData[CompareSuccessResponse](**face_compare_info)


@router_special.post(
    path="/basic-information/identity/identity-document/validate/",
    name="1. GTĐD - A. GTĐD - validate",
    description="validate ocr",
    responses=swagger_response(
        response_model=ResponseData[ValidateResponse],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def validate_ekyc(
        ocr_ekyc_request: OcrEkycRequest,
        BOOKING_ID: str = Header(None, description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    data = await CtrIdentityDocument(current_user).validate_ekyc(
        ocr_ekyc_request=ocr_ekyc_request,
        booking_id=BOOKING_ID
    )
    return ResponseData[ValidateResponse](**data)
