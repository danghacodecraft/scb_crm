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
    status, data_idm = await service_idm.login(username=username, password=password)
    detail = None
    if not status:
        for key, item in data_idm.items():
            detail = data_idm[key][0]

        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_IDM,
            detail=detail
        )
    data = {
        "user_info": {
            "token": data_idm['user_info']['token'],
            "username": data_idm['user_info']['username'],
            "email": data_idm['user_info']['email'],
            "full_name_vn": data_idm['user_info']['name'],
            "user_id": str(USER_ID),
            "avatar_url": "cdn/users/avatar/dev1.jpg"
        }
    }
    return ReposReturn(data=data)


async def repos_check_token(token: str) -> ReposReturn:
    if token == USER_TOKEN:
        return ReposReturn(data=USER_INFO)
    else:
        return ReposReturn(is_error=True, msg=ERROR_INVALID_TOKEN, loc='token')


async def repos_get_user_info(user_id: str) -> ReposReturn:
    if user_id == USER_ID:
        return ReposReturn(data=USER_INFO)
    else:
        return ReposReturn(is_error=True, msg=USER_ID_NOT_EXIST, loc='user_id')
