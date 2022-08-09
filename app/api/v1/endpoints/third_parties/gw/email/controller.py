from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.email.repository import (
    repos_gw_send_email
)


class CtrGWEmail(BaseController):
    async def ctr_gw_send_email(self,
                                product_code,
                                list_email_to,
                                list_email_cc,
                                list_email_bcc,
                                email_subject,
                                email_content_html,
                                list_email_attachment_file,
                                customers=None,
                                is_open_ebank_success=False
                                ):
        current_user = self.current_user
        send_email = self.call_repos(await repos_gw_send_email(
            product_code,
            list_email_to,
            list_email_cc,
            list_email_bcc,
            email_subject,
            email_content_html,
            list_email_attachment_file,
            current_user=current_user,
            customers=customers,
            is_open_ebank_success=is_open_ebank_success))

        return self.response(data=send_email)
