from typing import Dict, Union

from app.api.base.repository import ReposReturn
from app.utils.status.message import ERROR_CIF_ID_NOT_EXIST


async def repos_get_cif_info(cif_id: str) -> (bool, Union[str, Dict]):
    if cif_id == '123':
        return ReposReturn(data={
            "self_selected_cif_flag": True,
            "cif_number": "123456789",
            "customer_classification": {
                "id": "fd01b796-5ad1-4161-8e2c-2abe41390deb",
                "code": "CN",
                "name": "Cá nhân"
            },
            "customer_economic_profession": {
                "id": "b860d25e-0db2-496b-8bb7-76d6838d191a",
                "code": "KT1",
                "name": "Mã ngành KT"
            },
            "kyc_level": {
                "id": "24152d4a-13c8-4720-a92d-2f2e784af6af",
                "code": "LV1",
                "name": "Level 1"
            }
        }
        )
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')
