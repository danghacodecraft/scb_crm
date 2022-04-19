from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings.database import ORACLE_CONFIG, ORACLE_CONFIG_TASK

DATABASE_URL = "oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}".format_map({
    'host': ORACLE_CONFIG['host'],
    'port': ORACLE_CONFIG['port'],
    'username': ORACLE_CONFIG['username'],
    'password': ORACLE_CONFIG['password'],
    'service_name': ORACLE_CONFIG['service_name']
})

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DATABASE_URL_TASK = "oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}".format_map({
    'host': ORACLE_CONFIG_TASK['host'],
    'port': ORACLE_CONFIG_TASK['port'],
    'username': ORACLE_CONFIG_TASK['username'],
    'password': ORACLE_CONFIG_TASK['password'],
    'service_name': ORACLE_CONFIG_TASK['service_name']
})

engine_task = create_engine(DATABASE_URL_TASK)
SessionLocal_Task = sessionmaker(autocommit=False, autoflush=False, bind=engine_task)
metadata = MetaData(schema=ORACLE_CONFIG['service_name'])
Base = declarative_base(metadata=metadata)
# metadata = Base.metadata
