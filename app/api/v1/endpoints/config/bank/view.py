from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.bank.controller import CtrConfigBank
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/branch/",
    name="Bank Branch",
    description="Chi nhánh ngân hàng",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_bank_branch_info(
    current_user=Depends(get_current_user_from_header())
):
    bank_branch_info = await CtrConfigBank(current_user=current_user).ctr_get_bank_branch()
    return ResponseData[List[DropdownResponse]](**bank_branch_info)


@router.get(
    path="/",
    name="Bank",
    description="Ngân hàng",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_bank_info(
    napas_flag: bool = Query(False, description="Có Napas"),
    citad_flag: bool = Query(False, description="Có Citad"),
    current_user=Depends(get_current_user_from_header())
):
    bank_info = await CtrConfigBank(current_user=current_user).ctr_get_bank(
        napas_flag=napas_flag,
        citad_flag=citad_flag
    )
    return ResponseData[List[DropdownResponse]](**bank_info)
