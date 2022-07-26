RETRIEVE_EBANK_CIF_NUMBER_REQUEST = {
    "cif_info": {
        "cif_num": "1348783"
    }
}
RETRIEVE_EBANK_BY_CIF_NUMBER_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": [
                {
                    "ebank_info_item": {
                        "ebank_name": "Internet Banking",
                        "ebank_status": "Da kich hoat"
                    }
                },
                {
                    "ebank_info_item": {
                        "ebank_name": "Mobile Banking",
                        "ebank_status": "Chua dang ky"
                    }
                }
            ]
        }
    }
}

RETRIEVE_INTERNET_BANKING_CIF_NUMBER_REQUEST = {
    "cif_info": {
        "cif_num": "1348783"
    }
}

OPEN_INTERNET_BANKING_REQUEST = {
    "example": {
        "value": {
            "data": {
                "ebank_ibmb_info": {
                    "ebank_ibmb_username": "09091234567778",
                    "ebank_ibmb_mobilephone": "0909123456779"
                },
                "cif_info": {
                    "cif_num": "111111"
                },
                "address_info": {
                    "line": "927 Trần Hưng Đạo",
                    "ward_name": "Phường 1",
                    "district_name": "Quận 5",
                    "city_name": "Hồ Chí Minh",
                    "city_code": "79"
                },
                "customer_info": {
                    "full_name": "HOÀNG THỊ DUNG",
                    "first_name": "DUNG",
                    "middle_name": "THỊ",
                    "last_name": "HOÀNG",
                    "birthday": "1990-05-22",
                    "email": "hoangthidung@gmail.com"
                },
                "authentication_info": [
                    {
                        "authentication_code": "OTP"
                    }
                ],
                "service_package_info": {
                    "service_package_code": "100100"
                },
                "staff_referer": {
                    "staff_code": "15548"
                }
            }
        }

    }
}
