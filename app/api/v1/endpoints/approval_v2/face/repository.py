from typing import List

from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.booking.model import BookingCompareImage
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction
)


@auto_commit
async def repos_save_approval_compare_face(
        saving_customer_compare_images: List,
        saving_customer_compare_image_transactions: List,
        saving_booking_compare_images: List,
        session: Session
):
    """
    Lưu hình ảnh So sánh ở bước Phê duyệt
    """

    session.bulk_save_objects([
        CustomerCompareImage(**customer_compare_image)
        for customer_compare_image in saving_customer_compare_images
    ])
    session.bulk_save_objects([
        CustomerCompareImageTransaction(**customer_compare_image_transaction)
        for customer_compare_image_transaction in saving_customer_compare_image_transactions
    ])
    session.bulk_save_objects([
        BookingCompareImage(**saving_booking_compare_image)
        for saving_booking_compare_image in saving_booking_compare_images
    ])
    session.flush()

    return ReposReturn(data=None)
