from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress, CustomerContactTypeData, CustomerProfessional
)
from app.third_parties.oracle.models.cif.basic_information.fatca.model import (
    CustomerFatca, CustomerFatcaDocument
)
from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerSubIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.cif.debit_card.model import DebitCard
from app.third_parties.oracle.models.cif.e_banking.model import EBankingInfo
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount, JointAccountHolder, JointAccountHolderAgreementAuthorization
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.card import (
    BrandOfCard, CardIssuanceType
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerGender, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Branch, Career, FatcaCategory, MaritalStatus,
    Position, ResidentStatus
)
from app.third_parties.services.file import ServiceFile
from app.third_parties.services.tms import ServiceTMS
from app.utils.error_messages import ERROR_CALL_SERVICE_TEMPLATE


async def repos_branch_name(branch_id: str, session: Session):
    branch_name_info = session.execute(
        select(Branch.name).filter(Branch.id == branch_id)
    ).scalar()

    return ReposReturn(data=branch_name_info)


async def repos_teller_info(branch_id: str, session: Session):
    teller_info = session.execute(
        select(Branch.name).filter(Branch.id == branch_id)
    ).scalar()

    return ReposReturn(data=teller_info)


async def repo_form(data_request: dict, path: str) -> ReposReturn:
    body = {
        "parameter_values": {},
        "data_fill": data_request
    }

    service_tms = ServiceTMS()
    is_success, response = await service_tms.fill_form(body=body, path=path)

    if not is_success:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CALL_SERVICE_TEMPLATE,
            detail=str(response['message'])
        )

    if response.get('file_url'):
        response['file_url'] = ServiceFile().replace_with_cdn(response['file_url'])
    return ReposReturn(data=response)


async def repo_customer_info(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy thông tin khách hàng theo cif_id
    """
    customer_info = session.execute(
        select(
            Customer,
            CustomerIndividualInfo,
            CustomerIdentity,
            CustomerProfessional,
            AddressProvince,
            ResidentStatus,
            AddressCountry,
            PlaceOfIssue,
            Career,
            CustomerGender,
            AverageIncomeAmount,
            Position,
            MaritalStatus
        )
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(AddressProvince, CustomerIndividualInfo.place_of_birth_id == AddressProvince.id)
        .join(CustomerProfessional, Customer.customer_professional_id == CustomerProfessional.id)
        .join(AddressCountry, Customer.nationality_id == AddressCountry.id)
        .join(ResidentStatus, CustomerIndividualInfo.resident_status_id == ResidentStatus.id)
        .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(Career, CustomerProfessional.career_id == Career.id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .join(AverageIncomeAmount, CustomerProfessional.average_income_amount_id == AverageIncomeAmount.id)
        .outerjoin(Position, CustomerProfessional.position_id == Position.id)
        .join(MaritalStatus, CustomerIndividualInfo.marital_status_id == MaritalStatus.id)
        .filter(Customer.id == cif_id)
    ).all()
    return ReposReturn(data=customer_info)


async def repo_customer_contact_type_info(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy hình thức SCB liên hệ với khách hàng
    """
    customer_contact_type_info = session.execute(
        select(
            Customer,
            CustomerContactType
        )
        .outerjoin(CustomerContactTypeData, Customer.id == CustomerContactTypeData.customer_id)
        .outerjoin(CustomerContactType, CustomerContactTypeData.customer_contact_type_id == CustomerContactType.id)
        .filter(Customer.id == cif_id)
    ).all()
    return ReposReturn(data=customer_contact_type_info)


async def repo_customer_address(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy địa chỉ khách hàng theo cif_id
    """
    customer_address = session.execute(
        select(
            CustomerAddress,
            AddressWard,
            AddressDistrict,
            AddressProvince,
            AddressCountry,
        )
        .join(Customer, CustomerAddress.customer_id == Customer.id)
        .join(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .join(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .join(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id)
        .filter(Customer.id == cif_id)
    ).all()
    return ReposReturn(data=customer_address)


async def repo_sub_identity(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy giấy tờ định danh phụ theo cif_id
    """
    subs_identity = session.execute(
        select(
            CustomerSubIdentity
        ).filter(CustomerSubIdentity.customer_id == cif_id)
    ).scalars().all()
    return ReposReturn(data=subs_identity)


async def repo_guardians(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy thông tin người giám hộ
    """
    guardians = session.execute(
        select(
            CustomerPersonalRelationship,
            Customer,
            CustomerIdentity,
            CustomerRelationshipType
        )
        .join(Customer,
              CustomerPersonalRelationship.customer_personal_relationship_cif_number == Customer.cif_number)
        .join(CustomerIdentity, CustomerIdentity.customer_id == Customer.id)
        .join(CustomerRelationshipType,
              CustomerRelationshipType.id == CustomerPersonalRelationship.customer_relationship_type_id)
        .filter(CustomerPersonalRelationship.customer_id == cif_id)
    ).all()
    return ReposReturn(data=guardians)


async def repo_join_account_holder(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy thông tin đồng chủ tài khoản
    """
    join_account_holder = session.execute(
        select(
            JointAccountHolder.cif_num,
        )
        .join(JointAccountHolderAgreementAuthorization,
              JointAccountHolderAgreementAuthorization.joint_acc_agree_id == JointAccountHolder.joint_acc_agree_id)
        .join(CasaAccount,
              CasaAccount.id == JointAccountHolderAgreementAuthorization.casa_account_id)
        .join(Customer, Customer.id == CasaAccount.customer_id)
        .filter(Customer.id == cif_id)
    ).all()
    return ReposReturn(data=join_account_holder)


async def repo_debit_card(cif_id, session: Session) -> ReposReturn:
    """
    Lấy thông thẻ ghi nợ
    """
    parent_id = session.execute(select(DebitCard.id).filter(DebitCard.customer_id == cif_id)).scalar()
    debit_cards = None
    if parent_id:
        debit_cards = session.execute(
            select(
                DebitCard,
                Customer,
                BrandOfCard,
                CardIssuanceType,
                CasaAccount,
                CustomerIdentity,
            )
            .join(Customer, DebitCard.customer_id == Customer.id)
            .join(BrandOfCard, DebitCard.brand_of_card_id == BrandOfCard.id)
            .join(CardIssuanceType, DebitCard.card_issuance_type_id == CardIssuanceType.id)
            .outerjoin(CasaAccount, CasaAccount.customer_id == Customer.id)
            .join(CustomerIdentity, CustomerIdentity.customer_id == Customer.id)
            .filter(
                and_(
                    DebitCard.active_flag == 1,
                    or_(
                        DebitCard.customer_id == cif_id,
                        DebitCard.parent_card_id == parent_id
                    )
                )

            )).all()
    return ReposReturn(data=debit_cards)


async def repo_e_banking(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy thông tin E-Banking
    """
    e_bank_info = session.execute(
        select(
            EBankingInfo,
        ).filter(
            EBankingInfo.customer_id == cif_id
        )
    ).all()
    return ReposReturn(data=e_bank_info)


async def repos_fatca_info(cif_id: str, session: Session) -> ReposReturn:
    """
    Lấy thông tin Fatca
    """
    data_fatca = session.execute(
        select(
            CustomerFatca,
            FatcaCategory,
            CustomerFatcaDocument
        ).join(
            FatcaCategory, and_(
                CustomerFatca.fatca_category_id == FatcaCategory.id,
                CustomerFatca.customer_id == cif_id
            )
        ).outerjoin(
            CustomerFatcaDocument, CustomerFatca.id == CustomerFatcaDocument.customer_fatca_id
        ).order_by(FatcaCategory.order_no)
    ).first()
    return ReposReturn(data=data_fatca)
