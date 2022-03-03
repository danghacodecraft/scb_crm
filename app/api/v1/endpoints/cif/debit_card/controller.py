from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.debit_card.repository import (
    repos_add_debit_card, repos_debit_card, repos_get_list_debit_card
)
from app.api.v1.endpoints.cif.debit_card.schema import DebitCardRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.address import (
    AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.card import (
    BrandOfCard, CardIssuanceFee, CardIssuanceType, CardType
)
from app.third_parties.oracle.models.master_data.customer import CustomerType
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.error_messages import VALIDATE_ERROR
from app.utils.functions import generate_uuid, now
from app.utils.vietnamese_converter import convert_to_unsigned_vietnamese


class CtrDebitCard(BaseController):
    async def ctr_debit_card(self, cif_id: str):

        debit_card = self.call_repos(await repos_debit_card(cif_id, self.oracle_session))
        return self.response(debit_card)

    async def ctr_add_debit_card(
            self,
            cif_id: str,
            debt_card_req: DebitCardRequest
    ):
        # check register_flag == False thì ko insert data
        if not debt_card_req.issue_debit_card.register_flag:
            return self.response({"cif_id": cif_id})

        # check, get current user
        current_user = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        # convert last name, first name to unsigned vietnamese
        last_name = convert_to_unsigned_vietnamese(
            current_user.last_name
        )
        first_name = convert_to_unsigned_vietnamese(
            current_user.first_name
        )

        """
            I. validate physical_card_type
                 1. check Constant
                 2. check số lượng nhỏ hơn 2
                 3. check trùng loạis

        """
        card_type = []
        for debt_card_type in debt_card_req.issue_debit_card.physical_card_type:
            card_type.append(debt_card_type.id)
        if len(card_type) > 2:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="Too many physical_card_type",
                loc="issue_debit_card -> physical_card_type"
            )
        if len(card_type) < 1:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="physical_card_type is null",
                loc="issue_debit_card -> physical_card_type"
            )
        if len(card_type) == 2 and card_type[0] == card_type[1]:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="Data is duplicate",
                loc="issue_debit_card -> physical_card_type -> 1"
            )

        # check CardType exist
        await self.get_model_objects_by_ids(
            model=CardType,
            model_ids=list(card_type),
            loc="issue_debit_card -> physical_issuance_type -> id",
        )

        """Kiểm tra physical_issuance_type exist"""
        await self.get_model_object_by_id(
            model=CardIssuanceType,
            model_id=debt_card_req.issue_debit_card.physical_issuance_type.id,
            loc="issue_debit_card -> physical_issuance_type -> id",
        )

        """Kiểm tra customer_type"""
        await self.get_model_object_by_id(
            model=CustomerType,
            model_id=debt_card_req.issue_debit_card.customer_type.id,
            loc="issue_debit_card -> customer_type -> id",
        )

        """Kiểm tra branch_of_card"""
        await self.get_model_object_by_id(
            model=BrandOfCard,
            model_id=debt_card_req.issue_debit_card.branch_of_card.id,
            loc="issue_debit_card -> branch_of_card -> id",
        )

        """Kiểm tra issuance_fee"""
        await self.get_model_object_by_id(
            model=CardIssuanceFee,
            model_id=debt_card_req.issue_debit_card.issuance_fee.id,
            loc="issue_debit_card -> issuance fee -> id",
        )

        """Validate tên dập nổi không quá 21 kí tự"""
        lenght_name = len(first_name) + len(last_name)
        if debt_card_req.information_debit_card.name_on_card.middle_name_on_card:
            lenght_name = lenght_name + len(debt_card_req.information_debit_card.name_on_card.middle_name_on_card)

        if lenght_name > 21:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="Name on card is too long",
                loc="issue_debit_card -> information_debit_card -> name_on_card -> middle_name_on_card"
            )

        """Validate địa chỉ nhận thẻ"""
        if not debt_card_req.card_delivery_address.delivery_address_flag:
            # check Branch exist
            if not debt_card_req.card_delivery_address.scb_branch:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="scb_branch is null",
                    loc="card_delivery_address -> scb_branch"
                )
            await self.get_model_object_by_id(
                model=Branch,
                model_id=debt_card_req.card_delivery_address.scb_branch.id,
                loc="card_delivery_address -> scb_branch -> id",
            )
        else:
            if not debt_card_req.card_delivery_address.delivery_address:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="delivery_address is null",
                    loc="card_delivery_address -> delivery_address"
                )
            # check province
            await self.get_model_object_by_id(
                model=AddressProvince,
                model_id=debt_card_req.card_delivery_address.delivery_address.province.id,
                loc="card_delivery_address -> delivery_address -> province -> id",
            )
            # check district
            await self.get_model_object_by_id(
                model=AddressDistrict,
                model_id=debt_card_req.card_delivery_address.delivery_address.district.id,
                loc="card_delivery_address -> delivery_address -> district -> id",
            )
            # check ward
            await self.get_model_object_by_id(
                model=AddressWard,
                model_id=debt_card_req.card_delivery_address.delivery_address.ward.id,
                loc="card_delivery_address -> delivery_address -> ward -> id",
            )

            if not debt_card_req.card_delivery_address.delivery_address.number_and_street:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="number_and_street is null",
                    loc="card_delivery_address -> delivery_address -> number_and_street"
                )

        id_primary_card = generate_uuid()
        list_sub_delivery_address = []
        list_sub_debit_card = []
        list_sub_debit_card_type = []

        """Kiểm tra validate thông tin thẻ phụ"""
        if debt_card_req.information_sub_debit_card is not None:
            for index, sub_card in enumerate(debt_card_req.information_sub_debit_card.sub_debit_cards):

                """Kiểm tra sub physical_card_type (Tính vật lý) tồn tại"""
                sub_card_type = []
                for item_card_type in sub_card.physical_card_type:
                    sub_card_type.append(item_card_type.id)
                if len(sub_card_type) > 2 or len(sub_card_type) < 1:
                    return self.response_exception(
                        msg=VALIDATE_ERROR,
                        detail="Too many physical_card_type",
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> physical_card_type"
                    )
                if len(sub_card_type) == 2 and sub_card_type[0] == sub_card_type[1]:
                    return self.response_exception(
                        msg=VALIDATE_ERROR,
                        detail="Data physical_card_type is duplicate",
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> physical_card_type -> 1"
                    )

                for idx, _ in enumerate(sub_card.physical_card_type):
                    await self.get_model_object_by_id(
                        model_id=_.id,
                        model=CardType,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> physical_card_type -> {idx} -> id",
                    )

                """Kiểm tra physical_issuance_type (Hình thức phát hành thẻ) exist"""
                await self.get_model_object_by_id(
                    model=CardIssuanceType,
                    model_id=sub_card.card_issuance_type.id,
                    loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_issuance_type -> id",
                )

                """Validate địa chỉ nhận thẻ"""
                if not sub_card.card_delivery_address.delivery_address_flag:
                    # Kiểm tra Branch exist
                    if not sub_card.card_delivery_address.scb_branch:
                        return self.response_exception(
                            msg=VALIDATE_ERROR,
                            detail="scb_branch is null",
                            loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> scb_branch"
                        )
                    await self.get_model_object_by_id(
                        model=Branch,
                        model_id=sub_card.card_delivery_address.scb_branch.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> scb_branch -> id",
                    )
                else:
                    if not sub_card.card_delivery_address.delivery_address:
                        return self.response_exception(
                            msg=VALIDATE_ERROR,
                            detail="delivery_address is null",
                            loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> delivery_address"
                        )
                    # check province
                    await self.get_model_object_by_id(
                        model=AddressProvince,
                        model_id=sub_card.card_delivery_address.delivery_address.province.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> province -> id",
                    )
                    # check district
                    await self.get_model_object_by_id(
                        model=AddressDistrict,
                        model_id=sub_card.card_delivery_address.delivery_address.district.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> district -> id",
                    )
                    # check ward
                    await self.get_model_object_by_id(
                        model=AddressWard,
                        model_id=sub_card.card_delivery_address.delivery_address.ward.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> ward -> id",
                    )

            list_data_sub_debit_card = debt_card_req.information_sub_debit_card.sub_debit_cards

            for sub_debit_card in list_data_sub_debit_card:
                sub_uuid = generate_uuid()
                # neu scb_delivery_address_flag la True thi dia chi nhan la SCB
                if sub_debit_card.card_delivery_address.delivery_address_flag is False:
                    # dia chi nhan (the phu)
                    sub_delivery_add = {
                        "id": sub_uuid,
                        "branch_id": sub_debit_card.card_delivery_address.scb_branch.id,
                        "province_id": None,
                        "district_id": None,
                        "ward_id": None,
                        "card_delivery_address_address": None,
                        "card_delivery_address_note": None,
                    }
                    list_sub_delivery_address.append(sub_delivery_add)
                else:  # neu scb_delivery_address_flag la False thi dia chi nhan la dia chi khac
                    sub_delivery_add = {
                        "id": sub_uuid,
                        "branch_id": None,
                        "province_id": sub_debit_card.card_delivery_address.delivery_address.province.id,
                        "district_id": sub_debit_card.card_delivery_address.delivery_address.district.id,
                        "ward_id": sub_debit_card.card_delivery_address.delivery_address.ward.id,
                        "card_delivery_address_address": sub_debit_card.card_delivery_address.delivery_address.number_and_street,
                        "card_delivery_address_note": sub_debit_card.card_delivery_address.note,
                    }
                    list_sub_delivery_address.append(sub_delivery_add)
                # thong tin (the phu)
                sub_data_debit_card = {
                    "id": generate_uuid(),
                    "customer_id": cif_id,
                    "card_issuance_type_id": sub_debit_card.card_issuance_type.id,
                    "customer_type_id": debt_card_req.issue_debit_card.customer_type.id,
                    "brand_of_card_id": debt_card_req.issue_debit_card.branch_of_card.id,
                    "card_issuance_fee_id": debt_card_req.issue_debit_card.issuance_fee.id,
                    "card_delivery_address_id": sub_uuid,
                    "parent_card_id": id_primary_card,
                    "card_registration_flag": debt_card_req.issue_debit_card.register_flag,
                    "payment_online_flag": sub_debit_card.payment_online_flag,
                    "first_name_on_card": first_name.upper(),  # uppercase first name
                    "last_name_on_card": last_name.upper(),  # uppercase last name
                    "card_delivery_address_flag": sub_debit_card.card_delivery_address.delivery_address_flag,
                    "created_at": now(),
                    "active_flag": 1
                }
                if sub_debit_card.name_on_card.middle_name_on_card:
                    sub_data_debit_card.update({
                        "middle_name_on_card": sub_debit_card.name_on_card.middle_name_on_card.upper()
                    })
                list_sub_debit_card.append(sub_data_debit_card)
                # loai the (the phu)
                for card_type in sub_debit_card.physical_card_type:
                    data_sub_debit_card_type = {
                        "card_id": sub_data_debit_card["id"],
                        "card_type_id": card_type.id,
                    }
                    list_sub_debit_card_type.append(data_sub_debit_card_type)

        """ Insert data thẻ chính """
        uuid = generate_uuid()
        # Địa chỉ nhận thẻ chính
        # neu scb_delivery_address_flag la False thi dia chi nhan la SCB
        if not debt_card_req.card_delivery_address.delivery_address_flag:
            data_card_delivery_address = {
                "id": uuid,
                "branch_id": debt_card_req.card_delivery_address.scb_branch.id,
                "province_id": None,
                "district_id": None,
                "ward_id": None,
                "card_delivery_address_address": None,
                "card_delivery_address_note": None,
            }
        else:  # neu scb_delivery_address_flag la True thi dia chi nhan la dia chi khac
            data_card_delivery_address = {
                "id": uuid,
                "branch_id": None,
                "province_id": debt_card_req.card_delivery_address.delivery_address.province.id,
                "district_id": debt_card_req.card_delivery_address.delivery_address.district.id,
                "ward_id": debt_card_req.card_delivery_address.delivery_address.ward.id,
                "card_delivery_address_address": debt_card_req.card_delivery_address.delivery_address.number_and_street,
                "card_delivery_address_note": debt_card_req.card_delivery_address.note,
            }
        # thong tin the chinh
        data_debit_card = {
            "id": id_primary_card,
            "customer_id": cif_id,
            "card_issuance_type_id": debt_card_req.issue_debit_card.physical_issuance_type.id,
            "customer_type_id": debt_card_req.issue_debit_card.customer_type.id,
            "brand_of_card_id": debt_card_req.issue_debit_card.branch_of_card.id,
            "card_issuance_fee_id": debt_card_req.issue_debit_card.issuance_fee.id,
            "card_delivery_address_id": uuid,
            "parent_card_id": None,
            "card_registration_flag": debt_card_req.issue_debit_card.register_flag,
            "payment_online_flag": debt_card_req.issue_debit_card.payment_online_flag,
            "first_name_on_card": first_name.upper(),  # uppercase first name
            "last_name_on_card": last_name.upper(),  # uppercase last name
            "card_delivery_address_flag": debt_card_req.card_delivery_address.delivery_address_flag,
            "created_at": now(),
            "active_flag": 1,
        }
        if debt_card_req.information_debit_card.name_on_card.middle_name_on_card:
            data_debit_card.update({
                "middle_name_on_card": debt_card_req.information_debit_card.name_on_card.middle_name_on_card.upper()
            })

        # loai the (the chinh)
        list_debit_card_type = []
        for debit_card_type_data in debt_card_req.issue_debit_card.physical_card_type:
            debit_card_type = {
                "card_id": data_debit_card["id"],
                "card_type_id": debit_card_type_data.id,
            }
            list_debit_card_type.append(debit_card_type)

        add_debit_card = self.call_repos(
            await repos_add_debit_card(
                cif_id,
                data_card_delivery_address=data_card_delivery_address,
                data_debit_card=data_debit_card,
                list_debit_card_type=list_debit_card_type,
                list_sub_delivery_address=list_sub_delivery_address,
                list_sub_debit_card=list_sub_debit_card,
                list_sub_debit_card_type=list_sub_debit_card_type,
                log_data=debt_card_req.json(),
                session=self.oracle_session,
            )
        )
        return self.response(add_debit_card)

    async def ctr_list_debit_card_type(self, cif_id: str,
                                       branch_of_card_id: str,
                                       issuance_fee_id: str,
                                       annual_fee_id: str,
                                       ):
        info_debit_card_types = self.call_repos(
            await repos_get_list_debit_card(
                cif_id,
                branch_of_card_id,
                issuance_fee_id,
                annual_fee_id
            ))
        return self.response(info_debit_card_types)
