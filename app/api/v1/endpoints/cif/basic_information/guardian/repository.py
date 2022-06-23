from typing import List

from pydantic import json
from sqlalchemy import case, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.cif import CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN
from app.utils.functions import now


async def repos_get_guardians(
        cif_id: str,
        session: Session,
):
    guardians = session.execute(
        select(
            CustomerPersonalRelationship,
            CustomerRelationshipType
        )
        .join(Customer, CustomerPersonalRelationship.customer_id == Customer.id)
        .join(CustomerRelationshipType,
              CustomerPersonalRelationship.customer_relationship_type_id == CustomerRelationshipType.id)
        .filter(
            CustomerPersonalRelationship.customer_id == cif_id,
            CustomerPersonalRelationship.type == CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN,
        )
    ).all()

    return ReposReturn(data=guardians)

    # guardians = session.execute(
    #     select(
    #         CustomerPersonalRelationship,
    #         CustomerRelationshipType,
    #         Customer.id,
    #         Customer.avatar_url,
    #         Customer.cif_number,
    #         Customer.full_name_vn,
    #         Customer.telephone_number,
    #         Customer.mobile_number,
    #         Customer.email,
    #         CustomerIndividualInfo,
    #         CustomerGender,
    #         AddressCountry,
    #         CustomerIdentity,
    #         PlaceOfIssue,
    #         CustomerAddress,
    #         AddressProvince,
    #         AddressDistrict,
    #         AddressWard,
    #     )
    #     .join(Customer, CustomerPersonalRelationship.customer_relationship_id == Customer.id)
    #     .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
    #     .join(CustomerRelationshipType,
    #           CustomerPersonalRelationship.customer_relationship_type_id == CustomerRelationshipType.id)
    #     .outerjoin(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
    #     .outerjoin(AddressCountry, Customer.nationality_id == AddressCountry.id)
    #     .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
    #     .outerjoin(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
    #     .outerjoin(CustomerAddress, Customer.id == CustomerAddress.customer_id)
    #     .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
    #     .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
    #     .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
    #     .filter(
    #         CustomerPersonalRelationship.customer_id == cif_id,
    #         CustomerPersonalRelationship.type == CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN,
    #     )
    # ).all()
    #
    # # vì join với address bị lặp dữ liệu nên cần tạo dict địa chỉ dựa trên id để trả về
    # guardian_id__infos = {}
    # for guardian in guardians:
    #     if not guardian_id__infos.get(guardian.id):
    #         guardian_id__infos[guardian.id] = {
    #             "guardian": guardian,
    #             "contact_address": None,
    #             "resident_address": None,
    #         }
    #     address = {
    #         "province": dropdown(guardian.AddressProvince),
    #         "district": dropdown(guardian.AddressDistrict),
    #         "ward": dropdown(guardian.AddressWard),
    #         "number_and_street": guardian.CustomerAddress.address
    #     }
    #     if guardian.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
    #         guardian_id__infos[guardian.id]["contact_address"] = address
    #     else:
    #         guardian_id__infos[guardian.id]["resident_address"] = address
    #
    # return ReposReturn(data={
    #     "guardian_flag": True if guardian_id__infos else False,
    #     "number_of_guardian": len(guardian_id__infos),
    #     "guardians": [{
    #         "id": info["guardian"].id,
    #         "avatar_url": info["guardian"].avatar_url,
    #         "basic_information": {
    #             "cif_number": info["guardian"].cif_number,
    #             "customer_relationship": dropdown(info["guardian"].CustomerRelationshipType),
    #             "full_name_vn": info["guardian"].full_name_vn,
    #             "date_of_birth": info["guardian"].CustomerIndividualInfo.date_of_birth,
    #             "gender": dropdown(info["guardian"].CustomerGender),
    #             "nationality": dropdown(info["guardian"].AddressCountry),
    #             "telephone_number": info["guardian"].telephone_number,
    #             "mobile_number": info["guardian"].mobile_number,
    #             "email": info["guardian"].email,
    #         },
    #         "identity_document": {
    #             "identity_number": info["guardian"].CustomerIdentity.identity_num,
    #             "issued_date": info["guardian"].CustomerIdentity.issued_date,
    #             "place_of_issue": dropdown(info["guardian"].PlaceOfIssue),
    #             "expired_date": info["guardian"].CustomerIdentity.expired_date
    #         },
    #         "address_information": {
    #             "contact_address": info["contact_address"],
    #             "resident_address": info["resident_address"],
    #         }
    #     } for info in guardian_id__infos.values()]
    # })


@auto_commit
async def repos_save_guardians(
        cif_id: str,
        list_data_insert: list,
        created_by: str,
        session: Session,
        log_data: json,
        business_form_id: str,
        relationship_type: int = CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN,
):
    """
        repos xài chung cho guardians và relationship
    """
    # clear old data
    session.execute(delete(
        CustomerPersonalRelationship
    ).filter(
        CustomerPersonalRelationship.customer_id == cif_id,
        CustomerPersonalRelationship.type == relationship_type
    ))

    session.bulk_save_objects([CustomerPersonalRelationship(**guardian) for guardian in list_data_insert])
    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=business_form_id
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_guardians_by_cif_numbers(
        cif_numbers: List[str],
        session: Session
) -> ReposReturn:
    """
    Người giám hộ là người không có người giám hộ
    """
    has_guardian = select(
        Customer,
        CustomerPersonalRelationship
    ).join(
        Customer,
        CustomerPersonalRelationship.customer_id == Customer.id
    ).filter(
        Customer.cif_number.in_(cif_numbers)
    ).exists()
    guardians = session.execute(
        select(
            Customer,
            case(
                [(has_guardian, True)],
                else_=False
            ).label("has_guardian")
        ).filter(
            Customer.cif_number.in_(cif_numbers)
        )
    ).all()

    return ReposReturn(data=guardians)
