from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.fatca.repository import (
    repos_get_fatca_data, repos_save_fatca_document
)
from app.api.v1.endpoints.cif.basic_information.fatca.schema import (
    FatcaRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking_code, repos_get_initializing_customer
)
from app.settings.event import service_file
from app.third_parties.oracle.models.master_data.others import FatcaCategory
from app.utils.constant.cif import (
    LANGUAGE_ID_EN, LANGUAGE_ID_VN, LANGUAGE_TYPE_EN, LANGUAGE_TYPE_VN
)
from app.utils.constant.tms_dms import TMS_DMS_DATETIME_FORMAT
from app.utils.functions import generate_uuid, string_to_datetime


class CtrFatca(BaseController):
    async def ctr_save_fatca(self, cif_id: str, fatca_request: FatcaRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # lấy list fatca_category_id trong fatca_information
        fatca_category_ids = []
        for fatca_id in fatca_request.fatca_information:
            fatca_category_ids.append(fatca_id.id)

        # lấy list fatca_category_id trong document_information
        # in_document_fatca_category_ids = []
        # image_uuids = []
        # for document in fatca_request.document_information:
        #     for fatca_document in document.documents:
        #         in_document_fatca_category_ids.append(fatca_document.id)
        #         # lấy uuids từ url request
        #         uuid = parse_file_uuid(fatca_document.url)
        #         fatca_document.url = uuid
        #         image_uuids.append(uuid)

        # gọi service file check exist list uuid
        # await self.check_exist_multi_file(uuids=image_uuids)

        # RULE: Nếu Fatca info chọn có thì phải có document gửi lên
        # for fatca in fatca_request.fatca_information:
        #     if fatca.select_flag and fatca.id not in in_document_fatca_category_ids:
        #         return self.response_exception(msg='', detail='fatca_information select_flag true if not document')
        #
        # fatca_category_ids.extend(in_document_fatca_category_ids)

        # check list id fatca_category có tồn tại hay không
        await self.get_model_objects_by_ids(
            model_ids=fatca_category_ids,
            model=FatcaCategory,
            loc='list_fatca_id'
        )

        fatca_category__customer_fatca_ids = {}
        for fatca in fatca_request.fatca_information:
            fatca_category__customer_fatca_ids[fatca.id] = generate_uuid()

        # lấy list data insert customer_fatca
        list_data_insert_fatca = [{
            "id": fatca_category__customer_fatca_ids[fatca.id],
            "fatca_category_id": fatca.id,
            "value": fatca.select_flag,
            "customer_id": cif_id
        } for fatca in fatca_request.fatca_information]

        # Tạp danh sách data insert fatca_document
        # list_data_insert_fatca_document = []
        # for language_document in fatca_request.document_information:
        #     for fatca_document in language_document.documents:
        #         list_data_insert_fatca_document.append({
        #             "customer_fatca_id": fatca_category__customer_fatca_ids[fatca_document.id],
        #             "document_language_type": language_document.language_type.id,
        #             "document_name": 'document_name',
        #             "document_url": fatca_document.url,
        #             "document_version": '1',
        #             "active_flag": 1,
        #             'created_at': now(),
        #             'order_no': None
        #         })

        data_response_success = self.call_repos(
            await repos_save_fatca_document(
                cif_id=cif_id,
                list_data_insert_fatca=list_data_insert_fatca,
                # list_data_insert_fatca_document=list_data_insert_fatca_document,
                log_data=fatca_request.json(),
                session=self.oracle_session,
            )
        )

        # Lấy Booking Code
        booking_code = self.call_repos(await repos_get_booking_code(
            cif_id=cif_id, session=self.oracle_session
        ))
        data_response_success.update(booking_code=booking_code)

        return self.response(data=data_response_success)

    async def ctr_get_fatca(self, cif_id: str):
        fatca_data = self.call_repos(await repos_get_fatca_data(cif_id=cif_id, session=self.oracle_session))

        fatca_information = {}

        for customer_fatca, fatca_category, customer_fatca_document in fatca_data:
            if fatca_category.id not in fatca_information:
                fatca_information[fatca_category.id] = {
                    "id": fatca_category.id,
                    "code": fatca_category.code,
                    "name": fatca_category.name,
                    "select_flag": customer_fatca.value,
                    "document_depend_language": {}
                }
            # check customer_fatca_document
            if customer_fatca_document is not None:
                document = {
                    "id": customer_fatca_document.id,
                    "name": customer_fatca_document.document_name,
                    "url": customer_fatca_document.document_url,
                    "active_flag": customer_fatca_document.active_flag,
                    "document_language_type": customer_fatca_document.document_language_type,
                    "version": customer_fatca_document.document_version,
                    "content_type": "Word",  # TODO
                    "size": "1MB",  # TODO
                    "folder_name": "Khởi tạo CIF",  # TODO
                    "created_by": "Nguyễn Phúc",  # TODO
                    "created_at": customer_fatca_document.created_at,
                    "updated_by": "Trần Bình Liên",  # TODO
                    "updated_at": "2020-12-30 06:07:08",  # TODO
                    "note": "Tài liệu quan trọng"  # TODO
                }

                if customer_fatca_document.document_language_type == LANGUAGE_ID_EN:
                    fatca_information[fatca_category.id]["document_depend_language"][LANGUAGE_TYPE_EN] = document

                if customer_fatca_document.document_language_type == LANGUAGE_ID_VN:
                    fatca_information[fatca_category.id]["document_depend_language"][LANGUAGE_TYPE_VN] = document

        # TODO : xét cứng dữ liệu language -> chưa thấy table lưu

        list_uuid = [
            "2241329a624349cebfef8b79c074f789",
            "75f07b53cc16441094f26a7eb286f3e3",
            "76d713361b8e42a4822e6edc75903830",
            "016667da70854d0cbc22787f97eddb0e",
            "d4512a424431435aa8cff41ac4ed9620",
            "6bb788ca97c84165a7260d9424a4e8c5",
            "1fc561187b38443ab9f717077178390f"
        ]
        en_documents = []
        download_files = await service_file.download_multi_file(list_uuid)
        for download_file in download_files:

            file_uuid = download_file['uuid']
            file_info = await service_file.get_file_info(file_uuid)
            code_name = (download_file['file_name']).split(".")[0].upper()
            en_documents.append(dict(
                id=file_uuid,
                code=code_name,
                name=download_file['file_name'],
                size=file_info['size'],
                url=download_file['file_url'],
                version=file_info['version'],
                created_by=file_info['created_by'],
                created_at=string_to_datetime(string=file_info['created_at'], _format=TMS_DMS_DATETIME_FORMAT),
                updated_by=file_info['updated_by'],
                updated_at=string_to_datetime(string=file_info['updated_at'], _format=TMS_DMS_DATETIME_FORMAT),
                # note=file_info['note']
                content_type=file_info['content_type']
            ))
        vi_documents = en_documents

        return self.response(data={
            "fatca_information": list(fatca_information.values()),
            "document_information": [
                {
                    "language_type": {
                        "id": LANGUAGE_ID_VN,
                        "code": LANGUAGE_TYPE_VN,
                        "name": "VN"
                    },
                    "documents": vi_documents
                },
                {
                    "language_type": {
                        "id": LANGUAGE_ID_EN,
                        "code": LANGUAGE_TYPE_EN,
                        "name": "EN"
                    },
                    "documents": en_documents
                }
            ]
        })
