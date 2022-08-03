from app.api.base.controller import BaseController
from app.api.v1.endpoints.ekyc.repository import (
    repos_create_ekyc_customer
)
from app.api.v1.endpoints.ekyc.schema import CreateEKYCCustomerRequest
from app.utils.functions import generate_uuid, orjson_dumps, orjson_loads


class CtrEKYC(BaseController):
    async def ctr_create_ekyc_customer(self, request: CreateEKYCCustomerRequest):
        customer_ekyc_id = request.customer_id

        # print(orjson_dumps(request.dict()))

        customer_ekyc = dict(
            customer_id=customer_ekyc_id,
            # transaction_data=orjson_dumps(request.dict()),
            date_of_issue=request.date_of_issue,
            date_of_birth=request.date_of_birth,
            transaction_id=request.transaction_id,
            document_id=request.document_id,
            document_type=request.document_type,
            date_of_expiry=request.date_of_expiry,
            place_of_issue=request.place_of_issue,
            qr_code_data=request.qr_code_data,
            full_name=request.full_name,
            gender=request.gender,
            place_of_residence=request.place_of_residence,
            place_of_origin=request.place_of_origin,
            nationality=request.nationality,
            address_1=request.address_1,
            address_2=request.address_2,
            address_3=request.address_3,
            address_4=request.address_4,
            permanent_address=orjson_dumps(request.permanent_address),
            phone_number=request.phone_number,
            ocr_data=orjson_dumps(request.ocr_data),
            ocr_data_errors=orjson_dumps(request.ocr_data_errors),
            faces_matching_percent=request.faces_matching_percent,
            extra_info=orjson_dumps(request.extra_info),
            receive_ads=request.receive_ads,
            longitude=request.longitude,
            latitude=request.latitude,
            cif=request.cif,
            account_number=request.account_number,
            job_title=request.job_title,
            organization=request.organization,
            organization_address=request.organization_address,
            organization_phone_number=request.organization_phone_number,
            position=request.position,
            salary_range=request.salary_range,
            tax_number=request.tax_number,
            open_biometric=request.open_biometric,
            # avatar_image_url=request.avatar_image_url,
            # avatar_image_uri=request.avatar_image_uri,
            # attachment_info=orjson_dumps(request.attachment_info),
            # finger_ids=request.finger_ids,
            # face_ids=request.face_ids,
            # ekyc_level=request.ekyc_level,
            # ekyc_step=request.ekyc_step,
            # kss_status=request.kss_status,
            # status=request.status,
            user_eb=request.user_eb
        )

        steps = []
        ekyc_steps = request.ekyc_step
        if ekyc_steps:
            for ekyc_step in ekyc_steps:
                transaction_id = ekyc_step.transaction_id
                for info in ekyc_step.info_step:
                    steps.append(dict(
                        customer_id=customer_ekyc_id,
                        transaction_id=transaction_id,
                        step=info.step,
                        step_status=info.step_status,
                        reason=info.reason,
                        update_at=info.update_at,
                        start_date=info.start_date,
                        end_date=info.end_date
                    ))
        self.call_repos(await repos_create_ekyc_customer(
            customer=customer_ekyc,
            steps=steps,
            session=self.oracle_session
        ))

        return self.response(data=dict(
            customer_id=customer_ekyc_id
        ))
