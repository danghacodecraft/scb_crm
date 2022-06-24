from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.template.folder.repository import (
    repos_get_approval_template_folder_info, repos_get_files_from_folders
)
from app.api.v1.others.booking.controller import CtrBooking


class CtrTemplateFolder(BaseController):
    async def ctr_get_approval_template_folder_info(self, booking_id: str):
        business_type = await CtrBooking().ctr_get_business_type(booking_id=booking_id)
        # check booking
        folders = self.call_repos(await repos_get_approval_template_folder_info(
            business_type_code=business_type.code,
            session=self.oracle_session
        ))
        folder_ids = []
        approval_form_infos = []
        for folder in folders:
            approval_form_infos.append({folder.id: folder.name})
            folder_ids.append(folder.id)

        files = self.call_repos(await repos_get_files_from_folders(folder_ids=folder_ids, session=self.oracle_session))

        file_uuids = []
        for file in files:
            file_uuids.append(file.file_uuid)

        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_info_multi_file(uuids=file_uuids)

        response_datas = []
        for folder in folders:
            templates = []
            for file in files:
                templates.append(dict(
                    id=file.id,
                    name=uuid__link_downloads[file.file_uuid]['file_name'],
                    is_related_flag=True
                ))
            response_datas.append(dict(
                id=folder.id,
                name=folder.name,
                templates=templates
            ))

        return self.response(data=response_datas)
