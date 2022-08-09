from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_send_email(
        product_code,
        list_email_to,
        list_email_cc,
        list_email_bcc,
        email_subject,
        email_content_html,
        list_email_attachment_file,
        current_user,
        customers=None,
        is_open_ebank_success=False
):
    current_user = current_user.user_info
    is_success, send_email = await service_gw.send_email(
        product_code=product_code,
        list_email_to=list_email_to,
        list_email_cc=list_email_cc,
        list_email_bcc=list_email_bcc,
        email_subject=email_subject,
        email_content_html=email_content_html,
        list_email_attachment_file=list_email_attachment_file,
        current_user=current_user,
        customers=customers,
        is_open_ebank_success=is_open_ebank_success
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="send_email",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(send_email)
        )

    return ReposReturn(data=send_email)
