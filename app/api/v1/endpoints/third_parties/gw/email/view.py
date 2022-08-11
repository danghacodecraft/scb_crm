from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import EmailStr
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.email.controller import CtrGWEmail
from app.settings.service import SERVICE

router = APIRouter()


@router.post(
    path="/sendEmail",
    name="[GW] Send Email",
    description="[GW] Gửi Email",
    responses=swagger_response(
        response_model=None,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_send_email(
        current_user=Depends(get_current_user_from_header()),
        data_input__product_code: str = Form(..., alias="sendEmail_in.data_input.product_code",
                                             description="Mã chương trình -> Để chọn đúng SMTP config"),
        data_input__email_to: Optional[List[EmailStr]] = Form(SERVICE.get('gw', {}).get('email', {}),
                                                              alias="sendEmail_in.data_input.email_to",
                                                              description="Địa chỉ email cần gửi, cần gửi tới nhiều "
                                                                          "người thì gửi lên nhiều key này,"
                                                                          " không có thì không gửi lên"),
        data_input__email_cc: Optional[List[EmailStr]] = Form(None, alias="sendEmail_in.data_input.email_cc",
                                                              description="Địa chỉ email cần cc, cần gửi tới nhiều"
                                                                          " người thì gửi lên nhiều key này,"
                                                                          " không có thì không gửi lên"),
        data_input__email_bcc: Optional[List[EmailStr]] = Form(None, alias="sendEmail_in.data_input.email_bcc",
                                                               description="Địa chỉ email cần bcc, cần gửi tới"
                                                                           " nhiều người thì gửi lên nhiều key này,"
                                                                           " không có thì không gửi lên"),
        data_input__email_subject: str = Form(..., alias="sendEmail_in.data_input.email_subject",
                                              description="Tiêu đề"),
        data_input__email_content_html: str = Form(None, alias="sendEmail_in.data_input.email_content_html",
                                                   description="Nội dung HTML"),
        data_input__email_attachment_file: Optional[List[UploadFile]] = File(None,
                                                                             alias="sendEmail_in.data_input"
                                                                                   ".email_attachment_file",
                                                                             description="Tệp đính kèm, cần gửi nhiều"
                                                                                         " file thì gửi lên nhiều"
                                                                                         " key này,"
                                                                                         " không có thì không gửi lên"),
        data_input__customers: Optional[List[str]] = Form(None, alias="data_input__customers",
                                                          description="danh sách họ và tên khách hàng gửi mail,"
                                                                      " nếu sử dụng `data_input__customers` "
                                                                      "thì hệ thống sẽ sử dụng email template"
                                                                      " mẫu không sử dụng"
                                                                      " `data_input__email_content_html`"),
        data_input__is_open_ebank_success: bool = Form(False, alias="data_input__is_open_ebank_success",
                                                       description="""
- True Email trong trường hợp phê duyệt trạng thái Không hợp lệ sang Hợp lệ.

- False: Email trong trường hợp phê duyệt trạng thái Chờ hậu kiểm / cần xác minh sang Không hợp lệ.
                                                                  """)
):
    ctr_send_email = await CtrGWEmail(
        current_user).ctr_gw_send_email(
        product_code=data_input__product_code,
        list_email_to=data_input__email_to,
        list_email_cc=data_input__email_cc,
        list_email_bcc=data_input__email_bcc,
        email_subject=data_input__email_subject,
        email_content_html=data_input__email_content_html,
        list_email_attachment_file=data_input__email_attachment_file,
        customers=data_input__customers,
        is_open_ebank_success=data_input__is_open_ebank_success
    )

    ctr_send_email['data'] = None

    return ResponseData(**ctr_send_email)
