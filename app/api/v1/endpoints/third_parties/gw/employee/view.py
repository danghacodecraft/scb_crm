from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.endpoints.third_parties.gw.employee.example import (
    EMPLOYEE_CODE_EXAMPLE, EMPLOYEE_INFO_SUCCESS_EXAMPLE,
    EMPLOYEE_USER_NAME_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.employee.schema import (
    GWEmployeeInfoResponse
)

router = APIRouter()


@router.post(
    path="/code/{employee_code}/",
    name="[GW] Lấy thông tin nhân viên theo mã số nhân viên",
    description="Lấy thông tin nhân viên theo mã số nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeInfoResponse],
        success_examples=EMPLOYEE_INFO_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_employee_info_from_code(
        employee_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    employee_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_code(
        employee_code=employee_code
    )
    return ResponseData[GWEmployeeInfoResponse](**employee_info)


@router.post(
    path="/user-name/{employee_name}/",
    name="[GW] Lấy thông tin nhân viên theo tên tài khoản nhân viên",
    description="Lấy thông tin nhân viên theo tên tài khoản nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeInfoResponse],
        success_examples=EMPLOYEE_INFO_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_employee_info_from_user_name(
        employee_name: str = Path(..., example=EMPLOYEE_USER_NAME_EXAMPLE, description="Tên tài khoản nhân viên"),
        current_user=Depends(get_current_user_from_header())
):
    employee_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_user_name(
        employee_name=employee_name
    )
    return ResponseData[GWEmployeeInfoResponse](**employee_info)
