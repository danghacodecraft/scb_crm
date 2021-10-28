from typing import List

from app.api.base.repository import ReposReturn
from app.settings.event import service_file
from app.utils.error_messages import ERROR_CALL_SERVICE


async def repos_upload_file(file: bytes, name: str) -> ReposReturn:
    response = await service_file.upload_file(file=file, name=name)
    if not response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

    return ReposReturn(data=response)


async def repos_upload_multi_file(files: List[bytes], names: List[str]) -> ReposReturn:
    responses = await service_file.upload_multi_file(files=files, names=names)

    success_responses = []
    for response in responses:
        if not response:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

        success_responses.append(response)

    return ReposReturn(data=success_responses)


async def repos_download_file(uuid: str) -> ReposReturn:
    response = await service_file.download_file(uuid=uuid)
    if not response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

    return ReposReturn(data=response)


async def repos_download_multi_file(uuids: List[str]) -> ReposReturn:
    response = await service_file.download_multi_file(uuids=uuids)
    if not response:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

    return ReposReturn(data=response)