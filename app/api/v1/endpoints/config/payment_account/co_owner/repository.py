from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.payment_account.model import (
    AgreementAuthorization
)
from app.utils.constant.cif import AGREEMENT_AUTHOR_TYPE_DD


async def repos_get_agreement_authorization(session: Session):
    # TODO : Hiện tại sử dụng type DD cho danh mục thỏa thuận và ủy quyền
    account_structure_type_infos = session.execute(
        select(
            AgreementAuthorization
        )
        .filter(AgreementAuthorization.agreement_author_type == AGREEMENT_AUTHOR_TYPE_DD)
    ).scalars().all()

    return ReposReturn(data=[{
        "id": account_structure_type_info.id,
        "content": account_structure_type_info.name,
        "options": [
            {
                "id": '1',
                "title": 'Phương thức 1',
                "content": "Chữ ký của tất cả các đồng sở hữu"
            },
            {
                "id": '2',
                "title": 'Phương thức 2',
                "content": "Chữ ký của 1 trong bất kỳ các đồng chủ tài khoản"
            },
            {
                "id": '3',
                "title": "Phương thức 3",
                "content": 'Chữ ký của các đồng chủ tài khoản sau'
            },
        ]
    } for account_structure_type_info in account_structure_type_infos])
