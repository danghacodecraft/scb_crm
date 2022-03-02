from app.api.base.controller import BaseController
from app.utils.constant.cif import (
    APPROVE_STATUS_APPROVED, APPROVE_STATUS_PENDING, APPROVE_STATUS_REFUSE,
    POST_CHECK_TYPE, TRANSACTION_CIF, TRANSACTION_STATUS_FALSE,
    TRANSACTION_STATUS_TRUE, TRANSACTIONS_TYPE
)


class CtrPostCheck(BaseController):
    async def ctr_transaction_status(self):
        transaction_status = [
            {
                'id': TRANSACTION_STATUS_FALSE,
                'code': TRANSACTION_STATUS_FALSE,
                'name': POST_CHECK_TYPE[TRANSACTION_STATUS_FALSE]
            },
            {
                'id': TRANSACTION_STATUS_TRUE,
                'code': TRANSACTION_STATUS_TRUE,
                'name': POST_CHECK_TYPE[TRANSACTION_STATUS_TRUE]
            }
        ]
        return self.response(data=transaction_status)

    async def ctr_approve_status(self):
        approve_status = [
            {
                'id': APPROVE_STATUS_PENDING,
                'code': APPROVE_STATUS_PENDING,
                'name': POST_CHECK_TYPE[APPROVE_STATUS_PENDING]
            },
            {
                'id': APPROVE_STATUS_APPROVED,
                'code': APPROVE_STATUS_APPROVED,
                'name': POST_CHECK_TYPE[APPROVE_STATUS_APPROVED]
            },
            {
                'id': APPROVE_STATUS_REFUSE,
                'code': APPROVE_STATUS_REFUSE,
                'name': POST_CHECK_TYPE[APPROVE_STATUS_REFUSE]
            }
        ]
        return self.response(data=approve_status)

    async def ctr_transaction_type(self):
        transaction_type = [
            {
                'id': TRANSACTION_CIF,
                'code': TRANSACTION_CIF,
                'name': TRANSACTIONS_TYPE[TRANSACTION_CIF]
            }
        ]

        return self.response(data=transaction_type)