ORGANIZATION_INFO_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": [
                {
                    "id": "1",
                    "parent_id": "",
                    "name": "Ngân hàng TMCP Sài Gòn",
                    "short_name": "",
                    "path": "1;",
                    "path_description": "Ngân hàng TMCP Sài Gòn;",
                    "order_by": "1",
                    "childs": [
                        {
                            "id": "2",
                            "parent_id": "1",
                            "name": "Ban Kiểm soát",
                            "short_name": "BKS",
                            "path": "1;2;",
                            "path_description": "Ngân hàng TMCP Sài Gòn;Ban Kiểm soát;",
                            "order_by": "1",
                            "childs": [
                                {
                                    "id": "116",
                                    "parent_id": "2",
                                    "name": "Ban Kiểm soát",
                                    "short_name": "BKS",
                                    "path": "1;2;116;",
                                    "path_description": "Ngân hàng TMCP Sài Gòn;Ban Kiểm soát;Ban Kiểm soát;",
                                    "order_by": "1",
                                    "childs": []
                                },
                                {
                                    "id": "117",
                                    "parent_id": "2",
                                    "name": "Kiểm toán Nội bộ",
                                    "short_name": "KTNB",
                                    "path": "1;2;117;",
                                    "path_description": "Ngân hàng TMCP Sài Gòn;Ban Kiểm soát;Kiểm toán Nội bộ;",
                                    "order_by": "2",
                                    "childs": []
                                },
                                {
                                    "id": "11384",
                                    "parent_id": "2",
                                    "name": "Bộ phận hỗ trợ Ban Kiểm soát",
                                    "short_name": "BP.HTBKS",
                                    "path": "1;2;11384;",
                                    "path_description": "Ngân hàng TMCP Sài Gòn;Ban Kiểm soát;Bộ phận hỗ trợ Ban Kiểm soát;",
                                    "order_by": "3",
                                    "childs": []
                                }
                            ]
                        }
                    ]
                }
            ],
            "errors": []
        }
    }
}

ORGANIZATION_INFO_FROM_PARENT_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": [
                {
                    "id": "126",
                    "parent_id": "4",
                    "name": "Ban Điều hành/Giám đốc",
                    "short_name": "",
                    "path": "1;4;126;",
                    "path_description": "Ngân hàng TMCP Sài Gòn;Ban Điều hành;Ban Điều hành/Giám đốc;",
                    "order_by": "1"
                },
                {
                    "id": "128",
                    "parent_id": "4",
                    "name": "Các Hội đồng/Ban thuộc TGĐ",
                    "short_name": "",
                    "path": "1;4;128;",
                    "path_description": "Ngân hàng TMCP Sài Gòn;Ban Điều hành;Các Hội đồng/Ban thuộc TGĐ;",
                    "order_by": "2"
                }
            ],
            "errors": []
        }
    }
}

ORGANIZATION_INFO_FROM_CHILD_SUCCESS_EXAMPLE = {
    "example": {
        "value": {
            "data": [
                {
                    "id": "126",
                    "parent_id": "4",
                    "name": "Ban Điều hành/Giám đốc",
                    "short_name": "",
                    "path": "1;4;126;",
                    "path_description": "Ngân hàng TMCP Sài Gòn;Ban Điều hành;Ban Điều hành/Giám đốc;",
                    "order_by": "1"
                },
                {
                    "id": "128",
                    "parent_id": "4",
                    "name": "Các Hội đồng/Ban thuộc TGĐ",
                    "short_name": "",
                    "path": "1;4;128;",
                    "path_description": "Ngân hàng TMCP Sài Gòn;Ban Điều hành;Các Hội đồng/Ban thuộc TGĐ;",
                    "order_by": "2"
                }
            ],
            "errors": []
        }
    }
}
