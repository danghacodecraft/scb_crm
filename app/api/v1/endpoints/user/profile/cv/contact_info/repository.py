from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_contact_info(
        session: Session
) -> ReposReturn:
    data_response = {
        "contact_info": {
            "domicile": {
                "domicile": "210/58/56 Cách mạng tháng tám",
                "nationality": {
                    "id": "id",
                    "code": "Code",
                    "name": "Việt Nam"
                },
                "province": {
                    "id": "id",
                    "code": "Code",
                    "name": "Tp.HCM"
                },
                "district": {
                    "id": "id",
                    "code": "Code",
                    "name": "Quận Tân Bình"
                },
                "ward": {
                    "id": "id",
                    "code": "Code",
                    "name": "Phường 16"
                }
            },
            "resident": {
                "resident_address": "210/56/56 Cách mạng tháng 8",
                "nationality": {
                    "id": "id",
                    "code": "Code",
                    "name": "Việt Nam"
                },
                "province": {
                    "id": "id",
                    "code": "Code",
                    "name": "Tp.HCM"
                },
                "district": {
                    "id": "id",
                    "code": "Code",
                    "name": "Quận Tân Bình"
                },
                "ward": {
                    "id": "id",
                    "code": "Code",
                    "name": "Phường 16"
                }
            },
            "temporary_residence": {
                "temporary_residence_address": "210/56/56 Cách mạng tháng 8",
                "nationality": {
                    "id": "id",
                    "code": "Code",
                    "name": "Việt Nam"
                },
                "province": {
                    "id": "id",
                    "code": "Code",
                    "name": "Tp.HCM"
                },
                "district": {
                    "id": "id",
                    "code": "Code",
                    "name": "Quận Tân Bình"
                },
                "ward": {
                    "id": "id",
                    "code": "Code",
                    "name": "Phường 16"
                }
            },
            "contact": {
                "resident_address": "210/56/56 Cách mạng tháng 8",
                "nationality": {
                    "id": "id",
                    "code": "Code",
                    "name": "Việt Nam"
                },
                "province": {
                    "id": "id",
                    "code": "Code",
                    "name": "Tp.HCM"
                },
                "district": {
                    "id": "id",
                    "code": "Code",
                    "name": "Quận Tân Bình"
                },
                "ward": {
                    "id": "id",
                    "code": "Code",
                    "name": "Phường 16"
                }
            }
        },
        "other_info": {
            "contact": {
                "contact": "Trần Văn Sơn Vũ",
                "relationship": {
                    "id": "1",
                    "code": "Code",
                    "name": "Chồng"
                },
                "mobile_num": "0909125649"
            },
            "guardian": {
                "guardian": "Nguyễn Xuân An",
                "relationship": {
                    "id": "1",
                    "code": "Code",
                    "name": "Bạn bè"
                },
                "mobile_num": "0909125649"
            },
            "expiration_date": "2021-10-01"
        }
    }

    return ReposReturn(data=data_response)
