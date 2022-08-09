from typing import List

from app.api.v1.endpoints.casa.schema import (
    SenderInfoRequest, StatementInfoRequest
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.others.statement.repository import repos_get_denominations
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.cif import DROPDOWN_NONE_DICT
from app.utils.constant.gw import GW_DATE_FORMAT, GW_DATETIME_FORMAT
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_DENOMINATIONS_NOT_EXIST,
    ERROR_FIELD_REQUIRED
)
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown
)


class CtrCasa(CtrGWCustomer, CtrGWEmployee):
    async def validate_statement(self, statement: List[StatementInfoRequest]):
        """
        Validate thông tin bảng kê
        """
        denominations__amounts = {}
        statement_info = self.call_repos(await repos_get_denominations(currency_id="VND", session=self.oracle_session))

        for item in statement_info:
            denominations__amounts.update({
                str(int(item.denominations)): 0
            })

        denominations_errors = []
        for index, row in enumerate(statement):
            denominations = row.denominations
            if denominations not in denominations__amounts:
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

    async def get_sender_info(self, sender: dict):
        """
        Thông tin khách hàng giao dịch
        sender: {
            "cif_number": null,
            "full_name_vn": "string",
            "identity_number": "string",
            "issued_date": "2019-08-24",
            "place_of_issue": {
                "id": "12"
            },
            "address_full": "string",
            "mobile_number": "string"
        }
        """
        sender_response = dict(
            cif_number=None
        )
        sender_cif_number = sender['cif_number']
        if sender_cif_number:
            gw_customer_info = await self.ctr_gw_get_customer_info_detail(
                cif_number=sender_cif_number,
                return_raw_data_flag=True
            )
            gw_customer_info_identity_info = gw_customer_info['id_info']
            sender_response.update(
                cif_number=sender_cif_number,
                full_name_vn=gw_customer_info['full_name'],
                address_full=gw_customer_info['t_address_info']['contact_address_full'],
                identity_info=dict(
                    number=gw_customer_info_identity_info['id_num'],
                    issued_date=date_string_to_other_date_string_format(
                        gw_customer_info_identity_info['id_issued_date'],
                        from_format=GW_DATETIME_FORMAT,
                        to_format=GW_DATE_FORMAT
                    ),
                    place_of_issue=dict(
                        id=gw_customer_info_identity_info['id_issued_location'],
                        code=gw_customer_info_identity_info['id_issued_location'],
                        name=gw_customer_info_identity_info['id_issued_location']
                    )
                ),
                mobile_phone=gw_customer_info['mobile_phone'],
                telephone=gw_customer_info['telephone'],
                otherphone=gw_customer_info['otherphone']
            )
        else:
            sender_place_of_issue = sender['place_of_issue']
            identity_place_of_issue = DROPDOWN_NONE_DICT
            if sender_place_of_issue:
                identity_place_of_issue = await self.get_model_object_by_id(
                    model_id=sender_place_of_issue['id'],
                    model=PlaceOfIssue,
                    loc='place_of_issue -> id'
                )
            sender_response.update(
                full_name_vn=sender['full_name_vn'],
                address_full=sender['address_full'],
                identity_info=dict(
                    number=sender['identity_number'],
                    issued_date=sender['issued_date'],
                    place_of_issue=dropdown(identity_place_of_issue)
                ),
                mobile_phone=sender['mobile_number'],
            )
        # gw_direct_staff = await self.ctr_gw_get_employee_info_from_code(
        #     employee_code=sender['direct_staff_code'],
        #     return_raw_data_flag=True
        # )
        # direct_staff = dict(
        #     code=gw_direct_staff['staff_code'],
        #     name=gw_direct_staff['staff_name']
        # )
        # gw_indirect_staff = await self.ctr_gw_get_employee_info_from_code(
        #     employee_code=sender['indirect_staff_code'],
        #     return_raw_data_flag=True
        # )
        # indirect_staff = dict(
        #     code=gw_indirect_staff['staff_code'],
        #     name=gw_indirect_staff['staff_name']
        # )

        return sender_response
