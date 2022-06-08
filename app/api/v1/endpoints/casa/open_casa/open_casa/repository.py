from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.utils.error_messages import ERROR_CIF_NUMBER_NOT_EXIST


@auto_commit
async def repos_save_casa_casa_account(
        saving_casa_account: dict,
        session: Session
):
    session.add(
        CasaAccount(**saving_casa_account)
    )

    return ReposReturn(data=saving_casa_account)


########################################################################################################################
# Others
########################################################################################################################
async def repos_get_customer_by_cif_number(
        cif_number: str, session: Session
) -> ReposReturn:
    """
    Lấy dữ liệu customer theo số cif_number
    """
    customers = session.execute(
        select(
            Customer
        )
        # .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        # .join(AddressCountry, Customer.nationality_id == AddressCountry.id)
        # .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        # .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        # .join(
        #     CustomerIdentityType,
        #     CustomerIdentity.identity_type_id == CustomerIdentityType.id,
        # )
        # .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        # .join(
        #     CustomerPersonalRelationship,
        #     Customer.id == CustomerPersonalRelationship.customer_id,
        # )
        # .join(
        #     CustomerRelationshipType,
        #     CustomerRelationshipType.id
        #     == CustomerPersonalRelationship.customer_relationship_type_id,
        # )
        # .join(
        #     CustomerIdentityImage,
        #     and_(
        #         CustomerIdentity.id == CustomerIdentityImage.identity_id,
        #         CustomerIdentityImage.image_type_id == IMAGE_TYPE_SIGNATURE,
        #     ),
        # )
        .filter(Customer.cif_number == cif_number)
    ).scalar()

    if not customers:
        return ReposReturn(
            is_error=True, msg=ERROR_CIF_NUMBER_NOT_EXIST, loc="cif_number"
        )

    return ReposReturn(data=customers)
