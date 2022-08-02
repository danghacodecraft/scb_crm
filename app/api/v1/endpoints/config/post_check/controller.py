from app.api.base.controller import BaseController
from app.utils.constant.cif import (
    APPROVE_STATUS_APPROVED, APPROVE_STATUS_PENDING, APPROVE_STATUS_REFUSE,
    POST_CHECK_TYPE, TRANSACTION_STATUS_ALL, TRANSACTION_STATUS_CANCELED,
    TRANSACTION_STATUS_FAILED, TRANSACTION_STATUS_PROCESSING,
    TRANSACTION_STATUS_REJECTED, TRANSACTION_STATUS_SUCCESS,
    TRANSACTION_STATUS_TYPE, TRANSACTION_VTM, TRANSACTIONS_TYPE,
    TRANSACTION_eKYC, TRANSACTION_LiveBank
)


class CtrPostCheck(BaseController):
    async def ctr_transaction_status(self):
        transaction_status = [
            {
                'id': TRANSACTION_STATUS_ALL,
                'code': TRANSACTION_STATUS_ALL,
                'name': TRANSACTION_STATUS_TYPE[TRANSACTION_STATUS_ALL]
            },
            {
                'id': TRANSACTION_STATUS_PROCESSING,
                'code': TRANSACTION_STATUS_PROCESSING,
                'name': TRANSACTION_STATUS_TYPE[TRANSACTION_STATUS_PROCESSING]
            },
            {
                'id': TRANSACTION_STATUS_SUCCESS,
                'code': TRANSACTION_STATUS_SUCCESS,
                'name': TRANSACTION_STATUS_TYPE[TRANSACTION_STATUS_SUCCESS]
            },
            {
                'id': TRANSACTION_STATUS_REJECTED,
                'code': TRANSACTION_STATUS_REJECTED,
                'name': TRANSACTION_STATUS_TYPE[TRANSACTION_STATUS_REJECTED]
            },
            {
                'id': TRANSACTION_STATUS_FAILED,
                'code': TRANSACTION_STATUS_FAILED,
                'name': TRANSACTION_STATUS_TYPE[TRANSACTION_STATUS_FAILED]
            },
            {
                'id': TRANSACTION_STATUS_CANCELED,
                'code': TRANSACTION_STATUS_CANCELED,
                'name': TRANSACTION_STATUS_TYPE[TRANSACTION_STATUS_CANCELED]
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
                'id': TRANSACTION_eKYC,
                'code': TRANSACTION_eKYC,
                'name': TRANSACTIONS_TYPE[TRANSACTION_eKYC]
            },
            {
                'id': TRANSACTION_VTM,
                'code': TRANSACTION_VTM,
                'name': TRANSACTIONS_TYPE[TRANSACTION_VTM]
            },
            {
                'id': TRANSACTION_LiveBank,
                'code': TRANSACTION_LiveBank,
                'name': TRANSACTIONS_TYPE[TRANSACTION_LiveBank]
            }
        ]

        return self.response(data=transaction_type)
