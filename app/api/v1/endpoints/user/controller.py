import re
from urllib.parse import urlparse

from fastapi.security import HTTPBasicCredentials

from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.repository import (
    repos_get_list_banner, repos_login
)
from app.settings.event import INIT_SERVICE


class CtrUser(BaseController):
    async def ctr_login(self, credentials: HTTPBasicCredentials):
        auth_res = self.call_repos(
            await repos_login(username=credentials.username.upper(), password=credentials.password))
        return self.response(data=auth_res)

    async def ctr_get_banner_info(self, is_tablet: bool):
        is_success, info_banner_list = self.call_repos(await repos_get_list_banner())
        if not is_success:
            return self.response_exception(
                msg=info_banner_list['message'],
                detail=info_banner_list['detail']
            )

        if is_tablet:
            replace_fileshare_url_parse_result = urlparse(INIT_SERVICE['fileshare']['tablet_banner_share_link'])
            replace_fileshare_url = f'{replace_fileshare_url_parse_result.scheme}://{replace_fileshare_url_parse_result.netloc}'

            for info_banner in info_banner_list:
                info_banner['banner_link_512'] = f"{replace_fileshare_url}{re.sub(r'.*/thumbnail/', '/thumbnail/', info_banner['banner_link_512'])}"
                info_banner['banner_link_1024'] = f"{replace_fileshare_url}{re.sub(r'.*/thumbnail/', '/thumbnail/', info_banner['banner_link_1024'])}"
                info_banner['banner_link_2560'] = f"{replace_fileshare_url}{re.sub(r'.*/thumbnail/', '/thumbnail/', info_banner['banner_link_2560'])}"

        return self.response(info_banner_list)
