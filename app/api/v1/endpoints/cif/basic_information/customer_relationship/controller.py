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
    repos_check_exist_cif, repos_get_booking_code,
    repos_get_initializing_customer
)
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.settings.event import service_gw
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_MQHKH, CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP,
    DROPDOWN_NONE_DICT
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_CIF_NUMBER_DUPLICATED,
    ERROR_RELATION_CUSTOMER_SELF_RELATED
)
from app.utils.functions import (
    dropdown, dropdown_name, orjson_dumps, string_to_date
)


class CtrCustomerRelationship(BaseController):
    async def detail(self, cif_id: str):
        detail_customer_relationship_info = self.call_repos(
            await repos_get_customer_relationships(
                cif_id=cif_id,
                session=self.oracle_session,
            ))

        relationship_details = []
        for relationship, relationship_type in detail_customer_relationship_info:
            is_success, customer_relationship = await service_gw.get_customer_info_detail(
                customer_cif_number=relationship.customer_personal_relationship_cif_number,
                current_user=self.current_user.user_info
            )
            if not is_success:
                return self.response_exception(
                    msg=ERROR_CALL_SERVICE_GW,
                    detail='customer_relationship',
                    loc='customer_relationship'
                )

            customer_relationship_item = {}

            customer_relationship_data = customer_relationship['retrieveCustomerRefDataMgmt_out']['data_output'][
                'customer_info']

            identity_document = customer_relationship_data['id_info']

            resident_address = customer_relationship_data["p_address_info"]
            contact_address = customer_relationship_data["t_address_info"]

            customer_relationship_item.update(
                id=relationship.customer_personal_relationship_cif_number,
                avatar_url=None,
                basic_information=dict(
                    cif_number=relationship.customer_personal_relationship_cif_number,
                    full_name_vn=customer_relationship_data['full_name'],
                    customer_relationship=dropdown(relationship_type),
                    date_of_birth=string_to_date(customer_relationship_data['birthday'],
                                                 _format=DATETIME_INPUT_OUTPUT_FORMAT),
                    gender=dropdown_name(customer_relationship_data["gender"])
                    if customer_relationship_data["gender"] else DROPDOWN_NONE_DICT,
                    nationality=dropdown_name(customer_relationship_data["nationality_code"])
                    if customer_relationship_data["nationality_code"] else DROPDOWN_NONE_DICT,
                    telephone_number=customer_relationship_data['telephone'],
                    mobile_number=customer_relationship_data['mobile_phone'],
                    email=customer_relationship_data['email']),
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
            relationship_details.append(customer_relationship_item)

        data = {
            'customer_relationship_flag': True if detail_customer_relationship_info else False,
            'number_of_customer_relationship': len(detail_customer_relationship_info),
            "relationships": relationship_details
        }

        return self.response(data=data)

    async def save(self,
                   cif_id: str,
                   customer_relationship_save_request: List[SaveCustomerRelationshipRequest]):
        # check and get current customer
        current_user = self.current_user.user_info
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
                created_by=current_user.username,
                session=self.oracle_session,
                relationship_type=CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP,
                log_data=orjson_dumps(log_data),
                business_form_id=BUSINESS_FORM_TTCN_MQHKH
            ))

        # Lấy Booking Code
        booking_code = self.call_repos(await repos_get_booking_code(
            cif_id=cif_id, session=self.oracle_session
        ))
        save_customer_relationship_info.update(booking_code=booking_code)

        return self.response(data=save_customer_relationship_info)
