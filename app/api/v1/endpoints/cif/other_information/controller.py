from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.other_information.repository import (
    repos_other_info, repos_update_other_info
)
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationUpdateRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.utils.constant.cif import (
    STAFF_TYPE_BUSINESS_CODE, STAFF_TYPE_REFER_INDIRECT_CODE
)
from app.utils.error_messages import ERROR_MOBILE_NUMBER, ERROR_NO_DATA


class CtrOtherInfo(BaseController):
    async def ctr_other_info(self, cif_id: str):
        customer_employee = self.call_repos(await repos_other_info(cif_id, self.oracle_session))
        sale_staff = None
        indirect_sale_staff = None

        for _, staff_type, employee in customer_employee:
            if staff_type and employee:
                employee = await CtrGWEmployee(self.current_user).ctr_gw_get_employee_info_from_code(
                    employee_code=employee.employee_id
                )
                staff_info = dict(
                    id=employee['data']['staff_code'],
                    fullname_vn=employee['data']['fullname_vn']
                )
                if staff_type.code == STAFF_TYPE_BUSINESS_CODE:
                    sale_staff = staff_info
                if staff_type.code == STAFF_TYPE_REFER_INDIRECT_CODE:
                    indirect_sale_staff = staff_info

        legal_agreement_flag = customer_employee[0][0].legal_agreement_flag
        advertising_marketing_flag = customer_employee[0][0].advertising_marketing_flag

        if legal_agreement_flag is None or advertising_marketing_flag is None:
            return self.response_exception(msg=ERROR_NO_DATA)

        return self.response(data=dict(
            # lấy ra data ở vị trí 0 trong query sau đó lấy ra customer ở vị trí 0
            legal_agreement_flag=legal_agreement_flag,
            advertising_marketing_flag=advertising_marketing_flag,
            sale_staff=sale_staff,
            indirect_sale_staff=indirect_sale_staff,
        ))

    async def ctr_update_other_info(self, cif_id: str, update_other_info_req: OtherInformationUpdateRequest):
        # check cif đang tạo
        cif_info = self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        if not (cif_info.mobile_number or cif_info.telephone_number):
            return self.response_exception(
                msg=ERROR_MOBILE_NUMBER, loc=f" cif_info -> mobile_number : {cif_info.mobile_number}"
            )
        update_other_info = self.call_repos(
            await repos_update_other_info(
                cif_id=cif_id,
                update_other_info_req=update_other_info_req,
                extra_phone_number=update_other_info_req.extra_phone_number,
                customer_relationship=update_other_info_req.customer_relationship.id,
                current_user=self.current_user.user_info,
                session=self.oracle_session
            )
        )
        return self.response(update_other_info)
