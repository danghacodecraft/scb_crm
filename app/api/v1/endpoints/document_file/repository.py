from typing import Optional

from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.settings.event import service_ekyc, service_file
from app.third_parties.oracle.models.document_file.model import DocumentFile
from app.utils.error_messages import ERROR_CALL_SERVICE_FILE


async def repos_upload_file(file: bytes, name: str, ekyc_flag: bool, booking_id: Optional[str] = None) -> ReposReturn:
    response = await service_file.upload_file(
        file=file,
        name=name
    )

    if ekyc_flag:
        is_success, uuid_ekyc = await service_ekyc.upload_file(file=file, name=name, booking_id=booking_id)
        if not is_success:
            return ReposReturn(is_error=True, msg=f"{uuid_ekyc['response']['file']}")
        response.update({
            "uuid_ekyc": uuid_ekyc['uuid']
        })

    if not response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

    return ReposReturn(data=response)


@auto_commit
async def repo_add_document_file(data, session: Session) -> ReposReturn:
    session.add(DocumentFile(**data))
    return ReposReturn(data=data)
