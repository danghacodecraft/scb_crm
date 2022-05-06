from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.repository import (
    repos_customer_information, repos_get_cif_info,
    repos_get_initializing_customer, repos_get_total_participants,
    repos_profile_history, repos_validate_cif_number
)
from app.api.v1.endpoints.cif.schema import CustomerByCIFNumberRequest
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_gw_get_customer_info_detail
)
from app.api.v1.endpoints.user.contact.repository import repo_contact
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.utils.constant.cif import DROPDOWN_NONE_DICT, PROFILE_HISTORY_STATUS
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT, GW_LOC_CHECK_CIF_EXIST
)
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown, dropdownflag,
    orjson_loads, string_to_date
)
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, split_name
)


class CtrCustomer(BaseController):
    async def ctr_cif_info(self, cif_id: str):
        cif_info = self.call_repos(
            await repos_get_cif_info(
                cif_id=cif_id,
                session=self.oracle_session
            ))
        return self.response(cif_info)

    async def ctr_profile_history(self, cif_id: str):
        profile_histories = self.call_repos((await repos_profile_history(cif_id=cif_id, session=self.oracle_session)))
        full_logs = []
        for _, _, booking_business_form in profile_histories:
            log_data = orjson_loads(booking_business_form.log_data)
            if log_data:
                full_logs.extend(log_data)
        full_logs = sorted(full_logs, key=lambda d: d['created_at'], reverse=True)
        prev_created_at = None
        log_details = []
        response_datas = {}
        for full_log in full_logs:
            created_at = string_to_date(full_log['created_at'], _format=DATETIME_INPUT_OUTPUT_FORMAT)
            log_data = dict(
                description=full_log['description'],
                completed_at=full_log['completed_at'],
                started_at=full_log['created_at'],
                status=PROFILE_HISTORY_STATUS[full_log['status']],
                branch_id=full_log['branch_id'],
                branch_code=full_log['branch_code'],
                branch_name=full_log['branch_name'],
                user_id=full_log['user_id'],
                user_name=full_log['user_name'],
                position_id=full_log['position_id'],
                position_code=full_log['position_code'],
                position_name=full_log['position_name']
            )
            if not prev_created_at:
                prev_created_at = created_at
            if prev_created_at != created_at:
                log_details = []

            log_details.append(log_data)

            response_datas.update({created_at: log_details})

        return self.response(data=[dict(
            created_at=created_at,
            log_details=log_details
        ) for created_at, log_details in response_datas.items()])

    async def ctr_customer_information(self, cif_id: str):
        customer_information = self.call_repos(
            await repos_customer_information(cif_id=cif_id, session=self.oracle_session))
        first_row = customer_information[0]

        employees = self.call_repos(
            await repos_get_total_participants(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        list_distinct_employee = []
        for (
                user_id, user_fullname, user_name, user_email, position_id, position_code, position_name, department_id,
                department_code, department_name, branch_id, branch_code, branch_name, _
        ) in employees:
            hrm_user_data = self.call_repos(await repo_contact(
                code=user_id,
                session=self.oracle_session_task
            ))

            list_distinct_employee.append(dict(
                id=user_id,
                full_name_vn=user_fullname,
                avatar_url=hrm_user_data[-1],  # TODO: Tạm thời lấy từ HRM - User Contact
                user_name=user_name,
                email=user_email,
                position=dict(
                    id=position_id,
                    code=position_code,
                    name=position_name
                ),
                department=dict(
                    id=department_id,
                    code=department_code,
                    name=department_name
                ),
                branch=dict(
                    id=branch_id,
                    code=branch_code,
                    name=branch_name
                )
            ))
        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=[first_row.Customer.avatar_url])
        data_response = {
            "customer_id": first_row.Customer.id,
            "status": dropdownflag(first_row.CustomerStatus),
            "cif_number": first_row.Customer.cif_number if first_row.CustomerType else None,
            "avatar_url": uuid__link_downloads[first_row.Customer.avatar_url],
            "customer_classification": dropdown(first_row.CustomerClassification),
            "full_name": first_row.Customer.full_name,
            "gender": dropdown(first_row.CustomerGender),
            "email": first_row.Customer.email,
            "mobile_number": first_row.Customer.mobile_number,
            "identity_number": first_row.CustomerIdentity.identity_num,
            "place_of_issue": dropdown(first_row.PlaceOfIssue),
            "issued_date": first_row.CustomerIdentity.issued_date,
            "expired_date": first_row.CustomerIdentity.expired_date,
            "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
            "nationality": dropdown(first_row.AddressCountry),
            "marital_status": dropdown(first_row.MaritalStatus) if first_row.MaritalStatus else DROPDOWN_NONE_DICT,
            "customer_type": dropdown(first_row.CustomerType) if first_row.CustomerType else DROPDOWN_NONE_DICT,
            "credit_rating": None,
            "address": first_row.CustomerAddress.address,
            "total_employees": len(list_distinct_employee),
            "employees": list_distinct_employee
        }

        return self.response(data=data_response)

    async def ctr_check_exist_cif(self, cif_number: str):
        # validate cif_number
        self.call_repos(await repos_validate_cif_number(cif_number=cif_number))

        # check_exist_info = self.call_repos(
        #     await repos_check_exist_cif(cif_number=cif_number)
        # )
        # return self.response(data=check_exist_info)
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

    async def ctr_retrieve_customer_information_by_cif_number(
            self,
            cif_id: str,
            request: CustomerByCIFNumberRequest
    ):
        cif_number = request.cif_number

        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # check cif number is valid
        self.call_repos(await repos_validate_cif_number(cif_number=cif_number))

        gw_check_exist_customer_detail_info = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number,
            current_user=self.current_user,
            loc=GW_LOC_CHECK_CIF_EXIST
        ))
        data_output = gw_check_exist_customer_detail_info['retrieveCustomerRefDataMgmt_out']['data_output']
        customer_info = data_output['customer_info']
        cif_info = customer_info['cif_info']

        customer_type = customer_info['customer_type']
        cif_information = dict(
            cif_number=cif_number,
            issued_date=date_string_to_other_date_string_format(
                date_input=cif_info['cif_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            ),
            customer_type=customer_type
        )

        full_name_vn = customer_info['full_name']
        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        # Tách Họ, Tên và Ten đệm
        last_name, middle_name, first_name = split_name(full_name_vn)

        customer_information = dict(
            full_name=full_name,
            full_name_vn=full_name_vn,
            last_name=last_name,
            middle_name=middle_name,
            first_name=first_name,
            date_of_birth=date_string_to_other_date_string_format(
                date_input=customer_info['birthday'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            ),
            gender=customer_info['gender'],
            nationality=customer_info['nationality_code'],
            mobile=customer_info['mobile_phone'],
            telephone=customer_info['telephone'],
            email=customer_info['email']
        )

        identity_info = customer_info['id_info']
        identity_number = identity_info['id_num']
        identity_issued_date = date_string_to_other_date_string_format(
            date_input=identity_info['id_issued_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )
        identity_place_of_issue = identity_info['id_issued_location']
        identity_information = dict(
            identity_number=identity_number,
            issued_date=identity_issued_date,
            place_of_issue=identity_place_of_issue
        )
        #
        # customer_address = customer_info['address_info']
        # if flat_address:
        #     resident_address_response = dict(number_and_street=customer_address["address_full"])
        #     contact_address_response = dict(number_and_street=customer_address["contact_address_full"])
        # else:
        #     _, resident_address = matching_place_residence(customer_address["address_full"])
        #
        #     resident_address_province = resident_address["province_code"]
        #     if resident_address_province != '':
        #         resident_address_province_code = 'NAM' if gender == 'M' else 'NU'
        #         resident_address_province = await self.get_model_object_by_id(model_id=resident_address_province_code, model=AddressProvince, loc="resident_address_province_code")
        #         resident_address_province = dropdown(resident_address_province)
        #     resident_address_district = resident_address["district_code"]
        #     resident_address_ward = resident_address["ward_code"]
        #     resident_address_number_and_street = resident_address["street_name"]
        #     resident_address_response = dict(
        #         province=resident_address_province,
        #         district=resident_address_district,
        #         ward=resident_address_ward,
        #         number_and_street=resident_address_number_and_street
        #     )
        #
        #     _, contact_address = matching_place_residence(customer_address["contact_address_full"])
        #     contact_address_province = contact_address["province_code"]
        #     contact_address_district = contact_address["district_code"]
        #     contact_address_ward = contact_address["ward_code"]
        #     contact_address_number_and_street = contact_address["street_name"]
        #     contact_address_response = dict(
        #         province=contact_address_province,
        #         district=contact_address_district,
        #         ward=contact_address_ward,
        #         number_and_street=contact_address_number_and_street
        #     )

        customer_information = {
            "cif_information": cif_information,
            "customer_information": customer_information,
            # "career_information": career_information,
            "identity_information": identity_information,
            # "address_info": dict(
            #     resident_address=resident_address_response,
            #     contact_address=contact_address_response
            # )
        }
        return self.response(data=customer_information)

        # customer_information = self.call_repos(await repos_retrieve_customer_information_by_cif_number(
        #     cif_number=cif_number
        # ))
        #
        # if "is_existed" in customer_information:
        #     return self.response_exception(
        #         msg=ERROR_CIF_ID_NOT_EXIST,
        #         detail="Cif number is not exisst",
        #         loc=f"cif_number : {cif_number}"
        #     )
        #
        # cif_info = customer_information["retrieveCustomerRefDataMgmt_out"]["CIFInfo"]
        # customer_info = customer_information["retrieveCustomerRefDataMgmt_out"]["customerInfo"]
        # customer_address = customer_info["address"]
        # customer_identity = customer_info["IDInfo"]
        # email = customer_address["email"]
        # mobileNum = customer_address["mobileNum"]
        # telephoneNum = customer_address["telephoneNum"]
        # phoneNum = customer_address["phoneNum"]
        # faxNum = customer_address["faxNum"]
        #
        # if flat_address:
        #     resident_address_response = customer_address["address_vn"]
        #     contact_address_response = customer_address["address1"]
        # else:
        #     _, resident_address = matching_place_residence(customer_address["address_vn"])
        #     resident_address_response = {
        #         "province": resident_address["province_code"],
        #         "district": resident_address["district_code"],
        #         "ward": resident_address["ward_code"],
        #         "number_and_street": resident_address["street_name"]
        #     }
        #
        #     _, contact_address = matching_place_residence(customer_address["address1"])
        #     contact_address_response = {
        #         "province": contact_address["province_code"],
        #         "district": contact_address["district_code"],
        #         "ward": contact_address["ward_code"],
        #         "number_and_street": contact_address["street_name"]
        #     }
        #
        # # Tách Họ, Tên và Ten đệm
        # last_name, middle_name, first_name = split_name(customer_info['fullname_vn'])
        #
        # cif_number = cif_info['CIFNum']
        # issued_date = cif_info['CIFIssuedDate']
        # branch_code = cif_info['branchCode']
        # customer_type = cif_info['customerType']
        #
        # full_name = customer_info['fullname']
        # full_name_vn = customer_info['fullname_vn']
        # date_of_birth = customer_info['birthDay']
        # customer_vip_type = customer_info['customerVIPType']
        # manage_staff_id = customer_info['manageStaffID']
        # director_name = customer_info['directorName']
        # nationality_code = customer_info['nationlityCode']
        # nationality = customer_info['nationlity']
        # is_staff = customer_info['isStaff']
        # segment_type = customer_info['segmentType']
        #
        # identity_number = customer_identity['IDNum']
        # identity_issued_date = customer_identity['IDIssuedDate']
        # identity_place_of_issue = customer_identity['IDIssuedLocation']
        #
        # gender_id = CRM_GENDER_TYPE_MALE if customer_info['gender'] == SOA_GENDER_TYPE_MALE else CRM_GENDER_TYPE_FEMALE
        # gender = await self.get_model_object_by_id(
        #     model_id=gender_id,
        #     model=CustomerGender,
        #     loc=f"gender_id: {gender_id}"
        # )
        #
        # resident_provice = None
        # resident_district = None
        # resident_ward = None
        # contact_provice = None
        # contact_district = None
        # contact_ward = None
        #
        # if not flat_address:
        #     # Get thông tin đia chỉ thường trú
        #     ward_id = resident_address_response["ward"]
        #     if ward_id:
        #         resident_ward = await self.get_model_object_by_id(
        #             model_id=ward_id,
        #             model=AddressWard,
        #             loc=f"ward_id: {ward_id}")
        #     district_id = resident_address_response["district"]
        #     if district_id:
        #         resident_district = await self.get_model_object_by_id(
        #             model_id=district_id,
        #             model=AddressDistrict,
        #             loc=f"district_id: {district_id}")
        #
        #     province_id = resident_address_response["province"]
        #     if province_id:
        #         resident_provice = await self.get_model_object_by_id(
        #             model_id=province_id,
        #             model=AddressProvince,
        #             loc=f"provice_id: {province_id}")
        #
        #     # Get thông tin đia chỉ tạm trú
        #     contact_ward_id = contact_address_response["ward"]
        #     if contact_ward_id:
        #         contact_ward = await self.get_model_object_by_id(
        #             model_id=contact_ward_id,
        #             model=AddressWard,
        #             loc=f"ward_id: {contact_ward_id}")
        #     contact_district_id = contact_address_response["district"]
        #     if contact_district_id:
        #         contact_district = await self.get_model_object_by_id(
        #             model_id=contact_district_id,
        #             model=AddressDistrict,
        #             loc=f"district_id: {contact_district_id}")
        #
        #     contact_province_id = contact_address_response["province"]
        #     if contact_province_id:
        #         contact_provice = await self.get_model_object_by_id(
        #             model_id=contact_province_id,
        #             model=AddressProvince,
        #             loc=f"provice_id: {contact_province_id}")
        #
        # customer_information.update({
        #     "cif_information": {
        #         "cif_number": cif_number if cif_number else None,
        #         "issued_date": issued_date if issued_date else None,
        #         "branch_code": branch_code if branch_code else None,
        #         "customer_type": customer_type if customer_type else None,
        #     },
        #     "customer_information": {
        #         "full_name": full_name if full_name else None,
        #         "full_name_vn": full_name_vn if full_name_vn else None,
        #         "last_name": last_name if last_name else None,
        #         "middle_name": middle_name if middle_name else None,
        #         "first_name": first_name if first_name else None,
        #         "date_of_birth": date_of_birth if date_of_birth else None,
        #         "gender": dropdown(gender) if not gender else DROPDOWN_NONE_DICT,
        #         "customer_vip_type": customer_vip_type if customer_vip_type else None,
        #         "manage_staff_id": manage_staff_id if manage_staff_id else None,
        #         "director_name": director_name if director_name else None,
        #         "nationality_code": nationality_code if nationality_code else None,
        #         "nationality": nationality if nationality else None,
        #         "is_staff": is_staff if is_staff else None,
        #         "segment_type": segment_type if segment_type else None,
        #     },
        #     # "career_information": career_information,
        #     "identity_information": {
        #         "identity_number": identity_number if identity_number else None,
        #         "issued_date": date_string_to_other_date_string_format(
        #             identity_issued_date,
        #             from_format=SOA_DATETIME_FORMAT
        #         ) if identity_issued_date else None,
        #         "place_of_issue": identity_place_of_issue if identity_place_of_issue else None,
        #     },
        #     "address_info": {
        #         "resident_address": {
        #             "province": dropdown(
        #                 resident_provice) if not flat_address and resident_provice else DROPDOWN_NONE_DICT,
        #             "district": dropdown(
        #                 resident_district) if not flat_address and resident_district else DROPDOWN_NONE_DICT,
        #             "ward": dropdown(resident_ward) if not flat_address and resident_ward else DROPDOWN_NONE_DICT,
        #             "name": resident_address_response if flat_address else None
        #         },
        #         "contact_address": {
        #             "province": dropdown(
        #                 contact_provice) if not flat_address and contact_provice else DROPDOWN_NONE_DICT,
        #             "district": dropdown(
        #                 contact_district) if not flat_address and contact_district else DROPDOWN_NONE_DICT,
        #             "ward": dropdown(contact_ward) if not flat_address and contact_ward else DROPDOWN_NONE_DICT,
        #             "name": contact_address_response if flat_address else None
        #         },
        #         "email": email,
        #         "mobileNum": mobileNum,
        #         "telephoneNum": telephoneNum,
        #         "phoneNum": phoneNum,
        #         "faxNum": faxNum,
        #     }
        # })
        #
        # return self.response(data=customer_information)
