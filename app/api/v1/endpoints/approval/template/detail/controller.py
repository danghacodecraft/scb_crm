import ast

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.common_repository import (
    repos_get_next_receiver, repos_get_next_stage, repos_get_previous_stage,
    repos_get_previous_transaction_daily, repos_get_stage_information
)
from app.api.v1.endpoints.approval.template.detail.repository import (
    repo_customer_address, repo_customer_info, repo_debit_card, repo_e_banking,
    repo_form, repo_guardians, repo_join_account_holder, repo_sub_identity,
    repos_approve, repos_get_approval_process
)
from app.api.v1.endpoints.approval.template.detail.schema import (
    CifApproveRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.settings.config import DATE_INPUT_OUTPUT_EKYC_FORMAT
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.approval import (
    CIF_STAGE_APPROVE_KSS, CIF_STAGE_APPROVE_KSV, CIF_STAGE_BEGIN,
    CIF_STAGE_COMPLETED, CIF_STAGE_INIT
)
from app.utils.constant.cif import (
    BUSINESS_TYPE_INIT_CIF, CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
)
from app.utils.constant.tms_dms import (
    PATH_FORM_1, PATH_FORM_2, PATH_FORM_3, PATH_FORM_5
)
from app.utils.error_messages import (
    ERROR_CONTENT_NOT_NULL, ERROR_STAGE_COMPLETED, MESSAGE_STATUS
)
from app.utils.functions import (
    datetime_to_string, generate_uuid, now, orjson_dumps, orjson_loads, today
)


class CtrForm(BaseController):
    async def ctr_approval_process(self, cif_id: str):
        transactions = self.call_repos((await repos_get_approval_process(cif_id=cif_id, session=self.oracle_session)))
        response_data = []
        lst_parent = {}

        for _, _, _, _, transaction_root_daily in transactions:
            lst_parent.update({transaction_root_daily.created_at.date(): []})

        for parent_key, parent_value in lst_parent.items():
            childs = []

            for booking_customer, _, transaction_daily, transaction_sender, transaction_root_daily in transactions:
                content = orjson_loads(transaction_root_daily.data)
                if parent_key == transaction_root_daily.created_at.date():
                    childs.append({
                        "user_id": transaction_sender.user_id,
                        "full_name_vn": transaction_sender.user_fullname,
                        "avatar_url": None,
                        "position": {
                            "id": transaction_sender.position_id,
                            "code": transaction_sender.position_code,
                            "name": transaction_sender.position_name
                        },
                        "created_at": transaction_root_daily.created_at,
                        "content": content['content'] if content else ""
                    })
            response_data.append({
                "created_at": parent_key,
                "logs": childs
            })

        return self.response(data=response_data)

    async def ctr_get_approval(self, cif_id: str):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # Kiểm tra xem đang ở bước nào của giao dịch
        _, _, previous_transaction_daily, previous_transaction_stage, _, previous_transaction_sender = self.call_repos(
            await repos_get_previous_stage(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        previous_stage_code = None
        stage_teller = dict()
        teller_is_completed = False
        teller_content = None
        teller_created_at = None
        teller_created_by = None

        stage_supervisor = dict()
        supervisor_stage_code = None
        supervisor_is_disable = True
        supervisor_is_completed = False
        supervisor_content = None
        supervisor_created_at = None
        supervisor_created_by = None

        stage_audit = dict()
        audit_stage_code = None
        audit_is_disable = True
        audit_is_completed = False
        audit_content = None
        audit_created_at = None
        audit_created_by = None

        if previous_transaction_stage:
            previous_stage_code = previous_transaction_stage.transaction_stage_phase_code

        stages = []
        # GDV chưa gửi hồ sơ
        if previous_stage_code == CIF_STAGE_BEGIN:
            teller_is_disable = False
            teller_stage_code = None
        # KSV nhận hồ sơ từ GDV
        elif previous_stage_code == CIF_STAGE_INIT:
            teller_stage_code = previous_stage_code
            teller_is_disable = False
            teller_is_completed = True
            teller_content = ast.literal_eval(previous_transaction_daily.data)["content"]
            teller_created_at = previous_transaction_daily.created_at
            teller_created_by = previous_transaction_sender.user_fullname

        # KSS nhận hồ sơ từ KSV
        elif previous_stage_code == CIF_STAGE_APPROVE_KSV:
            supervisor_stage_code = previous_stage_code
            supervisor_transaction_daily = previous_transaction_daily
            supervisor_transaction_sender = previous_transaction_sender
            supervisor_is_disable = False
            supervisor_is_completed = True
            supervisor_content = ast.literal_eval(supervisor_transaction_daily.data)["content"]
            supervisor_created_at = supervisor_transaction_daily.created_at
            supervisor_created_by = supervisor_transaction_sender.user_fullname

            teller_transaction_daily, teller_transaction_sender, teller_transaction_stage, _ = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=supervisor_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            teller_stage_code = teller_transaction_stage.transaction_stage_phase_code
            teller_is_disable = False
            teller_is_completed = True
            teller_content = ast.literal_eval(teller_transaction_daily.data)["content"]
            teller_created_at = teller_transaction_daily.created_at
            teller_created_by = teller_transaction_sender.user_fullname

        # KSS đã duyệt hồ sơ
        else:
            audit_stage_code = previous_stage_code
            audit_transaction_daily = previous_transaction_daily
            audit_transaction_sender = previous_transaction_sender
            audit_is_disable = False
            audit_is_completed = True
            audit_content = ast.literal_eval(audit_transaction_daily.data)["content"]
            audit_created_at = audit_transaction_daily.created_at
            audit_created_by = audit_transaction_sender.user_fullname

            supervisor_transaction_daily, supervisor_transaction_sender, supervisor_transaction_stage, _ = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=audit_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            supervisor_stage_code = supervisor_transaction_stage.transaction_stage_phase_code
            supervisor_is_disable = False
            supervisor_is_completed = True
            supervisor_content = ast.literal_eval(supervisor_transaction_daily.data)["content"]
            supervisor_created_at = supervisor_transaction_daily.created_at
            supervisor_created_by = supervisor_transaction_sender.user_fullname

            teller_transaction_daily, teller_transaction_sender, teller_transaction_stage, _ = self.call_repos(
                await repos_get_previous_transaction_daily(
                    transaction_daily_id=supervisor_transaction_daily.transaction_id,
                    session=self.oracle_session
                ))
            teller_stage_code = teller_transaction_stage.transaction_stage_phase_code
            teller_is_disable = False
            teller_is_completed = True
            teller_content = ast.literal_eval(teller_transaction_daily.data)["content"]
            teller_created_at = teller_transaction_daily.created_at
            teller_created_by = teller_transaction_sender.user_fullname

        stage_teller.update(dict(
            stage_code=teller_stage_code,
            is_disable=teller_is_disable,
            is_completed=teller_is_completed,
            content=teller_content,
            created_at=teller_created_at,
            created_by=teller_created_by
        ))
        stage_supervisor.update(dict(
            stage_code=supervisor_stage_code,
            is_disable=supervisor_is_disable,
            is_completed=supervisor_is_completed,
            content=supervisor_content,
            created_at=supervisor_created_at,
            created_by=supervisor_created_by
        ))
        stage_audit.update(dict(
            stage_code=audit_stage_code,
            is_disable=audit_is_disable,
            is_completed=audit_is_completed,
            content=audit_content,
            created_at=audit_created_at,
            created_by=audit_created_by
        ))

        stages.extend([stage_teller, stage_supervisor, stage_audit])
        return self.response(data=dict(
            cif_id=cif_id,
            stages=stages
        ))

    async def ctr_approve(
            self,
            cif_id: str,
            request: CifApproveRequest
    ):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        content = request.content
        reject_flag = request.reject_flag
        business_type_id = BUSINESS_TYPE_INIT_CIF
        current_user = self.current_user

        _, _, _, previous_transaction_stage, _, _ = self.call_repos(
            await repos_get_previous_stage(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        ################################################################################################################
        # PREVIOUS STAGE
        ################################################################################################################
        is_stage_init = True
        previous_stage_code = None
        if previous_transaction_stage:
            is_stage_init = False
            _, previous_stage, _, _, _, _, _ = self.call_repos(
                await repos_get_stage_information(
                    business_type_id=business_type_id,
                    stage_id=previous_transaction_stage.transaction_stage_phase_code,
                    session=self.oracle_session
                ))
            previous_stage_code = previous_stage.code

        ################################################################################################################
        # CURRENT STAGE
        ################################################################################################################
        if not is_stage_init:
            current_stage = self.call_repos(await repos_get_next_stage(
                business_type_id=business_type_id,
                current_stage_code=previous_stage_code,
                session=self.oracle_session
            ))
            current_stage_code = current_stage.code
        else:
            current_stage_code = CIF_STAGE_INIT

        if current_stage_code == CIF_STAGE_COMPLETED:
            return self.response_exception(
                msg=ERROR_STAGE_COMPLETED,
                loc=f"current_stage: {current_stage_code}",
                detail=MESSAGE_STATUS[ERROR_STAGE_COMPLETED]
            )

        current_stage_status, current_stage, _, current_lane, _, current_phase, current_stage_role = self.call_repos(
            await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=current_stage_code,
                session=self.oracle_session
            ))

        current_stage_status_code = None
        current_stage_status_name = None
        current_stage_name = None
        current_lane_code = None
        current_lane_name = None
        current_phase_code = None
        current_phase_name = None
        current_stage_role_code = None
        current_stage_role_name = None

        if current_stage:
            current_stage_status_code = current_stage_status.code
            current_stage_status_name = current_stage_status.name
            current_stage_name = current_stage.name
            current_lane_code = current_lane.code
            current_lane_name = current_lane.name
            current_phase_code = current_phase.code
            current_phase_name = current_phase.name
            current_stage_role_code = current_stage_role.code
            current_stage_role_name = current_stage_role.name

        ################################################################################################################
        # NEXT STAGE
        ################################################################################################################
        next_stage = self.call_repos(await repos_get_next_stage(
            business_type_id=business_type_id,
            current_stage_code=current_stage_code,
            session=self.oracle_session
        ))
        next_stage_code = next_stage.code
        next_stage_role_code = None
        if next_stage_code != CIF_STAGE_COMPLETED:
            _, next_stage, _, _, _, _, next_stage_role = self.call_repos(await repos_get_stage_information(
                business_type_id=business_type_id,
                stage_id=next_stage_code,
                session=self.oracle_session
            ))
            next_stage_role_code = next_stage_role.code

        saving_transaction_stage_status_id = generate_uuid()
        saving_transaction_stage_id = generate_uuid()
        saving_transaction_stage_lane_id = generate_uuid()
        saving_transaction_stage_phase_id = generate_uuid()
        saving_transaction_stage_role_id = generate_uuid()
        transaction_daily_id = generate_uuid()

        saving_transaction_stage_status = dict(
            id=saving_transaction_stage_status_id,
            code=current_stage_status_code,
            name=current_stage_status_name
        )

        saving_transaction_stage_lane = dict(
            id=saving_transaction_stage_lane_id,
            code=current_lane_code,
            name=current_lane_name
        )

        saving_transaction_stage_phase = dict(
            id=saving_transaction_stage_phase_id,
            code=current_phase_code,
            name=current_phase_name
        )

        saving_transaction_stage_role = dict(
            id=saving_transaction_stage_role_id,
            code=current_stage_role_code,
            name=current_stage_role_name
        )

        saving_transaction_stage = dict(
            id=saving_transaction_stage_id,
            status_id=saving_transaction_stage_status_id,
            lane_id=saving_transaction_stage_lane_id,
            phase_id=saving_transaction_stage_phase_id,
            business_type_id=business_type_id,
            sla_transaction_id=None,  # TODO
            transaction_stage_phase_code=current_stage_code,
            transaction_stage_phase_name=current_stage_name
        )

        description = await self.get_description(
            current_stage_code=current_stage_code,
            current_stage_role_code=current_stage_role_code,
            next_stage_role_code=next_stage_role_code,
            reject_flag=reject_flag,
            content=content
        )
        json_data = dict(content=content)
        saving_transaction_daily = dict(
            transaction_id=transaction_daily_id,
            transaction_stage_id=saving_transaction_stage_id,
            transaction_parent_id=None,
            transaction_root_id=None,
            is_reject=False,
            data=orjson_dumps(json_data),
            description=description,
            created_at=now(),
            updated_at=now()
        )

        saving_transaction_sender = dict(
            transaction_id=transaction_daily_id,
            user_id=current_user.code,
            user_name=current_user.username,
            user_fullname=current_user.name,
            user_email=current_user.email,
            branch_id=current_user.hrm_branch_id,
            branch_code=current_user.hrm_branch_code,
            branch_name=current_user.hrm_branch_name,
            department_id=current_user.hrm_department_id,
            department_code=current_user.hrm_department_code,
            department_name=current_user.hrm_department_name,
            position_id=current_user.hrm_position_id,
            position_code=current_user.hrm_position_code,
            position_name=current_user.hrm_position_name
        )

        receiver_branch = None
        receiver_lane = self.call_repos(await repos_get_next_receiver(
            business_type_id=business_type_id,
            current_stage_id=current_stage_code,
            reject_flag=reject_flag,
            session=self.oracle_session
        ))
        if receiver_lane:
            receiver_branch = await self.get_model_object_by_id(
                model_id=receiver_lane.branch_id,
                model=Branch,
                loc="next_receiver -> branch_id"
            )
            # receiver_department = await self.get_model_object_by_id(
            #     model_id=next_receiver.department_id,
            #     model=Department,
            #     loc="next_receiver -> department_id"
            # )

        saving_transaction_receiver = dict(
            transaction_id=transaction_daily_id,
            user_id=current_user.code,
            user_name=current_user.username,
            user_fullname=current_user.name,
            user_email=current_user.email,
            branch_id=receiver_branch.id if receiver_lane else None,
            branch_code=receiver_branch.code if receiver_lane else None,
            branch_name=receiver_branch.name if receiver_lane else None,
            department_id=receiver_lane.department_id if receiver_lane else None,
            department_code=None,  # TODO
            department_name=None,  # TODO
            position_id=None,  # TODO
            position_code=None,  # TODO
            position_name=None  # TODO
        )

        approval_process = self.call_repos((await repos_approve(
            cif_id=cif_id,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_transaction_receiver=saving_transaction_receiver,
            is_stage_init=is_stage_init,
            session=self.oracle_session
        )))

        approval_process.update(
            previous_stage=previous_stage_code,
            current_stage=current_stage_code,
            next_stage=next_stage_code,
        )

        return self.response(approval_process)

    async def get_description(
            self,
            current_stage_code: str,
            current_stage_role_code: str,
            next_stage_role_code: str,
            reject_flag: bool,
            content: str
    ):
        # GDV
        if current_stage_code == CIF_STAGE_INIT:
            description = f"{current_stage_role_code} đã gửi hồ sơ cho {next_stage_role_code}."
        else:
            # KSV
            if current_stage_code == CIF_STAGE_APPROVE_KSV:
                if not reject_flag:
                    description = f"Hoàn tất hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role_code}" \
                                  f". Hồ sơ đã gửi cho {next_stage_role_code}."
                else:
                    if not content:
                        return self.response_exception(msg=ERROR_CONTENT_NOT_NULL, loc="content")
                    description = f"Hồ sơ bị từ chối. Lý do: {content}"
            # KSS
            elif current_stage_code == CIF_STAGE_APPROVE_KSS:
                if not reject_flag:
                    description = f"Hoàn thành hồ sơ. Hồ sơ đã được phê duyệt bởi {current_stage_role_code}."
                else:
                    if not content:
                        return self.response_exception(msg=ERROR_CONTENT_NOT_NULL, loc="content")
                    description = f"Hồ sơ bị từ chối. Lý do: {content}"
            else:
                return self.response_exception(msg=ERROR_STAGE_COMPLETED, loc="description")

        return description

    async def ctr_form_1(self, cif_id: str):
        """
        Biểu mẫu 1
        """
        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]

        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        subs_identity = self.call_repos(await repo_sub_identity(cif_id=cif_id, session=self.oracle_session))
        guardians = self.call_repos(await repo_guardians(cif_id=cif_id, session=self.oracle_session))
        customer_join = self.call_repos(await repo_join_account_holder(cif_id=cif_id, session=self.oracle_session))
        debit_cards = self.call_repos(await repo_debit_card(cif_id=cif_id, session=self.oracle_session))
        e_banking = self.call_repos(await repo_e_banking(cif_id=cif_id, session=self.oracle_session))
        # fatca_info = self.call_repos(await repos_fatca_info(cif_id=cif_id, session=self.oracle_session))

        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None
        if debit_cards:
            for address in customer_address:
                if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                    staying_address = address
                if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                    resident_address = address

        # Tách thẻ chính và thẻ phụ
        main_cards, sup_cards = [], []
        for item in debit_cards:
            if item.DebitCard.parent_card_id:
                sup_cards.append(item)
            else:
                main_cards.append(item)

        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": [cust.CustomerGender.name],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.2.23": [cust.ResidentStatus.name],
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.36": subs_identity[0].name,
            "S1.A.1.2.38": datetime_to_string(subs_identity[0].sub_identity_expired_date,
                                              DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            # TODO: Địa chỉ cư trú tại nước ngoài (chưa có)
            # "S1.A.1.2.30"
            # "S1.A.1.2.31"
            # "S1.A.1.2.32"
            # "S1.A.1.2.33"

            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.6": ["Đồng ý"] if cust.Customer.advertising_marketing_flag else ["Không đồng ý"],

            "S1.A.1.5.4": [cust.Career.name],
            "S1.A.1.5.3": [cust.AverageIncomeAmount.name],
            "S1.A.1.2.9": [cust.MaritalStatus.name],

        })
        # Người giám hộ
        if guardians:
            guardian = guardians[0]
            data_request.update({
                # "S1.A.1.2.41": guardian.CustomerRelationshipType.name,
                "S1.A.1.2.44": guardian.Customer.full_name_vn,
                "S1.A.1.2.42": guardian.Customer.cif_number,
                "S1.A.1.2.51": guardian.CustomerIdentity.identity_num
            })
        # Người đồng sở hữu
        if customer_join:
            customer = customer_join[0]
            data_request.update({
                # "S1.A.1.8": "",
                "S1.A.1.8.3": customer.CustomerJoin.full_name_vn,
                "S1.A.1.8.2": customer.CustomerJoin.cif_number,
                "S1.A.1.8.4": customer.CustomerIdentity.identity_num
            })
        # Thẻ ghi nợ (Thẻ chính - Thẻ phụ)
        if main_cards:
            data_request.update({
                "S1.A.1.10.10": main_cards[0].BrandOfCard.name,
                "S1.A.1.10.3": [main_cards[0].CardIssuanceType.name],
                "S1.A.1.10.16": main_cards[0].CasaAccount.casa_account_number,
                "S1.A.1.10.14": {
                    "value": main_cards[0].Customer.full_name,
                    "type": "embossed_table"

                }
            })

        if sup_cards:
            data_request.update({
                "S1.A.1.10.27.1": sup_cards[0].Customer.full_name_vn,
                "S1.A.1.10.27": sup_cards[0].Customer.cif_number,
                "S1.A.1.10.27.2": sup_cards[0].CustomerIdentity.identity_num,
                "S1.A.1.10.28": {
                    "value": sup_cards[0].Customer.full_name,
                    "type": "embossed_table"
                }
            })
            if sup_cards[0].DebitCard.card_delivery_address_flag:
                data_request.update({"S1.A.1.10.18": ["Địa chỉ liên lạc"]})
            else:
                data_request.update({"S1.A.1.10.18.1": ["SCB"]})
        # E-banking
        if e_banking:
            e_banking = e_banking[0]
            # TODO
            # "S1.A.1.9.14":
            if e_banking.EBankingInfo.account_name:
                data_request.update({"S1.A.1.9.5": [e_banking.EBankingInfo.account_name]})
            if e_banking.EBankingInfo.method_active_password_id:
                data_request.update({"S1.A.1.9.7": [e_banking.EBankingInfo.method_active_password_id]})
            if e_banking.EBankingInfo.account_payment_fee:
                data_request.update({"S1.A.1.9.15": "Tự động ghi nợ TK:"})
                data_request.update({"S1.A.1.9.12": ["Tài khoản thanh toán"]})
                data_request.update({"S1.A.1.9.13": e_banking.EBankingInfo.account_payment_fee})
            else:
                data_request.update({"S1.A.1.9.15.1": "Tiền mặt"})
            # TODO
            # "S1.A.1.2.5"

        # Fatca
        # TODO
        # if fatca_info:
        #     if fatca_info.CustomerFatca.value == "1":
        #         data_request.update({"S1.A.1.5.2": ["Có"]})
        #     if fatca_info.CustomerFatca.value == "0":
        #         data_request.update({"S1.A.1.5.2": ["Không"]})

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            " S1.A.1.11.12": f'{time.year}',

        })
        # data_request.update({
        #     "S1.A.1.11.5": self.current_user.
        # })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.tax_number:
            data_request.update({"S1.A.1.3.6": cust.Customer.tax_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})
        if cust.CustomerProfessional.company_name:
            data_request.update({"S1.A.1.2.10": cust.CustomerProfessional.company_name})
        if cust.CustomerProfessional.company_address:
            data_request.update({"S1.A.1.2.11": cust.CustomerProfessional.company_address})
        if cust.CustomerProfessional.company_phone:
            data_request.update({"S1.A.1.2.12": cust.CustomerProfessional.company_phone})
        if cust.Position:
            data_request.update({"S1.A.1.2.13": cust.Position.name})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_1))
        return self.response(data_tms)

    async def ctr_form_2(self, cif_id: str):
        """
            Biểu mẫu 2
        """
        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]

        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        subs_identity = self.call_repos(await repo_sub_identity(cif_id=cif_id, session=self.oracle_session))
        guardians = self.call_repos(await repo_guardians(cif_id=cif_id, session=self.oracle_session))
        customer_join = self.call_repos(await repo_join_account_holder(cif_id=cif_id, session=self.oracle_session))
        debit_cards = self.call_repos(await repo_debit_card(cif_id=cif_id, session=self.oracle_session))
        e_banking = self.call_repos(await repo_e_banking(cif_id=cif_id, session=self.oracle_session))
        # fatca_info = self.call_repos(await repos_fatca_info(cif_id=cif_id, session=self.oracle_session))

        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None
        if debit_cards:
            for address in customer_address:
                if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                    staying_address = address
                if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                    resident_address = address

        # Tách thẻ chính và thẻ phụ
        main_cards, sup_cards = [], []
        for item in debit_cards:
            if item.DebitCard.parent_card_id:
                sup_cards.append(item)
            else:
                main_cards.append(item)

        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Nam" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.2.23": ["Không cư trú/Non-resident"] if cust.ResidentStatus.name == "Không cư trú" else [
                "Cư trú/Resident"],
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.36": subs_identity[0].name,
            "S1.A.1.2.38": datetime_to_string(subs_identity[0].sub_identity_expired_date,
                                              DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            # TODO: Địa chỉ cư trú tại nước ngoài (chưa có)
            # "S1.A.1.2.30"
            # "S1.A.1.2.31"
            # "S1.A.1.2.32"
            # "S1.A.1.2.33"

            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.6": ["Đồng ý/Agree"] if cust.Customer.advertising_marketing_flag else [
                "Không đồng ý/Do not agree"],

            "S1.A.1.5.4": [cust.Career.name],
            "S1.A.1.5.3": [cust.AverageIncomeAmount.name],
            "S1.A.1.2.9": ["Độc thân/Single"] if cust.MaritalStatus.name == "Độc thân" else ["Đã có gia đình/Married"],

        })
        # Người giám hộ
        if guardians:
            guardian = guardians[0]
            data_request.update({
                # "S1.A.1.2.41":,
                "S1.A.1.2.44": guardian.Customer.full_name_vn,
                "S1.A.1.2.42": guardian.Customer.cif_number,
                "S1.A.1.2.51": guardian.CustomerIdentity.identity_num
            })
        # Người đồng sở hữu
        if customer_join:
            customer = customer_join[0]
            data_request.update({
                # "S1.A.1.8": "",
                "S1.A.1.8.3": customer.CustomerJoin.full_name_vn,
                "S1.A.1.8.2": customer.CustomerJoin.cif_number,
                "S1.A.1.8.4": customer.CustomerIdentity.identity_num
            })
        # Thẻ ghi nợ (Thẻ chính - Thẻ phụ)
        if main_cards:
            data_request.update({
                "S1.A.1.10.10": main_cards[0].BrandOfCard.name,
                "S1.A.1.10.3": ["Thông thường/Regular"] if main_cards[0].CardIssuanceType.name == "THÔNG THƯỜNG" else [
                    "Nhanh/Instant"],
                "S1.A.1.10.16": main_cards[0].CasaAccount.casa_account_number,
                "S1.A.1.10.14": {
                    "value": main_cards[0].Customer.full_name,
                    "type": "embossed_table"

                }
            })

        if sup_cards:
            data_request.update({
                "S1.A.1.10.27.1 ": sup_cards[0].Customer.full_name_vn,
                "S1.A.1.10.27": sup_cards[0].Customer.cif_number,
                "S1.A.1.10.27.2": sup_cards[0].CustomerIdentity.identity_num,
                "S1.A.1.10.28": {
                    "value": sup_cards[0].Customer.full_name,
                    "type": "embossed_table"
                }
            })
            if sup_cards[0].DebitCard.card_delivery_address_flag:
                data_request.update({"S1.A.1.10.18": ["Địa chỉ liên lạc"]})
            else:
                data_request.update({"S1.A.1.10.18.1": ["SCB"]})
        # E-banking
        if e_banking:
            e_banking = e_banking[0]
            # TODO
            # "S1.A.1.9.14":
            if e_banking.EBankingInfo.account_name:
                data_request.update({"S1.A.1.9.5": [e_banking.EBankingInfo.account_name]})
            if e_banking.EBankingInfo.method_active_password_id:
                data_request.update({"S1.A.1.9.7": [e_banking.EBankingInfo.method_active_password_id]})
            if e_banking.EBankingInfo.account_payment_fee:
                data_request.update({"S1.A.1.9.15": "Tự động ghi nợ TK/Auto debit to account:"})
                data_request.update({"S1.A.1.9.12": ["Tài khoản thanh toán/Current account:"]})
                data_request.update({"S1.A.1.9.13": e_banking.EBankingInfo.account_payment_fee})
            else:
                data_request.update({"S1.A.1.9.15.1": "Tiền mặt/Cash"})
            # TODO
            # "S1.A.1.2.5"

        # Fatca
        # TODO
        # if fatca_info:
        #     if fatca_info.CustomerFatca.value == "1":
        #         data_request.update({"S1.A.1.5.2": ["Có"]})
        #     if fatca_info.CustomerFatca.value == "0":
        #         data_request.update({"S1.A.1.5.2": ["Không"]})

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            "S1.A.1.11.12": f'{time.year}',

        })
        # data_request.update({
        #     "S1.A.1.11.5": self.current_user.
        # })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.tax_number:
            data_request.update({"S1.A.1.3.6": cust.Customer.tax_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})
        if cust.CustomerProfessional.company_name:
            data_request.update({"S1.A.1.2.10": cust.CustomerProfessional.company_name})
        if cust.CustomerProfessional.company_address:
            data_request.update({"S1.A.1.2.11": cust.CustomerProfessional.company_address})
        if cust.CustomerProfessional.company_phone:
            data_request.update({"S1.A.1.2.12": cust.CustomerProfessional.company_phone})
        if cust.Position:
            data_request.update({"S1.A.1.2.13": cust.Position.name})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_2))
        return self.response(data_tms)

    async def ctr_form_3(self, cif_id: str):
        """
            Biểu mẫu 3
        """

        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]
        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None

        for address in customer_address:
            if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                staying_address = address
            if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = address
        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Name" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.4": cust.Career.name,

        })

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.16.10": f'{time.day}',
            "S1.A.1.16.11": f'{time.month}',
            "S1.A.1.16.12": f'{time.year}',

        })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_3))
        return self.response(data_tms)

    async def ctr_form_5(self, cif_id: str):
        """
            Biểu mẫu 5
        """

        data_request = {}
        customer_db = self.call_repos(await repo_customer_info(cif_id=cif_id, session=self.oracle_session))
        customer_address = self.call_repos(await repo_customer_address(cif_id=cif_id, session=self.oracle_session))
        cust = customer_db[0]
        # Tách địa chỉ tạm trú và địa chỉ thường trú
        staying_address, resident_address = None, None

        for address in customer_address:
            if address.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                staying_address = address
            if address.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = address
        data_request.update({
            "S1.A.1.1.3": cust.Customer.full_name_vn,
            "S1.A.1.2.4": ["Nam/Male"] if cust.CustomerGender.name == "Nam" else ["Nữ/Female"],
            "S1.A.1.2.8": datetime_to_string(cust.CustomerIndividualInfo.date_of_birth, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.2.6": cust.AddressProvince.name,
            "S1.A.1.2.20": cust.AddressCountry.name,
            "S1.A.1.3.2": cust.CustomerIdentity.identity_num,
            "S1.A.1.3.3": datetime_to_string(cust.CustomerIdentity.issued_date, DATE_INPUT_OUTPUT_EKYC_FORMAT),
            "S1.A.1.3.4": cust.PlaceOfIssue.name,
            "S1.A.1.2.15": staying_address.CustomerAddress.address,
            "S1.A.1.2.16": staying_address.AddressWard.name,
            "S1.A.1.2.17": staying_address.AddressDistrict.name,
            "S1.A.1.2.18": staying_address.AddressProvince.name,
            "S1.A.1.2.19": staying_address.AddressCountry.name,
            "S1.A.1.2.25": resident_address.CustomerAddress.address,
            "S1.A.1.2.26": resident_address.AddressWard.name,
            "S1.A.1.2.27": resident_address.AddressDistrict.name,
            "S1.A.1.2.28": resident_address.AddressProvince.name,
            "S1.A.1.2.29": resident_address.AddressCountry.name,
            "S1.A.1.2.1": cust.Customer.mobile_number,
            "S1.A.1.5.4": cust.Career.name,

        })

        # Cam kết
        time = today()
        data_request.update({
            "S1.A.1.11.10": f'{time.day}',
            "S1.A.1.11.11": f'{time.month}',
            "S1.A.1.11.12": f'{time.year}',

        })

        # Những field option
        if cust.Customer.telephone_number:
            data_request.update({"S1.A.1.2.2": cust.Customer.telephone_number})
        if cust.Customer.email:
            data_request.update({"S1.A.1.2.3": cust.Customer.email})

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=PATH_FORM_5))
        return self.response(data_tms)
