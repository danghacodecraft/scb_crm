import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount, JointAccountHolder, JointAccountHolderAgreementAuthorization,
    MethodSign
)
from app.utils.constant.cif import BUSINESS_FORM_TKTT_DSH
from app.utils.error_messages import ERROR_CASA_ACCOUNT_ID_NOT_EXIST
from app.utils.functions import now


async def repos_check_casa_account(account_id: str, session: Session) -> ReposReturn:
    casa_account = session.execute(
        select(CasaAccount.id).filter(CasaAccount.id == account_id)
    ).scalar()

    if not casa_account:
        return ReposReturn(
            is_error=True, msg=ERROR_CASA_ACCOUNT_ID_NOT_EXIST, loc=f"account_id: {account_id}"
        )
    return ReposReturn(data=casa_account)


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
