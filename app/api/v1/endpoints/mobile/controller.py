from fastapi import UploadFile

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_upload_identity_document_and_ocr
)
from app.utils.constant.cif import (
    EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD,
    EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD, EKYC_IDENTITY_TYPE_PASSPORT,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_PASSPORT
)


class CtrIdentityMobile(BaseController):

    async def save_identity_mobile(
            self,
            full_name: str,
            date_of_birth: str,
            gender: str,
            nationality: str,
            identity_number: str,
            issued_date: str,
            expired_date: str,
            place_of_issued: str,
            identity_type: str,
            front_side_image: UploadFile,
            back_side_image: UploadFile,
            avatar_image: UploadFile,
            signature_image: UploadFile,
    ):
        # check back_side khi truyền identity_type không phải hộ chiếu
        print('identity_type', identity_type)
        if identity_type != IDENTITY_DOCUMENT_TYPE_PASSPORT and not back_side_image:
            return self.response_exception(msg='MISSING BACK_SIDE')

        front_side_image_name = front_side_image.filename
        front_side_image = await front_side_image.read()

        orc_data = None
        if identity_type == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            orc_data = self.call_repos(await repos_upload_identity_document_and_ocr(
                image_file=front_side_image,
                image_file_name=front_side_image_name,
                identity_type=EKYC_IDENTITY_TYPE_PASSPORT,
                session=self.oracle_session
            ))
        if back_side_image:
            back_side_image_name = back_side_image.filename
            back_side_image = await back_side_image.read()

            if identity_type == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
                orc_data = self.call_repos(await repos_upload_identity_document_and_ocr(
                    image_file=front_side_image,
                    image_file_name=front_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD,
                    session=self.oracle_session
                ))

                orc_data.update(self.call_repos(await(repos_upload_identity_document_and_ocr(
                    image_file=back_side_image,
                    image_file_name=back_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_BACK_SIDE_IDENTITY_CARD,
                    session=self.oracle_session
                ))))

            if identity_type == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
                orc_data = self.call_repos(await repos_upload_identity_document_and_ocr(
                    image_file=front_side_image,
                    image_file_name=front_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_FRONT_SIDE_CITIZEN_CARD,
                    session=self.oracle_session
                ))

                orc_data.update(self.call_repos(await(repos_upload_identity_document_and_ocr(
                    image_file=back_side_image,
                    image_file_name=back_side_image_name,
                    identity_type=EKYC_IDENTITY_TYPE_BACK_SIDE_CITIZEN_CARD,
                    session=self.oracle_session
                ))))

        return self.response(data=orc_data)
