from app.api.base.controller import BaseController
from app.api.v1.endpoints.news.repository import (
    get_data_by_id, get_list_scb_news, repos_add_scb_news,
    repos_update_scb_news
)
from app.settings.event import service_file
from app.third_parties.oracle.models.master_data.news import NewsCategory
from app.third_parties.oracle.models.news.model import News
from app.utils.error_messages import VALIDATE_ERROR
from app.utils.functions import dropdown, generate_uuid, now


class CtrNews(BaseController):
    async def ctr_save_news(self, request_data, avatar_image, thumbnail_image, current_user):

        """ Validate """
        # check category_id
        await self.get_model_object_by_id(
            model=NewsCategory,
            model_id=request_data["news_category_id"],
            loc="news_category_id",
        )
        if request_data["active_flag"] > 1 or request_data["active_flag"] < 0:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="active_flag invalid data",
                loc="active_flag"
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
            "created_at": now(),
            "active_flag": request_data["active_flag"]
        }

        if request_data["expired_date"] is not None:
            data_scb_news.update({
                "expired_date": request_data["expired_date"]
            })
        # Upload avatar và banner
        if avatar_image is not None:
            avatar_upload = await avatar_image.read()
            avatar = await service_file.upload_file(file=avatar_upload, name=uuid)
            data_scb_news.update({
                "avatar_url": avatar["uuid"]
            })
        thumbnail_upload = await thumbnail_image.read()
        thumbnail = await service_file.upload_file(file=thumbnail_upload, name=uuid)
        data_scb_news.update({
            "thumbnail_url": thumbnail["uuid"]
        })

        self.call_repos(
            await repos_add_scb_news(
                data_scb_news,
                session=self.oracle_session,
            )
        )
        return self.response(data={"news_id": uuid})

    async def ctr_update_nesws(self, news_id, request_data, avatar_image, thumbnail_image, current_user):

        """ Validate """
        news_obj = await self.get_model_object_by_id(
            model=News,
            model_id=news_id,
            loc="news_id",
        )

        await self.get_model_object_by_id(
            model=NewsCategory,
            model_id=request_data["news_category_id"],
            loc="news_category_id",
        )
        if request_data["active_flag"] > 1 or request_data["active_flag"] < 0:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="active_flag invalid data",
                loc="active_flag"
            )
        data_update = {
            "id": news_id,
            "title": request_data["tilte"],
            "category_id": request_data["news_category_id"],
            "user_id": current_user.code,
            "user_name": current_user.name,
            "content": request_data["content"],
            "summary": request_data["summary"],
            "start_date": request_data["start_date"],
            "active_flag": request_data["active_flag"],
            "created_at": news_obj.created_at,
            "updated_at": now()
        }
        if request_data["expired_date"] is not None:
            data_update.update({
                "expired_date": request_data["expired_date"]
            })

        # Upload avatar và banner
        if avatar_image is not None:
            avatar_upload = await avatar_image.read()
            avatar = await service_file.upload_file(file=avatar_upload, name=news_id)
            data_update.update({
                "avatar_url": avatar["uuid"]
            })
        thumbnail_upload = await thumbnail_image.read()
        thumbnail = await service_file.upload_file(file=thumbnail_upload, name=news_id)
        data_update.update({
            "thumbnail_url": thumbnail["uuid"]
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
        await self.get_model_object_by_id(
            model=News,
            model_id=news_id,
            loc="news_id",
        )
        news_data = self.call_repos(await get_data_by_id(self.oracle_session, news_id))
        data = {
            "id": news_data.News.id,
            "title": news_data.News.title,
            "news_category_id": dropdown(news_data.NewsCategory),
            "user_name": news_data.News.user_name,
            "content": news_data.News.content,
            "summary": news_data.News.summary,
            "start_date": news_data.News.start_date,
            "expired_date": news_data.News.expired_date,
            "created_at": news_data.News.created_at,
            "active_flag": news_data.News.active_flag
        }

        if news_data.News.avatar_url:
            avatar = await service_file.download_file(news_data.News.avatar_url)
            data.update({
                "avatar_url": avatar["file_url"]
            })
        thumbnail = await service_file.download_file(news_data.News.thumbnail_url)
        data.update({
            "thumbnail_url": thumbnail["file_url"]
        })

        return self.response(data)

    async def ctr_get_list_scb_news(self):
        list_news = self.call_repos(await get_list_scb_news(session=self.oracle_session))
        res_data = []
        for news_data in list_news:
            data = {
                "id": news_data.News.id,
                "title": news_data.News.title,
                "news_category_id": dropdown(news_data.NewsCategory),
                "user_name": news_data.News.user_name,
                "content": news_data.News.content,
                "summary": news_data.News.summary,
                "start_date": news_data.News.start_date,
                "expired_date": news_data.News.expired_date,
                "created_at": news_data.News.created_at,
                "active_flag": news_data.News.active_flag
            }

            if news_data.News.avatar_url:
                avatar = await service_file.download_file(news_data.News.avatar_url)
                data.update({
                    "avatar_url": avatar["file_url"]
                })
            thumbnail = await service_file.download_file(news_data.News.thumbnail_url)
            data.update({
                "thumbnail_url": thumbnail["file_url"]
            })
            res_data.append(data)

        return self.response_paging(data={
            "num_news": len(res_data),
            "list_news": res_data},
            total_item=len(res_data)
        )
