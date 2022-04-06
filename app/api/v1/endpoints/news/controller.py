from datetime import datetime

from app.api.base.controller import BaseController
from app.api.v1.endpoints.news.repository import (
    get_data_by_id, get_list_scb_news, repos_add_scb_news,
    repos_update_scb_news
)
from app.settings.event import service_file
from app.third_parties.oracle.models.master_data.news import NewsCategory
from app.utils.error_messages import VALIDATE_ERROR
from app.utils.functions import dropdown, generate_uuid, now


class CtrNews(BaseController):
    async def ctr_save_news(self, request_data, avatar_uuid, thumbnail_uuid, current_user):

        """ Validate """
        # check category_id
        await self.get_model_object_by_id(
            model=NewsCategory,
            model_id=request_data["news_category_id"],
            loc="news_category_id",
        )

        thumbnail_image = await service_file.download_file(thumbnail_uuid)
        if not thumbnail_image:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="thumbnail_uuid invalid value",
                loc="thumbnail_uuid"
            )

        uuid = generate_uuid()
        data_scb_news = {
            "id": uuid,
            "title": request_data["title"],
            "category_id": request_data["news_category_id"],
            "user_id": current_user.code,
            "user_name": current_user.name,
            "content": request_data["content"],
            "summary": request_data["summary"],
            "start_date": request_data["start_date"],
            "thumbnail_uuid": thumbnail_uuid,
            "created_at": now(),
            "active_flag": request_data["active_flag"]
        }

        if request_data["expired_date"] is not None:
            if request_data["expired_date"] < request_data["start_date"]:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="expired_date cannot be greater than start_date",
                    loc="expired_date"
                )
            data_scb_news.update({
                "expired_date": request_data["expired_date"]
            })

        if avatar_uuid is not None:
            avatar = await service_file.download_file(avatar_uuid)
            if not avatar:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="avatar_uuid invalid value",
                    loc="avatar_uuid"
                )
            data_scb_news.update({
                "avatar_uuid": avatar_uuid
            })

        self.call_repos(
            await repos_add_scb_news(
                data_scb_news,
                session=self.oracle_session,
            )
        )
        return self.response(data={"news_id": uuid})

    async def ctr_update_nesws(self, news_id, request_data, avatar_uuid, thumbnail_uuid, current_user):

        """ Validate """
        news_obj = self.call_repos(await get_data_by_id(self.oracle_session, news_id))

        await self.get_model_object_by_id(
            model=NewsCategory,
            model_id=request_data["news_category_id"],
            loc="news_category_id",
        )
        thumbnail_image = await service_file.download_file(thumbnail_uuid)
        if not thumbnail_image:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="thumbnail_uuid invalid value",
                loc="thumbnail_uuid"
            )
        data_update = {
            "id": news_id,
            "title": request_data["tilte"],
            "category_id": request_data["news_category_id"],
            "user_id": current_user.code,
            "user_name": current_user.name,
            "content": request_data["content"],
            "summary": request_data["summary"],
            "thumbnail_uuid": thumbnail_uuid,
            "start_date": request_data["start_date"],
            "active_flag": request_data["active_flag"],
            "created_at": news_obj.News.created_at,
            "updated_at": now()
        }
        if request_data["expired_date"] is not None:
            if request_data["expired_date"] < request_data["start_date"]:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="expired_date cannot be greater than start_date",
                    loc="expired_date"
                )
            data_update.update({
                "expired_date": request_data["expired_date"]
            })

        # Upload avatar và banner
        if avatar_uuid is not None:
            avatar = await service_file.download_file(avatar_uuid)
            if not avatar:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="avatar_uuid invalid value",
                    loc="avatar_uuid"
                )
            data_update.update({
                "avatar_uuid": avatar_uuid
            })

        self.call_repos(
            await repos_update_scb_news(
                news_id=news_id,
                data_scb_news=data_update,
                session=self.oracle_session,
            )
        )
        return self.response(data={"news_id": news_id})

    async def ctr_get_detail_news(self, news_id):

        news_data = self.call_repos(await get_data_by_id(self.oracle_session, news_id))
        data = {
            "id": news_data.News.id,
            "title": news_data.News.title,
            "avatar_uuid": news_data.News.avatar_uuid,
            "thumbnail_uuid": news_data.News.thumbnail_uuid,
            "news_category_id": dropdown(news_data.NewsCategory),
            "user_name": news_data.News.user_name,
            "content": news_data.News.content,
            "summary": news_data.News.summary,
            "start_date": news_data.News.start_date,
            "expired_date": news_data.News.expired_date,
            "created_at": news_data.News.created_at,
            "active_flag": news_data.News.active_flag
        }

        return self.response(data)

    async def ctr_get_list_scb_news(self, title, category_news, start_date, expired_date, active_flag):

        limit = self.pagination_params.limit
        page = 1
        if self.pagination_params.page:
            page = self.pagination_params.page
        start_date = datetime(start_date.year, start_date.month, start_date.day) if start_date else None
        expired_date = datetime(expired_date.year, expired_date.month, expired_date.day) if expired_date else None
        list_news = self.call_repos(await get_list_scb_news(session=self.oracle_session,
                                                            title=title,
                                                            category_news=category_news,
                                                            start_date=start_date,
                                                            expired_date=expired_date,
                                                            active_flag=active_flag,
                                                            limit=limit,
                                                            page=page))
        res_data = []

        if len(list_news["query_data"]) == 0:
            return self.response_paging(data={
                "num_news": 0,
                "list_news": []}
            )
        for news_data in list_news["query_data"]:
            data = {
                "id": news_data.News.id,
                "title": news_data.News.title,
                "avatar_uuid": news_data.News.avatar_uuid,
                "thumbnail_uuid": news_data.News.thumbnail_uuid,
                "news_category_id": dropdown(news_data.NewsCategory),
                "user_name": news_data.News.user_name,
                "content": news_data.News.content,
                "summary": news_data.News.summary,
                "start_date": news_data.News.start_date,
                "expired_date": news_data.News.expired_date,
                "created_at": news_data.News.created_at,
                "active_flag": news_data.News.active_flag
            }
            res_data.append(data)

        return self.response_paging(data={
            "num_news": len(list_news["total_row"]),
            "list_news": res_data}
        )
