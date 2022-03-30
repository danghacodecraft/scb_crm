from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.news.controller import CtrNews
from app.api.v1.endpoints.news.schema import (
    NewsImageRequest, NewsRequest, NewsResponse
)

router = APIRouter()
security = HTTPBasic()


# @router.get(
#     path="/",
#     name="News",
#     description="Danh sách tin tức scb",
#     responses=swagger_response(
#         response_model=PagingResponse[NewsResponse],
#         success_status_code=status.HTTP_200_OK
#     )
# )
# async def view_list_user(
#         current_user=Depends(get_current_user_from_header()),  # noqa
#         pagination_params: PaginationParams = Depends()
# ):
#     # paging_users = await CtrNews(is_init_oracle_session=False, pagination_params=pagination_params).ctr_get_list_user()
#     return None


@router.post(
    path="/",
    description="Create SCB News",
    name="Tin tức SCB",
    responses=swagger_response(
        response_model=ResponseData[NewsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_face(
        request_data: NewsRequest,
        request_img: NewsImageRequest = Depends(NewsImageRequest.get_upload_request),
        current_user=Depends(get_current_user_from_header())
):
    news_data = await CtrNews(current_user).ctr_save_news(
        request_data=request_data,
        request_img=request_img,
        current_user=current_user
    )

    return ResponseData[NewsResponse](**news_data)
