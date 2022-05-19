from typing import Optional

from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.others.booking.repository import (
    repos_check_exist_booking, repos_create_booking
)
from app.api.v1.others.permission.controller import PermissionController
from app.utils.constant.approval import CIF_STAGE_INIT
from app.utils.constant.business_type import BUSINESS_TYPES
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_OPEN_CIF, IDM_MENU_CODE_OPEN_CIF,
    IDM_PERMISSION_CODE_OPEN_CIF
)
from app.utils.error_messages import (
    ERROR_BOOKING_ID_NOT_EXIST, ERROR_BUSINESS_TYPE_NOT_EXIST, ERROR_PERMISSION
)


class CtrBooking(BaseController):
    async def ctr_create_booking(
            self,
            business_type_code: Optional[str] = None,
            booking_code_flag: bool = False,
            transaction_id: Optional[str] = None
    ):
        is_stage_teller = self.call_repos(await PermissionController.ctr_approval_check_permission_stage(
            auth_response=self.current_user,
            menu_code=IDM_MENU_CODE_OPEN_CIF,
            group_role_code=IDM_GROUP_ROLE_CODE_OPEN_CIF,
            permission_code=IDM_PERMISSION_CODE_OPEN_CIF,
            stage_code=CIF_STAGE_INIT
        ))
        if not is_stage_teller:
            return self.response_exception(
                loc=f"IDM_MENU_CODE: {IDM_MENU_CODE_OPEN_CIF}, "
                    f"IDM_GROUP_ROLE_CODE: {IDM_GROUP_ROLE_CODE_OPEN_CIF}, "
                    f"IDM_PERMISSION_CODE: {IDM_PERMISSION_CODE_OPEN_CIF}",
                msg=ERROR_PERMISSION,
                error_status_code=status.HTTP_403_FORBIDDEN
            )

        if business_type_code not in BUSINESS_TYPES:
            return self.response_exception(msg=ERROR_BUSINESS_TYPE_NOT_EXIST)

        booking = self.call_repos(await repos_create_booking(
            business_type_code=business_type_code,
            transaction_id=transaction_id,
            current_user=self.current_user.user_info,
            session=self.oracle_session,
            booking_code_flag=booking_code_flag
        ))
        booking_id, booking_code = booking

        return self.response(data=dict(
            booking_id=booking_id
        ))

    async def ctr_get_booking(self, booking_id: Optional[str], loc: str, business_type_code: str):
        if booking_id:
            booking = self.call_repos(await repos_check_exist_booking(
                booking_id=booking_id,
                business_type_code=business_type_code,
                session=self.oracle_session
            ))

            if not booking:
                return self.response_exception(msg=ERROR_BOOKING_ID_NOT_EXIST, loc=loc)

        return self.response(data=booking)
