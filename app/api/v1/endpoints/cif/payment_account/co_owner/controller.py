from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_detail_co_owner, repos_get_casa_account, repos_get_co_owner,
    repos_save_co_owner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking, repos_validate_cif_number
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.gw import GW_REQUEST_PARAMETER_CO_OWNER
from app.utils.error_messages import ERROR_CIF_NUMBER_NOT_EXIST
from app.utils.functions import dropdown, generate_uuid


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, cif_id: str, co_owner: AccountHolderRequest, booking_id: str):

        # Check exist Booking
        await CtrBooking().ctr_get_booking(
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        current_user = self.current_user.user_info
        # lấy casa_account_id theo số cif_id
        casa_account = self.call_repos(
            await repos_get_casa_account(cif_id=cif_id, session=self.oracle_session)
        )

        # lấy danh sách cif_number account request
        customer_relationship_not_exist_list = []
        for index, joint_account_holder in enumerate(co_owner.joint_account_holders):
            cif_number = joint_account_holder.cif_number

            is_existed = await CtrGWCustomer(current_user=self.current_user).ctr_gw_check_exist_customer_detail_info(
                cif_number=cif_number
            )

            if not is_existed:
                return self.response_exception(
                    msg=ERROR_CIF_NUMBER_NOT_EXIST, loc=f"joint_account_holders -> cif_number : {cif_number}"
                )
            customer_relationship_not_exist_list.append(joint_account_holder.customer_relationship.id)

        uuid = generate_uuid()
        save_info_co_owner = {
            "active_flag": co_owner.joint_account_holder_flag,
            "joint_acc_agree_id": uuid,
            "created_at": co_owner.create_at,
            "in_scb_flag": co_owner.address_flag,
            "casa_account_id": casa_account,
            "document_file_id": co_owner.file_uuid
        }

        save_account_holder = [{
            "joint_account_holder_id": generate_uuid(),
            "cif_num": item.cif_number,
            "relationship_type_id": item.customer_relationship.id,
            "joint_acc_agree_id": uuid,
            "created_at": co_owner.create_at
        } for item in co_owner.joint_account_holders]
        save_agreement_authorization = []
        for agreement_authorization in co_owner.agreement_authorization:
            for signature_item in agreement_authorization.signature_list:
                save_agreement_authorization.append({
                    "agreement_author_id": agreement_authorization.agreement_author_id,
                    "joint_acc_agree_id": uuid,
                    "created_at": co_owner.create_at,
                    "agreement_flag": agreement_authorization.agreement_flag,
                    "method_sign_type": agreement_authorization.method_sign,
                    "agree_join_acc_cif_num": signature_item.cif_number,
                    "agree_join_acc_name": signature_item.full_name_vn
                })

        co_owner_data = self.call_repos(
            await repos_save_co_owner(
                save_info_co_owner=save_info_co_owner,
                save_account_holder=save_account_holder,
                save_agreement_authorization=save_agreement_authorization,
                cif_id=cif_id,
                log_data=co_owner.json(),
                created_by=current_user.username,
                session=self.oracle_session
            )
        )

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        co_owner_data.update(booking=dict(
            id=booking.id,
            code=booking.code
        ))

        return self.response(data=co_owner_data)

    async def ctr_co_owner(self, cif_id: str):
        detail_co_owner = self.call_repos(
            await repos_get_co_owner(
                cif_id=cif_id,
                session=self.oracle_session,
            )
        )
        joint_account_holder_flag = False
        number_of_joint_account_holder = 0
        joint_account_holders = []

        for casa_account, joint_account_holder, customer_relationship_type in detail_co_owner:
            cif_number = joint_account_holder.cif_num

            data = await CtrGWCustomer(current_user=self.current_user).ctr_gw_get_customer_info_detail(
                cif_number=cif_number,
                parameter=GW_REQUEST_PARAMETER_CO_OWNER
            )

            gw_data = data['data']
            identity_document = gw_data['identity_document']
            identity_number = identity_document['identity_number']
            issued_date = identity_document['issued_date']
            expired_date = identity_document['expired_date']
            place_of_issue = identity_document['place_of_issue']

            basic_information = gw_data['basic_information']
            address_information = gw_data['address_information']

            joint_account_holders.append(dict(
                id=cif_number,
                basic_information=dict(
                    cif_number=cif_number,
                    customer_relationship=dropdown(customer_relationship_type),
                    full_name_vn=basic_information['full_name_vn'],
                    date_of_birth=basic_information['date_of_birth'],
                    gender=basic_information['gender'],
                    nationality=basic_information['nationality'],
                    mobile_number=basic_information['mobile_number'],
                    signature=None
                ),
                identity_document=dict(
                    identity_number=identity_number,
                    issued_date=issued_date,
                    expired_date=expired_date,
                    place_of_issue=place_of_issue,
                ),
                address_information=dict(
                    contact_address=address_information['contact_address'].strip(" "),
                    resident_address=address_information['resident_address'].strip(" ")
                ),
                avatar_url=None
            ))
            number_of_joint_account_holder += 1

        response_data = dict(
            joint_account_holder_flag=joint_account_holder_flag,
            number_of_joint_account_holder=number_of_joint_account_holder,
            joint_account_holders=joint_account_holders,
            # agreement_authorization=agreement_authorization
        )

        return self.response(data=response_data)

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
