from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.contact.repository import (
    repos_get_customer_addresses, repos_get_customer_professional,
    repos_get_detail_contact_information, repos_save_contact_information
)
from app.api.v1.endpoints.cif.basic_information.contact.schema import (
    ContactInformationSaveRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.repository import get_model_object_by_customer_id
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Career, Position
)
from app.utils.constant.cif import (
    ADDRESS_COUNTRY_CODE_VN, CONTACT_ADDRESS_CODE,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, RESIDENT_ADDRESS_CODE
)
from app.utils.functions import generate_uuid


class CtrContactInformation(BaseController):
    async def detail_contact_information(self, cif_id: str):
        contact_information_detail_data = self.call_repos(
            await repos_get_detail_contact_information(cif_id=cif_id)
        )
        return self.response(data=contact_information_detail_data)

    async def save_contact_information(
            self, cif_id: str,
            contact_information_save_request: ContactInformationSaveRequest
    ):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # Địa chỉ thường trú
        resident_address_domestic_flag = contact_information_save_request.resident_address.domestic_flag
        resident_address_domestic_address_country_id = contact_information_save_request. \
            resident_address.domestic_address.country.id
        resident_address_domestic_address_province_id = contact_information_save_request. \
            resident_address.domestic_address.province.id
        resident_address_domestic_address_district_id = contact_information_save_request. \
            resident_address.domestic_address.district.id
        resident_address_domestic_address_ward_id = contact_information_save_request. \
            resident_address.domestic_address.ward.id
        resident_address_domestic_number_and_street = contact_information_save_request. \
            resident_address.domestic_address.number_and_street

        resident_address_foreign_address_country_id = contact_information_save_request. \
            resident_address.foreign_address.country.id
        resident_address_foreign_address_province_id = contact_information_save_request. \
            resident_address.foreign_address.province.id
        resident_address_foreign_address_state_id = contact_information_save_request. \
            resident_address.foreign_address.state.id
        resident_address_foreign_address_address_1 = contact_information_save_request. \
            resident_address.foreign_address.address_1
        resident_address_foreign_address_address_2 = contact_information_save_request. \
            resident_address.foreign_address.address_2
        resident_address_foreign_zip_code = contact_information_save_request. \
            resident_address.foreign_address.zip_code

        # Địa chỉ liên lạc
        contact_address_resident_address_flag = contact_information_save_request.contact_address.resident_address_flag
        contact_address_province_id = contact_information_save_request.contact_address.province.id
        contact_address_district_id = contact_information_save_request.contact_address.district.id
        contact_address_ward_id = contact_information_save_request.contact_address.ward.id
        contact_address_number_and_street = contact_information_save_request.contact_address.number_and_street

        # Thông tin nghề nghiệp
        career_id = contact_information_save_request.career_information.career.id
        average_income_amount_id = contact_information_save_request.career_information.average_income_amount.id
        company_position_id = contact_information_save_request.career_information.company_position.id
        company_name = contact_information_save_request.career_information.company_name
        company_phone = contact_information_save_request.career_information.company_phone
        company_address = contact_information_save_request.career_information.company_address

        customer_identity = self.call_repos(await get_model_object_by_customer_id(
            customer_id=cif_id,
            model=CustomerIdentity,
            session=self.oracle_session,
            loc="customer_identity"
        ))
        resident_address = None
        contact_address = None
        # RULE: Nếu GTĐD là Hộ chiếu -> có địa chỉ thường trú, địa chỉ tạm trú
        if customer_identity.identity_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            ############################################################################################################
            # Địa chỉ thường trú
            ############################################################################################################
            resident_address = {
                "customer_id": cif_id,
                "address_type_id": RESIDENT_ADDRESS_CODE
            }
            contact_address = {
                "customer_id": cif_id,
                "address_type_id": CONTACT_ADDRESS_CODE
            }
            # Nếu là địa chỉ trong nước
            if resident_address_domestic_flag:
                # check resident_address_domestic_address_country
                await self.get_model_object_by_id(resident_address_domestic_address_country_id, AddressCountry,
                                                  "resident_address -> domestic_address -> country -> id")

                # check resident_address_domestic_address_province
                await self.get_model_object_by_id(resident_address_domestic_address_province_id, AddressProvince,
                                                  "resident_address -> domestic_address -> province -> id")

                # check resident_address_domestic_address_district
                await self.get_model_object_by_id(resident_address_domestic_address_district_id, AddressDistrict,
                                                  "resident_address -> domestic_address -> district -> id")

                # check resident_address_domestic_address_ward
                await self.get_model_object_by_id(resident_address_domestic_address_ward_id, AddressWard,
                                                  "resident_address -> domestic_address -> ward -> id")

                resident_address.update({
                    "address_country_id": resident_address_domestic_address_country_id,
                    "address_province_id": resident_address_domestic_address_province_id,
                    "address_district_id": resident_address_domestic_address_district_id,
                    "address_ward_id": resident_address_domestic_address_ward_id,
                    "address": resident_address_domestic_number_and_street,
                    "zip_code": None,
                    "latitude": None,
                    "longitude": None,
                    "address_primary_flag": None,
                    "address_domestic_flag": resident_address_domestic_flag,
                    "address_2": None,
                    "address_same_permanent_flag": False
                })
                ########################################################################################################
                # Địa chỉ liên lạc
                ########################################################################################################
                # Nếu giống địa chỉ thường trú
                if contact_address_resident_address_flag:
                    contact_address.update(resident_address)
                    # Giống địa chỉ thường trú nhưng vẫn là tạm trú
                    contact_address.update({
                        "address_same_permanent_flag": True,
                        "address_type_id": CONTACT_ADDRESS_CODE,
                        "address_domestic_flag": True  # Địa chỉ liên lạc là địa chỉ trong nước
                    })
                # Nếu khác địa chỉ thường trú
                else:
                    # check contact_address_province
                    await self.get_model_object_by_id(contact_address_province_id, AddressProvince,
                                                      "contact_address -> province -> id")

                    # check contact_address_district
                    await self.get_model_object_by_id(contact_address_district_id, AddressDistrict,
                                                      "contact_address -> district -> id")

                    # check contact_address_ward
                    await self.get_model_object_by_id(contact_address_ward_id, AddressWard,
                                                      "contact_address -> ward -> id")

                    contact_address.update({
                        "address_province_id": contact_address_province_id,
                        "address_district_id": contact_address_district_id,
                        "address_ward_id": contact_address_ward_id,
                        "address": contact_address_number_and_street,
                        "zip_code": None,
                        "latitude": None,
                        "longitude": None,
                        "address_primary_flag": None,
                        "address_domestic_flag": True,  # Địa chỉ liên lạc là địa chỉ trong nước
                        "address_2": None,
                        "address_same_permanent_flag": False
                    })
                ########################################################################################################

            # Nếu là địa chỉ nước ngoài
            else:
                # Không được giống địa chỉ thường trú
                if contact_address_resident_address_flag:
                    return self.response_exception(msg="resident_address_flag is not True",
                                                   loc="contact_address -> resident_address_flag")

                # check resident_address_foreign_address_country
                await self.get_model_object_by_id(resident_address_foreign_address_country_id, AddressCountry,
                                                  "resident_address -> foreign_address -> country -> id"),

                # Thành phố nước ngoài lưu vào AddressDistrict
                # check resident_address_foreign_address_province
                await self.get_model_object_by_id(resident_address_foreign_address_province_id, AddressDistrict,
                                                  "resident_address -> foreign_address -> province -> id")

                # Tỉnh/Bang nước ngoài là Tỉnh/TP VN
                # check resident_address_foreign_address_state
                await self.get_model_object_by_id(resident_address_foreign_address_state_id, AddressProvince,
                                                  "resident_address -> foreign_address -> state -> id")

                # check contact_address_province
                await self.get_model_object_by_id(contact_address_province_id, AddressProvince,
                                                  "contact_address -> province -> id")

                # check contact_address_district
                await self.get_model_object_by_id(contact_address_district_id, AddressDistrict,
                                                  "contact_address -> district -> id")

                # check contact_address_ward
                await self.get_model_object_by_id(contact_address_ward_id, AddressWard, "contact_address -> ward -> id")

                resident_address.update({
                    "address_country_id": resident_address_foreign_address_country_id,
                    "address_province_id": resident_address_foreign_address_state_id,
                    "address_district_id": resident_address_foreign_address_province_id,
                    "address_ward_id": None,
                    "address": resident_address_foreign_address_address_1,
                    "zip_code": resident_address_foreign_zip_code,
                    "latitude": None,
                    "longitude": None,
                    "address_primary_flag": None,
                    "address_domestic_flag": resident_address_domestic_flag,
                    "address_2": resident_address_foreign_address_address_2,
                    "address_same_permanent_flag": False
                })
                contact_address.update({
                    # Với địa chỉ thường trú nước ngoài, địa chỉ tạm trú phải lấy ở VN
                    "address_country_id": ADDRESS_COUNTRY_CODE_VN,
                    "address_province_id": contact_address_province_id,
                    "address_district_id": contact_address_district_id,
                    "address_ward_id": contact_address_ward_id,
                    "address": contact_address_number_and_street,
                    "zip_code": None,
                    "latitude": None,
                    "longitude": None,
                    "address_primary_flag": None,
                    "address_domestic_flag": True,  # Địa chỉ liên lạc là địa chỉ trong nước
                    "address_2": None,
                    "address_same_permanent_flag": False
                })

            ############################################################################################################

        ################################################################################################################
        # Thông tin nghề nghiệp
        ################################################################################################################
        # check career
        await self.get_model_object_by_id(career_id, Career, "career_information -> career -> id")

        # check average_income_amount
        await self.get_model_object_by_id(average_income_amount_id, AverageIncomeAmount,
                                          "career_information -> average_income_amount -> id")

        # check company_position
        await self.get_model_object_by_id(company_position_id, Position, "career_information -> company_position -> id")

        career_information = {
            "career_id": career_id,
            "average_income_amount_id": average_income_amount_id,
            "company_name": company_name,
            "company_phone": company_phone,
            "position_id": company_position_id,
            "company_address": company_address
        }

        ################################################################################################################

        is_exist_customer_address = await repos_get_customer_addresses(cif_id=cif_id, session=self.oracle_session)
        is_exist_customer_professional = await repos_get_customer_professional(
            cif_id=cif_id, session=self.oracle_session
        )
        # Nếu thông tin chưa có -> Tạo mới
        customer_professional_id = None
        if (not is_exist_customer_address) and (not is_exist_customer_professional):
            # Tạo thông tin nghề nghiệp khách hàng
            customer_professional_id = generate_uuid()
            career_information.update({
                "id": customer_professional_id
            })
            is_create = True
        # Nếu thông tin có trước ->  cập nhật
        else:
            is_create = False

        contact_information_detail_data = self.call_repos(
            await repos_save_contact_information(
                cif_id=cif_id,
                customer_professional_id=customer_professional_id,
                is_create=is_create,
                resident_address=resident_address,
                contact_address=contact_address,
                career_information=career_information,
                session=self.oracle_session
            )
        )
        return self.response(data=contact_information_detail_data)
