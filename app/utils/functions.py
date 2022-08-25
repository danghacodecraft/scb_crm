import json
import re
import uuid
from datetime import date, datetime, timedelta
from typing import Callable, Dict, Optional, Union
from urllib.parse import urlparse

import orjson

from app.settings.config import (
    DATE_INPUT_OUTPUT_FORMAT, DATETIME_INPUT_OUTPUT_FORMAT
)
from app.utils.constant.utils import UTF_8


def dropdown(data) -> dict:
    return {
        'id': data.id,
        'code': data.code,
        'name': data.name,
    }


def dropdown_name(name: str, code: Optional[str] = None) -> dict:
    return {
        'id': code,
        'code': code,
        'name': name
    }


def optional_dropdown(obj, obj_name: Optional[str] = None, obj_code: Optional[str] = None) -> dict:
    return dropdown(obj) if obj else dropdown_name(name=obj_name, code=obj_code)


# dropdown trả về content
def special_dropdown(data) -> dict:
    return {
        'id': data.id,
        'code': data.code,
        'content': data.content,
        'type': data.type
    }


# dropdown có trả cờ active_flag
def dropdownflag(data) -> dict:
    return {
        'id': data.id,
        'code': data.code,
        'name': data.name,
        'active_flag': data.active_flag
    }


def today():
    """
    get today
    :return: date
    """
    return date.today()


def now():
    return datetime.now()


def datetime_to_string(_time: datetime, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> str:
    if _time:
        return _time.strftime(_format)
    return ''


def string_to_datetime(string: str, default=None, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def date_to_string(_date: date, default='', _format=DATE_INPUT_OUTPUT_FORMAT) -> str:
    if _date:
        return _date.strftime(_format)
    return default


def string_to_date(string: str, default=None, _format=DATE_INPUT_OUTPUT_FORMAT) -> datetime:
    """
    Input: Datetime or date format
    Output: Date
    """
    try:
        st = datetime.strptime(string, _format)
        return st.date()
    except (ValueError, TypeError):
        return default


def date_to_datetime(date_input: date, default=None) -> datetime:
    try:
        return datetime.combine(date_input, datetime.min.time())
    except (ValueError, TypeError):
        return default


def datetime_to_date(datetime_input: datetime, default=None) -> date:
    try:
        return datetime_input.date()
    except (ValueError, TypeError):
        return default


def end_time_of_day(datetime_input: datetime, default=None) -> datetime:
    try:
        return datetime_input.replace(hour=23, minute=59, second=59, microsecond=999999)
    except (ValueError, TypeError):
        return default


def yesterday(date_input: date = today(), default=None):
    try:
        return date_input - timedelta(days=1)
    except (ValueError, TypeError):
        return default


def first_day_in_year(dt: datetime = datetime.now(), default=None) -> date:
    try:
        return dt.date().replace(month=1, day=1)
    except(ValueError, TypeError):
        return default


def last_day_in_year(dt: datetime, default=None) -> date:
    try:
        dt.now().date().replace(month=12, day=31)
    except(ValueError, TypeError):
        return default


def date_string_to_other_date_string_format(
        date_input: str,
        from_format: str,
        to_format: str = DATE_INPUT_OUTPUT_FORMAT,
        default=None
) -> Optional[str]:
    _date = string_to_date(date_input, _format=from_format)
    if not _date:
        return default

    return date_to_string(_date, _format=to_format, default=default)


def generate_uuid() -> str:
    """
    :return: str
    """
    return uuid.uuid4().hex.upper()


def set_id_after_inserted(schema, db_model):
    """
    Cần set uuid từ model vừa insert dưới db SQL lên schema của object tương ứng với đối tượng đó để insert vào mongdb
    :param schema:
    :param db_model:
    :return:
    """
    schema.set_uuid(db_model.uuid)


def travel_dict(d: dict, process_func: Callable):
    process_func(d)
    if isinstance(d, Dict):
        for key, value in d.items():
            if type(value) is dict:
                travel_dict(value, process_func)
            elif isinstance(value, (list, set, tuple,)):
                for item in value:
                    travel_dict(item, process_func)
            else:
                process_func((key, value))
    return d


def process_generate_uuid(d):
    if isinstance(d, dict) and ("uuid" in d) and (d["uuid"] is None):
        d.update({"uuid": generate_uuid()})


# Tính tuổi theo luật VN
def calculate_age(birth_date: date, end_date: date = date.today()) -> int:
    ages = (end_date - birth_date)
    age_number = int((ages.total_seconds()) / (365.242 * 24 * 3600))
    return age_number


def is_valid_mobile_number(mobile_number: str) -> bool:
    regex = r'0([0-9]{9})$'
    found = re.match(regex, mobile_number)
    return True if found else False


def parse_file_uuid(url: str, default='') -> str:
    matches = re.findall(r'/(\w{32})', url)
    return matches[0] if matches else default


def orjson_dumps(data: Union[dict, list]) -> str:
    try:
        json_data = orjson.dumps(data).decode(UTF_8)
    except orjson.JSONDecodeError:
        json_data = ""
    return json_data


def orjson_loads(data: str) -> json:
    try:
        json_data = orjson.loads(data)
    except orjson.JSONDecodeError:
        json_data = {}
    return json_data


def is_valid_number(casa_account_number: str):
    regex = re.search("[0-9]+", casa_account_number)
    if not regex or len(regex.group()) != len(casa_account_number):
        return False
    return True


def convert_string_to_uuidv4(customer_uuid: str) -> str:
    try:
        return f"{uuid.UUID(customer_uuid)}"
    except ValueError:
        return ""


def replace_with_cdn(cdn, file_url: str) -> str:
    if cdn:
        file_url_parse_result = urlparse(file_url)

        # Thay thế link tải file từ service bằng CDN config theo dự án
        return file_url.replace(f'{file_url_parse_result.scheme}://{file_url_parse_result.netloc}', cdn)
    else:
        return file_url


def gen_qr_code(data: dict):
    """
        Data truyền vào là 1 dict gồm nhiều key
    """
    identity = data.get('document_id')
    name = data.get('full_name')
    gender = data.get('gender')
    # gender = "Nam" if gender == "M" else "Nu"
    if gender == "M":
        gender = "Nam"
    elif gender == "F":
        gender = "Nu"

    address = data.get('place_of_residence')

    dob = data.get('date_of_birth').replace("/", "")
    date_of_issue = data.get('date_of_issue').replace("/", "")

    if None in [identity, name, gender, address, dob, date_of_issue]:
        return None

    return identity + "||" + name + "|" + dob + "|" + gender + "|" + address + "|" + date_of_issue


def make_description_from_dict(dictionary: dict):
    return "<br/>" + "<br/>".join(f'`{k}`: {v}' for k, v in dictionary.items())


def make_description_from_dict_to_list(dictionary: dict):
    return "<br/> [" + ", ".join(f'`{v}`' for v in dictionary.keys()) + "]"


def get_index_positions(list_of_elements, element):
    """
    Trả về 1 danh sách index các element nằm trong list
    """
    index_position_list = []
    index_position = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_position = list_of_elements.index(element, index_position)
            # Add the index position in list
            index_position_list.append(index_position)
            index_position += 1
        except ValueError:
            break
    return index_position_list


def calculate_percentage(unit, total):
    try:
        percentage = round(unit / total * 100, 2)
    except ZeroDivisionError:
        return None
    return percentage


def create_fcc_booking_code(
        business_type_sequence: int, branch_code: str, created_at: datetime, booking_code: str):

    date_code = datetime_to_string(created_at, _format='%Y%m%d')
    return f"{business_type_sequence:02d}{branch_code}{date_code}{booking_code[-7:]}"
