REDEEM_ACCOUNT_REQUEST_EXAMPLE = {
    "account_info": {
        "account_num": "123456789101"
    },
    "p_payout_detail": {
        "redemption_details": {
            "redemption_mode": "Y",
            "redemption_amount": 10000000,
            "waive_penalty": "N",
            "waive_interest": "N"
        },
        "payout_details": [
            {
                "payout_component": "P",
                "payout_mode": "S",
                "payout_amount": 10000000,
                "offset_account": "16742131993"
            },
            {
                "payout_component": "I",
                "payout_mode": "S",
                "payout_amount": 0,
                "offset_account": "16742131993"
            }
        ]
    }
}
