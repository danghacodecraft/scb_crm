import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import Booking
from app.third_parties.oracle.models.cif.payment_account.model import (
    AgreementAuthorization, CasaAccount, JointAccountHolder,
    JointAccountHolderAgreementAuthorization, MethodSign
)
from app.third_parties.oracle.models.document_file.model import DocumentFile
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.business_type import BUSINESS_TYPE_OPEN_CASA
from app.utils.constant.cif import BUSINESS_FORM_TKTT_DSH, IMAGE_TYPE_SIGNATURE
from app.utils.error_messages import ERROR_CASA_ACCOUNT_ID_DOES_NOT_EXIST
from app.utils.functions import now


async def ctr_get_booking_parent(booking_id, session: Session) -> ReposReturn:
    booking_parent = session.execute(
        select(Booking).filter(
            Booking.parent_id == booking_id,
            Booking.business_type_id == BUSINESS_TYPE_OPEN_CASA
        )
    ).scalar()

    return ReposReturn(data=booking_parent)


async def repos_check_casa_account(account_id: str, session: Session) -> ReposReturn:
    casa_account = session.execute(
        select(CasaAccount.id).filter(CasaAccount.id == account_id)
    ).scalar()

    if not casa_account:
        return ReposReturn(
            is_error=True, msg=ERROR_CASA_ACCOUNT_ID_DOES_NOT_EXIST, loc=f"account_id: {account_id}"
        )
    return ReposReturn(data=casa_account)


async def repos_check_file_id(file_uuid: str, session: Session) -> ReposReturn:
    file_uuid_info = session.execute(
        select(DocumentFile.id).filter(DocumentFile.file_uuid == file_uuid)
    ).scalar()

    return ReposReturn(data=file_uuid_info)


async def repos_acc_agree_info(document_no: str, session: Session) -> ReposReturn:
    casa_account_info = session.execute(
        select(JointAccountHolderAgreementAuthorization.casa_account_id)
        .filter(JointAccountHolderAgreementAuthorization.joint_acc_agree_document_no == document_no)
    ).scalar()

    return ReposReturn(data=casa_account_info)


async def repos_acc_agree_get_file(document_no: str, session: Session) -> ReposReturn:
    file_info = session.execute(
        select(JointAccountHolderAgreementAuthorization.joint_acc_agree_document_file_id)
        .filter(JointAccountHolderAgreementAuthorization.joint_acc_agree_document_no == document_no)
    ).scalars().all()

    return ReposReturn(data=file_info)


@auto_commit
async def repos_save_co_owner(
        save_info_co_owner,
        save_account_holder,
        save_agreement_authorization,
        account_id: str,
        log_data: json,
        created_by: str,
        session: Session
) -> ReposReturn:
    session.add(JointAccountHolderAgreementAuthorization(**save_info_co_owner))
    session.bulk_save_objects(
        JointAccountHolder(**account_holder)
        for account_holder in save_account_holder
    )

    session.bulk_save_objects(
        MethodSign(**agreement_authorization)
        for agreement_authorization in save_agreement_authorization
    )

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        account_id=account_id,
        business_form_id=BUSINESS_FORM_TKTT_DSH,
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(
        data={"account_id": account_id, "created_at": now(), "created_by": created_by}
    )


async def repos_get_co_owner(account_id: str, document_no: str, session: Session) -> ReposReturn:
    account_holders = session.execute(
        select(
            CasaAccount,
            JointAccountHolderAgreementAuthorization,
            JointAccountHolder,
            CustomerRelationshipType
        ).join(JointAccountHolderAgreementAuthorization,
               CasaAccount.id == JointAccountHolderAgreementAuthorization.casa_account_id)
        .join(JointAccountHolder,
              JointAccountHolderAgreementAuthorization.joint_acc_agree_id == JointAccountHolder.joint_acc_agree_id)
        .join(CustomerRelationshipType, JointAccountHolder.relationship_type_id == CustomerRelationshipType.id)
        .filter(CasaAccount.id == account_id,
                JointAccountHolderAgreementAuthorization.joint_acc_agree_document_no == document_no)
    ).all()

    account_holder_signs = session.execute(
        select(
            CasaAccount,
            JointAccountHolderAgreementAuthorization.joint_acc_agree_id,
            MethodSign,
            AgreementAuthorization,
        ).join(JointAccountHolderAgreementAuthorization,
               CasaAccount.id == JointAccountHolderAgreementAuthorization.casa_account_id)
        .join(MethodSign,
              JointAccountHolderAgreementAuthorization.joint_acc_agree_id == MethodSign.joint_acc_agree_id)
        .join(AgreementAuthorization, MethodSign.agreement_author_id == AgreementAuthorization.id)
        .filter(CasaAccount.id == account_id,
                JointAccountHolderAgreementAuthorization.joint_acc_agree_document_no == document_no
                )).all()

    return ReposReturn(data=(account_holders, account_holder_signs))


async def repos_account_co_owner(account_id: str, session: Session):
    account_co_owner = session.execute(
        select(
            JointAccountHolderAgreementAuthorization
        ).filter(JointAccountHolderAgreementAuthorization.casa_account_id == account_id)
    ).scalars().all()

    return ReposReturn(data=account_co_owner)


async def repos_get_uuid(document_id: str, session: Session):
    get_uuid = session.execute(
        select(
            DocumentFile.file_uuid
        ).filter(DocumentFile.id == document_id)
    ).scalar()

    return ReposReturn(data=get_uuid)


async def repos_get_co_owner_signature(cif_number: str, session: Session) -> ReposReturn:
    signatures = session.execute(
        select(
            Customer.cif_number,
            CustomerIdentityImage.id,
            CustomerIdentityImage.image_url
        ).join(CustomerIdentity, CustomerIdentityImage.identity_id == CustomerIdentity.id)
        .join(Customer, CustomerIdentity.customer_id == Customer.id)
        .filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_SIGNATURE,
            Customer.cif_number == cif_number
        )
    ).all()

    return ReposReturn(data=signatures)
