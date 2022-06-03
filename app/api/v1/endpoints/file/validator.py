from typing import List

from app.api.base.validator import ValidatorReturn
from app.settings.service import SERVICE
from app.utils.error_messages import (
    ERROR_FILE_IS_NULL, ERROR_FILE_TOO_LARGE, ERROR_TOO_MANY_FILE
)

MAX_FILE_SIZE = SERVICE["file-upload"]["file_size_max"]
FILE_LIMIT = SERVICE["file-upload"]["file_limit"]


async def file_validator(file: bytes) -> ValidatorReturn:
    file_size = len(file)
    if file_size == 0:
        return ValidatorReturn(is_error=True, msg=ERROR_FILE_IS_NULL, loc='file', detail="File is Null")

    if file_size > MAX_FILE_SIZE:
        return ValidatorReturn(is_error=True, msg=ERROR_FILE_TOO_LARGE, loc='file')

    return ValidatorReturn(data=None)


async def multi_file_validator(files: List[bytes]) -> ValidatorReturn:
    if len(files) == 0:
        return ValidatorReturn(is_error=True, msg=ERROR_FILE_IS_NULL, loc='files')

    if len(files) > FILE_LIMIT:
        return ValidatorReturn(is_error=True, msg=ERROR_TOO_MANY_FILE, loc='files')

    for file in files:
        validator_return = await file_validator(file)
        if validator_return.is_error:
            return validator_return

    return ValidatorReturn(data=None)
