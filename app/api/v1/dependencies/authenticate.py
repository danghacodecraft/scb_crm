import base64
from typing import Callable, Optional, Union

from fastapi import Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials, HTTPBasic, HTTPBearer
)

from app.api.base.except_custom import ExceptionHandle
from app.api.v1.endpoints.user.repository import repos_check_token
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_INVALID_TOKEN

bearer_token = HTTPBearer()

basic_auth = HTTPBasic()


def get_current_user_from_header(is_require_login: bool = True) -> Callable:
    return _get_authorization_header if is_require_login else _get_authorization_header_optional


def check_token_ekyc(credentials) -> bool:
    try:
        auth_parts = base64.b64decode(credentials)
        auth_parts = auth_parts.decode('utf-8').split(':')
    except UnicodeDecodeError:
        return False

    if auth_parts:
        if auth_parts[0] == SERVICE['ekyc']['token'] and auth_parts[1] == SERVICE['ekyc']['otp']:
            return True
    return False


async def _get_authorization_header(
        scheme_and_credentials: HTTPAuthorizationCredentials = Security(bearer_token),
) -> Union[AuthResponse, bool]:
    # bypass token check if service ekyc
    if check_token_ekyc(scheme_and_credentials.credentials):
        return AuthResponse(**{"user_info": {"token": ""}, "menu_list": []})
    result_check_token = await repos_check_token(token=scheme_and_credentials.credentials)
    if result_check_token.is_error:
        raise ExceptionHandle(
            errors=[{'loc': None, 'msg': ERROR_INVALID_TOKEN}],
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return AuthResponse(**result_check_token.data)


async def _get_authorization_header_optional(
        scheme_and_credentials: Optional[HTTPAuthorizationCredentials] = Security(HTTPBearer(auto_error=False))
) -> Union[AuthResponse, None]:
    if scheme_and_credentials:
        return await _get_authorization_header(
            scheme_and_credentials=scheme_and_credentials
        )
    return None
