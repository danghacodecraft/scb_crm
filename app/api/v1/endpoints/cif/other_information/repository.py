from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationUpdateRequest
)
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.other_information.model import (
    CustomerEmployee
)
from app.third_parties.oracle.models.master_data.others import StaffType
from app.utils.constant.cif import (
    BUSINESS_FORM_TTK, STAFF_TYPE_BUSINESS_CODE, STAFF_TYPE_REFER_INDIRECT_CODE
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST, ERROR_NO_DATA


async def repos_other_info(cif_id: str, session: Session) -> ReposReturn:
    customer_employee_engine = session.execute(
        select(
            Customer, StaffType, CustomerEmployee
        ).outerjoin(
            CustomerEmployee, Customer.id == CustomerEmployee.customer_id
        ).outerjoin(
            StaffType, CustomerEmployee.staff_type_id == StaffType.id
        )
        .filter(
            Customer.id == cif_id,
            Customer.active_flag == 1
        )
    )
    customer_employee = customer_employee_engine.all()

    if not customer_employee:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    sale_staff = None
    indirect_sale_staff = None

    for _, staff_type, employee in customer_employee:
        if staff_type and employee:
            if staff_type.code == STAFF_TYPE_BUSINESS_CODE:
                sale_staff = {
                    "id": employee.employee_id,
                    "fullname_vn": None
                }
            if staff_type.code == STAFF_TYPE_REFER_INDIRECT_CODE:
                indirect_sale_staff = {
                    "id": employee.employee_id,
                    "fullname_vn": None
                }
    legal_agreement_flag = customer_employee[0][0].legal_agreement_flag
    advertising_marketing_flag = customer_employee[0][0].advertising_marketing_flag
    if legal_agreement_flag is None or advertising_marketing_flag is None:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA)

    return ReposReturn(data={
        # lấy ra data ở vị trí 0 trong query sau đó lấy ra customer ở vị trí 0
        "legal_agreement_flag": legal_agreement_flag,
        "advertising_marketing_flag": advertising_marketing_flag,
        "sale_staff": sale_staff,
        "indirect_sale_staff": indirect_sale_staff,
    })


@auto_commit
async def repos_update_other_info(
        cif_id: str, update_other_info_req: OtherInformationUpdateRequest,
        current_user: UserInfoResponse,
        session: Session
) -> ReposReturn:

    session.execute(
        update(Customer).filter(Customer.id == cif_id).values(
            legal_agreement_flag=update_other_info_req.legal_agreement_flag,
            advertising_marketing_flag=update_other_info_req.advertising_marketing_flag
        )
    )

    new_customer_employees = []
    if update_other_info_req.sale_staff:
        new_customer_employees.append(
            {
                "staff_type_id": STAFF_TYPE_BUSINESS_CODE,
                "employee_id": update_other_info_req.sale_staff.id,
                "customer_id": cif_id
            }
        )

    if update_other_info_req.indirect_sale_staff:
        new_customer_employees.append(
            {
                "staff_type_id": STAFF_TYPE_REFER_INDIRECT_CODE,
                "employee_id": update_other_info_req.indirect_sale_staff.id,
                "customer_id": cif_id
            }
        )

    # xóa dữ liệu cũ
    session.execute(
        delete(
            CustomerEmployee
        ).filter(CustomerEmployee.customer_id == cif_id)
    )

    data_insert = [CustomerEmployee(**data_insert) for data_insert in new_customer_employees]
    session.bulk_save_objects(data_insert)

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=update_other_info_req.json(),
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TTK
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        'created_at': booking_response['created_at'],
        'created_by': current_user.name,
        'updated_at': booking_response['updated_at'],
        'updated_by': current_user.name
    })
