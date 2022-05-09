from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.cif import (
    CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP
)

CUSTOMER_RELATIONSHIP_INFO_DETAIL = {
    "customer_relationship_flag": True,
    "number_of_customer_relationship": "1",
    "relationships": [
        {
            "id": "1",
            "avatar_url": "https://example.com/example.jpg",
            "basic_information": {
                "cif_number": "1",
                "customer_relationship": {
                    "id": "1",
                    "code": "MOTHER",
                    "name": "Mẹ"
                },
                "full_name_vn": "Nguyễn Anh Đào",
                "date_of_birth": "2021-02-18",
                "gender": {
                    "id": "1",
                    "code": "NU",
                    "name": "Nữ"
                },
                "nationality": {
                    "id": "1",
                    "code": "VN",
                    "name": "Việt Nam"
                },
                "telephone_number": "",
                "mobile_number": "0867589623",
                "email": "example@example.com"
            },
            "identity_document": {
                "identity_number": "079190254791",
                "issued_date": "2021-02-18",
                "expired_date": "2021-02-18",
                "place_of_issue": {
                    "id": "1",
                    "code": "CAHCM",
                    "name": "Công an TPHCM"
                }
            },
            "address_information": {
                "resident_address": {
                    "number_and_street": "125 Võ Thị Sáu",
                    "province": {
                        "id": "1",
                        "code": "HCM",
                        "name": "Hồ Chí Minh"
                    },
                    "district": {
                        "id": "3",
                        "code": "Q3",
                        "name": "Quận 3"
                    },
                    "ward": {
                        "id": "8",
                        "code": "P8",
                        "name": "Phường 8"
                    }
                },
                "contact_address": {
                    "number_and_street": "120/6 Điện Biên Phủ",
                    "province": {
                        "id": "1",
                        "code": "HCM",
                        "name": "Hồ Chí Minh"
                    },
                    "district": {
                        "id": "BT",
                        "code": "BT",
                        "name": "Quận Bình Thạnh"
                    },
                    "ward": {
                        "id": "8",
                        "code": "AP",
                        "name": "Phường An Phước"
                    }
                }
            }
        }
    ]
}


async def repos_get_customer_relationships(
        cif_id: str,
        session: Session,
):
    customer_relationships = session.execute(
        select(
            CustomerPersonalRelationship,
            CustomerRelationshipType
        )
        .join(Customer, CustomerPersonalRelationship.customer_id == Customer.id)
        .join(CustomerRelationshipType,
              CustomerPersonalRelationship.customer_relationship_type_id == CustomerRelationshipType.id)
        .filter(
            CustomerPersonalRelationship.customer_id == cif_id,
            CustomerPersonalRelationship.type == CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP,
        )
    ).all()

    return ReposReturn(data=customer_relationships)

    # móc data từ db crm
    # customer_relationships = session.execute(
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
    #         CustomerPersonalRelationship.type == CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP,
    #     )
    # ).all()

    # # vì join với address bị lặp dữ liệu nên cần tạo dict địa chỉ dựa trên id để trả về
    # customer_relationship_id__infos = {}
    # for customer_relationship in customer_relationships:
    #     if not customer_relationship_id__infos.get(customer_relationship.id):
    #         customer_relationship_id__infos[customer_relationship.id] = {
    #             "customer_relationship": customer_relationship,
    #             "contact_address": None,
    #             "resident_address": None,
    #         }
    #     address = {
    #         "province": dropdown(customer_relationship.AddressProvince),
    #         "district": dropdown(customer_relationship.AddressDistrict),
    #         "ward": dropdown(customer_relationship.AddressWard),
    #         "number_and_street": customer_relationship.CustomerAddress.address
    #     }
    #     if customer_relationship.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
    #         customer_relationship_id__infos[customer_relationship.id]["contact_address"] = address
    #     else:
    #         customer_relationship_id__infos[customer_relationship.id]["resident_address"] = address

    # return ReposReturn(data={
    #     "customer_relationship_flag": True if customer_relationship_id__infos else False,
    #     "number_of_customer_relationship": len(customer_relationship_id__infos),
    #     "relationships": [{
    #         "id": info["customer_relationship"].id,
    #         "avatar_url": info["customer_relationship"].avatar_url,
    #         "basic_information": {
    #             "cif_number": info["customer_relationship"].cif_number,
    #             "customer_relationship": dropdown(info["customer_relationship"].CustomerRelationshipType),
    #             "full_name_vn": info["customer_relationship"].full_name_vn,
    #             "date_of_birth": info["customer_relationship"].CustomerIndividualInfo.date_of_birth,
    #             "gender": dropdown(info["customer_relationship"].CustomerGender),
    #             "nationality": dropdown(info["customer_relationship"].AddressCountry),
    #             "telephone_number": info["customer_relationship"].telephone_number,
    #             "mobile_number": info["customer_relationship"].mobile_number,
    #             "email": info["customer_relationship"].email,
    #         },
    #         "identity_document": {
    #             "identity_number": info["customer_relationship"].CustomerIdentity.identity_num,
    #             "issued_date": info["customer_relationship"].CustomerIdentity.issued_date,
    #             "place_of_issue": dropdown(info["customer_relationship"].PlaceOfIssue),
    #             "expired_date": info["customer_relationship"].CustomerIdentity.expired_date
    #         },
    #         "address_information": {
    #             "contact_address": info["contact_address"],
    #             "resident_address": info["resident_address"],
    #         }
    #     } for info in customer_relationship_id__infos.values()]
    # })

# Hiện tại lưu mối quan hệ khách hàng đang dùng chung hàm với Người giám hộ
# async def repos_save_customer_relationship(
#         cif_id: str,
#         customer_relationship_save_request: List[SaveCustomerRelationshipRequest],
#         created_by
# ):
#     if cif_id != CIF_ID_TEST:
#         return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
#
#     return ReposReturn(data={
#         "cif_id": cif_id,
#         "created_at": now(),
#         "created_by": created_by
#     })
