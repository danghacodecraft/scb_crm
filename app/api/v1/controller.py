from typing import Optional

from starlette import status

from app.api.base.controller import BaseController
from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.utils.error_messages import ERROR_PERMISSION, MESSAGE_STATUS


class PermissionController(BaseController):
    @staticmethod
    async def ctr_approval_check_permission(
            auth_response: AuthResponse,
            menu_code: str,
            group_role_code: str,
            permission_code: str,
            stage_code: Optional[str] = None
    ):
        """
        Check has permission in IDM
        Return: ReposReturn(None/Error)
        """
        current_user = auth_response.user_info
        menu_list = auth_response.menu_list
        try:
            filter_code = list(filter(lambda x: x.menu_code == menu_code, menu_list))[0]
            filter_group_code = \
                list(filter(lambda x: x.group_role_code == group_role_code, filter_code.group_role_list))[0]
        except IndexError:
            return ReposReturn(
                is_error=True,
                msg=ERROR_PERMISSION,
                loc=f"Stage: {stage_code}, User: {current_user.code}",
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )
        filter_permission_code = list(filter(
            lambda x: x.permission_code == permission_code, filter_group_code.permission_list
        ))

        if not filter_permission_code or not filter_group_code.is_permission:
            return ReposReturn(
                is_error=True,
                loc=f"Stage: {stage_code}, User: {current_user.code}",
                msg=ERROR_PERMISSION,
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN
            )
        return ReposReturn(data=None)

    @staticmethod
    async def ctr_approval_check_permission_stage(
            auth_response: AuthResponse,
            menu_code: str,
            group_role_code: str,
            permission_code: str,
            stage_code: Optional[str] = None
    ) -> ReposReturn:
        """
        Kiểm tra xem User có được thao tác ở bước đó không
        Return: ReposReturn(True/False/Error)
        """
        current_user = auth_response.user_info
        menu_list = auth_response.menu_list
        try:
            filter_code = list(filter(lambda x: x.menu_code == menu_code, menu_list))[0]
            filter_group_code = \
                list(filter(lambda x: x.group_role_code == group_role_code, filter_code.group_role_list))[0]
        except IndexError:
            return ReposReturn(
                is_error=True,
                msg=ERROR_PERMISSION,
                loc=f"Stage: {stage_code}, User: {current_user.code}",
                detail=MESSAGE_STATUS[ERROR_PERMISSION],
                error_status_code=status.HTTP_403_FORBIDDEN,
                data=False
            )
        filter_permission_code = list(filter(
            lambda x: x.permission_code == permission_code, filter_group_code.permission_list
        ))

        if not filter_permission_code or not filter_group_code.is_permission:
            return ReposReturn(data=False)
        return ReposReturn(data=True)
