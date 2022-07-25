from app.api.base.controller import BaseController
from app.api.v1.endpoints.ekyc.repository import repos_create_ekyc_customer
from app.api.v1.endpoints.ekyc.schema import CreateEKYCCustomerRequest
from app.utils.functions import generate_uuid, orjson_dumps


class CtrEKYC(BaseController):
    async def ctr_create_ekyc_customer(self, request: CreateEKYCCustomerRequest):
        generate_id = generate_uuid()
        customer_ekyc_id = request.customer_id

        # status_id = request.status_id
        # # if status_id not in EKYC_CUSTOMER_STATUS:
        # #     self.response_exception(msg=f"status_id must be in {EKYC_CUSTOMER_STATUS}")
        #
        # kss_status_id = request.kss_status_id
        # if kss_status_id not in EKYC_CUSTOMER_KSS_STATUS:
        #     self.response_exception(msg=f"kss_status_id must be in {EKYC_CUSTOMER_KSS_STATUS}")
        #
        # approve_status_id = request.approve_status_id
        # if approve_status_id not in EKYC_CUSTOMER_APPROVE_STATUS:
        #     self.response_exception(msg=f"approve_status_id must be in {EKYC_CUSTOMER_APPROVE_STATUS}")

        # customer_ekyc = dict(
        #     id=generate_id,
        #     customer_id=request.customer_id,
        #     transaction_id=request.transaction_id,
        #     full_name=request.full_name,
        #     cif=request.cif,
        #     phone_number=request.phone_number,
        #     document_id=request.document_id,
        #     document_type=request.document_type,
        #     status=EKYC_CUSTOMER_STATUS[status_id],
        #     status_id=status_id,
        #     trans_date=request.trans_date,
        #     ekyc_step=request.ekyc_step,
        #     kss_status=EKYC_CUSTOMER_KSS_STATUS[kss_status_id],
        #     kss_status_id=kss_status_id,
        #     date_kss=request.date_kss,
        #     user_kss=request.user_kss,
        #     approve_status=EKYC_CUSTOMER_APPROVE_STATUS[approve_status_id],
        #     approve_status_id=approve_status_id,
        #     date_approve=request.date_approve,
        #     user_approve=request.user_approve,
        #     transaction_data=request.json(),
        #     created_date=request.created_date,
        #     updated_date=request.updated_date
        # )
        customer_ekyc = request.dict()
        customer_ekyc.update(
            id=generate_id,
            transaction_data=orjson_dumps(request.dict())
        )
        self.call_repos(await repos_create_ekyc_customer(
            customer=customer_ekyc,
            session=self.oracle_session
        ))
        return self.response(data=dict(
            id=generate_id,
            customer_ekyc_id=customer_ekyc_id
        ))
