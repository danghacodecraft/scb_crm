from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.endpoints.third_parties.gw.employee.example import (
    EMPLOYEE_CODE_EXAMPLE, EMPLOYEE_DISCIPLINE_CODE_EXAMPLE,
    EMPLOYEE_DISCIPLINE_SUCCESS_EXAMPLE, EMPLOYEE_INFO_CODE_EXAMPLE,
    EMPLOYEE_INFO_SUCCESS_EXAMPLE, EMPLOYEE_KPIS_SUCCESS_EXAMPLE,
    EMPLOYEE_LIST_SUCCESS_EXAMPLE, EMPLOYEE_REWARD_CODE_EXAMPLE,
    EMPLOYEE_REWARD_SUCCESS_EXAMPLE, EMPLOYEE_STAFF_OTHER_CODE_EXAMPLE,
    EMPLOYEE_STAFF_OTHER_SUCCESS_EXAMPLE, EMPLOYEE_TOPIC_SUCCESS_EXAMPLE,
    EMPLOYEE_USER_NAME_EXAMPLE, EMPLOYEE_WORKING_PROCESS_SUCCESS_EXAMPLE,
    ORG_ID_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.employee.schema import (
    GWEmployeeDisciplineResponse, GWEmployeeInfoResponse,
    GWEmployeeKpisResponse, GWEmployeeListResponse, GWEmployeeRewardResponse,
    GWEmployeeStaffOtherResponse, GWEmployeeTopicResponse,
    GWEmployeeWorkingProcessResponse, GWRetrieveEmployeeResponse
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


@router.post(
    path="/list/{org_id}/",
    name="[GW] Lấy danh sách nhân viên theo org id",
    description="Lấy danh sách nhân viên theo org id",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeInfoResponse],
        success_examples=EMPLOYEE_LIST_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_employee_list_from_org_id(
        org_id: str = Path(..., example=ORG_ID_EXAMPLE, description="Mã tổ chức"),
        current_user=Depends(get_current_user_from_header())
):
    employee_infos = await CtrGWEmployee(current_user).ctr_gw_get_employee_list_from_org_id(
        org_id=org_id
    )
    return ResponseData[GWEmployeeListResponse](**employee_infos)


@router.post(
    path="/retrieve/code/{staff_code}",
    name="[GW] Lấy thông tin chi tiết nhân viên theo mã nhân viên",
    description="Lấy thông tin chi tiết nhân viên theo mã nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWRetrieveEmployeeResponse],
        success_examples=EMPLOYEE_LIST_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_retrieve_employee_info_from_code(
        staff_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_INFO_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    employee_info = await CtrGWEmployee(current_user).ctr_gw_get_retrieve_employee_info_from_code(
        staff_code=staff_code
    )
    return ResponseData[GWRetrieveEmployeeResponse](**employee_info)


@router.post(
    path="/working-process/{staff_code}",
    name="[GW] Lấy thông tin quá trình công tác theo mã nhân viên",
    description="Lấy thông tin quá trình công tác theo mã nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeWorkingProcessResponse],
        success_examples=EMPLOYEE_WORKING_PROCESS_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_working_process_info_from_code(
        staff_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    working_process_info = await CtrGWEmployee(current_user).ctr_gw_get_working_process_info_from_code(
        staff_code=staff_code
    )
    return ResponseData[GWEmployeeWorkingProcessResponse](**working_process_info)


@router.post(
    path="/reward/{staff_code}",
    name="[GW] Lấy thông tin khen thưởng theo mã nhân viên",
    description="Lấy thông tin khen thưởng theo mã nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeRewardResponse],
        success_examples=EMPLOYEE_REWARD_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_reward_info_from_code(
        staff_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_REWARD_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    working_process_info = await CtrGWEmployee(current_user).ctr_gw_get_reward_info_from_code(
        staff_code=staff_code
    )
    return ResponseData[GWEmployeeRewardResponse](**working_process_info)


@router.post(
    path="/discipline/{staff_code}",
    name="[GW] Lấy thông tin kỷ luật theo mã nhân viên",
    description="Lấy thông tin kỷ luật theo mã nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeDisciplineResponse],
        success_examples=EMPLOYEE_DISCIPLINE_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_discipline_info_from_code(
        staff_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_DISCIPLINE_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    discipline_info = await CtrGWEmployee(current_user).ctr_gw_get_discipline_info_from_code(
        staff_code=staff_code
    )
    return ResponseData[GWEmployeeDisciplineResponse](**discipline_info)


@router.post(
    path="/topic/{staff_code}",
    name="[GW] Lấy thông tin đào tạo nội bộ theo mã nhân viên",
    description="Lấy thông tin đào tạo nội bộ theo mã nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeTopicResponse],
        success_examples=EMPLOYEE_TOPIC_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_topic_info_from_code(
        staff_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_INFO_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    working_process_info = await CtrGWEmployee(current_user).ctr_gw_get_topic_info_from_code(
        staff_code=staff_code
    )
    return ResponseData[GWEmployeeTopicResponse](**working_process_info)


@router.post(
    path="/kpis/{staff_code}",
    name="[GW] Lấy thông tin hiệu quả công việc theo mã nhân viên",
    description="Lấy thông tin hiệu quả công việc theo mã nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeKpisResponse],
        success_examples=EMPLOYEE_KPIS_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_kpis_info_from_code(
        staff_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_INFO_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    kpis_info = await CtrGWEmployee(current_user).ctr_gw_get_kpis_info_from_code(
        staff_code=staff_code
    )
    return ResponseData[GWEmployeeKpisResponse](**kpis_info)


@router.post(
    path="/staff-other/{staff_code}",
    name="[GW] Lấy thông tin khác theo mã nhân viên",
    description="Lấy thông tin khác theo mã nhân viên",
    responses=swagger_response(
        response_model=ResponseData[GWEmployeeStaffOtherResponse],
        success_examples=EMPLOYEE_STAFF_OTHER_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_staff_other_info_from_code(
        staff_code: str = Path(..., description="Mã số nhân viên", example=EMPLOYEE_STAFF_OTHER_CODE_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    staff_other = await CtrGWEmployee(current_user).ctr_gw_get_staff_other_info_from_code(
        staff_code=staff_code
    )
    return ResponseData[GWEmployeeStaffOtherResponse](**staff_other)
