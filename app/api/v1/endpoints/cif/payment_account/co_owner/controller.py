from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_account_co_owner, repos_check_cif_id, repos_check_file_id,
    repos_get_casa_account, repos_get_co_owner, repos_get_co_owner_signatures,
    repos_get_file_uuid, repos_save_co_owner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_booking
from app.api.v1.endpoints.file.repository import (
    repos_check_is_exist_multi_file, repos_download_file
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.others.booking.controller import CtrBooking
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.gw import GW_REQUEST_PARAMETER_CO_OWNER
from app.utils.error_messages import (
    ERROR_ACCOUNT_ID_DOES_NOT_EXIST, ERROR_CIF_ID_DOES_NOT_EXIST,
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_DOCUMENT_ID_DOES_NOT_EXIST
)
from app.utils.functions import dropdown, generate_uuid


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, cif_id: str, co_owner: AccountHolderRequest, booking_id: str):

        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
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

        # Check exist file_id
        file_id = self.call_repos(
            await repos_check_file_id(
                file_uuid=co_owner.file_uuid,
                session=self.oracle_session))

        if not file_id:
            is_exist = self.call_repos(await repos_check_is_exist_multi_file(uuids=[co_owner.file_uuid]))
            if not is_exist:
                return self.response_exception(
                    msg='',
                    loc='file_uuid',
                    detail='Can not found file in service file'
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
            "joint_acc_agree_document_no": co_owner.document_no,
            "created_at": co_owner.create_at,
            "in_scb_flag": co_owner.address_flag,
            "joint_acc_agree_document_address": co_owner.document_address,
            "casa_account_id": casa_account,
            "joint_acc_agree_document_file_id": file_id
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

    async def ctr_co_owner(self, cif_id: str, booking_id: str):
        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_INIT_CIF,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        # Check exist cif_id
        account_id = self.call_repos(
            await repos_check_cif_id(
                cif_id=cif_id,
                session=self.oracle_session))

        if not account_id:
            return self.response_exception(
                msg=ERROR_CIF_ID_DOES_NOT_EXIST, loc=account_id
            )

        account_co_owner = self.call_repos(await repos_account_co_owner(
            account_id=account_id,
            session=self.oracle_session
        ))
        if not account_co_owner:
            return self.response_exception(
                msg=ERROR_ACCOUNT_ID_DOES_NOT_EXIST, loc=account_id
            )

        document_uuid = self.call_repos(await repos_get_file_uuid(
            document_id=account_co_owner.joint_acc_agree_document_file_id,
            session=self.oracle_session
        ))

        if not document_uuid:
            return self.response_exception(
                msg=ERROR_DOCUMENT_ID_DOES_NOT_EXIST, loc=account_co_owner.joint_acc_agree_document_file_id
            )

        document_uuids = [document_uuid]
        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_info_multi_file(uuids=document_uuids)

        account_holders, account_holder_signs = self.call_repos(
            await repos_get_co_owner(
                account_id=account_id,
                session=self.oracle_session,
            )
        )
        number_of_joint_account_holder = 0
        joint_account_holders = []
        agreement_authorizations = []
        signature_list = []
        cif_numbers = []

        for casa_account, acc_joint_acc_agree, joint_account_holder, customer_relationship_type in account_holders:
            cif_number = joint_account_holder.cif_num
            cif_numbers.append(cif_number)
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

            gender_name = basic_information["gender"]["name"]
            dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=CustomerGender, name=None, code=gender_name
            )

            nationality_name = basic_information['nationality']["name"]
            dropdown_nationality = await self.dropdown_mapping_crm_model_or_dropdown_name(
                model=AddressCountry, name=None, code=nationality_name
            )

            joint_account_holders.append(dict(
                id=joint_account_holder.joint_account_holder_id,
                basic_information=dict(
                    cif_number=joint_account_holder.cif_num,
                    customer_relationship=dropdown(customer_relationship_type),
                    full_name_vn=basic_information['full_name_vn'],
                    date_of_birth=basic_information['date_of_birth'],
                    gender=dropdown_gender,
                    nationality=dropdown_nationality,
                    mobile_number=basic_information['mobile_number'],
                    signature=[]
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
            ))

            number_of_joint_account_holder += 1
            for _, joint_acc_agree_id, method_sign, agreement_authorization in account_holder_signs:
                if acc_joint_acc_agree.joint_acc_agree_id == joint_acc_agree_id:
                    agreement_authorizations.append(dict(
                        id=agreement_authorization.id,
                        code=agreement_authorization.code,
                        name=agreement_authorization.name,
                        agreement_flag=agreement_authorization.active_flag,
                        method_sign=method_sign.method_sign_type,
                        signature_list=[]
                    ))
                    agree_join_acc = dict(
                        cif_number=method_sign.agree_join_acc_cif_num,
                        full_name_vn=method_sign.agree_join_acc_name,
                    )
                    if agree_join_acc not in signature_list:
                        signature_list.append(agree_join_acc)

        signatures = self.call_repos(await repos_get_co_owner_signatures(
            cif_numbers=cif_numbers, session=self.oracle_session))

        for idx, (_, _, joint_account_holder, _) in enumerate(account_holders):
            for signature in signatures:
                if joint_account_holder.cif_num == signature.cif_number:
                    image_info = self.call_repos(await repos_download_file(signature.image_url))
                    joint_account_holders[idx]['basic_information']['signature'].append(dict(
                        id=signature.id,
                        image_url=image_info['file_url']
                    ))
            if agreement_authorizations[idx]['method_sign'] == 3:
                agreement_authorizations[idx]["signature_list"] = signature_list

        response_data = dict(
            joint_account_holder_flag=account_co_owner.active_flag,
            document_no=account_co_owner.joint_acc_agree_document_no,
            created_at=account_co_owner.created_at,
            address_flag=account_co_owner.in_scb_flag,
            document_address=account_co_owner.joint_acc_agree_document_address,
            file_uuid=uuid__link_downloads[document_uuid],

            number_of_joint_account_holder=number_of_joint_account_holder,
            joint_account_holders=joint_account_holders,
            agreement_authorization=agreement_authorizations
        )
        return self.response(data=response_data)
