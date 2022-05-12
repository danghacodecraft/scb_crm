from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name
)
from app.utils.functions import dropdown, dropdown_name


class CtrGW(BaseController):
    async def dropdown_mapping_crm_model_or_dropdown_name(
            self, model, name: str, code: Optional[str] = None):
        """
        Input: code hoặc name
        Output: dropdown object
        """
        obj_mapping_crm = await get_optional_model_object_by_code_or_name(
            model=model,
            model_code=code,
            model_name=name,
            session=self.oracle_session
        )

        return dropdown(obj_mapping_crm) if obj_mapping_crm else dropdown_name(name=name)
