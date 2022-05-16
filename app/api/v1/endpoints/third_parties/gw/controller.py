from typing import Optional

from virtualenv.run import Session

from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name
)
from app.third_parties.oracle.base import Base
from app.utils.functions import dropdown, dropdown_name


class CtrGW(BaseController):
    @staticmethod
    async def dropdown_mapping_crm_model_or_dropdown_name(
            session: Session, model: Base, name: Optional[str], code: Optional[str] = None) -> dict:
        """
        Input: code hoặc name
        Output: dropdown object
        """
        obj_mapping_crm = await get_optional_model_object_by_code_or_name(
            model=model,
            model_code=code,
            model_name=name,
            session=session
        )

        return dropdown(obj_mapping_crm) if obj_mapping_crm else dropdown_name(name=name)
