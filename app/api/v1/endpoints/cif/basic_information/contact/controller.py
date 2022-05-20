from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.contact.repository import (
    repos_get_customer_professional_and_identity_and_address,
    repos_get_detail_contact_info, repos_save_contact_information
)
from app.api.v1.endpoints.cif.basic_information.contact.schema import (
    ContactInformationSaveRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking, repos_get_customer_identity,
    repos_get_initializing_customer
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Career, Position
)
from app.utils.constant.cif import (
    ADDRESS_COUNTRY_CODE_VN, CONTACT_ADDRESS_CODE,
    CUSTOMER_ADDRESS_DOMESTIC_FLAG, CUSTOMER_ADDRESS_SAME_PERMANENT_FLAG,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, RESIDENT_ADDRESS_CODE
)
from app.utils.functions import dropdown, generate_uuid


class CtrContactInformation(BaseController):
    async def detail_contact_information(self, cif_id: str):
        # lấy customer_identity
        customer_identity = self.call_repos(await repos_get_customer_identity(
            cif_id=cif_id,
            session=self.oracle_session
        ))
        # tạo flag
        resident_address_active_flag = False
        contact_address_active_flag = False
        # check nếu giấy tờ định danh là passport
        if customer_identity.identity_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            resident_address_active_flag = True
            contact_address_active_flag = True
        # lấy dữ liệu thông tin liên lạc
        contact_information_detail_data = self.call_repos(
            await repos_get_detail_contact_info(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        resident_address = None
        contact_address = None
        career_information = None

        for row in contact_information_detail_data:
            if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                if row.CustomerAddress.address_domestic_flag == CUSTOMER_ADDRESS_DOMESTIC_FLAG:
                    resident_address = {
                        "domestic_flag": row.CustomerAddress.address_domestic_flag,
                        "domestic_address": {
                            "country": dropdown(row.AddressCountry),
                            'province': dropdown(row.AddressProvince),
                            'district': dropdown(row.AddressDistrict),
                            "ward": dropdown(row.AddressWard),
                            'number_and_street': row.CustomerAddress.address
                        },
                        "foreign_address": None
                    }
                else:
                    resident_address = {
                        "domestic_flag": row.CustomerAddress.address_domestic_flag,
                        "domestic_address": None,
                        "foreign_address": {
                            "country": dropdown(row.AddressCountry),
                            'address_1': row.CustomerAddress.address,
                            'province': dropdown(row.AddressProvince),
                            'address_2': row.CustomerAddress.address_2,
                            'state': dropdown(row.AddressDistrict),
                            "zip_code": row.CustomerAddress.zip_code
                        }
                    }
            else:
                if row.CustomerAddress.address_same_permanent_flag == CUSTOMER_ADDRESS_SAME_PERMANENT_FLAG:
                    contact_address = {
                        "country": dropdown(row.AddressCountry),
                        'province': dropdown(row.AddressProvince),
                        'district': dropdown(row.AddressDistrict),
                        "ward": dropdown(row.AddressWard),
                        'number_and_street': row.CustomerAddress.address,
                        'resident_address_flag': row.CustomerAddress.address_same_permanent_flag
                    }
                # TODO: kiểm tra lại cờ giống địa chỉ thường trú
                elif row.CustomerAddress.address_domestic_flag == CUSTOMER_ADDRESS_DOMESTIC_FLAG:
                    resident_address['domestic_address'].update(
                        resident_address_flag=row.CustomerAddress.address_same_permanent_flag
                    )
                    contact_address = resident_address['domestic_address']

            # lấy thông tin nghề nghiệp
            career_information = {
                "career": dropdown(row.Career) if row.Career else None,
                "average_income_amount": dropdown(row.AverageIncomeAmount),
                "company_name": row.CustomerProfessional.company_name,
                "company_phone": row.CustomerProfessional.company_phone,
                "company_position": dropdown(row.Position) if row.Position else None,
                "company_address": row.CustomerProfessional.company_address
            }

        response_data = {
            'resident_address': resident_address,
            'resident_address_active_flag': resident_address_active_flag,
            'contact_address': contact_address,
            'contact_address_active_flag': contact_address_active_flag,
            'career_information': career_information
        }
        return self.response(
            data=response_data
        )

    async def save_contact_information(
            self, cif_id: str,
            contact_information_save_request: ContactInformationSaveRequest
    ):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # Kiểm tra thông tin liên lạc tạo mới hay cập nhật => Kiểm tra theo thông tin nghề nghiệp
        customer_datas = self.call_repos(
            await repos_get_customer_professional_and_identity_and_address(cif_id=cif_id, session=self.oracle_session))
        _, customer_professional, customer_identity, _ = customer_datas[0]
        is_create = True if not customer_professional else False

        saving_resident_address = None
        saving_contact_address = None

        customer_resident_address = None
        customer_contact_address = None
        for _, _, _, customer_address in customer_datas:
            if customer_address:
                if customer_address.address_type_id == RESIDENT_ADDRESS_CODE:
                    customer_resident_address = customer_address
                if customer_address.address_type_id == CONTACT_ADDRESS_CODE:
                    customer_contact_address = customer_address

        is_passport = False
        # RULE: Nếu GTĐD là Hộ chiếu -> có địa chỉ thường trú, địa chỉ liên lạc
        if customer_identity.identity_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            is_passport = True
            ############################################################################################################
            # Địa chỉ thường trú
            ############################################################################################################
            resident_address = contact_information_save_request.resident_address
            # Địa chỉ thường trú không được để trống
            if not resident_address:
                return self.response_exception(msg="Resident Address is not null", loc="resident_address")

            resident_address_domestic_flag = resident_address.domestic_flag

            saving_resident_address = {
                "customer_id": cif_id,
                "address_type_id": RESIDENT_ADDRESS_CODE
            }
            # Nếu địa chỉ thường trú là địa chỉ trong nước
            if resident_address_domestic_flag:
                if not resident_address.domestic_address:
                    return self.response_exception(
                        msg="Domestic Address not is not null",
                        loc="resident_address -> domestic_address"
                    )
                # check resident_address_domestic_address_country
                resident_domestic_country_id = resident_address.domestic_address.country.id
                if is_create or resident_domestic_country_id:
                    await self.get_model_object_by_id(
                        model_id=resident_domestic_country_id,
                        model=AddressCountry,
                        loc="resident_address -> domestic_address -> country -> id"
                    )

                # check resident_address_domestic_address_province
                resident_domestic_province_id = resident_address.domestic_address.province.id
                if is_create or (customer_resident_address.address_province_id != resident_domestic_province_id):
                    await self.get_model_object_by_id(
                        model_id=resident_domestic_province_id,
                        model=AddressProvince,
                        loc="resident_address -> domestic_address -> province -> id"
                    )

                # check resident_address_domestic_address_district
                resident_domestic_district_id = resident_address.domestic_address.district.id
                if is_create or (customer_resident_address.address_district_id != resident_domestic_district_id):
                    await self.get_model_object_by_id(
                        model_id=resident_domestic_district_id,
                        model=AddressDistrict,
                        loc="resident_address -> domestic_address -> district -> id"
                    )

                # check resident_address_domestic_address_ward
                resident_domestic_ward_id = resident_address.domestic_address.ward.id
                if is_create or (customer_resident_address.address_ward_id != resident_domestic_ward_id):
                    await self.get_model_object_by_id(
                        model_id=resident_domestic_ward_id,
                        model=AddressWard,
                        loc="resident_address -> domestic_address -> ward -> id"
                    )

                saving_resident_address.update({
                    "address_country_id": resident_domestic_country_id,
                    "address_province_id": resident_domestic_province_id,
                    "address_district_id": resident_domestic_district_id,
                    "address_ward_id": resident_domestic_ward_id,
                    "address": resident_address.domestic_address.number_and_street,
                    "zip_code": None,
                    "latitude": None,
                    "longitude": None,
                    "address_primary_flag": None,
                    "address_domestic_flag": resident_address_domestic_flag,
                    "address_2": None,
                    "address_same_permanent_flag": False
                })

            # Nếu địa chỉ thường trú là địa chỉ nước ngoài
            else:
                # check resident_address_foreign_address_country
                resident_foreign_country_id = resident_address.foreign_address.country.id
                if is_create or (customer_resident_address.address_country_id != resident_foreign_country_id):
                    await self.get_model_object_by_id(
                        model_id=resident_foreign_country_id,
                        model=AddressCountry,
                        loc="resident_address -> foreign_address -> country -> id"
                    )

                # Thành phố nước ngoài lưu vào AddressDistrict
                # check resident_address_foreign_address_province
                resident_foreign_province_id = resident_address.foreign_address.province.id
                if is_create or (customer_resident_address.address_district_id != resident_foreign_province_id):
                    await self.get_model_object_by_id(
                        model_id=resident_foreign_province_id,
                        model=AddressDistrict,
                        loc="resident_address -> foreign_address -> province -> id"
                    )

                # Tỉnh/Bang nước ngoài là Tỉnh/TP VN
                # check resident_address_foreign_address_state
                resident_foreign_state_id = resident_address.foreign_address.state.id
                if is_create or (customer_resident_address.address_province_id != resident_foreign_state_id):
                    await self.get_model_object_by_id(
                        model_id=resident_foreign_state_id,
                        model=AddressProvince,
                        loc="resident_address -> foreign_address -> state -> id"
                    )

                resident_foreign_address_1 = resident_address.foreign_address.address_1

                resident_foreign_address_2 = resident_address.foreign_address.address_2

                resident_foreign_zip_code = resident_address.foreign_address.zip_code

                saving_resident_address.update({
                    "address_country_id": resident_foreign_country_id,
                    "address_province_id": resident_foreign_state_id,
                    "address_district_id": resident_foreign_province_id,
                    "address_ward_id": None,
                    "address": resident_foreign_address_1,
                    "zip_code": resident_foreign_zip_code,
                    "latitude": None,
                    "longitude": None,
                    "address_primary_flag": None,
                    "address_domestic_flag": resident_address_domestic_flag,
                    "address_2": resident_foreign_address_2,
                    "address_same_permanent_flag": False
                })
            ############################################################################################################

            ############################################################################################################
            # Địa chỉ liên lạc
            ############################################################################################################

            contact_address = contact_information_save_request.contact_address
            # RULE: Địa chỉ liên lạc không được giống địa chỉ thường trú nếu địa chỉ thường trú là địa chỉ nước ngoài
            if not resident_address.domestic_flag and contact_address.resident_address_flag:
                return self.response_exception(msg="resident_address_flag is not True",
                                               loc="contact_address -> resident_address_flag")
            contact_address_resident_address_flag = contact_address.resident_address_flag
            contact_address_province_id = contact_address.province.id
            contact_address_district_id = contact_address.district.id
            contact_address_ward_id = contact_address.ward.id

            # Nếu địa chỉ liên lạc khác địa chỉ thường trú hoặc địa chỉ thường trú là nước ngoài
            if not contact_address_resident_address_flag or not resident_address.domestic_flag:
                # check contact_address_province
                if is_create or (customer_contact_address.address_province_id != contact_address_province_id):
                    await self.get_model_object_by_id(contact_address_province_id, AddressProvince,
                                                      "contact_address -> province -> id")

                # check contact_address_district
                if is_create or (customer_contact_address.address_district_id != contact_address_district_id):
                    await self.get_model_object_by_id(contact_address_district_id, AddressDistrict,
                                                      "contact_address -> district -> id")

                # check contact_address_ward
                if is_create or (customer_contact_address.address_ward_id != contact_address_ward_id):
                    await self.get_model_object_by_id(contact_address_ward_id, AddressWard,
                                                      "contact_address -> ward -> id")

                saving_contact_address = {
                    "customer_id": cif_id,
                    "address_type_id": CONTACT_ADDRESS_CODE,
                    # RULE: Với địa chỉ thường trú nước ngoài, địa chỉ tạm trú phải lấy ở VN
                    "address_country_id": ADDRESS_COUNTRY_CODE_VN,
                    "address_province_id": contact_address_province_id,
                    "address_district_id": contact_address_district_id,
                    "address_ward_id": contact_address_ward_id,
                    "address": contact_address.number_and_street,
                    "zip_code": None,
                    "latitude": None,
                    "longitude": None,
                    "address_primary_flag": None,
                    "address_domestic_flag": True,  # Địa chỉ liên lạc là địa chỉ trong nước
                    "address_2": None,
                    "address_same_permanent_flag": False
                }
            # Nếu địa chỉ liên lạc giống địa chỉ thường trú
            else:
                saving_contact_address = saving_resident_address.copy()
                # Giống địa chỉ thường trú nhưng vẫn là tạm trú
                saving_contact_address.update({
                    "address_same_permanent_flag": True,
                    "address_type_id": CONTACT_ADDRESS_CODE,
                    "address_domestic_flag": True  # Địa chỉ liên lạc là địa chỉ trong nước
                })
        ############################################################################################################

        ################################################################################################################
        # Thông tin nghề nghiệp
        ################################################################################################################

        # check career
        career_id = contact_information_save_request.career_information.career.id
        if is_create or (customer_professional.career_id != career_id):
            await self.get_model_object_by_id(career_id, Career, "career_information -> career -> id")

        # check average_income_amount
        average_income_amount_id = contact_information_save_request.career_information.average_income_amount.id
        if is_create or (customer_professional.average_income_amount_id != average_income_amount_id):
            await self.get_model_object_by_id(average_income_amount_id, AverageIncomeAmount,
                                              "career_information -> average_income_amount -> id")

        # check company_position
        company_position_id = contact_information_save_request.career_information.company_position.id
        if is_create or (customer_professional.position_id != company_position_id):
            if company_position_id:
                await self.get_model_object_by_id(company_position_id, Position,
                                                  "career_information -> company_position -> id")

        if is_create:
            # Tạo thông tin nghề nghiệp khách hàng
            customer_professional_id = generate_uuid()
        else:
            customer_professional_id = customer_professional.id
        saving_career_information = {
            "id": customer_professional_id,
            "career_id": career_id,
            "average_income_amount_id": average_income_amount_id,
            "company_name": contact_information_save_request.career_information.company_name,
            "company_phone": contact_information_save_request.career_information.company_phone,
            "position_id": company_position_id,
            "company_address": contact_information_save_request.career_information.company_address
        }

        ################################################################################################################
        contact_information_detail_data = self.call_repos(
            await repos_save_contact_information(
                cif_id=cif_id,
                customer_professional_id=customer_professional_id,
                is_create=is_create,
                is_passport=is_passport,
                saving_resident_address=saving_resident_address,
                saving_contact_address=saving_contact_address,
                saving_career_information=saving_career_information,
                log_data=contact_information_save_request.json(),
                session=self.oracle_session
            )
        )

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        contact_information_detail_data.update(booking=dict(
            id=booking.id,
            code=booking.code
        ))

        return self.response(data=contact_information_detail_data)
