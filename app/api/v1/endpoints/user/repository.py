import base64
import binascii
import zlib

import orjson
from starlette import status

from app.api.base.repository import ReposReturn
from app.settings.event import service_idm
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_IDM, ERROR_INVALID_TOKEN, USER_ID_NOT_EXIST
)

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
    detail = None

    if not is_success:
        for key, item in data_idm.items():
            detail = data_idm[key][0]

        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_IDM,
            detail=detail
        )
    data_idm['user_info']['token'] = base64.b64encode(
        zlib.compress(orjson.dumps(data_idm))
    ).decode('utf-8')

    try:
        # Check has permission in IDM
        filter_code = list(filter(lambda x: x.get('menu_code') == "CRM", data_idm['menu_list']))[0]
        filter_group_code = list(filter(lambda x: x.get('group_role_code') == "QUANLY", filter_code['group_role_list']))[0]
    except IndexError:
        return ReposReturn(
            is_error=True,
            msg="Permission Denied",
            detail="Permission Denied",
            error_status_code=status.HTTP_403_FORBIDDEN
        )
    filter_permission_code = list(filter(lambda x: x.get('permission_code') == "ACCESS", filter_group_code['permission_list']))

    if not filter_permission_code or not filter_group_code['is_permission']:
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
        return ReposReturn(is_error=True, msg=ERROR_INVALID_TOKEN, loc='token')

    status, check_token = await service_idm.check_token(username=auth_parts['user_info']['username'], bearer_token=auth_parts['user_info']['token'])

    if not status:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_IDM,
            detail="Token is invalid"
        )
    return ReposReturn(data=auth_parts)


async def repos_get_user_info(user_id: str) -> ReposReturn:
    if user_id == USER_ID:
        return ReposReturn(data=USER_INFO)
    else:
        return ReposReturn(is_error=True, msg=USER_ID_NOT_EXIST, loc='user_id')
