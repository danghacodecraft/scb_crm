from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.guardian.repository import (
    repos_get_guardians, repos_get_guardians_by_cif_numbers,
    repos_save_guardians
)
from app.api.v1.endpoints.cif.basic_information.guardian.schema import (
    SaveGuardianRequest
)
from app.api.v1.endpoints.cif.basic_information.repository import (
    repos_get_customer_detail_by_cif_number
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_NGH, CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN
)
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_DUPLICATED, ERROR_RELATION_CUSTOMER_SELF_RELATED,
    ERROR_RELATIONSHIP_NOT_GUARDIAN
)
from app.utils.functions import orjson_dumps


class CtrGuardian(BaseController):
    async def detail(self, cif_id: str):
        detail_guardian_info = self.call_repos(
            await repos_get_guardians(
                session=self.oracle_session,
                cif_id=cif_id
            ))

        return self.response(data=detail_guardian_info)

    async def save(self,
                   cif_id: str,
                   guardian_save_request: List[SaveGuardianRequest]):
        # check and get current customer
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        guardian_cif_numbers, log_data, relationship_types = [], [], set()
        for guardian in guardian_save_request:
            guardian_cif_numbers.append(guardian.cif_number),
            # lấy danh sách các loại mối quan hệ để kiểm tra,
            # xài set để hàm check không bị lỗi khi số lượng không giống nhau
            relationship_types.add(guardian.customer_relationship.id)
            # parse về dict để ghi log
            guardian_log = {
                "cif_number": guardian.cif_number,
                "customer_relationship": {
                    "id": guardian.customer_relationship.id
                }
            }
            log_data.append(orjson_dumps(guardian_log))

        # check duplicate cif_number in request body
        if len(guardian_cif_numbers) != len(set(guardian_cif_numbers)):
            return self.response_exception(
                msg=ERROR_CIF_NUMBER_DUPLICATED,
                loc="cif_number",
            )

        # check if it relates to itself
        if current_customer.cif_number in guardian_cif_numbers:
            return self.response_exception(
                msg=ERROR_RELATION_CUSTOMER_SELF_RELATED,
                loc="cif_number",
            )

        # check guardian's existence
        guardians = self.call_repos(
            await repos_get_guardians_by_cif_numbers(
                cif_numbers=guardian_cif_numbers,
                session=self.oracle_session
            )
        )

        # # check relationship types exist
        # await self.get_model_objects_by_ids(
        #     model=CustomerRelationshipType,
        #     model_ids=list(relationship_types),
        #     loc="customer_relationship"
        # )
        # Kiểm tra người giám hộ có tồn tại trong Core không
        for guardian in guardian_save_request:
            self.call_repos(await repos_get_customer_detail_by_cif_number(
                cif_number=guardian.cif_number,
                session=self.oracle_session
            ))

        # guardians_cif_number__id = {}
        for index, guardian in enumerate(guardians):
            # guardians_cif_number__id[guardian.Customer.cif_number] = guardian.Customer.id
            # Đảm bảo người giám hộ không có người giám hộ
            if guardian.has_guardian:
                return self.response_exception(
                    msg=ERROR_RELATIONSHIP_NOT_GUARDIAN,
                    loc=f"{index} -> cif_number",
                )

        list_data_insert = [{
            "customer_id": cif_id,
            "customer_relationship_type_id": guardian.customer_relationship.id,
            "type": CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN,
            "customer_personal_relationship_cif_number": guardian.cif_number
        } for guardian in guardian_save_request]

        save_guardian_info = self.call_repos(
            await repos_save_guardians(
                cif_id=cif_id,
                list_data_insert=list_data_insert,
                created_by=self.current_user.username,
                session=self.oracle_session,
                log_data=log_data,
                business_form_id=BUSINESS_FORM_TTCN_NGH
            ))

        return self.response(data=save_guardian_info)
