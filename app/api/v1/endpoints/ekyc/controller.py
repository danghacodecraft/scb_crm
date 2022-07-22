from app.api.base.controller import BaseController
from app.api.v1.endpoints.ekyc.repository import repos_create_ekyc_customer
from app.api.v1.endpoints.ekyc.schema import CreateEKYCCustomerRequest
from app.utils.constant.ekyc import (
    EKYC_CUSTOMER_APPROVE_STATUS, EKYC_CUSTOMER_KSS_STATUS,
    EKYC_CUSTOMER_STATUS
)
from app.utils.functions import generate_uuid, now


class CtrEKYC(BaseController):
    async def ctr_create_ekyc_customer(self, request: CreateEKYCCustomerRequest):
        generate_id = generate_uuid()
        customer_ekyc_id = request.customer_id

        status_id = request.status_id
        # if status_id not in EKYC_CUSTOMER_STATUS:
        #     self.response_exception(msg=f"status_id must be in {EKYC_CUSTOMER_STATUS}")

        kss_status_id = request.kss_status_id
        if kss_status_id not in EKYC_CUSTOMER_KSS_STATUS:
            self.response_exception(msg=f"kss_status_id must be in {EKYC_CUSTOMER_STATUS}")

        approve_status_id = request.approve_status_id
        if approve_status_id not in EKYC_CUSTOMER_APPROVE_STATUS:
            self.response_exception(msg=f"approve_status_id must be in {EKYC_CUSTOMER_STATUS}")

        customer_ekyc = dict(
            id=generate_id,
            customer_id=customer_ekyc_id,
            transaction_id=request.transaction_id,
            full_name=request.full_name,
            cif=request.cif,
            phone_number=request.phone_number,
            document_id=request.document_id,
            document_type=request.document_type,
            status=EKYC_CUSTOMER_STATUS[status_id],
            status_id=status_id,
            trans_date=request.trans_date,
            ekyc_step=request.ekyc_step,
            kss_status=EKYC_CUSTOMER_KSS_STATUS[kss_status_id],
            kss_status_id=kss_status_id,
            date_kss=None,
            user_kss=None,
            approve_status=EKYC_CUSTOMER_APPROVE_STATUS[approve_status_id],
            approve_status_id=approve_status_id,
            date_approve=None,
            user_approve=None,
            transaction_data=request.json(),
            created_date=now(),
            updated_date=None
        )
        self.call_repos(await repos_create_ekyc_customer(
            customer=customer_ekyc,
            session=self.oracle_session
        ))
        return self.response(data=dict(
            id=generate_id,
            customer_ekyc_id=customer_ekyc_id
        ))
