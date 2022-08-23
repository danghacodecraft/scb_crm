from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_check_mobile_num, repos_get_casa_account_number_open_cif,
    repos_get_cif_number_open_cif, repos_get_customer_avatar_url_from_cif,
    repos_get_customer_ids_from_cif_numbers, repos_get_customer_open_cif,
    repos_get_progress_open_cif, repos_gw_get_authorized,
    repos_gw_get_co_owner, repos_gw_get_customer_info_detail,
    repos_gw_get_customer_info_list, repos_push_casa_to_gw,
    repos_push_cif_to_gw, repos_push_debit_to_gw,
    repos_push_internet_banking_to_gw
)
from app.api.v1.endpoints.third_parties.gw.customer.schema import (
    CheckMobileNumRequest
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.settings.event import service_file
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerCategory, CustomerGender, CustomerRelationshipType, CustomerType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import (
    Branch, Career, MaritalStatus, ResidentStatus
)
from app.utils.constant.approval import CIF_STAGE_APPROVE_KSV
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.cif import CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT, GW_GENDER_FEMALE, GW_GENDER_MALE,
    GW_LOC_CHECK_CIF_EXIST, GW_REQUEST_PARAMETER_CO_OWNER,
    GW_REQUEST_PARAMETER_DEBIT_CARD, GW_REQUEST_PARAMETER_DEFAULT,
    GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP
)
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_KSV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_KSV
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_OPEN_CIF, ERROR_PERMISSION,
    ERROR_PHONE_NUMBER, ERROR_PHONE_NUMBER_NOT_EXITS,
    ERROR_VALIDATE_ONE_FIELD_REQUIRED
)
from app.utils.functions import (
    date_string_to_other_date_string_format, is_valid_mobile_number,
    orjson_dumps
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
        if {cif_number, identity_number, mobile_number, full_name} == {None}:
            return self.response_exception(
                msg=ERROR_VALIDATE_ONE_FIELD_REQUIRED,
                loc=f"cif_number: {cif_number}, identity_number: {identity_number}, mobile_number: {mobile_number}, "
                    f"full_name: {full_name}"
            )

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

    async def ctr_gw_get_customer_info_detail(
            self,
            cif_number: str,
            parameter: str = GW_REQUEST_PARAMETER_DEFAULT,
            return_raw_data_flag=False
    ):
        current_user = self.current_user
        customer_info_detail = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number, current_user=current_user))

        customer_info = customer_info_detail['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info']
        if return_raw_data_flag:
            return customer_info

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

        customer_category_code_or_name = customer_info['customer_category']
        dropdown_customer_category = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=CustomerCategory, code=customer_category_code_or_name, name=customer_category_code_or_name)

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
        identity_expired_date = date_string_to_other_date_string_format(
            date_input=identity_info['id_expired_date'],
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

        avatar_url = self.call_repos(await repos_get_customer_avatar_url_from_cif(
            cif_number=cif_number, session=self.oracle_session))

        avatar_url = await service_file.download_file(avatar_url)

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
                expired_date=identity_expired_date,
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
        elif parameter == GW_REQUEST_PARAMETER_CO_OWNER:
            customer_information = dict(
                id=cif_number,
                basic_information=dict(
                    cif_number=cif_number,
                    customer_relationship=None,  # TODO: Không tìm ra mối qh KH
                    full_name_vn=full_name_vn,
                    date_of_birth=date_of_birth,
                    gender=dropdown_gender,
                    nationality=dropdown_nationality,
                    mobile_number=mobile,
                    signature=None
                ),
                identity_document=dict(
                    identity_number=identity_info['id_num'],
                    issued_date=identity_issued_date,
                    expired_date=identity_expired_date,
                    place_of_issue=dropdown_place_of_issue
                ),
                address_information=dict(
                    resident_address=resident_address_full,
                    contact_address=contact_address_full
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

            career_name = job_info["professional_name"]
            career_code = job_info["professional_code"]

            dropdown_career = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=Career, name=career_name, code=career_code
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
                customer_category=dropdown_customer_category,
                resident_status=dropdown_resident_status,
                legal_representativeprsn_name=customer_info['legal_representativeprsn_name'],
                legal_representativeprsn_id=customer_info['legal_representativeprsn_id'],
                biz_contact_person_phone_num=customer_info['biz_contact_person_phone_num'],
                biz_line=customer_info['biz_line'],
                biz_license_issue_date=biz_license_issue_date,
                is_staff=customer_info['is_staff'],
                ekyc_level=customer_info['ekyc_level'],
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
                job_info=dict(
                    career=dropdown_career,
                    position=job_info['position'],
                    official_telephone=job_info['official_telephone'],
                    official_name=job_info['official_name'],
                    income_average=job_info['income_average'],
                    contact_address_full=job_info['address_info']['contact_address_full']
                ),
                branch_info=dropdown_branch,
                avatar_url=avatar_url['file_url'] if avatar_url else None
            ))
        customer_information.update(
            avatar_url=avatar_url['file_url'] if avatar_url else None
        )

        return self.response(data=customer_information)

    async def ctr_gw_check_exist_customer_detail_info(
            self,
            cif_number: str,
            return_raw_data_flag=False
    ):
        gw_check_exist_customer_detail_info = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number,
            current_user=self.current_user,
            loc=GW_LOC_CHECK_CIF_EXIST
        ))
        data_output = gw_check_exist_customer_detail_info['retrieveCustomerRefDataMgmt_out']['data_output']
        customer_info = data_output['customer_info']['id_info']
        if return_raw_data_flag:
            return True if customer_info['id_num'] else False

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

    async def ctr_gw_open_cif(self, cif_id: str, BOOKING_ID: str):

        casa_account_number = None
        cif_number = None

        # Check exist Booking
        booking = await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            booking_id=BOOKING_ID,
            cif_id=cif_id,
            loc=f"header -> booking-id, booking_id: {BOOKING_ID}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        is_role_supervisor = self.call_repos(await PermissionController.ctr_approval_check_permission_stage(
            auth_response=self.current_user,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_KSV,
            permission_code=IDM_PERMISSION_CODE_KSV,
            stage_code=CIF_STAGE_APPROVE_KSV
        ))
        if not is_role_supervisor:
            self.response_exception(
                loc=f"user: {self.current_user.user_info.code} - {self.current_user.user_info.username}",
                msg=ERROR_PERMISSION,
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        # Init response_info
        response_info = {
            "booking_id": BOOKING_ID,
            "cif_id": cif_id,
            "cif_num": {
                "status": False,
                "data": None
            },
            "account_num": {
                "status": False,
                "data": None
            },
            "ebank_num": {
                "status": False,
                "data": None
            },
            "debit_num": {
                "status": False,
                "data": None
            }
        }

        maker_staff_name = booking['data'].created_by
        if not maker_staff_name:
            return self.response_exception(
                loc="ctr_gw_open_cif",
                msg=ERROR_OPEN_CIF,
                detail="maker not found"
            )

        response_customers = self.call_repos(await repos_get_customer_open_cif(
            cif_id=cif_id, session=self.oracle_session))

        is_complete_cif, is_complete_casa, is_complete_eb, is_complete_debit = self.call_repos(
            await repos_get_progress_open_cif(booking_id=BOOKING_ID, session=self.oracle_session))

        # Push CIF (trả lỗi ngay)
        if not is_complete_cif:
            cif_number_result = await repos_push_cif_to_gw(
                booking_id=BOOKING_ID,
                session=self.oracle_session,
                response_customers=response_customers,
                current_user=self.current_user,
                cif_id=cif_id,
                maker_staff_name=maker_staff_name
            )

            if cif_number_result.is_error:
                self.response_exception(
                    loc=cif_number_result.loc,
                    msg=cif_number_result.msg,
                    detail=cif_number_result.detail,
                    data=response_info,
                )

            cif_number = cif_number_result.data
            is_complete_cif = True

        # Push CASA (trả lỗi ngay)
        if is_complete_cif and not is_complete_casa:
            if not cif_number:
                cif_number = self.call_repos(await repos_get_cif_number_open_cif(
                    cif_id=cif_id, session=self.oracle_session))

            casa_account_number_result = await repos_push_casa_to_gw(
                booking_id=BOOKING_ID,
                session=self.oracle_session,
                current_user=self.current_user,
                cif_id=cif_id,
                cif_number=cif_number,
                maker_staff_name=maker_staff_name
            )

            if casa_account_number_result.is_error:
                if casa_account_number_result.msg == ERROR_CALL_SERVICE_GW:
                    response_info["cif_num"]["status"] = True
                    response_info["cif_num"]["data"] = cif_number
                    self.response_exception(
                        loc=casa_account_number_result.loc,
                        msg=casa_account_number_result.msg,
                        detail=casa_account_number_result.detail,
                        data=response_info,
                    )
                else:
                    self.call_repos(result_call_repos=casa_account_number_result)

            casa_account_number = casa_account_number_result.data
            is_complete_casa = True

        # Push EB, SMS, Debit (Trả lỗi sau)
        # RULE: Phải hoàn thành CIF với CASA trước
        error_list = []
        if is_complete_cif and is_complete_casa:

            if not casa_account_number:
                casa_account_number = self.call_repos(await repos_get_casa_account_number_open_cif(
                    cif_id=cif_id, session=self.oracle_session))

            if not cif_number:
                cif_number = self.call_repos(await repos_get_cif_number_open_cif(
                    cif_id=cif_id, session=self.oracle_session))

            # Push EB
            if not is_complete_eb:
                result = await repos_push_internet_banking_to_gw(
                    booking_id=BOOKING_ID,
                    session=self.oracle_session,
                    response_customers=response_customers,
                    current_user=self.current_user,
                    cif_id=cif_id,
                    cif_number=cif_number,
                    casa_account_number=casa_account_number,
                    maker_staff_name=maker_staff_name
                )
                if result.is_error:
                    error_list.append({
                        "e_banking": {
                            "loc": result.loc,
                            "msg": result.msg,
                            "detail": result.detail
                        }
                    })
                else:
                    is_complete_eb = True

            # Push Debit
            if not is_complete_debit:
                result = await repos_push_debit_to_gw(
                    booking_id=BOOKING_ID,
                    session=self.oracle_session,
                    current_user=self.current_user,
                    cif_id=cif_id,
                    cif_number=cif_number,
                    casa_account_number=casa_account_number,
                    response_customers=response_customers,
                    maker_staff_name=maker_staff_name
                )
                if result.is_error:
                    error_list.append({
                        "debit_card": {
                            "loc": result.loc,
                            "msg": result.msg,
                            "detail": result.detail
                        }
                    })
                else:
                    is_complete_debit = True

        if not casa_account_number:
            casa_account_number = self.call_repos(await repos_get_casa_account_number_open_cif(
                cif_id=cif_id, session=self.oracle_session))

        if not cif_number:
            cif_number = self.call_repos(await repos_get_cif_number_open_cif(
                cif_id=cif_id, session=self.oracle_session))

        response_info["cif_num"]["status"] = True
        response_info["cif_num"]["data"] = cif_number
        response_info["account_num"]["status"] = True
        response_info["account_num"]["data"] = casa_account_number
        if is_complete_eb:
            response_info["ebank_num"]["status"] = True
        if is_complete_debit:
            response_info["debit_num"]["status"] = True

        if error_list:
            return self.response_exception(
                data=response_info,
                loc="ctr_gw_open_cif",
                msg=ERROR_OPEN_CIF,
                detail=orjson_dumps(error_list)
            )

        return self.response(data=response_info)

    async def ctr_check_mobile_num(self, request: CheckMobileNumRequest):

        if not is_valid_mobile_number(mobile_number=request.mobile_number):
            return self.response_exception(loc='mobile_number', msg=ERROR_PHONE_NUMBER)

        mobile_info = self.call_repos(
            await repos_check_mobile_num(
                mobile_num=request.mobile_number,
                session=self.oracle_session
            ))

        if not mobile_info:
            return self.response(data=dict(
                mobile_number=False,
                message=ERROR_PHONE_NUMBER_NOT_EXITS
            ))

        return self.response(data=True)
