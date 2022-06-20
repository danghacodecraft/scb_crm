from datetime import date

from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.repository import (
    repos_accounting_entry, repos_branch, repos_count_total_item,
    repos_get_customer, repos_get_open_casa_info_from_booking,
    repos_get_open_cif_info_from_booking, repos_get_senders,
    repos_get_sla_trans, repos_get_total_item, repos_get_transaction_list,
    repos_region
)
from app.utils.constant.business_type import (
    BUSINESS_TYPE_INIT_CIF, BUSINESS_TYPE_OPEN_CASA
)
from app.utils.constant.cif import (
    CIF_STAGE_ROLE_CODE_AUDIT, CIF_STAGE_ROLE_CODE_SUPERVISOR,
    CIF_STAGE_ROLE_CODE_TELLER, CIF_STAGE_ROLE_CODES
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import dropdown


class CtrDashboard(BaseController):
    async def ctr_get_transaction_list(self, region_id: str, branch_id: str, business_type_id: str,
                                       status_code: str, search_box: str, from_date: date, to_date: date):
        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        transaction_list = self.call_repos(await repos_get_transaction_list(
            region_id=region_id,
            branch_id=branch_id,
            business_type_id=business_type_id,
            status_code=status_code,
            search_box=search_box,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            page=current_page,
            session=self.oracle_session
        ))

        total_item = self.call_repos(await repos_count_total_item(
            region_id=region_id, branch_id=branch_id, business_type_id=business_type_id, status_code=status_code,
            search_box=search_box, from_date=from_date, to_date=to_date, session=self.oracle_session))

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        mapping_datas = {}
        booking_ids = []
        business_type_init_cifs = []
        business_type_open_casas = []

        for transaction in transaction_list:
            booking, branch, status = transaction

            booking_id = booking.id
            booking_code = booking.code
            booking_ids.append(booking_id)
            business_type = booking.business_type

            business_type_id = business_type.id
            business_type_name = business_type.name

            branch_code = branch.code
            branch_name = branch.name

            if business_type_id == BUSINESS_TYPE_INIT_CIF:
                business_type_init_cifs.append(booking_id)
            if business_type_id == BUSINESS_TYPE_OPEN_CASA:
                business_type_open_casas.append(booking_id)
            # TODO: còn các loại nghiệp vụ khác

            mapping_datas.update({
                booking_id: dict(
                    created_at=booking.created_at,
                    full_name_vn=None,
                    cif_id=None,
                    cif_number=None,
                    booking_id=booking_id,
                    booking_code=booking_code,
                    business_type=dict(
                        name=business_type_name,
                        numbers=[]
                    ),
                    branch_code=branch_code,
                    branch_name=branch_name,
                    stage_role=None,
                    status=status,
                    teller=dict(
                        name=None,
                        created_at=None
                    ),
                    supervisor=dict(
                        name=None,
                        created_at=None
                    ),
                    audit=dict(
                        name=None,
                        created_at=None
                    )
                )
            })
        print(booking_ids)

        # Lấy thông tin các giao dịch Mở TKTT
        open_casa_infos = self.call_repos(
            await repos_get_open_casa_info_from_booking(booking_ids=business_type_open_casas,
                                                        session=self.oracle_session))
        exist_booking = {}
        for booking, _, casa_account, customer in open_casa_infos:
            account_info = dict(
                number=casa_account.casa_account_number,
                approval_status=casa_account.approve_status
            )
            if booking.parent_id not in exist_booking:
                account_numbers = [account_info]
            else:
                account_numbers = exist_booking[booking.parent_id]
                account_numbers.append(account_info)
            exist_booking.update({booking.parent_id: account_numbers})

            mapping_datas[booking.parent_id].update(
                full_name_vn=customer.full_name_vn,
                cif_id=customer.id,
                cif_number=customer.cif_number
            )
            mapping_datas[booking.parent_id]['business_type'].update(
                numbers=account_numbers
            )

        # Lấy thông tin các giao dịch Mở CIF
        open_cif_infos = self.call_repos(
            await repos_get_open_cif_info_from_booking(booking_ids=business_type_init_cifs,
                                                       session=self.oracle_session))

        for booking, _, customer in open_cif_infos:
            if customer:
                mapping_datas[booking.id].update(
                    full_name_vn=customer.full_name_vn,
                    cif_id=customer.id,
                    cif_number=customer.cif_number
                )
                mapping_datas[booking.id]['business_type'].update(
                    numbers=[dict(
                        number=customer.cif_number,
                        approval_status=customer.complete_flag
                    )]
                )

        # Lấy tất cả người thực hiện của giao dịch
        if booking_ids:
            stage_infos = self.call_repos(await repos_get_senders(
                booking_ids=tuple(booking_ids),
                region_id=region_id, branch_id=branch_id, status_code=status_code,
                search_box=search_box, from_date=from_date, to_date=to_date, session=self.oracle_session
            ))

            for transaction_daily, stage, stage_role, sender, booking_id, business_type_id in stage_infos:
                if stage_role and stage_role.code in CIF_STAGE_ROLE_CODES:
                    mapping_datas[booking_id].update(
                        stage_role=stage_role.code,
                    )
                    if stage_role.code == CIF_STAGE_ROLE_CODE_TELLER:
                        mapping_datas[booking_id]['teller'].update(
                            name=sender.user_fullname,
                            created_at=transaction_daily.created_at
                        )
                    if stage_role.code == CIF_STAGE_ROLE_CODE_SUPERVISOR:
                        mapping_datas[booking_id]['supervisor'].update(
                            name=sender.user_fullname,
                            created_at=transaction_daily.created_at
                        )
                    if stage_role.code == CIF_STAGE_ROLE_CODE_AUDIT:
                        mapping_datas[booking_id]['audit'].update(
                            name=sender.user_fullname,
                            created_at=transaction_daily.created_at
                        )

        sla_trans = self.call_repos(await repos_get_sla_trans(
            booking_ids=tuple(business_type_init_cifs),
            region_id=region_id, branch_id=branch_id, business_type_id=business_type_id, status_code=status_code,
            search_box=search_box, from_date=from_date, to_date=to_date, session=self.oracle_session))

        init_time = None
        teller_time = None
        teller_sla_time = None
        supervisor_time = None
        supervisor_sla_time = None
        audit_time = None
        audit_sla_time = None
        for idx, (trans_dl, trans_stg, sla_transaction, book_id) in enumerate(sla_trans):
            if sla_transaction.sla_id is None:
                init_time = sla_transaction.created_at
                print('1')
                print(init_time)
            elif sla_transaction.sla_id == "CIF_GDV":
                teller_time = sla_transaction.created_at
                print('2')
                print(teller_time)
            elif sla_transaction.sla_id == "CIF_KSV":
                supervisor_time = sla_transaction.created_at
                print('3')
                print(supervisor_time)
            elif sla_transaction.sla_id == "CIF_KSS":
                audit_time = sla_transaction.created_at
                print('4')
                print(audit_time)

            if init_time and teller_time:
                teller_sla_time = teller_time - init_time

            if teller_time and supervisor_time:
                supervisor_sla_time = supervisor_time - teller_time

            if supervisor_time and audit_time:
                audit_sla_time = audit_time - supervisor_time

            mapping_datas[book_id]['teller'].update(
                sla_time=teller_sla_time
            )

            mapping_datas[book_id]['supervisor'].update(
                sla_time=supervisor_sla_time
            )

            mapping_datas[book_id]['audit'].update(
                sla_time=audit_sla_time
            )

            # print(idx)
            # print("trans_dl.__dict")
            # print(trans_dl.__dict__)
            # print("trans_stg.__dict")
            # print(trans_stg.__dict__)
            # print("sla_tr.__dict")
            # print(sla_tr.__dict__)
            # print("bk_id")
            # print(bk_id)
            # print(idx)
            # mapping_datas.update()

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
                branch_code=branch_code
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
                branch_code=branch_code
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
            await repos_region()
        )
        if not is_success:
            return self.response_exception(msg=str(contract_info))

        return self.response(data=contract_info)
