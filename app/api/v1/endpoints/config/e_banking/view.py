from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.e_banking.controller import CtrConfigEBanking
from app.api.v1.endpoints.config.e_banking.schema import (
    EBankingQuestionResponse
)
from app.api.v1.schemas.utils import DropdownResponse
from app.utils.constant.cif import EB_QUESTION_TYPE

router = APIRouter()


@router.get(
    path="/eb-notification/",
    name="E-Banking Notification",
    description="Lấy dữ liệu Tùy chọn thông báo",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_e_banking_notification_info(
        type_id: str = Query(
            ...,
            description="Loại thông báo: "
                        "<br>`DD` Biến động số dư tài khoản Thanh toán"
                        "<br>`FD` Biến động số dư tài khoản Tiết kiệm",
            min_length=1
        ),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_notification_info = await CtrConfigEBanking(current_user).ctr_e_banking_notification_info(type_id=type_id)
    return ResponseData[List[DropdownResponse]](**e_banking_notification_info)


@router.get(
    path="/eb-question/",
    name="E-Banking Question",
    description="Lấy dữ liệu Danh sách câu hỏi",
    responses=swagger_response(
        response_model=ResponseData[List[EBankingQuestionResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_e_banking_question_info(
        e_banking_question_type: str = Query(..., description=f"Loại câu hỏi {EB_QUESTION_TYPE}"),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_question_info = await CtrConfigEBanking(current_user).ctr_e_banking_question_info(
        e_banking_question_type=e_banking_question_type
    )
    return ResponseData[List[EBankingQuestionResponse]](**e_banking_question_info)
