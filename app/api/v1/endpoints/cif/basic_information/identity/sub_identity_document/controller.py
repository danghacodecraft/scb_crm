from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.repository import (
    repos_get_detail_sub_identity, repos_get_list_log,
    repos_get_sub_identities_and_sub_identity_images, repos_save_sub_identity
)
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import (
    SubIdentityDocumentRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.identity import (
    CustomerSubIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import IMAGE_TYPE_CODE_SUB_IDENTITY
from app.utils.functions import generate_uuid, now


class CtrSubIdentityDocument(BaseController):
    async def get_detail_sub_identity(self, cif_id: str):

        detail_data = self.call_repos(
            await repos_get_detail_sub_identity(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        return self.response(data=detail_data)

    async def get_list_log(self, cif_id: str):
        logs_data = self.call_repos(
            await repos_get_list_log(cif_id=cif_id)
        )
        return self.response(data=logs_data)

    async def save_sub_identity(self, cif_id: str, sub_identity_request: List[SubIdentityDocumentRequest]):
        # check cif đang tạo
        customer = self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        sub_identity_type_ids = []
        place_of_issue_ids = []
        for sub_identity in sub_identity_request:
            sub_identity_type_ids.append(sub_identity.sub_identity_document_type.id)
            place_of_issue_ids.append(sub_identity.ocr_result.place_of_issue.id)

        # check exist sub_identity_type_ids
        await self.get_model_objects_by_ids(model_ids=sub_identity_type_ids, model=CustomerSubIdentityType,
                                            loc="sub_identity_document_type -> id")

        # check exist place_of_issue_ids
        await self.get_model_objects_by_ids(model_ids=place_of_issue_ids, model=PlaceOfIssue,
                                            loc="ocr_result -> place_of_issue -> id")

        old_sub_identities_and_sub_identity_images = self.call_repos(
            await repos_get_sub_identities_and_sub_identity_images(customer_id=cif_id, session=self.oracle_session)
        )

        old_sub_identity_ids = [old_sub_identity.id
                                for old_sub_identity, _ in old_sub_identities_and_sub_identity_images]

        old_sub_identity_id__image_ids = {}
        for _, old_sub_identity_image in old_sub_identities_and_sub_identity_images:
            old_sub_identity_id__image_ids[old_sub_identity_image.identity_id] = old_sub_identity_image.id

        saved_by = self.current_user.full_name_vn

        # Giấy tờ định danh phụ:
        # + Nếu có gửi lên id là chỉnh sửa
        # + Không gửi lên id là tạo mới
        # + Những id có tồn tại trong hệ thống như không gửi lên là bị xóa

        delete_sub_identity_ids = []

        create_sub_identities = []
        create_sub_identity_images = []

        update_sub_identities = []
        update_sub_identity_images = []
        update_sub_identities_ids = []

        for sub_identity in sub_identity_request:
            customer_sub_identity = {
                "sub_identity_type_id": sub_identity.sub_identity_document_type.id,
                "name": sub_identity.name,
                "number": sub_identity.ocr_result.sub_identity_number,
                "symbol": sub_identity.ocr_result.symbol,
                "full_name": sub_identity.ocr_result.full_name_vn,
                "date_of_birth": sub_identity.ocr_result.date_of_birth,
                "passport_number": sub_identity.ocr_result.passport_number,
                "issued_date": sub_identity.ocr_result.issued_date,
                "sub_identity_expired_date": sub_identity.ocr_result.expired_date,
                "place_of_issue_id": sub_identity.ocr_result.place_of_issue.id,
                "customer_id": customer.id,
                "maker_at": now(),
                "maker_id": saved_by,
                "updater_at": now(),
                "updater_id": saved_by
            }
            customer_sub_identity_image = {
                "image_type_id": IMAGE_TYPE_CODE_SUB_IDENTITY,
                "image_url": sub_identity.sub_identity_document_image_url,
                "maker_id": saved_by,
                "maker_at": now(),
                "updater_id": saved_by,
                "updater_at": now()
            }

            # Cập nhật
            if sub_identity.id:
                # Trả lỗi nếu id gửi lên không tồn tại
                if sub_identity.id not in old_sub_identity_ids:
                    return self.response_exception(
                        msg='',
                        detail='sub_identity_id is not exist',
                        loc='id'
                    )

                customer_sub_identity['id'] = sub_identity.id
                update_sub_identities.append(customer_sub_identity)

                update_sub_identities_ids.append(customer_sub_identity['id'])

                customer_sub_identity_image['identity_id'] = sub_identity.id
                customer_sub_identity_image['id'] = old_sub_identity_id__image_ids[sub_identity.id]
                update_sub_identity_images.append(customer_sub_identity_image)

            # Tạo mới
            else:
                sub_identity_id = generate_uuid()

                customer_sub_identity['id'] = sub_identity_id
                create_sub_identities.append(customer_sub_identity)

                customer_sub_identity_image['identity_id'] = sub_identity_id
                create_sub_identity_images.append(customer_sub_identity_image)

        # những SubIdentity id tồn tại trong hệ thống mà không gửi lên -> xóa
        for old_sub_identity, _ in old_sub_identities_and_sub_identity_images:
            if old_sub_identity.id not in update_sub_identities_ids:
                delete_sub_identity_ids.append(old_sub_identity.id)

        info_save_document = self.call_repos(
            await repos_save_sub_identity(
                customer=customer,
                delete_sub_identity_ids=delete_sub_identity_ids,
                create_sub_identities=create_sub_identities,
                create_sub_identity_images=create_sub_identity_images,
                update_sub_identities=update_sub_identities,
                update_sub_identity_images=update_sub_identity_images,
                session=self.oracle_session
            )
        )
        return self.response(data=info_save_document)
