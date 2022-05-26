from datetime import date

from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.repository import (
    repos_accounting_entry, repos_branch, repos_count_total_item,
    repos_get_customer, repos_get_total_item, repos_get_transaction_list,
    repos_region, repos_get_senders
)
from app.utils.constant.cif import CIF_STAGE_ROLE_CODE_TELLER, CIF_STAGE_ROLE_CODES, CIF_STAGE_ROLE_CODE_SUPERVISOR, \
    CIF_STAGE_ROLE_CODE_AUDIT
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import dropdown


class CtrDashboard(BaseController):
    async def ctr_get_transaction_list(self, region_id: str, branch_id: str, transaction_type_id: str,
                                       status_code: str, search_box: str, from_date: date, to_date: date):
        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        transaction_list = self.call_repos(await repos_get_transaction_list(
            region_id=region_id,
            branch_id=branch_id,
            transaction_type_id=transaction_type_id,
            status_code=status_code,
            search_box=search_box,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            page=current_page,
            session=self.oracle_session
        ))

        total_item = self.call_repos(await repos_count_total_item(
            region_id=region_id, branch_id=branch_id, transaction_type_id=transaction_type_id, status_code=status_code,
            search_box=search_box, from_date=from_date, to_date=to_date, session=self.oracle_session))

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        mapping_datas = {}
        booking_ids = []

        for transaction in transaction_list:
            full_name_vn, cif_id, cif_number, booking_id, booking_code, status, business_type, branch_code, branch_name = transaction
            booking_ids.append(booking_id)
            mapping_datas.update({
                booking_id: dict(
                    full_name_vn=full_name_vn,
                    cif_id=cif_id,
                    cif_number=cif_number,
                    booking_id=booking_id,
                    booking_code=booking_code,
                    business_type=business_type,
                    branch_code=branch_code,
                    branch_name=branch_name,
                    stage_role=None,
                    teller=None,
                    supervisor=None,
                    audit=None
                )
            })

        senders = self.call_repos(await repos_get_senders(booking_ids=tuple(booking_ids), session=self.oracle_session))
        for stage, stage_role, sender, _, booking, _ in senders:
            if stage_role and stage_role.code in CIF_STAGE_ROLE_CODES:
                if stage_role.code == CIF_STAGE_ROLE_CODE_TELLER:
                    mapping_datas[booking.id].update(
                        teller=sender.user_fullname,
                        stage_role=stage_role.code
                    )
                elif stage_role.code == CIF_STAGE_ROLE_CODE_SUPERVISOR:
                    mapping_datas[booking.id].update(
                        supervisor=sender.user_fullname,
                        stage_role=stage_role.code
                    )
                elif stage_role.code == CIF_STAGE_ROLE_CODE_AUDIT:
                    mapping_datas[booking.id].update(
                        teller=sender.user_fullname,
                        audit=stage_role.code
                    )

        return self.response_paging(
            data=[mapping_data for _, mapping_data in mapping_datas.items()],
            current_page=current_page,
            total_items=total_item,
            total_page=total_page
        )

    async def ctr_get_customer_list(self, cif_number: str, identity_number: str, phone_number: str, full_name: str):

        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        customers = self.call_repos(await repos_get_customer(
            cif_number=cif_number,
            identity_number=identity_number,
            phone_number=phone_number,
            full_name=full_name,
            limit=limit,
            page=current_page,
            session=self.oracle_session))

        total_item = self.call_repos(
            await repos_get_total_item(
                cif_number=cif_number,
                identity_number=identity_number,
                phone_number=phone_number,
                full_name=full_name,
                session=self.oracle_session
            )
        )

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        response_data = [{
            "cif_id": item.Customer.id,
            "cif_number": item.Customer.cif_number,
            "full_name": item.Customer.full_name_vn,
            "identity_number": item.CustomerIdentity.identity_num if item.CustomerIdentity else None,
            "phone_number": item.Customer.mobile_number,
            "street": item.CustomerAddress.address if item.CustomerAddress else None,
            "ward": dropdown(item.AddressWard) if item.AddressWard else None,
            "district": dropdown(item.AddressDistrict) if item.AddressDistrict else None,
            "province": dropdown(item.AddressProvince) if item.AddressProvince else None,
            "branch": dropdown(item.Branch) if item.Branch else None
        } for item in customers]

        return self.response_paging(
            data=response_data,
            current_page=current_page,
            total_items=total_item,
            total_page=total_page
        )

    async def ctr_branch(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        branch_code = current_user.hrm_branch_code

        is_success, contract_info = self.call_repos(
            await repos_branch(
                branch_code=branch_code,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(contract_info))

        return self.response(data=contract_info)

    async def ctr_accounting_entry(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        branch_code = current_user.hrm_branch_code

        is_success, contract_info = self.call_repos(
            await repos_accounting_entry(
                branch_code=branch_code,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(contract_info))

        return self.response(data=contract_info)

    async def ctr_region(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        is_success, contract_info = self.call_repos(
            await repos_region(
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(contract_info))

        return self.response(data=contract_info)
