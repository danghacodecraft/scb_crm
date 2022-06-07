import datetime

from sqlalchemy.orm import Session

from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.third_parties.oracle.models.document_file.model import DocumentFile
from app.utils.constant.document_file import (
    DOCUMENT_FILE_FOLDER_CODE_DEFAULT, DOCUMENT_FILE_TYPE_CODE_FILE
)
from app.utils.functions import generate_uuid


async def plugin_create_document_file(
        file_uuid: str,
        booking_id: str,
        created_at: datetime,
        current_user: UserInfoResponse,
        session: Session,
        **kwargs
):
    document_file_id = generate_uuid()
    document_file = dict(
        id=document_file_id,
        file_uuid=file_uuid,
        root_id=document_file_id,
        booking_id=booking_id,
        document_file_type_id=DOCUMENT_FILE_TYPE_CODE_FILE
        if 'document_file_type_id' not in kwargs.keys()
        else kwargs.get('document_file_type_id'),
        document_file_folder_id=DOCUMENT_FILE_FOLDER_CODE_DEFAULT
        if 'document_file_folder_id' not in kwargs.keys()
        else kwargs.get('document_file_folder_id'),
        created_at=created_at,
        created_by_branch_name=current_user.hrm_branch_name,
        created_by_branch_code=current_user.hrm_branch_code,
        created_by_user_name=current_user.name,
        created_by_user_code=current_user.code
    )

    {document_file.update({key: value}) for key, value in kwargs.items()}  # noqa

    session.add(DocumentFile(**document_file))
    session.commit()

    return document_file_id
