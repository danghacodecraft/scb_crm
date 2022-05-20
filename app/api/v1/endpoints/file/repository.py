from typing import List, Optional

from app.api.base.repository import ReposReturn
from app.settings.event import service_ekyc, service_file
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


async def repos_upload_multi_file(files: List[bytes], names: List[str]) -> ReposReturn:
    responses = await service_file.upload_multi_file(files=files, names=names)

    success_responses = []
    for response in responses:
        if not response:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

        success_responses.append(response)

    return ReposReturn(data=success_responses)


async def repos_download_file(uuid: str) -> ReposReturn:
    response = await service_file.download_file(uuid=uuid)
    if not response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

    return ReposReturn(data=response)


async def repos_download_multi_file(uuids: List[str]) -> ReposReturn:
    response = await service_file.download_multi_file(uuids=uuids)
    if not response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

    return ReposReturn(data=response)


async def repos_check_is_exist_multi_file(uuids: List[str]) -> ReposReturn:
    result = await service_file.is_exist_multi_file(uuids=uuids)
    if result is None:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

    return ReposReturn(data=result)


async def repos_download_ekyc_file(uuid: str, booking_id: Optional[str]) -> ReposReturn:
    is_success, response = await service_ekyc.download_file(uuid=uuid, booking_id=booking_id)
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_FILE)

    return ReposReturn(data=response)
