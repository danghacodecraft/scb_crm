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
    "soa": {
        "url": os.getenv("SERVICE_SOA_URL"),
        "authorization_username": "crm",
        "authorization_password": "123456"
    }
}
