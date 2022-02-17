import json
from typing import List

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name,
    repos_get_model_object_by_id_or_code,
    write_transaction_log_and_update_booking
)
from app.settings.event import service_soa
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    AgreementAuthorization, CasaAccount, JointAccountHolder,
    JointAccountHolderAgreementAuthorization
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import (
    AGREEMENT_AUTHOR_TYPE_DD, BUSINESS_FORM_TKTT_DSH,
    CUSTOMER_RELATIONSHIP_TYPE_CUSTOMER_RELATIONSHIP, DROPDOWN_NONE_DICT,
    IMAGE_TYPE_SIGNATURE
)
from app.utils.error_messages import (
    ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST, ERROR_CALL_SERVICE_SOA,
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_CIF_NUMBER_NOT_EXIST, ERROR_NO_DATA,
    ERROR_RELATIONSHIP_EXIST
)
from app.utils.functions import dropdown, now


async def repos_check_list_cif_number(list_cif_number_request: list, session: Session) -> ReposReturn:
    list_customer = session.execute(
        select(
            Customer
        ).filter(Customer.cif_number.in_(list_cif_number_request))
    ).all()

    if not list_customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_NOT_EXIST, loc="joint_account_holders -> cif_number")

    return ReposReturn(data=list_customer)


async def repos_check_list_relationship_id(list_cif_number_relationship_request: list, session: Session) -> ReposReturn:
    list_relationship = session.execute(
        select(
            CustomerRelationshipType
        ).filter(CustomerRelationshipType.id.in_(list_cif_number_relationship_request))
    ).all()

    if not list_relationship:
        return ReposReturn(is_error=True, msg=ERROR_RELATIONSHIP_EXIST, loc="joint_account_holders -> customer_relationship")

    return ReposReturn(data=list_relationship)


async def repos_get_co_owner(cif_id: str, session: Session) -> ReposReturn:
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

    account_holders = session.execute(
        select(
            JointAccountHolder
        ).join(
            CasaAccount,
            CasaAccount.id == JointAccountHolder.casa_account_id
        ).filter(CasaAccount.customer_id == cif_id)
    ).scalars().all()

    customer_relationship_detail = []
    for account in account_holders:
        is_success, customer_relationship = await service_soa.retrieve_customer_ref_data_mgmt(
            cif_number=account.cif_num,
            flat_address=True,
        )
        customer_detail_data = customer_relationship['data']

        if customer_detail_data['basic_information']['gender']:
            gender = await repos_get_model_object_by_id_or_code(
                model_id=customer_detail_data['basic_information']['gender'],
                model_code=None,
                loc="[SERVICE][SOA] gender",
                model=CustomerGender,
                session=session
            )
            customer_detail_data['basic_information']['gender'] = dropdown(gender.data) if gender.data else DROPDOWN_NONE_DICT
        if customer_detail_data['basic_information']['nationality']:
            nationality = await repos_get_model_object_by_id_or_code(
                model_id=customer_detail_data['basic_information']['nationality'],
                model_code=None,
                loc="[SERVICE][SOA] nationality",
                model=AddressCountry,
                session=session
            )
            if nationality.data:
                customer_detail_data['basic_information']['nationality'] = dropdown(nationality.data)
        for relationship, relationship_type in customer_relationships:
            customer_detail_data['basic_information'].update({
                'customer_relationship': dropdown(relationship_type)
            })
        # TODO: place_of_issue query k có trong db crm nên đang để là str
        # if customer_detail_data['identity_document']['place_of_issue']:
        #
        #     place_of_issue_model = await get_optional_model_object_by_code_or_name(
        #         model=PlaceOfIssue,
        #         model_code=None,
        #         model_name=customer_detail_data['identity_document']['place_of_issue'],
        #         session=session
        #     )
        #     customer_detail_data['identity_document']['place_of_issue'] = dropdown(place_of_issue_model) if place_of_issue_model else DROPDOWN_NONE_DICT

        # TODO: pypass chữ ký vì trong SOA không có chữ ký
        customer_detail_data['basic_information'].update(
            {
                "signature": [
                    {
                        "id": "string",
                        "image_url": "https://example.com"
                    },
                    {
                        "id": "string",
                        "image_url": "https://example.com"
                    }
                ]
            }
        )

        customer_relationship_detail.append(customer_relationship.get('data'))

    return ReposReturn(data={
        "joint_account_holder_flag": account_holders[0].joint_account_holder_flag if account_holders else False,
        "number_of_joint_account_holder": len(account_holders),
        "joint_account_holders": customer_relationship_detail,
        "agreement_authorization": None
    })


async def repos_get_casa_account(cif_id: str, session: Session) -> ReposReturn:
    casa_account = session.execute(
        select(
            CasaAccount.id
        ).filter(CasaAccount.customer_id == cif_id)
    ).scalar()
    if not casa_account:
        return ReposReturn(is_error=True, msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc=f"cif_id: {cif_id}")
    return ReposReturn(data=casa_account)


@auto_commit
async def repos_save_co_owner(
        cif_id: str,
        save_account_holder: list,
        save_account_agree: list,
        save_cust_personal_relationship: list,
        log_data: json,
        session: Session,
        created_by: str
) -> ReposReturn:
    # lấy danh sách account holder để xóa
    account_holder_ids = session.execute(
        select(
            JointAccountHolder.id
        ).join(
            CasaAccount, and_(
                JointAccountHolder.casa_account_id == CasaAccount.id,
                CasaAccount.customer_id == cif_id
            )
        )
    ).scalars().all()

    # xóa JointAccountHolderAgreementAuthorization
    session.execute(
        delete(
            JointAccountHolderAgreementAuthorization
        ).filter(
            JointAccountHolderAgreementAuthorization.joint_account_holder_id.in_(account_holder_ids)
        )
    )

    # xóa account holder
    session.execute(
        delete(
            JointAccountHolder
        ).filter(JointAccountHolder.id.in_(account_holder_ids))
    )
    # xóa relationship
    session.execute(
        delete(
            CustomerPersonalRelationship
        ).filter(CustomerPersonalRelationship.customer_id == cif_id)
    )
    session.bulk_save_objects([JointAccountHolder(**data_insert) for data_insert in save_account_holder])

    session.bulk_save_objects(
        [JointAccountHolderAgreementAuthorization(**data_insert) for data_insert in save_account_agree])

    session.bulk_save_objects([
        CustomerPersonalRelationship(**data_insert) for data_insert in save_cust_personal_relationship
    ])
    await write_transaction_log_and_update_booking(
        description="Tạo CIF -> Tài khoản thanh toán -> Thông tin đồng sở hữu -- Tạo mới",
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TKTT_DSH
    )

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_list_cif_number(cif_id: str, session: Session):
    # lấy dữ liệu các đồng sở hữu của tài khoản thanh toán theo cif_id
    account_holders = session.execute(
        select(
            JointAccountHolder
        ).join(
            CasaAccount,
            CasaAccount.id == JointAccountHolder.casa_account_id
        ).filter(CasaAccount.customer_id == cif_id)
    ).all()

    # check account_holder
    if not account_holders:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc='cif_id')

    # lấy list cif_number trong account_holder
    list_cif_number = []
    for account_holder in account_holders:
        list_cif_number.append(account_holder.JointAccountHolder.cif_num)

    return ReposReturn(data=(account_holders, list_cif_number))


async def repos_get_customer_by_cif_number(list_cif_number: List[str], session: Session) -> ReposReturn:
    # lấy dữ liệu customer theo số cif_number
    customers = session.execute(
        select(
            Customer,
            AddressCountry,
            CustomerIdentity,
            CustomerIdentityImage,
            CustomerIndividualInfo,
            CustomerGender,
            PlaceOfIssue,
            CustomerIdentityType,
            CustomerPersonalRelationship,
            CustomerRelationshipType
        ).join(
            CustomerIdentity, Customer.id == CustomerIdentity.customer_id
        ).join(
            AddressCountry, Customer.nationality_id == AddressCountry.id
        ).join(
            PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id
        ).join(
            CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id
        ).join(
            CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id
        ).join(
            CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id
        ).join(
            CustomerPersonalRelationship, Customer.id == CustomerPersonalRelationship.customer_id
        ).join(
            CustomerRelationshipType,
            CustomerRelationshipType.id == CustomerPersonalRelationship.customer_relationship_type_id
        ).join(
            CustomerIdentityImage, and_(
                CustomerIdentity.id == CustomerIdentityImage.identity_id,
                CustomerIdentityImage.image_type_id == IMAGE_TYPE_SIGNATURE
            )
        ).filter(Customer.cif_number.in_(list_cif_number))
    ).all()

    if not customers:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_NOT_EXIST, loc='cif_number')

    return ReposReturn(data=customers)


async def repos_get_customer_address(list_cif_number: List[str], session: Session) -> ReposReturn:
    customer_address = session.execute(
        select(
            CustomerAddress,
        ).join(
            Customer, CustomerAddress.customer_id == Customer.id
        ).filter(Customer.cif_number.in_(list_cif_number))
    ).all()

    return ReposReturn(data=customer_address)


async def repos_get_agreement_authorizations(session: Session) -> ReposReturn:
    agreement_authorizations = session.execute(
        select(
            AgreementAuthorization
        ).filter(AgreementAuthorization.agreement_author_type == AGREEMENT_AUTHOR_TYPE_DD)
    ).scalars()

    if not agreement_authorizations:
        return ReposReturn(is_error=True, msg=ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST, loc='agreement_authorizations')

    return ReposReturn(data=agreement_authorizations)


async def repos_detail_co_owner(cif_id: str, cif_number_need_to_find: str, session: Session):

    is_success, detail_co_owner = await service_soa.retrieve_customer_ref_data_mgmt(
        cif_number=cif_number_need_to_find,
        flat_address=True
    )

    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_SOA, detail=detail_co_owner['message'])

    if not detail_co_owner["is_existed"]:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_NOT_EXIST,
            loc="cif_number",
            detail=f"cif_number={cif_number_need_to_find}"
        )

    detail_co_owner_data = detail_co_owner['data']
    basic_information = detail_co_owner_data['basic_information']

    # map gender(str) từ Service SOA thành gender(dropdown) CRM
    basic_information_gender = basic_information["gender"]
    if basic_information_gender:
        gender = await repos_get_model_object_by_id_or_code(
            model_id=basic_information_gender,
            model_code=None,
            loc="[SERVICE][SOA] gender",
            model=CustomerGender,
            session=session
        )
        basic_information["gender"] = dropdown(gender.data) if gender.data else DROPDOWN_NONE_DICT

    # map nationality(str) từ Service SOA thành nationality(dropdown) CRM
    basic_information_nationality = basic_information["nationality"]
    basic_information["nationality"] = DROPDOWN_NONE_DICT
    if basic_information_nationality:
        nationality = await repos_get_model_object_by_id_or_code(
            model_id=basic_information_nationality,
            model_code=None,
            loc="[SERVICE][SOA] nationality",
            model=AddressCountry,
            session=session
        )
        if nationality.data:
            basic_information["nationality"] = dropdown(nationality.data)

    # map place_of_issue(str) từ Service SOA thành place_of_issue(dropdown) CRM
    identity_document = detail_co_owner_data["identity_document"]
    basic_information_place_of_issue = identity_document["place_of_issue"]
    identity_document["place_of_issue"] = DROPDOWN_NONE_DICT
    if basic_information_place_of_issue:
        place_of_issue_model = await get_optional_model_object_by_code_or_name(
            model=PlaceOfIssue,
            model_code=None,
            model_name=basic_information_place_of_issue,
            session=session
        )
        if place_of_issue_model:
            identity_document["place_of_issue"] = dropdown(place_of_issue_model)

    signatures = []  # TODO: Chữ ký của cif phải được lấy từ thông tin của CIF trong DB,
    # phần này cần có 1 bước phê duyệt để có 1 CIF test
    customer_relationship = DROPDOWN_NONE_DICT  # TODO: Cần có mô tả về mối quan hệ với khách hàng thông qua số CIF

    basic_information.update(
        customer_relationship=customer_relationship,
        signature=signatures
    )

    # detail_co_owner = session.execute(
    #     select(
    #         Customer,
    #         CustomerIdentity,
    #         CustomerIndividualInfo,
    #         CustomerIdentityImage,
    #         AddressCountry,
    #         CustomerAddress,
    #         CustomerGender,
    #         PlaceOfIssue,
    #         CustomerIdentityType,
    #         CustomerPersonalRelationship,
    #         CustomerRelationshipType
    #     ).join(
    #         CustomerIdentity, CustomerIdentity.customer_id == Customer.id
    #     ).join(
    #         CustomerIndividualInfo, CustomerIndividualInfo.customer_id == Customer.id
    #     ).join(
    #         CustomerIdentityImage, and_(
    #             CustomerIdentity.id == CustomerIdentityImage.identity_id,
    #             CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_SIGNATURE
    #         )
    #     ).join(
    #         AddressCountry, Customer.nationality_id == AddressCountry.id
    #     ).join(
    #         CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id
    #     ).join(
    #         PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id
    #     ).join(
    #         CustomerPersonalRelationship,
    #         CustomerPersonalRelationship.customer_personal_relationship_cif_number == cif_number_need_to_find
    #     ).join(
    #         CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id
    #     ).join(
    #         CustomerRelationshipType,
    #         CustomerPersonalRelationship.customer_relationship_type_id == CustomerRelationshipType.id
    #     ).join(
    #         CustomerAddress, CustomerAddress.customer_id == Customer.id
    #     ).filter(Customer.cif_number == cif_number_need_to_find)
    # ).all()
    #
    # if not detail_co_owner:
    #     return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_NOT_EXIST, loc='cif_number')

    return ReposReturn(data=detail_co_owner['data'])
