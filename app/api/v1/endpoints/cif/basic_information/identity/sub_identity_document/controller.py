from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.repository import (
    repos_get_detail_sub_identity,
    repos_get_sub_identities_and_sub_identity_images,
    repos_get_sub_identity_log_list, repos_save_sub_identity
)
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import (
    SubIdentityDocumentRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.identity import (
    CustomerSubIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import IMAGE_TYPE_CODE_SUB_IDENTITY
from app.utils.functions import (
    date_to_string, generate_uuid, now, orjson_dumps, parse_file_uuid
)


class CtrSubIdentityDocument(BaseController):
    async def get_detail_sub_identity(self, cif_id: str):
        detail_datas = self.call_repos(
            await repos_get_detail_sub_identity(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        image_uuids = [detail_data['sub_identity_document_image_url'] for detail_data in detail_datas]
        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        for detail_data in detail_datas:
            sub_identity_document_image_url = detail_data['sub_identity_document_image_url']
            detail_data['sub_identity_document_image_url'] = uuid__link_downloads[sub_identity_document_image_url]

        return self.response(data=detail_datas)

    async def get_sub_identity_log_list(self, cif_id: str):
        sub_identity_image_transactions = self.call_repos(await repos_get_sub_identity_log_list(
            cif_id=cif_id, session=self.oracle_session
        ))

        sub_identity_log_infos = []

        if not sub_identity_image_transactions:
            return self.response(data=sub_identity_log_infos)

        # các uuid cần phải gọi qua service file để check
        image_uuids = [sub_identity_image_transaction.image_url
                       for sub_identity_image_transaction in sub_identity_image_transactions]

        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        date__sub_identity_images = {}

        for sub_identity_image_transaction in sub_identity_image_transactions:
            maker_at = date_to_string(sub_identity_image_transaction.maker_at)

            if maker_at not in date__sub_identity_images.keys():
                date__sub_identity_images[maker_at] = []

            date__sub_identity_images[maker_at].append({
                "image_url": uuid__link_downloads[sub_identity_image_transaction.image_url]
            })

        sub_identity_log_infos = [{
            "reference_flag": True if index == 0 else False,
            "created_date": created_date,
            "identity_images": identity_images
        } for index, (created_date, identity_images) in enumerate(date__sub_identity_images.items())]

        return self.response(data=sub_identity_log_infos)

    async def save_sub_identity(self, cif_id: str, sub_identity_request: List[SubIdentityDocumentRequest]):
        # check cif đang tạo
        customer = self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # các uuid cần phải gọi qua service file để check
        image_uuids = []

        for sub_identity in sub_identity_request:
            uuid = parse_file_uuid(sub_identity.sub_identity_document_image_url)
            sub_identity.sub_identity_document_image_url = uuid
            image_uuids.append(uuid)

        # gọi qua service file để check exist list uuid
        await self.check_exist_multi_file(uuids=image_uuids)

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

        saved_by = self.current_user.username

        # Giấy tờ định danh phụ:
        # + Nếu có gửi lên id là chỉnh sửa
        # + Không gửi lên id là tạo mới
        # + Những id có tồn tại trong hệ thống như không gửi lên là bị xóa

        delete_sub_identity_ids = []

        create_sub_identities = []
        create_sub_identity_images = []
        create_customer_sub_identity_image_transactions = []

        update_sub_identities = []
        update_sub_identity_images = []
        update_sub_identities_ids = []
        update_customer_sub_identity_image_transactions = []

        log_data = []

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
            customer_sub_identity_image_transaction = {
                "image_url": customer_sub_identity_image["image_url"],
                "active_flag": True,
                "maker_id": saved_by,
                "maker_at": now()
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

                customer_sub_identity_image_transaction['identity_image_id'] = customer_sub_identity_image['id']
                update_customer_sub_identity_image_transactions.append(customer_sub_identity_image_transaction)

            # Tạo mới
            else:
                sub_identity_id = generate_uuid()

                customer_sub_identity['id'] = sub_identity_id
                create_sub_identities.append(customer_sub_identity)

                customer_sub_identity_image['identity_id'] = sub_identity_id
                customer_sub_identity_image['id'] = generate_uuid()
                create_sub_identity_images.append(customer_sub_identity_image)

                customer_sub_identity_image_transaction['identity_image_id'] = customer_sub_identity_image['id']
                create_customer_sub_identity_image_transactions.append(customer_sub_identity_image_transaction)

            log_data.append(orjson_dumps({  # Vì data có trường hợp None nên parse sang json chuẩn dạng null
                "id": sub_identity.id,
                "name": sub_identity.name,
                "sub_identity_document_type": {
                    "id": sub_identity.sub_identity_document_type.id
                },
                "sub_identity_document_image_url": sub_identity.sub_identity_document_image_url,
                "ocr_result": {
                    "sub_identity_number": sub_identity.ocr_result.sub_identity_number,
                    "symbol": sub_identity.ocr_result.symbol,
                    "full_name_vn": sub_identity.ocr_result.full_name_vn,
                    "date_of_birth": date_to_string(sub_identity.ocr_result.date_of_birth),
                    "passport_number": sub_identity.ocr_result.passport_number,
                    "place_of_issue": {
                        "id": sub_identity.ocr_result.place_of_issue.id
                    },
                    "expired_date": date_to_string(sub_identity.ocr_result.expired_date),
                    "issued_date": date_to_string(sub_identity.ocr_result.issued_date)
                }
            }))

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
                create_customer_sub_identity_image_transactions=create_customer_sub_identity_image_transactions,
                update_sub_identities=update_sub_identities,
                update_sub_identity_images=update_sub_identity_images,
                update_customer_sub_identity_image_transactions=update_customer_sub_identity_image_transactions,
                session=self.oracle_session,
                log_data=log_data
            )
        )
        return self.response(data=info_save_document)
