from sqlalchemy import CLOB, VARCHAR, Column, DateTime, text, DATE
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class EKYCCustomer(Base):
    __tablename__ = 'crm_ekyc_customer'

    id = Column(NUMBER, primary_key=True)
    customer_id = Column(VARCHAR(100), nullable=True)
    document_id = Column(VARCHAR(12), nullable=False)
    document_type = Column(NUMBER(2), nullable=False)
    date_of_issue = Column(DATE, nullable=False)
    place_of_issue = Column(VARCHAR(1000), nullable=False)
    qr_code_data = Column(VARCHAR(1000), nullable=False)
    full_name = Column(VARCHAR(1000), nullable=False)
    date_of_birth = Column(DATE, nullable=False)
    gender = Column(VARCHAR(1), nullable=False)
    place_of_residence = Column(VARCHAR(1000), nullable=False)
    place_of_origin = Column(VARCHAR(1000), nullable=False)
    nationality = Column(VARCHAR(500), nullable=False)
    address_1 = Column(VARCHAR(1000), nullable=False)
    address_2 = Column(VARCHAR(1000), nullable=False)
    address_3 = Column(VARCHAR(1000), nullable=False)
    address_4 = Column(VARCHAR(1000), nullable=False)
    phone_number = Column(VARCHAR(12), nullable=False)
    ocr_data = Column(CLOB, nullable=False)
    extra_info = Column(CLOB, nullable=True)
    receive_ads = Column(NUMBER(1), nullable=False)
    longitude = Column(NUMBER, nullable=True)
    latitude = Column(NUMBER, nullable=True)
    user = Column(VARCHAR(500), nullable=False)
    cif = Column(VARCHAR(500), nullable=False)
    account_number = Column(VARCHAR(100), nullable=False)
    ekyc_step_info = Column(CLOB, nullable=False)
    job_title = Column(VARCHAR(100), nullable=False)
    organization = Column(VARCHAR(500), nullable=False)
    organization_address = Column(VARCHAR(1000), nullable=False)
    organization_phone_number = Column(VARCHAR(100), nullable=False)
    position = Column(VARCHAR(500), nullable=False)
    salary_range = Column(VARCHAR(100), nullable=False)
    tax_number = Column(VARCHAR(10), nullable=False)
    created_date = Column(DATE, nullable=True)
    faces_matching_percent = Column(NUMBER, nullable=True)
    ocr_data_errors = Column(CLOB, nullable=False)
    permanent_address = Column(CLOB, nullable=False)
    transaction_id = Column(VARCHAR(100), nullable=True)
    delete_flag = Column(NUMBER(1), nullable=True)
    open_biometric = Column(NUMBER(1), nullable=True)
    date_of_expiry = Column(DATE, nullable=True)


class EKYCCustomerStep(Base):
    __tablename__ = 'crm_ekyc_customer_step'
    id = Column(NUMBER, primary_key=True)
    step = Column(VARCHAR(50), nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    step_status = Column(VARCHAR(100), nullable=False)
    update_at = Column(DATE, nullable=True)
    reason = Column(VARCHAR(500), nullable=True)
    customer_id = Column(VARCHAR(100), nullable=False)
    transaction_id = Column(VARCHAR(100), nullable=True)
