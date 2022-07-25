from app.api.base.controller import BaseController
from app.api.v1.endpoints.ekyc.repository import (
    repos_create_ekyc_customer, repos_get_ekyc_customer,
    repos_update_ekyc_customer
)
from app.api.v1.endpoints.ekyc.schema import CreateEKYCCustomerRequest
from app.utils.functions import generate_uuid, orjson_dumps


class CtrEKYC(BaseController):
    async def ctr_create_ekyc_customer(self, request: CreateEKYCCustomerRequest):
        generate_id = generate_uuid()
        customer_ekyc_id = request.customer_id

        customer_ekyc = request.dict()
        customer_ekyc.update(
            id=generate_id,
            transaction_data=orjson_dumps(request.dict())
        )

        is_update = self.call_repos(await repos_get_ekyc_customer(
            customer_id=customer_ekyc_id, session=self.oracle_session
        ))

        if not is_update:
            self.call_repos(await repos_create_ekyc_customer(
                customer=customer_ekyc,
                session=self.oracle_session
            ))
        else:
            self.call_repos(await repos_update_ekyc_customer(
                customer=customer_ekyc,
                customer_id=customer_ekyc_id,
                session=self.oracle_session
            ))

        return self.response(data=dict(
            customer_id=customer_ekyc_id
        ))
