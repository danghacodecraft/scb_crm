import os

ORACLE_CONFIG = {
    "host": os.getenv("ORACLE_HOST"),
    "port": os.getenv("ORACLE_PORT"),
    "username": os.getenv("ORACLE_USERNAME"),
    "password": os.getenv("ORACLE_PASSWORD"),
    "service_name": os.getenv("ORACLE_SERVICE_NAME")
}

#
# ORACLE_CONFIG_TASK = {
#     "host": os.getenv("ORACLE_TASK_HOST"),
#     "port": os.getenv("ORACLE_TASK_PORT"),
#     "username": os.getenv("ORACLE_TASK_USERNAME"),
#     "password": os.getenv("ORACLE_TASK_PASSWORD"),
#     "service_name": os.getenv("ORACLE_TASK_SERVICE_NAME")
# }
