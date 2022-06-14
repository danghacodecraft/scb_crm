CUSTOMER_CIF_ID = "0578213"

AUTHORIZED_ACCOUNT_NUMBER = "79555559179"

COOWNER_ACCOUNT_NUMBER = "06079823979"

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
                "fullname_vn": "L2J27NIEXBUCJXWB02CB1WFV3CET04ZH0C9",
                "short_name": "SCB145308",
                "date_of_birth": "1958-03-15",
                "martial_status": {
                    "id": None,
                    "code": None,
                    "name": None
                },
                "gender": {
                    "id": "NAM",
                    "code": "NAM",
                    "name": "Nam"
                },
                "email": None,
                "nationality": {
                    "id": None,
                    "code": None,
                    "name": None
                },
                "mobile_phone": "0903849162",
                "telephone": "0903849162",
                "otherphone": "0903849162-0903849162",
                "customer_type": {
                    "id": None,
                    "code": None,
                    "name": "I"
                },
                "resident_status": {
                    "id": None,
                    "code": None,
                    "name": "R"
                },
                "legal_representativeprsn_name": None,
                "legal_representativeprsn_id": None,
                "biz_contact_person_phone_num": "0903849162",
                "biz_line": "T_0806",
                "biz_license_issue_date": None,
                "is_staff": "N",
                "cif_info": {
                    "customer_id": None,
                    "cif_number": "0011774",
                    "issued_date": None
                },
                "id_info": {
                    "number": "025058000274",
                    "name": "ID CARD/PASSPORT",
                    "issued_date": "2019-04-12",
                    "expired_date": None,
                    "place_of_issue": {
                        "id": None,
                        "code": None,
                        "name": "CTCCS QLHC VTTXH"
                    }
                },
                "resident_address": {
                    "address_full": "OBY3Q2RAI3ZBTOG8ZS9VAPL46HXJD57VFTJ9KU2TFCY0844WPS PHƯỜNG 13 Q TÂN BÌNH TPHCM",
                    "number_and_street": "Y9IZIMVUWY2ABUTT7F4YIF82P8VYT7GO0Y9PRIH8OZQ4UYKXER",
                    "ward": {
                        "id": "27136",
                        "code": "27136",
                        "name": "PHƯỜNG 13"
                    },
                    "district": {
                        "id": "766",
                        "code": "766",
                        "name": "Q TÂN BÌNH"
                    },
                    "province": {
                        "id": "79",
                        "code": "79",
                        "name": "TPHCM"
                    }
                },
                "contact_address": {
                    "address_full": "Y9IZIMVUWY2ABUTT7F4YIF82P8VYT7GO0Y9PRIH8OZQ4UYKXER PHƯỜNG 13 Q TÂN BÌNH TPHCM",
                    "number_and_street": "Y9IZIMVUWY2ABUTT7F4YIF82P8VYT7GO0Y9PRIH8OZQ4UYKXER",
                    "ward": {
                        "id": "27136",
                        "code": "27136",
                        "name": "PHƯỜNG 13"
                    },
                    "district": {
                        "id": "766",
                        "code": "766",
                        "name": "Q TÂN BÌNH"
                    },
                    "province": {
                        "id": "79",
                        "code": "79",
                        "name": "TPHCM"
                    }
                },
                "job_info": {
                    "id": "TU_DO",
                    "code": "TU_DO",
                    "name": "TỰ DO"
                },
                "branch_info": {
                    "id": None,
                    "code": None,
                    "name": "CN TAN BINH"
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
                        "fullname_vn": "Vũ  Lưu Chuyền",
                        "date_of_birth": "1977-11-01",
                        "martial_status": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "gender": {
                            "id": "NAM",
                            "code": "NAM",
                            "name": "Nam"
                        },
                        "email": None,
                        "nationality": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "mobile_phone": "0937721727",
                        "telephone": "0937721727",
                        "otherphone": "0937721727-0937721727",
                        "customer_type": {
                            "id": None,
                            "code": None,
                            "name": "I"
                        },
                        "cif_info": {
                            "customer_id": "831cd5f3dc7b48aa8d01a11562a2bf4b",
                            "cif_number": "0035596",
                            "issued_date": "2011-04-27"
                        },
                        "id_info": {
                            "number": "077077000007",
                            "name": "ID CARD/PASSPORT",
                            "issued_date": "2016-03-01",
                            "expired_date": None,
                            "place_of_issue": {
                                "id": None,
                                "code": None,
                                "name": "CUC CS DKQL CU TRU VA DLQG VE DC"
                            }
                        },
                        "branch_info": {
                            "id": "001",
                            "code": "001",
                            "name": "CN Cống Quỳnh"
                        },
                        "address_info": {
                            "address_full": "7WPYVZ75EGG0CC10VAMM872IG1CET887871OTK5S596J0W5636 THANH,TP.HCM  "
                        }
                    }
                ]
            },
            "errors": []
        }
    }
}

CUSTOMER_COOWNER_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 1,
                "coowner_info_list": [
                    {
                        "full_name_vn": "4AFS633ISCPGGKPDI77MZKN77N235AOVI3K",
                        "date_of_birth": "1960-04-22 00:00:00",
                        "gender": "F",
                        "email": "",
                        "nationality_code": "",
                        "mobile_phone": "0369577553",
                        "customer_type": "I",
                        "coowner_relationship": "PRIMARY",
                        "cif_info": {
                            "cif_number": "",
                            "issued_date": "2008-06-04 00:00:00"
                        },
                        "id_info": {
                            "number": "079160005359",
                            "name": "ID CARD/PASSPORT",
                            "issued_date": "2018-02-22 00:00:00",
                            "expired_date": "2020-04-22 00:00:00",
                            "place_of_issue": "CUC CSDKQL CU TRU VA DLQG VE DAN CU"
                        },
                        "address_info": {
                            "contact_address_full": "OGNND2CON76SGDOHHGA6CWPQ6TG24IZ2OKH5KV2FIHSMVTP3DN PHUONG 7 QUAN 8",
                            "address_full": ""
                        }
                    }
                ]
            },
            "errors": []
        }
    }
}

CUSTOMER_AUTHORIZER_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 1,
                "authorized_info_list": [
                    {
                        "full_name_vn": "PQNTKYJ2GTKRIJOASL4S7U940SV4CB4DYZP",
                        "date_of_birth": "1969-09-07 00:00:00",
                        "gender": "M",
                        "email": "",
                        "nationality_code": "",
                        "mobile_phone": "0983010209",
                        "customer_type": "I",
                        "coowner_relationship": "PRIMARY",
                        "cif_info": {
                            "cif_number": "",
                            "issued_date": "2018-06-05 00:00:00"
                        },
                        "id_info": {
                            "number": "079069000974",
                            "name": "ID CARD/PASSPORT",
                            "issued_date": "2016-03-17 00:00:00",
                            "expired_date": "",
                            "place_of_issue": "CCS DKQL CT VA DLQG VE DC"
                        },
                        "address_info": {
                            "contact_address_full": "XCTGJPPKMB85OXJ5PB98B04RTNEXW5Y77LFK50LEYLTAGZG02T  Q. GÒ VẤP, HỒ CHÍ MINH",
                            "address_full": ""
                        }
                    }
                ]
            },
            "errors": []
        }
    }
}
