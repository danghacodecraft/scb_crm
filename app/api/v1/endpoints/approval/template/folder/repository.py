from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.document_file.model import (
    DocumentFile, DocumentFileFolder
)


async def repos_get_approval_template_folder_info(
        business_type_code: str,
        session: Session
):
    template_folders = session.execute(
        select(DocumentFileFolder)
        .filter(DocumentFileFolder.id == business_type_code)
    ).scalars().all()
    # template_folders = [
    #     {
    #         "id": 1,
    #         "name": "01 BM MO CIF V1",
    #         "templates": [
    #             {
    #                 "id": 1,
    #                 "name": "BM_01_Giay_dang_ky_thong_tin_kiem_Hop_dong_mo_TK_va_su_dung_DV_TV",
    #                 "is_related_flag": True
    #             },
    #             {
    #                 "id": 2,
    #                 "name": "BM_01_Giay_dang_ky_thong_tin_kiem_Hop_dong_mo_TK_va_su_dung_DV_SN",
    #                 "is_related_flag": True
    #             },
    #             {
    #                 "id": 3,
    #                 "name": " BM 01- GIAY DE NGHI MO TAI KHOAN DTGT",
    #                 "is_related_flag": True
    #             },
    #             {
    #                 "id": 4,
    #                 "name": "BM 02- GIAY DE NGHI MO TAI KHOAN DTTT vao VN bang VND",
    #                 "is_related_flag": True
    #             },
    #             {
    #                 "id": 5,
    #                 "name": "BM 03- GIAY DE NGHI MO TAI KHOAN DTTT vao VN bang ngoai te",
    #                 "is_related_flag": True
    #             },
    #             {
    #                 "id": 6,
    #                 "name": "BM 04- GIAY DE NGHI MO TAI KHOAN DTTT ra NN",
    #                 "is_related_flag": True
    #             },
    #         ]
    #     }
    # ]
    return ReposReturn(data=template_folders)


async def repos_get_files_from_folders(
        folder_ids: List,
        session: Session
):
    files = session.execute(
        select(
            DocumentFile
        )
        .filter(DocumentFile.document_file_folder_id.in_(tuple(folder_ids)))
        .order_by(DocumentFile.created_at)
    ).scalars().all()
    return ReposReturn(data=files)
