from pydantic import Field

from app.api.base.schema import BaseSchema

# GW checkUsernameIBMBExist


class CheckUsernameIBMBExistTransactionInfoItemRequest(BaseSchema):
    transaction_name: str = Field(..., description="Kênh eBank: `Internet Banking`, `Mobile Banking`, `SMS Banking`",
                                  example='Internet Banking')
    transaction_value: str = Field(..., description="Username đăng nhập IBMB", example='0945228866')


class CheckUsernameIBMBExistRequest(BaseSchema):
    transaction_info: CheckUsernameIBMBExistTransactionInfoItemRequest


class CheckUsernameIBMBExistEbankIBMBInfoItemResponse(BaseSchema):
    ebank_ibmb_status: str = Field(..., description="""Trạng thái khi kiểm tra username, nếu username có tồn tại:`UNAVAILABLE`, không tồn tại, có thể sử dụng dc: `AVAILABLE`
    """)


class CheckUsernameIBMBExistResponse(BaseSchema):
    ebank_ibmb_info: CheckUsernameIBMBExistEbankIBMBInfoItemResponse
