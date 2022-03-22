from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_detail_co_owner, repos_get_account_holders,
    repos_get_agreement_authorizations, repos_get_casa_account,
    repos_get_co_owner, repos_save_co_owner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_check_exist_cif, repos_validate_cif_number
)
from app.settings.event import service_soa
from app.utils.functions import generate_uuid


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, cif_id: str, co_owner: AccountHolderRequest):
        # lấy casa_account_id theo số cif_id
        casa_account = self.call_repos(
            await repos_get_casa_account(cif_id=cif_id, session=self.oracle_session)
        )

        # lấy danh sách cif_number account request
        for cif_number in co_owner.joint_account_holders:
            # check số cif_number có tồn tại trong SOA
            response = self.call_repos(
                await repos_check_exist_cif(cif_number=cif_number.cif_number)
            )
            if not response["is_existed"]:
                return self.response_exception(
                    msg="cif_number not exits in SOA", loc="AccountHolderRequest"
                )

        # # check cif_number có tồn tại
        # self.call_repos(
        #     await repos_check_list_cif_number(
        #         list_cif_number_request=list_cif_number_request,
        #         session=self.oracle_session
        #     )
        # )

        save_account_holder = []
        for account_holder in co_owner.joint_account_holders:
            save_account_holder.append(
                {
                    "id": generate_uuid(),
                    "cif_num": account_holder.cif_number,
                    "casa_account_id": casa_account,
                    "joint_account_holder_flag": co_owner.joint_account_holder_flag,
                    "joint_account_holder_no": 1,
                }
            )

        save_account_agree = []
        for agreement in co_owner.agreement_authorization:
            for signature in agreement.signature_list:
                for account_holder in save_account_holder:
                    if signature.cif_number == account_holder["cif_num"]:
                        save_account_agree.append(
                            {
                                "agreement_authorization_id": agreement.id,
                                "joint_account_holder_id": account_holder["id"],
                                "agreement_flag": agreement.agreement_flag,
                                "method_sign": agreement.method_sign,
                            }
                        )

        co_owner_data = self.call_repos(
            await repos_save_co_owner(
                cif_id=cif_id,
                save_account_holder=save_account_holder,
                save_account_agree=save_account_agree,
                log_data=co_owner.json(),
                session=self.oracle_session,
                created_by=self.current_user.username
            )
        )

        return self.response(data=co_owner_data)

    async def ctr_co_owner(self, cif_id: str):
        detail_co_owner = self.call_repos(
            await repos_get_co_owner(
                cif_id=cif_id,
                session=self.oracle_session,
            )
        )
        agreement_authorizations = self.call_repos(
            await repos_get_agreement_authorizations(
                session=self.oracle_session
            )
        )
        account_holders = self.call_repos(
            await repos_get_account_holders(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        signature__data = {}
        method__sign = {}

        for item in account_holders:
            is_success, customer = await service_soa.retrieve_customer_ref_data_mgmt(
                cif_number=item.JointAccountHolder.cif_num
            )
            # lấy full_name_vn từ cif_number
            customer_detail = customer.get('data')
            agree_author = item.JointAccountHolderAgreementAuthorization.agreement_authorization_id
            if agree_author not in signature__data:

                signature__data[agree_author] = []
                # lấy phương thức ký và flag
                method__sign[agree_author] = {
                    'method_sign': None,
                    'agreement_flag': None
                }
                # gán lại giá trị cho phương thức ký và flag
                method__sign[agree_author]['method_sign'] = item.JointAccountHolderAgreementAuthorization.method_sign
                method__sign[agree_author]['agreement_flag'] = item.JointAccountHolderAgreementAuthorization.agreement_flag
            # lấy cif_num và full_name_vn
            signature__data[agree_author].append({
                'cif_number': item.JointAccountHolder.cif_num,
                'full_name_vn': customer_detail["basic_information"]["full_name_vn"]
            })

        agreement_authorization = [
            {
                "id": item.id,
                "code": item.code,
                "name": item.name,
                "active_flag": None,
                "method_sign": None,
                'signature_list': None
            }
            for item in agreement_authorizations
        ]

        for agreement_author in agreement_authorization:
            for agree_author, signature_list in signature__data.items():
                if agreement_author['id'] == agree_author:
                    agreement_author['signature_list'] = signature_list

            for agreements_author, method_sign in method__sign.items():
                if agreement_author['id'] == agreements_author:
                    agreement_author['method_sign'] = method_sign['method_sign']
                    agreement_author['active_flag'] = method_sign['agreement_flag']

        detail_co_owner.update(agreement_authorization=agreement_authorization)

        return self.response(data=detail_co_owner)

        # query db crm
        # account_holders, list_cif_number = self.call_repos(
        #     await repos_get_list_cif_number(cif_id=cif_id, session=self.oracle_session)
        # )

        # customers_by_list_cif = self.call_repos(
        #     await repos_get_customer_by_cif_number(
        #         list_cif_number=list_cif_number,
        #         session=self.oracle_session
        #     )
        # )
        # customer_address = self.call_repos(
        #     await repos_get_customer_address(
        #         list_cif_number=list_cif_number,
        #         session=self.oracle_session
        #     ))
        #
        # # lấy data address
        # address_information = {}
        # for row in customer_address:
        #     if row.CustomerAddress.customer_id not in address_information:
        #         address_information[row.CustomerAddress.customer_id] = {
        #             "contact_address": None,
        #             "resident_address": None
        #         }
        #
        #     if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
        #         address_information[row.CustomerAddress.customer_id]["contact_address"] = row.CustomerAddress.address
        #
        #     if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
        #         address_information[row.CustomerAddress.customer_id]["resident_address"] = row.CustomerAddress.address
        #
        # # lấy data customer
        # address = None
        # signature = None
        # customer__signature = {}
        # account__holder = {}
        # for customer in customers_by_list_cif:
        #     if not customer.CustomerIndividualInfo:
        #         return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_INDIVIDUAL_INFO, loc=f'{customer.Customer.id}')
        #
        #     if not customer.CustomerIdentity:
        #         return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_IDENTITY, loc=f'{customer.Customer.id}')
        #     # # gán lại giá trị cho address
        #     for key, values in address_information.items():
        #         if customer.Customer.id == key:
        #             address = values
        #
        #     if not customer.CustomerIdentityImage:
        #         return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_IDENTITY_IMAGE, loc=f'{customer.Customer.id}')
        #     # lấy danh sách chữ ký theo từng customer_id
        #     if customer.Customer.id not in customer__signature:
        #         customer__signature[customer.Customer.id] = []
        #
        #     customer__signature[customer.Customer.id].append({
        #         "id": customer.CustomerIdentityImage.id,
        #         "image_url": customer.CustomerIdentityImage.image_url
        #     })
        #     # gán giá trị cho chứ ký
        #     for key, values in customer__signature.items():
        #         if customer.Customer.id == key:
        #             signature = values
        #
        #     if customer.Customer.id not in account__holder:
        #         account__holder[customer.Customer.id] = {
        #             "id": customer.Customer.id,
        #             "full_name_vn": customer.Customer.full_name_vn,
        #             "basic_information": {
        #                 "cif_number": customer.Customer.cif_number,
        #                 "full_name_vn": customer.Customer.full_name_vn,
        #                 "customer_relationship": dropdown(customer.CustomerRelationshipType),
        #                 "date_of_birth": customer.CustomerIndividualInfo.date_of_birth,
        #                 "gender": dropdown(customer.CustomerGender),
        #                 "nationality": dropdown(customer.AddressCountry),
        #                 "mobile_number": customer.Customer.mobile_number,
        #                 "signature": signature
        #             },
        #             "identity_document": {
        #                 "identity_number": customer.CustomerIdentity.identity_num,
        #                 "identity_type": dropdown(customer.CustomerIdentityType),
        #                 "issued_date": customer.CustomerIdentity.issued_date,
        #                 "expired_date": customer.CustomerIdentity.expired_date,
        #                 "place_of_issue": dropdown(customer.PlaceOfIssue)
        #             },
        #             "address_information": address,
        #         }
        #
        # agreement_authorizations = self.call_repos(
        #     await repos_get_agreement_authorizations(session=self.oracle_session))
        # agreement_authorization = [{
        #     "id": item.id,
        #     "code": item.code,
        #     "name": item.name,
        #     "active_flag": item.active_flag,
        # } for item in agreement_authorizations]
        #
        # return self.response(data={
        #     "joint_account_holder_flag": account_holders[0].JointAccountHolder.joint_account_holder_flag,
        #     "number_of_joint_account_holder": len(account_holders),
        #     "joint_account_holders": [customer for customer in account__holder.values()],
        #     "agreement_authorization": agreement_authorization
        # })

    async def detail_co_owner(self, cif_id: str, cif_number_need_to_find: str):

        # validate cif_number
        self.call_repos(
            await repos_validate_cif_number(cif_number=cif_number_need_to_find)
        )

        detail_co_owner = self.call_repos(
            await repos_detail_co_owner(
                cif_id=cif_id,
                cif_number_need_to_find=cif_number_need_to_find,
                session=self.oracle_session,
            )
        )

        # resident_address = None
        # contact_address = None
        #
        # for row in detail_co_owner:
        #     if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
        #         resident_address = row.CustomerAddress.address
        #     if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
        #         contact_address = row.CustomerAddress.address
        #
        # first_row = detail_co_owner[0]
        #
        # # lọc giá trị trùng chữ ký khi query
        # customer__signature = {}
        # for signature in detail_co_owner:
        #     if signature.CustomerIdentityImage.id not in customer__signature:
        #         customer__signature[signature.CustomerIdentityImage.id] = []
        #         customer__signature[signature.CustomerIdentityImage.id].append({
        #             'id': signature.CustomerIdentityImage.id,
        #             'image_url': signature.CustomerIdentityImage.image_url
        #         })
        #
        # signature = []
        # for customer_signature in customer__signature.values():
        #     signature.extend(customer_signature)

        # response_data = {
        #     "id": basic_information['cif_number'],
        #     "basic_information": basic_information,
        #     "identity_document": identity_document,
        #     "address_information": address_information
        # }
        # detail_co_owner = self.call_repos(await repos_detail_co_owner(
        #     cif_id=cif_id,
        #     cif_number_need_to_find=cif_number_need_to_find,
        #     session=self.oracle_session
        # ))
        #
        # resident_address = None
        # contact_address = None
        #
        # for row in detail_co_owner:
        #     if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
        #         resident_address = row.CustomerAddress.address
        #     if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
        #         contact_address = row.CustomerAddress.address
        #
        # first_row = detail_co_owner[0]
        #
        # # lọc giá trị trùng chữ ký khi query
        # customer__signature = {}
        # for signature in detail_co_owner:
        #     if signature.CustomerIdentityImage.id not in customer__signature:
        #         customer__signature[signature.CustomerIdentityImage.id] = []
        #         customer__signature[signature.CustomerIdentityImage.id].append({
        #             'id': signature.CustomerIdentityImage.id,
        #             'image_url': signature.CustomerIdentityImage.image_url
        #         })
        #
        # signature = []
        # for customer_signature in customer__signature.values():
        #     signature.extend(customer_signature)
        #
        # response_data = {
        #     "id": first_row.Customer.id,
        #     "basic_information": {
        #         "full_name_vn": first_row.Customer.full_name_vn,
        #         "cif_number": first_row.Customer.cif_number,
        #         "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
        #         "customer_relationship": dropdown(first_row.CustomerRelationshipType),
        #         "nationality": dropdown(first_row.AddressCountry),
        #         "gender": dropdown(first_row.CustomerGender),
        #         "mobile_number": first_row.Customer.mobile_number,
        #         "signature": signature
        #     },
        #     "identity_document": {
        #         "identity_number": first_row.CustomerIdentity.identity_num,
        #         "identity_type": dropdown(first_row.CustomerIdentityType),
        #         "issued_date": first_row.CustomerIdentity.issued_date,
        #         "expired_date": first_row.CustomerIdentity.expired_date,
        #         "place_of_issue": dropdown(first_row.PlaceOfIssue)
        #     },
        #     "address_information": {
        #         'contact_address': contact_address,
        #         'resident_address': resident_address
        #     }
        # }
        return self.response(data=detail_co_owner)
