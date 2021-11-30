import re

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.personal.repository import (
    repos_get_contact_type_data, repos_get_personal_data, repos_save_personal
)
from app.api.v1.endpoints.cif.basic_information.personal.schema import (
    PersonalRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressProvince
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerTitle
)
from app.third_parties.oracle.models.master_data.others import (
    MaritalStatus, ResidentStatus
)
from app.utils.constant.cif import (
    CUSTOMER_CONTACT_TYPE_EMAIL, CUSTOMER_CONTACT_TYPE_MOBILE
)
from app.utils.functions import now
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, make_short_name, split_name
)


class CtrPersonal(BaseController):
    async def ctr_save_personal(self, cif_id: str, personal_request: PersonalRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        contact_type_data = self.call_repos(
            await repos_get_contact_type_data(cif_id=cif_id, session=self.oracle_session))

        # TODO : chưa có data contact_type nên đang để test
        list_contact_type_data = [
            {
                "customer_contact_type_id": CUSTOMER_CONTACT_TYPE_EMAIL,
                "customer_id": cif_id,
                "customer_contact_type_created_at": now(),
                "active_flag": personal_request.contact_method.email_flag,
                "order_no": 1
            },
            {
                "customer_contact_type_id": CUSTOMER_CONTACT_TYPE_MOBILE,
                "customer_id": cif_id,
                "customer_contact_type_created_at": now(),
                "active_flag": personal_request.contact_method.mobile_number_flag,
                "order_no": 1
            }
        ]

        full_name_vn = personal_request.full_name_vn
        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        first_name, middle_name, last_name = split_name(full_name)
        if first_name is None and middle_name is None and last_name is None:
            return self.response_exception(msg='', detail='Can not split name to fist, middle and last name')

        # check nationality_id
        nationality_id = personal_request.nationality.id
        await self.get_model_object_by_id(model_id=nationality_id, model=AddressCountry, loc='nationality_id')

        # check gender_id
        gender_id = personal_request.gender.id
        await self.get_model_object_by_id(model_id=gender_id, model=CustomerGender, loc='gender_id')

        # check title_id
        title_id = personal_request.honorific.id
        await self.get_model_object_by_id(model_id=title_id, model=CustomerTitle, loc='title_id')

        # check place_of_birth_id
        place_of_birth_id = personal_request.place_of_birth.id
        await self.get_model_object_by_id(model_id=place_of_birth_id, model=AddressProvince, loc='place_of_birth_id')

        # check country_of_birth_id
        country_of_birth_id = personal_request.country_of_birth.id
        await self.get_model_object_by_id(model_id=country_of_birth_id, model=AddressCountry, loc='country_of_birth_id')

        # check resident_status_id
        resident_status_id = personal_request.resident_status.id
        await self.get_model_object_by_id(model_id=resident_status_id, model=ResidentStatus, loc='resident_status_id')

        # check marital_status_id
        marital_status_id = personal_request.marital_status.id
        await self.get_model_object_by_id(model_id=marital_status_id, model=MaritalStatus, loc='marital_status_id')

        regex = r'0([0-9]{9})'
        number = re.search(regex, personal_request.mobile_number)
        if not number:
            return self.response_exception(loc='mobile_number', msg='MOBILE_IN_VALID', detail='MOBILE_IN_VALID')

        data_update_customer = {
            "full_name": full_name,
            "full_name_vn": full_name_vn,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "short_name": make_short_name(first_name, middle_name, last_name),
            "email": personal_request.email,
            "telephone_number": personal_request.telephone_number,
            "mobile_number": personal_request.mobile_number,
            "tax_number": personal_request.tax_number,
            "nationality_id": nationality_id
        }

        data_update_customer_individual = {
            "gender_id": gender_id,
            "title_id": title_id,
            "date_of_birth": personal_request.date_of_birth,
            "place_of_birth_id": place_of_birth_id,
            "country_of_birth_id": country_of_birth_id,
            "resident_status_id": resident_status_id,
            "marital_status_id": marital_status_id,
        }

        personal_data = self.call_repos(
            await repos_save_personal(
                cif_id=cif_id,
                data_update_customer=data_update_customer,
                data_update_customer_individual=data_update_customer_individual,
                contact_type_data=contact_type_data,
                list_contact_type_data=list_contact_type_data,
                session=self.oracle_session,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=personal_data)

    async def ctr_personal(self, cif_id: str):
        personal_data = self.call_repos(await repos_get_personal_data(cif_id))

        return self.response(data=personal_data)
