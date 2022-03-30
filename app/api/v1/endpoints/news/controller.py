from app.api.base.controller import BaseController
from app.api.v1.endpoints.news.schema import NewsRequest
# from app.api.v1.endpoints.news.repository import repos_add_scb_news
from app.settings.event import service_file
from app.utils.functions import generate_uuid, now


class CtrNews(BaseController):
    async def ctr_save_news(self, request_data: NewsRequest, avatar_image, thumbnail_image, current_user):

        uuid = generate_uuid()
        data_scb_news = {
            "id": uuid,
            "title": request_data.tilte,
            "category_id": request_data.news_category_id,
            "user_id": current_user.code,
            "user_name": current_user.name,
            "content": request_data.content,
            "summary": request_data.summary,
            "start_date": request_data.start_date,
            "expired_date": request_data.expired_date,
            "created_at": now(),
        }

        avatar_upload = await avatar_image.read()
        avatar = await service_file.upload_file(file=avatar_upload, name=uuid)
        thumbnail_upload = await thumbnail_image.read()
        thumbnail = await service_file.upload_file(file=thumbnail_upload, name=uuid)
        print(avatar)
        data_scb_news.update({
            "avatar_url": avatar.file_url,
            "thumbnail_url": thumbnail.file_url
        })

        # add_scb_news = self.call_repos(
        #     await repos_add_scb_news(
        #         data_scb_news,
        #         session=self.oracle_session,
        #     )
        # )
        return self.response(data={"aq": "231231"})
