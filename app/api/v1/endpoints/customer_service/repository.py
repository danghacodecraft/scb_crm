from app.api.base.repository import ReposReturn
from app.settings.event import service_ekyc


async def repos_get_list_kss(
        query_data: dict
) -> ReposReturn:
    is_success, response = await service_ekyc.get_list_kss(query_data=query_data)

    return ReposReturn(data={
        'detail': response.get('detail'),
        'total_page': response.get('total_page'),
        'total_record': response.get('total_record'),
        'page': response.get('page')
    })


async def repos_get_list_branch(query_param: dict) -> ReposReturn:
    is_success, response = await service_ekyc.get_list_branch(query_param=query_param)

    return ReposReturn(data=response)


async def repos_get_list_zone() -> ReposReturn:
    is_success, response = await service_ekyc.get_list_zone()

    return ReposReturn(data=response)


async def repos_get_statistics_profiles() -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics_profiles()

    return ReposReturn(data=response)


async def repos_get_statistics_month(months: int) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics_months(months=months)

    return ReposReturn(data=response)


async def repos_get_history_post_post_check(postcheck_uuid: str) -> ReposReturn:
    is_success, response = await service_ekyc.get_history_post_check(postcheck_uuid=postcheck_uuid)

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc='CALL_SERVICE_eKYC',
            msg=response.get('message'),
            detail=response.get('message')
        )

    return ReposReturn(data=response)


async def repos_update_post_check(request_data: dict) -> ReposReturn:
    is_success, response = await service_ekyc.update_post_check(request_data=request_data)

    return ReposReturn(data=response)


async def repos_get_statistics(query_param: dict) -> ReposReturn:
    is_success, response = await service_ekyc.get_statistics(query_param)

    if not is_success and response['detail']:
        return ReposReturn(
            is_error=True,
            loc='CALL_SERVICE_eKYC',
            msg=response['detail'],
            detail=response['detail']
        )

    return ReposReturn(data=response)


async def repos_get_customer_detail(postcheck_uuid: str) -> ReposReturn:

    is_success, response = await service_ekyc.get_customer_detail(postcheck_uuid=postcheck_uuid)
    return ReposReturn(data=response)
