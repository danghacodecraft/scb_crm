from datetime import date

from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import HTTPBasic
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.news.controller import CtrNews
from app.api.v1.endpoints.news.schema import (
    ListNewsResponse, NewsDetailResponse, NewsImageRequest, NewsResponse
)

router = APIRouter()
security = HTTPBasic()


@router.post(
    path="/",
    description="Tạo mới Tin tức SCB",
    name="Tạo mới Tin tức SCB",
    responses=swagger_response(
        response_model=ResponseData[NewsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_scb_news(
        request: NewsImageRequest = Depends(NewsImageRequest.get_upload_request),
):
    (
        avatar_image, thumbnail_image, current_user, title, news_category_id, content, summary, start_date,
        expired_date, active_flag
    ) = request
    data = {
        "title": title,
        "news_category_id": news_category_id,
        "content": content,
        "summary": summary,
        "start_date": start_date,
        "expired_date": expired_date,
        "active_flag": active_flag
    }
    news_data = await CtrNews(current_user).ctr_save_news(
        request_data=data,
        avatar_image=avatar_image,
        thumbnail_image=thumbnail_image,
        current_user=current_user
    )

    return ResponseData[NewsResponse](**news_data)


@router.post(
    path="/{news_id}",
    description="Cập nhật Tin tức SCB",
    name="Cập nhật Tin tức SCB",
    responses=swagger_response(
        response_model=ResponseData[NewsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_update_scb_news(
        request: NewsImageRequest = Depends(NewsImageRequest.get_upload_request),
        news_id: str = Path(..., description='News ID')
):
    (
        avatar_image, thumbnail_image, current_user, title, news_category_id, content, summary, start_date,
        expired_date, active_flag
    ) = request
    data = {
        "tilte": title,
        "news_category_id": news_category_id,
        "content": content,
        "summary": summary,
        "start_date": start_date,
        "expired_date": expired_date,
        "active_flag": active_flag
    }
    news_data = await CtrNews(current_user).ctr_update_nesws(
        news_id=news_id,
        request_data=data,
        avatar_image=avatar_image,
        thumbnail_image=thumbnail_image,
        current_user=current_user
    )

    return ResponseData[NewsResponse](**news_data)


@router.get(
    path="/{news_id}",
    name="Chi tiết tin tức",
    description='Chi tiết tin tức',
    responses=swagger_response(
        response_model=ResponseData[NewsDetailResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_scb_news(
        news_id: str = Path(..., description='News ID'),
        current_user=Depends(get_current_user_from_header())
):
    scb_news = await CtrNews(current_user).ctr_get_detail_news(news_id=news_id)
    return ResponseData[NewsDetailResponse](**scb_news)


@router.get(
    path="/",
    name="Danh sách tin tức",
    description='Danh sách tin tức',
    responses=swagger_response(
        response_model=ResponseData[ListNewsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_scb_news(
        current_user=Depends(get_current_user_from_header()),
        pagination_params: PaginationParams = Depends(),
        title: str = Query(None, description='Tiêu đề'),
        category_news: str = Query(None, description='Danh mục'),
        start_date: date = Query(None, description='Ngày bắt đầu'),
        expired_date: date = Query(None, description='Ngày kết thúc'),
        active_flag: bool = Query(None, description='Trạng thái')
):
    scb_news = await CtrNews(current_user, pagination_params=pagination_params
                             ).ctr_get_list_scb_news(title=title,
                                                     category_news=category_news,
                                                     start_date=start_date,
                                                     expired_date=expired_date,
                                                     active_flag=active_flag)
    return ResponseData[ListNewsResponse](**scb_news)
