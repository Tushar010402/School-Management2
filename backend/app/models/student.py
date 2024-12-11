from enum import Enum
from sqlalchemy import Integer, String, Date, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql.schema import Column
from app.models.base import BaseModel

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"

class Student(BaseModel):
    __tablename__ = "students"

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    admission_number = Column(String, unique=True, index=True)
    admission_date = Column(Date, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    blood_group = Column(SQLEnum(BloodGroup))
    address = Column(String, nullable=False)
    phone = Column(String)
    emergency_contact = Column(String, nullable=False)
    medical_conditions = Column(String)
    previous_school = Column(String)
    is_active = Column(Boolean, default=True)

class Guardian(BaseModel):
    __tablename__ = "guardians"

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    relationship = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    occupation = Column(String)
    phone = Column(String, nullable=False)
    email = Column(String)
    address = Column(String)
    is_emergency_contact = Column(Boolean, default=False)
    is_authorized_pickup = Column(Boolean, default=False)

class StudentDocument(BaseModel):
    __tablename__ = "student_documents"

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    
    document_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(Date)

class StudentNote(BaseModel):
    __tablename__ = "student_notes"

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    note_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_confidential = Column(Boolean, default=False)