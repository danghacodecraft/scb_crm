from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.close_casa.repository import (
    repos_save_casa_account
)
from app.api.v1.endpoints.casa.close_casa.schema import CloseCasaRequest


class CtrCloseCasa(BaseController):
    async def ctr_close_casa(
            self,
            close_casa_request: CloseCasaRequest,
            booking_id: str,
    ):
        # Kiểm tra booking
        # await CtrBooking().ctr_get_booking_and_validate(
        #     booking_id=BOOKING_ID,
        #     business_type_code=BUSINESS_TYPE_CLOSE_CASA,
        #     check_correct_booking_flag=False,
        #     loc=f'booking_id: {BOOKING_ID}'
        # )

        account_list = []

        for account in close_casa_request.account_list:
            account_list_info = dict(
                account_num=account.account_num,
                content=account.content
            )
            account_list.append(account_list_info)

        receipt_type_original_currency = close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.receipt_type,
        amount_money_original_currency = close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.amount_money,
        content_original_currency = close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.content,
        account_no_original_currency = close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.account_no,
        type_original_currency = close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.type.id,
        form_of_receipt_original_currency = close_casa_request.transaction_fee_payment_info.source_of_money.original_currency. \
            form_of_receipt.id

        amount_money = close_casa_request.transaction_fee_payment_info.source_of_money.sell_foreign_currency_to_SCB.amount_money
        buying_rate = close_casa_request.transaction_fee_payment_info.source_of_money.sell_foreign_currency_to_SCB.buying_rate
        amount = amount_money * buying_rate,
        reciprocal_rate = close_casa_request.transaction_fee_payment_info.source_of_money.sell_foreign_currency_to_SCB.reciprocal_rate
        content = close_casa_request.transaction_fee_payment_info.source_of_money.sell_foreign_currency_to_SCB.content
        form_of_receipt = close_casa_request.transaction_fee_payment_info.source_of_money.sell_foreign_currency_to_SCB. \
            form_of_receipt.id

        transaction_fee_payment_info = dict( # noqa
            source_of_money=dict(
                flag_original_currency=close_casa_request.transaction_fee_payment_info.source_of_money.flag_original_currency,
                original_currency=dict(
                    receipt_type=receipt_type_original_currency,
                    amount_money=amount_money_original_currency,
                    content=content_original_currency,
                    account_no=account_no_original_currency,
                    type=type_original_currency,
                    form_of_receipt=form_of_receipt_original_currency
                ),
                flag_sell_foreign_currency=close_casa_request.transaction_fee_payment_info.source_of_money.flag_sell_foreign_currency,
                sell_foreign_currency_to_SCB=dict(
                    amount_money=amount_money,
                    buying_rate=buying_rate,
                    reciprocal_rate=reciprocal_rate,
                    amount=amount,
                    content=content,
                    form_of_receipt=form_of_receipt,
                    actual_amount_spent=amount
                )
            )
        )

        current_user_info = self.current_user.user_info  # noqa

        # if close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.receipt_type == "CASA":
        #     if not close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.type:
        #         self.response_exception(loc='', detail='Transfer type not null')
        #     if not close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.form_of_receipt:
        #         self.response_exception(loc='', detail='Form of receipt not null')
        #     if not close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.account_no:
        #         self.response_exception(loc='', detail='Account_no not null')
        #
        #     p_blk_closure = [dict(
        #         close_mode=close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.receipt_type,
        #         account_no=close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.account_no
        #     )]
        #
        #     request = {}
        #     for index, account in enumerate(close_casa_request.account_list):
        #         request.update(
        #             account_info=dict(
        #                 account_num=account.account_num
        #             ),
        #             p_blk_closure=p_blk_closure
        #
        #         )
        # await CtrGWCasaAccount(current_user=self.current_user).ctr_gw_get_close_casa_account(request)
        # else:
        #     p_blk_closure = [dict(
        #         close_mode=close_casa_request.transaction_fee_payment_info.source_of_money.original_currency.receipt_type
        #     )]
        #     request = {}
        #     for index, account in enumerate(close_casa_request.account_list):
        #         request.update(
        #             account_info=dict(
        #                 account_num=account.account_num,
        #                 p_blk_closure=p_blk_closure
        #             )
        #         )
        #     await CtrGWCasaAccount(current_user=self.current_user).ctr_gw_get_close_casa_account(request)

        saving_casa_accounts = self.call_repos(await repos_save_casa_account(
            booking_id=booking_id,
            request_json=close_casa_request.json(),
            session=self.oracle_session
        ))

        # return self.response(data=dict(
        #     account_num=request['account_info']['account_num'],
        #     booking_id=BOOKING_ID,
        #     booking_type=booking_type
        # ))

        return self.response(data=saving_casa_accounts)
