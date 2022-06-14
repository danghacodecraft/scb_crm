from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest


############################################################
# Request
############################################################
class SignatureAgreementAuthorRequest(BaseSchema):
    cif_number: str = CustomField(
        description="Mã định danh của đồng sở hữu"
    ).CIFNumberField
    full_name_vn: str = Field(..., description="Tên tiếng việt của đồng sở hữu")


class AgreementAuthorRequest(BaseSchema):
    agreement_author_id: str = Field(..., description="Mã danh mục thỏa thuận và uỷ quyền")
    agreement_flag: bool = Field(
        ...,
        description="Thỏa thuận chữ ký các hồ sơ chứng từ.`True`: Có , `False`: Không",
    )
    method_sign: int = Field(..., description="Phương thức ký")
    signature_list: Optional[List[SignatureAgreementAuthorRequest]] = Field(
        ..., description="Chữ ký của đồng sở hữu"
    )


class AccountRequest(BaseSchema):
    cif_number: str = CustomField(description="Số CIF của đồng sở hữu").CIFNumberField
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ của khách hàng với đồng sở hữu")


class AccountHolderRequest(BaseSchema):
    joint_account_holder_flag: bool = Field(
        ..., description="Có đồng chủ sở hữu. `True`: Có , `False`: Không"
    )
    document_no: str = Field(..., description="Số văn bản")
    create_at: date = Field(..., description="Ngày lập")
    address_flag: bool = Field(..., description="Nơi lập")
    document_address: Optional[str] = Field(None, description="Thông tin địa chỉ file")
    file_uuid: str = Field(..., description="Tập tin đính kèm")
    joint_account_holders: List[AccountRequest] = Field(
        ..., description="Danh sách các đồng sở hữu"
    )
    agreement_authorization: List[AgreementAuthorRequest] = Field(
        ..., description="Danh mục thỏa thuận và ủy quyền"
    )
