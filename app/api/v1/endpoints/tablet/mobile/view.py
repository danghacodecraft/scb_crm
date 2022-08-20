from typing import List

from fastapi import APIRouter, File, Form, Query, Security, UploadFile
from fastapi.security import HTTPAuthorizationCredentials

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import bearer_token
from app.api.v1.endpoints.tablet.mobile.controller import CtrTabletMobile
from app.api.v1.endpoints.tablet.mobile.schema import (
    ListBannerCategoryResponse, ListBannerLanguageCodeQueryParam,
    SyncWithWebByOTPRequest, SyncWithWebByOTPResponse
)
from app.api.v1.endpoints.tablet.web.schema import TabletStatusResponse

router = APIRouter()


@router.post(
    path="/pair/",
    name="Sync with web by OTP",
    description="Đăng nhập để đồng bộ với web của giao dịch viên bằng OTP",
    responses=swagger_response(
        response_model=ResponseData[SyncWithWebByOTPResponse]
    )
)
async def view_sync_with_web_by_otp(
        request: SyncWithWebByOTPRequest
):
    """
    Dùng ở màn hình nhập OTP sau khi mở app. Sau khi nhập OTP là 6 số, click đăng nhập
    Mỗi lần mở app thì nhập lại OTP, app không cần lưu lại config

    :param request: mã OTP và device info (tạm thời chỉ là địa chỉ MAC)
    :return:
        + Nếu status code khác 200 thì app tự xử lý hiện thông báo Mã OTP không chính xác
        + Nếu status code là 200 thì sẽ trả về
            . config mqtt để app consume message
            . token tương ứng với phiên này để mobile dùng gọi các API khác
            . thông tin trên top bar và thông tin giao dịch viên để hiện ở màn hình liên quan
    """
    token_and_mqtt_info = await CtrTabletMobile().sync_with_web_by_otp(request=request)
    return ResponseData[SyncWithWebByOTPResponse](**token_and_mqtt_info)


@router.get(
    path="/banners/",
    name="List banner",
    description="Lấy danh sách banner quảng cáo",
    responses=swagger_response(
        response_model=ResponseData[List[ListBannerCategoryResponse]]
    )
)
async def view_list_banner(
        language_code: ListBannerLanguageCodeQueryParam = Query(..., description='Ngôn ngữ người dùng lựa chọn'),
):
    """
    :param language_code: vi hoặc en tương ứng với ngôn ngữ mà người dùng lựa chọn
    :return: danh sách banner quảng cáo đi theo category thẻ, tiết kiệm, vay, .... Các ảnh này lưu ở fileshare (DMS SCB)
    """
    banner_categories = await CtrTabletMobile().list_banner(language_code=language_code)
    return ResponseData[List[ListBannerCategoryResponse]](**banner_categories)


# @router.post(
#     path="/customer/identity_number/",
#     name="Customer identity number",
#     description="Gửi định danh khách hàng",
#     responses=swagger_response(
#         response_model=ResponseData[CreateUpdateEKYCCustomerResponse],
#         success_status_code=status.HTTP_201_CREATED
#     ),
#     status_code=status.HTTP_201_CREATED
# )
# async def view_update_ekyc_customer(
#         request: UpdateEKYCCustomerRequest,
#         server_auth: str = Header(..., alias="Server-Auth")
# ):
#     # tìm trong DB
#     # nếu có thì send message cho web để hiển thị khach hàng tương ứng, send message mobile để qua màn hình chụp ảnh giấy tờ (gửi kèm cờ để biết ở bước login)
#     # nếu không có thì send message cho web để hiển thị danh sách trống, send message mobile để hiển thị màn hình quảng cáo
#     update_ekyc_customer_info = await CtrEKYC().ctr_update_ekyc_customer(request=request, server_auth=server_auth)
#     return ResponseData[CreateUpdateEKYCCustomerResponse](**update_ekyc_customer_info)
#
#
@router.post(
    path="/customer/photo/",
    name="Photo",
    description="Gửi ảnh chụp giấy tờ định danh, ảnh khuôn mặt, ảnh chữ ký",
    responses=swagger_response(
        response_model=ResponseData[TabletStatusResponse]
    )
)
async def view_take_photo(
        file: UploadFile = File(..., description='File cần upload'),
        is_identify_customer_step: bool = Form(..., description="Giá trị của field này nhận từ data trong message"),
        scheme_and_credentials: HTTPAuthorizationCredentials = Security(bearer_token),
):
    file_info = await CtrTabletMobile().take_photo(
        tablet_token=scheme_and_credentials.credentials,
        is_identify_customer_step=is_identify_customer_step,
        file_upload=file
    )
    return ResponseData[TabletStatusResponse](**file_info)
