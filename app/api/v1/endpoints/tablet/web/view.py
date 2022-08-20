from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from starlette.responses import Response

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import (
    bearer_token, get_current_user_from_header
)
from app.api.v1.endpoints.tablet.web.controller import CtrTabletWeb
from app.api.v1.endpoints.tablet.web.schema import TabletOTPAndMqttInfoResponse

router = APIRouter()


@router.get(
    path="/otp/",
    name="OTP for mobile",
    description="Lấy mã OTP để đăng nhập bên tablet",
    responses=swagger_response(
        response_model=ResponseData[TabletOTPAndMqttInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_otp(
        current_user=Depends(get_current_user_from_header()),
):
    """
    Click đồng bộ tablet hiện màn hình mã OTP

    :param current_user: truyền bearer token đã trả về khi đăng nhập
    :return: mã OTP, thời gian hết hạn và web stomp config để FE Web consume message
    """
    otp_and_mqtt_info = await CtrTabletWeb(
        current_user=current_user
    ).ctr_get_otp_and_mqtt_info()
    return ResponseData[TabletOTPAndMqttInfoResponse](**otp_and_mqtt_info)


# @router.put(
#     path="/screen/",
#     name="Switch to other screen in tablet",
#     description="Chuyển tablet sang màn hình khác",
#     responses=swagger_response(
#         response_model=ResponseData[CreateUpdateEKYCCustomerResponse],
#         success_status_code=status.HTTP_200_OK
#     )
# )
# async def view_create_ekyc_customer(
#         request: CreateEKYCCustomerRequest,
#         server_auth: str = Header(..., alias="Server-Auth")
# ):
#     # bắt đầu giao dịch nào thì chuyển sang màn hình giao dịch
#     # chuyển sang màn hình chụp ảnh giấy tờ khi mở cif
#     # chuyển sang màn hình chụp ảnh khuôn mặt khi mở cif
#     create_ekyc_customer_info = await CtrEKYC().ctr_create_ekyc_customer(request=request, server_auth=server_auth)
#     return ResponseData[CreateUpdateEKYCCustomerResponse](**create_ekyc_customer_info)
#
#
@router.delete(
    path="/otp/",
    name="Unpair tablet if exists",
    description="Hủy ghép nối với tablet (nếu có) khi logout hoặc quá 15 phút",
    responses=swagger_response(
        response_model=None,
        success_status_code=status.HTTP_204_NO_CONTENT
    ),
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def view_unpair_tablet(
        scheme_and_credentials: HTTPAuthorizationCredentials = Security(bearer_token),
):
    """
    Dùng khi click logout hoặc quá 15 phút không hoạt động
    Vì giao dịch viên có thể chưa kết nối với tablet nên chỉ hủy ghép nối nếu có kết nối

    Khi có thiết bị và unpair thành công thì gửi message cho mobile để hiện màn hình nhập OTP

    :param scheme_and_credentials: Vì khi giao dịch viên không hoạt động quá 15 phút -> token bên IDM đã hết hạn
                                   => Chỉ lấy username trong token, không gọi qua IDM check để không bị 403
    :return: HTTP_204_NO_CONTENT
    """

    # TODO: check if expired instead of only get username from token
    await CtrTabletWeb().ctr_unpair_tablet(token=scheme_and_credentials.credentials)
    return None
