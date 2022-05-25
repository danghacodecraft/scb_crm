p_spc1 = "Có kỳ hạn"
p_spc2 = "Tiết kiệm CKH"
p_spc3 = "Thông thường"
p_spc31 = "Lãi cuối kỳ"
ccy_code = "VND"
ccy_code2 = "USD"
branch_code = "000"
account_class = "CAI025"
p_customer_no = "0561561"
p_cus_ac_no = "05615610003"
p_module = "TIEN_GUI"
p_tk_vay = "001CLZ1122650007"
p_user_id = "TRUNGNTN"
p_sotaikhoan = "00663000004"
p_tu_ngay = "5/4/2019"
p_den_ngay = "5/10/2020"
p_account_class = "CAI025"
p_type = "D"

GW_CATEGORIES = [
    {
        "category_name": "Danh mục sản phẩm cấp 1",
        "transaction_name": "DM_SP01",
        "transaction_value": []
    },
    {
        "category_name": "Danh mục sản phẩm cấp 2",
        "transaction_name": "DM_SP02",
        "transaction_value": [{"param1": p_spc1}]
    },
    {
        "category_name": "Danh mục sản phẩm cấp 3",
        "transaction_name": "DM_SP03",
        "transaction_value": [{"param1": p_spc1, "param2": p_spc2}]
    },
    {
        "category_name": "Danh mục sản phẩm cấp 4",
        "transaction_name": "DM_SP04",
        "transaction_value": [{"param1": p_spc1, "param2": p_spc2, "param3": p_spc3, "param4": p_spc31}]
    },
    {
        "category_name": "Danh mục sản phẩm cấp 4 lãi suất cuối kỳ",
        "transaction_name": "DM_SP04_LS",
        "transaction_value": [
            {"param1": p_spc1, "param2": p_spc2, "param3": p_spc3, "param4": p_spc31, "param5": ccy_code}]
    },
    {
        "category_name": "Lấy lãi suất theo sản phẩm và loại tiền gửi TD",
        "transaction_name": "DM_SP_LS",
        "transaction_value": [{"param1": branch_code, "param2": account_class, "param3": ccy_code}]
    },
    {
        "category_name": "Danh mục tài khoản treo của đơn vị",
        "transaction_name": "DM_TK_TD_TREO",
        "transaction_value": [{"param1": p_customer_no, "param2": ccy_code}]
    },
    {
        "category_name": "Lấy số tiền gốc và lãi tất toán đúng hạn của tài khoản TD",
        "transaction_name": "DM_TK_TD_TT",
        "transaction_value": [{"param1": p_cus_ac_no}]
    },
    {
        "category_name": "Lấy danh mục giao dịch viên của đơn vị",
        "transaction_name": "DM_GDV_DONVI",
        "transaction_value": [{"param1": branch_code, "param2": p_module}]
    },
    {
        "category_name": "Lấy số tiền gốc và lãi tất toán đúng hạn của tài khoản TD",
        "transaction_name": "DM_RTH_TK",
        "transaction_value": [{"param1": p_cus_ac_no}]
    },
    {
        "category_name": "Lấy loại hình tài khoản DD",
        "transaction_name": "DM_TK_DD",
        "transaction_value": []
    },
    {
        "category_name": "Lấy danh sách nhân viên kinh doanh của đơn vị	",
        "transaction_name": "DM_NVKD_DONVI",
        "transaction_value": [{"param1": branch_code}]
    },
    {
        "category_name": "Danh mục tài khoản thanh toán",
        "transaction_name": "DM_TK_TT_CIF",
        "transaction_value": [{"param1": p_customer_no, "param2": ccy_code}]
    },
    {
        "category_name": "Thông tin lãi trả nợ vay",
        "transaction_name": "DM_TRANO_VAY",
        "transaction_value": [{"param1": p_tk_vay}]
    },
    {
        "category_name": "Thông tin tài sản vay",
        "transaction_name": "DM_TSAN_VAY",
        "transaction_value": [{"param1": p_tk_vay}]
    },
    {
        "category_name": "Thông tin trạng thái tài khoản",
        "transaction_name": "DM_TRANGTHAI_TK",
        "transaction_value": [{"param1": p_customer_no}]
    },
    {
        "category_name": "Tính lãi số tài khoản	",
        "transaction_name": "DM_TINHLAI_STK",
        "transaction_value": [{"param1": p_user_id, "param2": p_sotaikhoan, "param3": p_tu_ngay, "param4": p_den_ngay}]
    },
    {
        "category_name": "Master account",
        "transaction_name": "DM_GET_MASTER_ACC",
        "transaction_value": [{"param1": p_cus_ac_no}]
    },
    {
        "category_name": "Danh mục tài khoản thanh toán của khách hàng",
        "transaction_name": "DM_GET_RATE_TRANFS",
        "transaction_value": [{"param1": ccy_code, "param2": ccy_code2}]
    },
    {
        "category_name": "Danh mục promo code",
        "transaction_name": "DM_GET_PROMO_CODE",
        "transaction_value": [{"param1": p_customer_no, "param2": p_account_class, "param3": ccy_code}]
    },
    {
        "category_name": "Lãi suất cộng thêm",
        "transaction_name": "DM_GET_RATE_OTHER",
        "transaction_value": [{"param1": p_account_class, "param2": ccy_code}]
    },
    {
        "category_name": "Lấy danh sách nhân viên kinh doanh của đơn vị	",
        "transaction_name": "DS_NV_DIRECT_INDIRECT",
        "transaction_value": [{"param1": p_type, "param2": branch_code}]
    },
    {
        "category_name": "Lấy thu nhập bình quân 3 tháng",
        "transaction_name": "FN_LAY_DS_KH_UDF_LOV",
        "transaction_value": []
    }
]
GW_CATEGORY_EXAMPLES = {}
for category in GW_CATEGORIES:
    category_name = category["category_name"]
    transaction_name = category["transaction_name"]
    transaction_value = category["transaction_value"]
    GW_CATEGORY_EXAMPLES.update({
        category_name: {
            "summary": category_name,
            "description": category_name,
            "value": {
                "transaction_name": transaction_name,
                "transaction_value": transaction_value
            }
        }
    })
