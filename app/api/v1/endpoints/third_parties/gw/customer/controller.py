from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name
)
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_get_customer_ids_from_cif_numbers, repos_gw_get_authorized,
    repos_gw_get_co_owner, repos_gw_get_customer_info_detail,
    repos_gw_get_customer_info_list
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType, CustomerType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import (
    Branch, Career, MaritalStatus, ResidentStatus
)
from app.utils.constant.cif import CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT, GW_GENDER_FEMALE, GW_GENDER_MALE,
    GW_LOC_CHECK_CIF_EXIST, GW_REQUEST_PARAMETER_DEBIT_CARD,
    GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP
)
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown, dropdown_name,
    optional_dropdown
)
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, split_name
)


class CtrGWCustomer(BaseController):
    async def ctr_gw_get_customer_info_list(
            self,
            cif_number: str,
            identity_number: str,
            mobile_number: str,
            full_name: str
    ):
        current_user = self.current_user
        customer_info_list = self.call_repos(await repos_gw_get_customer_info_list(
            cif_number=cif_number,
            identity_number=identity_number,
            mobile_number=mobile_number,
            full_name=full_name,
            current_user=current_user
        ))
        response_data = {}
        customer_list = customer_info_list["selectCustomerRefDataMgmtCIFNum_out"]["data_output"]["customer_list"]

        customer_list_info = []
        cif_numbers = []

        for customer in customer_list:
            customer_info = customer["customer_info_item"]['customer_info']

            cif_info = customer_info['cif_info']
            id_info = customer_info['id_info']

            address_info = customer_info['address_info']
            branch_info = customer_info['branch_info']

            date_of_birth = date_string_to_other_date_string_format(
                date_input=customer_info['birthday'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            martial_status_code_or_name = customer_info['martial_status']
            martial_status = await get_optional_model_object_by_code_or_name(
                model=MaritalStatus,
                model_code=martial_status_code_or_name,
                model_name=martial_status_code_or_name,
                session=self.oracle_session
            )
            dropdown_martial_status = optional_dropdown(obj=martial_status, obj_name=martial_status_code_or_name)

            gender_code_or_name = customer_info["gender"]
            if gender_code_or_name == GW_GENDER_MALE:
                gender_code_or_name = CRM_GENDER_TYPE_MALE
            if gender_code_or_name == GW_GENDER_FEMALE:
                gender_code_or_name = CRM_GENDER_TYPE_FEMALE
            gender = await get_optional_model_object_by_code_or_name(
                model=CustomerGender,
                model_code=gender_code_or_name,
                model_name=gender_code_or_name,
                session=self.oracle_session
            )
            dropdown_gender = dropdown(gender) if gender else dropdown_name(gender_code_or_name)

            nationality_code_or_name = customer_info["nationality_code"]

            nationality = await get_optional_model_object_by_code_or_name(
                model=AddressCountry,
                model_code=nationality_code_or_name,
                model_name=nationality_code_or_name,
                session=self.oracle_session
            )
            dropdown_nationality = dropdown(nationality) if nationality else dropdown_name(nationality_code_or_name)

            customer_type_code_or_name = customer_info['customer_type']
            customer_type = await get_optional_model_object_by_code_or_name(
                model=CustomerType,
                model_code=customer_type_code_or_name,
                model_name=customer_type_code_or_name,
                session=self.oracle_session
            )
            dropdown_customer_type = dropdown(customer_type) if customer_type else dropdown_name(
                customer_type_code_or_name)

            cif_issued_date = date_string_to_other_date_string_format(
                date_input=cif_info['cif_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            id_issued_date = date_string_to_other_date_string_format(
                date_input=id_info['id_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            id_expired_date = date_string_to_other_date_string_format(
                date_input=id_info['id_expired_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )
            place_of_issue_code_or_name = id_info["id_issued_location"]
            place_of_issue = await get_optional_model_object_by_code_or_name(
                model=PlaceOfIssue,
                model_code=place_of_issue_code_or_name,
                model_name=place_of_issue_code_or_name,
                session=self.oracle_session
            )
            dropdown_place_of_issue = dropdown(place_of_issue) if place_of_issue else dropdown_name(
                place_of_issue_code_or_name)

            customer_list_info.append(dict(
                fullname_vn=customer_info['full_name'],
                date_of_birth=date_of_birth,
                martial_status=dropdown_martial_status,
                gender=dropdown_gender,
                email=customer_info['email'],
                nationality=dropdown_nationality,
                mobile_phone=customer_info['mobile_phone'],
                telephone=customer_info['telephone'],
                otherphone=customer_info['otherphone'],
                customer_type=dropdown_customer_type,
                cif_info=dict(
                    cif_number=cif_info['cif_num'],
                    issued_date=cif_issued_date
                ),
                id_info=dict(
                    number=id_info['id_num'],
                    name=id_info['id_name'],
                    issued_date=id_issued_date,
                    expired_date=id_expired_date,
                    place_of_issue=dropdown_place_of_issue
                ),
                address_info=dict(
                    address_full=address_info['address_full']
                ),
                branch_info=dict(
                    name=branch_info['branch_name'],
                    code=branch_info['branch_code'],
                )
            ))
            cif_numbers.append(cif_info['cif_num'])

        cif_in_db = self.call_repos(await repos_get_customer_ids_from_cif_numbers(
            cif_numbers=cif_numbers, session=self.oracle_session))
        for customer_id, cif_number in cif_in_db:
            for customer in customer_list_info:
                if cif_number == customer['cif_info']['cif_number']:
                    customer['cif_info'].update(customer_id=customer_id)

        response_data.update({
            "customer_info_list": customer_list_info,
            "total_items": len(customer_list_info)
        })

        return self.response(data=response_data)

    async def ctr_gw_get_customer_info_detail(self, cif_number: str, parameter: str):
        current_user = self.current_user
        customer_info_detail = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number, current_user=current_user))

        customer_info = customer_info_detail['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info']

        cif_info = customer_info['cif_info']
        cif_issued_date = date_string_to_other_date_string_format(
            date_input=cif_info['cif_issued_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        date_of_birth = date_string_to_other_date_string_format(
            date_input=customer_info['birthday'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        gender_code_or_name = customer_info["gender"]
        if gender_code_or_name == GW_GENDER_MALE:
            gender_code_or_name = CRM_GENDER_TYPE_MALE
        if gender_code_or_name == GW_GENDER_FEMALE:
            gender_code_or_name = CRM_GENDER_TYPE_FEMALE
        gender = await get_optional_model_object_by_code_or_name(
            model=CustomerGender,
            model_code=gender_code_or_name,
            model_name=gender_code_or_name,
            session=self.oracle_session
        )
        dropdown_gender = dropdown(gender) if gender else dropdown_name(gender_code_or_name)

        customer_type_code_or_name = customer_info['customer_type']
        customer_type = await get_optional_model_object_by_code_or_name(
            model=CustomerType,
            model_code=customer_type_code_or_name,
            model_name=customer_type_code_or_name,
            session=self.oracle_session
        )
        dropdown_customer_type = dropdown(customer_type) if customer_type else dropdown_name(customer_type_code_or_name)

        full_name_vn = customer_info['full_name']
        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        # Tách Họ, Tên và Ten đệm
        last_name, middle_name, first_name = split_name(full_name_vn)

        nationality_code_or_name = customer_info["nationality_code"]
        nationality = await get_optional_model_object_by_code_or_name(
            model=AddressCountry,
            model_code=nationality_code_or_name,
            model_name=nationality_code_or_name,
            session=self.oracle_session
        )
        dropdown_nationality = dropdown(nationality) if nationality else dropdown_name(nationality_code_or_name)

        identity_info = customer_info['id_info']
        place_of_issue_code_or_name = identity_info["id_issued_location"]
        place_of_issue = await get_optional_model_object_by_code_or_name(
            model=PlaceOfIssue,
            model_code=place_of_issue_code_or_name,
            model_name=place_of_issue_code_or_name,
            session=self.oracle_session
        )
        dropdown_place_of_issue = dropdown(place_of_issue) if place_of_issue else dropdown_name(
            place_of_issue_code_or_name)

        resident_address_info = customer_info['p_address_info']

        resident_address_province_code_or_name = resident_address_info["city_name"]
        resident_address_province = await get_optional_model_object_by_code_or_name(
            model=AddressProvince,
            model_code=resident_address_province_code_or_name,
            model_name=resident_address_province_code_or_name,
            session=self.oracle_session
        )
        dropdown_resident_address_province = dropdown(
            resident_address_province) if resident_address_province else dropdown_name(
            resident_address_province_code_or_name)

        resident_address_district_code_or_name = resident_address_info["district_name"]
        resident_address_district = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=resident_address_district_code_or_name,
            model_name=resident_address_district_code_or_name,
            session=self.oracle_session
        )
        dropdown_resident_address_district = dropdown(
            resident_address_district) if resident_address_district else dropdown_name(
            resident_address_district_code_or_name)

        resident_address_ward_code_or_name = resident_address_info["ward_name"]
        resident_address_ward = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=resident_address_ward_code_or_name,
            model_name=resident_address_ward_code_or_name,
            session=self.oracle_session
        )
        dropdown_resident_address_ward = dropdown(
            resident_address_ward) if resident_address_ward else dropdown_name(resident_address_ward_code_or_name)

        resident_address_number_and_street = resident_address_info["line"]

        resident_address_full = resident_address_info["address_full"]

        resident_address_response = dict(
            province=dropdown_resident_address_province,
            district=dropdown_resident_address_district,
            ward=dropdown_resident_address_ward,
            number_and_street=resident_address_number_and_street,
            address_full=resident_address_full
        )

        contact_address_info = customer_info['t_address_info']

        contact_address_province_code_or_name = contact_address_info["contact_address_city_name"]
        contact_address_province = await get_optional_model_object_by_code_or_name(
            model=AddressProvince,
            model_code=contact_address_province_code_or_name,
            model_name=contact_address_province_code_or_name,
            session=self.oracle_session
        )
        dropdown_contact_address_province = dropdown(
            contact_address_province) if contact_address_province else dropdown_name(
            contact_address_province_code_or_name)

        contact_address_district_code_or_name = contact_address_info["contact_address_district_name"]
        contact_address_district = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=contact_address_district_code_or_name,
            model_name=contact_address_district_code_or_name,
            session=self.oracle_session
        )
        dropdown_contact_address_district = dropdown(
            contact_address_district) if contact_address_district else dropdown_name(
            contact_address_district_code_or_name)

        contact_address_ward_code_or_name = contact_address_info["contact_address_ward_name"]
        contact_address_ward = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=contact_address_ward_code_or_name,
            model_name=contact_address_ward_code_or_name,
            session=self.oracle_session
        )
        dropdown_contact_address_ward = dropdown(
            contact_address_ward) if contact_address_ward else dropdown_name(contact_address_ward_code_or_name)

        contact_address_number_and_street = contact_address_info["contact_address_line"]

        contact_address_full = contact_address_info["contact_address_full"]

        identity_issued_date = date_string_to_other_date_string_format(
            date_input=identity_info['id_issued_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )
        mobile = customer_info['mobile_phone']
        telephone = customer_info['telephone']
        email = customer_info['email']

        branch_info = customer_info['branch_info']
        branch_name = branch_info["branch_name"]
        branch_code = branch_info["branch_code"]
        branch = await get_optional_model_object_by_code_or_name(
            model=Branch,
            model_code=branch_code,
            model_name=branch_name,
            session=self.oracle_session
        )
        dropdown_branch = optional_dropdown(obj=branch, obj_name=branch_name, obj_code=branch_code)

        delivery_address_response = dict(
            province=dropdown_resident_address_province,
            district=dropdown_resident_address_district,
            ward=dropdown_resident_address_ward,
            number_and_street=resident_address_number_and_street,
            address_full=resident_address_full
        )

        if parameter == GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP:
            cif_information = dict(
                cif_number=cif_number,
                issued_date=cif_issued_date,
                customer_type=dropdown_customer_type
            )

            customer_information = dict(
                full_name=full_name,
                full_name_vn=full_name_vn,
                last_name=last_name,
                middle_name=middle_name,
                first_name=first_name,
                date_of_birth=date_of_birth,
                gender=dropdown_gender,
                nationality=dropdown_nationality,
                mobile=mobile,
                telephone=telephone,
                email=email
            )

            identity_information = dict(
                identity_number=identity_info['id_num'],
                issued_date=identity_issued_date,
                expired_date=date_string_to_other_date_string_format(
                    date_input=identity_info['id_expired_date'],
                    from_format=GW_DATETIME_FORMAT,
                    to_format=GW_DATE_FORMAT
                ),
                place_of_issue=dropdown_place_of_issue
            )

            contact_address_response = dict(
                province=dropdown_contact_address_province,
                district=dropdown_contact_address_district,
                ward=dropdown_contact_address_ward,
                number_and_street=contact_address_number_and_street,
                address_full=contact_address_full
            )

            customer_information = dict(
                cif_information=cif_information,
                customer_information=customer_information,
                # career_information=career_information,
                identity_information=identity_information,
                address_info=dict(
                    resident_address=resident_address_response,
                    contact_address=contact_address_response
                )
            )
        elif parameter == GW_REQUEST_PARAMETER_DEBIT_CARD:
            customer_information = dict(
                cif_number=cif_number,
                name_on_card=dict(
                    last_name_on_card=last_name,
                    middle_name_on_card=middle_name,
                    first_name_on_card=first_name
                ),
                card_delivery_address=dict(
                    branch=dropdown_branch,
                    delivery_address=delivery_address_response
                )
            )
        else:
            data_output = customer_info_detail['retrieveCustomerRefDataMgmt_out']['data_output']
            customer_info = data_output['customer_info']

            job_info = customer_info['job_info']

            short_name = customer_info['short_name']

            martial_status_code_or_name = customer_info['martial_status']
            martial_status = await get_optional_model_object_by_code_or_name(
                model=MaritalStatus,
                model_code=martial_status_code_or_name,
                model_name=martial_status_code_or_name,
                session=self.oracle_session
            )
            dropdown_martial_status = optional_dropdown(obj=martial_status, obj_name=martial_status_code_or_name)

            resident_status_code_or_name = customer_info['resident_status']
            resident_status = await get_optional_model_object_by_code_or_name(
                model=ResidentStatus,
                model_code=resident_status_code_or_name,
                model_name=resident_status_code_or_name,
                session=self.oracle_session
            )
            dropdown_resident_status = optional_dropdown(obj=resident_status, obj_name=resident_status_code_or_name)

            identity_expired_date = date_string_to_other_date_string_format(
                date_input=identity_info['id_expired_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            biz_license_issue_date = date_string_to_other_date_string_format(
                date_input=customer_info['biz_license_issue_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            job_name = job_info["professional_name"]
            job_code = job_info["professional_code"]
            job = await get_optional_model_object_by_code_or_name(
                model=Career,
                model_code=job_code,
                model_name=job_name,
                session=self.oracle_session
            )
            dropdown_job = optional_dropdown(obj=job, obj_name=job_name, obj_code=job_code)

            return self.response(data=dict(
                fullname_vn=full_name_vn,
                short_name=short_name,
                date_of_birth=date_of_birth,
                martial_status=dropdown_martial_status,
                gender=dropdown_gender,
                email=email,
                nationality=dropdown_nationality,
                mobile_phone=customer_info['mobile_phone'],
                telephone=customer_info['telephone'],
                otherphone=customer_info['otherphone'],
                customer_type=dropdown_customer_type,
                resident_status=dropdown_resident_status,
                legal_representativeprsn_name=customer_info['legal_representativeprsn_name'],
                legal_representativeprsn_id=customer_info['legal_representativeprsn_id'],
                biz_contact_person_phone_num=customer_info['biz_contact_person_phone_num'],
                biz_line=customer_info['biz_line'],
                biz_license_issue_date=biz_license_issue_date,
                is_staff=customer_info['is_staff'],
                cif_info=dict(
                    cif_number=cif_number,
                    issued_date=cif_issued_date
                ),
                id_info=dict(
                    number=identity_info["id_num"],
                    name=identity_info["id_name"],
                    issued_date=identity_issued_date,
                    expired_date=identity_expired_date,
                    place_of_issue=dropdown_place_of_issue
                ),
                resident_address=dict(
                    address_full=resident_address_info['address_full'],
                    number_and_street=resident_address_info['line'],
                    ward=dropdown_resident_address_ward,
                    district=dropdown_resident_address_district,
                    province=dropdown_resident_address_province
                ),
                contact_address=dict(
                    address_full=contact_address_info['contact_address_full'],
                    number_and_street=contact_address_info['contact_address_line'],
                    ward=dropdown_contact_address_ward,
                    district=dropdown_contact_address_district,
                    province=dropdown_contact_address_province
                ),
                job_info=dropdown_job,
                branch_info=dropdown_branch
            ))

        return self.response(data=customer_information)

    async def ctr_gw_check_exist_customer_detail_info(
        self,
        cif_number: str
    ):
        gw_check_exist_customer_detail_info = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number,
            current_user=self.current_user,
            loc=GW_LOC_CHECK_CIF_EXIST
        ))
        data_output = gw_check_exist_customer_detail_info['retrieveCustomerRefDataMgmt_out']['data_output']
        customer_info = data_output['customer_info']['id_info']

        return self.response(data=dict(
            is_existed=True if customer_info['id_num'] else False
        ))

    async def ctr_gw_get_co_owner(self, account_number: str):
        current_user = self.current_user
        co_owner_info_list = self.call_repos(await repos_gw_get_co_owner(
            account_number=account_number, current_user=current_user))

        co_owner_list = co_owner_info_list["selectCoownerRefDataMgmtAccNum_out"]["data_output"][
            "coowner_info_list"]

        data_response = []

        for co_owner in co_owner_list:
            co_owner_info = co_owner["coowner_info_item"]['customer_info']
            cif_info = co_owner_info['cif_info']
            identity_info = co_owner_info['id_info']
            address_info = co_owner_info['address_info']

            gender_code_or_name = co_owner_info['gender']
            if gender_code_or_name == GW_GENDER_MALE:
                gender_code_or_name = CRM_GENDER_TYPE_MALE
            if gender_code_or_name == GW_GENDER_FEMALE:
                gender_code_or_name = CRM_GENDER_TYPE_FEMALE
            gender = await get_optional_model_object_by_code_or_name(
                model=CustomerGender,
                model_code=gender_code_or_name,
                model_name=None,
                session=self.oracle_session
            )
            dropdown_gender = optional_dropdown(obj=gender, obj_name=gender_code_or_name)

            nationality_code_or_name = co_owner_info["nationality_code"]
            nationality = await get_optional_model_object_by_code_or_name(
                model=AddressCountry,
                model_code=nationality_code_or_name,
                model_name=nationality_code_or_name,
                session=self.oracle_session
            )
            dropdown_nationality = optional_dropdown(obj=nationality, obj_name=nationality_code_or_name)

            customer_type_code_or_name = co_owner_info['customer_type']
            customer_type = await get_optional_model_object_by_code_or_name(
                model=CustomerType,
                model_code=customer_type_code_or_name,
                model_name=None,
                session=self.oracle_session
            )
            dropdown_customer_type = optional_dropdown(
                obj=customer_type,
                obj_name=customer_type_code_or_name
            )

            customer_relationship_code_or_name = co_owner_info['coowner_relationship']
            customer_relationship = await get_optional_model_object_by_code_or_name(
                model=CustomerRelationshipType,
                model_code=customer_relationship_code_or_name,
                model_name=None,
                session=self.oracle_session
            )
            dropdown_customer_relationship = optional_dropdown(
                obj=customer_relationship,
                obj_name=customer_relationship_code_or_name
            )

            cif_issued_date = date_string_to_other_date_string_format(
                date_input=cif_info['cif_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            identity_issued_date = date_string_to_other_date_string_format(
                date_input=identity_info['id_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            identity_expired_date = date_string_to_other_date_string_format(
                date_input=identity_info['id_expired_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            place_of_issue_code_or_name = identity_info["id_issued_location"]
            place_of_issue = await get_optional_model_object_by_code_or_name(
                model=PlaceOfIssue,
                model_code=None,
                model_name=place_of_issue_code_or_name,
                session=self.oracle_session
            )
            dropdown_place_of_issue = optional_dropdown(obj=place_of_issue, obj_name=place_of_issue_code_or_name)

            date_of_birth = date_string_to_other_date_string_format(
                date_input=co_owner_info['birthday'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            data_response.append(dict(
                full_name_vn=co_owner_info['full_name'],
                date_of_birth=date_of_birth,
                gender=dropdown_gender,
                email=co_owner_info['email'],
                mobile_phone=co_owner_info['mobile_phone'],
                nationality=dropdown_nationality,
                customer_type=dropdown_customer_type,
                co_owner_relationship=dropdown_customer_relationship,
                cif_info=dict(
                    cif_number=cif_info['cif_num'],
                    issued_date=cif_issued_date
                ),
                id_info=dict(
                    number=identity_info['id_num'],
                    name=identity_info['id_name'],
                    issued_date=identity_issued_date,
                    expired_date=identity_expired_date,
                    place_of_issue=dropdown_place_of_issue
                ),
                address_info=dict(
                    contact_address_full=address_info['contact_address_full'],
                    address_full=address_info['address_full']
                )
            ))

        return self.response(data={
            "co_owner_info_list": data_response,
            "total_items": len(data_response)
        })

    async def ctr_gw_get_authorized(self, account_number: str):
        current_user = self.current_user
        authorized_info_list = self.call_repos(await repos_gw_get_authorized(
            account_number=account_number, current_user=current_user))

        response_data = {}
        authorized_list = authorized_info_list["selectAuthorizedRefDataMgmtAccNum_out"]["data_output"][
            "authorized_info_list"]

        data_response = []

        for authorized in authorized_list:
            authorized_info = authorized["authorized_info_item"]['customer_info']
            cif_info = authorized_info['cif_info']
            id_info = authorized_info['id_info']
            address_info = authorized_info['address_info']

            data_response.append(dict(
                full_name_vn=authorized_info['full_name'],
                date_of_birth=authorized_info['birthday'],
                gender=authorized_info['gender'],
                email=authorized_info['email'],
                mobile_phone=authorized_info['mobile_phone'],
                nationality_code=authorized_info['nationality_code'],
                customer_type=authorized_info['customer_type'],
                coowner_relationship=authorized_info['coowner_relationship'],
                cif_info=dict(
                    cif_number=cif_info['cif_num'],
                    issued_date=cif_info['cif_issued_date']
                ),
                id_info=dict(
                    number=id_info['id_num'],
                    name=id_info['id_name'],
                    issued_date=id_info['id_issued_date'],
                    expired_date=id_info['id_expired_date'],
                    place_of_issue=id_info['id_issued_location']
                ),
                address_info=dict(
                    contact_address_full=address_info['contact_address_full'],
                    address_full=address_info['address_full']
                )
            ))

            response_data.update({
                "authorized_info_list": data_response,
                "total_items": len(data_response)
            })

            return self.response(data=response_data)
