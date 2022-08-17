import base64
import binascii
import zlib

import orjson
from starlette import status

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.event import (
    INIT_SERVICE, service_gw, service_idm, service_redis
)
from app.third_parties.services.idm import ServiceIDM
from app.utils.constant.gw import GW_FUNC_SELECT_USER_INFO_BY_USER_ID_OUT
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_CALL_SERVICE_IDM, ERROR_INVALID_TOKEN,
    USER_ID_NOT_EXIST
)
from app.utils.functions import string_to_date

USER_ID = "9651cdfd9a9a4eb691f9a3a125ac46b0"
USER_TOKEN = "OTY1MWNkZmQ5YTlhNGViNjkxZjlhM2ExMjVhYzQ2YjA6N2VlN2E2ZTg1MTUzN2M2YzFmYWIwMWQzODYzMWU4YTIx"

USER_INFO = {
    "user_id": str(USER_ID),
    "username": "dev1",
    "full_name_vn": "Developer 1",
    "avatar_url": "cdn/users/avatar/dev1.jpg",
    "token": "5deb5d337c8ae85564717dde65f4861930ae5c75",
    "email": "thanghd@scb.com.vn"
}


async def repos_get_list_user() -> ReposReturn:
    return ReposReturn(data=[USER_INFO])


async def repos_login(username: str, password: str) -> ReposReturn:
    is_success, data_idm = await service_idm.login(username=username, password=password)

    if not is_success:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_IDM,
            detail=str(data_idm)
        )

    is_success, data_gw = await service_gw.gw_detail_user(
        current_user=UserInfoResponse(**data_idm["user_info"]),
        data_input={
            "staff_info": {
                "staff_code": data_idm['user_info']['code']
            }
        }
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_GW, detail=str(data_gw))

    gw_data_output = data_gw[GW_FUNC_SELECT_USER_INFO_BY_USER_ID_OUT]['data_output']
    if gw_data_output:
        gw_data_output = gw_data_output[0]
        user_info = data_idm['user_info']
        user_info['hrm_title_name'] = gw_data_output['staff_info']['title_name']
        user_info['hrm_branch_code'] = gw_data_output['branch_info']['branch_code']
        user_info['hrm_branch_name'] = gw_data_output['branch_info']['branch_name']
        user_info['fcc_current_date'] = string_to_date(gw_data_output['current_date'])

    data_idm["user_info"]["avatar_url"] = ServiceIDM(init_service=INIT_SERVICE).replace_with_cdn(data_idm["user_info"]["avatar_url"])
    data_idm['user_info']['token'] = base64.b64encode(
        zlib.compress(orjson.dumps(data_idm['user_info']))
    ).decode('utf-8')

    await service_redis.getset(data_idm["user_info"]['username'], data_idm['menu_list'])

    lst_data = []
    list(map(lambda x: lst_data.extend(x['group_role_list']), data_idm['menu_list']))
    filter_permission_code = list(filter(
        lambda x: x.get('is_permission') is True,
        list(filter(
            lambda item: len(
                list(filter(
                    lambda permission: permission.get('permission_code') == "ACCESS", item['permission_list']))
            ) > 0, lst_data))

    ))

    if not filter_permission_code:
        return ReposReturn(
            is_error=True,
            msg="Permission Denied",
            detail="Permission Denied",
            error_status_code=status.HTTP_403_FORBIDDEN
        )

    return ReposReturn(data=data_idm)


async def repos_check_token(token: str) -> ReposReturn:
    try:
        auth_parts = orjson.loads(zlib.decompress(base64.b64decode(token)))
    except (TypeError, UnicodeDecodeError, binascii.Error, IndexError, zlib.error):
        return ReposReturn(
            is_error=True,
            msg=ERROR_INVALID_TOKEN,
            loc='token',
            error_status_code=status.HTTP_401_UNAUTHORIZED
        )

    username = auth_parts['username']

    is_success, check_token = await service_idm.check_token(username=username, bearer_token=auth_parts['token'])

    if not is_success:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_IDM,
            detail="Token is invalid"
        )

    menu_list = await service_redis.get(username)

    return ReposReturn(data=dict(
        user_info=auth_parts,
        menu_list=menu_list
    ))


async def repos_get_user_info(user_id: str) -> ReposReturn:
    if user_id == USER_ID:
        return ReposReturn(data=USER_INFO)
    else:
        return ReposReturn(is_error=True, msg=USER_ID_NOT_EXIST, loc='user_id')


async def repos_get_user_info_core_fcc(current_user):
    service_gw.gw_detail_user(current_user=current_user)


async def repos_get_list_banner():
    banner_list = await service_idm.banner_list()
    return ReposReturn(data=banner_list)
