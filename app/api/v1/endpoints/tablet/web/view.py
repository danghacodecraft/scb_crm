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
from app.api.v1.endpoints.tablet.web.schema import (
    TabletOTPAndMqttInfoResponse, TabletSwitchScreenRequest,
    TabletSwitchScreenResponse
)

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


@router.put(
    path="/screen/",
    name="Switch to others screen in tablet",
    description="""Chuyển tablet sang màn hình khác
- Khi bắt đầu giao dịch với khách hàng, giao dịch viên chọn giao dịch tương ứng mong muốn khách hàng:
action=`PROCESS_TRANSACTION` và extra_data=`{"transaction_name": "chuyển tiền"}`.
Tablet chuyển đến screen giao dịch đang xử lý.

- Trong quá trình giao dịch, giao dịch viên muốn chụp ảnh giấy tờ:
action=`TAKE_DOCUMENT_PHOTO` và extra_data=`{}`.
Tablet chuyển đến screen chụp ảnh giấy tờ.

- Trong quá trình giao dịch, giao dịch viên muốn chụp ảnh khuôn mặt:
action=`TAKE_FACE_PHOTO` và extra_data=`{}`.
Tablet chuyển đến screen chụp ảnh khuôn mặt.

- Trong quá trình giao dịch, giao dịch viên muốn khách hàng ký vào các biểu mẫu:
action=`SIGN` và extra_data=`{"documents": [{"name": "BM nộp tiền", "file_url": "http://example.com/1.pdf"}, {"name": "BM 18B", "file_url": "http://example.com/2.pdf"}]}`.
Tablet chuyển đến screen ký tên các biểu mẫu.

- Khi phiên giao dịch thành công:
action=`TRANSACT_SUCCESS` và extra_data=`{}`.
Tablet chuyển đến screen giao dịch thành công.

- Khi khách hàng hiện tại muốn thực hiện giao dịch mới, giao dịch viên click giao dịch mới trong dropdown tablet trên top bar:
action=`NEW_TRANSACTION` và extra_data=`{}`.
Tablet chuyển sang màn hình chờ trước giao dịch mới

- Khi xong phiên của khách hàng, giao dịch viên click kết thúc phiên giao dịch trong dropdown tablet trên top bar:
action=`ENTER_IDENTITY_NUMBER` và extra_data=`{}`.
Tablet chuyển sang màn hình nhập số giấy tờ định danh khách hàng mới.""",
    responses=swagger_response(
        response_model=ResponseData[TabletSwitchScreenResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_switch_tablet_screen(
        request: TabletSwitchScreenRequest,
        current_user=Depends(get_current_user_from_header()),
):
    """
    Nếu đã kết nối với tablet thì sẽ gửi message tương ứng với action.
    Nếu chưa kết nối với tablet sẽ trả lỗi

    :param request: action và extra_data như description bên trên
    :param current_user: bearer token của giao dịch viên
    :return: status=True khi gửi message thành công
    """
    status_info = await CtrTabletWeb(
        current_user=current_user
    ).ctr_switch_tablet_screen(request=request)
    return ResponseData[TabletSwitchScreenResponse](**status_info)


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
