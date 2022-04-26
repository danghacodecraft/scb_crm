CUSTOMER_CIF_ID = {"cif_number": "0578213"}

CUSTOMER_CHECK_EXIST_CIF_ID_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "is_existed": True
            },
            "errors": []
        }
    }
}

CUSTOMER_CHECK_EXIST_CIF_ID_FAIL_EXAMPLE = {
    "example": {
        "value": {
            "data": None,
            "errors": [
                {
                    "loc": "body -> cif_number",
                    "msg": "VALIDATE_ERROR",
                    "detail": "ensure this value has at most 7 characters"
                }
            ]
        }
    }
}

CUSTOMER_INFO_DETAIL_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "fullname_vn": "E5MCD9OL1RC9OU7AHTH4FBOQF0EZ6R4EH11",
                "short_name": "VY_0578213",
                "date_of_birth": "1990-01-03 00:00:00",
                "martial_status": "",
                "gender": "F",
                "email": "thinh@minerva.vn",
                "nationality_code": "",
                "mobile_phone": "0389937908",
                "telephone": "01689937908",
                "otherphone": "01689937908-0389937908",
                "customer_type": "I",
                "resident_status": "R",
                "legal_representativeprsn_name": "",
                "legal_representativeprsn_id": "",
                "biz_contact_person_phone_num": "0389937908",
                "biz_line": "T_0806",
                "biz_license_issue_date": "",
                "is_staff": "Y",
                "cif_info": {
                    "cif_number": "",
                    "issued_date": ""
                },
                "id_info": {
                    "number": "024316156",
                    "name": "ID CARD/PASSPORT",
                    "issued_date": "2015-03-12 00:00:00",
                    "expired_date": "",
                    "place_of_issue": "TPHCM"
                },
                "address_info": {
                    "address_full": "8OKE3AGY50WBKCSFZD5DI3XBAO0IVFKNBIV5XTB2JH8Z1J916T PHƯỜNG 13 QUẬN 6 TPHCM",
                    "contact_address_full": "JVLPCN0ZSGINJ0422OH90NGTQT0CEP9P1QSUAGZD90850RJC1B PHƯỜNG 13 QUẬN 6 TPHCM"
                },
                "job_info": {
                    "name": "TỰ DO",
                    "code": "TU_DO"
                },
                "branch_info": {
                    "code": "204",
                    "name": "CN  Binh Tay"
                }
            },
            "errors": []
        }
    }
}

CUSTOMER_INFO_LIST_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 1,
                "customer_info_list": [
                    {
                        "fullname_vn": "NGUYỄN THỊ ÁI VY",
                        "date_of_birth": "1990-01-03 00:00:00",
                        "martial_status": "",
                        "gender": "F",
                        "email": "thinh@minerva.vn",
                        "nationality_code": "",
                        "mobile_phone": "0389937908",
                        "telephone": "01689937908",
                        "otherphone": "01689937908-0389937908",
                        "customer_type": "I",
                        "cif_info": {
                            "cif_number": "0578213",
                            "issued_date": "2014-04-15 00:00:00"
                        },
                        "id_info": {
                            "number": "024316156",
                            "name": "ID CARD/PASSPORT",
                            "issued_date": "2015-03-12 00:00:00",
                            "expired_date": "",
                            "place_of_issue": "TPHCM"
                        },
                        "branch_info": {
                            "code": "204",
                            "name": "CN Bình Tây"
                        },
                        "address_info": {
                            "address_full": "JVLPCN0ZSGINJ0422OH90NGTQT0CEP9P1QSUAGZD90850RJC1B PHƯỜNG 13 QUẬN 6 TPHCM"
                        }
                    }
                ]
            },
            "errors": []
        }
    }
}
