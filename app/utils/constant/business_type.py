BUSINESS_TYPE_INIT_CIF = "CIF"
BUSINESS_TYPE_EKYC_AUDIT = "KSS_EKYC"
BUSINESS_TYPE_OPEN_CASA = "OPEN_CASA"
BUSINESS_TYPE_CLOSE_CASA = "CLOSE_CASA"
BUSINESS_TYPE_WITHDRAW = "WITHDRAW"
BUSINESS_TYPE_TD_ACCOUNT_OPEN_ACCOUNT = "OPEN_TD_ACCOUNT"
BUSINESS_TYPE_AMOUNT_BLOCK = "AMOUNT_BLOCK"
BUSINESS_TYPE_AMOUNT_UNBLOCK = "AMOUNT_UNBLOCK"
BUSINESS_TYPE_REDEEM_ACCOUNT = "REDEEM_ACCOUNT"
BUSINESS_TYPE_CASA_TOP_UP = "CASA_TOP_UP"

BUSINESS_TYPES = {
    BUSINESS_TYPE_INIT_CIF: "Mở CIF",
    BUSINESS_TYPE_OPEN_CASA: "Mở mới tài khoản thanh toán",
    BUSINESS_TYPE_CLOSE_CASA: "Đóng tài khoản thanh toán",
    BUSINESS_TYPE_WITHDRAW: "Rút tiền từ tài khoản thanh toán",
    BUSINESS_TYPE_EKYC_AUDIT: "Kiểm soát sau EKYC",
    BUSINESS_TYPE_AMOUNT_BLOCK: "Phong tỏa tài khoản",
    BUSINESS_TYPE_AMOUNT_UNBLOCK: "Giải tỏa tài khoản",
    BUSINESS_TYPE_REDEEM_ACCOUNT: "Tất toán tài khoản",
    BUSINESS_TYPE_CASA_TOP_UP: "Nộp tiền mặt vào tài khoản thanh toán",
    BUSINESS_TYPE_TD_ACCOUNT_OPEN_ACCOUNT: "Mở mới tài khoản tiết kiệm"
}

# Những business type không cần dùng cif
BUSINESS_TYPE_NO_CIFS = [
    BUSINESS_TYPE_CASA_TOP_UP
]
