from datetime import date
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.cif.payment_account.detail.repository import (
    repos_get_detail_payment_accounts_by_account_ids
)
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_get_casa_account_by_account_number,
    repos_get_sms_casa_mobile_number_from_db_by_account_number,
    repos_save_transaction_jobs, repos_update_approval_status_for_ebank,
    repos_update_approval_status_for_reg_balance, repos_update_casa_account
)
from app.api.v1.endpoints.third_parties.gw.ebank.repository import (
    repos_get_e_banking_from_db_by_cif_number,
    repos_pull_e_banking_from_gw_cif_number_and_return_is_exist_ebank
)
from app.api.v1.endpoints.user.schema import AuthResponse, UserInfoResponse
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.others import TransactionJob
from app.utils.constant.approval import (
    BUSINESS_JOB_CODE_OPEN_CASA, BUSINESS_JOB_CODE_OPEN_CASA_DEBIT,
    BUSINESS_JOB_CODE_OPEN_CASA_EB, BUSINESS_JOB_CODE_START_CASA,
    BUSINESS_JOB_CODE_WITHDRAW
)
from app.utils.constant.casa import CASA_ACCOUNT_STATUS_APPROVED
from app.utils.constant.cif import (
    BUSINESS_FORM_CLOSE_CASA_PD, BUSINESS_FORM_OPEN_CASA_PD,
    BUSINESS_FORM_WITHDRAW_PD
)
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DEFAULT_VALUE, GW_FUNC_CASH_WITHDRAWS_OUT,
    GW_RESPONSE_STATUS_SUCCESS, GW_TRANSACTION_NAME_COLUMN_CHART,
    GW_TRANSACTION_NAME_PIE_CHART, GW_TRANSACTION_NAME_STATEMENT
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_CASA_ACCOUNT_APPROVED, ERROR_NO_DATA
)
from app.utils.functions import (
    date_to_string, generate_uuid, now, orjson_dumps
)
from app.utils.mapping import mapping_authentication_code_crm_to_core
from app.utils.vietnamese_converter import split_name


async def repos_gw_get_casa_account_by_cif_number(
        cif_number: str, current_user: AuthResponse
):
    is_success, casa_accounts = await service_gw.get_casa_account_from_cif(
        casa_cif_number=cif_number, current_user=current_user.user_info
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(casa_accounts)
        )

    return ReposReturn(data=casa_accounts)


async def repos_gw_get_casa_account_info(
        account_number: str,
        current_user: str
):
    is_success, gw_casa_account_info = await service_gw.get_casa_account(
        current_user=current_user,
        account_number=account_number
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_casa_account_info)
        )

    return ReposReturn(data=gw_casa_account_info)


async def repos_gw_get_pie_chart_casa_account_info(
    account_number: str,
    current_user: str,
):
    is_success, gw_report_history_account_info = await service_gw.get_report_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_PIE_CHART
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_report_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_report_history_account_info)
        )

    return ReposReturn(data=gw_report_history_account_info)


async def repos_gw_get_column_chart_casa_account_info(
    account_number: str,
    current_user: str,
    from_date: date,
    to_date: date
):
    is_success, gw_report_column_chart_casa_account_info = await service_gw.get_report_history_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_COLUMN_CHART,
        from_date=from_date,
        to_date=to_date
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="gw_report_column_chart_casa_account_info",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_report_column_chart_casa_account_info)
        )

    return ReposReturn(data=gw_report_column_chart_casa_account_info)


async def repos_gw_get_statements_casa_account_info(
    account_number: str,
    current_user: str,
    from_date: date,
    to_date: date
):
    is_success, gw_report_history_account_info = await service_gw.get_report_statement_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_STATEMENT,
        from_date=from_date,
        to_date=to_date
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_report_statement_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_report_history_account_info)
        )

    return ReposReturn(data=gw_report_history_account_info)


async def repos_gw_open_casa_account(
    cif_number: str,
    self_selected_account_flag: bool,
    casa_account_info,
    booking_parent_id: str,
    session: Session,
    current_user: AuthResponse,
    maker_staff_name: str
):
    current_user = current_user.user_info
    is_success, gw_open_casa_account_info, form_data = await service_gw.get_open_casa_account(
        cif_number=cif_number,
        self_selected_account_flag=self_selected_account_flag,
        casa_account_info=casa_account_info,
        current_user=current_user,
        maker_staff_name=maker_staff_name
    )
    await repos_add_business_form_and_transaction_job(
        booking_id=booking_parent_id,
        business_form_id=BUSINESS_FORM_OPEN_CASA_PD,
        form_data=form_data,
        gw_response=gw_open_casa_account_info,
        is_success=is_success,
        session=session
    )

    return is_success, gw_open_casa_account_info


async def repos_get_progress_open_casa(booking_id: str, session: Session):
    transaction_jobs = session.execute(
        select(
            TransactionJob
        )
        .filter(TransactionJob.booking_id == booking_id)
    ).scalars().all()

    completed_bussiness_jobs = [
        transaction_job.business_job_id for transaction_job in transaction_jobs if transaction_job.complete_flag]

    is_complete_casa = True if BUSINESS_JOB_CODE_OPEN_CASA in completed_bussiness_jobs else False
    is_complete_eb = True if BUSINESS_JOB_CODE_OPEN_CASA_EB in completed_bussiness_jobs else False
    is_complete_debit = True if BUSINESS_JOB_CODE_OPEN_CASA_DEBIT in completed_bussiness_jobs else False

    response = (is_complete_casa, is_complete_eb, is_complete_debit)
    return ReposReturn(data=response)


@auto_commit
async def repos_gw_get_close_casa_account(
        current_user,
        request_data_gw: list,
        booking_id,
        session
):
    response_data = []
    account_number = []
    current_user = current_user.user_info
    for item in request_data_gw:

        is_success, gw_close_casa_account = await service_gw.get_close_casa_account(
            data_input=item,
            current_user=current_user
        )
        # lưu form data request GW
        session.add(
            BookingBusinessForm(**dict(
                booking_business_form_id=generate_uuid(),
                booking_id=booking_id,
                form_data=orjson_dumps(item),
                business_form_id=BUSINESS_FORM_CLOSE_CASA_PD,
                save_flag=True,
                created_at=now(),
                log_data=orjson_dumps(gw_close_casa_account)
            ))
        )
        casa_account_number = item.get('account_info').get('account_num')
        casa_account = await repos_get_casa_account_by_account_number(casa_account_number, session)

        if is_success:
            close_casa = gw_close_casa_account['closeCASA_out']['transaction_info']
            if close_casa.get('transaction_error_code') == GW_RESPONSE_STATUS_SUCCESS:
                account_number.append({
                    "id": casa_account.data,
                    "casa_account_number": casa_account_number,
                    "acc_active_flag": False
                })
            response_data.append({
                "transaction": {
                    "account_number": casa_account_number,
                    "code": close_casa.get('transaction_error_code'),
                    "msg": close_casa.get('transaction_error_msg')
                }
            })
        else:
            response_data.append({
                "transaction": {
                    "account_number": casa_account_number,
                    "code": ERROR_CALL_SERVICE_GW,
                    "msg": ERROR_CALL_SERVICE_GW
                }
            })

    # đóng trạng thái hoạt động của tài khoản
    session.bulk_update_mappings(CasaAccount, account_number)

    return ReposReturn(data=response_data)


async def repos_open_casa_get_casa_account_infos(
    casa_account_ids: List[str],
    session: Session
):
    casa_account_infos = session.execute(
        select(
            CasaAccount
        )
        .filter(CasaAccount.id.in_(casa_account_ids))
    ).scalars().all()
    return ReposReturn(data=casa_account_infos)


async def repos_add_business_form_and_transaction_job(
    booking_id: str,
    business_form_id: str,
    form_data: dict,
    session: Session,
    gw_response,
    is_success: bool,
):
    history_datas = []
    error_code = None
    error_desc = None
    if not is_success:
        transaction_info = gw_response['openCASA_out']['transaction_info']
        error_code = transaction_info['transaction_error_code']
        error_desc = transaction_info['transaction_error_msg']

    session.add_all([
        TransactionJob(**dict(
            transaction_id=generate_uuid(),
            booking_id=booking_id,
            business_job_id=BUSINESS_JOB_CODE_OPEN_CASA,
            complete_flag=is_success,
            error_code=error_code,
            error_desc=error_desc,
            created_at=now()
        )),
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            booking_business_form_id=generate_uuid(),
            business_form_id=business_form_id,
            save_flag=True,
            created_at=now(),
            form_data=orjson_dumps(form_data),
            log_data=orjson_dumps(history_datas)
        ))
    ])

    session.commit()
    return True


@auto_commit
async def repos_update_casa_account_to_approved(
    update_casa_accounts: List,
    session: Session
):
    session.bulk_update_mappings(CasaAccount, update_casa_accounts)

    return ReposReturn(data=True)


async def repos_check_casa_account_approved(casa_account_ids: List, session: Session):
    casa_account_status_approved_ids = session.execute(
        select(
            CasaAccount.id
        ).filter(and_(
            CasaAccount.id.in_(casa_account_ids),
            CasaAccount.approve_status == CASA_ACCOUNT_STATUS_APPROVED
        ))
    ).scalars().all()

    if casa_account_status_approved_ids:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CASA_ACCOUNT_APPROVED,
            loc=f'casa_account_ids: {casa_account_status_approved_ids}'
        )

    return ReposReturn(data=casa_account_status_approved_ids)


async def repos_gw_get_tele_transfer(current_user: UserInfoResponse, data_input):
    is_success, tele_transfer = await service_gw.get_tele_transfer(
        current_user=current_user,
        data_input=data_input
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="repos_gw_get_tele_transfer",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(tele_transfer)
        )

    return ReposReturn(data=tele_transfer)


@auto_commit
async def repos_gw_withdraw(
        current_user,
        request_data_gw,
        booking_id,
        session: Session
):
    is_success, gw_withdraw = await service_gw.gw_withdraw(
        current_user=current_user.user_info,
        data_input=request_data_gw
    )

    # lưu form data request GW
    session.add(
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            booking_business_form_id=generate_uuid(),
            form_data=orjson_dumps(request_data_gw),
            business_form_id=BUSINESS_FORM_WITHDRAW_PD,
            save_flag=True,
            created_at=now(),
            log_data=orjson_dumps(gw_withdraw)
        ))
    )

    session.add(TransactionJob(**dict(
        transaction_id=generate_uuid(),
        booking_id=booking_id,
        business_job_id=BUSINESS_JOB_CODE_WITHDRAW,
        complete_flag=is_success,
        error_code=gw_withdraw.get(GW_FUNC_CASH_WITHDRAWS_OUT).get('transaction_info').get(
            'transaction_error_code'),
        error_desc=gw_withdraw.get(GW_FUNC_CASH_WITHDRAWS_OUT).get('transaction_info').get(
            'transaction_error_msg'),
        created_at=now()
    )))

    return ReposReturn(data=(is_success, gw_withdraw))


async def repos_gw_get_retrieve_ben_name_by_account_number(current_user: UserInfoResponse, data_input):
    is_success, ben_name = await service_gw.get_ben_name_by_account_number(
        current_user=current_user,
        data_input=data_input
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="repos_gw_get_retrieve_ben_name_by_account_number",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(ben_name)
        )
    return ReposReturn(data=ben_name)


async def repos_gw_get_retrieve_ben_name_by_card_number(current_user: UserInfoResponse, data_input):
    is_success, ben_name = await service_gw.get_ben_name_by_card_number(
        current_user=current_user,
        data_input=data_input
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="repos_gw_get_retrieve_ben_name_by_card_number",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(ben_name)
        )
    return ReposReturn(data=ben_name)


async def repos_gw_change_status_account(current_user, account_number):
    # TODO default đóng tài khoản thanh toán
    data_input = {
        "account_info": {
            "account_num": account_number
        },
        # TODO hard core
        "p_blk_main": {
            "TRANSACTION_INFO": {
                "SOURCE_CODE": "ODC1",
                "USER_ID": "ODC1",
                "BRANCH_CODE": ""
            },
            "CHANGE_DETAIL": {
                "NEW_STATUS": "NORM",
                "NO_DEBIT": "Y",
                "NO_CREDIT": "Y"
            }
        },
        "p_blk_charge": "",
        "p_blk_udf": "",
        "p_udf": "",
        # TODO hard checker, maker
        "staff_info_checker": {
            "staff_name": "PLGDKSS"
        },
        "staff_info_maker": {
            "staff_name": "PLGDKSS"
        }
    }

    is_success, response_data, request_data = await service_gw.change_status_account(current_user, data_input)

    return ReposReturn(data=(is_success, response_data))


async def repos_push_casa_to_gw_open_casa(booking_id: str,
                                          session: Session,
                                          current_user: any,
                                          cif_number: str,
                                          maker_staff_name,
                                          casa_account_ids: List[str] = None):
    account_number_list = []

    payment_account_list_result = await repos_get_detail_payment_accounts_by_account_ids(
        casa_account_ids=casa_account_ids,
        session=session
    )
    if payment_account_list_result.is_error:
        return ReposReturn(
            is_error=True,
            msg=payment_account_list_result.msg,
            loc=payment_account_list_result.loc,
            detail=payment_account_list_result.detail,
            error_status_code=payment_account_list_result.error_status_code
        )

    for payment_account in payment_account_list_result.data:

        casa_account = payment_account[0]

        is_success, gw_open_casa_account_info, _ = await service_gw.get_open_casa_account(
            cif_number=cif_number,
            self_selected_account_flag=casa_account.self_selected_account_flag,
            casa_account_info=casa_account,
            current_user=current_user.user_info,
            maker_staff_name=maker_staff_name
        )

        # Chỉ Lưu transaction job bị fail
        if not is_success:
            await repos_save_transaction_jobs(
                session=session,
                booking_id=booking_id,
                is_success=is_success,
                response_data=gw_open_casa_account_info,
                business_job_ids=[BUSINESS_JOB_CODE_START_CASA, BUSINESS_JOB_CODE_OPEN_CASA]
            )

            return ReposReturn(
                is_error=True,
                loc="open_casa",
                msg=ERROR_CALL_SERVICE_GW,
                detail=str(gw_open_casa_account_info)
            )

        account_number = gw_open_casa_account_info['openCASA_out']['data_output']['account_info']['account_num']

        # cập nhật lại casa_number
        await repos_update_casa_account(
            casa_account=casa_account, account_number=account_number, session=session
        )

        account_number_list.append(account_number)

    # Lưu lại transacton thành công
    await repos_save_transaction_jobs(
        session=session,
        booking_id=booking_id,
        is_success=True,
        response_data=None,
        business_job_ids=[BUSINESS_JOB_CODE_START_CASA, BUSINESS_JOB_CODE_OPEN_CASA]
    )

    return ReposReturn(data=account_number_list)


async def repos_account_number_list_by_casa_account_ids(
        casa_account_ids: List[str], session: Session
):
    account_number_list = []
    for casa_account_id in casa_account_ids:
        casa_account_number = session.execute(
            select(
                CasaAccount.casa_account_number
            ).filter(
                CasaAccount.id == casa_account_id
            )
        ).scalars().first()

        if not casa_account_number:
            return ReposReturn(
                is_error=True,
                loc="open_casa -> repos_account_number_list_by_casa_account_ids ->casa_account_number",
                msg=ERROR_NO_DATA
            )

        account_number_list.append(casa_account_number)

    return ReposReturn(data=account_number_list)


@auto_commit
async def repos_push_internet_banking_to_gw_open_casa(booking_id: str,
                                                      session: Session,
                                                      response_customers: dict,
                                                      current_user: any,
                                                      cif_id: str,
                                                      cif_number: str,
                                                      account_number_list: str,
                                                      maker_staff_name: str):

    first_row = response_customers[0]
    customer = first_row.Customer
    cust_individual = first_row.CustomerIndividualInfo

    # Pull Ebank từ GW
    is_exist_ebank = (await repos_pull_e_banking_from_gw_cif_number_and_return_is_exist_ebank(
        cif_id=cif_id,
        cif_number=cif_number,
        current_user=current_user,
        session=session
    )).data

    e_banking = None
    # Nếu trên core không có EB, kiểm tra DB có thông tin EB hay không để push
    if not is_exist_ebank:
        e_banking = (await repos_get_e_banking_from_db_by_cif_number(
            cif_number=cif_number, session=session
        )).data

    # Lấy thông tin SMS casa từ DB
    account_number__reg_balacne_info = {}

    for account_number in account_number_list:
        balance_id__relationship_mobile_numbers_result = await repos_get_sms_casa_mobile_number_from_db_by_account_number(
            account_number=account_number, session=session)
        if balance_id__relationship_mobile_numbers_result.is_error:
            return ReposReturn(
                is_error=True,
                msg=balance_id__relationship_mobile_numbers_result.msg,
                loc=balance_id__relationship_mobile_numbers_result.loc,
                detail=balance_id__relationship_mobile_numbers_result.detail,
                error_status_code=balance_id__relationship_mobile_numbers_result.error_status_code
            )
        balance_id__relationship_mobile_numbers = balance_id__relationship_mobile_numbers_result.data

        if balance_id__relationship_mobile_numbers:
            account_number__reg_balacne_info[account_number] = balance_id__relationship_mobile_numbers

    # Không tìm thấy thông tin từ DB có thể do khách hàng không đăng ký, hoặc đã đăng ký thành công từ lần trước
    if not e_banking and not account_number__reg_balacne_info:
        # Lưu transaction job
        await repos_save_transaction_jobs(
            session=session,
            booking_id=booking_id,
            is_success=True,
            response_data=None,
            business_job_ids=[BUSINESS_JOB_CODE_OPEN_CASA_EB]
        )
        return ReposReturn(data=None)

    # Push GW EBANK
    error_messages = []
    is_success_eb = False
    is_success_sms = False

    if e_banking:
        authentication_info = []
        for authentication_code in e_banking["authentication_info_list"]:
            authentication_info.append({
                "authentication_code": mapping_authentication_code_crm_to_core(authentication_code)
            })

        e_banking_info = {
            "ebank_ibmb_info": {
                "ebank_ibmb_username": e_banking["account_name"],
                "ebank_ibmb_mobilephone": customer.mobile_number
            },
            "cif_info": {
                "cif_num": cif_number
            },
            "address_info": {
                "line": first_row.CustomerAddress.address,
                "ward_name": first_row.AddressWard.name,
                "district_name": first_row.AddressDistrict.name,
                "city_name": first_row.AddressProvince.name,
                "city_code": first_row.AddressCountry.id
            },
            "customer_info": {
                "full_name": customer.full_name_vn,
                "first_name": split_name(customer.full_name_vn)[2] if split_name(customer.full_name_vn)[2] else " ",
                "middle_name": split_name(customer.full_name_vn)[1] if split_name(customer.full_name_vn)[1] else " ",
                "last_name": split_name(customer.full_name_vn)[0],
                "birthday": date_to_string(cust_individual.date_of_birth, _format=GW_DATE_FORMAT) if cust_individual.date_of_birth else GW_DEFAULT_VALUE,
                "email": customer.email if customer.email else GW_DEFAULT_VALUE
            },
            "authentication_info": authentication_info,
            "service_package_info": {
                "service_package_code": GW_DEFAULT_VALUE
            },
            "staff_referer": {
                "staff_code": GW_DEFAULT_VALUE
            }
        }

        is_success_eb, eb_response_data = await service_gw.get_open_ib(
            current_user=current_user.user_info,
            data_input=e_banking_info
        )

        if is_success_eb:
            await repos_update_approval_status_for_ebank(
                ebank_id=e_banking['id'], session=session
            )
        else:
            error_messages.append(eb_response_data)

    # Push GW SMS
    if account_number__reg_balacne_info:
        for casa_account_number, balance_id__relationship_mobile_numbers in account_number__reg_balacne_info.items():
            ebank_sms_info_list = []
            reg_balance_id = None
            for balance_id, mobile_numbers in balance_id__relationship_mobile_numbers.items():
                ebank_sms_info_list = [{
                    "ebank_sms_info_item": {
                        "ebank_sms_indentify_num": mobile_number,
                        "cif_info": {
                            "cif_num": cif_number
                        },
                        "branch_info": {
                            "branch_code": current_user.user_info.hrm_branch_code
                        }
                    }
                } for mobile_number in mobile_numbers]

                reg_balance_id = balance_id

            # @TODO: hard code account_type là "TT" biến động số dư
            account_info = {
                "account_num": casa_account_number,
                "account_type": "TT"
            }
            staff_info_checker = {
                "staff_name": current_user.user_info.username
            }
            staff_info_maker = {
                "staff_name": maker_staff_name
            }

            is_success_sms, sms_response_data = await service_gw.register_sms_service_by_account_casa(
                current_user=current_user.user_info,
                account_info=account_info,
                ebank_sms_info_list=ebank_sms_info_list,
                staff_info_checker=staff_info_checker,
                staff_info_maker=staff_info_maker
            )

            if is_success_sms:
                await repos_update_approval_status_for_reg_balance(
                    reg_balance_id=reg_balance_id, session=session
                )
            else:
                error_messages.append(sms_response_data)

    # Lưu transaction job
    await repos_save_transaction_jobs(
        session=session,
        booking_id=booking_id,
        is_success=False if error_messages else True,
        response_data=error_messages,
        business_job_ids=[BUSINESS_JOB_CODE_OPEN_CASA_EB]
    )

    if error_messages:
        return ReposReturn(
            is_error=True,
            loc="open_cif -> repos_push_internet_banking_to_gw",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(error_messages)
        )

    return ReposReturn(data=None)
