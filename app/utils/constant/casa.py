ACCOUNT_ALLOW_NUMBER_LENGTH = [0, 8, 10, 11, 12, 16]

CASA_ACCOUNT_STATUS_APPROVED = 1
CASA_ACCOUNT_STATUS_UNAPPROVED = 0

RECEIVING_METHOD_SCB_TO_ACCOUNT = 'SCB_TO_ACCOUNT'
RECEIVING_METHOD_SCB_BY_IDENTITY = 'SCB_BY_IDENTITY'
RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT = 'THIRD_PARTY_TO_ACCOUNT'
RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY = 'THIRD_PARTY_BY_IDENTITY'
RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT = 'THIRD_PARTY_247_TO_ACCOUNT'
RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD = 'THIRD_PARTY_247_TO_CARD'

RECEIVING_METHODS = {
    RECEIVING_METHOD_SCB_TO_ACCOUNT: "Trong SCB đến tài khoản",
    RECEIVING_METHOD_SCB_BY_IDENTITY: "Trong SCB nhận bằng giấy tờ định danh",
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT: "Ngoài SCB đến tài khoản",
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY: "Ngoài SCB nhận bằng giấy tờ định danh",
    RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT: "Ngoài SCB 24/7 tài khoản",
    RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD: "Ngoài SCB 24/7 số thẻ"
}

RECEIVING_METHOD_SCB = "Trong hệ thống"
RECEIVING_METHOD_THIRD_PARTY = "Ngoài hệ thống"
RECEIVING_METHOD__METHOD_TYPES = {
    RECEIVING_METHOD_SCB_TO_ACCOUNT: RECEIVING_METHOD_SCB,
    RECEIVING_METHOD_SCB_BY_IDENTITY: RECEIVING_METHOD_SCB,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT: RECEIVING_METHOD_THIRD_PARTY,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY: RECEIVING_METHOD_THIRD_PARTY,
    RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT: RECEIVING_METHOD_THIRD_PARTY,
    RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD: RECEIVING_METHOD_THIRD_PARTY
}

DENOMINATIONS_FIVE_HUNDRED_THOUSAND = "500000"
DENOMINATIONS_TWO_HUNDRED_THOUSAND = "200000"
DENOMINATIONS_ONE_HUNDRED_THOUSAND = "100000"
DENOMINATIONS_FIFTY_THOUSAND = "50000"
DENOMINATIONS_TWENTY_THOUSAND = "20000"
DENOMINATIONS_TEN_THOUSAND = "10000"
DENOMINATIONS_FIVE_THOUSAND = "5000"
DENOMINATIONS_TWO_THOUSAND = "2000"
DENOMINATIONS_ONE_THOUSAND = "1000"
DENOMINATIONS_FIVE_HUNDRED = "500"

DENOMINATIONS__AMOUNTS = {
    DENOMINATIONS_FIVE_HUNDRED_THOUSAND: 0,
    DENOMINATIONS_TWO_HUNDRED_THOUSAND: 0,
    DENOMINATIONS_ONE_HUNDRED_THOUSAND: 0,
    DENOMINATIONS_FIFTY_THOUSAND: 0,
    DENOMINATIONS_TWENTY_THOUSAND: 0,
    DENOMINATIONS_TEN_THOUSAND: 0,
    DENOMINATIONS_FIVE_THOUSAND: 0,
    DENOMINATIONS_TWO_THOUSAND: 0,
    DENOMINATIONS_ONE_THOUSAND: 0,
    DENOMINATIONS_FIVE_HUNDRED: 0
}
