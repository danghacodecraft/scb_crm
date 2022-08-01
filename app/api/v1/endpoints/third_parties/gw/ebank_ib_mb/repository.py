from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_check_username_ib_mb_exist(
        transaction_name,
        transaction_value,
        current_user
):
    current_user = current_user.user_info
    is_success, check_username_ib_mb_exist = await service_gw.check_username_ib_mb_exist(
        current_user=current_user,
        transaction_name=transaction_name,
        transaction_value=transaction_value
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_check_username_ib_mb_exist",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(check_username_ib_mb_exist)
        )

    return ReposReturn(data=check_username_ib_mb_exist)


async def repos_gw_retrieve_ib_info_by_cif(
        current_user,
        cif_num
):
    current_user = current_user.user_info
    is_success, retrieve_ib_info_by_cif = await service_gw.retrieve_ib_info_by_cif(
        current_user=current_user,
        cif_num=cif_num
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_ib_info_by_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(retrieve_ib_info_by_cif)
        )

    return ReposReturn(data=retrieve_ib_info_by_cif)


async def repos_gw_retrieve_mb_info_by_cif(
        current_user,
        cif_num
):
    current_user = current_user.user_info
    is_success, retrieve_mb_info_by_cif = await service_gw.retrieve_mb_info_by_cif(
        current_user=current_user,
        cif_num=cif_num
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_mb_info_by_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(retrieve_mb_info_by_cif)
        )

    return ReposReturn(data=retrieve_mb_info_by_cif)


async def repos_gw_summary_bp_trans_by_service(
        current_user,
        cif_num,
        transaction_val_date,
        transaction_val_date_to_date
):
    current_user = current_user.user_info
    is_success, summary_bp_trans_by_service = await service_gw.summary_bp_trans_by_service(
        current_user=current_user,
        cif_num=cif_num,
        transaction_val_date=transaction_val_date,
        transaction_val_date_to_date=transaction_val_date_to_date
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_summary_bp_trans_by_service",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(summary_bp_trans_by_service)
        )

    return ReposReturn(data=summary_bp_trans_by_service)
