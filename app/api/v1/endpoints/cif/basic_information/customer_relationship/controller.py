from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.customer_relationship.repository import (
    repos_get_customer_relationships
)
from app.api.v1.endpoints.cif.basic_information.customer_relationship.schema import (
    SaveCustomerRelationshipRequest
)
from app.api.v1.endpoints.cif.basic_information.guardian.repository import (
    repos_save_guardians
)
from app.api.v1.endpoints.cif.repository import (
    repos_check_exist_cif, repos_get_initializing_customer
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_MQHKH, CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP
)
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_DUPLICATED, ERROR_RELATION_CUSTOMER_SELF_RELATED
)
from app.utils.functions import orjson_dumps


class CtrCustomerRelationship(BaseController):
    async def detail(self, cif_id: str):
        detail_customer_relationship_info = self.call_repos(
            await repos_get_customer_relationships(
                cif_id=cif_id,
                session=self.oracle_session,
            ))
        return self.response(data=detail_customer_relationship_info)

    async def save(self,
                   cif_id: str,
                   customer_relationship_save_request: List[SaveCustomerRelationshipRequest]):
        # check and get current customer
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))
        log_data = []
        customer_relationship_cif_numbers, relationship_types = [], set()
        for customer_relationship in customer_relationship_save_request:
            # check số cif có tồn tại trong SOA
            self.call_repos(await repos_check_exist_cif(cif_number=customer_relationship.cif_number))
            customer_relationship_cif_numbers.append(customer_relationship.cif_number),
            relationship_types.add(customer_relationship.customer_relationship.id)

            relationship_log = {
                "cif_number": customer_relationship.cif_number,
                "customer_relationship": {
                    "id": customer_relationship.customer_relationship.id
                }
            }
            log_data.append(orjson_dumps(relationship_log))

        # check duplicate cif_number in request body
        if len(customer_relationship_cif_numbers) != len(set(customer_relationship_cif_numbers)):
            return self.response_exception(
                msg=ERROR_CIF_NUMBER_DUPLICATED,
                loc="cif_number",
            )
        # check if it relates to itself
        if current_customer.cif_number in customer_relationship_cif_numbers:
            return self.response_exception(
                msg=ERROR_RELATION_CUSTOMER_SELF_RELATED,
                loc="cif_number",
            )

        # check relationship types exist
        await self.get_model_objects_by_ids(
            model=CustomerRelationshipType,
            model_ids=list(relationship_types),
            loc="customer_relationship"
        )

        list_data_insert = [{
            "customer_id": cif_id,
            "customer_relationship_type_id": customer_relationship.customer_relationship.id,
            "type": CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP,
            "customer_personal_relationship_cif_number": customer_relationship.cif_number,
        } for customer_relationship in customer_relationship_save_request]

        save_customer_relationship_info = self.call_repos(
            await repos_save_guardians(
                cif_id=cif_id,
                list_data_insert=list_data_insert,
                created_by="TUONGHD",
                session=self.oracle_session,
                relationship_type=CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP,
                log_data=log_data,
                business_form_id=BUSINESS_FORM_TTCN_MQHKH
            ))

        return self.response(data=save_customer_relationship_info)
