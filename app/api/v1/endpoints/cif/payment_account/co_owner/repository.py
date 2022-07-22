import json
from typing import List

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    AgreementAuthorization, CasaAccount, JointAccountHolder,
    JointAccountHolderAgreementAuthorization, MethodSign
)
from app.third_parties.oracle.models.document_file.model import DocumentFile
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.cif import (
    AGREEMENT_AUTHOR_TYPE_DD, BUSINESS_FORM_TKTT_DSH, IMAGE_TYPE_SIGNATURE
)
from app.utils.error_messages import (
    ERROR_ACCOUNT_ID_DOES_NOT_EXIST, ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_DOCUMENT_ID_DOES_NOT_EXIST,
    ERROR_NO_DATA
)
from app.utils.functions import now


async def repos_get_co_owner(account_id: str, session: Session) -> ReposReturn:
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
        .filter(CasaAccount.id == account_id)
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
        .filter(CasaAccount.id == account_id)
    ).all()

    return ReposReturn(data=(account_holders, account_holder_signs))


async def repos_payment_account_co_owner(cif_id: str, session: Session):
    co_owner = session.execute(
        select(
            JointAccountHolderAgreementAuthorization
        )
        .join(JointAccountHolder,
              JointAccountHolderAgreementAuthorization.joint_acc_agree_id == JointAccountHolder.joint_acc_agree_id)
        .join(Customer,
              JointAccountHolder.cif_num == Customer.cif_number)
        .filter(Customer.id == cif_id)
    ).scalar()

    if not co_owner:
        return ReposReturn(
            loc="account_id_does_not_exit",
            msg=ERROR_ACCOUNT_ID_DOES_NOT_EXIST,
            detail=co_owner
        )

    return ReposReturn(data=co_owner)


async def repos_get_file_uuid(document_id: str, session: Session):
    get_uuid = session.execute(
        select(
            DocumentFile.file_uuid
        ).filter(DocumentFile.id == document_id)
    ).scalar()

    if not get_uuid:
        return ReposReturn(
            loc="document_id_does_not_exit",
            msg=ERROR_DOCUMENT_ID_DOES_NOT_EXIST,
            detail=get_uuid
        )

    return ReposReturn(data=get_uuid)


async def repos_get_co_owner_signatures(cif_numbers: List, session: Session) -> ReposReturn:
    signatures = session.execute(
        select(
            Customer.cif_number,
            CustomerIdentityImage.id,
            CustomerIdentityImage.image_url
        )
        .join(CustomerIdentity, CustomerIdentityImage.identity_id == CustomerIdentity.id)
        .join(Customer, CustomerIdentity.customer_id == Customer.id)
        .filter(and_(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_SIGNATURE,
            Customer.cif_number.in_(tuple(set(cif_numbers)))
        ))
    ).all()

    return ReposReturn(data=signatures)


async def repos_get_casa_account(cif_id: str, session: Session) -> ReposReturn:
    casa_account = session.execute(
        select(CasaAccount.id).filter(CasaAccount.customer_id == cif_id)
    ).scalar()
    if not casa_account:
        return ReposReturn(
            is_error=True, msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc=f"cif_id: {cif_id}"
        )
    return ReposReturn(data=casa_account)


async def repos_check_acc_agree(account_id: str, session: Session) -> ReposReturn:
    acc_agree_info = session.execute(
        select(JointAccountHolderAgreementAuthorization)
        .filter(JointAccountHolderAgreementAuthorization.casa_account_id == account_id)
    ).scalar()

    if acc_agree_info:
        session.execute(delete(JointAccountHolderAgreementAuthorization).filter(
            JointAccountHolderAgreementAuthorization.casa_account_id == account_id))

        session.execute(delete(JointAccountHolder).filter(
            JointAccountHolder.joint_acc_agree_id == acc_agree_info.joint_acc_agree_id))

        session.execute(delete(MethodSign).filter(
            MethodSign.joint_acc_agree_id == acc_agree_info.joint_acc_agree_id))

    return ReposReturn(data=acc_agree_info)


async def repos_check_file_id(file_uuid: str, session: Session) -> ReposReturn:
    file_uuid_info = session.execute(
        select(DocumentFile.id).filter(DocumentFile.file_uuid == file_uuid)
    ).scalar()

    return ReposReturn(data=file_uuid_info)


@auto_commit
async def repos_save_co_owner(
        save_info_co_owner,
        save_account_holder,
        save_agreement_authorization,
        cif_id: str,
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
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TKTT_DSH,
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(
        data={"cif_id": cif_id, "created_at": now(), "created_by": created_by}
    )


async def repos_check_cif_id(cif_id: str, session: Session):
    account_co_owner = session.execute(
        select(
            CasaAccount.id,
        ).filter(CasaAccount.customer_id == cif_id)
    ).scalar()

    if not account_co_owner:
        return ReposReturn(
            loc="account_id_does_not_exit",
            msg=ERROR_ACCOUNT_ID_DOES_NOT_EXIST,
            detail=account_co_owner
        )

    return ReposReturn(data=account_co_owner)


async def repos_account_co_owner(account_id: str, session: Session):
    account_co_owner = session.execute(
        select(
            JointAccountHolderAgreementAuthorization
        ).filter(JointAccountHolderAgreementAuthorization.casa_account_id == account_id)
    ).scalars().all()

    if not account_co_owner:
        return ReposReturn(
            loc="account_id_does_not_exit",
            msg=ERROR_ACCOUNT_ID_DOES_NOT_EXIST,
            detail=account_co_owner
        )

    return ReposReturn(data=account_co_owner)


async def repos_acc_agree_info(document_no: str, session: Session):
    acc_agree_info = session.execute(
        select(
            JointAccountHolderAgreementAuthorization
        ).filter(JointAccountHolderAgreementAuthorization.joint_acc_agree_document_no == document_no)
    ).scalars().all()

    return ReposReturn(data=acc_agree_info)


async def repos_get_list_cif_number(cif_id: str, session: Session):
    # lấy dữ liệu các đồng sở hữu của tài khoản thanh toán theo cif_id
    account_holders = session.execute(
        select(JointAccountHolder)
        .join(CasaAccount, CasaAccount.id == JointAccountHolder.casa_account_id)
        .filter(CasaAccount.customer_id == cif_id)
    ).all()

    # check account_holder
    if not account_holders:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc="cif_id")

    # lấy list cif_number trong account_holder
    list_cif_number = []
    for account_holder in account_holders:
        list_cif_number.append(account_holder.JointAccountHolder.cif_num)

    return ReposReturn(data=(account_holders, list_cif_number))


async def repos_get_customer_address(
        list_cif_number: List[str], session: Session
) -> ReposReturn:
    customer_address = session.execute(
        select(
            CustomerAddress,
        )
        .join(Customer, CustomerAddress.customer_id == Customer.id)
        .filter(Customer.cif_number.in_(list_cif_number))
    ).all()

    return ReposReturn(data=customer_address)


async def repos_get_agreement_authorizations(session: Session) -> ReposReturn:
    agreement_authorizations = session.execute(
        select(AgreementAuthorization).filter(
            AgreementAuthorization.agreement_author_type == AGREEMENT_AUTHOR_TYPE_DD
        )
    ).scalars()

    if not agreement_authorizations:
        return ReposReturn(
            is_error=True,
            msg=ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST,
            loc="agreement_authorizations",
        )

    return ReposReturn(data=agreement_authorizations)


async def repos_get_account_holders(cif_id: str, session: Session) -> ReposReturn:
    casa_account_holder = session.execute(
        select(
            JointAccountHolder,
            JointAccountHolderAgreementAuthorization,
            AgreementAuthorization
        )
        .join(CasaAccount, JointAccountHolder.casa_account_id == CasaAccount.id)
        .join(
            JointAccountHolderAgreementAuthorization,
            JointAccountHolder.id == JointAccountHolderAgreementAuthorization.joint_account_holder_id
        )
        .join(AgreementAuthorization,
              JointAccountHolderAgreementAuthorization.agreement_authorization_id == AgreementAuthorization.id)
        .filter(CasaAccount.customer_id == cif_id)
    ).all()

    return ReposReturn(data=casa_account_holder)
