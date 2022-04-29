from loguru import logger
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction,
    CustomerIdentityImage, CustomerIdentityImageTransaction
)


async def create_customer_identity_image_and_customer_compare_image(
        identity_id: str,
        new_first_identity_image_id,
        new_second_identity_image_id,
        saving_customer_identity_images,
        saving_customer_compare_image,
        is_create: bool,
        session: Session
):
    """
        Tạo giấy tờ định danh lưu log
    """
    new_first_identity_image = saving_customer_identity_images[0]
    new_first_identity_image['id'] = new_first_identity_image_id
    new_first_identity_image['identity_id'] = identity_id

    session.add_all([
        CustomerIdentityImage(**new_first_identity_image),
        CustomerIdentityImageTransaction(**{
            "identity_image_id": new_first_identity_image['id'],
            "image_url": new_first_identity_image['image_url'],
            "active_flag": True,
            "maker_id": new_first_identity_image['maker_id'],
            "maker_at": new_first_identity_image['maker_at']
        })
    ])
    # tạo CustomerIdentityImage mặt sau nếu có
    if len(saving_customer_identity_images) > 1:
        new_second_identity_image = saving_customer_identity_images[1]
        new_second_identity_image['id'] = new_second_identity_image_id
        new_second_identity_image['identity_id'] = identity_id
        session.add_all([
            CustomerIdentityImage(**new_second_identity_image),
            CustomerIdentityImageTransaction(**{
                "identity_image_id": new_second_identity_image['id'],
                "image_url": new_second_identity_image['image_url'],
                "active_flag": True,
                "maker_id": new_second_identity_image['maker_id'],
                "maker_at": new_second_identity_image['maker_at']
            })
        ])
    # tạo mới CustomerCompareImage
    compare_transaction_parent_id = None
    saving_customer_compare_image['identity_id'] = identity_id
    saving_customer_compare_image['identity_image_id'] = new_second_identity_image_id

    if not is_create:
        try:
            compare_transaction_parent_id = session.execute(
                select(
                    CustomerIdentityImageTransaction.id
                )
                .join(CustomerIdentityImage,
                      CustomerIdentityImageTransaction.identity_image_id == CustomerIdentityImage.id)
                .join(CustomerCompareImage,
                      CustomerCompareImageTransaction.compare_image_id == CustomerCompareImage.id)
                .order_by(desc(CustomerCompareImageTransaction.maker_at))
            ).scalars().first()
        except Exception as ex:
            logger.error(str(ex))
            return True, dict(message="Write Transaction Error")

    return False, dict(compare_transaction_parent_id=compare_transaction_parent_id)
