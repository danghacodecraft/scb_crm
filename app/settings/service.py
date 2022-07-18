import os

SERVICE = {
    "file": {
        "url": os.getenv("SERVICE_FILE_URL"),
        "server-auth": os.getenv("SERVICE_FILE_SERVICE_AUTH"),
        "authorization": "bearer 3",
        "service_file_cdn": os.getenv("SERVICE_FILE_CDN")
    },
    "file-upload": {
        "file_limit": int(os.getenv("FILE_LIMIT", 10)),
        "file_size_max": int(os.getenv("FILE_SIZE_MAX", 5000000))
    },
    "ekyc": {
        "url": os.getenv("SERVICE_EKYC_URL"),
        "x-transaction-id": "CRM_TEST",
        "authorization": f"bearer {os.getenv('SERVICE_EKYC_BEARER_TOKEN')}",
        'otp': os.getenv('OTP_EKYC', 'scbmnv9271q5a2Aa224')
    },
    "template": {
        "url": os.getenv("SERVICE_TEMPLATE_URL"),
        "server-auth": os.getenv("SERVICE_TEMPLATE_SERVICE_AUTH")
    },
    "card": {
        "url": os.getenv("SERVICE_CARD_URL"),
        "authorization": f"bearer {os.getenv('SERVICE_CARD_BEARER_TOKEN')}",
        "x-transaction-id": "CRM_TEST"
    },
    "idm": {
        "host": os.getenv("SERVICE_IDM_URL"),
        "headers": {
            'Content-Type': 'application/json'
        },
        "my_service": "CRM"

    },
    "tms": {
        "url": os.getenv("SERVICE_TEMPLATE_URL"),
        "headers": {
            'Content-Type': 'application/json',
            "server-auth": "BCQjyTXFB0TWJiLjKcuzAenpYsbXV5O0",
            "authorization": "Bearer 1"
        }
    },
    "dwh": {
        "url": os.getenv("SERVICE_DWH_URL"),
        "headers": {
            'Content-Type': 'application/json',
            "server-auth": os.getenv("SERVICE_DWH_SERVER_AUTH")
        }
    },
    "gw": {
        "url": os.getenv("SERVICE_GW_URL"),
        "bypass": bool(os.getenv("SERVICE_GW_BYPASS", "") if os.getenv("SERVICE_GW_BYPASS", "") in ["True", "true", "1"] else False)
    }
}
