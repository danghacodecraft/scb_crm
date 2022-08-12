from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.schemas.utils import DropdownRequest
from app.settings.config import (
    DATE_INPUT_OUTPUT_FORMAT, DATETIME_INPUT_OUTPUT_FORMAT
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.cif import DROPDOWN_NONE_DICT
from app.utils.error_messages import ERROR_FIELD_REQUIRED
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown
)


class CtrPaymentSender(BaseController):
    async def get_payment_sender(
            self,
            sender_cif_number: Optional[str],
            sender_full_name_vn: Optional[str],
            sender_address_full: Optional[str],
            sender_identity_number: Optional[str],
            sender_issued_date: Optional[str],
            sender_mobile_number: Optional[str],
            sender_place_of_issue: Optional[DropdownRequest],
            sender_note: Optional[str]
    ):
        if sender_cif_number:
            gw_customer_info = await CtrGWCustomer(self.current_user).ctr_gw_get_customer_info_detail(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            gw_customer_info_identity_info = gw_customer_info['id_info']
            sender_response = dict(
                cif_number=sender_cif_number,
                fullname_vn=gw_customer_info['full_name'],
                address_full=gw_customer_info['t_address_info']['contact_address_full'],
                identity_info=dict(
                    number=gw_customer_info_identity_info['id_num'],
                    issued_date=date_string_to_other_date_string_format(
                        gw_customer_info_identity_info['id_issued_date'],
                        from_format=DATETIME_INPUT_OUTPUT_FORMAT,
                        to_format=DATE_INPUT_OUTPUT_FORMAT
                    ),
                    place_of_issue=await self.dropdown_mapping_crm_model_or_dropdown_name(
                        model=PlaceOfIssue,
                        code=gw_customer_info_identity_info['id_issued_location'],
                        name=gw_customer_info_identity_info['id_issued_location']
                    )
                ),
                mobile_phone=gw_customer_info['mobile_phone'],
                telephone=gw_customer_info['telephone'],
                otherphone=gw_customer_info['otherphone'],
                note=sender_note

            )
        else:
            identity_place_of_issue = DROPDOWN_NONE_DICT
            if sender_place_of_issue:
                identity_place_of_issue = await self.get_model_object_by_id(
                    model_id=sender_place_of_issue.id,
                    model=PlaceOfIssue,
                    loc='sender_place_of_issue -> id'
                )
            sender_full_name_vn = sender_full_name_vn
            sender_address_full = sender_address_full
            sender_identity_number = sender_identity_number
            sender_issued_date = sender_issued_date
            sender_mobile_number = sender_mobile_number
            sender_response = dict(
                cif_number=sender_cif_number,
                fullname_vn=sender_full_name_vn,
                address_full=sender_address_full,
                identity_info=dict(
                    number=sender_identity_number,
                    issued_date=sender_issued_date,
                    place_of_issue=dropdown(identity_place_of_issue)
                ),
                mobile_phone=sender_mobile_number,
                telephone=None,
                otherphone=None,
                note=sender_note
            )
            errors = []
            if not sender_full_name_vn:
                errors.append(f'sender_full_name_vn: {sender_full_name_vn}')
            if not sender_identity_number:
                errors.append(f'sender_identity_number: {sender_identity_number}')
            if not sender_issued_date:
                errors.append(f'sender_issued_date: {sender_issued_date}')
            if not sender_address_full:
                errors.append(f'sender_address_full: {sender_address_full}')
            if not sender_mobile_number:
                errors.append(f'sender_mobile_number: {sender_mobile_number}')

            if errors:
                return self.response_exception(msg=ERROR_FIELD_REQUIRED, loc=', '.join(errors))
        return sender_response
