from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.template.detail.repository import (
    repo_customer_address, repo_customer_info, repo_debit_card, repo_e_banking,
    repo_form, repo_guardians, repo_join_account_holder, repo_sub_identity
)
from app.settings.config import DATE_INPUT_OUTPUT_EKYC_FORMAT
from app.utils.constant.cif import CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
from app.utils.constant.tms_dms import (
    PATH_FORM_1, PATH_FORM_2, PATH_FORM_3, PATH_FORM_4, PATH_FORM_5,
    PATH_FORM_6
)
from app.utils.functions import datetime_to_string, today


class CtrTemplateDetail(BaseController):
    async def ctr_form_1(self, cif_id: str):
        """
        Biểu mẫu 1
        """
        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]

        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        subs_identity = self.call_repos(await repo_sub_identity(cif_id=cif_id, session=self.oracle_session))
        guardians = self.call_repos(await repo_guardians(cif_id=cif_id, session=self.oracle_session))
        customer_join = self.call_repos(await repo_join_account_holder(cif_id=cif_id, session=self.oracle_session))
        debit_cards = self.call_repos(await repo_debit_card(cif_id=cif_id, session=self.oracle_session))
        e_banking = self.call_repos(await repo_e_banking(cif_id=cif_id, session=self.oracle_session))
        # fatca_info = self.call_repos(await repos_fatca_info(cif_id=cif_id, session=self.oracle_session))

        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None
        if debit_cards:
            for address in customer_address:
                if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                    staying_address = address
                if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                    resident_address = address

        # Tách thẻ chính và thẻ phụ
        main_cards, sup_cards = [], []
        for item in debit_cards:
            if item.DebitCard.parent_card_id:
                sup_cards.append(item)
            else:
                main_cards.append(item)

        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": [cust.CustomerGender.name],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.2.23": [cust.ResidentStatus.name],
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.36": subs_identity[0].name,
            "S1.A.1.2.38": datetime_to_string(subs_identity[0].sub_identity_expired_date,
                                              DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            # TODO: Địa chỉ cư trú tại nước ngoài (chưa có)
            # "S1.A.1.2.30"
            # "S1.A.1.2.31"
            # "S1.A.1.2.32"
            # "S1.A.1.2.33"

            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.6": ["Đồng ý"] if cust.Customer.advertising_marketing_flag else ["Không đồng ý"],

            "S1.A.1.5.4": [cust.Career.name],
            "S1.A.1.5.3": [cust.AverageIncomeAmount.name],
            "S1.A.1.2.9": [cust.MaritalStatus.name],

        })
        # Người giám hộ
        if guardians:
            guardian = guardians[0]
            data_request.update({
                # "S1.A.1.2.41": guardian.CustomerRelationshipType.name,
                "S1.A.1.2.44": guardian.Customer.full_name_vn,
                "S1.A.1.2.42": guardian.Customer.cif_number,
                "S1.A.1.2.51": guardian.CustomerIdentity.identity_num
            })
        # Người đồng sở hữu
        if customer_join:
            customer = customer_join[0]
            data_request.update({
                # "S1.A.1.8": "",
                "S1.A.1.8.3": customer.CustomerJoin.full_name_vn,
                "S1.A.1.8.2": customer.CustomerJoin.cif_number,
                "S1.A.1.8.4": customer.CustomerIdentity.identity_num
            })
        # Thẻ ghi nợ (Thẻ chính - Thẻ phụ)
        if main_cards:
            data_request.update({
                "S1.A.1.10.10": main_cards[0].BrandOfCard.name,
                "S1.A.1.10.3": [main_cards[0].CardIssuanceType.name],
                "S1.A.1.10.16": main_cards[0].CasaAccount.casa_account_number,
                "S1.A.1.10.14": {
                    "value": main_cards[0].Customer.full_name,
                    "type": "embossed_table"

                }
            })

        if sup_cards:
            data_request.update({
                "S1.A.1.10.27.1": sup_cards[0].Customer.full_name_vn,
                "S1.A.1.10.27": sup_cards[0].Customer.cif_number,
                "S1.A.1.10.27.2": sup_cards[0].CustomerIdentity.identity_num,
                "S1.A.1.10.28": {
                    "value": sup_cards[0].Customer.full_name,
                    "type": "embossed_table"
                }
            })
            if sup_cards[0].DebitCard.card_delivery_address_flag:
                data_request.update({"S1.A.1.10.18": ["Địa chỉ liên lạc"]})
            else:
                data_request.update({"S1.A.1.10.18.1": ["SCB"]})
        # E-banking
        if e_banking:
            e_banking = e_banking[0]
            # TODO
            # "S1.A.1.9.14":
            if e_banking.EBankingInfo.account_name:
                data_request.update({"S1.A.1.9.5": [e_banking.EBankingInfo.account_name]})
            if e_banking.EBankingInfo.method_active_password_id:
                data_request.update({"S1.A.1.9.7": [e_banking.EBankingInfo.method_active_password_id]})
            if e_banking.EBankingInfo.account_payment_fee:
                data_request.update({"S1.A.1.9.15": "Tự động ghi nợ TK:"})
                data_request.update({"S1.A.1.9.12": ["Tài khoản thanh toán"]})
                data_request.update({"S1.A.1.9.13": e_banking.EBankingInfo.account_payment_fee})
            else:
                data_request.update({"S1.A.1.9.15.1": "Tiền mặt"})
            # TODO
            # "S1.A.1.2.5"

        # Fatca
        # TODO
        # if fatca_info:
        #     if fatca_info.CustomerFatca.value == "1":
        #         data_request.update({"S1.A.1.5.2": ["Có"]})
        #     if fatca_info.CustomerFatca.value == "0":
        #         data_request.update({"S1.A.1.5.2": ["Không"]})

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            " S1.A.1.11.12": f'{time.year}',

        })
        # data_request.update({
        #     "S1.A.1.11.5": self.current_user.
        # })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.tax_number:
            data_request.update({"S1.A.1.3.6": cust.Customer.tax_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})
        if cust.CustomerProfessional.company_name:
            data_request.update({"S1.A.1.2.10": cust.CustomerProfessional.company_name})
        if cust.CustomerProfessional.company_address:
            data_request.update({"S1.A.1.2.11": cust.CustomerProfessional.company_address})
        if cust.CustomerProfessional.company_phone:
            data_request.update({"S1.A.1.2.12": cust.CustomerProfessional.company_phone})
        if cust.Position:
            data_request.update({"S1.A.1.2.13": cust.Position.name})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_1))
        return self.response(data_tms)

    async def ctr_form_2(self, cif_id: str):
        """
            Biểu mẫu 2
        """
        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]

        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        subs_identity = self.call_repos(await repo_sub_identity(cif_id=cif_id, session=self.oracle_session))
        guardians = self.call_repos(await repo_guardians(cif_id=cif_id, session=self.oracle_session))
        customer_join = self.call_repos(await repo_join_account_holder(cif_id=cif_id, session=self.oracle_session))
        debit_cards = self.call_repos(await repo_debit_card(cif_id=cif_id, session=self.oracle_session))
        e_banking = self.call_repos(await repo_e_banking(cif_id=cif_id, session=self.oracle_session))
        # fatca_info = self.call_repos(await repos_fatca_info(cif_id=cif_id, session=self.oracle_session))

        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None
        if debit_cards:
            for address in customer_address:
                if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                    staying_address = address
                if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                    resident_address = address

        # Tách thẻ chính và thẻ phụ
        main_cards, sup_cards = [], []
        for item in debit_cards:
            if item.DebitCard.parent_card_id:
                sup_cards.append(item)
            else:
                main_cards.append(item)

        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Nam" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.2.23": ["Không cư trú/Non-resident"] if cust.ResidentStatus.name == "Không cư trú" else [
                "Cư trú/Resident"],
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.36": subs_identity[0].name,
            "S1.A.1.2.38": datetime_to_string(subs_identity[0].sub_identity_expired_date,
                                              DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            # TODO: Địa chỉ cư trú tại nước ngoài (chưa có)
            # "S1.A.1.2.30"
            # "S1.A.1.2.31"
            # "S1.A.1.2.32"
            # "S1.A.1.2.33"

            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.6": ["Đồng ý/Agree"] if cust.Customer.advertising_marketing_flag else [
                "Không đồng ý/Do not agree"],

            "S1.A.1.5.4": [cust.Career.name],
            "S1.A.1.5.3": [cust.AverageIncomeAmount.name],
            "S1.A.1.2.9": ["Độc thân/Single"] if cust.MaritalStatus.name == "Độc thân" else ["Đã có gia đình/Married"],

        })
        # Người giám hộ
        if guardians:
            guardian = guardians[0]
            data_request.update({
                # "S1.A.1.2.41":,
                "S1.A.1.2.44": guardian.Customer.full_name_vn,
                "S1.A.1.2.42": guardian.Customer.cif_number,
                "S1.A.1.2.51": guardian.CustomerIdentity.identity_num
            })
        # Người đồng sở hữu
        if customer_join:
            customer = customer_join[0]
            data_request.update({
                # "S1.A.1.8": "",
                "S1.A.1.8.3": customer.CustomerJoin.full_name_vn,
                "S1.A.1.8.2": customer.CustomerJoin.cif_number,
                "S1.A.1.8.4": customer.CustomerIdentity.identity_num
            })
        # Thẻ ghi nợ (Thẻ chính - Thẻ phụ)
        if main_cards:
            data_request.update({
                "S1.A.1.10.10": main_cards[0].BrandOfCard.name,
                "S1.A.1.10.3": ["Thông thường/Regular"] if main_cards[0].CardIssuanceType.name == "THÔNG THƯỜNG" else [
                    "Nhanh/Instant"],
                "S1.A.1.10.16": main_cards[0].CasaAccount.casa_account_number,
                "S1.A.1.10.14": {
                    "value": main_cards[0].Customer.full_name,
                    "type": "embossed_table"

                }
            })

        if sup_cards:
            data_request.update({
                "S1.A.1.10.27.1 ": sup_cards[0].Customer.full_name_vn,
                "S1.A.1.10.27": sup_cards[0].Customer.cif_number,
                "S1.A.1.10.27.2": sup_cards[0].CustomerIdentity.identity_num,
                "S1.A.1.10.28": {
                    "value": sup_cards[0].Customer.full_name,
                    "type": "embossed_table"
                }
            })
            if sup_cards[0].DebitCard.card_delivery_address_flag:
                data_request.update({"S1.A.1.10.18": ["Địa chỉ liên lạc"]})
            else:
                data_request.update({"S1.A.1.10.18.1": ["SCB"]})
        # E-banking
        if e_banking:
            e_banking = e_banking[0]
            # TODO
            # "S1.A.1.9.14":
            if e_banking.EBankingInfo.account_name:
                data_request.update({"S1.A.1.9.5": [e_banking.EBankingInfo.account_name]})
            if e_banking.EBankingInfo.method_active_password_id:
                data_request.update({"S1.A.1.9.7": [e_banking.EBankingInfo.method_active_password_id]})
            if e_banking.EBankingInfo.account_payment_fee:
                data_request.update({"S1.A.1.9.15": "Tự động ghi nợ TK/Auto debit to account:"})
                data_request.update({"S1.A.1.9.12": ["Tài khoản thanh toán/Current account:"]})
                data_request.update({"S1.A.1.9.13": e_banking.EBankingInfo.account_payment_fee})
            else:
                data_request.update({"S1.A.1.9.15.1": "Tiền mặt/Cash"})
            # TODO
            # "S1.A.1.2.5"

        # Fatca
        # TODO
        # if fatca_info:
        #     if fatca_info.CustomerFatca.value == "1":
        #         data_request.update({"S1.A.1.5.2": ["Có"]})
        #     if fatca_info.CustomerFatca.value == "0":
        #         data_request.update({"S1.A.1.5.2": ["Không"]})

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            "S1.A.1.11.12": f'{time.year}',

        })
        # data_request.update({
        #     "S1.A.1.11.5": self.current_user.
        # })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.tax_number:
            data_request.update({"S1.A.1.3.6": cust.Customer.tax_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})
        if cust.CustomerProfessional.company_name:
            data_request.update({"S1.A.1.2.10": cust.CustomerProfessional.company_name})
        if cust.CustomerProfessional.company_address:
            data_request.update({"S1.A.1.2.11": cust.CustomerProfessional.company_address})
        if cust.CustomerProfessional.company_phone:
            data_request.update({"S1.A.1.2.12": cust.CustomerProfessional.company_phone})
        if cust.Position:
            data_request.update({"S1.A.1.2.13": cust.Position.name})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_2))
        return self.response(data_tms)

    async def ctr_form_3(self, cif_id: str):
        """
            Biểu mẫu 3
        """

        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]
        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None

        for address in customer_address:
            if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                staying_address = address
            if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = address
        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Nam" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.4": cust.Career.name,

        })

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.16.10": f'{time.day}',
            "S1.A.1.16.11": f'{time.month}',
            "S1.A.1.16.12": f'{time.year}',

        })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_3))
        return self.response(data_tms)

    async def ctr_form_4(self, cif_id: str):
        """
            Biểu mẫu 4
        """

        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]
        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None

        for address in customer_address:
            if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                staying_address = address
            if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = address
        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Nam" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.4": cust.Career.name,

        })

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            "S1.A.1.11.12": f'{time.year}',

        })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_4))
        return self.response(data_tms)

    async def ctr_form_5(self, cif_id: str):
        """
            Biểu mẫu 5
        """

        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]
        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None

        for address in customer_address:
            if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                staying_address = address
            if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = address
        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Nam" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.4": cust.Career.name,

        })

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            "S1.A.1.11.12": f'{time.year}',

        })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_5))
        return self.response(data_tms)

    async def ctr_form_6(self, cif_id: str):
        """
            Biểu mẫu 6
        """

        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]
        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None

        for address in customer_address:
            if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                staying_address = address
            if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = address
        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Nam" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.4": cust.Career.name,

        })

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            "S1.A.1.11.12": f'{time.year}',

        })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_6))
        return self.response(data_tms)
