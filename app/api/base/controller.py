from typing import List, Optional, Union

from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from app.api.base.except_custom import ExceptionHandle
from app.api.base.repository import ReposReturn
from app.api.base.schema import Error
from app.api.base.validator import ValidatorReturn
from app.api.v1.endpoints.approval.common_repository import (
    repos_get_begin_stage, repos_get_next_receiver
)
from app.api.v1.endpoints.file.repository import (
    repos_check_is_exist_multi_file, repos_download_multi_file
)
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name,
    repos_get_model_object_by_id_or_code, repos_get_model_objects_by_ids
)
from app.api.v1.endpoints.user.schema import AuthResponse, UserInfoResponse
from app.third_parties.oracle.base import Base, SessionLocal, SessionLocal_Task
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.ekyc import is_success
from app.utils.error_messages import (
    ERROR_GROUP_ROLE_CODE, ERROR_MENU_CODE, MESSAGE_STATUS
)
from app.utils.functions import (
    datetime_to_string, dropdown, dropdown_name, generate_uuid, now,
    orjson_dumps
)


class BaseController:
    """
    BaseController use business
    """

    def __init__(self, current_user=None, pagination_params=None, is_init_oracle_session=True):
        self.current_user = current_user
        self.pagination_params = pagination_params
        self.errors = []

        self.oracle_session: Optional[Session] = None
        if is_init_oracle_session:
            logger.debug("Started session Oracle")
            self.oracle_session = SessionLocal()

        self.oracle_session_task: Optional[Session] = None
        if is_init_oracle_session:
            logger.debug("Started session Oracle")
            self.oracle_session_task = SessionLocal_Task()

    def _close_oracle_session(self):
        if self.oracle_session:
            self.oracle_session.close()
            logger.debug("Closed Oracle session")

    def call_validator(self, result_call_validator: ValidatorReturn):
        if result_call_validator.is_error:
            self.response_exception(
                msg=result_call_validator.msg,
                loc=result_call_validator.loc,
                detail=result_call_validator.detail
            )

        return result_call_validator.data

    def call_repos(self, result_call_repos: ReposReturn):
        if result_call_repos.is_error:
            self.response_exception(
                msg=result_call_repos.msg,
                loc=result_call_repos.loc,
                detail=result_call_repos.detail,
                error_status_code=result_call_repos.error_status_code
            )

        return result_call_repos.data

    async def get_model_object_by_id(self, model_id: str, model: Base, loc: str):
        return self.call_repos(
            await repos_get_model_object_by_id_or_code(
                model_id=model_id,
                model_code=None,
                model=model,
                loc=loc,
                session=self.oracle_session
            )
        )

    async def get_model_objects_by_ids(self, model_ids: List[str], model: Base, loc: str):
        return self.call_repos(
            await repos_get_model_objects_by_ids(
                model_ids=model_ids,
                model=model,
                loc=loc,
                session=self.oracle_session
            )
        )

    async def get_model_object_by_code(self, model_code: str, model: Base, loc: str):
        return self.call_repos(
            await repos_get_model_object_by_id_or_code(
                model_id=None,
                model_code=model_code,
                model=model,
                loc=loc,
                session=self.oracle_session
            )
        )

    async def check_exist_multi_file(self, uuids: List[str]):
        """
        Hàm kiểm tra các file có tồn tại trên service file hay không
        :param uuids:
        :return:
        """
        if len(uuids) != len(set(uuids)):
            self.response_exception(
                msg='',
                loc='file_url',
                detail='File uuid is duplicated'
            )

        if any([True if not uuid else False for uuid in uuids]):
            self.response_exception(
                msg='',
                loc='file_url',
                detail='File uuid is not valid'
            )

        is_exist = self.call_repos(await repos_check_is_exist_multi_file(uuids=uuids))
        if not is_exist:
            self.response_exception(
                msg='',
                loc='file_url',
                detail='Can not found file in service file'
            )

    async def get_link_download_multi_file(self, uuids: List[str]) -> dict:
        """
        Hàm get link download file từ service file
        :param uuids:
        :return: dict, key là uuid, value là link download file đó
        """

        # FIXME: service file không cho download các uuid trùng nhau, dữ liệu đang test nên có thể trùng uuid
        uuids = list(set(uuids))

        if not uuids:
            return {}

        return {
            info['uuid']: info['file_url']
            for info in self.call_repos(await repos_download_multi_file(uuids=uuids))
        }

    def append_error(self, msg: str, loc: str = "", detail: str = ""):
        """
        Hàm add exception để trả về
        :param msg: code exception
        :param loc: fields cần thông báo
        :param detail: Thông tin thông báo
        :return:
        """
        self.errors.append(Error(msg=msg, detail=detail, loc=loc))

    def _raise_exception(self, error_status_code=status.HTTP_400_BAD_REQUEST):
        errors = []
        for temp in self.errors:
            errors.append(temp.dict())
        raise ExceptionHandle(errors=errors, status_code=error_status_code)

    def response_exception(self, msg, loc="", detail="", params="", error_status_code=status.HTTP_400_BAD_REQUEST):
        self._close_oracle_session()

        self.append_error(msg=msg, loc=loc, detail=detail, params=params)
        self._raise_exception(error_status_code=error_status_code)

    def response(self, data, error_status_code=status.HTTP_400_BAD_REQUEST):
        self._close_oracle_session()

        if self.errors:
            self._raise_exception(error_status_code=error_status_code)
        else:
            return {
                "data": data,
                "errors": self.errors,
            }

    def response_paging(
            self,
            data,
            total_items: int = 1,
            current_page: int = 1,
            total_page: int = 1,
            error_status_code=status.HTTP_400_BAD_REQUEST
    ):
        self._close_oracle_session()

        if self.errors:
            self._raise_exception(error_status_code=error_status_code)
        else:
            return {
                "data": data,
                "total_items": total_items,
                "total_page": total_page,
                "current_page": current_page,
                "errors": self.errors,
            }

    def nested_list(
            self,
            objects: Union[dict, list],
            map_with_key: str,
            children_fields: dict,
            children_list: list = None,
            key_child_map_parent=None
    ):
        """
        thay kiểu dũ liệu trong childfields sẽ ra data như mong muốn
        - children_fields={"detail": {'t1', 't2'}}: data child la dict
        - children_fields={"detail": ['t1', 't2']}: data child la list
        - Có thể nest con vào cha theo trường hợp trên:
            + tách key mapping
        re = ctr.nested_list(objects=data, map_with_key='the_luong_id', children_fields={"detail": ['t1', 't2']})

        re = ctr.nested_list(
            objects=re, map_with_key='id', children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']}
        )

        re = ctr.nested_list(
            objects=NEST_PARENT_FD,
            map_with_key='id',
            children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']},
            children_list=NEST_CHILDREN_FD
        )
        """
        objects_cp = objects.copy()

        if isinstance(objects, dict):
            object_list = [objects_cp]
        else:
            object_list = objects_cp

        if not isinstance(children_fields, dict):
            raise Exception('fields type is dict')

        if len(children_fields) < 1:
            return objects_cp

        if not objects_cp:
            return objects_cp

        for key in children_fields:
            assert isinstance(children_fields[key], (list, set)), 'children is type list'
            assert len(children_fields[key]) > 0, 'children is not null'
            # assert children_fields[key][0][-2:] == "id", "First field of child  must be primary key ID"

        if children_list:
            data_result = self._nest_child_to_parent(
                parent_list=object_list,
                map_with_key=map_with_key,
                children_fields=children_fields,
                children_list=children_list,
                key_child_map_parent=key_child_map_parent
            )
        else:
            data_result = self._nest_me(
                objects=object_list,
                map_with_key=map_with_key,
                fields=children_fields
            )
        if isinstance(objects, dict):
            return data_result[0] if data_result else {}
        else:
            return data_result

    def _nest_me(
            self,
            objects: list,
            map_with_key: str,
            fields: dict
    ):

        all_key_child = []
        for key_child, value_child in fields.items():
            all_key_child += list(value_child)

        nest_level_data = list(
            map(
                lambda x: self._nest_level(data_item=x, all_key_child=all_key_child, fields=fields),
                objects
            )
        )

        key_in_parent = set()
        data_parent = dict()

        for temp in list(nest_level_data):
            if temp[map_with_key] not in key_in_parent:
                key_in_parent.add(temp[map_with_key])
                data_parent.update({
                    temp[map_with_key]: temp
                })
            else:
                for key_field, value_field in fields.items():
                    if not temp[key_field]:
                        continue

                    if isinstance(value_field, list):
                        if temp[key_field][0] not in data_parent[temp[map_with_key]][key_field]:
                            data_parent[temp[map_with_key]][key_field].append(temp[key_field][0])
        return list(data_parent.values())

    def _nest_child_to_parent(
            self, parent_list, map_with_key: str, children_fields: dict,
            children_list: list = None, key_child_map_parent=None
    ):

        all_key_child = []
        for key_child, value_child in children_fields.items():
            all_key_child += list(value_child)

        nest_level_data = list(
            map(
                lambda x: self._nest_level(data_item=x, all_key_child=all_key_child, fields=children_fields),
                children_list
            )
        )

        for parent in parent_list:
            for child in nest_level_data:
                if key_child_map_parent:
                    if parent[map_with_key] == child[key_child_map_parent]:
                        self._nest_type(parent=parent, child=child, children_fields=children_fields)
                else:
                    if parent[map_with_key] == child[map_with_key]:
                        self._nest_type(parent=parent, child=child, children_fields=children_fields)
        return parent_list

    @staticmethod
    def _nest_type(parent, child, children_fields):
        for key_field, value_field in children_fields.items():
            if not child[key_field]:
                continue
            if isinstance(value_field, list):
                if key_field not in parent:
                    parent.update({
                        key_field: [child[key_field][0]]
                    })
                elif child[key_field][0] not in parent[key_field]:
                    parent[key_field].append(child[key_field][0])
            else:
                parent.update({
                    key_field: child[key_field][0]
                })

    @staticmethod
    def _nest_level(data_item: dict, all_key_child: list, fields: dict):
        child_temp = {}
        parent_temp = {}
        for key_temp, value_temp in data_item.items():
            if key_temp in all_key_child:
                for key_field, value_field in fields.items():
                    if key_temp in value_field:
                        if key_field not in child_temp:
                            child_temp.update({
                                key_field: {}
                            })
                        child_temp[key_field].update({
                            key_temp: value_temp
                        })
            else:
                parent_temp.update({
                    key_temp: value_temp
                })

        for key_field, value_field in fields.items():
            if isinstance(value_field, list):
                parent_temp.update({
                    key_field: [child_temp[key_field]]
                })
            else:
                parent_temp.update({
                    key_field: child_temp[key_field]
                })

        return parent_temp

    async def ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            self,
            business_type_id: str
    ):
        """
        Tạo data TransactionDaily và các TransactionStage khác cho bước mở CIF khi tạo giấy tờ định danh
        """
        current_user = self.current_user.user_info

        saving_transaction_stage_status_id = generate_uuid()
        saving_transaction_stage_id = generate_uuid()
        transaction_daily_id = generate_uuid()

        begin_stage_status, begin_stage = self.call_repos(
            await repos_get_begin_stage(
                business_type_id=business_type_id,
                session=self.oracle_session
            ))

        saving_transaction_stage_status = dict(
            id=saving_transaction_stage_status_id,
            code=begin_stage_status.code,
            name=begin_stage_status.name
        )

        saving_transaction_stage = dict(
            id=saving_transaction_stage_id,
            status_id=saving_transaction_stage_status_id,
            lane_id=None,
            phase_id=None,
            business_type_id=business_type_id,
            sla_transaction_id=None,  # TODO
            transaction_stage_phase_code=begin_stage.code,
            transaction_stage_phase_name=begin_stage.name,
            action_id=None,
            is_reject=False
        )

        saving_transaction_daily = dict(
            transaction_id=transaction_daily_id,
            transaction_stage_id=saving_transaction_stage_id,
            transaction_parent_id=None,
            transaction_root_id=transaction_daily_id,
            is_reject=False,
            data=orjson_dumps(dict(
                content="Giao dịch viên đang chuẩn bị hồ sơ. "
                        "Mốc thời gian tính từ lúc GDV điền thông tin tab đầu tiên [Thông tin cá nhân]"
            )),
            description="Khởi tạo CIF",
            created_at=now()
        )

        # sender_branch = await self.get_model_object_by_id(
        #     model_id=current_user.branch_id,
        #     model=Branch,
        #     loc="stage_lane"
        # )

        # sender_department = await self.get_model_object_by_id(
        #     model_id=stage_lane.department_id,
        #     model=Department,
        #     loc="stage_lane"
        # )

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
            position_name=current_user.hrm_position_name,
            title_id=current_user.hrm_title_id,
            title_code=current_user.hrm_title_code,
            title_name=current_user.hrm_title_name
        )

        receiver = self.call_repos(await repos_get_next_receiver(
            business_type_id=business_type_id,
            current_stage_id=begin_stage.id,
            reject_flag=False,
            session=self.oracle_session
        ))

        receiver_branch = await self.get_model_object_by_id(
            model_id=receiver.branch_id,
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
            branch_id=receiver_branch.id,
            branch_code=receiver_branch.code,
            branch_name=receiver_branch.name,
            department_id=receiver.department_id,
            department_code=current_user.hrm_department_code,
            department_name=current_user.hrm_department_name,
            position_id=current_user.hrm_position_id,
            position_code=current_user.hrm_position_code,
            position_name=current_user.hrm_position_name
        )

        return (saving_transaction_stage_status, saving_transaction_stage, saving_transaction_daily,
                saving_transaction_sender, saving_transaction_receiver)

    @staticmethod
    def check_permission(current_user: AuthResponse, menu_code: str, group_role_code: str):
        permissions = []
        list_role_code = []
        for item in current_user.menu_list:
            if item.menu_name == menu_code:
                permissions.extend(item.group_role_list)

        if not permissions:
            return False, {'msg': MESSAGE_STATUS[ERROR_MENU_CODE]}

        for permission in permissions:
            # kiểm tra group_role_code có tồn tại không, kiểm tra permision có được kích hoạt
            if permission.group_role_code == group_role_code and not permission.is_permission:
                return False, {"msg": MESSAGE_STATUS[ERROR_GROUP_ROLE_CODE]}
            list_role_code.append(permission.group_role_code)
        # check group_role_code k tồn tại
        if group_role_code not in list_role_code:
            return False, {'msg': MESSAGE_STATUS[ERROR_GROUP_ROLE_CODE]}

        return True, {"msg": is_success}

    async def dropdown_mapping_crm_model_or_dropdown_name(
            self, model: Base, name: Optional[str], code: Optional[str] = None) -> dict:
        """
        Input: code hoặc name
        Output: dropdown object
        """
        obj_mapping_crm = await get_optional_model_object_by_code_or_name(
            model=model,
            model_code=code,
            model_name=name,
            session=self.oracle_session
        )

        return dropdown(obj_mapping_crm) if obj_mapping_crm else dropdown_name(name=name)

    @staticmethod
    def make_history_log_data(description: str, history_status: int, current_user: UserInfoResponse):
        history_log_data = [dict(
            description=description,
            completed_at=datetime_to_string(now()),
            created_at=datetime_to_string(now()),
            status=history_status,
            branch_id=current_user.hrm_branch_id,
            branch_code=current_user.hrm_branch_code,
            branch_name=current_user.hrm_branch_name,
            user_id=current_user.code,
            user_name=current_user.name,
            user_username=current_user.username,
            user_avatar=current_user.avatar_url,
            user_email=current_user.email,
            position_id=current_user.hrm_position_id,
            position_code=current_user.hrm_position_code,
            position_name=current_user.hrm_position_name,
            department_id=current_user.hrm_department_id,
            department_code=current_user.hrm_department_code,
            department_name=current_user.hrm_department_name,
            title_id=current_user.hrm_title_id,
            title_code=current_user.hrm_title_code,
            title_name=current_user.hrm_title_name
        )]
        return history_log_data
