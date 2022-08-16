from app.api.base.repository import ReposReturn
from app.settings.event import service_ekyc
from app.utils.error_messages import ERROR_CALL_SERVICE_EKYC


async def repos_get_list_kss(
        query_data: dict
) -> ReposReturn:
    is_success, response = await service_ekyc.get_list_kss(
        query_data=query_data
    )
    if not is_success:
        return ReposReturn(is_error=True, loc="LIST KSS", detail=response.get('message'))
    # for item in response.get('detail'):
    #     if item['status'] == STATUS_SUCCESS and not item['kss_status']:
    #         item['kss_status'] = "Chờ hậu kiểm"
    #         item['date_kss'] = item['trans_date']

    return ReposReturn(data={
        'detail': response.get('detail'),
        'total_page': response.get('total_page'),
        'total_record': response.get('total_record'),
        'page': response.get('page')
    })


async def repos_get_list_branch(query_param: dict) -> ReposReturn:
    is_success, response = await service_ekyc.get_list_branch(
        query_param=query_param
    )

    return ReposReturn(data=response)


async def repos_get_list_zone() -> ReposReturn:
    is_success, response = await service_ekyc.get_list_zone()

    return ReposReturn(data=response)


async def repos_get_statistics_profiles(query_data) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics_profiles(query_data)

    if not is_success:
        return ReposReturn(is_error=True, loc="STATISTICS PROFILES", detail=response.get('message'))

    return ReposReturn(data=response)


async def repos_get_statistics_month(months: int) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics_months(months=months)
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_EKYC, detail=str(response))

    return ReposReturn(data=response)


async def repos_get_history_post_post_check(postcheck_uuid: str) -> ReposReturn:
    is_success, response = await service_ekyc.get_history_post_check(
        postcheck_uuid=postcheck_uuid
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response.get('message'),
            detail=response.get('message')
        )

    return ReposReturn(data=response)


async def repos_update_post_check(request_data: dict) -> ReposReturn:
    is_success, response = await service_ekyc.update_post_check(request_data=request_data)

    if not is_success:
        return ReposReturn(is_error=True, loc="UPDATE_POST_CHECK", detail=response.get('message'))

    return ReposReturn(data=response)


async def repos_get_statistics(query_param: dict) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics(query_param)

    if not is_success and response['detail']:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response['detail'],
            detail=response['detail']
        )

    return ReposReturn(data=response)


async def repos_get_customer_detail(postcheck_uuid: str) -> ReposReturn:
    is_success, response = await service_ekyc.get_customer_detail(postcheck_uuid=postcheck_uuid)

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response['message'],
            detail=response['message']
        )

    return ReposReturn(data=response)


async def repos_create_post_check(payload_data: dict) -> ReposReturn:
    is_success, response = await service_ekyc.create_post_check(
        payload_data=payload_data,
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc='CREATE_POST_CHECK',
            msg=ERROR_CALL_SERVICE_EKYC,
            detail=str(response.get('post_control'))
        )

    return ReposReturn(data=(is_success, response))


async def repos_get_post_control(query_params) -> ReposReturn:
    is_success, response = await service_ekyc.get_post_control(
        query_params=query_params
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=ERROR_CALL_SERVICE_EKYC,
            msg=response['message'],
            detail=response['message']
        )
    return ReposReturn(data=response)


async def repos_save_customer_ekyc(
        body_request: dict,
):
    is_success, response = await service_ekyc.save_customer_ekyc(
        body_data=body_request,
    )

    return ReposReturn(data=response)
