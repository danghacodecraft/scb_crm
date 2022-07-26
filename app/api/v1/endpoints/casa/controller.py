from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.schema import (
    SenderInfoRequest, StatementInfoRequest
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.casa import DENOMINATIONS__AMOUNTS
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_DENOMINATIONS_NOT_EXIST,
    ERROR_FIELD_REQUIRED
)


class CtrCasa(BaseController):
    async def validate_statement(self, statement: List[StatementInfoRequest]):
        """
        Validate thông tin bảng kê
        """
        denominations__amounts = DENOMINATIONS__AMOUNTS
        denominations_errors = []
        for index, row in enumerate(statement):
            denominations = row.denominations
            if denominations not in DENOMINATIONS__AMOUNTS:
                denominations_errors.append(dict(
                    index=index,
                    value=denominations
                ))

            denominations__amounts[denominations] = row.amount

        if denominations_errors:
            return self.response_exception(
                msg=ERROR_DENOMINATIONS_NOT_EXIST,
                loc=str(denominations_errors)
            )
        return denominations__amounts

    async def validate_sender(self, sender: SenderInfoRequest):
        """
        Validate thông tin người giao dịch
        """
        sender_cif_number = sender.cif_number
        # TH1: có nhập cif -> Kiểm tra số CIF có tồn tại trong CRM không
        if sender_cif_number:
            # self.call_repos(await repos_get_customer_by_cif_number(
            #     cif_number=cif_number,
            #     session=self.oracle_session
            # ))
            customer_detail = await CtrGWCustomer(self.current_user).ctr_gw_get_customer_info_detail(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            if not customer_detail['full_name']:
                return self.response_exception(
                    msg=ERROR_CIF_NUMBER_NOT_EXIST,
                    loc=f"sender_cif_number {sender_cif_number}"
                )
        # TH2: Không nhập CIF
        else:
            sender_full_name_vn = sender.full_name_vn
            sender_identity_number = sender.identity_number
            sender_issued_date = sender.issued_date
            sender_address_full = sender.address_full
            sender_mobile_number = sender.mobile_number

            sender_place_of_issue_id = sender.place_of_issue.id
            await self.get_model_object_by_id(
                model_id=sender_place_of_issue_id,
                model=PlaceOfIssue,
                loc=f'sender_place_of_issue_id: {sender_place_of_issue_id}'
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

        return None
