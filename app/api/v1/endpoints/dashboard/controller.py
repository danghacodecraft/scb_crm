from datetime import date

from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.repository import (
    repos_count_total_item, repos_get_amount_block_from_booking,
    repos_get_customer, repos_get_customers_by_cif_number,
    repos_get_open_casa_info_from_booking,
    repos_get_open_cif_info_from_booking, repos_get_senders,
    repos_get_sla_transaction_infos, repos_get_td_account_from_booking,
    repos_get_total_item, repos_get_transaction_list,
    repos_get_withdraw_info_from_booking
)
from app.api.v1.endpoints.third_parties.gw.category.controller import (
    CtrSelectCategory
)
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_CASA_TOP_UP, BUSINESS_TYPE_CASA_TRANSFER,
    BUSINESS_TYPE_CLOSE_CASA, BUSINESS_TYPE_INIT_CIF, BUSINESS_TYPE_OPEN_CASA,
    BUSINESS_TYPE_TD_ACCOUNT_OPEN_ACCOUNT, BUSINESS_TYPE_WITHDRAW
)
from app.utils.constant.casa import (
    CASA_TOP_UP_NUMBER_TYPE_CASA_ACCOUNT_NUMBER,
    CASA_TOP_UP_NUMBER_TYPE_IDENTITY_NUMBER,
    CASA_TRANSFER_NUMBER_TYPE_CASA_ACCOUNT_NUMBER,
    CASA_TRANSFER_NUMBER_TYPE_IDENTITY_NUMBER
)
from app.utils.constant.cif import (
    CIF_STAGE_ROLE_CODE_AUDIT, CIF_STAGE_ROLE_CODE_SUPERVISOR,
    CIF_STAGE_ROLE_CODE_TELLER, CIF_STAGE_ROLE_CODES
)
from app.utils.constant.gw import GW_TRANSACTION_NAME, GW_TRANSACTION_VALUE
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import dropdown, orjson_loads


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
        business_type_amount_block = []
        business_type_withdraws = []
        business_type_open_td_account = []
        for transaction in transaction_list:
            booking, branch, status, stage_role = transaction

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
            if business_type_id == BUSINESS_TYPE_AMOUNT_BLOCK \
                    or business_type_id == BUSINESS_TYPE_AMOUNT_UNBLOCK \
                    or business_type_id == BUSINESS_TYPE_CLOSE_CASA:
                business_type_amount_block.append(booking_id)
            if business_type_id == BUSINESS_TYPE_WITHDRAW:
                business_type_withdraws.append(booking_id)
            if business_type_id == BUSINESS_TYPE_TD_ACCOUNT_OPEN_ACCOUNT:
                business_type_open_td_account.append(booking_id)
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
                    stage_role=stage_role.code,
                    status=status,
                    teller=dict(),
                    supervisor=dict(),
                    audit=dict()
                )
            })
        # lấy thông tin giao dịch tài khoản tiết kiệm
        td_account = self.call_repos(
            await repos_get_td_account_from_booking(
                booking_ids=business_type_open_td_account,
                session=self.oracle_session
            )
        )

        for booking, _, _, customer in td_account:
            mapping_datas[booking.id].update(
                full_name_vn=customer.full_name_vn,
                cif_id=customer.id,
                cif_number=customer.cif_number
            )

        # lấy thông tin các giao dịch aoumut_block
        amount_blocks = self.call_repos(
            await repos_get_amount_block_from_booking(
                booking_ids=business_type_amount_block,
                session=self.oracle_session
            )
        )
        for booking, _, casa_account, customer in amount_blocks:
            mapping_datas[booking.id].update(
                full_name_vn=customer.full_name_vn,
                cif_id=customer.id,
                cif_number=customer.cif_number
            )

        # Lấy thông tin các giao dịch Mở TKTT\
        open_casa_infos = self.call_repos(
            await repos_get_open_casa_info_from_booking(booking_ids=business_type_open_casas,
                                                        session=self.oracle_session))
        exist_booking = {}
        for booking, _, casa_account, customer in open_casa_infos:
            account_info = dict(
                number=casa_account.casa_account_number,
                approval_status=casa_account.approve_status,
                number_type=CASA_TOP_UP_NUMBER_TYPE_CASA_ACCOUNT_NUMBER
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

        # Lấy thông tin các giao dịch Rút tiền
        withdraw_infos = self.call_repos(
            await repos_get_withdraw_info_from_booking(booking_ids=business_type_withdraws,
                                                       session=self.oracle_session))
        withdraw__cif_numbers = []
        for booking, booking_business_form in withdraw_infos:
            form_data = orjson_loads(booking_business_form.form_data)
            customer_info = form_data['customer_info']['sender_info']
            cif_number = customer_info['cif_number']
            withdraw__cif_numbers.append(cif_number)

        withdraw_cif_infos = self.call_repos(await repos_get_customers_by_cif_number(
            cif_numbers=withdraw__cif_numbers,
            session=self.oracle_session
        ))

        for booking, booking_business_form in withdraw_infos:
            form_data = orjson_loads(booking_business_form.form_data)
            cif_number = form_data['customer_info']['sender_info']['cif_number']
            for cif_info in withdraw_cif_infos:
                if cif_number == cif_info.cif_number:
                    mapping_datas[booking.id].update(
                        full_name_vn=cif_info.full_name_vn,
                        cif_id=cif_info.id,
                        cif_number=cif_number,
                    )
                    mapping_datas[booking.id]['business_type'].update(
                        numbers=[dict(
                            number=customer_info['cif_number'],
                            approval_status=customer_info['cif_flag']
                        )]
                    )

        # Lấy tất cả người thực hiện của giao dịch
        if booking_ids:
            stage_infos = self.call_repos(await repos_get_senders(
                booking_ids=tuple(booking_ids),
                region_id=region_id, branch_id=branch_id, status_code=status_code, business_type_id=business_type_id,
                search_box=search_box, from_date=from_date, to_date=to_date, session=self.oracle_session
            ))
            for transaction_daily, stage, stage_role, sender, booking, sla_transaction in stage_infos:
                booking_id = booking.id
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

        sla_transaction_infos = self.call_repos(await repos_get_sla_transaction_infos(
            booking_ids=tuple(booking_ids), session=self.oracle_session
        ))

        for (
                booking, sla_transaction, sender_sla_transaction, sla_transaction_parent, sender_sla_trans_parent,
                sla_transaction_grandparent, sender_sla_trans_grandparent, booking_business_form
        ) in sla_transaction_infos:
            for booking_id, data in mapping_datas.items():
                stage_role_code = data['stage_role']

                sla_transaction_created_at = sla_transaction.created_at
                sla_transaction_info = dict(
                    name=sender_sla_transaction.user_fullname,
                    created_at=sla_transaction_created_at,
                    sla_time=str(sla_transaction_created_at - booking.created_at),
                    sla_deadline=sla_transaction.sla_deadline
                )
                sla_transaction_parent_info = dict(
                    name=None,
                    created_at=None,
                    sla_time=None,
                    sla_deadline=None
                )
                sla_transaction_grandparent_info = dict(
                    name=None,
                    created_at=None,
                    sla_time=None,
                    sla_deadline=None
                )
                if sender_sla_trans_parent:
                    sla_transaction_parent_created_at = sla_transaction_parent.created_at
                    sla_transaction_parent_info = dict(
                        name=sender_sla_trans_parent.user_fullname,
                        created_at=sla_transaction_parent_created_at,
                        sla_time=str(sla_transaction_created_at - sla_transaction_parent_created_at),
                        sla_deadline=sla_transaction_parent.sla_deadline
                    )
                    if sender_sla_trans_grandparent:
                        sla_transaction_grandparent_created_at = sla_transaction_grandparent.created_at
                        sla_transaction_grandparent_info = dict(
                            name=sender_sla_trans_grandparent.user_fullname,
                            created_at=sla_transaction_grandparent_created_at,
                            sla_time=str(sla_transaction_parent_created_at - sla_transaction_grandparent_created_at),
                            sla_deadline=sla_transaction_grandparent.sla_deadline
                        )
                if booking.id == booking_id:
                    if stage_role_code == CIF_STAGE_ROLE_CODE_TELLER:
                        mapping_datas[booking_id]['teller'].update(sla_transaction_info)

                    if stage_role_code == CIF_STAGE_ROLE_CODE_SUPERVISOR:
                        mapping_datas[booking_id]['teller'].update(sla_transaction_parent_info)
                        mapping_datas[booking_id]['supervisor'].update(sla_transaction_info)

                    if stage_role_code == CIF_STAGE_ROLE_CODE_AUDIT:
                        mapping_datas[booking_id]['teller'].update(sla_transaction_grandparent_info)
                        mapping_datas[booking_id]['supervisor'].update(sla_transaction_parent_info)
                        mapping_datas[booking_id]['audit'].update(sla_transaction_info)

                    if booking_business_form and booking.business_type_id == BUSINESS_TYPE_CASA_TOP_UP and booking_business_form.form_data:
                        form_data = orjson_loads(booking_business_form.form_data)
                        sender_cif_number_key = 'sender_cif_number'
                        sender_full_name_key = 'sender_full_name_vn'
                        mapping_datas[booking_id].update(
                            cif_number=form_data[sender_cif_number_key] if sender_cif_number_key in form_data else None,
                            full_name_vn=form_data[sender_full_name_key] if sender_full_name_key in form_data else None
                        )

                        numbers = []
                        number_key_account_number = 'receiver_account_number'

                        if number_key_account_number in form_data:
                            numbers.append(dict(
                                number=form_data[number_key_account_number],
                                number_type=CASA_TOP_UP_NUMBER_TYPE_CASA_ACCOUNT_NUMBER,
                                approval_status=1  # TODO: trạng thái phê duyệt cho từng number
                            ))

                        number_key_identity_number = 'receiver_identity_number'
                        if number_key_identity_number in form_data:
                            numbers.append(dict(
                                number=form_data[number_key_identity_number],
                                number_type=CASA_TOP_UP_NUMBER_TYPE_IDENTITY_NUMBER,
                                approval_status=1  # TODO: trạng thái phê duyệt cho từng number
                            ))
                        mapping_datas[booking_id]['business_type']['numbers'] = numbers

                    if booking_business_form and booking.business_type_id == BUSINESS_TYPE_CASA_TRANSFER \
                            and booking_business_form.form_data:
                        form_data = orjson_loads(booking_business_form.form_data)

                        sender_cif_number_key = 'sender_cif_number'
                        sender_full_name_key = 'sender_full_name_vn'
                        mapping_datas[booking_id].update(
                            cif_number=form_data[sender_cif_number_key]
                            if sender_cif_number_key in form_data else None,
                            full_name_vn=form_data[sender_full_name_key]
                            if sender_full_name_key in form_data else None
                        )
                        numbers = []
                        number_key_account_number = 'receiver_account_number'
                        if number_key_account_number in form_data:
                            numbers.append(dict(
                                number=form_data[number_key_account_number],
                                number_type=CASA_TRANSFER_NUMBER_TYPE_CASA_ACCOUNT_NUMBER,
                                approval_status=1  # TODO: trạng thái phê duyệt cho từng number
                            ))

                        number_key_identity_number = 'receiver_identity_number'
                        if number_key_identity_number in form_data:
                            numbers.append(dict(
                                number=form_data[number_key_identity_number],
                                number_type=CASA_TRANSFER_NUMBER_TYPE_IDENTITY_NUMBER,
                                approval_status=1  # TODO: trạng thái phê duyệt cho từng number
                            ))
                        mapping_datas[booking_id]['business_type']['numbers'] = numbers

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

        gw_contract_infos = await CtrSelectCategory(current_user).ctr_select_category(
            transaction_name=GW_TRANSACTION_NAME,
            transaction_value=GW_TRANSACTION_VALUE
        )
        if not gw_contract_infos:
            return self.response_exception(msg=str(gw_contract_infos))

        contract_infos = gw_contract_infos['data']

        response_data = [dict(
            branch_code=contract_info['BRANCH_CODE'],
            branch_name=contract_info['BRANCH_DESC'],
        ) for contract_info in contract_infos]

        return self.response(data=response_data)

    # async def ctr_accounting_entry(self):
    #     current_user = self.current_user.user_info
    #     if not current_user:
    #         return self.response_exception(
    #             msg=USER_NOT_EXIST,
    #             detail=MESSAGE_STATUS[USER_NOT_EXIST],
    #             loc="current_user"
    #         )
    #
    #     branch_code = current_user.hrm_branch_code
    #
    #     is_success, contract_info = self.call_repos(
    #         await repos_accounting_entry(
    #             branch_code=branch_code
    #         )
    #     )
    #     if not is_success:
    #         return self.response_exception(msg=str(contract_info))
    #
    #     return self.response(data=contract_info)
