from app.api.base.controller import BaseController
from app.api.v1.others.statement.repository import repos_get_denominations


class CtrStatement(BaseController):
    async def ctr_statement_info(self, statement_request):
        statement = {}
        statement_info = self.call_repos(await repos_get_denominations(currency_id="VND", session=self.oracle_session))

        for item in statement_info:
            statement.update({
                str(int(item.denominations)): 0
            })

        for row in statement_request:
            statement.update({row['denominations']: row['amount']})

        statements = []
        total_amount = 0
        total_number_of_bills = 0
        for denominations, amount in statement.items():
            into_money = int(denominations) * amount
            statements.append(dict(
                denominations=denominations,
                amount=amount,
                into_money=into_money
            ))
            total_number_of_bills += amount
            total_amount += into_money

        statement_response = dict(
            total_number_of_bills=total_number_of_bills,
            statements=statements,
            total=total_amount,
        )
        return statement_response
