from app.api.base.controller import BaseController
from app.api.v1.endpoints.news.repository import (
    get_comment_by_id, get_comment_like_by_user, get_data_by_id,
    get_like_by_user, get_list_comment, get_list_scb_news, get_parent_comment,
    repo_add_comment, repo_add_comment_like, repo_remove_comment_like,
    repos_add_scb_news, repos_update_scb_news
)
from app.api.v1.endpoints.news.schema import NewsCommentRequest
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_employee_info_from_code
)
from app.settings.event import service_file
from app.third_parties.oracle.models.master_data.news import NewsCategory
from app.utils.constant.cif import NEWS_COMMENT_FILTER_PARAMS
from app.utils.constant.gw import GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT
from app.utils.error_messages import VALIDATE_ERROR
from app.utils.functions import (
    date_to_datetime, dropdown, end_time_of_day, generate_uuid, now
)


class CtrNews(BaseController):
    async def ctr_save_news(self, request_data, avatar_uuid, current_user):

        """ Validate """
        # check category_id
        await self.get_model_object_by_id(
            model=NewsCategory,
            model_id=request_data["news_category_id"],
            loc="news_category_id",
        )

        uuid = generate_uuid()
        data_scb_news = {
            "id": uuid,
            "title": request_data["title"],
            "category_id": request_data["news_category_id"],
            "user_id": current_user.user_info.code,
            "user_name": current_user.user_info.name,
            "content": request_data["content"],
            "summary": request_data["summary"],
            "start_date": request_data["start_date"],
            "expired_date": request_data["expired_date"],
            "created_at": now(),
            "total_comment": 0,
            "active_flag": request_data["active_flag"]
        }

        if request_data["expired_date"] is not None and request_data["start_date"] is not None:
            if request_data["expired_date"] < request_data["start_date"]:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="expired_date cannot be greater than start_date",
                    loc="expired_date"
                )

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

    async def ctr_update_nesws(self, news_id, request_data, avatar_uuid, current_user):

        """ Validate """
        news_obj = self.call_repos(await get_data_by_id(self.oracle_session, news_id))

        await self.get_model_object_by_id(
            model=NewsCategory,
            model_id=request_data["news_category_id"],
            loc="news_category_id",
        )

        data_update = {
            "id": news_id,
            "title": request_data["tilte"],
            "category_id": request_data["news_category_id"],
            "user_id": current_user.user_info.code,
            "user_name": current_user.user_info.name,
            "content": request_data["content"],
            "summary": request_data["summary"],
            "start_date": request_data["start_date"],
            "expired_date": request_data["expired_date"],
            "active_flag": request_data["active_flag"],
            "created_at": news_obj.News.created_at,
            "total_comment": news_obj.News.total_comment,
            "updated_at": now()
        }
        if request_data["expired_date"] is not None and request_data["start_date"] is not None:
            if request_data["expired_date"] < request_data["start_date"]:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="expired_date cannot be greater than start_date",
                    loc="expired_date"
                )

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
            "total_comment": news_data.News.total_comment,
            "avatar_uuid": news_data.News.avatar_uuid,
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

        start_date = date_to_datetime(start_date) if start_date else None
        expired_date = end_time_of_day(date_to_datetime(expired_date)) if expired_date else None

        list_news = self.call_repos(await get_list_scb_news(session=self.oracle_session,
                                                            title=title,
                                                            category_news=category_news,
                                                            start_date=start_date,
                                                            expired_date=expired_date,
                                                            active_flag=active_flag,
                                                            limit=limit,
                                                            page=page))
        res_data = []
        url_avatars = []
        url_avatar_dict = {}

        if len(list_news["query_data"]) == 0:
            return self.response_paging(data={
                "num_news": 0,
                "list_news": []}
            )
        for news_data in list_news["query_data"]:
            data = {
                "id": news_data.News.id,
                "title": news_data.News.title,
                "total_comment": news_data.News.total_comment,
                "avatar_uuid": news_data.News.avatar_uuid,
                "news_category_id": dropdown(news_data.NewsCategory),
                "user_name": news_data.News.user_name,
                "content": news_data.News.content,
                "summary": news_data.News.summary,
                "start_date": news_data.News.start_date,
                "expired_date": news_data.News.expired_date,
                "created_at": news_data.News.created_at,
                "active_flag": news_data.News.active_flag
            }
            if news_data.News.avatar_uuid:
                url_avatars.append(news_data.News.avatar_uuid)
            res_data.append(data)

        if len(url_avatars):
            url_avatars = await service_file.download_multi_file(url_avatars)

            for avatar_item in url_avatars:
                url_avatar_dict.update({
                    avatar_item["uuid"]: avatar_item["file_url"]
                })
            for i in res_data:
                if i["avatar_uuid"] is not None:
                    i.update({
                        "avatar_uuid": url_avatar_dict[f'{i["avatar_uuid"]}']
                    })

        return self.response_paging(data={
            "num_news": len(list_news["total_row"]),
            "list_news": res_data}
        )

    async def ctr_news_comment(self, data_comment: NewsCommentRequest, news_id):

        # Validate: check tồn tại news_id
        self.call_repos(await get_data_by_id(self.oracle_session, news_id))

        uuid = generate_uuid()
        data_insert = {
            "id": uuid,
            "news_id": news_id,
            "content": data_comment.content,
            "create_user_id": self.current_user.user_info.code,
            "create_user_name": self.current_user.user_info.name,
            "create_user_username": self.current_user.user_info.username,
            "total_likes": 0,
            "created_at": now()
        }
        if data_comment.parent_id:
            self.call_repos(await get_parent_comment(session=self.oracle_session, news_id=news_id,
                                                     comment_id=data_comment.parent_id))
            data_insert.update({
                "parent_id": data_comment.parent_id
            })
        self.call_repos(
            await repo_add_comment(
                data_comment=data_insert,
                news_id=news_id,
                session=self.oracle_session,
            )
        )
        return self.response(data={
            "comment_id": uuid
        })

    async def ctr_get_comment_by_news_id(self, news_id, filter_by, page):

        if filter_by not in NEWS_COMMENT_FILTER_PARAMS:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                loc='filter_by',
                detail=f'{filter_by} {VALIDATE_ERROR}'
            )

        comments = self.call_repos(await get_list_comment(self.oracle_session, news_id, filter_by, page=page))

        total_comment_parent = len(comments["total_comment_parent"])
        total_comment = total_comment_parent + len(comments["list_child_comment"])

        list_comment = comments["list_comment"]
        list_comment_child = comments["list_child_comment"]

        list_comment_id = []
        list_data_res = []

        """ 1. Lấy thông tin user_code người dùng đã bình luận (user_codes)
            2. Lấy id comment(list_comment_id)
        """
        if len(list_comment):
            user_codes = []
            for cmt_parent_item in list_comment:
                user_codes.append(cmt_parent_item.create_user_id)
                list_comment_id.append(cmt_parent_item.id)
            for cmt_child_item in list_comment_child:
                user_codes.append(cmt_child_item.create_user_id)
                list_comment_id.append(cmt_child_item.id)

            if len(user_codes) == 1:
                user_codes = user_codes[0]
            else:
                user_codes = tuple(user_codes)

            comments_like_by_user = self.call_repos(await get_comment_like_by_user(session=self.oracle_session,
                                                                                   comment_ids=list_comment_id,
                                                                                   user_id=self.current_user.user_info.code))

            users_info_cmt = {}
            for user_code in user_codes:
                gw_employee_info = self.call_repos(await repos_gw_get_employee_info_from_code(
                    employee_code=user_code, current_user=self.current_user))
                user_info = gw_employee_info[GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT]['data_output']['employee_info']
                users_info_cmt.update({
                    user_code: {
                        "title_name": user_info['title_name'],
                        "avatar_link": user_info['avatar'].replace(
                            "https://192.168.73.151/cdn-profile", "/cdn-profile/thumb")
                    }
                })

            for cmt_item in list_comment:
                cmt_data = {
                    "news_id": cmt_item.news_id,
                    "comment_id": cmt_item.id,
                    "create_name": cmt_item.create_user_name,
                    "user_name": cmt_item.create_user_username,
                    "user_title_name": users_info_cmt[cmt_item.create_user_id]["title_name"],
                    "avatar_link": users_info_cmt[cmt_item.create_user_id]["avatar_link"],
                    "content": cmt_item.content,
                    "total_likes": cmt_item.total_likes,
                    "parent_id": cmt_item.parent_id,
                    "created_at": cmt_item.created_at,
                    "is_like": False
                }
                if cmt_item.id in comments_like_by_user:
                    cmt_data.update({
                        "is_like": True
                    })
                list_data_res.append(cmt_data)

            for parrent_cmt in list_data_res:
                comment_child = []
                for child_cmt in list_comment_child:
                    if child_cmt.parent_id == parrent_cmt["comment_id"]:
                        cmt_child_data = {
                            "news_id": child_cmt.news_id,
                            "comment_id": child_cmt.id,
                            "create_name": child_cmt.create_user_name,
                            "user_name": child_cmt.create_user_username,
                            "user_title_name": users_info_cmt[child_cmt.create_user_id]["title_name"],
                            "avatar_link": users_info_cmt[child_cmt.create_user_id]["avatar_link"],
                            "content": child_cmt.content,
                            "total_likes": child_cmt.total_likes,
                            "parent_id": child_cmt.parent_id,
                            "created_at": child_cmt.created_at,
                            "is_like": False
                        }
                        if child_cmt.id in comments_like_by_user:
                            cmt_child_data.update({
                                "is_like": True
                            })
                        comment_child.append(cmt_child_data)
                parrent_cmt.update({
                    "comment_child": comment_child
                })

        return self.response(data={
            "total_comment_parent": total_comment_parent,
            "total_comment": total_comment,
            "comments": list_data_res
        })

    async def ctr_comment_like(self, comment_id):
        user_id = self.current_user.user_info.code
        self.call_repos(await get_comment_by_id(session=self.oracle_session, comment_id=comment_id))
        like_db_obj = self.call_repos(
            await get_like_by_user(session=self.oracle_session, user_id=user_id, comment_id=comment_id))
        uuid = generate_uuid()

        if like_db_obj:
            # nếu đã like -> unlike
            uuid = like_db_obj.CommentLike.id
            total_like = self.call_repos(
                await repo_remove_comment_like(comment_id=comment_id, session=self.oracle_session, like_id=uuid))
        else:
            like_data_insert = {
                "id": uuid,
                "comment_id": comment_id,
                "create_user_id": user_id,
                "create_user_name": self.current_user.user_info.name,
                "create_user_username": self.current_user.user_info.username,
                "created_at": now()
            }

            total_like = self.call_repos(
                await repo_add_comment_like(comment_id=comment_id, like_data=like_data_insert,
                                            session=self.oracle_session))
        return self.response(data={
            "like_id": uuid,
            "total_like": total_like
        })
