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
        'otp': os.getenv('SERVICE_EKYC_OTP'),
        'token': os.getenv('SERVICE_EKYC_BEARER_TOKEN'),
        'server-auth': os.getenv('SERVICE_EKYC_SERVER_TOKEN')
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
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("SERVICE_IDM_BEARER_TOKEN")}'
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
    },
    "kafka": {
        "sasl_mechanism": os.getenv("KAFKA_SASL_MECHANISM"),
        "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        "security_protocol": os.getenv("KAFKA_SECURITY_PROTOCOL"),
        "sasl_plain_username": os.getenv("KAFKA_SASL_PLAIN_USERNAME"),
        "sasl_plain_password": os.getenv("KAFKA_SASL_PLAIN_PASSWORD"),
        "producer_topic": os.getenv("KAFKA_PRODUCER_TOPIC"),
        "message_max_bytes": os.getenv("KAFKA_MESSAGE_MAX_BYTES"),
    }
}
