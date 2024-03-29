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
    repos_get_booking, repos_get_initializing_customer
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.settings.event import service_gw
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_MQHKH, CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE,
    CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP
)
from app.utils.constant.gw import GW_GENDER_FEMALE, GW_GENDER_MALE
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_CIF_NUMBER_DUPLICATED,
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_RELATION_CUSTOMER_SELF_RELATED
)
from app.utils.functions import dropdown, orjson_dumps, string_to_date


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

            gender_code = customer_relationship_data["gender"]
            if gender_code == GW_GENDER_MALE:
                gender_code = CRM_GENDER_TYPE_MALE
            if gender_code == GW_GENDER_FEMALE:
                gender_code = CRM_GENDER_TYPE_FEMALE

            dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerGender, name=None, code=gender_code
            )

            nationality_code = customer_relationship_data["nationality_code"]

            dropdown_nationality = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressCountry, name=None, code=nationality_code
            )

            resident_address = customer_relationship_data["p_address_info"]
            contact_address = customer_relationship_data["t_address_info"]

            resident_city_name = resident_address["city_name"]

            resident_dropdown_city = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressProvince, name=resident_city_name, code=resident_city_name
            )

            resident_district_name = resident_address["district_name"]

            resident_dropdown_district = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressDistrict, name=resident_district_name, code=resident_district_name
            )

            resident_ward_name = resident_address["ward_name"]

            resident_dropdown_ward = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressWard, name=resident_ward_name, code=resident_ward_name
            )

            contact_city_name = contact_address["contact_address_city_name"]

            contact_dropdown_city = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressProvince, name=contact_city_name, code=contact_city_name
            )

            contact_district_name = contact_address["contact_address_district_name"]

            contact_dropdown_district = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressDistrict, name=contact_district_name, code=contact_district_name
            )

            contact_address_ward = contact_address["contact_address_ward_name"]

            contact_dropdown_ward = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressWard, name=contact_address_ward, code=contact_address_ward
            )

            identity_document = customer_relationship_data['id_info']

            place_of_issue = identity_document['id_issued_location']

            dropdown_place_of_issue = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=PlaceOfIssue, name=place_of_issue, code=place_of_issue
            )

            customer_relationship_item.update(
                id=relationship.customer_personal_relationship_cif_number,
                avatar_url=None,
                basic_information=dict(
                    cif_number=relationship.customer_personal_relationship_cif_number,
                    full_name_vn=customer_relationship_data['full_name'],
                    customer_relationship=dropdown(relationship_type),
                    date_of_birth=string_to_date(customer_relationship_data['birthday'],
                                                 _format=DATETIME_INPUT_OUTPUT_FORMAT),
                    gender=dropdown_gender,
                    nationality=dropdown_nationality,
                    telephone_number=customer_relationship_data['telephone'],
                    mobile_number=customer_relationship_data['mobile_phone'],
                    email=customer_relationship_data['email']),
                identity_document=dict(
                    identity_number=identity_document['id_num'],
                    issued_date=string_to_date(identity_document['id_issued_date'],
                                               _format=DATETIME_INPUT_OUTPUT_FORMAT),
                    expired_date=string_to_date(identity_document['id_expired_date'],
                                                _format=DATETIME_INPUT_OUTPUT_FORMAT),
                    place_of_issue=dropdown_place_of_issue
                ),
                address_information=dict(
                    resident_address=dict(
                        province=resident_dropdown_city,
                        district=resident_dropdown_district,
                        ward=resident_dropdown_ward,
                        number_and_street=resident_address["line"]
                    ),
                    contact_address=dict(
                        province=contact_dropdown_city,
                        district=contact_dropdown_district,
                        ward=contact_dropdown_ward,
                        number_and_street=contact_address["contact_address_line"]
                    )))
            relationship_details.append(customer_relationship_item)

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))

        data = dict(
            customer_relationship_flag=True if detail_customer_relationship_info else False,
            number_of_customer_relationship=len(detail_customer_relationship_info),
            relationships=relationship_details,
            booking=dict(
                id=booking.id,
                code=booking.code,
            )
        )

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
            # check số cif có tồn tại trong GW
            check_is_exist = await CtrGWCustomer(current_user).ctr_gw_check_exist_customer_detail_info(
                cif_number=customer_relationship.cif_number
            )
            if not check_is_exist['data']['is_existed']:
                return self.response_exception(msg=ERROR_CIF_NUMBER_NOT_EXIST)

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
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        save_customer_relationship_info.update(booking=dict(
            id=booking.id,
            code=booking.code
        ))

        return self.response(data=save_customer_relationship_info)
