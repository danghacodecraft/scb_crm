from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import repos_get_approval_process
from app.api.v1.endpoints.cif.repository import (
    repos_customer_information, repos_get_cif_id_by_cif_number,
    repos_get_cif_info, repos_get_customer_working_infos,
    repos_profile_history, repos_validate_cif_number
)
from app.api.v1.endpoints.cif.schema import CustomerByCIFNumberRequest
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name
)
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_gw_get_customer_info_detail
)
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_employee_info_from_code
)
from app.settings.config import DATETIME_INPUT_OUTPUT_FORMAT
from app.third_parties.oracle.models.master_data.address import (
    AddressDistrict, AddressProvince
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.services.file import ServiceFile
from app.third_parties.services.idm import ServiceIDM
from app.utils.constant.cif import DROPDOWN_NONE_DICT, PROFILE_HISTORY_STATUS
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT,
    GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT, GW_LOC_CHECK_CIF_EXIST
)
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown, dropdown_name,
    dropdownflag, orjson_loads, string_to_date
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

    async def ctr_customer_information(self, cif_id: str, booking_id):
        customer_information = self.call_repos(
            await repos_customer_information(cif_id=cif_id, session=self.oracle_session))
        first_row = customer_information[0]

        # employees = self.call_repos(
        #     await repos_get_total_participants(
        #         cif_id=cif_id,
        #         session=self.oracle_session
        #     )
        # )

        transactions = self.call_repos((await repos_get_approval_process(booking_id=booking_id, session=self.oracle_session)))

        list_distinct_employee = []
        list_distinct_user_code = []
        for _, _, _, transaction_sender, transaction_root_daily in transactions:
            employee_info = self.call_repos(await repos_gw_get_employee_info_from_code(
                employee_code=transaction_sender.user_id, current_user=self.current_user))
            avatar = ServiceIDM().replace_with_cdn(employee_info[GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT]['data_output']['employee_info']['avatar'])

            if transaction_sender.user_id not in list_distinct_user_code:
                list_distinct_employee.append(dict(
                    id=transaction_sender.user_id,
                    full_name_vn=transaction_sender.user_fullname,
                    avatar_url=avatar,
                    user_name=transaction_sender.user_name,
                    email=transaction_sender.user_email,
                    position=dict(
                        id=transaction_sender.position_id,
                        code=transaction_sender.position_code,
                        name=transaction_sender.position_name
                    ),
                    department=dict(
                        id=transaction_sender.department_id,
                        code=transaction_sender.department_code,
                        name=transaction_sender.department_name
                    ),
                    branch=dict(
                        id=transaction_sender.branch_id,
                        code=transaction_sender.branch_code,
                        name=transaction_sender.branch_name
                    ),
                    title=dict(
                        id=transaction_sender.title_id,
                        code=transaction_sender.title_code,
                        name=transaction_sender.title_name
                    )
                ))
                list_distinct_user_code.append(transaction_sender.user_id)

        # list_employee = []
        # for employee in employees:
        #     employee = orjson_loads(employee)
        #     list_employee.extend(employee)
        #
        # list_distinct_user_id = []
        # for employee in list_employee:
        #     user_id = employee['user_id']
        #     if user_id in list_distinct_user_id:
        #         continue
        #
        #     list_distinct_user_id.append(user_id)
        #     user_fullname = employee['user_name']
        #     user_name = employee['user_username']
        #     user_email = employee['user_email']
        #     user_avatar = employee['user_avatar']
        #     position_id = employee['position_id']
        #     position_code = employee['position_code']
        #     position_name = employee['position_name']
        #     department_id = employee['department_id']
        #     department_code = employee['department_code']
        #     department_name = employee['department_name']
        #     branch_id = employee['branch_id']
        #     branch_code = employee['branch_code']
        #     branch_name = employee['branch_name']
        #     title_id = employee['title_id']
        #     title_code = employee['title_code']
        #     title_name = employee['title_name']
        #
        #     hrm_user_data = self.call_repos(await repo_contact(
        #         code=employee['user_id'],
        #         session=self.oracle_session_task
        #     ))
        #
        #     list_distinct_employee.append(dict(
        #         id=user_id,
        #         full_name_vn=user_fullname,
        #         avatar_url=hrm_user_data[-1],  # TODO: Tạm thời lấy từ HRM - User Contact
        #         user_name=user_name,
        #         email=user_email,
        #         avatar=user_avatar,
        #         position=dict(
        #             id=position_id,
        #             code=position_code,
        #             name=position_name
        #         ),
        #         department=dict(
        #             id=department_id,
        #             code=department_code,
        #             name=department_name
        #         ),
        #         branch=dict(
        #             id=branch_id,
        #             code=branch_code,
        #             name=branch_name
        #         ),
        #         title=dict(
        #             id=title_id,
        #             code=title_code,
        #             name=title_name
        #         )
        #     ))

        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=[first_row.Customer.avatar_url])
        data_response = {
            "customer_id": first_row.Customer.id,
            "completed_flag": first_row.Customer.complete_flag,
            "status": dropdownflag(first_row.CustomerStatus),
            "cif_number": first_row.Customer.cif_number,
            "avatar_url": ServiceFile().replace_with_cdn(uuid__link_downloads[first_row.Customer.avatar_url]),
            "customer_classification": dropdown(first_row.CustomerClassification),
            "full_name": first_row.Customer.full_name,
            "full_name_vn": first_row.Customer.full_name_vn,
            "gender": dropdown(first_row.CustomerGender),
            "email": first_row.Customer.email,
            "mobile_number": first_row.Customer.mobile_number,
            "resident_status": dropdown(first_row.ResidentStatus),
            "identity_number": first_row.CustomerIdentity.identity_num,
            "place_of_issue": dropdown(first_row.PlaceOfIssue),
            "issued_date": first_row.CustomerIdentity.issued_date,
            "expired_date": first_row.CustomerIdentity.expired_date,
            "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
            "nationality": dropdown(first_row.AddressCountry),
            "marital_status": dropdown(first_row.MaritalStatus) if first_row.MaritalStatus else DROPDOWN_NONE_DICT,
            "customer_type": dropdown(first_row.CustomerType) if first_row.CustomerType else DROPDOWN_NONE_DICT,
            "customer_category": dropdown(first_row.CustomerCategory) if first_row.CustomerCategory else DROPDOWN_NONE_DICT,
            "credit_rating": None,
            "address": first_row.CustomerAddress.address,
            "total_employees": len(list_distinct_employee),
            "employees": list_distinct_employee
        }

        return self.response(data=data_response)

    async def ctr_check_exist_cif(self, cif_number: str):
        # validate cif_number
        self.call_repos(await repos_validate_cif_number(cif_number=cif_number))

        cif_id = self.call_repos(await repos_get_cif_id_by_cif_number(
            cif_number=cif_number, session=self.oracle_session
        ))

        gw_check_exist_customer_detail_info = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number,
            current_user=self.current_user,
            loc=GW_LOC_CHECK_CIF_EXIST
        ))
        data_output = gw_check_exist_customer_detail_info['retrieveCustomerRefDataMgmt_out']['data_output']
        customer_info = data_output['customer_info']['id_info']

        return self.response(data=dict(
            is_existed=True if customer_info['id_num'] else False,
            cif_id=cif_id
        ))

    async def ctr_retrieve_customer_information_by_cif_number(
            self,
            request: CustomerByCIFNumberRequest
    ):
        cif_number = request.cif_number

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

        customer_type_code = customer_info['customer_type']
        customer_type = await get_optional_model_object_by_code_or_name(
            model=CustomerType,
            model_code=customer_type_code,
            model_name=None,
            session=self.oracle_session
        )
        dropdown_customer_type = dropdown(customer_type) if customer_type else dropdown_name(customer_type_code)

        cif_information = dict(
            cif_number=cif_number,
            issued_date=date_string_to_other_date_string_format(
                date_input=cif_info['cif_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            ),
            customer_type=dropdown_customer_type
        )

        full_name_vn = customer_info['full_name']
        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        # Tách Họ, Tên và Ten đệm
        last_name, middle_name, first_name = split_name(full_name_vn)

        gender_code = customer_info["gender"]
        gender = await get_optional_model_object_by_code_or_name(
            model=CustomerGender,
            model_code=gender_code,
            model_name=None,
            session=self.oracle_session
        )
        dropdown_gender = dropdown(gender) if gender else dropdown_name(gender_code)

        nationality_code = customer_info["nationality_code"]
        nationality = await get_optional_model_object_by_code_or_name(
            model=CustomerGender,
            model_code=nationality_code,
            model_name=None,
            session=self.oracle_session
        )
        dropdown_nationality = dropdown(nationality) if nationality else dropdown_name(nationality_code)

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
            gender=dropdown_gender,
            nationality=dropdown_nationality,
            mobile=customer_info['mobile_phone'],
            telephone=customer_info['telephone'],
            email=customer_info['email']
        )

        identity_info = customer_info['id_info']
        place_of_issue_code = identity_info["id_issued_location"]
        place_of_issue = await get_optional_model_object_by_code_or_name(
            model=PlaceOfIssue,
            model_id=place_of_issue_code,
            model_code=None,
            model_name=None,
            session=self.oracle_session
        )
        dropdown_place_of_issue = dropdown(place_of_issue) if place_of_issue else dropdown_name(place_of_issue_code)

        identity_information = dict(
            identity_number=identity_info['id_num'],
            issued_date=date_string_to_other_date_string_format(
                date_input=identity_info['id_issued_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            ),
            expired_date=date_string_to_other_date_string_format(
                date_input=identity_info['id_expired_date'],
                from_format=GW_DATETIME_FORMAT,
                to_format=GW_DATE_FORMAT
            ),
            place_of_issue=dropdown_place_of_issue
        )

        resident_address_info = customer_info['p_address_info']

        resident_address_province_name = resident_address_info["city_name"]
        resident_address_province = await get_optional_model_object_by_code_or_name(
            model=AddressProvince,
            model_code=None,
            model_name=resident_address_province_name,
            session=self.oracle_session
        )
        dropdown_resident_address_province = dropdown(
            resident_address_province) if resident_address_province else dropdown_name(resident_address_province_name)

        resident_address_district_name = resident_address_info["district_name"]
        resident_address_district = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=None,
            model_name=resident_address_district_name,
            session=self.oracle_session
        )
        dropdown_resident_address_district = dropdown(
            resident_address_province) if resident_address_district else dropdown_name(resident_address_district_name)

        resident_address_ward_name = resident_address_info["ward_name"]
        resident_address_ward = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=None,
            model_name=resident_address_ward_name,
            session=self.oracle_session
        )
        dropdown_resident_address_ward = dropdown(
            resident_address_ward) if resident_address_ward else dropdown_name(resident_address_ward_name)

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

        contact_address_province_name = contact_address_info["contact_address_city_name"]
        contact_address_province = await get_optional_model_object_by_code_or_name(
            model=AddressProvince,
            model_code=None,
            model_name=contact_address_province_name,
            session=self.oracle_session
        )
        dropdown_contact_address_province = dropdown(
            contact_address_province) if contact_address_province else dropdown_name(contact_address_province_name)

        contact_address_district_name = contact_address_info["contact_address_district_name"]
        contact_address_district = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=None,
            model_name=contact_address_district_name,
            session=self.oracle_session
        )
        dropdown_contact_address_district = dropdown(
            contact_address_province) if contact_address_district else dropdown_name(contact_address_district_name)

        contact_address_ward_name = contact_address_info["contact_address_ward_name"]
        contact_address_ward = await get_optional_model_object_by_code_or_name(
            model=AddressDistrict,
            model_code=None,
            model_name=contact_address_ward_name,
            session=self.oracle_session
        )
        dropdown_contact_address_ward = dropdown(
            contact_address_ward) if contact_address_ward else dropdown_name(contact_address_ward_name)

        contact_address_number_and_street = contact_address_info["contact_address_line"]

        contact_address_full = contact_address_info["contact_address_full"]

        contact_address_response = dict(
            province=dropdown_contact_address_province,
            district=dropdown_contact_address_district,
            ward=dropdown_contact_address_ward,
            number_and_street=contact_address_number_and_street,
            address_full=contact_address_full
        )

        customer_information = {
            "cif_information": cif_information,
            "customer_information": customer_information,
            # "career_information": career_information,
            "identity_information": identity_information,
            "address_info": dict(
                resident_address=resident_address_response,
                contact_address=contact_address_response
            )
        }
        return self.response(data=customer_information)

    async def ctr_retrieve_customer_working_info_by_cif_number(self, cif_id_or_number):
        working_infos = self.call_repos(await repos_get_customer_working_infos(
            cif_id_or_number=cif_id_or_number, session=self.oracle_session
        ))

        response_data = dict(
            career=DROPDOWN_NONE_DICT,
            average_income_amount=DROPDOWN_NONE_DICT,
            company_position=DROPDOWN_NONE_DICT
        )

        if working_infos:
            customer, customer_professional, career, average_income_amount, position = working_infos

            if customer_professional:
                response_data.update(
                    company_name=customer_professional.company_name,
                    company_phone=customer_professional.company_phone,
                    company_address=customer_professional.company_address
                )
            if career:
                response_data.update(
                    average_income_amount=dropdown(average_income_amount),
                    career=dropdown(career) if career else None,
                    company_position=dropdown(position) if position else DROPDOWN_NONE_DICT
                )

        return self.response(data=response_data)
