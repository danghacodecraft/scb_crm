import re

import Levenshtein as lev  # pip install python-Levenshtein==0.12.2

from app.utils.address_functions import gis


def create_gis():
    def no_accent_vietnamese(s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        s.replace(" ", "")
        return s

    def acronyms(text):
        res = ""
        tokens = text.split(" ")
        first = True
        for token in tokens:
            n = len(token)
            if first and n < 3:
                res = token + " "
            elif token.isnumeric():
                res = res + str(token)
            elif n > 0:
                res = res + token[0]
            first = False
        return res

    gis_db = {
        "datas": {},
        "street": {
            "CHX": "C/X",
            "CHC": "C/C",
        }
    }
    addressInfos = gis.datas["selectProvinceInfo_out"]["addressInfo"]
    for addressInfo in addressInfos:
        provinceName = addressInfo["provinceName"]
        districtName = addressInfo["districtName"]
        wardName = addressInfo["ward"]

        if provinceName not in gis_db["datas"].keys():
            province = {
                "provinceCode": addressInfo["provinceCode"],
                "provinceName": [provinceName, acronyms(provinceName), no_accent_vietnamese(provinceName)],
                "locCodeProvince": addressInfo["locCodeProvince"],
                "datas": {}
            }
            gis_db["datas"][provinceName] = province

        province = gis_db["datas"][provinceName]
        if districtName not in province["datas"].keys():
            district = {
                "districtCode": addressInfo["districtCode"],
                "districtName": [districtName, acronyms(districtName), no_accent_vietnamese(districtName)],
                "datas": {}
            }
            province["datas"][districtName] = district

        district = province["datas"][districtName]
        if wardName not in district["datas"].keys():
            ward = {
                "wardCode": addressInfo["wardCode"],
                "wardName": [wardName, acronyms(wardName), no_accent_vietnamese(wardName)],
                "zipCode": addressInfo["zipCode"]
            }
            district["datas"][wardName] = ward
    return gis_db


gis_db = create_gis()


def matching_place_residence(key):
    def get_list(dic, key):
        lst = []
        for k in dic:
            lst.append(dic[k][key])
        return lst

    def matching(key, datas):
        re = key
        ra = 0
        for places in datas:
            for place in places:
                ratio = lev.ratio(key, place.upper())
                if ratio > ra:
                    re = places[0]
                    ra = ratio
        return re, ra

    def get_match(text, lst, n=-1):
        nn = len(text)
        if n == -1:
            n = nn - text.rfind(" ") - 1

        res_text = text
        res_n = n
        res_r = 0
        count = 0
        while nn > n:
            n = n + 1
            t = text[-n:]

            tt, rat = matching(t, lst)
            if rat >= res_r:
                res_r = rat
                res_text = tt
                res_n = n
                count = 0

            elif res_r < rat:
                count = count + 1

            if rat == 1:
                break

            if count > 2:
                break

            if n > 20:
                break
        return res_text, res_n, res_r

    # data = key.strip()
    # data = replace_address_correct(data)
    data = key.upper()
    data = data.replace("THÀNH PHỐ", "TP")
    data = data.replace("PHƯỜNG", "P")
    data = data.replace("QUẬN", "Q")
    data = data.replace("HUYỆN", "H")
    data = data.replace("TỈNH", "T")
    data = data.replace("THỊ TRẤN", "TT")
    data = data.replace("THỊ XÃ", "TX")
    data = data.replace("XÃ", "X")
    data = data.replace("- ", " ")
    data = data.replace(".", " ")
    data = data.replace(",", " ")
    data = re.sub(' +', ' ', data)

    province_code = ""
    province_name = ""
    district_code = ""
    district_name = ""
    ward_code = ""
    ward_name = ""
    street_name = ""
    address = ""

    nn = len(data)
    if nn > -1:
        lst = get_list(gis_db["datas"], "provinceName")
        res, n, r = get_match(data, lst)
        if r > 0.8 and res in gis_db["datas"]:
            province = gis_db["datas"][res]
            province_name = province["provinceName"][0]
            province_code = province["provinceCode"]
            data = data[0:nn - n].strip()

            # DISTRICT
            nn = len(data)
            if nn > -1:
                lst = get_list(province["datas"], "districtName")
                res, n, r = get_match(data, lst, 1)
                if r > 0.7 and res in province["datas"]:
                    district = province["datas"][res]
                    district_name = district["districtName"][0]
                    district_code = district["districtCode"]
                    data = data[0:nn - n].strip()

                    # WARD
                    nn = len(data)
                    if nn > -1:
                        lst = get_list(district["datas"], "wardName")
                        res, n, r = get_match(data, lst, 1)
                        if r > 0.7 and res in district["datas"]:
                            ward = district["datas"][res]
                            ward_name = ward["wardName"][0]
                            ward_code = ward["wardCode"]

                            street_name = data[0:nn - n].strip()
                            res, n, r = get_match(street_name, gis.streets)
                            if r > 0.95:
                                street_name = street_name[0:len(street_name) - n] + res
                        else:
                            street_name = data.strip()
                else:
                    street_name = data.strip()
        else:
            street_name = data.strip()
    address_list = [street_name, ward_name, district_name, province_name]

    address = ', '.join(add for add in address_list if add)
    address = address.title()

    address_info = {
        "province_code": province_code,
        "province_name": province_name,
        "district_code": district_code,
        "district_name": district_name,
        "ward_code": ward_code,
        "ward_name": ward_name,
        "street_name": street_name
    }
    return address, address_info


def combine_full_address(number_and_street: str = None, ward: str = None, district: str = None, province: str = None):
    if ward or district or province:
        address = f"{number_and_street}, " if number_and_street else ""
    else:
        return number_and_street if number_and_street else ""
    if district or province:
        if ward:
            address = address + f"{ward}, "
        if province:
            if district:
                address = address + f"{district}, "
            address = address + f"{province}"
        else:
            address += district
    else:
        address += ward

    return address
