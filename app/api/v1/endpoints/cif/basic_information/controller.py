from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.repository import (
    repos_get_customer_personal_relationships
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_initializing_customer, repos_validate_cif_number
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.utils.error_messages import (
    ERROR_RELATION_CUSTOMER_SELF_RELATED, ERROR_RELATIONSHIP_EXIST
)


class CtrBasicInformation(BaseController):
    async def customer_detail(
            self,
            cif_id: str,
            cif_number_need_to_find: str,
            relationship_type: int
    ):
        # validate cif_number
        self.call_repos(await repos_validate_cif_number(cif_number=cif_number_need_to_find))

        # RULE: chỉ cif_id đang khởi tạo mới được sử dụng API này
        # check current customer is initializing
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        # kiểm tra xem có đang tự quan hệ với bản thân không?
        if current_customer.cif_number == cif_number_need_to_find:
            return self.response_exception(
                msg=ERROR_RELATION_CUSTOMER_SELF_RELATED,
                loc="cif_number",
            )

        customer_detail_data = CtrGWCustomer().ctr_gw_check_exist_customer_detail_info(
            cif_number=cif_number_need_to_find
        )

        relationships = await repos_get_customer_personal_relationships(
            session=self.oracle_session,
            relationship_type=relationship_type,
            cif_id=cif_id,
        )
        # kiểm tra Customer có từng quan hệ với cif_number này chưa
        if relationships:
            relationship_cif_numbers = [relationship.customer_personal_relationship_cif_number for relationship in
                                        relationships]
            if cif_number_need_to_find in relationship_cif_numbers:
                return self.response_exception(
                    msg=ERROR_RELATIONSHIP_EXIST,
                    loc="cif_number",
                )

        return self.response(data=customer_detail_data)
