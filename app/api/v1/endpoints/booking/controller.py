from app.api.base.controller import BaseController
from app.api.v1.endpoints.booking.repository import (
    get_list_comment, repo_add_comment
)
from app.api.v1.endpoints.booking.schema import NewsCommentRequest
from app.third_parties.oracle.models.cif.form.model import Booking
from app.third_parties.services.idm import ServiceIDM
from app.utils.functions import generate_uuid, now


class CtrNewsComment(BaseController):
    async def ctr_news_comment(self, data_comment: NewsCommentRequest, booking_id):
        # Validate: check tồn tại booking_id
        await self.get_model_object_by_id(model_id=booking_id, model=Booking, loc="booking_id")
        current_user = self.current_user.user_info

        uuid = generate_uuid()
        data_insert = {
            "booking_id": booking_id,
            "username": current_user.username,
            "avatar_url": ServiceIDM().replace_with_cdn(current_user.avatar_url),
            "name": current_user.name,
            "code": current_user.code,
            "email": current_user.email,
            "hrm_department_id": current_user.hrm_department_id,
            "hrm_department_code": current_user.hrm_department_code,
            "hrm_department_name": current_user.hrm_department_name,
            "hrm_branch_id": current_user.hrm_branch_id,
            "hrm_branch_code": current_user.hrm_branch_code,
            "hrm_branch_name": current_user.hrm_branch_name,
            "hrm_title_id": current_user.hrm_title_id,
            "hrm_title_code": current_user.hrm_title_code,
            "hrm_title_name": current_user.hrm_title_name,
            "hrm_position_id": current_user.hrm_position_id,
            "hrm_position_code": current_user.hrm_position_code,
            "hrm_position_name": current_user.hrm_position_name,
            "content": data_comment.content,
            "created_at": now(),
            "updated_at": now(),
            "file_uuid": "[]"
        }

        self.call_repos(
            await repo_add_comment(
                data_comment=data_insert,
                session=self.oracle_session
            )
        )
        return self.response(data={
            "comment_id": uuid
        })

    async def ctr_get_comment_by_booking_id(self, booking_id: str):
        # Validate: check tồn tại booking_id
        await self.get_model_object_by_id(model_id=booking_id, model=Booking, loc="booking_id")
        comments = self.call_repos(await get_list_comment(self.oracle_session, booking_id))

        return self.response(data=[dict(
            id=cmt_item.id,
            booking_id=cmt_item.booking_id,
            username=cmt_item.username,
            name=cmt_item.name,
            code=cmt_item.code,
            email=cmt_item.email,
            hrm_department_id=cmt_item.hrm_department_id,
            hrm_department_code=cmt_item.hrm_department_code,
            hrm_department_name=cmt_item.hrm_department_name,
            hrm_branch_id=cmt_item.hrm_branch_id,
            hrm_branch_code=cmt_item.hrm_branch_code,
            hrm_branch_name=cmt_item.hrm_branch_name,
            hrm_title_id=cmt_item.hrm_title_id,
            hrm_title_code=cmt_item.hrm_title_code,
            hrm_title_name=cmt_item.hrm_title_name,
            hrm_position_id=cmt_item.hrm_position_id,
            hrm_position_code=cmt_item.hrm_position_code,
            hrm_position_name=cmt_item.hrm_position_name,
            content=cmt_item.content,
            created_at=cmt_item.created_at,
            updated_at=cmt_item.updated_at,
            file_uuid=cmt_item.file_uuid
        ) for cmt_item in comments])
