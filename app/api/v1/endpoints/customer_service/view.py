from typing import List

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.customer_service.controller import CtrKSS
from app.api.v1.endpoints.customer_service.schema import (
    BranchResponse, CreatePostCheckRequest, CustomerDetailResponse,
    HistoryPostCheckResponse, KSSResponse, PostControlResponse,
    QueryParamsKSSRequest, StatisticsMonth, StatisticsProfilesResponse,
    StatisticsResponse, UpdatePostCheckRequest, ZoneRequest
)

router = APIRouter()


@router.get(
    path="/",
    name="Kiểm Soát Sau",
    description="Truy suất danh sách hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[KSSResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_kss(
        query_params: QueryParamsKSSRequest = Depends(),
        current_user=Depends(get_current_user_from_header())
):
    kss_response = await CtrKSS(current_user).ctr_get_list_kss(
        query_params=query_params
    )

    return ResponseData[KSSResponse](**kss_response)


@router.get(
    path="/branch/",
    name="Danh sách đơn vị",
    description="Truy suất danh sách đơn vị",
    responses=swagger_response(
        response_model=ResponseData[List[BranchResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_branch(
        zone_id: int = Query(None, description='Zone ID', nullable=True),
        current_user=Depends(get_current_user_from_header())
):
    branch_response = await CtrKSS(current_user).ctr_get_list_branch(zone_id=zone_id)

    return ResponseData[List[BranchResponse]](**branch_response)


@router.get(
    path="/zone/",
    name="Danh sách vùng",
    description="Truy suất danh sách vùng",
    responses=swagger_response(
        response_model=ResponseData[List[ZoneRequest]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_zone(
        current_user=Depends(get_current_user_from_header())
):
    zone_response = await CtrKSS(current_user).ctr_get_list_zone()

    return ResponseData[List[ZoneRequest]](**zone_response)


@router.get(
    path="/customer/postcontrol/{postcheck_uuid}/",
    name="Thông tin hậu kiểm của khách hàng",
    description="Thông tin hậu kiểm của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[PostControlResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_post_control(
        postcheck_uuid: str = Path(..., description='Id của khách hàng'),
        post_control_his_id: int = Query(None, description='ID lịch sử hậu kiểm'),
        current_user=Depends(get_current_user_from_header())
):
    post_control_response = await CtrKSS(current_user).ctr_get_post_control(
        postcheck_uuid=postcheck_uuid,
        post_control_his_id=post_control_his_id
    )

    return ResponseData[PostControlResponse](**post_control_response)


@router.get(
    path="/history/{postcheck_uuid}/",
    name="Lịch sử hậu kiểm",
    description="Lịch sử hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[List[HistoryPostCheckResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_history_post_check(
        postcheck_uuid: str = Path(..., description='Id của khách hàng'),
        current_user=Depends(get_current_user_from_header())
):
    history_post_check = await CtrKSS(current_user).ctr_history_post_check(
        postcheck_uuid=postcheck_uuid
    )

    return ResponseData[List[HistoryPostCheckResponse]](**history_post_check)


@router.get(
    path="/statistics/months/",
    name="Thống kê theo tháng",
    description="Thống kê theo tháng",
    responses=swagger_response(
        response_model=ResponseData[List[StatisticsMonth]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_statistics_month(
        months: int = Query(..., description='Số tháng để thống kê'),
        current_user=Depends(get_current_user_from_header())
):
    statistics_month_response = await CtrKSS(current_user).ctr_statistics_month(
        months=months
    )

    return ResponseData[List[StatisticsMonth]](**statistics_month_response)


@router.get(
    path="/statistics/profiles/",
    name="Thống kê hồ sơ hậu kiểm",
    description="Thống kê hồ sơ hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[StatisticsProfilesResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_statistics_profiles(
        selected_date: str = Query(None, description='Chọn ngày kết thúc DD/MM/YYYY'),
        start_date: str = Query(None, description='Chọn ngày'),
        end_date: str = Query(None, description='Chọn ngày bắt đầu DD/MM/YYYY'),
        current_user=Depends(get_current_user_from_header())
):
    statistics_profiles = await CtrKSS(current_user).ctr_get_statistics_profiles()

    return ResponseData[StatisticsProfilesResponse](**statistics_profiles)


@router.get(
    path="/statistics/",
    name="Thống kê số liệu API POST",
    description="Thống kê số liệu API POST",
    responses=swagger_response(
        response_model=ResponseData[List[StatisticsResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_statistics(
        search_type: int = Query(None, description="""Loại tìm kiếm
            \n `search_type` = 1, hiển thị theo ngày
            \n `search_type` = 2, hiển thị theo tuần
            \n `search_type` = 3, hiển thị theo tháng
            \n `search_type` = 4, hiển thị theo năm
            """),
        selected_date: str = Query(None, description='Chọn ngày `DD/MM/YYYY`'),
        current_user=Depends(get_current_user_from_header())
):
    statistics = await CtrKSS(current_user).ctr_get_statistics(search_type=search_type, selected_date=selected_date)

    return ResponseData[List[StatisticsResponse]](**statistics)


@router.post(
    path="/",
    name="Thêm mới hậu kiểm",
    description="Thêm mới hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[CreatePostCheckRequest],
        success_status_code=status.HTTP_200_OK
    )
)
async def create_post_check(
        post_check_request: CreatePostCheckRequest,
        current_user=Depends(get_current_user_from_header())
):
    post_check = await CtrKSS(current_user).ctr_create_post_check(post_check_request=post_check_request)

    return ResponseData[CreatePostCheckRequest](**post_check)


@router.put(
    path="/",
    name="Phê duyệt hậu kiểm",
    description="Phê duyệt hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[UpdatePostCheckRequest],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_post_check(
        postcheck_update_request: UpdatePostCheckRequest,
        current_user=Depends(get_current_user_from_header())
):
    update_postcheck = await CtrKSS(current_user).ctr_update_post_check(postcheck_update_request=postcheck_update_request)

    return ResponseData[UpdatePostCheckRequest](**update_postcheck)


@router.get(
    path="/customer/{postcheck_uuid}",
    name="Chi tiết thông tin khách hàng",
    description="Chi tiết thông tin khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CustomerDetailResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customer(
        postcheck_uuid: str = Path(..., description='ID của khách hàng'),
        current_user=Depends(get_current_user_from_header())
):
    customer_detail_information = await CtrKSS(current_user).ctr_get_customer_detail(postcheck_uuid=postcheck_uuid)

    return ResponseData[CustomerDetailResponse](**customer_detail_information)


# @router.post(
#     path="/customer/",
#     name="Tạo khách hàng",
#     description="Tạo khách hàng",
#     responses=swagger_response(
#         response_model=ResponseData[CustomerDetailResponse],
#         success_status_code=status.HTTP_200_OK
#     )
# )
# async def save_customer_ekyc(
#     current_user=Depends(get_current_user_from_header())
# ):
#     customer = await CtrKSS(current_user).ctr_save_customer()
#
#     return ResponseData(**customer)
