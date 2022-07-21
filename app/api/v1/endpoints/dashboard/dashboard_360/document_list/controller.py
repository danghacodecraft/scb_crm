from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.dashboard_360.document_list.repository import (
    repos_count_document_item, repos_get_document_list
)
from app.api.v1.endpoints.file.repository import repos_download_multi_file
from app.utils.functions import dropdown


class CtrDocumentList(BaseController):
    async def ctr_document_list(self, cif_number: str):
        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        document_list = self.call_repos(await repos_get_document_list(
            cif_number=cif_number,
            limit=limit,
            page=current_page,
            session=self.oracle_session
        ))

        total_item = self.call_repos(await repos_count_document_item(
            cif_number=cif_number,
            session=self.oracle_session))

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        document_datas = {}
        document_file_uuids = []
        for document in document_list:
            document_file_uuids.append(document.file_uuid)

            document_datas.update({
                document.file_uuid: {
                    "created_by": document.created_by_user_name,
                    "file_uuid": document.file_uuid,
                    "create_at": document.created_at,
                    "file_type": dropdown(document.document_file_type)
                }
            })
        file_datas = self.call_repos(await repos_download_multi_file(uuids=document_file_uuids))
        for file_data in file_datas:
            document_datas[file_data['uuid']].update(file_name=file_data['file_name'])
            # document_datas[file_data['uuid']].update(file_size=file_data['file_size'])      #todo

        response_datas = []
        for _, document_data in document_datas.items():
            response_datas.append(document_data)

        return self.response_paging(
            data=response_datas,
            current_page=current_page,
            total_items=total_item,
            total_page=total_page
        )
