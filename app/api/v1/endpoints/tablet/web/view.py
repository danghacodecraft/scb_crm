from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
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
# @router.delete(
#     path="/otp/",
#     name="Unpair tablet",
#     description="Hủy ghép nối với tablet khi logout hoặc quá 15 phút",
#     responses=swagger_response(
#         response_model=ResponseData[CreateUpdateEKYCCustomerResponse],
#         success_status_code=status.HTTP_200_OK
#     )
# )
# async def view_create_ekyc_customer(
#         request: CreateEKYCCustomerRequest,
#         server_auth: str = Header(..., alias="Server-Auth")
# ):
#     # kiểm tra có đang kết nối với tablet nào không, nêú có thì hiện lại OTP cũ
#     # trả về MQTT để web kết nối tương ứng OTP đó, khi nào có message connect thành công thì hiện phiên giao dịch với khách hàng ở top bar
#     create_ekyc_customer_info = await CtrEKYC().ctr_create_ekyc_customer(request=request, server_auth=server_auth)
#     return ResponseData[CreateUpdateEKYCCustomerResponse](**create_ekyc_customer_info)
