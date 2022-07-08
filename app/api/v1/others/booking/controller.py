from typing import Optional

from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session
from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.others.booking.repository import (
    repos_check_exist_booking, repos_create_booking, repos_get_booking,
    repos_get_business_type, repos_get_customer_from_booking_account,
    repos_get_customer_from_booking_account_amount_block,
    repos_get_customer_from_booking_customer, repos_is_correct_booking,
    repos_is_used_booking
)
from app.api.v1.others.permission.controller import PermissionController
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.utils.constant.approval import CIF_STAGE_INIT
from app.utils.constant.business_type import BUSINESS_TYPES
from app.utils.constant.casa import CASA_ACCOUNT_STATUS_APPROVED
from app.utils.constant.cif import (
    BUSINESS_TYPE_CODE_AMOUNT_BLOCK, BUSINESS_TYPE_CODE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_CODE_CIF, BUSINESS_TYPE_CODE_CLOSE_CASA,
    BUSINESS_TYPE_CODE_OPEN_CASA, BUSINESS_TYPE_CODE_TOP_UP_CASA
)
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_GDV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_GDV
)
from app.utils.error_messages import (
    ERROR_BOOKING_ALREADY_USED, ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST,
    ERROR_BOOKING_ID_NOT_EXIST, ERROR_BOOKING_INCORRECT,
    ERROR_BUSINESS_TYPE_CODE_INCORRECT, ERROR_BUSINESS_TYPE_NOT_EXIST,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_CIF_ID_NOT_EXIST,
    ERROR_CUSTOMER_NOT_EXIST, ERROR_PERMISSION
)


class CtrBooking(BaseController):
    async def ctr_create_booking(
            self,
            business_type_code: Optional[str] = None,
            booking_code_flag: bool = True,
            transaction_id: Optional[str] = None
    ):
        is_stage_teller = self.call_repos(await PermissionController.ctr_approval_check_permission_stage(
            auth_response=self.current_user,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_GDV,
            permission_code=IDM_PERMISSION_CODE_GDV,
            stage_code=CIF_STAGE_INIT
        ))
        if not is_stage_teller:
            return self.response_exception(
                loc=f"IDM_MENU_CODE: {IDM_MENU_CODE_TTKH}, "
                    f"IDM_GROUP_ROLE_CODE: {IDM_GROUP_ROLE_CODE_GDV}, "
                    f"IDM_PERMISSION_CODE: {IDM_PERMISSION_CODE_GDV}",
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
            booking_id=booking_id,
            booking_code=booking_code
        ))

    async def ctr_get_booking_and_validate(
            self,
            booking_id: Optional[str],
            loc: str,
            business_type_code: str,
            cif_id: Optional[str] = None,
            check_correct_booking_flag: Optional[bool] = True,
    ):
        """
        check_correct_booking_flag: Đối với step đầu tiên của module, param này bằng False và phải truyền cif id
        """
        booking = None
        if booking_id:
            booking = self.call_repos(await repos_check_exist_booking(
                booking_id=booking_id,
                session=self.oracle_session
            ))

        if not booking:
            return self.response_exception(msg=ERROR_BOOKING_ID_NOT_EXIST, loc=loc)

        if booking.business_type_id != business_type_code:
            return self.response_exception(msg=ERROR_BUSINESS_TYPE_CODE_INCORRECT, loc="booking -> business_type_code")

        # Kiểm tra booking bước trước đó có giống với booking bước hiện tại không
        if check_correct_booking_flag:
            if not cif_id:
                return self.response_exception(msg=ERROR_CIF_ID_NOT_EXIST, loc=f"cif_id: {cif_id}")
            is_correct_booking = await repos_is_correct_booking(
                booking_id=booking_id,
                cif_id=cif_id,
                session=self.oracle_session
            )
            if not is_correct_booking:
                return self.response_exception(msg=ERROR_BOOKING_INCORRECT, loc="header -> booking_id")

        return self.response(data=booking)

    async def is_used_booking(self, booking_id: str):
        is_used_booking = await repos_is_used_booking(booking_id=booking_id, session=self.oracle_session)
        if is_used_booking:
            return self.response_exception(msg=ERROR_BOOKING_ALREADY_USED, loc=f"booking_id: {booking_id}")

        return self.response(data=is_used_booking)

    async def ctr_get_business_type(self, booking_id: str):
        """
        Lấy thông tin nghiệp vụ thông qua booking
        """
        business_type = self.call_repos(await repos_get_business_type(
            booking_id=booking_id,
            session=self.oracle_session
        ))
        return business_type

    async def ctr_get_booking(self, booking_id: str):
        """
        Lấy thông tin nghiệp vụ thông qua booking
        """
        booking = self.call_repos(await repos_get_booking(
            booking_id=booking_id,
            session=self.oracle_session
        ))
        if not booking:
            return self.response_exception(msg=ERROR_BOOKING_ID_NOT_EXIST, loc=f"booking_id: {booking_id}")
        return booking

    async def ctr_get_customer_from_booking(self, booking_id: str):
        booking = await self.ctr_get_booking(booking_id=booking_id)
        customer = None
        business_type_id = booking.business_type.id

        # Mở CIF
        if business_type_id == BUSINESS_TYPE_CODE_CIF:
            customer = self.call_repos(await repos_get_customer_from_booking_customer(
                booking_id=booking_id, session=self.oracle_session
            ))

        # Mở TKTT
        if booking.business_type.id == BUSINESS_TYPE_CODE_OPEN_CASA:
            customer = self.call_repos(await repos_get_customer_from_booking_account(
                booking_id=booking_id, session=self.oracle_session
            ))

        # Phong tỏa, giải tỏa
        if business_type_id in [
            BUSINESS_TYPE_CODE_AMOUNT_BLOCK,
            BUSINESS_TYPE_CODE_AMOUNT_UNBLOCK,
            BUSINESS_TYPE_CODE_TOP_UP_CASA,
            BUSINESS_TYPE_CODE_CLOSE_CASA
        ]:
            customer = self.call_repos(await repos_get_customer_from_booking_account_amount_block(
                booking_id=booking_id, session=self.oracle_session
            ))

        if not customer:
            return self.response_exception(
                msg=ERROR_CUSTOMER_NOT_EXIST,
                loc=f"booking_id: {booking_id}"
            )

        return customer

    async def ctr_get_casa_account_from_booking(self, booking_id: str, session: Session):
        casa_accounts = session.execute(
            select(
                CasaAccount,
                Booking,
                BookingAccount
            )
            .join(BookingAccount, Booking.id == BookingAccount.booking_id)
            .join(CasaAccount, BookingAccount.account_id == CasaAccount.id)
            .filter(Booking.parent_id == booking_id)
        ).scalars().all()

        if not casa_accounts:
            return self.response_exception(msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc=f'booking_id: {booking_id}')

        approved_casa_account_ids = []
        for casa_account in casa_accounts:
            if casa_account.approve_status == CASA_ACCOUNT_STATUS_APPROVED:
                approved_casa_account_ids.append(casa_account.id)

        return casa_accounts

    async def ctr_get_booking_business_form(self, booking_id: str, session: Session):
        booking_business_form = session.execute(
            select(
                BookingBusinessForm,
                Booking
            )
            .join(BookingBusinessForm, and_(
                Booking.id == BookingBusinessForm.booking_id,
                BookingBusinessForm.business_form_id.notilike('%_GW')
            ))
            .filter(Booking.id == booking_id)
            .order_by(desc(BookingBusinessForm.created_at))
        ).scalars().all()
        if not booking_business_form:
            return self.response_exception(msg=ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST, loc=f"booking_id: {booking_id}")
        return booking_business_form[0]
