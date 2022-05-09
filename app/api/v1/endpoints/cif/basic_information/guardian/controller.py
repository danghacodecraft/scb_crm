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
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking_code, repos_get_initializing_customer
)
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.settings.event import service_gw
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_NGH, CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN,
    DROPDOWN_NONE_DICT
)
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_DUPLICATED, ERROR_RELATION_CUSTOMER_SELF_RELATED,
    ERROR_RELATIONSHIP_NOT_GUARDIAN
)
from app.utils.functions import (
    dropdown, dropdown_name, orjson_dumps, string_to_date
)


class CtrGuardian(BaseController):
    async def detail(self, cif_id: str):

        guardians = self.call_repos(
            await repos_get_guardians(
                session=self.oracle_session,
                cif_id=cif_id
            ))

        guardian_details = []
        for guardian, guardian_relationship in guardians:
            is_success, guardian_detail = await service_gw.get_customer_info_detail(
                customer_cif_number=guardian.customer_personal_relationship_cif_number,
                current_user=self.current_user.user_info)

            if not is_success:
                return self.response_exception(
                    msg='call gw',
                    loc="cif_number",
                )

            guardian_item = {}

            guardian_detail_data = guardian_detail['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info']

            identity_document = guardian_detail_data['id_info']

            resident_address = guardian_detail_data["p_address_info"]
            contact_address = guardian_detail_data["t_address_info"]

            guardian_item.update(
                id=guardian.customer_personal_relationship_cif_number,
                avatar_url=None,
                basic_information=dict(
                    cif_number=guardian.customer_personal_relationship_cif_number,
                    full_name_vn=guardian_detail_data['full_name'],
                    customer_relationship=dropdown(guardian_relationship),
                    date_of_birth=string_to_date(guardian_detail_data['birthday'],
                                                 _format=DATETIME_INPUT_OUTPUT_FORMAT),
                    gender=dropdown_name(guardian_detail_data["gender"])
                    if guardian_detail_data["gender"] else DROPDOWN_NONE_DICT,
                    nationality=dropdown_name(guardian_detail_data["nationality_code"])
                    if guardian_detail_data["nationality_code"] else DROPDOWN_NONE_DICT,
                    telephone_number=guardian_detail_data['telephone'],
                    mobile_number=guardian_detail_data['mobile_phone'],
                    email=guardian_detail_data['email']),
                identity_document=dict(
                    identity_number=identity_document['id_num'],
                    issued_date=string_to_date(identity_document['id_issued_date'],
                                               _format=DATETIME_INPUT_OUTPUT_FORMAT),
                    expired_date=string_to_date(identity_document['id_expired_date'],
                                                _format=DATETIME_INPUT_OUTPUT_FORMAT),
                    place_of_issue=dropdown_name(identity_document['id_issued_location'])
                    if identity_document['id_issued_location'] else DROPDOWN_NONE_DICT
                ),
                address_information=dict(
                    resident_address=dict(
                        province=dropdown_name(resident_address["city_name"])
                        if resident_address["city_name"] else DROPDOWN_NONE_DICT,
                        district=dropdown_name(resident_address["district_name"])
                        if resident_address["city_name"] else DROPDOWN_NONE_DICT,
                        ward=dropdown_name(resident_address["ward_name"])
                        if resident_address["city_name"] else DROPDOWN_NONE_DICT,
                        number_and_street=resident_address["line"] if resident_address["line"] else None
                    ),
                    contact_address=dict(
                        province=dropdown_name(contact_address["contact_address_city_name"])
                        if contact_address["contact_address_city_name"] else DROPDOWN_NONE_DICT,
                        district=dropdown_name(contact_address["contact_address_district_name"])
                        if contact_address["contact_address_district_name"] else DROPDOWN_NONE_DICT,
                        ward=dropdown_name(contact_address["contact_address_ward_name"])
                        if contact_address["contact_address_ward_name"] else DROPDOWN_NONE_DICT,
                        number_and_street=contact_address["contact_address_line"]
                        if contact_address["contact_address_line"] else None
                    )))

            guardian_details.append(guardian_item)
        data_response = {
            "guardian_flag": True if guardians else False,
            "number_of_guardian": len(guardians),
            "guardians": guardian_details
        }

        return self.response(data=data_response)

    async def save(self,
                   cif_id: str,
                   guardian_save_request: List[SaveGuardianRequest]):
        current_user = self.current_user.user_info
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
                created_by=current_user.username,
                session=self.oracle_session,
                log_data=orjson_dumps(log_data),
                business_form_id=BUSINESS_FORM_TTCN_NGH
            ))

        # Lấy Booking Code
        booking_code = self.call_repos(await repos_get_booking_code(
            cif_id=cif_id, session=self.oracle_session
        ))
        save_guardian_info.update(booking_code=booking_code)

        return self.response(data=save_guardian_info)
