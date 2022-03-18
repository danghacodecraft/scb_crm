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
    },
    "idm": {
        "host": "http://192.168.73.135:9006",
        "secret_key": "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        "algorithm": "HS256",
        "access_token_expire_minutes": 60 * 24,
        "headers": {
            'Content-Type': 'application/json'
        },
        "my_service": "CRM"

    }
}
