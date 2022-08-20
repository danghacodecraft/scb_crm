from fastapi import APIRouter

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.tablet.mobile.controller import CtrTabletMobile
from app.api.v1.endpoints.tablet.mobile.schema import (
    SyncWithWebByOTPRequest, SyncWithWebByOTPResponse
)

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
    # nếu đã kết nối nhưng out app, thì vào chỉ cần nhập lại OTP cũ
    # đăng nhập thì công thì server gửi đến topic web để web hiện phiên giao dịch
    # trả về mqtt cho mobile kết nối, trả về token tương ứng với phiên này để mobile dùng gọi các API
    token_and_mqtt_info = await CtrTabletMobile().sync_with_web_by_otp(request=request)
    return ResponseData[SyncWithWebByOTPResponse](**token_and_mqtt_info)


# @router.get(
#     path="/banners/",
#     name="List banner",
#     description="Lấy danh sách banner quảng cáo",
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
#     # cho truyền lên ngôn ngữ
#     # trả về danh sách banner quảng cáo
#     update_ekyc_customer_info = await CtrEKYC().ctr_update_ekyc_customer(request=request, server_auth=server_auth)
#     return ResponseData[CreateUpdateEKYCCustomerResponse](**update_ekyc_customer_info)
#
#
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
# @router.post(
#     path="/customer/photo/",
#     name="Photo",
#     description="Gửi ảnh chụp giấy tờ định danh, ảnh khuôn mặt, ảnh chữ ký",
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
#     # gửi kèm cờ có phải login hay không trả về ở mqtt
#     update_ekyc_customer_info = await CtrEKYC().ctr_update_ekyc_customer(request=request, server_auth=server_auth)
#     return ResponseData[CreateUpdateEKYCCustomerResponse](**update_ekyc_customer_info)