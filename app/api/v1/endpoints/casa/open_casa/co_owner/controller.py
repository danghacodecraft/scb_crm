from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.co_owner.repository import (
    repos_check_casa_account, repos_save_co_owner
)
from app.api.v1.endpoints.casa.open_casa.co_owner.schema import (
    AccountHolderRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_booking_account
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import (
    BUSINESS_TYPE_INIT_CIF, BUSINESS_TYPE_OPEN_CASA
)
from app.utils.error_messages import (
    ERROR_CASA_ACCOUNT_ID_NOT_EXIST, ERROR_CIF_NUMBER_NOT_EXIST
)
from app.utils.functions import generate_uuid


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, account_id: str, co_owner: AccountHolderRequest, booking_id: str):

        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_OPEN_CASA,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_INIT_CIF}"
        )

        current_user = self.current_user.user_info
        # Check exist casa_account_id
        account_id = self.call_repos(
            await repos_check_casa_account(
                account_id=account_id,
                session=self.oracle_session))

        if not account_id:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_ID_NOT_EXIST, loc=account_id
            )

        # Lấy danh sách cif_number account request
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
            "joint_acc_agree_document_no": co_owner.document_no,
            "in_scb_flag": co_owner.address_flag,
            "joint_acc_agree_document_address": co_owner.document_address,
            "casa_account_id": account_id,
            "joint_acc_agree_document_file_id": co_owner.file_uuid
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
                account_id=account_id,
                log_data=co_owner.json(),
                created_by=current_user.username,
                session=self.oracle_session
            )
        )

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking_account(
            account_id=account_id, session=self.oracle_session
        ))
        co_owner_data.update(booking=dict(
            id=booking.id,
            code=booking.code
        ))

        return self.response(data=co_owner_data)
