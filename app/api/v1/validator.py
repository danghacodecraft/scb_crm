from typing import List, Tuple

from loguru import logger

from app.api.v1.schemas.utils import HistoryData


def validate_history_data(history_datas: List[dict]) -> Tuple:
    """
    Output: is_success, history_response
    """
    idx = None
    try:
        for index, history_data in enumerate(history_datas):
            idx = index
            HistoryData(**history_data)
        return True, {}
    except Exception as ex:
        logger.error(ex)
        return False, dict(
            loc=str(idx),
            msg="History data Error",
            detail=str(ex)
        )
