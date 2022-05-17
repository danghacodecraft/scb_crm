from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_get_customer_ids_from_cif_numbers, repos_get_customer_open_cif,
    repos_gw_get_authorized, repos_gw_get_co_owner,
    repos_gw_get_customer_info_detail, repos_gw_get_customer_info_list,
    repos_gw_open_cif
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType, CustomerType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import (
    Branch, Career, MaritalStatus, ResidentStatus
)
from app.utils.constant.cif import (
    CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE, EKYC_GENDER_TYPE_FEMALE,
    EKYC_GENDER_TYPE_MALE, RESIDENT_ADDRESS_CODE
)
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT, GW_GENDER_FEMALE, GW_GENDER_MALE,
    GW_LOC_CHECK_CIF_EXIST, GW_REQUEST_PARAMETER_DEBIT_CARD,
    GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP
)
from app.utils.functions import date_string_to_other_date_string_format
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

            date_of_birth = date_string_to_other_date_string_format(
                date_input=customer_info['birthday'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            martial_status_code_or_name = customer_info['martial_status']

            dropdown_martial_status = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=MaritalStatus, name=martial_status_code_or_name, code=martial_status_code_or_name)

            gender_code_or_name = customer_info["gender"]
            if gender_code_or_name == GW_GENDER_MALE:
                gender_code_or_name = CRM_GENDER_TYPE_MALE
            if gender_code_or_name == GW_GENDER_FEMALE:
                gender_code_or_name = CRM_GENDER_TYPE_FEMALE

            dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerGender, name=gender_code_or_name, code=gender_code_or_name)

            nationality_code_or_name = customer_info["nationality_code"]

            dropdown_nationality = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressCountry, name=nationality_code_or_name, code=nationality_code_or_name)

            customer_type_code_or_name = customer_info['customer_type']

            dropdown_customer_type = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerType, name=customer_type_code_or_name, code=customer_type_code_or_name)

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

            dropdown_place_of_issue = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=PlaceOfIssue, name=place_of_issue_code_or_name, code=place_of_issue_code_or_name)

            branch_info = customer_info['branch_info']
            branch_name = branch_info["branch_name"]
            branch_code = branch_info["branch_code"]

            dropdown_branch = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=Branch, name=branch_name, code=branch_code)

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
                branch_info=dropdown_branch
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

        dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=CustomerGender, name=gender_code_or_name, code=gender_code_or_name
        )

        customer_type_code_or_name = customer_info['customer_type']

        dropdown_customer_type = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=CustomerType, name=customer_type_code_or_name, code=customer_type_code_or_name
        )

        full_name_vn = customer_info['full_name']
        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        # Tách Họ, Tên và Ten đệm
        last_name, middle_name, first_name = split_name(full_name_vn)

        nationality_code_or_name = customer_info["nationality_code"]

        dropdown_nationality = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressCountry, name=nationality_code_or_name, code=nationality_code_or_name
        )

        identity_info = customer_info['id_info']
        place_of_issue_code_or_name = identity_info["id_issued_location"]

        dropdown_place_of_issue = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=PlaceOfIssue, name=place_of_issue_code_or_name, code=place_of_issue_code_or_name
        )

        resident_address_info = customer_info['p_address_info']

        resident_address_province_code_or_name = resident_address_info["city_name"]

        dropdown_resident_address_province = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressProvince, name=resident_address_province_code_or_name,
            code=resident_address_province_code_or_name
        )

        resident_address_district_code_or_name = resident_address_info["district_name"]

        dropdown_resident_address_district = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressDistrict, name=resident_address_district_code_or_name,
            code=resident_address_district_code_or_name
        )

        resident_address_ward_code_or_name = resident_address_info["ward_name"]

        dropdown_resident_address_ward = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressWard, name=resident_address_ward_code_or_name, code=resident_address_ward_code_or_name
        )

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

        dropdown_contact_address_province = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressProvince, name=contact_address_province_code_or_name,
            code=contact_address_province_code_or_name
        )

        contact_address_district_code_or_name = contact_address_info["contact_address_district_name"]

        dropdown_contact_address_district = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressDistrict, name=contact_address_district_code_or_name,
            code=contact_address_district_code_or_name
        )

        contact_address_ward_code_or_name = contact_address_info["contact_address_ward_name"]

        dropdown_contact_address_ward = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressWard, name=contact_address_ward_code_or_name, code=contact_address_ward_code_or_name
        )

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

        dropdown_branch = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=Branch, name=branch_name, code=branch_code
        )

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

            dropdown_martial_status = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=MaritalStatus, name=martial_status_code_or_name, code=martial_status_code_or_name
            )

            resident_status_code_or_name = customer_info['resident_status']

            dropdown_resident_status = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=ResidentStatus, name=resident_status_code_or_name, code=resident_status_code_or_name
            )

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

            dropdown_job = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=Career, name=job_name, code=job_code
            )

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

            dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerGender, name=gender_code_or_name, code=gender_code_or_name)

            nationality_code_or_name = co_owner_info["nationality_code"]

            dropdown_nationality = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressCountry, name=nationality_code_or_name, code=nationality_code_or_name
            )

            customer_type_code_or_name = co_owner_info['customer_type']

            dropdown_customer_type = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerType, name=customer_type_code_or_name, code=customer_type_code_or_name
            )

            customer_relationship_code_or_name = co_owner_info['coowner_relationship']

            dropdown_customer_relationship = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerRelationshipType, name=customer_relationship_code_or_name,
                code=customer_relationship_code_or_name
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

            dropdown_place_of_issue = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=PlaceOfIssue, name=place_of_issue_code_or_name, code=place_of_issue_code_or_name
            )
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

            date_of_birth = date_string_to_other_date_string_format(
                date_input=authorized_info['birthday'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )
            # thay đổi giới tính thành danh mục trong crm
            gender_code = authorized_info['gender']
            if gender_code == GW_GENDER_MALE:
                gender_code = CRM_GENDER_TYPE_MALE
            if gender_code == GW_GENDER_FEMALE:
                gender_code = CRM_GENDER_TYPE_FEMALE

            dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerGender, name=gender_code, code=gender_code
            )

            nationality_code = authorized_info['nationality_code']

            dropdown_nationality = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressCountry, name=nationality_code, code=nationality_code)

            cif_issued_date = cif_info['cif_issued_date']
            cif_issued_date = date_string_to_other_date_string_format(
                date_input=cif_issued_date,
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )
            id_issued_date = id_info['id_issued_date']
            id_issued_date = date_string_to_other_date_string_format(
                date_input=id_issued_date,
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )
            id_expired_date = id_info['id_expired_date']
            id_expired_date = date_string_to_other_date_string_format(
                date_input=id_expired_date,
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            )

            place_of_issue_code_or_name = id_info['id_issued_location']

            dropdown_place_of_issue = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=PlaceOfIssue, name=place_of_issue_code_or_name, code=place_of_issue_code_or_name
            )
            data_response.append(dict(
                full_name_vn=authorized_info['full_name'],
                date_of_birth=date_of_birth,
                gender=dropdown_gender,
                email=authorized_info['email'],
                mobile_phone=authorized_info['mobile_phone'],
                nationality=dropdown_nationality,
                customer_type=authorized_info['customer_type'],
                coowner_relationship=authorized_info['coowner_relationship'],
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
                    contact_address_full=address_info['contact_address_full'],
                    address_full=address_info['address_full']
                )
            ))

        response_data.update({
            "authorized_info_list": data_response,
            "total_items": len(data_response)
        })

        return self.response(data=response_data)

    async def ctr_gw_open_cif(self, cif_id: str):
        current_user = self.current_user
        response_customers = self.call_repos(await repos_get_customer_open_cif(
            cif_id=cif_id, session=self.oracle_session))
        first_row = response_customers[0]
        customer = first_row.Customer

        cust_identity = first_row.CustomerIdentity
        cust_individual = first_row.CustomerIndividualInfo
        cust_professional = first_row.CustomerProfessional

        cif_info = {
            "cif_auto": "Y" if customer.self_selected_cif_flag else "N",
            "cif_num": customer.cif_number if customer.self_selected_cif_flag else ""
        }
        # địa chỉ thường trú
        address_info_i = {
            "line": "",
            "ward_name": "",
            "district_name": "",
            "city_name": "",
            "country_name": "",
            "same_addr": ""
        }
        address_contact_info_i = {
            "contact_address_line": "",
            "contact_address_ward_name": "",
            "contact_address_district_name": "",
            "contact_address_city_name": "",
            "contact_address_country_name": ""
        }
        # địa chỉ đăng ký doanh nghiệp
        address_info_c = {
            "line": "",
            "ward_name": "",
            "district_name": "",
            "city_name": "",
            "country_name": "",
            "cor_same_addr ": ""
        }
        # địa chỉ liên lạc doanh nghiệp
        address_contact_info_c = {
            "contact_address_line": "",
            "contact_address_ward_name": "",
            "contact_address_district_name": "",
            "contact_address_city_name": "",
            "contact_address_country_name": ""
        }
        for row in response_customers:
            if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                address_info_i = {
                    "line": row.CustomerAddress.address,
                    "ward_name": row.AddressWard.name,
                    "district_name": row.AddressDistrict.name,
                    "city_name": row.AddressProvince.name,
                    "country_name": row.AddressCountry.name,
                    "same_addr": "Y"
                }
            else:
                address_contact_info_i = {
                    "contact_address_line": row.CustomerAddress.address,
                    "contact_address_ward_name": row.AddressWard.name,
                    "contact_address_district_name": row.AddressDistrict.name,
                    "contact_address_city_name": row.AddressProvince.name,
                    "contact_address_country_name": row.AddressCountry.name
                }

        customer_info = {
            "customer_category": customer.customer_category_id,
            "customer_type": customer.customer_type_id if customer.customer_type_id else "",
            "cus_ekyc": customer.kyc_level_id if customer.kyc_level_id else "",
            "full_name": customer.full_name_vn,
            "gender": EKYC_GENDER_TYPE_FEMALE if cust_individual.gender_id == CRM_GENDER_TYPE_FEMALE else EKYC_GENDER_TYPE_MALE,
            "telephone": customer.telephone_number if customer.telephone_number else "",
            "mobile_phone": customer.mobile_number if customer.mobile_number else "",
            "email": customer.email if customer.email else "",
            "place_of_birth": cust_individual.country_of_birth_id if cust_individual.country_of_birth_id else "",
            "birthday": cust_individual.date_of_birth if cust_individual.date_of_birth else "",
            "tax": customer.tax_number if customer.tax_number else "",
            "resident_status": cust_individual.resident_status_id if cust_individual.resident_status_id else "",
            "legal_guardian": "",
            "co_owner": "",
            "nationality": customer.nationality_id if customer.nationality_id else "",
            "birth_country": "",
            "language": "",
            "local_code": "101",
            "current_official": "",
            "biz_license_issue_date": "",
            "cor_capital": "",
            "cor_email": "",
            "cor_fax": "",
            "cor_tel": "",
            "cor_mobile": "",
            "cor_country": "",
            "cor_desc": "",
            "coowner_relationship": "",
            "martial_status": "M",
            "p_us_res_status": "N",
            "p_vst_us_prev": "N",
            "p_field9": "",
            "p_field10": "",
            "p_field11": "",
            "p_field12": "",
            "p_field13": "",
            "p_field14": "",
            "p_field15": "",
            "p_field16": "",
            "cif_info": cif_info,
            "id_info_main": {
                "id_num": cust_identity.identity_num,
                "id_issued_date": cust_identity.issued_date,
                "id_expired_date": cust_identity.expired_date,
                "id_issued_location": cust_identity.place_of_issue_id,
                "id_type": cust_identity.identity_type_id
            },
            "address_info_i": address_info_i,
            "address_contact_info_i": address_contact_info_i,
            "address_info_c": address_info_c,
            "address_contact_info_c": address_contact_info_c,
            "id_info_extra": {
                "id_num": "",
                "id_issued_date": "",
                "id_expired_date": "",
                "id_issued_location": "",
                "id_type": ""
            },
            "branch_info": {
                "branch_code": current_user.user_info.hrm_branch_code
            },
            "job_info": {
                "professional_code": cust_professional.career_id,
                "position": cust_professional.position_id if cust_professional.position_id else "",
                "official_telephone": cust_professional.company_phone if cust_professional.company_phone else "",
                "address_office_info": {
                    "address_full": cust_professional.company_address if cust_professional.company_address else ""
                }
            }
        }
        response_data = self.call_repos(await repos_gw_open_cif(cif_id=cif_id, current_user=current_user)) # noqa

        return self.response(data=customer_info)
