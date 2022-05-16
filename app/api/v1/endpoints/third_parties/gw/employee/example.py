EMPLOYEE_CODE_EXAMPLE = "employee_code: 13952"
EMPLOYEE_USER_NAME_EXAMPLE = "employee_name: thanhdv3"
ORG_ID_EXAMPLE = "org_id: 12516"
EMPLOYEE_REWARD_CODE_EXAMPLE = "employee_code: 05645"
EMPLOYEE_DISCIPLINE_CODE_EXAMPLE = "employee_code: 08675"
EMPLOYEE_INFO_CODE_EXAMPLE = "employee_code: 03627"
EMPLOYEE_STAFF_OTHER_CODE_EXAMPLE = "employee_code: 03626"

EMPLOYEE_INFO_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "staff_code": "13952",
                "staff_name": "ĐỖ VĂN THẠNH",
                "fullname_vn": "ĐỖ VĂN THẠNH",
                "work_location": "Số 19-21-23-25 Nguyễn Huệ, Phường Bến Nghé, Quận 1, TP.Hồ Chí Minh",
                "email": "thanhdv3@scb.com.vn",
                "contact_mobile": "mb_13952",
                "internal_mobile": "imb_13952",
                "title_code": "040-249",
                "title_name": "Chuyên viên chính Phát triển Ứng dụng nội bộ",
                "branch_org": [
                    {
                        "L1ID": "1",
                        "L1": "Ngân hàng TMCP Sài Gòn",
                        "L2ID": "4",
                        "L2": "Ban Điều hành",
                        "L3ID": "3325",
                        "L3": "Khối Vận hành và Công nghệ",
                        "L4ID": "11374",
                        "L4": "Trung tâm Vận hành và Phát triển Giải pháp",
                        "L5ID": "11820",
                        "L5": "Phòng Phát triển Giải pháp",
                        "L6ID": "13612",
                        "L6": "Mảng Phát triển Hệ thống [Back-end]"
                    }
                ],
                "avatar": "https://192.168.73.151/cdn-profile/13952.jpeg"
            },
            "errors": []
        }
    }
}

EMPLOYEE_LIST_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 2,
                "employee_infos": [
                    {
                        "staff_code": "00969",
                        "staff_name": "PHUONGPTM",
                        "fullname_vn": "PHẠM THỊ MỸ PHƯỢNG",
                        "work_location": "Số 19-21-23-25 Nguyễn Huệ, Phường Bến Nghé, Quận 1, TP.Hồ Chí Minh",
                        "email": "phuongptm@scb.com.vn",
                        "contact_mobile": "mb_00969",
                        "internal_mobile": "imb_00969",
                        "title_code": "028-144",
                        "title_name": "Giám đốc Phân tích Nghiệp vụ",
                        "branch_org": [
                            {
                                "L1ID": "1",
                                "L1": "Ngân hàng TMCP Sài Gòn",
                                "L2ID": "4",
                                "L2": "Ban Điều hành",
                                "L3ID": "3325",
                                "L3": "Khối Vận hành và Công nghệ",
                                "L4ID": "11374",
                                "L4": "Trung tâm Vận hành và Phát triển Giải pháp",
                                "L5ID": "11820",
                                "L5": "Phòng Phát triển Giải pháp",
                                "L6ID": "12516",
                                "L6": "Mảng Phân tích Nghiệp vụ"
                            }
                        ],
                        "avatar": "https://192.168.73.151/cdn-profile/00969.jpeg"
                    },
                    {
                        "staff_code": "04219",
                        "staff_name": "HOANGNGUYENV",
                        "fullname_vn": "NGUYỄN VĂN HOÀNG",
                        "work_location": "Số 19-21-23-25 Nguyễn Huệ, Phường Bến Nghé, Quận 1, TP.Hồ Chí Minh",
                        "email": "hoangnguyenv@scb.com.vn",
                        "contact_mobile": "mb_04219",
                        "internal_mobile": "imb_04219",
                        "title_code": "039-532",
                        "title_name": "Trưởng Bộ phận Phân tích Nghiệp vụ Nội bộ",
                        "branch_org": [
                            {
                                "L1ID": "1",
                                "L1": "Ngân hàng TMCP Sài Gòn",
                                "L2ID": "4",
                                "L2": "Ban Điều hành",
                                "L3ID": "3325",
                                "L3": "Khối Vận hành và Công nghệ",
                                "L4ID": "11374",
                                "L4": "Trung tâm Vận hành và Phát triển Giải pháp",
                                "L5ID": "11820",
                                "L5": "Phòng Phát triển Giải pháp",
                                "L6ID": "12516",
                                "L6": "Mảng Phân tích Nghiệp vụ"
                            }
                        ],
                        "avatar": "https://192.168.73.151/cdn-profile/04219.jpeg"
                    }],
                "errors": []
            }
        }
    }
}

EMPLOYEE_WORKING_PROCESS_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 15,
                "working_process_infos": [
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2021-11-15",
                        "position": "Giám đốc Phòng Quản lý Khai thác, Phân tích Dữ liệu"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2021-11-15",
                        "position": "Giám đốc Quản lý và Khai thác Dữ liệu"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2020-11-09",
                        "position": "Giám đốc Phòng Data Warehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2020-11-09",
                        "position": "Giám đốc Quản lý và Khai thác Dữ liệu"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2019-08-10",
                        "position": "Giám đốc Phòng Data Warehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2019-08-10",
                        "position": "Giám đốc Data Warehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2019-04-08",
                        "position": "Giám đốc Data Warehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2018-08-10",
                        "position": "Giám đốc Data Warehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2017-08-01",
                        "position": "Giám đốc Data Warehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": None,
                        "to_date": "2014-03-07",
                        "position": "Phó Giám đốc Data Warehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Sài Gòn",
                        "from_date": "2014-03-06",
                        "to_date": "2012-01-01",
                        "position": "Trưởng nhóm"
                    },
                    {
                        "company": "Ngân hàng TMCP Đệ Nhất",
                        "from_date": "2011-12-31",
                        "to_date": "2011-09-01",
                        "position": "Trưởng nhóm Phân hệ Báo cáo và Datawarehouse"
                    },
                    {
                        "company": "Ngân hàng TMCP Đệ Nhất",
                        "from_date": "2011-08-31",
                        "to_date": "2010-09-01",
                        "position": "Nhân viên"
                    },
                    {
                        "company": "Công ty TNHH Bảo Hiểm Nhân Thọ Manulife Việt Nam",
                        "from_date": "2010-08-31",
                        "to_date": "2006-11-01",
                        "position": "Nhân viên Tin học"
                    },
                    {
                        "company": "Công ty LPT Co.Ltd",
                        "from_date": "2006-10-30",
                        "to_date": "2006-03-01",
                        "position": "Nhân viên Tin học"
                    }
                ]
            },
            "errors": []
        }
    }
}

EMPLOYEE_REWARD_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 2,
                "reward_infos": [
                    {
                        "effect_date": "2016-04-21",
                        "number": "916/QĐ-TGĐ.16",
                        "title": "DHKT_3",
                        "level": "CKT1",
                        "jobtitle": None,
                        "department": None,
                        "reason": "Khen thưởng cho các cá nhân đạt thành tích xuất sắc năm 2015",
                        "form": "DHKT_3",
                        "of_amount": "4580060",
                        "signing_date": "2016-04-21",
                        "signer": None
                    },
                    {
                        "effect_date": "2018-03-13",
                        "number": "971/QĐ-TGĐ.18",
                        "title": "DHKT_3",
                        "level": "CKT1",
                        "jobtitle": None,
                        "department": None,
                        "reason": "Khen thưởng các Cán bộ nhân viên đạt thành tích xuất sắc năm 2017",
                        "form": "DHKT_3",
                        "of_amount": "5000000",
                        "signing_date": "2018-03-13",
                        "signer": None
                    }
                ]
            },
            "errors": []
        }
    }
}

EMPLOYEE_DISCIPLINE_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 1,
                "reward_infos": [
                    {
                        "effect_date": "2019-11-20",
                        "expire_date": None,
                        "jobtitle": None,
                        "department": None,
                        "reason": "Vi phạm Điểm 9.4.9 Khoản 9.4 Điều 9 “Thực hiện các hành vi giả tạo (không có thật) trong tác nghiệp nhằm mục đích trục lợi cá nhân cho bản thân hoặc cho cá nhân, tổ chức khác”",
                        "description": "Cung cấp HS giải ngân là Thỏa thuận cho vay ngắn hạn cụ thể tại hồ sơ đề nghị giải ngân của KH là Công ty TNHH Giao nhận Vận tải DHB Quốc tế là không xác thực."
                    }
                ]
            },
            "errors": []
        }
    }
}

EMPLOYEE_TOPIC_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 2,
                "topic_infos": [
                    {
                        "code": "KNLV.03",
                        "name": "Kỹ năng quản lý thời gian",
                        "from_date": "2020-12-21",
                        "to_date": "2020-12-21",
                        "result": "Đạt",
                        "description": "Kỹ năng quản lý thời gian"
                    },
                    {
                        "code": "KNBH.04",
                        "name": "Kỹ năng đàm phán và thương lượng",
                        "from_date": "2020-12-21",
                        "to_date": "2020-12-21",
                        "result": "Đạt",
                        "description": "Kỹ năng đàm phán và thương lượng"
                    }
                ]
            }
        }
    }
}

EMPLOYEE_KPIS_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "total_items": 0,
                "kpis_infos": []
            },
            "errors": []
        }
    }
}

EMPLOYEE_STAFF_OTHER_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": {
                "staff_other": {
                    "seniority_month": "6",
                    "annual_number": "12",
                    "recruitment_info": {
                        "code": "TD - 123456",
                        "reason": "Bổ sung nhân sự đầu năm",
                        "presenter": "Trần Thanh Sang",
                        "replace_staff": "3622",
                        "note": "",
                        "other": "Nhân viên lâu năm"
                    }
                }
            },
            "errors": []
        }
    }
}
